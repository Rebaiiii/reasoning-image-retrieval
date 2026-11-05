"""Read experiment definitions and verify their source images."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads(path.read_text())


def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_experiment(name):
    folder = ROOT / 'experiments' / name
    config = read_json(folder / 'config.json')
    manifest_path = ROOT / config['manifest']
    records = read_json(manifest_path)
    names = [r['image'] for r in records]
    if len(names) != len(set(names)):
        raise ValueError('Duplicate image IDs in manifest')
    return folder, config, manifest_path, records


def verified_paths(records):
    paths = []
    for record in records:
        path = ROOT / 'data/images' / record['image']
        if checksum(path) != record['sha256']:
            raise ValueError(f'Image checksum mismatch: {path.name}')
        paths.append(path)
    return sorted(paths)
