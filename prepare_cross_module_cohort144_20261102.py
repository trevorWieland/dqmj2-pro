from project import ROOT, read_json, write_json


def main():
    name = 'cohort144-textures-record-lookup-and-arm7-20261102'
    reports = [
        ('evidence/matches/main-texture-pattern436-v3-20261102.json', 'match_main_texture_pattern436_v3_20261102.py'),
        ('evidence/matches/mechanics-save-20261102-lane-record-expand438.json', 'match_mechanics_save_20261102_lane_record_expand438.py'),
        ('evidence/matches/ov000-20261102-lookup893.json', 'match_ov000_lookup893_20261102.py'),
        ('evidence/matches/arm7-sdk376-receive-helpers1092-20261102.json', 'validate_arm7_sdk377_receive_helpers_20261102.py'),
    ]
    manifests = [
        'provenance/main-texture-pattern436-windows-ready-20261102.json',
        'evidence/lanes/save-core/record-expand438-ready-20261102.json',
        'provenance/handoffs/ov000-lookup893-ready-20261102.json',
        'provenance/arm7-sdk380-receive-helpers1092-handoff-20261102.json',
        'provenance/handoffs/ov000-geometry895-windows-ready-20261102.json',
        'provenance/handoffs/ov000-neighbors894-ready-20261102.json',
        'evidence/lanes/save-core/thumb443-ready-20261102.json',
    ]
    archives = ['save-core-record-expand438-20261102', 'ov000-lookup893-20261102',
        'arm7-sdk380-receive-helpers1092-20261102', 'ov000-geometry895-windows-20261102',
        'ov000-neighbors894-20261102', 'save-core-thumb443-20261102']
    receipts = ['save-core-record-expand438', 'ov000-lookup893', 'arm7-sdk380',
        'ov000-geometry895-windows', 'ov000-neighbors894', 'save-core-thumb443']
    specification = dict(cohort=144, previousAcceptedCohort=143, migrations=[],
        packets=[dict(report=report, producer=[producer], directProducer=False) for report, producer in reports],
        expectedAdditions=[dict(module=row['module'], mode=row.get('mode', 'arm'), address=row['address'], bytes=row['bytes'])
            for report, _ in reports for row in read_json(ROOT / report)['matches']],
        originalChecksRetained=True,
        postSealCommands=[['check_main_texture_pattern436_windows32_20261102.py']],
        oracles=[dict(report='evidence/ports/main-texture-pattern436-windows32-20261102.json',
            reproduce=['check_main_texture_pattern436_windows32_20261102.py'])])
    assert len(specification['expectedAdditions']) == 10
    assert sum(row['bytes'] for row in specification['expectedAdditions']) == 2100
    write_json(ROOT / (name + '-specification.json'), specification)
    stage = 'stage_cross_module_cohort144_20261102.py'
    extra = [name + '-specification.json', stage, __file__.split('\\')[-1],
        'docs/2026-11-02-cohort144-textures-record-lookup-and-arm7.md',
        'record_cohort144_independent_replays_20261102.py',
        'evidence/verification/cohort142-packaging-resumption-20261102.json',
        *[f'evidence/verification/{label}-independent-replay-20261102.json' for label in receipts]]
    write_json(ROOT / (name + '-package.json'), dict(cohort=144, manifests=manifests,
        archives=archives, traces=[], extra=extra))
    (ROOT / stage).write_text("import sys\nimport stage_declared_source_package_v7_20261102 as staging\n\n\nif __name__ == '__main__':\n    sys.argv = [sys.argv[0], '" + name + "-package.json']\n    staging.main()\n", encoding='utf-8')
    print(dict(cohort=144, proposedFunctions=10, proposedBytes=2100, registryMutated=False))


if __name__ == '__main__':
    main()
