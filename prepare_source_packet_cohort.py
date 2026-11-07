import argparse
import subprocess
import sys
from unittest.mock import patch
import recovery_registry
import source_selection
from project import ROOT, configuration, read_json, write_json, sha256
from ledger_state import collect_matches
from qualify_child_message_data_additions_20261106 import selected_data
from qualify_mathematical_data_additions import qualify
from source_packet_contracts import local

def committed_bytes(revision, name):
    return subprocess.check_output(['git','show',revision+':'+name], cwd=ROOT)

def prepare(specification, qualification_output):
    spec_path = local(specification)
    spec = read_json(spec_path)
    cohort, previous = spec['cohort'], spec['previousAcceptedCohort']
    if cohort != previous + 1 or spec['expectedCounts'] != dict(newFunctions=12,newFunctionBytes=2824,
            newDataObjects=4,newDataBytes=708,migrationFunctions=52,migrationBytes=13176):
        raise ValueError('Reviewed mathematical-data/function migration cohort required')
    output = (ROOT/qualification_output).resolve()
    if not output.is_relative_to(ROOT/'work') or output.exists():
        raise ValueError('Fresh work-only qualification output required before preparing transactions')
    live = {name:(ROOT/name).read_bytes() for name in ('recovery.json','source-preferences.json','ledger/functions.jsonl')}
    if any(content != committed_bytes(spec['baselineRevision'],name) for name,content in live.items()):
        raise ValueError('Accepted registry, preferences or ledger changed before preparation')
    old = read_json(ROOT/f'evidence/verification/cohort-2026-10-29-{previous}.json')
    if old['linksPending'] or sha256(ROOT/'recovery.json') != old['sourceRegistrySha256'] or sha256(ROOT/'source-preferences.json') != old['sourcePreferenceSha256']:
        raise ValueError('Previous source cohort is not closed at the accepted bindings')
    plan_path = ROOT/f'evidence/verification/cohort-2026-10-29-{cohort}.json'
    if plan_path.exists():
        raise ValueError('Prepared cohort plan already exists; preserve/review it before continuing')
    for item in spec['migrations']:
        evidence = ROOT/f'evidence/abi/{item["module"]}-{int(item["address"],0):08x}-explicit-input-migration-20261101.json'
        if evidence.exists():
            raise ValueError('Legacy preparer would overwrite a frozen migration proof: '+str(evidence))
    before_data = selected_data()
    subprocess.run([sys.executable,str(ROOT/'prepare_source_cohort_migrations_20261101.py'),specification],cwd=ROOT,check=True)
    transaction = ROOT/f'work/integration/cohort{cohort}-recovery-transaction.json'
    preferences = ROOT/f'work/integration/cohort{cohort}-preference-transaction.json'
    original_preferences = source_selection.preferences
    with patch.object(recovery_registry,'REGISTRY',transaction), patch.object(source_selection,'preferences',
            lambda namespace: original_preferences(namespace,path=preferences)):
        after_data = selected_data()
        after_functions, rejected = collect_matches(configuration()['romSha256'])
    if rejected:
        raise ValueError('Prepared source transaction contains rejected functions')
    data = qualify(before_data,after_data,spec['expectedDataAdditions'],after_functions,ROOT/qualification_output)
    plan = read_json(plan_path)
    if plan['newSourceFunctions'] != 12 or plan['newSourceBytes'] != 2824 or plan['duplicateMigrationFunctions'] != 52 or plan['duplicateMigrationBytes'] != 13176:
        raise ValueError('Legacy function/migration accounting differs from the reviewed intake')
    expected_bytes = old['sourceLinkedBytes'] + 2824 + 708
    plan.update(newSourceBytes=3532,expectedSourceLinkedBytes=expected_bytes,
        newInitializedDataObjects=4,newInitializedDataBytes=708,newTypedConstantDataBytes=708,
        newEncodedAssetBytes=0,newDataAlignmentBytes=0,earlierDataRecordsPreserved=len(before_data),
        expectedDataRecords=len(after_data),mathematicalDataQualification=data,
        sourcePacketSpecificationSha256=sha256(spec_path),
        typedDataQualifier='qualify_mathematical_data_additions.py',typedDataQualifierSha256=sha256(ROOT/'qualify_mathematical_data_additions.py'),
        transactionPreparedOnly=True,linksPending=True,fullCleanReplayOfThisCohortProven=False)
    if any((ROOT/name).read_bytes() != content for name,content in live.items()):
        raise ValueError('Preparation changed an accepted live source state')
    write_json(plan_path,plan)
    write_json(ROOT/qualification_output/'qualification.json',data)
    print(dict(cohort=cohort,newFunctions=12,newFunctionBytes=2824,newDataBytes=708,
        zeroCreditMigrationFunctions=52,expectedFunctions=plan['expectedSourceMatchedFunctions'],
        expectedInitializedBytes=expected_bytes,transactionPreparedOnly=True,liveRegistryChanged=False))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specification')
    parser.add_argument('--qualification-output',required=True)
    args = parser.parse_args()
    prepare(args.specification,args.qualification_output)

if __name__ == '__main__':
    main()
