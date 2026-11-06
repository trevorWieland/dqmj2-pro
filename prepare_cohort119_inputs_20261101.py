from pathlib import Path
from project import ROOT, read_json, write_json, sha256


def main():
    manifests = ['provenance/main-indexed-word32-ready-20261101.json',
        'provenance/arm7-child-poll44-functional-handoff-20261101.json',
        'provenance/arm7-breadth115-116-private-checkpoint-20261101.json',
        'evidence/lanes/save-core/recovery-state161-alias164-ready-20261101.json',
        'provenance/handoffs/ov001-growth636-scoped-functional-source-20261101.json']
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
    write_json(ROOT / 'evidence/verification/cohort119-worker-existing-inputs-20261101.json', dict(passed=True, packets=counts))
    packets = [dict(report='evidence/matches/main-indexed-word32-20261101.json',
        producer=['match_main_indexed_word32_20261101.py'], directProducer=False)]
    row = read_json(ROOT / packets[0]['report'])['matches'][0]
    additions = [{key: row[key] for key in ['module', 'mode', 'address', 'bytes']}]
    assert len(additions) == 1 and additions[0]['bytes'] == 32
    specification = dict(cohort=119, previousAcceptedCohort=118, migrations=[], packets=packets,
        expectedAdditions=additions, oracles=[], postSealCommands=[['validate_arm7_child_poll44_functional_20261101.py'],
            ['prove_save_core_recovery_state161_20261101.py'], ['prove_save_core_recovery_alias164_20261101.py'],
            ['probe_main_float630_growth_native_20261101.py'], ['prove_ov001_growth636_20261101.py'],
            ['classify_ov001_growth636_regions_20261101.py']])
    write_json(ROOT / 'cohort119-specification-20261101.json', specification)
    prior = [read_json(ROOT / f'cohort{number}-specification-20261101.json') for number in range(114, 119)]
    write_json(ROOT / 'cohort119-prerequisite-exclusion-20261101.json', dict(sourceCredit=0,
        purpose='Pending identity exclusion only; no accepted coverage',
        packets=[packet for item in prior for packet in item['packets']],
        expectedAdditions=[row for item in prior for row in item['expectedAdditions']]))
    package = dict(cohort=119, manifests=manifests,
        archives=['arm7-child-poll44-20261101', 'arm7-breadth115-116-20261101',
            'save-recovery161-alias164-20261101', 'ov001-growth636-20261101'],
        extra=['cohort119-specification-20261101.json', 'stage_cohort119_package_20261101.py',
            'cohort119-prerequisite-exclusion-20261101.json', Path(__file__).name,
            'docs/2026-11-01-cohort119-indexed-word-and-caller-alias.md',
            'evidence/verification/cohort119-worker-existing-inputs-20261101.json',
            'evidence/verification/cohort119-identity-preflight-20261101.json',
            'evidence/verification/cohort119-first-required-inputs-20261101.json',
            'evidence/verification/cohort119-growth-required-inputs-20261101.json',
            'evidence/attempts/indexed-word32-fixture-initialization-failure-20261101.json',
            'reproduce_card_control452_current_products_20261101.py',
            'resume_clean_checks106_current_products_20261101.py'], traces=[])
    write_json(ROOT / 'cohort119-package-20261101.json', package)
    print(dict(functionCandidates=1, initializedBytes=32, researchPackets=4, otherSourceCredit=0))


if __name__ == '__main__':
    main()
