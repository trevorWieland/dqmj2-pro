import sys
from project import ROOT, read_json, write_json, sha256, configuration
from ledger_state import collect_matches
import recovery_registry
import prepare_source_cohort_v4_20261102 as original
from qualify_sdk_constant_data_additions_20261106 import selected_data
from wave20261106_gp_character_data_additions import qualify


def main():
    assert sha256(ROOT / 'wave20261106_gp_character_data_additions.py') == '504a250e059d3c81ef030714b4d3e48c68f25bdac9a9b7c4ea851e48f8edf7bc'
    assert len(sys.argv) == 2
    spec = read_json(ROOT / sys.argv[1])
    assert spec['migrations'] == [] and isinstance(spec['dataOnlyCohort'], bool)
    assert len(spec['expectedDataAdditions']) == 259
    assert spec['dataOnlyCohort'] == (spec['expectedAdditions'] == [])
    cohort = spec['cohort']
    assert cohort == spec['previousAcceptedCohort'] + 1
    files = ['prepare_source_cohort_v3_20261102.py', 'prepare_source_cohort_v4_20261102.py',
             'recovery.json', 'source-preferences.json']
    unchanged = {name: sha256(ROOT / name) for name in files}
    before_data = selected_data()
    before_functions, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected
    original.base.classify_additions = original.classify
    original.base.main()
    after_functions, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected
    added_functions = set(after_functions) - set(before_functions)
    wanted = {(row['module'], row['mode'], int(row['address'], 0)): row['bytes'] for row in spec['expectedAdditions']}
    assert added_functions == set(wanted)
    assert all(after_functions[key]['size'] == wanted[key] for key in added_functions)
    for key, row in before_functions.items():
        assert all(after_functions[key].get(field) == row.get(field) for field in
                   ['source', 'sourceSha256', 'object', 'objectSha256', 'size', 'targetSha256'])
    qualification = qualify(before_data, selected_data(), spec['expectedDataAdditions'], after_functions,
                            ROOT / f'work/integration/cohort{cohort}-initialized-data-qualification')
    plan_path = ROOT / f'evidence/verification/cohort-2026-10-29-{cohort}.json'
    plan = read_json(plan_path)
    function_bytes = sum(after_functions[key]['size'] for key in added_functions)
    assert plan['newSourceFunctions'] == len(added_functions) and plan['newSourceBytes'] == function_bytes
    assert plan['newOrdinaryCBytes'] + plan['newVerifiedOriginalAssemblyBytes'] == function_bytes
    assert plan['expectedSourceMatchedFunctions'] == len(after_functions)
    assert sha256(recovery_registry.REGISTRY) == plan['sourceRegistrySha256']
    initialized = qualification['newInitializedDataBytes']
    plan.update(newSourceBytes=function_bytes + initialized,
                expectedSourceLinkedBytes=plan['previousAcceptedBytes'] + function_bytes + initialized,
                newInitializedDataObjects=qualification['newInitializedDataObjects'],
                newInitializedDataBytes=initialized, newEncodedAssetBytes=qualification['newEncodedAssetBytes'],
                newDataAlignmentBytes=qualification['newDataAlignmentBytes'],
                newTypedConstantDataBytes=qualification['newTypedConstantDataBytes'],
                allEarlierDataSourcesAndObjectsPreserved=True, originalFunctionAdmissionGuardsRetained=True)
    assert plan['newSourceBytes'] == function_bytes + plan['newEncodedAssetBytes'] + plan['newDataAlignmentBytes'] + plan['newTypedConstantDataBytes']
    assert unchanged == {name: sha256(ROOT / name) for name in files}
    write_json(plan_path, plan)
    write_json(ROOT / f'evidence/verification/cohort{cohort}-initialized-data-qualification-20261106.json',
        dict(qualification, sourceCredit=0, originalGuardInputs=unchanged,
             generatorSha256=sha256(__file__), qualifierSha256=sha256(ROOT / 'wave20261106_gp_character_data_additions.py')))
    print(dict(cohort=cohort, newFunctions=len(added_functions), newInitializedDataBytes=initialized,
               transactionPreparedOnly=True, originalFunctionGuardsRetained=True))


if __name__ == '__main__':
    main()
