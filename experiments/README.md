# Experiment records

Each numbered folder keeps the questions, labels, methods and recorded results for one completed experiment. I keep the original input and result files unchanged so that restructuring the code does not rewrite the experiment history.

- `config.json` selects the evaluation mode and image manifest.
- `queries.json` or `cases.json` fixes the query text and expected answers.
- `audit.json`, where present, records screening before scoring.
- `example_run.json` is the original recorded output.
- `results/` holds new runs and is ignored by Git.

The first experiment still runs through `python baseline.py`. For experiments 02–05, use `python -m retrieval.download --experiment NAME` followed by `python -m retrieval.evaluate --experiment NAME` from the repository root.

## Evaluation modes

`full` ranks all photos in the selected manifest for each query. `wording` compares the original and explicit query against the same two photos. `pairs` evaluates two opposing queries against a fixed pair.

New shared-evaluator outputs include model revision, device, manifest and input hashes, and every ranking. Each query records `target_margin` (target score minus the strongest alternative), `correct`, and `tie`. Pair experiments additionally report whether the choice changed and whether both answers were correct. When an audit is present, results are reported for both all pairs and unflagged pairs.

Scores are cosine similarities, not probabilities. An exact tie is never counted as correct by the shared evaluator. The original practice baseline retains its historical stable-ranking tie behaviour.

## Layout migration

The earlier folders were renamed as follows; their JSON inputs and recorded results were preserved byte-for-byte:

| Previous location | Current experiment |
|---|---|
| Root `example_run.json` | `01_baseline/example_run.json` |
| `datasets/spatial_small` | `02_spatial_examples` |
| `datasets/spatial_probe` | `03_query_wording` |
| `datasets/relation_switch` | `04_relation_switch` |
| `datasets/probe100` | `05_relation_switch_100` |

Image manifests moved to `data/manifests/`. Real photos now share `data/images/`, with duplicate IDs checked for identical content during migration. Individual experiment candidate sets are unchanged. Historical result schemas are retained; fresh runs use the shared schema above.
