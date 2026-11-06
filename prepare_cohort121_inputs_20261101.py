from pathlib import Path
from project import ROOT, read_json, write_json, sha256


def main():
    manifests = ['provenance/main-random-word152-ready-20261101.json',
        'provenance/arm7-core118-packet176-handoff-20261101.json',
        'provenance/handoffs/ov003-panel652-resource-slots-20261101.json']
    counts = {}
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
    write_json(ROOT / 'evidence/verification/cohort121-worker-existing-inputs-20261101.json', dict(passed=True, packets=counts))
    packets = [dict(report='evidence/matches/main-random-word152-20261101.json',
        producer=['match_main_random_word152_20261101.py'], directProducer=False),
        dict(report='evidence/matches/arm7-core118-packet176-20261101.json',
        producer=['match_arm7_core118_packet176_20261101.py'], directProducer=True),
        dict(report='evidence/matches/ov003-20261101-panel652.json',
        producer=['match_ov003_panel652_20261101.py'], directProducer=False)]
    additions = []
    for packet in packets:
        for row in read_json(ROOT / packet['report'])['matches']:
            additions.append({key: row[key] for key in ['module', 'mode', 'address', 'bytes']})
    assert len(additions) == 3 and sum(row['bytes'] for row in additions) == 716
    specification = dict(cohort=121, previousAcceptedCohort=120, migrations=[], packets=packets,
        expectedAdditions=additions, postSealCommands=[], oracles=[
            dict(report='evidence/verification/arm7-core118-packet176-controls-20261101.json',
                reproduce=['validate_arm7_core118_packet176_20261101.py'])])
    write_json(ROOT / 'cohort121-specification-20261101.json', specification)
    prior = [read_json(ROOT / f'cohort{number}-specification-20261101.json') for number in range(117, 121)]
    write_json(ROOT / 'cohort121-prerequisite-exclusion-20261101.json', dict(sourceCredit=0,
        purpose='Pending identity exclusion only; no accepted coverage',
        packets=[packet for item in prior for packet in item['packets']],
        expectedAdditions=[row for item in prior for row in item['expectedAdditions']]))
    extra = ['cohort121-specification-20261101.json', 'stage_cohort121_package_20261101.py',
        'cohort121-prerequisite-exclusion-20261101.json', Path(__file__).name,
        'docs/2026-11-01-cohort121-rng-word-and-connected-callers.md',
        'evidence/verification/cohort121-worker-existing-inputs-20261101.json',
        'evidence/verification/cohort121-arm7-existing-inputs-20261101.json',
        'evidence/verification/cohort121-overlay-existing-inputs-20261101.json',
        'evidence/verification/cohort121-identity-preflight-20261101.json']
    write_json(ROOT / 'cohort121-package-20261101.json', dict(cohort=121, manifests=manifests,
        archives=['arm7-core118-packet176-20261101', 'ov003-panel652-20261101'], extra=extra, traces=[]))
    print(dict(functionCandidates=3, initializedBytes=716, initializedDenominatorDelta=0))


if __name__ == '__main__':
    main()
