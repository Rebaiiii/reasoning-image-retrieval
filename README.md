# Reasoning-Based Image Retrieval

I’m testing whether text-to-image retrieval distinguishes spatial relationships, such as a cat **on** a laptop versus a cat **beside** it.

The current baseline is frozen CLIP ViT-B/32. I run it on CPU, one image at a time, on an M1 MacBook with 8 GB RAM. Qwen reranking is planned; it is not implemented yet.

## Current results

In the latest experiment, I tested 100 photo pairs with two opposing queries per pair. CLIP answered **109/200 queries correctly** and selected the same photo for both queries in **83/100 pairs**.

Visual screening flagged 43 ambiguous pairs before scoring. On the 57 unflagged pairs, accuracy was **66/114**, with both answers correct in **10/57 pairs**. These are exploratory results, not evidence that CLIP cannot understand depth. [Read the experiment and limitations](experiments/05_relation_switch_100/README.md).

## Setup

Run from the repository root with Python 3.10–3.12:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python baseline.py
```

The first run downloads the model weights (about 605 MB). Subsequent runs reuse `cache/`. The six generated practice images check the pipeline; they are not a research benchmark.

```bash
python baseline.py --query "A red circle to the left of a blue square."
```

## Reproduce an experiment

```bash
python -m retrieval.download --experiment 05_relation_switch_100
python -m retrieval.evaluate --experiment 05_relation_switch_100
```

The downloader checks image hashes. The evaluator uses only the images specified by the selected experiment, even when other photos are downloaded. Add `--cache-dir /path/to/existing/cache` to reuse a cache elsewhere.

New output goes to the experiment’s `results/latest.json`. Recorded `example_run.json` files remain unchanged. The shared evaluator records rankings, scores and input hashes; its output schema is documented in [the experiment guide](experiments/README.md).

## Project layout

```text
retrieval/             Shared CLIP, downloading, evaluation and metrics code
experiments/           Fixed queries, audit notes, methods and recorded results
data/manifests/        Image URLs, source annotations and checksums
data/images/           Downloaded photos (ignored by Git)
practice/              Original generated examples
tests/                Evaluation checks
baseline.py            Original baseline command
```

## Experiments

| Experiment | Question |
|---|---|
| [01 — Baseline](experiments/01_baseline/README.md) | Does the retrieval pipeline work? |
| [02 — Spatial examples](experiments/02_spatial_examples/README.md) | Can it retrieve two spatial descriptions among four photos? |
| [03 — Query wording](experiments/03_query_wording/README.md) | Does more explicit wording change the answer? |
| [04 — Relation switch](experiments/04_relation_switch/README.md) | Does changing the relationship change the selected photo? |
| [05 — 100-pair relation switch](experiments/05_relation_switch_100/README.md) | Does that behaviour persist across more examples? |

Experiment numbers record completed steps; they do not imply independent test sets. Source annotations and photo rights are documented with each experiment. Downloaded COCO photos are not included in Git.

## Checks

```bash
python -m unittest discover -s tests -v
```

I’m keeping the project training-free and adding one research step at a time. The next planned comparison is CLIP retrieval with and without multimodal reranking.
