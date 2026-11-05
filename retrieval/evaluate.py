"""Run a frozen CLIP experiment without changing its inputs or recorded results."""
import argparse
import json
from pathlib import Path
import torch
from transformers import CLIPModel, CLIPProcessor
from .clip_baseline import MODEL_ID, MODEL_REVISION, encode_images, rank_images
from .data import ROOT, checksum, load_experiment, read_json, verified_paths
from .metrics import score_pair, score_query, summarize


def validate_cases(cases, names, mode):
    """Catch missing photos and invalid targets before loading the model."""
    ids = [case['id'] for case in cases]
    if len(set(ids)) != len(ids):
        raise ValueError('Duplicate case IDs')
    for case in cases:
        candidates = case['images'] if mode == 'pairs' else [case['positive'], case['negative']]
        if len(candidates) != 2 or len(set(candidates)) != 2 or not set(candidates) <= set(names):
            raise ValueError(f"Invalid candidate pair: {case['id']}")
        if mode == 'pairs':
            if len(case['queries']) != 2 or {q['target'] for q in case['queries']} != set(candidates):
                raise ValueError(f"Expected opposing targets: {case['id']}")


@torch.inference_mode()
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--experiment', required=True)
    parser.add_argument('--cache-dir', type=Path, default=ROOT / 'cache')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    folder, config, manifest_path, records = load_experiment(args.experiment)
    paths = verified_paths(records)
    names = [p.name for p in paths]
    mode = config['mode']
    if mode not in ['full', 'wording', 'pairs']:
        raise ValueError(f'Unknown evaluation mode: {mode}')
    input_path = folder / ('queries.json' if mode == 'full' else 'cases.json')
    cases = read_json(input_path)
    if mode != 'full':
        validate_cases(cases, names, mode)
    elif not cases or any(q['target'] not in names for q in cases):
        raise ValueError('Missing queries or target images')
    audit_path = folder / 'audit.json'
    flagged = set()
    if audit_path.exists():
        audit = read_json(audit_path)['cases']
        if len(audit) != len(cases) or {x['id'] for x in audit} != {x['id'] for x in cases}:
            raise ValueError('Audit does not cover the experiment cases')
        flagged = {x['id'] for x in audit if x['status'] == 'flagged'}
    print(f'Encoding {len(paths)} photos on CPU', flush=True)
    options = dict(revision=MODEL_REVISION, cache_dir=args.cache_dir)
    processor = CLIPProcessor.from_pretrained(MODEL_ID, use_fast=False, **options)
    model = CLIPModel.from_pretrained(MODEL_ID, **options).eval()
    features = encode_images(model, processor, paths, 'cpu')

    def query_result(candidates, query):
        subset = features[[names.index(name) for name in candidates]]
        _, scores = rank_images(model, processor, subset, query['text'], 'cpu')
        return score_query(candidates, scores, query)

    results = []
    for case in cases:
        if mode == 'full':
            results.append(query_result(names, {'text': case['query'], 'target': case['target']}))
        elif mode == 'wording':
            candidates = sorted([case['positive'], case['negative']])
            for wording in ['query', 'explicit_query']:
                result = query_result(candidates, {'text': case[wording], 'target': case['positive']})
                results.append({**case, 'wording': wording, **result})
        else:
            candidates = sorted(case['images'])
            queries = [query_result(candidates, q) for q in case['queries']]
            results.append({'id': case['id'], 'category': case.get('category', 'unspecified'),
                            'flagged': case['id'] in flagged, **score_pair(queries)})
    report = {'experiment': args.experiment, 'model': MODEL_ID, 'revision': MODEL_REVISION,
              'device': 'cpu', 'manifest_sha256': checksum(manifest_path),
              'inputs_sha256': checksum(input_path), 'results': results}
    if mode == 'pairs':
        report['summaries'] = {'all': summarize(results)}
        if audit_path.exists():
            report['audit_sha256'] = checksum(audit_path)
            report['summaries']['unflagged'] = summarize([r for r in results if not r['flagged']])
        report['by_category'] = {
            cat: {scope: summarize([r for r in results if r['category'] == cat and
                                   (scope == 'all' or not r['flagged'])])
                  for scope in report['summaries']}
            for cat in sorted({r['category'] for r in results})}
        print(json.dumps(report['summaries'], indent=2))
    else:
        report['query_correct'] = sum(r['correct'] for r in results)
        report['query_count'] = len(results)
        print(f"Correct: {report['query_correct']}/{report['query_count']}")
    output = args.output or folder / 'results/latest.json'
    # Historical results are immutable experiment records.
    if output.resolve() == (folder / 'example_run.json').resolve():
        raise ValueError('Choose a new output path; preserve example_run.json')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(f'Saved {output}')


if __name__ == '__main__':
    main()
