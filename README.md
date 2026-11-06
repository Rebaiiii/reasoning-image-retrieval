# Reasoning-Based Image Retrieval

This project tests whether CLIP can find images from descriptions such as a cat **on** a laptop or a cat **beside** it.

The starting model is CLIP ViT-B/32, used without extra training. It runs on CPU, one image at a time, on an M1 MacBook with 8 GB RAM. A later step will use Qwen to check and reorder CLIP’s results.

## Current results

The 100-pair test uses two descriptions per pair, each with a different expected photo. CLIP answered **109/200 queries correctly** and selected the same photo for both queries in **83/100 pairs**.

A review of the photos marked 43 pairs as unclear before running CLIP. For the other 57 pairs, CLIP got **66/114** answers right and both answers right in **10/57 pairs**. This early test does not prove that CLIP cannot understand depth. [Read the experiment and limitations](experiments/05_relation_switch_100/README.md).

## Setup

Run from the main project folder with Python 3.10–3.12:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python baseline.py
```

The first run downloads the model weights (about 605 MB). Later runs reuse `cache/`. The six generated practice images check that the code works. They are too simple to measure performance on real photos.

```bash
python baseline.py --query "A red circle to the left of a blue square."
```

## Run an experiment again

```bash
python -m retrieval.download --experiment 05_relation_switch_100
python -m retrieval.evaluate --experiment 05_relation_switch_100
```

The downloader uses file hashes to check that the photos match the saved copies. Each test uses only its listed photos, even if other photos have been downloaded. Add `--cache-dir /path/to/existing/cache` to reuse a cache elsewhere.

New output goes to the experiment’s `results/latest.json`. Recorded `example_run.json` files remain unchanged. The test code saves image order, scores and file hashes. The saved fields are explained in [the experiment guide](experiments/README.md).

## Project layout

```text
retrieval/             Shared model, download and test code
experiments/           Saved questions, review notes and results
data/manifests/        Photo links, source labels and file hashes
data/images/           Downloaded photos (ignored by Git)
practice/              Original generated examples
tests/                 Checks for the test code
baseline.py            Original baseline command
```

## Experiments

| Experiment | Question |
|---|---|
| [01 — Baseline](experiments/01_baseline/README.md) | Does the search code work? |
| [02 — Spatial examples](experiments/02_spatial_examples/README.md) | Can it find the right photo among four choices? |
| [03 — Query wording](experiments/03_query_wording/README.md) | Does clearer wording change the answer? |
| [04 — Relation switch](experiments/04_relation_switch/README.md) | Does changing the relationship change the selected photo? |
| [05 — 100-pair relation switch](experiments/05_relation_switch_100/README.md) | Does the same problem appear in more examples? |

The folder numbers show the order of the tests. Some tests reuse earlier photos. Each folder lists its data sources and photo rights. Downloaded COCO photos are not included in Git.

## Checks

```bash
python -m unittest discover -s tests -v
```

The project uses existing models without extra training. The next planned comparison is CLIP alone versus CLIP with Qwen checking its results.
