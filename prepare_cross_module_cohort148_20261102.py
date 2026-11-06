from project import ROOT, read_json, write_json


def main():
    name = 'cohort148-nitrosdk-breadth-and-coherent-scene-20261102'
    reports = [('evidence/matches/main-nitrosdk18424-20261102.json', 'match_main_nitrosdk18424_20261102.py'),
        ('evidence/matches/main-scene284-20261102.json', 'match_main_scene284_v2_20261102.py'),
        ('evidence/matches/main-tp256-20261102.json', 'match_main_tp256_20261102.py'),
        ('evidence/matches/ov000-20261102-raw-setter933.json', 'match_ov000_raw_setter933_20261102.py')]
    additions = [dict(module=r['module'], mode=r.get('mode', 'arm'), address=r['address'], bytes=r['bytes'])
        for report, _ in reports[:-1] for r in read_json(ROOT / report)['matches']]
    assert len(additions) == 119 and sum(r['bytes'] for r in additions) == 18964
    write_json(ROOT / (name + '-specification.json'), dict(cohort=148, previousAcceptedCohort=147,
        migrations=[dict(module='ov000', mode='arm', address='0x21df200', bytes=16,
            reason='Use measured full-word input/return with low-byte store, closing main0203DB28 unsigned LDRB caller; zero new coverage')],
        packets=[dict(report=r, producer=[p], directProducer=False) for r, p in reports],
        expectedAdditions=additions, originalChecksRetained=True, postSealCommands=[], oracles=[]))
    stage = 'stage_cross_module_cohort148_20261102.py'
    manifests = ['provenance/main-nitrosdk18424-ready-20261102.json',
        'provenance/main-scene284-ready-20261102.json', 'provenance/main-tp256-ready-20261102.json',
        'provenance/handoffs/ov000-setter937-ready-20261102.json',
        'evidence/lanes/save-core/mechanics484-ready-20261102.json',
        'provenance/handoffs/ov001-constructor938-ready-20261102.json']
    extra = [name + '-specification.json', stage, __file__.split('\\')[-1],
        'docs/2026-11-02-cohort148-nitrosdk-breadth-and-coherent-scene.md',
        'record_cohort148_independent_replays_20261102.py',
        'evidence/verification/ov000-setter937-independent-replay-20261102.json',
        'evidence/verification/save-core-mechanics484-independent-replay-20261102.json',
        'evidence/verification/ov001-constructor938-independent-replay-20261102.json']
    assert all((ROOT / p).is_file() for p in extra if p not in [stage, name + '-specification.json'])
    write_json(ROOT / (name + '-package.json'), dict(cohort=148, manifests=manifests,
        archives=['ov000-setter937-20261102', 'save-core-mechanics484-20261102', 'ov001-constructor938-20261102'],
        traces=[], extra=extra))
    (ROOT / stage).write_text("import sys\nimport stage_declared_source_package_v7_20261102 as staging\n\n\nif __name__ == '__main__':\n    sys.argv = [sys.argv[0], '" + name + "-package.json']\n    staging.main()\n", encoding='utf-8')
    print(dict(cohort=148, proposedFunctions=119, proposedBytes=18964, zeroCreditMigrationBytes=16,
        registryMutated=False))


if __name__ == '__main__':
    main()
