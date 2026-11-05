# Cleanup validation — 2026-11-05

I reran all five existing experiments after moving the code and data.

| Experiment | Reproduced result |
|---|---|
| Practice baseline | 3/6 queries |
| Four-photo spatial examples | 1/2 queries |
| Query wording | 8/18 across both wordings and all nine pairs |
| Five-pair relation switch | 7/10 queries; 2/5 pairs both correct |
| 100-pair relation switch | 109/200 queries; 13/100 pairs both correct |
| Unflagged subset of the 100 pairs | 66/114 queries; 10/57 pairs both correct |

Every ranking matched the historical output. Every cosine score matched within an absolute tolerance of 0.000001. The original practice output matched exactly. This is a regression check of the reorganization, not a new experiment or independent replication.

All original JSON inputs, source manifests, screening records and recorded results were preserved byte-for-byte. Downloaded image hashes were checked, and local documentation links resolved.

Six evaluation tests passed: correct switches, incorrect switches, unchanged choices, exact ties, missing candidate images, and invalid opposing targets. Run them with `python -m unittest discover -s tests -v`.

The reruns used CPU, the pinned model revision in `retrieval/clip_baseline.py`, and the versions listed in `requirements.txt`. Fresh rerun outputs are local files under each experiment's ignored `results/` directory.
