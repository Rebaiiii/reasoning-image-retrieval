### Module 2: A Small Spatial Dataset

Four COCO photographs and two queries for inspecting spatial retrieval. The
photos were selected from the VSR random development split and checked visually
before running CLIP. These photos are used to explore the problem, not as a separate final test.

## Examples

| Query | Correct image | Similar but incorrect image |
|---|---|---|
| The cat is on top of the laptop. | 000000107664.jpg | 000000018903.jpg |
| The cat is under the car. | 000000230224.jpg | 000000000650.jpg |

The first pair contains a cat on a laptop and a cat beside a laptop. The second
contains a cat under a car and a cat on its roof. Each query searches all four
images, with one labelled answer among these four photos.

An incorrect image containing the same objects is called a **hard negative**.
It helps check whether CLIP can tell the relationships apart. The photos also
differ in other ways, so a correct answer does not prove that CLIP understood the relationship.

## Files

- `data/manifests/02_spatial_examples.json`: image URLs, checksums, original VSR labels, and source row numbers.
- `queries.json`: the two positive captions and their correct image filenames.
- `retrieval/download.py`: shared image downloader; no model is loaded.
- `example_run.json`: the recorded baseline output for this exact candidate set.

A VSR label of 0 means the caption is false for that image. It does not mean the
image should be removed: that photo can be a useful distractor. Labels are used
for evaluation only; CLIP receives the image pixels and query text.

## How to Run

With the Module 1 environment activated, run from the main project folder:

```bash
python -m retrieval.download --experiment 02_spatial_examples
python -m retrieval.evaluate --experiment 02_spatial_examples
```

The images are already downloaded in the local project. The download command
checks existing files and avoids downloading them again. The image files are
ignored by Git; a fresh checkout retrieves them using the manifest.

The retrieval code is unchanged. Only the image folder and query labels differ
from Module 1. Compare each query's target rank, not the overall percentage with
the earlier six-shape exercise: the candidate images and queries are different.

## Recorded Run

The CPU baseline retrieved the correct image for 1 of 2 queries. For the laptop
query it placed the cat beside the laptop first (0.3044), just above the cat on
the laptop (0.3039). The car query ranked the correct image first. These are
cosine similarity scores, which measure how closely the image and text match; they are not probabilities. Small device differences may affect
close rankings. The examples were selected before observing these scores.

## Review

1. Open the four photos and identify each target before looking at the scores.
2. Find the hard negative for each query. Explain why it is incorrect.
3. Read the full ranking for one query in `example_run.json`.

Two queries are deliberately small enough to inspect individually. Their score
are not enough for a broad research claim. They are development examples and must
not later be described as an new, unseen test set. Adding a photo also requires
checking whether it becomes another valid answer to an existing query.

Before expanding the dataset, inspect CLIP's centre crop: important objects can
disappear in non-square photographs. These four photos were reviewed both in
full and after the baseline processor's crop.

## Sources

Annotations: [Visual Spatial Reasoning](https://github.com/cambridgeltl/visual-spatial-reasoning),
Fangyu Liu, Guy Edward Toh Emerson and Nigel Collier, TACL 2023.
Selected from `data/splits/random/dev.jsonl`; row numbers are zero-based.
The original captions and labels are saved in the manifest. VSR is a
true/false caption benchmark; this small retrieval exercise adapts those labels
and is not an official VSR evaluation.

Photos: COCO 2017, downloaded from its public S3 bucket. Image IDs and exact
download URLs are in the manifest. Original image rights remain with the
photographers; VSR's Apache-2.0 license covers its repository, not all COCO photos.
The VSR license is included as `VSR_LICENSE.txt`.

Qwen reranking is reserved for a later module.

## File locations

Run commands from the main project folder. Shared code is in `retrieval/`, and downloaded photos are in `data/images/`. Saved results stay in `example_run.json`. New runs go to this experiment’s `results/` folder, which Git ignores.
