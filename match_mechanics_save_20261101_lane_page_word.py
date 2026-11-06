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
import save_core_page_word220_machine_20261101 as M

ORACLE='evidence/application/save-core-page-word223-20261101.json'
PRODUCER='evidence/application/save_core_page_word223_fixtures_20261101.py'
CASE_SHA='4a9c442abc3db2af2bb4badf85c76088f5a84833710c1ee6b87fc19e86077327'
CONTROL_SHA='9091c014706298dc0a7becd43f2a96b6dbe1871b0eef3eed4814ee0bc5f769cb'
SOURCES={34006720: 'b2014df699b36f8aae685594d9ddfc703256ce0c5f162108ed69698d7e30f3ac', 34015364: 'e650e2e4377d17ee8fb4faeb784b89797d9239cb4ba451bb3789c355ae55383c', 33957040: 'a824eccd1234ff7818729572a76a5eb612167e26151644878fb4aa38af0219f5', 34004176: 'e18fe583dcea96208630155c4424dc51572792dd28bb6e671ff44b780f0e05d6', 33957072: '03c4db53b2c5dbba004219c020addbfb1773876e0d1c5dc6af257809cb7c6f88'}
PREVIOUS={M.SETTER:('src/runtime/runtime07/native_main_020624b0.c','c389722fb94901718c1b73e1ec11668a6ae80069fc1c19f1b196461e21677873'),M.CHANGE:('src/runtime/main-null01/native_main_0206dcd0.c','f15eff03872647638726236bf2882c87f65e9100b5a406eb53f390a8d787a428'),M.MODE:('src/runtime/runtime09/native_main_020624d0.c','5946635eca8099550bdc6e521287ba6cb3baf6ea40e3d345cc8b5a275e27354b')}


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4'
    verify_inputs()
    process=subprocess.run([sys.executable,str(ROOT/PRODUCER)],capture_output=True,text=True,timeout=1200,creationflags=subprocess.CREATE_NO_WINDOW)
    assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text())
    vectors=unpack(oracle['vectorSidecar'],CASE_SHA)
    wrong=unpack(oracle['controls']['vectorSidecar'],CONTROL_SHA)
    assert len(vectors)==15905 and all(v['native']['actualReturn'] and v['source']['actualReturn'] for v in vectors)
    assert oracle['counts']==dict(pairs=15905,actualEntryReturns=31810,actualHelperReturns=82302,providedCalls=900)
    assert len(wrong)==6 and sum(v['rejected'] for v in wrong)==3
    assert all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in wrong)
    assert oracle['controls']['counts']==dict(contexts=6,actualEntryReturns=12,independentRejections=3,positiveControls=3)
    assert len(oracle['unsupported'])==1 and not oracle['unsupported'][0]['actualReturn']
    cache,entries,matches={},{},[]
    for candidate in oracle['matches']:
        row=dict(candidate)
        row.update(row['realLinkSnapshot'])
        address=int(row['address'],0)
        assert row['sourceSha256']==SOURCES[address]
        assert row['compiledBytes']==row['bytes']==M.FUNCTIONS[address][0] and row['exactByteEqual'] and dependencies_current(row)
        for key,digest in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[key]).read_bytes())==row[digest]
        own=native_entry('main',address,cache)
        metadata,binary,_=cache['main']
        offset=address-int(metadata['base'],0)
        native=binary[offset:offset+row['bytes']]
        linked=(ROOT/row['isolatedCallerBinary']).read_bytes()
        validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
        assert linked==native and code_bytes(row)==M.FUNCTIONS[address][1] and validation['exactCallerBytes']
        assert validation['sourceSha256']==row['sourceSha256'] and validation['sourceObjectSha256']==row['objectSha256']
        assert validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked)
        assert validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode']==0
        expected=set(range(0,M.FUNCTIONS[address][1],4))
        coverage=oracle['ownCodeCoverage'][hex(address)]
        assert all(set(v)<=expected for v in coverage.values())
        if address!=M.CHANGE:assert all(set(v)==expected for v in coverage.values())
        selected=[v for v in vectors if int(v['entry'],0)==address]
        if address==M.WORDS:assert all(v['native']['rawReturnWord']==1 and v['independentModel']['typedReturnContract'] for v in selected)
        row.update(exactBytes=row['bytes'],exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,linked=False,outputSha256=sha(linked),coverageClassification='new' if address in [M.WORDS,M.CLAMP] else 'zero-credit preferred source alternative',oracle=dict(supported=True,cases=len(selected),actualReturns=2*len(selected),report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        matches.append(row)
        entries[row['name']]=own
        for relocation in row['relocations']:
            module=relocation.get('targetModule') or 'main'
            target=int(relocation['target'],0)
            loader=data_entry if relocation['symbol'].startswith('native_data_') else native_entry
            entries[relocation['symbol']]=loader(module,target,cache)
    for address,(path,digest) in PREVIOUS.items():assert sha((ROOT/path).read_bytes())==digest
    source_by_address={int(row['address'],0):(ROOT/row['source']).read_text() for row in matches}
    assert 'u32 native_main_020624b0(u32 arg0, u32 arg1)' in source_by_address[M.SETTER]
    for address in [M.CHANGE,M.MODE]:assert 'extern u32 native_fn_020624b0(u32,u32);' in source_by_address[address]
    assert 'extern u32 native_fn_020624b0(u32 arg0, u32 arg1);' in source_by_address[M.CLAMP]
    setter_arguments={call['arguments'][1] for v in vectors for call in v['native']['helperCalls'] if call['entry']==M.SETTER}
    assert {0xFFFFFF80,0xFFFFFFFF,0x80000000}<=setter_arguments
    deps=runtime_files()|{PRODUCER,ORACLE,'match_mechanics_save_20261101_lane_page_word.py','evidence/application/save_core_page_word220_machine_20261101.py','provenance/seed-manifest.json',oracle['vectorSidecar']['path'],oracle['controls']['vectorSidecar']['path']}
    for dependency in oracle['runtimeDependencies']:
        assert sha((ROOT/dependency['path']).read_bytes())==dependency['sha256']
        deps.add(dependency['path'])
    for candidate in [*matches,*oracle['controls']['candidates']]:
        deps.add(candidate['source'])
        deps.update(d['path'] for d in candidate.get('sourceDependencies',[]))
    deps.update(path for path,_ in PREVIOUS.values())
    deps.update(f'nonmatching/save-core/20261101-page-raw-return223/native_main_{address:08x}.c' for address in SOURCES)
    deps.update(value[0]['symbolsFile'] for value in cache.values())
    verify_inputs()
    output=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=matches,matchedFunctions=5,matchedBytes=604,newFunctions=2,newBytes=176,zeroCreditFunctions=3,zeroCreditBytes=428,
        nativeSymbolEntries=entries,nativeSymbols={name:value['address'] for name,value in entries.items()},nativeSymbolModules={name:value['module'] for name,value in entries.items() if value['module']!='main'},sourceDependencies=[],
        replayDependencies=[file_identity(Path(p).as_posix()) for p in sorted(deps)],replayRequires=[],proposedPrimaryMigrations=[dict(address=hex(at),previousSource=path,previousSourceSha256=digest,preferredSource=next(row['source'] for row in matches if int(row['address'],0)==at),preferredSourceSha256=SOURCES[at],newFunctionCredit=0,newByteCredit=0) for at,(path,digest) in PREVIOUS.items()],
        selectedInterfaceClosureRequired=[hex(M.SETTER),hex(M.CHANGE),hex(M.MODE)],oracle=dict(cases=15905,actualReturns=31810,nativeCaseDigest=CASE_SHA,counts=oracle['counts'],report=ORACLE),negativeControls=dict(report=ORACLE,nativeCaseDigest=CONTROL_SHA,counts=oracle['controls']['counts']),wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    path=ROOT/'evidence/matches/mechanics-save-20261101-lane-page-word.json'
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(dict(newFunctions=2,newBytes=176,migrations=3,migrationBytes=428,actualEntryReturns=31810,actualHelperReturns=82302,reportSha256=sha(path.read_bytes())))


if __name__=='__main__':main()
