"""Module 1: frozen CLIP embeddings, cosine ranking, and top-1 evaluation."""

import argparse
import json
from pathlib import Path

import torch
import torch.nn.functional as F
from PIL import Image, ImageOps
from transformers import CLIPModel, CLIPProcessor

ROOT = Path(__file__).resolve().parent
MODEL_ID = "openai/clip-vit-base-patch32"
MODEL_REVISION = "3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268"


def read_inputs(image_dir, queries_file, query):
    """Read candidate filenames and labels before loading the model."""
    extensions = {".jpg", ".jpeg", ".png"}
    images = sorted(
        p for p in image_dir.iterdir()
        if p.suffix.lower() in extensions and p.is_file()
    )
    if not images:
        raise ValueError(f"No JPG or PNG images in {image_dir}")
    if query is not None:
        if not query.strip():
            raise ValueError("The query must not be empty.")
        return images, [{"query": query}]

    examples = json.loads(queries_file.read_text())
    if not isinstance(examples, list) or not examples:
        raise ValueError("The queries file must contain a nonempty JSON list.")
    names = {p.name for p in images}
    for example in examples:
        if (not isinstance(example, dict)
                or not isinstance(example.get("query"), str)
                or not example["query"].strip()):
            raise ValueError("Every example needs a nonempty 'query' string.")
        if not isinstance(example.get("target"), str) or example["target"] not in names:
            raise ValueError(f"Target must name an image in the candidate folder: {example}")
    return images, examples


def encode_images(model, processor, image_paths, device):
    """Encode each image once; keep only small, normalized vectors on CPU."""
    features = []
    for path in image_paths:
        with Image.open(path) as image:
            image = ImageOps.exif_transpose(image).convert("RGB")
            inputs = processor(images=image, return_tensors="pt").to(device)
        vector = model.get_image_features(**inputs)
        features.append(F.normalize(vector.float().cpu(), dim=-1))
    return torch.cat(features)  # Shape: [number of images, 512].


def rank_images(model, processor, image_features, query, device):
    """Return image indices from highest to lowest cosine similarity."""
    inputs = processor(text=[query], return_tensors="pt", padding=True)
    if inputs.input_ids.shape[1] > model.config.text_config.max_position_embeddings:
        raise ValueError("CLIP accepts at most 77 tokens, including special tokens. Shorten the query.")
    vector = model.get_text_features(**inputs.to(device))
    vector = F.normalize(vector.float().cpu(), dim=-1)
    scores = (vector @ image_features.T).squeeze(0)
    # For exact ties, keep filename order so results are reproducible.
    order = torch.argsort(scores, descending=True, stable=True).tolist()
    return order, scores.tolist()


@torch.inference_mode()
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images", type=Path, default=ROOT / "practice/images")
    parser.add_argument("--queries", type=Path, default=ROOT / "practice/queries.json")
    parser.add_argument("--query", help="Search with your own text instead of evaluating the labels.")
    parser.add_argument("--device", choices=["cpu", "mps"], default="cpu")
    parser.add_argument("--output", type=Path, default=ROOT / "results/last_run.json")
    parser.add_argument("--cache-dir", type=Path, default=ROOT / "cache")
    args = parser.parse_args()
    try:
        image_paths, examples = read_inputs(args.images, args.queries, args.query)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    if args.device == "mps" and not torch.backends.mps.is_available():
        parser.error("Apple GPU (MPS) is unavailable here. Run with --device cpu.")

    print(f"Loading {MODEL_ID} on {args.device}. The first run downloads the weights.", flush=True)
    # A local cache avoids downloading the model again on subsequent runs.
    options = {"revision": MODEL_REVISION, "cache_dir": args.cache_dir}
    processor = CLIPProcessor.from_pretrained(MODEL_ID, use_fast=False, **options)
    model = CLIPModel.from_pretrained(MODEL_ID, **options).to(args.device).eval()
    image_features = encode_images(model, processor, image_paths, args.device)
    names = [p.name for p in image_paths]

    results = []
    for example in examples:
        order, scores = rank_images(model, processor, image_features, example["query"], args.device)
        ranking = [{"image": names[i], "cosine_similarity": scores[i]} for i in order]
        result = {"query": example["query"], "ranking": ranking}
        print(f"\nQuery: {example['query']}")
        for rank, item in enumerate(ranking[:3], start=1):
            print(f"  {rank}. {item['image']}  cosine={item['cosine_similarity']:.4f}")
        if "target" in example:
            target_rank = [names[i] for i in order].index(example["target"]) + 1
            result.update(target=example["target"], target_rank=target_rank)
            print(f"  Expected: {example['target']} | rank: {target_rank}")
        results.append(result)

    report = {
        "model": MODEL_ID,
        "revision": MODEL_REVISION,
        "device": args.device,
        "candidate_count": len(names),
        "results": results,
    }
    if args.query is None:
        correct = sum(result["target_rank"] == 1 for result in results)
        report["top1_accuracy"] = correct / len(results)
        print(f"\nTop-1 accuracy (single-target Recall@1): {correct}/{len(results)} = {correct / len(results):.1%}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Saved full rankings: {args.output}")


if __name__ == "__main__":
    main()
