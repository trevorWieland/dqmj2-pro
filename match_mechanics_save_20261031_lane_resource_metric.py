import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,native_entry,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current
FIXTURE='evidence/application/save_core_resource_metric_fixtures_20261031.py'
ORACLE='evidence/application/save-core-resource-metric-source-20261031.json'
CONTROLS='evidence/lanes/save-core/resource-metric-controls-20261031.json'
CONTROL_SCRIPT='evidence/application/save_core_resource_metric_controls_20261031.py'
CASE_DIGEST='412c2b9b90170232dc8e81eda18c256c693bac6345627fe951dc2398804872d9'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4'
    verify_inputs()
    command=[sys.executable,str(ROOT/FIXTURE)]
    for cmd in (command,[sys.executable,str(ROOT/CONTROL_SCRIPT)]):
        process=subprocess.run(cmd,capture_output=True,text=True,timeout=300)
        assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text());controls=json.loads((ROOT/CONTROLS).read_text())
    assert oracle['allContextResultDigest']==CASE_DIGEST
    assert oracle['counts']['contexts']==65658 and oracle['counts']['actualReturns']==131316
    assert controls['counts']['nativeReturns']==48 and controls['counts']['compiledWrongReturns']==48
    assert controls['counts']['independentRejections']==8 and controls['counts']['positiveControls']==40
    rows,entries,cache=[],{},{}
    for raw in oracle['matches']:
        row=dict(raw);row.update(row['realLinkSnapshot'])
        assert row['exactByteEqual'] and row['compiledBytes']==96 and dependencies_current(row)
        for path_key,hash_key in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT/row[path_key]).read_bytes())==row[hash_key]
        at=int(row['address'],0);own=native_entry('main',at,cache)
        assert row['nativeAlias']==own['nativeAlias'] and row['bytes']==own['bytes']==96
        metadata,binary,functions=cache['main'];off=at-int(metadata['base'],0)
        native=binary[off:off+96];linked=(ROOT/row['isolatedCallerBinary']).read_bytes()
        validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
        assert native==linked and len(linked)==96 and validation['exactCallerBytes'] is True
        assert validation['linkerAttempt']['exitCode']==0 and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
        assert validation['sourceSha256']==row['sourceSha256'] and validation['sourceObjectSha256']==row['objectSha256']
        assert validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked)
        row.update(outputSha256=sha(linked),linked=False,exactBytes=96,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,
            signature='u32 '+row['name']+'(u32 key, const s16 *values, s32 count)',oracle=dict(supported=True,cases=65658,actualReturns=131316,
                report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        rows.append(row);entries[row['name']]=own
        for relocation in row['relocations']:
            module,target=relocation['targetModule'],int(relocation['target'],0)
            entries[relocation['symbol']]=data_entry(module,target,cache) if relocation['targetMode']=='data' else native_entry(module,target,cache)
    assert len(rows)==1
    for dependency in oracle['runtimeDependencies']:
        assert sha((ROOT/dependency['path']).read_bytes())==dependency['sha256']
    deps=[d['path'] for d in oracle['runtimeDependencies']]
    deps += [FIXTURE,CONTROLS,CONTROL_SCRIPT,
        'evidence/application/save_core_resource_metric_build_20261031.py','match_mechanics_save_20261031_lane_resource_metric.py',
        'match_mechanics_save_20261029_record33.py','match_mechanics_save_20261029_item_use.py','source_dependencies.py','provenance/seed-manifest.json']
    deps += [row['source'] for row in rows]+[row['source'] for row in controls['wholeSourceRealLinks']]
    deps += [v[0]['symbolsFile'] for v in cache.values()]
    sys.path.insert(0,str(ROOT/'evidence/application'))
    import save_core_resource_metric_controls_20261031 as controller
    deps += [d['path'] for d in controller.F.M.F.runtime_dependencies()]
    verify_inputs()
    report=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=rows,
        matchedFunctions=1,matchedBytes=96,nativeSymbolEntries=entries,
        nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items()},
        sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(set(deps))],replayRequires=[],
        oracle=dict(cases=65658,actualReturns=131316,counts=oracle['counts'],providerKinds=0,providedCalls=0,
            nativeCaseDigest=CASE_DIGEST,reports=[r['oracle'] for r in rows],reproductionCommands=[command]),
        negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts']),
        wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-resource-metric.json'
    target.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(functions=1,bytes=96,actualReturns=131316,reportSha256=sha(target.read_bytes()))))


if __name__=='__main__':
    main()
