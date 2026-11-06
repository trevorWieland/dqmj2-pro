from project import ROOT, read_json, write_json


def main():
    name = 'cohort146-vram-gecom-sound-recruitment-and-abi-20261102'
    reports = [
        ('evidence/matches/main-vram1340-20261102.json', 'match_main_vram1340_20261102.py'),
        ('evidence/matches/main-sound-canvas492-20261102.json', 'match_main_sound_canvas492_20261102.py'),
        ('evidence/matches/main-alarm72-20261102.json', 'match_main_alarm72_20261102.py'),
        ('evidence/matches/main-gecom352-20261102.json', 'match_main_gecom352_20261102.py'),
        ('evidence/matches/ov001-20261102-nextstage924.json', 'match_ov001_nextstage924_20261102.py'),
        ('evidence/matches/mechanics-save-20261102-lane-context-abi476.json', 'match_mechanics_save_20261102_lane_context_abi476.py'),
    ]
    specification = dict(cohort=146, previousAcceptedCohort=145,
        migrations=[dict(module='main', mode='thumb', address='0x209de84', bytes=340,
            reason='Align exact selected word/pointer/void helper interfaces with explicit conversions; zero new coverage')],
        packets=[dict(report=report, producer=[producer], directProducer=False) for report, producer in reports],
        expectedAdditions=[dict(module=row['module'], mode=row.get('mode', 'arm'), address=row['address'], bytes=row['bytes'])
            for report, _ in reports[:-1] for row in read_json(ROOT / report)['matches']],
        originalChecksRetained=True, postSealCommands=[], oracles=[])
    assert len(specification['expectedAdditions']) == 18
    assert sum(row['bytes'] for row in specification['expectedAdditions']) == 2552
    write_json(ROOT / (name + '-specification.json'), specification)
    manifests = ['provenance/main-vram1340-ready-20261102.json',
        'provenance/main-sound-canvas492-ready-20261102.json', 'provenance/main-alarm72-ready-20261102.json',
        'provenance/main-gecom352-ready-20261102.json', 'provenance/handoffs/ov001-nextstage924-ready-20261102.json',
        'evidence/lanes/save-core/context-abi476-ready-20261102.json',
        'provenance/handoffs/ov001-scratch922-ready-20261102.json']
    stage = 'stage_cross_module_cohort146_20261102.py'
    extra = [name + '-specification.json', stage, __file__.split('\\')[-1],
        'docs/2026-11-02-cohort146-vram-gecom-sound-recruitment-and-abi.md',
        'record_cohort146_independent_replays_20261102.py',
        'docs/2026-11-02-application-integration-evidence-update-v4.md',
        'evidence/verification/save-core-context-abi476-independent-replay-20261102.json',
        'evidence/verification/ov001-scratch922-independent-replay-20261102.json',
        'evidence/verification/ov001-nextstage924-independent-replay-20261102.json',
        'evidence/attempts/main-vram-init-function-role-refusal-20261102.json',
        'evidence/attempts/main-vram-init-int-word-refusal-20261102.json',
        'nonmatching/main/20261102-vram-init-function-role/native_main_0203c438.c',
        'nonmatching/main/20261102-vram-init-int-word/native_main_0203c438.c']
    write_json(ROOT / (name + '-package.json'), dict(cohort=146, manifests=manifests,
        archives=['ov001-nextstage924-20261102', 'save-core-context-abi476-20261102', 'ov001-scratch922-20261102'],
        traces=[], extra=extra))
    (ROOT / stage).write_text("import sys\nimport stage_declared_source_package_v7_20261102 as staging\n\n\nif __name__ == '__main__':\n    sys.argv = [sys.argv[0], '" + name + "-package.json']\n    staging.main()\n", encoding='utf-8')
    print(dict(cohort=146, proposedFunctions=18, proposedBytes=2552, zeroCreditMigrationBytes=340,
        registryMutated=False))


if __name__ == '__main__':
    main()
