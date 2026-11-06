### Changing the Relationship in the Query

Five pairs of existing real photographs, with two queries per pair. The expected
answer changes between the queries. This checks whether CLIP's top-ranked image
changes with the relationship described in the text.

## Results

- Correct queries: **7/10**.
- Pairs with both answers correct: **2/5**.
- Pairs where the selected image changed: **2/5**; both switches were correct.
- Exact score ties: **0**.

| Pair | First query | Second query | Behaviour |
|---|---|---|---|
| Laptop A | On laptop: wrong | Beside laptop: correct | Same image |
| Laptop B | On laptop: correct | Beside laptop: wrong | Same image |
| Refrigerator | On top: correct | Inside: correct | Correct switch |
| Wine glass | Behind: correct | In front: wrong | Same image |
| Car | Under: correct | On roof: correct | Correct switch |

The wine-glass pair shows why one correct answer can be misleading. CLIP
selected the photo showing a cat behind a glass for both “behind” and “in front
of.” The earlier successful behind-query alone did not show that CLIP could reliably tell front from behind.

The cosine scores changed when the query changed, even in pairs where the winner
did not. An unchanged winner does not mean the text encoder completely ignored
the relation. Neither the similarity nor the score margin is a probability.

## What This Tests

Within each pair, the candidate images remain identical across both queries;
only the text changes. Both queries name the same object categories, though
“on the roof of” also specifies a part of the car. The labels in `cases.json`
were fixed before this run. No prompts were adjusted after seeing this result.

The ten photographs are different: no photo is reused across these five pairs.
They come from the earlier spatial probe, whose original-query results were
already known. These photos help explore the problem. They are not a fresh test set.

All five pairs were visually reviewed in full and through CLIP's centre crop.
The second descriptions were added during the photo review. They are not extra
labels checked by VSR. The paired relationships
are alternatives for these particular photos, not always opposites
in every scene.

The photographs within each pair differ in camera viewpoint, background, and
object appearance. This is **not** the proposed fixed-camera experiment with the
same objects rearranged. Those new photos have not been taken yet.
Object positions were not kept the same across photos, so this test cannot show
whether 2D or 3D understanding caused the errors.

## What the results show

CLIP got both answers right in two pairs and kept the same image in the other
three. It did not reliably change its answer when the relationship changed.
This does not prove that CLIP only uses 2D clues. Two correct pairs also do not
prove that it understands 3D space in general.

A stronger follow-up would photograph the same objects from a fixed camera in
both arrangements, label them before scoring, and include cases where apparent
image height stays similar while physical support changes.

## Run again

From the main project folder, with the existing environment activated:

```bash
python -m retrieval.download --experiment 03_query_wording
python -m retrieval.evaluate --experiment 04_relation_switch
```

The runner reuses the photos in `data/images/` and the unchanged
Module 1 encoding and ranking functions. `--cache-dir` can point to an existing
CLIP cache. Model: pinned CLIP ViT-B/32, CPU, no training. Each image is encoded
once. Only the two assigned candidates are ranked for each query.

`cases.json` defines the text and expected answers. `data/manifests/04_relation_switch.json` records the
source image IDs, URLs, VSR metadata, and file hashes. `example_run.json` contains
the checked output, all scores, and hashes of both input manifests. New runs save
to `results/latest.json`. Exact ties are flagged and never counted as correct.

## Sources

The photographs and original label sources come from
[the spatial probe](../03_query_wording/README.md), using COCO images referenced by
[VSR](https://github.com/cambridgeltl/visual-spatial-reasoning).
The VSR license remains in the adjacent `03_query_wording` folder. Original image
rights remain with the photographers; photos are not included in Git.

## File locations

Run commands from the main project folder. Shared code is in `retrieval/`, and downloaded photos are in `data/images/`. Saved results stay in `example_run.json`. New runs go to this experiment’s `results/` folder, which Git ignores.
