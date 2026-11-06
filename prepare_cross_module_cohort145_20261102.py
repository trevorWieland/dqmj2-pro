from project import ROOT, read_json, write_json


def main():
    name = 'cohort145-sdk-sbc-hints-context-and-arm7-20261102'
    reports = [
        ('evidence/matches/main-sdk-breadth3176-20261102.json', 'match_main_sdk_breadth3176_20261102.py'),
        ('evidence/matches/main-sbc2480-20261102.json', 'match_main_sbc2480_20261102.py'),
        ('evidence/matches/main-animation-hints292-20261102.json', 'match_main_animation_hints292_20261102.py'),
        ('evidence/matches/mechanics-save-20261102-lane-parent-context455.json', 'match_mechanics_save_20261102_lane_parent_context455.py'),
        ('evidence/matches/arm7-sdk387-receive-registration1436-20261102.json', 'validate_arm7_sdk388_receive_registration_20261102.py'),
    ]
    manifests = [
        'provenance/main-sdk-breadth3176-ready-20261102.json', 'provenance/main-sbc2480-ready-20261102.json',
        'provenance/main-animation-hints292-windows-ready-20261102.json',
        'evidence/lanes/save-core/parent-context455-ready-20261102.json',
        'provenance/arm7-sdk390-receive-registration1436-handoff-20261102.json',
        'provenance/handoffs/ov000-geometry902-ready-20261102.json',
        'provenance/handoffs/ov005-controller907-ready-20261102.json',
        'provenance/handoffs/ov001-recruit912-ready-20261102.json',
        'provenance/handoffs/ov001-selector921-ready-20261102.json',
    ]
    archives = ['save-core-parent-context455-20261102', 'arm7-sdk390-receive-registration1436-20261102',
        'ov000-geometry902-20261102', 'ov005-controller907-20261102', 'ov001-recruit912-20261102',
        'ov001-selector921-20261102']
    receipts = ['save-core-parent-context455', 'arm7-sdk390', 'ov000-geometry902',
        'ov005-controller907', 'ov001-recruit912', 'ov001-selector921']
    specification = dict(cohort=145, previousAcceptedCohort=144, migrations=[],
        packets=[dict(report=report, producer=[producer], directProducer=False) for report, producer in reports],
        expectedAdditions=[dict(module=row['module'], mode=row.get('mode', 'arm'), address=row['address'], bytes=row['bytes'])
            for report, _ in reports for row in read_json(ROOT / report)['matches']], originalChecksRetained=True,
        postSealCommands=[['check_main_animation_hints292_windows32_20261102.py']],
        oracles=[dict(report='evidence/ports/main-animation-hints292-windows32-20261102.json',
            reproduce=['check_main_animation_hints292_windows32_20261102.py'])])
    assert len(specification['expectedAdditions']) == 31
    assert sum(row['bytes'] for row in specification['expectedAdditions']) == 7804
    write_json(ROOT / (name + '-specification.json'), specification)
    stage = 'stage_cross_module_cohort145_20261102.py'
    extra = [name + '-specification.json', stage, __file__.split('\\')[-1],
        'docs/2026-11-02-cohort145-sdk-sbc-hints-context-and-arm7.md',
        'record_cohort145_independent_replays_20261102.py', 'audit_application_selector_validity_20261102.py',
        'evidence/abi/application-selector-validity-static-audit-20261102.json',
        'docs/2026-11-02-application-integration-evidence-update-v3.md',
        *[f'evidence/verification/{label}-independent-replay-20261102.json' for label in receipts]]
    write_json(ROOT / (name + '-package.json'), dict(cohort=145, manifests=manifests,
        archives=archives, traces=[], extra=extra))
    (ROOT / stage).write_text("import sys\nimport stage_declared_source_package_v7_20261102 as staging\n\n\nif __name__ == '__main__':\n    sys.argv = [sys.argv[0], '" + name + "-package.json']\n    staging.main()\n", encoding='utf-8')
    print(dict(cohort=145, proposedFunctions=31, proposedBytes=7804, registryMutated=False))


if __name__ == '__main__':
    main()
