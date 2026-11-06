# 100-Pair Spatial Retrieval Test

This test uses CLIP ViT-B/32 on 100 photo pairs. Each pair has two queries with different expected answers. Each query ranks only the two photos in its pair, not the full collection.

For example, one query asks for a cat in front of a laptop; the other asks for a cat behind a laptop. The expected answer changes. The test checks whether CLIP switches to the right photo.

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

## What the results show

CLIP often chose the same photo when the relationship changed. Left/right queries also had errors. The problem is not limited to depth-related queries in this set.

This does not show that CLIP ignores depth. The photos differ in viewpoint, background, visibility and appearance. Its scores may respond to the relation without changing the winning image. To test the cause, new photos would need to keep the camera and objects the same while changing their positions.

## How the pairs were chosen

- The captions come from VSR's random train and development sets. Both captions in a pair name the same objects, but use different relationships. VSR marks each caption as true for its own photo.
- The set has 200 different image filenames and file hashes. No photo is reused between pairs. Earlier reviewed photos were left out. Some photos still show similar scenes or the same types of objects.
- The selection uses random seed 20261105 and fixed group sizes: 40 front/behind, 25 left/right, 20 on top/inside, and 15 on/under pairs. These chosen group sizes mean the set does not represent all possible spatial queries.
- The pairs were saved before running CLIP. An AI review of the full photos marked 43 pairs as unclear. The reasons are in `audit.json`. All 100 pairs stayed in the full result.
- At the time of this run, the other 57 pairs had only passed the AI review. They had not been checked by a person. The cropped images seen by CLIP were not checked separately in this run.
- VSR marks each caption as true for its own photo. This test assumes it is false for the other photo in the pair; VSR does not supply that second label here. Both descriptions can sometimes fit a photo. Words such as “in front of” can also depend on the viewpoint.

The model is unchanged: frozen CLIP ViT-B/32 on CPU, one photo encoded at a time, with the existing baseline's preprocessing and cosine ranking. No training or reranking was added.

## Run

From the main project folder, with the existing Python environment active:

```bash
python -m retrieval.download --experiment 05_relation_switch_100
python -m retrieval.evaluate --experiment 05_relation_switch_100
```

Add `--cache-dir /path/to/existing/cache` to reuse the downloaded model. Results go to `experiments/05_relation_switch_100/results/latest.json`. The recorded run is `example_run.json`, including every score and hashes of the cases, manifest and pre-score audit.

`cases.json` fixes the queries and candidate pairs. `data/manifests/05_relation_switch_100.json` records image sources and checksums. `provenance.json` records source annotation hashes, selection rules and exclusions. Local review sheets are in `reviews/`; photos and sheets are excluded from Git.

## Source

The captions and COCO photo links come from [Visual Spatial Reasoning](https://github.com/cambridgeltl/visual-spatial-reasoning). This paired retrieval test is not the official VSR evaluation. VSR's repository license is saved in `VSR_LICENSE.txt`; the photo rights stay with their owners.

## File locations

Run commands from the main project folder. Shared code is in `retrieval/`, and downloaded photos are in `data/images/`. Saved results stay in `example_run.json`. New runs go to this experiment’s `results/` folder, which Git ignores.
