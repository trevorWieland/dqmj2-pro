import gzip
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,native_entry,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current
FIXTURE='evidence/application/save_core_selection_transition_fixtures_20261031.py'
ORACLE='evidence/application/save-core-selection-transition-source-20261031.json'
CONTROL_SCRIPT='evidence/application/save_core_selection_transition_controls_20261031.py'
CONTROLS='evidence/lanes/save-core/selection-transition-controls-20261031.json'
CASE_DIGEST='dec5e6fb9469e466822786db0bf5b7ddd8d0759e56088fa496dd3bf7fe327d29'
CONTROL_DIGEST='089cc13940b097c3cb31dec494b62a35a2f757357f571e09d882ee28cb5338ad'
LENGTHS={0x020C1540:184}


def unpack(sidecar,expected):
    raw=(ROOT/sidecar['path']).read_bytes()
    assert sha(raw)==sidecar['sha256'] and len(raw)==sidecar['compressedBytes']
    decoded=gzip.decompress(raw)
    assert sha(decoded)==sidecar['uncompressedSha256']==expected and len(decoded)==sidecar['uncompressedBytes']
    vectors=json.loads(decoded);assert len(vectors)==sidecar['contexts']
    return vectors


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
    assert oracle['counts']['contexts']==324 and oracle['counts']['actualReturns']==648
    assert controls['counts']['nativeReturns']==64 and controls['counts']['compiledWrongReturns']==64
    assert controls['counts']['independentRejections']==30 and controls['counts']['positiveControls']==34
    vectors=unpack(oracle['vectorSidecar'],CASE_DIGEST)
    assert len(vectors)==324 and all(v['actualReturn'] for v in vectors)
    negatives=unpack(controls['vectorSidecar'],CONTROL_DIGEST)
    assert len(negatives)==64 and sum(v['independentRejected'] for v in negatives)==30
    assert all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in negatives)
    rows,entries,cache=[],{},{}
    for raw in oracle['matches']:
        row=dict(raw);row.update(row['realLinkSnapshot']);at=int(row['address'],0);length=LENGTHS[at]
        assert row['exactByteEqual'] and row['compiledBytes']==length and dependencies_current(row)
        for path_key,hash_key in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT/row[path_key]).read_bytes())==row[hash_key]
        own=native_entry('main',at,cache);assert row['nativeAlias']==own['nativeAlias'] and row['bytes']==own['bytes']==length
        metadata,binary,functions=cache['main'];off=at-int(metadata['base'],0)
        native=binary[off:off+length];linked=(ROOT/row['isolatedCallerBinary']).read_bytes()
        validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
        assert native==linked and len(linked)==length and validation['exactCallerBytes'] is True
        assert validation['linkerAttempt']['exitCode']==0 and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
        assert validation['sourceSha256']==row['sourceSha256'] and validation['sourceObjectSha256']==row['objectSha256']
        assert validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked)
        unit=oracle['counts']
        signature='(void)'
        row.update(outputSha256=sha(linked),linked=False,exactBytes=length,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,
            signature='u32 '+row['name']+signature,oracle=dict(supported=True,cases=unit['contexts'],actualReturns=unit['actualReturns'],
                report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        rows.append(row);entries[row['name']]=own
        for relocation in row['relocations']:
            module,target=relocation['targetModule'],int(relocation['target'],0)
            entries[relocation['symbol']]=data_entry(module,target,cache) if relocation['targetMode']=='data' else native_entry(module,target,cache)
    assert len(rows)==1
    for dependency in oracle['runtimeDependencies']:
        assert sha((ROOT/dependency['path']).read_bytes())==dependency['sha256']
    deps=[d['path'] for d in oracle['runtimeDependencies']]+[oracle['vectorSidecar']['path']]+[controls['vectorSidecar']['path']]
    deps += [FIXTURE,CONTROLS,CONTROL_SCRIPT,'evidence/application/save_core_selection_transition_build_20261031.py',
        'match_mechanics_save_20261031_lane_selection_transition.py','match_mechanics_save_20261029_record33.py',
        'match_mechanics_save_20261029_item_use.py','source_dependencies.py','provenance/seed-manifest.json']
    deps += [row['source'] for row in rows]+[row['source'] for row in controls['wholeSourceRealLinks']]+[v[0]['symbolsFile'] for v in cache.values()]
    sys.path.insert(0,str(ROOT/'evidence/application'))
    import save_core_selection_transition_controls_20261031 as ctl
    deps += [d['path'] for d in ctl.F.M.F.runtime_dependencies()]
    verify_inputs()
    report=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=rows,matchedFunctions=1,matchedBytes=184,
        nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items()},
        sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(set(deps))],replayRequires=[],
        oracle=dict(cases=324,actualReturns=648,counts=oracle['counts'],providerKinds=3,providedCalls=oracle['counts']['providedCalls'],nativeCaseDigest=CASE_DIGEST,
            reports=[r['oracle'] for r in rows],reproductionCommands=[command]),
        negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts']),
        wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-selection-transition.json';target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(functions=1,bytes=184,actualReturns=648,reportSha256=sha(target.read_bytes()))))


if __name__=='__main__':
    main()
