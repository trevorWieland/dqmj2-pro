import argparse
from project import ROOT, read_json, write_json, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', nargs=4, action='append', default=[],
        metavar=('MANIFEST', 'REPORT', 'PRODUCER', 'ARCHIVE'))
    options = parser.parse_args()
    assert len(options.packet) == 2
    manifests = ['provenance/root-large-callback-queue652-ready-20261101.json',
        'provenance/root-local-ast-breadth22-research-20261101.json']
    packets = [dict(report='evidence/matches/main-callback380-20261101.json',
        producer=['match_main_callback380_20261101.py'], directProducer=False),
        dict(report='evidence/matches/main-queue272-20261101.json',
        producer=['match_main_queue272_20261101.py'], directProducer=False)]
    archives, counts = [], {}
    for manifest, report, producer, archive in options.packet:
        manifests.append(manifest)
        packets.append(dict(report=report, producer=[producer], directProducer=False))
        archives.append(archive)
    for name in manifests:
        fields = {}
        for field, rows in read_json(ROOT / name).items():
            if ('required' in field.lower() or 'existing' in field.lower()) and isinstance(rows, list):
                if not all(isinstance(row, dict) and 'path' in row and 'sha256' in row for row in rows):
                    continue
                for row in rows:
                    assert sha256(ROOT / row['path']) == row['sha256'], row['path']
                fields[field] = len(rows)
        counts[name] = fields
    write_json(ROOT / 'evidence/verification/cohort121-breadth-existing-inputs-20261101.json',
        dict(passed=True, packets=counts))
    additions = [{key: row[key] for key in ['module', 'mode', 'address', 'bytes']}
        for packet in packets for row in read_json(ROOT / packet['report'])['matches']]
    assert len(additions) == 4 and sum(row['bytes'] for row in additions) == 2020
    write_json(ROOT / 'cohort121-breadth-specification-20261101.json', dict(cohort=121,
        previousAcceptedCohort=120, migrations=[], packets=packets, expectedAdditions=additions,
        originalChecksRetained=True, postSealCommands=[], oracles=[]))
    write_json(ROOT / 'cohort121-breadth-package-20261101.json', dict(cohort=121, manifests=manifests,
        archives=archives, traces=[], extra=['prepare_cohort121_breadth_20261101.py',
            'stage_cohort121_breadth_20261101.py', 'cohort121-breadth-specification-20261101.json',
            'docs/2026-11-01-cohort121-larger-source-bodies.md',
            'evidence/verification/cohort121-breadth-existing-inputs-20261101.json',
            'evidence/verification/cohort121-save-roster-existing-inputs-20261101.json',
            'evidence/verification/cohort121-overlay702-existing-inputs-20261101.json']))
    print(dict(functionCandidates=len(additions), initializedBytes=sum(row['bytes'] for row in additions)))


if __name__ == '__main__':
    main()
