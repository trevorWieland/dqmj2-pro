import argparse
import subprocess
import sys
from project import ROOT, read_json, write_json, configuration, sha256
from ledger_state import collect_matches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    args = parser.parse_args()
    plan = read_json(ROOT / f'evidence/verification/cohort-2026-10-29-{args.cohort}.json')
    assert not plan['linksPending'] and plan['sourceRegistrySha256'] == sha256(ROOT / 'recovery.json')
    matches, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and len(matches) == plan['sourceMatchedFunctions']
    functions = []
    for key, row in sorted(matches.items(), key=lambda item: tuple(str(value) for value in item[0])):
        address = row['address']
        address = int(address, 0) if isinstance(address, str) else address
        functions.append(dict(processor=row.get('processor'), program=row.get('program'),
            module=row['module'], mode=row['mode'], name=row['name'], address=address,
            source=row['source'], sourceSha256=row['sourceSha256'], bytes=row['size']))
    path = ROOT / f'evidence/verification/accepted-cohort{args.cohort}-identities-20261031.json'
    document = dict(acceptedCohort=args.cohort, romSha256=configuration()['romSha256'], functions=functions)
    if path.exists():
        assert read_json(path) == document
    else:
        write_json(path, document)
    subprocess.run([sys.executable, str(ROOT / 'normalize_accepted_snapshot_20261031.py'), '--cohort', str(args.cohort)], cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
