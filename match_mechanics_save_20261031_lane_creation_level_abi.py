import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry,unpack
from source_dependencies import dependencies_current
FIXTURE='evidence/application/save_core_creation_level_fixtures_20261031.py'
ORACLE='evidence/application/save-core-creation-level-abi-source-20261031.json'
CONTROL_SCRIPT='evidence/application/save_core_creation_level_controls_20261031.py'
CONTROLS='evidence/lanes/save-core/creation-level-controls-20261031.json'
CASE_DIGEST='b168b9b839065db4979140ad75aef40f99a76cad0e57e93fe4904da130f674d8'
CONTROL_DIGEST='05c8afe434bee8f6386071753d853bb096c8480894079a8a0f166ff4d6e3c111'
SPECS={0x02044F9C:(16,4096,8192),0x02057CB0:(108,776,1552)}


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4'
    verify_inputs()
    commands=[[sys.executable,str(ROOT/p)] for p in (FIXTURE,CONTROL_SCRIPT)]
    for cmd in commands:
        process=subprocess.run(cmd,capture_output=True,text=True,timeout=300)
        assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text())
    controls=json.loads((ROOT/CONTROLS).read_text())
    assert oracle['counts']['actualReturns']==9744 and oracle['counts']['actualNativeHelperReturns']==26668
    assert oracle['counts']['providedCalls']==3444 and oracle['counts']['providerKinds']==3
    vectors=unpack(oracle['vectorSidecar'],CASE_DIGEST)
    negatives=unpack(controls['vectorSidecar'],CONTROL_DIGEST)
    assert len(vectors)==4872 and all(v['actualReturn'] for v in vectors)
    assert len(negatives)==1088 and sum(v['independentRejected'] for v in negatives)==898
    assert all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in negatives)
    assert len(oracle['unsupported'])==5 and not any(v['actualReturn'] for v in oracle['unsupported'])
    rows,entries,cache=[],{},{}
    for raw in oracle['matches']:
        row=dict(raw)
        row.update(row['realLinkSnapshot'])
        at=int(row['address'],0)
        length,cases,returns=SPECS[at]
        assert row['compiledBytes']==length and row['exactByteEqual'] and row['sourceAlternativeForExistingFunction']
        assert dependencies_current(row)
        for p,h in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT/row[p]).read_bytes())==row[h]
        own=native_entry('main',at,cache)
        assert row['nativeAlias']==own['nativeAlias'] and row['bytes']==own['bytes']==length
        metadata,binary,functions=cache['main']
        off=at-int(metadata['base'],0)
        native=binary[off:off+length]
        linked=(ROOT/row['isolatedCallerBinary']).read_bytes()
        validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
        assert native==linked and len(linked)==length and validation['exactCallerBytes'] is True
        assert validation['linkerAttempt']['exitCode']==0 and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
        assert validation['sourceSha256']==row['sourceSha256'] and validation['sourceObjectSha256']==row['objectSha256']
        assert validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked)
        parameters='(s32 species,s32 unused_variant)' if at==0x02044F9C else '(u32 id)'
        row.update(outputSha256=sha(linked),linked=False,exactBytes=length,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,
            signature='u32 '+row['name']+parameters,oracle=dict(supported=True,cases=cases,actualReturns=returns,
                report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        rows.append(row)
        entries[row['name']]=own
        for rel in row['relocations']:entries[rel['symbol']]=native_entry('main',int(rel['target'],0),cache)
    assert len(rows)==2 and sum(r['bytes'] for r in rows)==124
    for dep in oracle['runtimeDependencies']:assert sha((ROOT/dep['path']).read_bytes())==dep['sha256']
    deps=[d['path'] for d in oracle['runtimeDependencies']]+[oracle['vectorSidecar']['path'],controls['vectorSidecar']['path']]
    deps += [FIXTURE,CONTROL_SCRIPT,CONTROLS,'match_mechanics_save_20261031_lane_creation_level_abi.py',
        'match_mechanics_save_20261031_lane_pointer_sequence.py','source_dependencies.py',
        'evidence/application/save_core_controller_controls_20261031_v2.py',
        'match_mechanics_save_20261029_record33.py','provenance/seed-manifest.json',
        'evidence/attempts/creation-level-control-hook-ownership-20261031.json']
    deps += [r['source'] for r in rows+controls['builds']]+[v[0]['symbolsFile'] for v in cache.values()]
    deps += [r['path'] for r in oracle['retainedPrimaries']]
    for retained in oracle['retainedPrimaries']:assert sha((ROOT/retained['path']).read_bytes())==retained['sha256']
    verify_inputs()
    report=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=rows,
        matchedFunctions=2,matchedBytes=124,sourceCreditAdded=0,sourceAlternativeForExistingFunctions=True,retainedPrimaries=oracle['retainedPrimaries'],
        nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items()},
        sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(set(deps))],replayRequires=[],
        oracle=dict(cases=4872,actualReturns=9744,counts=oracle['counts'],providerKinds=3,providedCalls=3444,
            nativeCaseDigest=CASE_DIGEST,reports=[r['oracle'] for r in rows],reproductionCommands=commands),
        negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts']),
        wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-creation-level-abi.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(functions=2,bytes=124,actualReturns=9744,sourceCreditAdded=0,reportSha256=sha(target.read_bytes()))))


if __name__=='__main__':main()
