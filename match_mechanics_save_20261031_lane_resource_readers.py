import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,native_entry,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current
FIXTURE='evidence/application/save_core_resource_readers_fixtures_20261031.py'
ORACLE='evidence/application/save-core-resource-readers-source-20261031.json'
CONTROLS='evidence/lanes/save-core/resource-readers-controls-20261031.json'
CONTROL_SCRIPT='evidence/application/save_core_resource_readers_controls_20261031.py'
CASE_DIGEST='49d835f03adf01a309e3b440f6af1afac177e1044b4bc6a23bbd5eccfce2c5d2'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4'
    verify_inputs()
    command=[sys.executable,str(ROOT/FIXTURE)]
    for cmd in (command,[sys.executable,str(ROOT/CONTROL_SCRIPT)]):
        process=subprocess.run(cmd,capture_output=True,text=True,timeout=300)
        assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text());controls=json.loads((ROOT/CONTROLS).read_text())
    assert oracle['nativeCaseDigest']==CASE_DIGEST
    assert oracle['counts']['contexts']==1668 and oracle['counts']['actualHostReturns']==3336
    assert controls['counts']['nativeReturns']==18 and controls['counts']['compiledWrongReturns']==18
    assert controls['counts']['independentRejections']==9 and controls['counts']['positiveControls']==9
    rows,entries,cache=[],{},{}
    for raw in oracle['matches']:
        row=dict(raw);row.update(row['realLinkSnapshot'])
        assert row['exactByteEqual'] and row['compiledBytes']==row['bytes'] and dependencies_current(row)
        for path_key,hash_key in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT/row[path_key]).read_bytes())==row[hash_key]
        at=int(row['address'],0);own=native_entry('main',at,cache)
        assert row['nativeAlias']==own['nativeAlias'] and row['bytes']==own['bytes'] and row['bytes'] in (136,84)
        length=row['bytes']
        metadata,binary,functions=cache['main'];off=at-int(metadata['base'],0)
        native=binary[off:off+length];linked=(ROOT/row['isolatedCallerBinary']).read_bytes()
        validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
        assert native==linked and len(linked)==length and validation['exactCallerBytes'] is True
        assert validation['linkerAttempt']['exitCode']==0 and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
        assert validation['sourceSha256']==row['sourceSha256'] and validation['sourceObjectSha256']==row['objectSha256']
        assert validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked)
        cases=sum(int(v['profile']['entry'],0)==at for v in oracle['vectors'])
        row.update(outputSha256=sha(linked),linked=False,exactBytes=length,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,
            signature='u32 '+row['name']+'(s32 heapWord)',oracle=dict(supported=True,cases=cases,actualReturns=2*cases,
                report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limits']))
        rows.append(row);entries[row['name']]=own
        for relocation in row['relocations']:
            module,target=relocation['targetModule'],int(relocation['target'],0)
            entries[relocation['symbol']]=data_entry(module,target,cache) if relocation['targetMode']=='data' else native_entry(module,target,cache)
    assert len(rows)==2
    for contract in oracle['acceptedAdapterSourceContracts']:
        assert sha((ROOT/contract['path']).read_bytes())==contract['sha256']
    for address in (0x0201D444,0x0203CC2C,0x0201D3DC,0x0202A8E0,0x0203CB8C,0x0202A498):
        own=native_entry('main',address,cache)
        entries[own['nativeAlias']]=own
    for dependency in oracle['runtimeDependencies']:
        assert sha((ROOT/dependency['path']).read_bytes())==dependency['sha256']
    deps=[d['path'] for d in oracle['runtimeDependencies']]
    deps += [FIXTURE,CONTROLS,CONTROL_SCRIPT,'evidence/application/save_core_resource_readers_machine_20261031.py',
        'evidence/application/save_core_resource_readers_build_20261031.py','match_mechanics_save_20261031_lane_resource_readers.py',
        'match_mechanics_save_20261029_record33.py','match_mechanics_save_20261029_item_use.py','source_dependencies.py','provenance/seed-manifest.json']
    deps += [row['source'] for row in rows]+[row['source'] for row in controls['wholeSourceRealLinks']]
    deps += [v[0]['symbolsFile'] for v in cache.values()]
    deps += [contract['path'] for contract in oracle['acceptedAdapterSourceContracts']]
    verify_inputs()
    report=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=rows,
        matchedFunctions=2,matchedBytes=220,nativeSymbolEntries=entries,
        nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items()},
        sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(set(deps))],replayRequires=[],
        oracle=dict(cases=1668,actualReturns=3336,counts=oracle['counts'],providerKinds=4,providedCalls=oracle['counts']['suppliedBoundaryCompletions'],
            nativeCaseDigest=CASE_DIGEST,reports=[r['oracle'] for r in rows],reproductionCommands=[command]),
        negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts']),
        acceptedAdapterSourceContracts=oracle['acceptedAdapterSourceContracts'],unsupported=oracle['unsupported'],
        wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limits'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-resource-readers.json'
    target.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(functions=2,bytes=220,actualReturns=3336,reportSha256=sha(target.read_bytes()))))


if __name__=='__main__':
    main()
