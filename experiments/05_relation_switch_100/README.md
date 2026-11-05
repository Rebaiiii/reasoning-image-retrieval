# 100-Pair Spatial Retrieval Test

I tested CLIP ViT-B/32 on 100 photo pairs, with two opposing queries per pair. Each query ranks only the two photos in its pair, not the full collection.

For example, one query asks for a cat in front of a laptop; the other asks for a cat behind a laptop. The expected answer changes. I check whether CLIP changes its choice correctly.

## Results

| Measure | All 100 pairs | 57 unflagged pairs |
|---|---:|---:|
| Correct queries | 109/200 (54.5%) | 66/114 (57.9%) |
| Both queries correct | 13/100 (13.0%) | 10/57 (17.5%) |
| Same image for both queries | 83/100 (83.0%) | 46/57 (80.7%) |
| Switched, but both wrong | 4/100 | 1/57 |

There were no exact score ties. Choosing the same image for both opposing queries gives one correct answer out of two, so query accuracy alone hides the main failure pattern.

| Relationship | All: correct queries | All: both correct | Unflagged: correct queries | Unflagged: both correct |
|---|---:|---:|---:|---:|
| In front of / behind | 44/80 | 4/40 | 21/38 | 2/19 |
| Left / right | 24/50 | 3/25 | 18/32 | 3/16 |
| On top / inside | 24/40 | 4/20 | 14/22 | 3/11 |
| On / under | 17/30 | 2/15 | 13/22 | 2/11 |

## What I take from this

CLIP often kept the same preferred photo when the spatial relationship changed. That makes relationship sensitivity worth investigating further. Horizontal relationships also had errors, so these results do not isolate a specifically 3D problem.

This does not show that CLIP ignores depth. The photos differ in viewpoint, background, visibility and appearance. Its scores may respond to the relation without changing the winning image. I would need controlled scenes to separate image-plane position from physical depth or support.

## How I built the test

- I used positive captions from VSR's random train and development splits, matching the subject and object text across opposing relationships.
- The set has 200 distinct image filenames and 200 distinct file hashes. No photo is reused between pairs, and earlier inspected photos are excluded. Similar scenes and repeated object categories can still be correlated.
- I used seed 20261105 and fixed quotas: 40 depth, 25 horizontal, 20 support/containment, and 15 support/vertical pairs. This is a quota-selected exploratory set, not a representative random benchmark sample.
- I froze the pairs before scoring. AI-assisted visual screening of full-image contact sheets flagged 43 pairs before inference. Reasons are in `audit.json`; none were removed from the full result.
- The 57 unflagged pairs are provisional, not independently human-validated labels. CLIP's center crops were not separately audited in this run.
- Each caption is positive for its own photo in VSR. Treating it as negative for the other photo is an inference made for this experiment. Some relationships overlap or depend on the reference frame.

The model is unchanged: frozen CLIP ViT-B/32 on CPU, one photo encoded at a time, with the existing baseline's preprocessing and cosine ranking. No training or reranking was added.

## Run

From the repository root, with the existing Python environment active:

```bash
python -m retrieval.download --experiment 05_relation_switch_100
python -m retrieval.evaluate --experiment 05_relation_switch_100
```

Add `--cache-dir /path/to/existing/cache` to reuse the downloaded model. Results go to `experiments/05_relation_switch_100/results/latest.json`. The recorded run is `example_run.json`, including every score and hashes of the cases, manifest and pre-score audit.

`cases.json` fixes the queries and candidate pairs. `data/manifests/05_relation_switch_100.json` records image sources and checksums. `provenance.json` records source annotation hashes, selection rules and exclusions. Local review sheets are in `reviews/`; photos and sheets are excluded from Git.

## Source

I adapted captions and COCO photos referenced by [Visual Spatial Reasoning](https://github.com/cambridgeltl/visual-spatial-reasoning). This paired retrieval test is not the official VSR evaluation. VSR's repository license is retained in `VSR_LICENSE.txt`; the underlying photographs retain their own rights.

## Repository layout

Paths in commands are relative to the repository root. Shared code is in `retrieval/`; downloaded photos are in `data/images/`. Recorded `example_run.json` files are preserved unchanged. Fresh runs go to this experiment’s ignored `results/` directory.
