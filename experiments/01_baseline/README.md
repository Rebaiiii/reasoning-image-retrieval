# CLIP baseline

I started with six generated shapes and six queries. The recorded run scored 3/6. This checks the pipeline, not research performance.

Run `python baseline.py` from the repository root. Inputs remain in `practice/`; the original output is `example_run.json`.

## Repository layout

Paths in commands are relative to the repository root. Shared code is in `retrieval/`; downloaded photos are in `data/images/`. Recorded `example_run.json` files are preserved unchanged. Fresh runs go to this experiment’s ignored `results/` directory.
