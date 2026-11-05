"""Download an experiment's photos and verify their recorded checksums."""
import argparse
import hashlib
import requests
from .data import ROOT, load_experiment


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--experiment', required=True)
    args = parser.parse_args()
    _, _, _, records = load_experiment(args.experiment)
    directory = ROOT / 'data/images'
    directory.mkdir(parents=True, exist_ok=True)
    for record in records:
        destination = directory / record['image']
        if destination.exists():
            data = destination.read_bytes()
        else:
            response = requests.get(record['url'], timeout=30)
            response.raise_for_status()
            data = response.content
        if hashlib.sha256(data).hexdigest() != record['sha256']:
            raise ValueError(f'Image checksum mismatch: {destination.name}')
        if not destination.exists():
            destination.write_bytes(data)
    print(f'Verified {len(records)} photos for {args.experiment}')


if __name__ == '__main__':
    main()
