### More Spatial Examples

Nine fixed photo pairs: seven new comparisons and two previously inspected examples. Each pair contains one image matching the query and one distractor. CLIP ViT-B/32 is unchanged; the runner imports the existing baseline functions.

## Results

On the seven new pairs, both the original captions and the more explicit descriptions selected the correct image in **3/7 cases**. No winner changed with the explicit wording. The two previous examples scored 1/2 in both conditions and are reported separately.

| Pair | Original caption | Explicit description | Original margin | Explicit margin |
|---|---|---|---:|---:|
| laptop_1 | Incorrect | Incorrect | -0.04039 | -0.05802 |
| laptop_2 | Incorrect | Incorrect | -0.00227 | -0.01924 |
| laptop_3 | Incorrect | Incorrect | -0.00363 | -0.03059 |
| laptop_under_cat | Correct | Correct | +0.01249 | +0.01795 |
| apple_banana | Incorrect | Incorrect | -0.01735 | -0.01276 |
| cat_fridge | Correct | Correct | +0.05446 | +0.02696 |
| cat_glass | Correct | Correct | +0.03787 | +0.04624 |
| original_laptop (previous) | Incorrect | Incorrect | -0.00044 | -0.01210 |
| original_car (previous) | Correct | Correct | +0.04683 | +0.04051 |

The margin is the correct image’s cosine score minus the distractor’s score. A negative margin means CLIP preferred the distractor. It is not a probability or a statistical confidence interval. Exact ties would be reported separately and not counted as correct; there were none.

## Interpretation

The three new cat-on-laptop pairs all failed. Two use closed laptops; one uses an open laptop. All three share the same cat-beside-laptop distractor, so these are related comparisons, not three independent demonstrations. The apple-on-banana pair also failed.

CLIP succeeded on the laptop-under-cat pair with a different distractor, the cat-on-refrigerator pair, and the cat-behind-wine-glass pair. These results support investigating errors involving object relationships. They do not establish that CLIP only uses 2D positions or lacks all depth information.

Explicit physical wording did not fix the failures in this set. Differences in object visibility, framing, background, word choice, and CLIP’s training distribution remain possible explanations. Even a correct selection can be driven by visual shortcuts.

## How the examples were chosen

- Source: VSR random development annotations and their COCO photographs. Original true/false labels and row numbers are retained in `data/manifests/03_query_wording.json`.
- Cases and both query wordings were written to `cases.json` before scoring. This was one run, with no selection or prompt changes based on its scores.
- Full photos and CLIP’s centre crops were visually inspected. Both named objects needed to remain visible and the source label needed to look reasonable. This is one reviewer’s screening, not independently validated annotation.
- `screening.json` records rejected pairs. Several false captions referred to an object that was absent or unclear, making them unsuitable for this check.
- There are 15 unique photos across all nine pairs, including the previous examples. The three new cat-on-laptop comparisons reuse one previous distractor.
- Each query ranks only its two assigned candidates. This differs from ranking all four or six images in the earlier exercises.
- The set was chosen to inspect a suspected failure, not randomly sampled. It is development data, not a held-out benchmark.
- Image-plane positions and visual appearance are not experimentally matched across the photographs. A stronger causal test would control those factors and use more independent pairs.

## Run

From the repository root, using the existing environment:

```bash
python -m retrieval.download --experiment 03_query_wording
python -m retrieval.evaluate --experiment 03_query_wording
```

Use `--cache-dir` to reuse a model cache elsewhere. The default is CPU. The model encodes each photo once, then reuses the embeddings across the fixed pairs and wordings. Results are written to `experiments/03_query_wording/results/latest.json`. The checked run is in `example_run.json`.

The cases and manifest checksums are saved in each result. Photos and review sheets are ignored by Git; the downloader retrieves exactly the files listed in the manifest and checks their hashes.

## Inspect the photos

The locally generated review sheets place the expected matching image on the left and the distractor on the right. Labels on these sheets are for human inspection only; the model receives individual unlabelled photographs.

[Laptop pairs](review_0.jpg) · [Other new pairs](review_4.jpg)

## Sources

[Visual Spatial Reasoning](https://github.com/cambridgeltl/visual-spatial-reasoning), Fangyu Liu, Guy Edward Toh Emerson and Nigel Collier, TACL 2023. The captions and labels come from `data/splits/random/dev.jsonl`. `VSR_LICENSE.txt` retains the source license. This is an adapted paired-retrieval exercise, not the official VSR benchmark.

Images are from COCO 2017. Their original IDs, URLs and checksums are retained; image rights remain with the original photographers. VSR’s repository license does not replace individual photo licenses.

## Repository layout

Paths in commands are relative to the repository root. Shared code is in `retrieval/`; downloaded photos are in `data/images/`. Recorded `example_run.json` files are preserved unchanged. Fresh runs go to this experiment’s ignored `results/` directory.
