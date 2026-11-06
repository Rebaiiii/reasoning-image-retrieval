# Checks after the folder cleanup — 2026-11-05

All five tests were run again after moving the code and data.

| Experiment | Reproduced result |
|---|---|
| Practice baseline | 3/6 queries |
| Four-photo spatial examples | 1/2 queries |
| Query wording | 8/18 across both wordings and all nine pairs |
| Five-pair relation switch | 7/10 queries; 2/5 pairs both correct |
| 100-pair relation switch | 109/200 queries; 13/100 pairs both correct |
| Unflagged subset of the 100 pairs | 66/114 queries; 10/57 pairs both correct |

Every image ranking matched the saved result. No cosine score differed by more than 0.000001. The practice result matched exactly. These checks show that the folder cleanup did not change the results. They are not new research tests.

All original JSON inputs, source manifests, screening records and recorded results were kept exactly the same. Downloaded image hashes were checked, and local file links worked.

Six evaluation tests passed: correct switches, incorrect switches, unchanged choices, exact ties, missing candidate images, and invalid opposing targets. Run them with `python -m unittest discover -s tests -v`.

The reruns used CPU, the fixed model version in `retrieval/clip_baseline.py`, and the versions listed in `requirements.txt`. Fresh rerun outputs are local files under each experiment's ignored `results/` directory.
