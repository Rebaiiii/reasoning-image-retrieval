# CLIP baseline

The first test uses six generated shapes and six queries. CLIP got 3/6 answers right. This checks that the code works, not how well it handles real photos.

Run `python baseline.py` from the main project folder. Inputs remain in `practice/`; the original output is `example_run.json`.

## File locations

Run commands from the main project folder. Shared code is in `retrieval/`, and downloaded photos are in `data/images/`. Saved results stay in `example_run.json`. New runs go to `results/last_run.json` in the main project folder, which Git ignores.
