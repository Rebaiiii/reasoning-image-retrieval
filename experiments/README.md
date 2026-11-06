# Experiment records

Each numbered folder keeps the questions, labels, methods and recorded results for one completed experiment. The original input and result files stay unchanged when the code moves.

- `config.json` selects the evaluation mode and image manifest.
- `queries.json` or `cases.json` fixes the query text and expected answers.
- `audit.json`, where present, records screening before scoring.
- `example_run.json` is the original recorded output.
- `results/` holds new runs and is ignored by Git.

The first experiment still runs through `python baseline.py`. For experiments 02–05, use `python -m retrieval.download --experiment NAME` followed by `python -m retrieval.evaluate --experiment NAME` from the main project folder.

## Test types

`full` ranks all photos in the selected manifest for each query. `wording` compares the original and explicit query against the same two photos. `pairs` checks two queries with different expected answers against the same two photos.

New results include the model version, device, file hashes, and every image ranking. Each query records `target_margin` (target score minus the strongest alternative), `correct`, and `tie`. Pair tests also report whether the choice changed and whether both answers were correct. When an audit is present, results are reported for both all pairs and unflagged pairs.

Scores are cosine similarities, not probabilities. An exact tie is never counted as correct by the shared evaluator. The original practice code keeps filename order when scores tie.

## Folder changes

The earlier folders were renamed as follows; their JSON inputs and recorded results were kept exactly the same:

| Previous location | Current experiment |
|---|---|
| Root `example_run.json` | `01_baseline/example_run.json` |
| `datasets/spatial_small` | `02_spatial_examples` |
| `datasets/spatial_probe` | `03_query_wording` |
| `datasets/relation_switch` | `04_relation_switch` |
| `datasets/probe100` | `05_relation_switch_100` |

Image manifests moved to `data/manifests/`. Real photos now share `data/images/`, files with the same ID were checked to make sure their contents matched. Each test still uses the same photos as before. Old result files keep their original format. New runs use the fields described above.
