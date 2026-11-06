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
FIXTURE='evidence/application/save_core_stat_scaling_fixtures_20261031.py'
ORACLE='evidence/application/save-core-stat-scaling-source-20261031.json'
CONTROL_SCRIPT='evidence/application/save_core_stat_scaling_controls_20261031.py'
CONTROLS='evidence/lanes/save-core/stat-scaling-controls-20261031.json'
CASE_DIGEST='22d48f171a0a34f859e1d635e966a4637c27e59881cf48b1010c15f885d769ff'
CONTROL_DIGEST='819aca710baab5b0002610f4181ecc39eb2fab46a4d0fa65ed2e2b4ebadbc11c'
LENGTHS={0x0207C164:40,0x0207C844:60}


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
    assert oracle['nativeCaseDigest']==CASE_DIGEST and sha(json.dumps(oracle['unitCounts'],sort_keys=True,separators=(',',':')).encode())==CASE_DIGEST
    assert oracle['counts']['contexts']==69071 and oracle['counts']['actualReturns']==138142
    assert controls['counts']['nativeReturns']==26 and controls['counts']['compiledWrongReturns']==26
    assert controls['counts']['independentRejections']==8 and controls['counts']['positiveControls']==18
    for unit in oracle['unitCounts']:
        vectors=unpack(unit['vectorSidecar'],unit['nativeCaseDigest'])
        assert len(vectors)==unit['contexts'] and all(v['actualReturn'] and v['entry']==unit['address'] for v in vectors)
    negatives=unpack(controls['vectorSidecar'],CONTROL_DIGEST)
    assert len(negatives)==26 and sum(v['independentRejected'] for v in negatives)==8
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
        unit=next(u for u in oracle['unitCounts'] if int(u['address'],0)==at)
        signature='(s32 value, s32 divisor)' if length==40 else '(u8 *record, u32 scaleWord, const u8 *features)'
        row.update(outputSha256=sha(linked),linked=False,exactBytes=length,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,
            signature='u32 '+row['name']+signature,oracle=dict(supported=True,cases=unit['contexts'],actualReturns=unit['actualReturns'],
                report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        rows.append(row);entries[row['name']]=own
        for relocation in row['relocations']:
            module,target=relocation['targetModule'],int(relocation['target'],0)
            entries[relocation['symbol']]=data_entry(module,target,cache) if relocation['targetMode']=='data' else native_entry(module,target,cache)
    assert len(rows)==2
    for dependency in oracle['runtimeDependencies']:
        assert sha((ROOT/dependency['path']).read_bytes())==dependency['sha256']
    deps=[d['path'] for d in oracle['runtimeDependencies']]+[s['path'] for s in oracle['vectorSidecars']]+[controls['vectorSidecar']['path']]
    deps += [FIXTURE,CONTROLS,CONTROL_SCRIPT,'evidence/application/save_core_stat_scaling_build_20261031.py',
        'match_mechanics_save_20261031_lane_stat_scaling.py','match_mechanics_save_20261029_record33.py',
        'match_mechanics_save_20261029_item_use.py','source_dependencies.py','provenance/seed-manifest.json']
    deps += [row['source'] for row in rows]+[row['source'] for row in controls['wholeSourceRealLinks']]+[v[0]['symbolsFile'] for v in cache.values()]
    sys.path.insert(0,str(ROOT/'evidence/application'))
    import save_core_stat_scaling_controls_20261031 as ctl
    deps += [d['path'] for d in ctl.F.M.F.runtime_dependencies()]
    verify_inputs()
    report=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=rows,matchedFunctions=2,matchedBytes=100,
        nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items()},
        sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(set(deps))],replayRequires=[],
        oracle=dict(cases=69071,actualReturns=138142,counts=oracle['counts'],providerKinds=0,providedCalls=0,nativeCaseDigest=CASE_DIGEST,
            reports=[r['oracle'] for r in rows],reproductionCommands=[command]),
        negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts']),
        wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-stat-scaling.json';target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(functions=2,bytes=100,actualReturns=138142,reportSha256=sha(target.read_bytes()))))


if __name__=='__main__':
    main()
