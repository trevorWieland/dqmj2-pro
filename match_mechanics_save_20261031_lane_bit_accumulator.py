import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry,unpack
from source_dependencies import dependencies_current
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
import save_core_bit_accumulator_fixtures_20261031 as P
ORACLE='evidence/application/save-core-bit-accumulator-source-20261031.json'
CONTROLS='evidence/application/save-core-bit-accumulator-controls-20261031.json'
PROFILE=P.PROFILE
CASE='9750deead0311958842ebc2a4d9f6d141d31fcc0179fca2b288f67b737dd67f7'
CONTROL_CASE='2da275a00197787dc08433d9b9d052f881bbcafb7ab93cc2d6edc7d08e78e1a9'
PROFILE_SHA='20571e3d032808725f4e80eee0a9e79f0d0d2fee328a4c13a3386d0c37e0ff2d'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4';verify_inputs();assert sha((ROOT/PROFILE).read_bytes())==PROFILE_SHA
    producers=['evidence/application/save_core_bit_accumulator_fixtures_20261031.py','evidence/application/save_core_bit_accumulator_controls_20261031.py','check_save_core_bit_accumulator_ports_20261031.py']
    for producer in producers:
        result=subprocess.run([sys.executable,str(ROOT/producer)],capture_output=True,text=True,timeout=300);assert result.returncode==0,result.stdout+result.stderr
    oracle=json.loads((ROOT/ORACLE).read_text());controls=json.loads((ROOT/CONTROLS).read_text());vectors=unpack(oracle['vectorSidecar'],CASE);negatives=unpack(controls['vectorSidecar'],CONTROL_CASE);assert len(vectors)==1536 and oracle['counts']['actualTopReturns']==3072 and oracle['counts']['providerCalls']==0 and oracle['counts']['dataMemoryAccesses']==0;assert all(v['actualReturn'] and v['returnWord']==P.expected(v['word']) for v in vectors);assert set.union(*(set(v['instructionOffsets']) for v in vectors))==set(range(0,38,2));assert len(negatives)==3072 and sum(v['independentRejection'] for v in negatives)==1536 and all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in negatives)
    row=dict(oracle['matches'][0]);row.update(row['realLinkSnapshot']);p=json.loads((ROOT/PROFILE).read_text())['rows'][0];assert row['sourceSha256']==p['sourceSha256'] and row['compiledBytes']==row['bytes']==38 and row['exactByteEqual'] and dependencies_current(row)
    for path,digest in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[path]).read_bytes())==row[digest]
    cache={};own=native_entry('main',P.ENTRY,cache);metadata,binary,config=cache['main'];native=binary[0xA771C:0xA7742];linked=(ROOT/row['isolatedCallerBinary']).read_bytes();validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text());assert native==linked and validation['exactCallerBytes'] and validation['sourceSha256']==row['sourceSha256'] and validation['sourceObjectSha256']==row['objectSha256'] and validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked) and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode']==0
    row.update(outputSha256=sha(linked),linked=False,exactBytes=38,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,oracle=dict(supported=True,cases=1536,actualReturns=3072,report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']),returnContract=dict(sourceReturnType='u32',inputView='u32',rawR0ProducedAndCompared=True,semanticNameProven=False,consumerAuditComplete=False))
    port_path='evidence/portability/save-core-bit-accumulator-ports-20261031.json';port=json.loads((ROOT/port_path).read_text());assert port['actualWindowsPublicReturns']==1536 and port['androidExecutions']==0 and port['failures']==0 and port['nativeCaseDigest']==CASE and port['androidBuild']['machine']=='EM_AARCH64' and port['androidBuild']['undefinedSymbols']==0
    deps=runtime_files()|set(producers)|{ORACLE,CONTROLS,PROFILE,oracle['vectorSidecar']['path'],controls['vectorSidecar']['path'],port_path,'ports/windows-native/bit_accumulator_runner_20261031.c','check_save_core_packed_pointer_windows32_20261031.py','evidence/verification/packed-pointer-abi-host-tools-20261031.json','match_mechanics_save_20261031_lane_bit_accumulator.py','provenance/seed-manifest.json'};rows=[row]+controls['builds'];deps.update(r['source'] for r in rows)
    for r in rows:deps.update(p['path'] for p in r.get('sourceDependencies',[]))
    deps.update(v[0]['symbolsFile'] for v in cache.values());verify_inputs();entries={row['name']:own}
    out=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=[row],matchedFunctions=1,matchedBytes=38,nativeSymbols={row['name']:own['address']},nativeSymbolEntries=entries,nativeSymbolModules={},sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],oracle=dict(cases=1536,actualReturns=3072,nativeCaseDigest=CASE,report=ORACLE,counts=oracle['counts']),negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts'],nativeCaseDigest=CONTROL_CASE),portableExecution=dict(report=port_path,sha256=sha((ROOT/port_path).read_bytes()),actualWindowsPublicReturns=1536,androidBuildOnly=True,androidExecutions=0),wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations']);path=ROOT/'evidence/matches/mechanics-save-20261031-lane-bit-accumulator.json';path.write_text(json.dumps(out,indent=2)+'\n');print(dict(functions=1,bytes=38,actualTopReturns=3072,wrongTopReturns=6144,windowsReturns=1536,reportSha256=sha(path.read_bytes())))


if __name__=='__main__':main()
