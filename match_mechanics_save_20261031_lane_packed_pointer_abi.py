import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry,unpack
from source_dependencies import dependencies_current
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
import save_core_packed_pointer_abi_fixtures_20261031 as P
import check_save_core_packed_pointer_windows32_20261031 as W
ORACLE='evidence/application/save-core-packed-pointer-abi-source-20261031.json'
PORT='evidence/portability/save-core-packed-pointer-abi-windows32-20261031.json'
PROFILE='evidence/lanes/save-core/packed-pointer-abi-profile-20261031.json'
CASE='a2b96a2aaac8eb2797d13dea6e4f0d2c7d7f78928d28390bee51db8cf2a779a9'
PROFILE_SHA='0d689e04e9e53478ff785db8e209a89a71fa344d92b2c64236c9df0e115e0d39'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4';verify_inputs();assert sha((ROOT/PROFILE).read_bytes())==PROFILE_SHA
    producers=['evidence/application/save_core_packed_pointer_abi_fixtures_20261031.py','check_save_core_packed_pointer_windows32_20261031.py']
    for producer in producers:
        process=subprocess.run([sys.executable,str(ROOT/producer)],capture_output=True,text=True,timeout=300);assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text());port=json.loads((ROOT/PORT).read_text());vectors=unpack(oracle['vectorSidecar'],CASE);assert len(vectors)==768 and all(v['native']['actualReturn'] and v['wrongCaller']['actualReturn'] and v['typedEqual'] for v in vectors)
    assert oracle['counts']['actualOriginalAndTypedTopReturns']==1536 and oracle['counts']['actualWrongCallerReturns']==768 and oracle['counts']['independentWrongCallerRejections']==282 and oracle['counts']['providers']==0
    assert port['actualWindowsPublicReturns']==12288 and port['failures']==0 and len(port['oldInterfaceCompileRejections'])==6 and port['nativeCaseDigest']==CASE
    profiles=json.loads((ROOT/PROFILE).read_text())['rows'];cache={};matches=[];entries={}
    for raw in oracle['matches']:
        row=dict(raw);row.update(row['realLinkSnapshot']);address=int(row['address'],0);p=next(p for p in profiles if int(p['address'],0)==address);length=p['bytes'];assert row['sourceSha256']==p['sourceSha256'] and row['compiledBytes']==row['bytes']==length and row['exactByteEqual'] and dependencies_current(row)
        assert sha((ROOT/p['expectedPrimarySource']).read_bytes())==p['expectedPrimarySourceSha256']
        for path,digest in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[path]).read_bytes())==row[digest]
        own=native_entry('main',address,cache);metadata,binary,config=cache['main'];offset=address-int(metadata['base'],0);native=binary[offset:offset+length];linked=(ROOT/row['isolatedCallerBinary']).read_bytes();validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text());assert native==linked and validation['exactCallerBytes'] and validation['sourceSha256']==row['sourceSha256']
        assert validation['sourceObjectSha256']==row['objectSha256'] and validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked) and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode']==0
        row.update(outputSha256=sha(linked),linked=False,exactBytes=length,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,migrationOnly=True,newExecutableBytes=0,expectedPrimarySource=p['expectedPrimarySource'],expectedPrimarySourceSha256=p['expectedPrimarySourceSha256'],oracle=dict(supported=True,cases=128,actualReturns=256,report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        entries[row['name']]=own
        for rel in row['relocations']:entries[rel['symbol']]=native_entry('main',int(rel['target'],0),cache)
        matches.append(row)
    assert len(matches)==6 and sum(r['bytes'] for r in matches)==140
    deps=runtime_files()|set(producers)|{ORACLE,PORT,PROFILE,oracle['vectorSidecar']['path'],'provenance/seed-manifest.json','match_mechanics_save_20261031_lane_packed_pointer_abi.py',W.RUNNER,W.LEAF,'evidence/verification/packed-pointer-abi-host-tools-20261031.json'}
    rows=matches+oracle['scopeCallers']+oracle['compiledWrongCallers'];deps.update(r['source'] for r in rows)
    for p in profiles:deps.add(p['expectedPrimarySource'])
    for row in rows:deps.update(p['path'] for p in row.get('sourceDependencies',[]))
    deps.update(v[0]['symbolsFile'] for v in cache.values());verify_inputs()
    toolmeta=json.loads((ROOT/'evidence/verification/packed-pointer-abi-host-tools-20261031.json').read_text())
    out=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=matches,matchedFunctions=6,matchedBytes=140,newMatchedFunctions=0,newMatchedBytes=0,sourceMigrations=6,migrationOnly=True,nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items()},sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],runtimeToolDependencies=[{k:p[k] for k in ('path','sha256','bytes')} for p in toolmeta['files']],oracle=dict(cases=768,actualReturns=1536,nativeCaseDigest=CASE,report=ORACLE,counts=oracle['counts']),wrongCallerControls=dict(actualReturns=768,rejections=282),windows32=dict(report=PORT,sha256=sha((ROOT/PORT).read_bytes()),actualPublicReturns=12288,legacyContractCompileRejections=6),expectedPrimaries=oracle['expectedPrimaries'],wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations']+port['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-packed-pointer-abi.json';target.write_text(json.dumps(out,indent=2)+'\n');print(dict(sourceMigrations=6,migrationBytes=140,newCoverage=0,actualNativePairReturns=1536,actualWindowsPublicReturns=12288,reportSha256=sha(target.read_bytes())))


if __name__=='__main__':main()
