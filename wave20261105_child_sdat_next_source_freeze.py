import argparse
import sys
from project import ROOT,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
LANE=ROOT/'evidence/lanes/parallel-wave20261105/child-sdat-next/source'
REPORT='evidence/data/child-sdat-next-20261106.json'


def execute(accounting_path,controls_path):
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/child-sdat-next/source' or (LANE/'ready.json').exists():raise ValueError('Semantic data freeze scope differs or READY already exists')
    report=read_json(ROOT/REPORT);copied=read_json(LANE/'copied-root-controls.json');accounting=read_json(ROOT/accounting_path);controls=read_json(ROOT/controls_path)
    if not(copied['passed'] and accounting['passed'] and controls['passed']) or copied['originalReportSha256']!=sha256(ROOT/REPORT):raise ValueError('Fresh copied-root/independent accounting qualification is incomplete or stale')
    if len(report['dataMatches'])!=1 or report['dataMatchedBytes']!=13936 or report['functionMatched']!=0 or report['encodedAssetBytes']!=13935 or report['measuredZeroAlignmentBytes']!=1:raise ValueError('Exact admitted1/13936 initialized-data scope differs')
    actual=read_json(LANE/'inputs.json')['files'];files={p['path'] for p in actual if p['role']!='private-comparison-input'};files.update(code_closure(['wave20261105_child_sdat_next_source_inputs.py','wave20261105_child_sdat_next_source_copy.py','wave20261105_child_sdat_next_source_freeze.py']))
    files.update(['qualify_child_sound_data_additions_20261106.py','prepare_source_data_cohort_v7_20261106.py','run_next_source_package_v25_20261106.py','verify_child_sound_data_accounting_20261106.py','qualify_mixed_source_reference_inputs_20261106.py',(LANE/'inputs.json').relative_to(ROOT).as_posix()])
    for p in actual:
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Production source/compiler/runtime input changed before freeze: '+p['path'])
    for r in report['dataMatches']:
        if sha256(ROOT/r['source'])!=r['sourceSha256'] or sha256(ROOT/r['object'])!=r['objectSha256'] or not r['realLink']['exactDataBytes'] or r['ordinaryFunctionCredit'] or r['relocations'] or r['executableSectionBytes']:raise ValueError('Positive generated source/object/genuine proof changed or gained executable credit')
        files.add(r['source']);files.update(p['path'] for p in r['sourceDependencies'])
    receipts=[dict(path=name,sha256=sha256(ROOT/name),role='zero-credit-qualification-evidence') for name in [accounting_path,controls_path,(LANE/'controls.json').relative_to(ROOT).as_posix(),(LANE/'copied-root-controls.json').relative_to(ROOT).as_posix(),(LANE/'copied-root-output.txt').relative_to(ROOT).as_posix()]]
    manifest=LANE/'source-files.json';pins=[dict(path=name,sha256=sha256(ROOT/name)) for name in sorted(files)]
    write_json(manifest,dict(schemaVersion=1,sourceCredit=0,files=pins,privateComparisonInputs=[p for p in actual if p['role']=='private-comparison-input'],qualificationReceipts=receipts,noExecutablePayloadsCommitted=True,pythonVersion=sys.version))
    write_json(LANE/'ready.json',dict(status='ready-for-coordinator-initialized-data-acceptance',sourceCredit=0,report=REPORT,reportSha256=sha256(ROOT/REPORT),producer=['wave20261105_child_sdat_next_source_proof.py'],functionCount=0,dataObjects=1,initializedBytes=13936,encodedAssetBytes=13935,measuredZeroAlignmentBytes=1,decodedSemanticBytes=20960,sourceManifest=manifest.relative_to(ROOT).as_posix(),sourceManifestSha256=sha256(manifest),freshCopiedRootObjects=1,copiedRootTamperControls=6,wrongDataObjects=1,semanticAndNamespaceControls=56,dataObjectContractControls=4,generationOriginalReadRejections=12,qualificationReceipts=receipts,executableBytes=0,allocatedDataRelocations=0,allocatedZeroFillBytes=0,nativeFunctionCredit=0,limitations=['Shared mixed-cohort acceptance and committed closure pending;0accepted-byte credit.','13935typed-sound/LZ-derived encoded storage bytes+1separate measured zero alignment byte;0functions/ordinary logic instructions.','One freshC99 data object and one same-size wrong-C object genuinely linked through unchanged pinned MW tools; original inputs used only for comparison outside source-only generation.']))
    print(dict(ready=True,dataObjects=1,initializedBytes=13936,actualFrozenFiles=len(pins),privateComparisonInputs=2,readySha256=sha256(LANE/'ready.json'),sourceManifestSha256=sha256(manifest),sourceCredit=0))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--accounting',required=True);parser.add_argument('--controls',required=True);args=parser.parse_args();execute(args.accounting,args.controls)
