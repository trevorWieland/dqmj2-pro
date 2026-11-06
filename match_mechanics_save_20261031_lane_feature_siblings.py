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
FIXTURE='evidence/application/save_core_feature_siblings_fixtures_20261031.py'
ORACLE='evidence/application/save-core-feature-siblings-source-20261031.json'
CONTROLS='evidence/lanes/save-core/feature-siblings-controls-20261031.json'
CONTROL_SCRIPT='evidence/application/save_core_feature_siblings_controls_20261031.py'
CASE_DIGEST='7317792e83b4c44f76a8e754dfae12f6e4a0ddc15eb5aa4583ead49313055d68'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4'
    verify_inputs()
    command=[sys.executable,str(ROOT/FIXTURE)]
    for cmd in (command,[sys.executable,str(ROOT/CONTROL_SCRIPT)]):
        process=subprocess.run(cmd,capture_output=True,text=True,timeout=300)
        assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text());controls=json.loads((ROOT/CONTROLS).read_text())
    sidecar=oracle['vectorSidecar']
    compressed=(ROOT/sidecar['path']).read_bytes()
    assert sha(compressed)==sidecar['sha256'] and len(compressed)==sidecar['compressedBytes']
    vector_raw=gzip.decompress(compressed)
    assert sha(vector_raw)==CASE_DIGEST==sidecar['uncompressedSha256'] and len(vector_raw)==sidecar['uncompressedBytes']
    vectors=json.loads(vector_raw)
    assert len(vectors)==12390 and all(v['result']['actualReturn'] is True for v in vectors)
    for unit in oracle['unitCounts']:
        assert sum(v['unit']==unit['address'] for v in vectors)==unit['contexts']==4130
    assert oracle['nativeCaseDigest']==CASE_DIGEST
    assert oracle['counts']['contexts']==12390 and oracle['counts']['actualReturns']==24780
    assert controls['counts']['nativeReturns']==24 and controls['counts']['compiledWrongReturns']==24
    assert controls['counts']['independentRejections']==6 and controls['counts']['positiveControls']==18
    rows,entries,cache=[],{},{}
    for raw in oracle['matches']:
        row=dict(raw);row.update(row['realLinkSnapshot'])
        assert row['exactByteEqual'] and row['compiledBytes']==264 and dependencies_current(row)
        for path_key,hash_key in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT/row[path_key]).read_bytes())==row[hash_key]
        at=int(row['address'],0);own=native_entry('main',at,cache)
        assert row['nativeAlias']==own['nativeAlias'] and row['bytes']==own['bytes']==264
        metadata,binary,functions=cache['main'];off=at-int(metadata['base'],0)
        native=binary[off:off+264];linked=(ROOT/row['isolatedCallerBinary']).read_bytes()
        validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
        assert native==linked and len(linked)==264 and validation['exactCallerBytes'] is True
        assert validation['linkerAttempt']['exitCode']==0 and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
        assert validation['sourceSha256']==row['sourceSha256'] and validation['sourceObjectSha256']==row['objectSha256']
        assert validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked)
        row.update(outputSha256=sha(linked),linked=False,exactBytes=264,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,
            signature='u32 '+row['name']+'(const u8 *record, const u8 *features)',oracle=dict(supported=True,cases=4130,actualReturns=8260,
                report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        rows.append(row);entries[row['name']]=own
        for relocation in row['relocations']:
            module,target=relocation['targetModule'],int(relocation['target'],0)
            entries[relocation['symbol']]=data_entry(module,target,cache) if relocation['targetMode']=='data' else native_entry(module,target,cache)
    assert len(rows)==3
    for dependency in oracle['runtimeDependencies']:
        assert sha((ROOT/dependency['path']).read_bytes())==dependency['sha256']
    deps=[d['path'] for d in oracle['runtimeDependencies']]+[sidecar['path']]
    deps += [FIXTURE,CONTROLS,CONTROL_SCRIPT,
        'evidence/application/save_core_feature_siblings_build_20261031.py','match_mechanics_save_20261031_lane_feature_siblings.py',
        'match_mechanics_save_20261029_record33.py','match_mechanics_save_20261029_item_use.py','source_dependencies.py','provenance/seed-manifest.json']
    deps += [row['source'] for row in rows]+[row['source'] for row in controls['wholeSourceRealLinks']]
    deps += [v[0]['symbolsFile'] for v in cache.values()]
    sys.path.insert(0,str(ROOT/'evidence/application'))
    import save_core_feature_siblings_controls_20261031 as controller
    deps += [d['path'] for d in controller.F.M.F.runtime_dependencies()]
    verify_inputs()
    report=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=rows,
        matchedFunctions=3,matchedBytes=792,nativeSymbolEntries=entries,
        nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items()},
        sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(set(deps))],replayRequires=[],
        oracle=dict(cases=12390,actualReturns=24780,counts=oracle['counts'],providerKinds=0,providedCalls=0,
            nativeCaseDigest=CASE_DIGEST,reports=[r['oracle'] for r in rows],reproductionCommands=[command]),
        negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts']),
        wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-feature-siblings.json'
    target.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(functions=3,bytes=792,actualReturns=24780,reportSha256=sha(target.read_bytes()))))


if __name__=='__main__':
    main()
