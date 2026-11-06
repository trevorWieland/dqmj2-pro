from pathlib import Path
from project import ROOT, read_json, write_json, sha256


def main():
    manifests = ['provenance/main-signed-store136-ready-20261101.json',
        'provenance/arm7-core117-state240-handoff-20261101.json',
        'provenance/same-width-bitcast32-ready-20261101.json']
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
    write_json(ROOT / 'evidence/verification/cohort120-worker-existing-inputs-20261101.json', dict(passed=True, packets=counts))
    packets = [dict(report='evidence/matches/main-signed-store136-20261101.json',
        producer=['match_main_signed_store136_20261101.py'], directProducer=False),
        dict(report='evidence/matches/arm7-core117-state240-20261101.json',
        producer=['match_arm7_core117_state240_20261101.py'], directProducer=True)]
    additions = []
    for packet in packets:
        for row in read_json(ROOT / packet['report'])['matches']:
            additions.append({key: row[key] for key in ['module', 'mode', 'address', 'bytes']})
    assert len(additions) == 3 and sum(row['bytes'] for row in additions) == 376
    specification = dict(cohort=120, previousAcceptedCohort=119, migrations=[], packets=packets,
        expectedAdditions=additions, postSealCommands=[['validate_arm7_core117_gap52_20261101.py'],
            ['probe_same_width_bitcasts_20261101.py']], oracles=[
            dict(report='evidence/verification/arm7-core117-state240-controls-20261101.json',
                reproduce=['validate_arm7_core117_state240_20261101.py'])])
    write_json(ROOT / 'cohort120-specification-20261101.json', specification)
    prior = [read_json(ROOT / f'cohort{number}-specification-20261101.json') for number in range(117, 120)]
    write_json(ROOT / 'cohort120-prerequisite-exclusion-20261101.json', dict(sourceCredit=0,
        purpose='Pending identity exclusion only; no accepted coverage',
        packets=[packet for item in prior for packet in item['packets']],
        expectedAdditions=[row for item in prior for row in item['expectedAdditions']]))
    extra = ['cohort120-specification-20261101.json', 'stage_cohort120_package_20261101.py',
        'cohort120-prerequisite-exclusion-20261101.json', Path(__file__).name,
        'docs/2026-11-01-cohort120-initializer-and-arm7-state.md',
        'evidence/verification/cohort120-worker-existing-inputs-20261101.json',
        'evidence/verification/cohort120-arm7-required-inputs-20261101.json',
        'evidence/verification/cohort120-identity-preflight-20261101.json',
        'reproduce_alarm_registration156_current_products_20261101.py',
        'resume_clean_checks106_v2_20261101.py']
    for directory in ['evidence/attempts/clean106-alarm156-prerequisite-20261101',
            'evidence/verification/clean106-alarm156-replay-20261101']:
        extra.extend(path.relative_to(ROOT).as_posix() for path in (ROOT / directory).glob('*') if path.is_file())
    write_json(ROOT / 'cohort120-package-20261101.json', dict(cohort=120, manifests=manifests,
        archives=['arm7-core117-state240-20261101'], extra=extra, traces=[]))
    print(dict(functionCandidates=3, initializedBytes=376, initializedDenominatorDelta=0, bitcastGameSourceCredit=0))


if __name__ == '__main__':
    main()
