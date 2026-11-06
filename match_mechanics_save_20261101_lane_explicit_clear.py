import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA,native_entry
from match_mechanics_save_20261031_lane_pointer_sequence import unpack
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
import save_core_explicit_clear_fixtures_20261101 as P
import save_core_explicit_clear_controls_20261101 as C
ORACLE='evidence/application/save-core-explicit-clear120-source-20261101.json'
CONTROLS='evidence/application/save-core-explicit-clear120-controls-20261101.json'
PORT='evidence/portability/save-core-explicit-clear120-windows32-20261101.json'
PROFILE='evidence/lanes/save-core/explicit-clear120-profile-20261101.json'
CASE='e750eaa3bcabde23f351ffc2e7b7cf7671796fc5c73a4b0e5348c90d26469393'
CONTROL_CASE='ff336eb3646c54d7ee4b2d83b9a3dc192a2f7b37457776053976cc252fc3d2ec'
PROFILE_SHA='7f5dae39c33c8e7b06bbc84cbe35bb1d9795f9618a0307b261d7bc29438cc31f'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4';verify_inputs();assert sha((ROOT/PROFILE).read_bytes())==PROFILE_SHA
    producers=['evidence/application/save_core_explicit_clear_fixtures_20261101.py','evidence/application/save_core_explicit_clear_controls_20261101.py','check_save_core_explicit_clear_windows32_20261101.py']
    for producer in producers:
        process=subprocess.run([sys.executable,str(ROOT/producer)],capture_output=True,text=True,timeout=300);assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text());controls=json.loads((ROOT/CONTROLS).read_text());port=json.loads((ROOT/PORT).read_text());vectors=unpack(oracle['vectorSidecar'],CASE);negatives=unpack(controls['vectorSidecar'],CONTROL_CASE)
    assert len(vectors)==2560 and all(v['actualReturn'] for v in vectors) and oracle['counts']['actualTopReturns']==7424 and oracle['counts']['physicalNativeHelperReturns']==59904 and oracle['counts']['providedServiceCalls']==37824 and oracle['counts']['unsupportedStops']==2
    assert len(negatives)==62 and sum(v['independentRejection'] for v in negatives)==38 and all(v['actualOriginalReturn'] and v['actualPositiveReturn'] and v['actualWrongReturn'] for v in negatives)
    assert port['receipt']==[0x4A324346,1,2048,2048,2048,1792,256,1792,1792,0,2838162373,0] and port['actualWindowsTypedReturns']==2048 and port['actualWindowsRetainedReturns']==2048 and port['retainedCallerWordRejects']==1792 and port['retainedNullGatePositives']==256
    profiles=json.loads((ROOT/PROFILE).read_text())['rows'];cache={};matches=[];entries={}
    for raw in oracle['matches']:
        row=dict(raw);row.update(row['realLinkSnapshot']);address=int(row['address'],0);p=next(p for p in profiles if int(p['address'],0)==address);length=p['bytes'];assert row['sourceSha256']==p['sourceSha256'] and row['compiledBytes']==row['bytes']==length and row['exactByteEqual'] and dependencies_current(row)
        for path,digest in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[path]).read_bytes())==row[digest]
        own=native_entry('main',address,cache);metadata,binary,config=cache['main'];offset=address-int(metadata['base'],0);native=binary[offset:offset+length];linked=(ROOT/row['isolatedCallerBinary']).read_bytes();validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text());assert native==linked and validation['exactCallerBytes'] and validation['sourceSha256']==row['sourceSha256']
        assert validation['sourceObjectSha256']==row['objectSha256'] and validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked) and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode']==0
        selected=[v for v in vectors if v['entry']==address];assert set.union(*(set(v['ownInstructionOffsets']) for v in selected))==set(range(0,P.M.ENTRIES[address][1],4));returns=len(selected)*(3 if address==P.M.ENTRY else 2)
        row.update(outputSha256=sha(linked),linked=False,exactBytes=length,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,oracle=dict(supported=True,cases=len(selected),actualReturns=returns,report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']),netNewBytes=p['netNewBytes'],zeroNetNewCoverage=address!=P.M.ENTRY)
        row['returnContract']=dict(sourceReturnType='u32',physicalR0Compared=True,apiReturnProven=False,callerConsumptionComplete=False)
        if address!=P.M.ENTRY:
            assert sha((ROOT/p['oldSource']).read_bytes())==p['oldSourceSha256'];prior=next(r for r in oracle['retainedPrimaries'] if int(r['address'],0)==address);assert prior['source']==p['oldSource'] and prior['sourceSha256']==p['oldSourceSha256'] and prior['exactByteEqual'];row['retainedPrimary']=dict(source=p['oldSource'],sourceSha256=p['oldSourceSha256'],bytes=length,untouched=True,zeroNewCredit=True)
        entries[row['name']]=own
        for rel in row['relocations']:
            module='ov000' if rel['symbol'].startswith('native_fn_ov000_') else 'main';entries[rel['symbol']]=(data_entry if rel['kind']=='data' else native_entry)(module,int(rel['target'],0),cache)
        matches.append(row)
    assert len(matches)==3 and sum(r['bytes'] for r in matches)==280 and sum(r['netNewBytes'] for r in matches)==192
    deps=runtime_files()|set(producers)|{ORACLE,CONTROLS,PORT,PROFILE,oracle['vectorSidecar']['path'],controls['vectorSidecar']['path'],'provenance/seed-manifest.json','match_mechanics_save_20261101_lane_explicit_clear.py'}
    rows=matches+[v['match'] for v in controls['controls']]+oracle['retainedPrimaries'];deps.update(r['source'] for r in rows);deps.update(p['oldSource'] for p in profiles);deps.update(v['path'] for v in port['inputSources'])
    for row in rows:deps.update(p['path'] for p in row.get('sourceDependencies',[]))
    for address in [*P.M.ENTRIES,*P.M.HELPERS,*P.M.PROVIDERS]:entries[f'qualified_native_{address:08x}']=native_entry('ov000' if address==0x21F24BC else 'main',address,cache)
    deps.update(v[0]['symbolsFile'] for v in cache.values());verify_inputs()
    out=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=matches,matchedFunctions=3,matchedBytes=280,netNewFunctions=1,netNewBytes=192,zeroCreditAlternatives=2,zeroCreditBytes=88,nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items() if v['module']!='main'},sourceDependencies=[],replayDependencies=[file_identity(Path(p).as_posix()) for p in sorted(deps)],replayRequires=[],oracle=dict(cases=2560,actualReturns=7424,nativeCaseDigest=CASE,report=ORACLE,counts=oracle['counts']),negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts'],nativeCaseDigest=CONTROL_CASE),portableProof=dict(report=PORT,sha256=sha((ROOT/PORT).read_bytes()),actualWindowsTypedReturns=2048,actualWindowsRetainedReturns=2048,receipt=port['receipt']),wholeLinkedRebuild=False,registrationPerformedByThisScript=False,primaryMigrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261101-lane-explicit-clear.json';target.write_text(json.dumps(out,indent=2)+'\n');print(dict(newFunctions=1,newBytes=192,zeroBytes=88,actualReturns=7424,wrongReturns=62,reportSha256=sha(target.read_bytes())))


if __name__=='__main__':main()
