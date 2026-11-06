from project import ROOT, read_json, write_json


def main():
    name = 'cohort149-storage-closure-and-battle-context-20261102'
    reports = [('evidence/matches/main-nitrosdk14376-20261102.json', 'match_main_nitrosdk14376_20261102.py'),
        ('evidence/matches/main-sdk1188-20261102.json', 'match_main_sdk1188_20261102.py'),
        ('evidence/matches/ov001-20261102-battle-state954.json', 'match_ov001_battle_state954_20261102.py')]
    additions = [dict(module=r['module'], mode=r.get('mode', 'arm'), address=r['address'], bytes=r['bytes'])
        for report, _ in reports for r in read_json(ROOT / report)['matches']]
    assert len(additions) == 84 and sum(r['bytes'] for r in additions) == 16192
    write_json(ROOT / (name + '-specification.json'), dict(cohort=149, previousAcceptedCohort=148,
        migrations=[], packets=[dict(report=r, producer=[p], directProducer=False) for r, p in reports],
        expectedAdditions=additions, originalChecksRetained=True, postSealCommands=[], oracles=[]))
    stage = 'stage_cross_module_cohort149_20261102.py'
    manifests = ['provenance/main-nitrosdk14376-ready-20261102.json', 'provenance/main-sdk1188-ready-20261102.json',
        'provenance/handoffs/ov001-battle957-ready-20261102.json',
        'evidence/lanes/save-core/creation495-ready-20261102.json',
        'provenance/handoffs/ov001-constructor945-ready-20261102.json']
    extra = [name + '-specification.json', stage, __file__.split('\\')[-1],
        'docs/2026-11-02-cohort149-storage-closure-and-battle-context.md',
        'docs/2026-11-02-application-integration-evidence-update-v6.md',
        'record_cohort149_independent_replays_20261102.py',
        'evidence/verification/ov001-battle957-independent-replay-20261102.json',
        'evidence/verification/save-core-creation495-independent-replay-20261102.json',
        'evidence/verification/ov001-constructor945-independent-replay-20261102.json']
    assert all((ROOT / p).is_file() for p in extra if p not in [stage, name + '-specification.json'])
    write_json(ROOT / (name + '-package.json'), dict(cohort=149, manifests=manifests,
        archives=['ov001-battle957-20261102', 'save-core-creation495-20261102', 'ov001-constructor945-20261102'],
        traces=[], extra=extra))
    (ROOT / stage).write_text("import sys\nimport stage_declared_source_package_v7_20261102 as staging\n\n\nif __name__ == '__main__':\n    sys.argv = [sys.argv[0], '" + name + "-package.json']\n    staging.main()\n", encoding='utf-8')
    print(dict(cohort=149, proposedFunctions=84, proposedBytes=16192, registryMutated=False))


if __name__ == '__main__':
    main()
