from project import ROOT, read_json, write_json


def main():
    name = 'cohort150-arm7-receive-and-source-breadth-20261102'
    reports = [('evidence/matches/main-sdk2520-20261102.json', 'match_main_sdk2520_20261102.py'),
        ('evidence/matches/arm7-sdk436-intr-transmit-compiler1236-20261102.json', 'validate_arm7_sdk437_intr_transmit_compiler_20261102.py'),
        ('evidence/matches/arm7-sdk423-beacon-probe-key3016-20261102.json', 'validate_arm7_sdk424_beacon_probe_key_20261102.py'),
        ('evidence/matches/ov001-20261102-battle-state961.json', 'match_ov001_battle_phase961_20261102.py')]
    additions = [dict(module=r['module'], mode=r.get('mode', 'arm'), address=r['address'], bytes=r['bytes'])
        for report, _ in reports for r in read_json(ROOT / report)['matches']]
    assert len(additions) == 15 and sum(r['bytes'] for r in additions) == 7396
    write_json(ROOT / (name + '-specification.json'), dict(cohort=150, previousAcceptedCohort=149,
        migrations=[], packets=[dict(report=r, producer=[p], directProducer=False) for r, p in reports],
        expectedAdditions=additions, originalChecksRetained=True, postSealCommands=[], oracles=[]))
    stage = 'stage_cross_module_cohort150_20261102.py'
    manifests = ['provenance/main-sdk2520-ready-20261102.json',
        'provenance/arm7-sdk439-intr-transmit-compiler1236-handoff-20261102.json',
        'provenance/arm7-sdk426-beacon-probe-key3016-handoff-20261102.json',
        'provenance/handoffs/ov001-phase965-ready-20261102.json']
    extra = [name + '-specification.json', stage, __file__.split('\\')[-1],
        'docs/2026-11-02-cohort150-arm7-receive-and-source-breadth.md',
        'record_cohort150_independent_replays_20261102.py',
        'evidence/verification/arm7-sdk439-independent-replay-20261102.json',
        'evidence/verification/arm7-sdk426-independent-replay-20261102.json',
        'evidence/verification/ov001-phase965-independent-replay-20261102.json']
    assert all((ROOT / p).is_file() for p in extra if p not in [stage, name + '-specification.json'])
    write_json(ROOT / (name + '-package.json'), dict(cohort=150, manifests=manifests,
        archives=['arm7-sdk439-compiler1236-20261102', 'arm7-sdk426-receive3016-20261102', 'ov001-phase965-20261102'],
        traces=[], extra=extra))
    (ROOT / stage).write_text("import sys\nimport stage_declared_source_package_v7_20261102 as staging\n\n\nif __name__ == '__main__':\n    sys.argv = [sys.argv[0], '" + name + "-package.json']\n    staging.main()\n", encoding='utf-8')
    print(dict(cohort=150, proposedFunctions=15, proposedBytes=7396, registryMutated=False))


if __name__ == '__main__':
    main()
