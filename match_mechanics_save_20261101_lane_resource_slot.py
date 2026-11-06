import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,native_entry,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import unpack
from match_mechanics_save_20261029_item_use import data_entry
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
from source_dependencies import dependencies_current
from save_core_cleanup_words_fixtures_20261031 import code_bytes
import save_core_resource_slot196_machine_20261101 as M

ORACLE='evidence/application/save-core-resource-slot197-20261101.json'
PRODUCER='evidence/application/save_core_resource_slot197_fixtures_20261101.py'
CASE_SHA='c51cf950c54baf8dbaf5f5d2f55de71fd232df3a685e6ead0f7bee1d775289b9'
CONTROL_SHA='ed6046ea8de2f36cc2e34d9ef81d9d5e055f53eda877673aa3f09bca8a3fa209'
SOURCES={M.LOAD:'8c24f2c62ba833ab5acb71d2022f5fad6e6bd512e8f4ac3ce8c62eb7acd061bd',M.SLOT:'d7e7f33cc92e0d9add0aa08408f4d82a462ec4ee6cf309f5584a3ce13c327515'}


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4'
    verify_inputs()
    process=subprocess.run([sys.executable,str(ROOT/PRODUCER)],capture_output=True,text=True,timeout=900,creationflags=subprocess.CREATE_NO_WINDOW)
    assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text())
    vectors=unpack(oracle['vectorSidecar'],CASE_SHA)
    wrong=unpack(oracle['controls']['vectorSidecar'],CONTROL_SHA)
    assert len(vectors)==870 and all(v['native']['actualReturn'] and v['source']['actualReturn'] for v in vectors)
    assert oracle['counts']==dict(pairs=870,actualEntryReturns=1740,actualHelperReturns=1392,providedCalls=4032)
    assert len(wrong)==8 and sum(v['rejected'] for v in wrong)==4
    assert all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in wrong)
    assert oracle['controls']['counts']==dict(contexts=8,actualEntryReturns=16,independentRejections=4,positiveControls=4)
    assert len(oracle['unsupported'])==1 and not oracle['unsupported'][0]['actualReturn'] and not oracle['unsupported'][0]['postFaultCredit']
    cache,entries,matches={},{},[]
    for candidate in oracle['matches']:
        row=dict(candidate)
        row.update(row['realLinkSnapshot'])
        address=int(row['address'],0)
        assert row['sourceSha256']==SOURCES[address]
        assert row['compiledBytes']==row['bytes']==M.FUNCTIONS[address][0] and row['exactByteEqual'] and dependencies_current(row)
        for key,digest in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT/row[key]).read_bytes())==row[digest]
        own=native_entry('main',address,cache)
        metadata,binary,_=cache['main']
        offset=address-int(metadata['base'],0)
        native=binary[offset:offset+row['bytes']]
        linked=(ROOT/row['isolatedCallerBinary']).read_bytes()
        validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
        assert linked==native and code_bytes(row)==M.FUNCTIONS[address][1] and validation['exactCallerBytes']
        assert validation['sourceSha256']==row['sourceSha256'] and validation['sourceObjectSha256']==row['objectSha256']
        assert validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked)
        assert validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
        assert validation['linkerAttempt']['exitCode']==0
        expected=set(range(0,M.FUNCTIONS[address][1],4))
        assert all(set(v)==expected for v in oracle['ownCodeCoverage'][hex(address)].values())
        selected=[v for v in vectors if int(v['entry'],0)==address]
        row.update(exactBytes=row['bytes'],exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,linked=False,
            outputSha256=sha(linked),oracle=dict(supported=True,cases=len(selected),actualReturns=2*len(selected),report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        matches.append(row)
        entries[row['name']]=own
        for relocation in row['relocations']:
            module=relocation.get('targetModule') or 'main'
            target=int(relocation['target'],0)
            loader=data_entry if relocation['symbol'].startswith('native_data_') else native_entry
            entries[relocation['symbol']]=loader(module,target,cache)
    deps=runtime_files()|{PRODUCER,ORACLE,'match_mechanics_save_20261101_lane_resource_slot.py',
        'evidence/application/save_core_resource_slot196_machine_20261101.py','provenance/seed-manifest.json',
        oracle['vectorSidecar']['path'],oracle['controls']['vectorSidecar']['path']}
    for dependency in oracle['runtimeDependencies']:
        assert sha((ROOT/dependency['path']).read_bytes())==dependency['sha256']
        deps.add(dependency['path'])
    for candidate in [*matches,*oracle['controls']['candidates']]:
        deps.add(candidate['source'])
        deps.update(d['path'] for d in candidate.get('sourceDependencies',[]))
    for origin in ['nonmatching/save-core/20261101-resource-interfaces192/native_main_020445e4.c','nonmatching/save-core/20261101-cache-verified-style195/native_main_0205c448.c']:
        deps.add(origin)
    deps.update(value[0]['symbolsFile'] for value in cache.values())
    verify_inputs()
    output=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=matches,
        matchedFunctions=2,matchedBytes=264,nativeSymbolEntries=entries,nativeSymbols={name:value['address'] for name,value in entries.items()},
        nativeSymbolModules={name:value['module'] for name,value in entries.items() if value['module']!='main'},sourceDependencies=[],
        replayDependencies=[file_identity(Path(p).as_posix()) for p in sorted(deps)],replayRequires=[],
        oracle=dict(cases=870,actualReturns=1740,nativeCaseDigest=CASE_SHA,counts=oracle['counts'],report=ORACLE),
        negativeControls=dict(report=ORACLE,nativeCaseDigest=CONTROL_SHA,counts=oracle['controls']['counts']),
        wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    path=ROOT/'evidence/matches/mechanics-save-20261101-lane-resource-slot.json'
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(dict(functions=2,bytes=264,actualEntryReturns=1740,actualHelperReturns=1392,wrongCActualReturns=16,reportSha256=sha(path.read_bytes())))


if __name__=='__main__':
    main()
