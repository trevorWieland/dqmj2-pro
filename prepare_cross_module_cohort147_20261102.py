from project import ROOT, read_json, write_json


def main():
    name = 'cohort147-arm7-cam-bootstrap-and-native-constructor-20261102'
    report = 'evidence/matches/arm7-sdk405-cam-bootstrap292-20261102.json'
    specification = dict(cohort=147, previousAcceptedCohort=146, migrations=[],
        packets=[dict(report=report, producer=['validate_arm7_sdk407_cam_bootstrap_20261102.py'], directProducer=False)],
        expectedAdditions=[dict(module=r['module'], mode=r.get('mode', 'arm'), address=r['address'], bytes=r['bytes'])
            for r in read_json(ROOT / report)['matches']],
        originalChecksRetained=True, postSealCommands=[], oracles=[])
    assert len(specification['expectedAdditions']) == 2
    assert sum(r['bytes'] for r in specification['expectedAdditions']) == 292
    write_json(ROOT / (name + '-specification.json'), specification)
    stage = 'stage_cross_module_cohort147_20261102.py'
    manifests = ['provenance/arm7-sdk409-cam-bootstrap292-handoff-20261102.json',
        'evidence/lanes/save-core/mechanics475-ready-20261102.json',
        'provenance/handoffs/ov001-constructor928-ready-20261102.json']
    extra = [name + '-specification.json', stage, __file__.split('\\')[-1],
        'docs/2026-11-02-cohort147-arm7-cam-bootstrap-and-native-constructor.md',
        'docs/2026-11-02-application-integration-evidence-update-v5.md',
        'record_cohort147_independent_replays_20261102.py',
        'evidence/verification/arm7-sdk409-independent-replay-20261102.json',
        'evidence/verification/save-core-mechanics475-independent-replay-20261102.json',
        'evidence/verification/ov001-constructor928-independent-replay-20261102.json',
        'probe_mwcc_clz_c_intrinsics_20261102.py',
        'evidence/attempts/mwcc-clz-c-intrinsic-probes-20261102.json',
        'draft_main_arrange760_recursive_closure_20261102.py',
        'evidence/attempts/main-arrange760-recursive-closure-20261102.json',
        'draft_main_arrange760_ordinary_clz_20261102.py',
        'evidence/attempts/main-arrange760-ordinary-clz-20261102.json',
        'nonmatching/main/20261102-arrange760-ordinary-clz/native_main_02036538.c',
        'draft_main_arrange760_typed_storage_20261102.py',
        'evidence/attempts/main-arrange760-typed-storage-20261102.json',
        'nonmatching/main/20261102-arrange760-typed-storage/native_main_02036538.c',
        'draft_main_scene284_store_paths_20261102.py',
        'evidence/attempts/main-scene284-store-paths-20261102.json',
        'nonmatching/main/20261102-scene284-store-paths/native_main_0203db28.c',
        'draft_main_scene284_store_paths_v2_20261102.py',
        'evidence/attempts/main-scene284-store-paths-v2-20261102.json',
        'nonmatching/main/20261102-scene284-store-paths-v2/native_main_0203db28.c',
        'review_main_scene284_selected_interfaces_20261102.py',
        'evidence/abi/main-scene284-selected-interface-review-20261102.json']
    assert all((ROOT / p).is_file() for p in extra if p not in [stage, name + '-specification.json'])
    write_json(ROOT / (name + '-package.json'), dict(cohort=147, manifests=manifests,
        archives=['arm7-sdk409-cam-bootstrap292-20261102', 'save-core-mechanics475-20261102',
            'ov001-constructor928-20261102'], traces=[], extra=extra))
    (ROOT / stage).write_text("import sys\nimport stage_declared_source_package_v7_20261102 as staging\n\n\nif __name__ == '__main__':\n    sys.argv = [sys.argv[0], '" + name + "-package.json']\n    staging.main()\n", encoding='utf-8')
    print(dict(cohort=147, proposedFunctions=2, proposedBytes=292, researchSourceCredit=0, registryMutated=False))


if __name__ == '__main__':
    main()
