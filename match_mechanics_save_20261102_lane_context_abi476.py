import gzip
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry,data_entry
from match_mechanics_save_20261102_lane_state_dispatch import runtime_files
from source_dependencies import dependencies_current
SOURCE='src/mechanics_save/20261102_lane_context_abi/native_main_0209de84.c'
SOURCE_SHA='292ce0e5e04cf36d5a4653853c30f9d0a76e7ee3aa758d8660824fd0485c9619'
OLD='src/mechanics_save/20261101_lane_context_initializer/native_main_0209de84.c'
OLD_SHA='96220af1d7c8d7af3619c870460c1965cc5abb0068cf6109f6c1179cd04e1647'
PRODUCER='evidence/application/save_core_context474_abi_fixtures_20261102.py'
REPORT='evidence/application/save-core-parent474-20261102.json'

def main():
 verify_inputs();assert sha((ROOT/SOURCE).read_bytes())==SOURCE_SHA and sha((ROOT/OLD).read_bytes())==OLD_SHA
 result=subprocess.run([sys.executable,'-I','-S',str(ROOT/PRODUCER)],cwd=ROOT,capture_output=True,text=True,timeout=600);assert result.returncode==0,result.stdout+result.stderr
 r=json.loads((ROOT/REPORT).read_text());assert (r['pairs'],r['properOriginalAndSourceReturns'],r['properWrongReturns'],r['actualHelperReturns'],r['suppliedRngCalls'],r['candidateHelperObservedReturns'])==(200,400,400,130920,800,800)
 assert r['wrongRejects']==[200,200] and r['wrongPositiveControls']==[0,0];side=r['sidecar'];packed=(ROOT/side['path']).read_bytes();assert sha(packed)==side['sha256'] and sha(gzip.decompress(packed))==side['caseSha256']
 row=dict(r['candidate']);row.update(row['realLinkSnapshot']);assert row['sourceSha256']==SOURCE_SHA and row['mode']=='thumb' and row['bytes']==row['compiledBytes']==340 and row['exactByteEqual'] and dependencies_current(row)
 for key,digest in [('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[key]).read_bytes())==row[digest]
 body=(ROOT/row['isolatedCallerBinary']).read_bytes();v=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text());assert v['exactCallerBytes'] and v['sourceSha256']==SOURCE_SHA and v['sourceObjectSha256']==row['objectSha256'] and v['linkedCallerSha256']==v['nativeSpanSha256']==sha(body) and v['linkerAttempt']['exitCode']==0 and v['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
 cache={};entries={row['name']:native_entry('main',0x0209DE84,cache)};assert body==cache['main'][1][0x9DE84:0x9DFD8]
 for rel in row['relocations']:entries[rel['symbol']]=(data_entry if rel['kind']=='data' else native_entry)('main',int(rel['target'],0),cache)
 snapshot='evidence/verification/accepted-cohort143-identities-v2-20261101.json';accepted=json.loads((ROOT/snapshot).read_text())['functions'];previous=next(x for x in accepted if x['processor']=='arm9' and x['module']=='main' and x['address']==0x0209DE84);assert previous['source']==OLD and previous['sourceSha256']==OLD_SHA and previous['bytes']==340
 interfaces=[];deps=runtime_files()|{SOURCE,OLD,PRODUCER,REPORT,side['path'],snapshot,'evidence/application/save_core_parent451_model_20261102.py','evidence/application/save_core_thumb_unit425_20261102.py','match_mechanics_save_20261102_lane_context_abi476.py','docs/2026-11-02-context-constructor-selected-interface-repair.md'}
 for address in (0x020A3D64,0x020A3D70,0x020A3D7C,0x020A2AC8,0x0209F80C):
  item=next(x for x in accepted if x['processor']=='arm9' and x['module']=='main' and x['address']==address);assert sha((ROOT/item['source']).read_bytes())==item['sourceSha256'];interfaces.append(item);deps.add(item['source'])
 deps.update(x['source'] for x in r['controls']);deps.update(x[0]['symbolsFile'] for x in cache.values());row.update(exactBytes=340,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,outputSha256=sha(body),linked=False,ordinaryCReconstruction=True,oracle=dict(supported=True,cases=200,actualReturns=400,qualification='400 original/matchingC proper340 helper returns inside400 original420 parent returns;wrong helpers add400 separate proper returns',report=REPORT,reportSha256=sha((ROOT/REPORT).read_bytes()),limits=r['limits']))
 verify_inputs();out=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=[row],matchedFunctions=1,matchedBytes=340,newFunctions=0,newBytes=0,additionalCoverage=0,sourceMigration=dict(previousSource=OLD,previousSourceSha256=OLD_SHA,preferredSource=SOURCE,preferredSourceSha256=SOURCE_SHA,executableUnchanged=True),nativeSymbolEntries=entries,nativeSymbols={n:e['address'] for n,e in entries.items()},nativeSymbolModules={},sourceDependencies=[],selectedInterfaceClosure=interfaces,replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],oracle=dict(actualParentOriginalAndSourceReturns=400,actualParentWrongReturns=400,properMigrationHelperReturns=800,helperReturnsAreNestedSubset=True,actualAllHelperReturns=130920,suppliedRngCalls=800,nativeCaseDigest=side['caseSha256']),negativeControls=dict(wholeWrongCRejects=[200,200],positiveControls=[0,0],unsupportedParentControls=r['unsupportedControls']),wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limits=r['limits']+['Zero additional native function/byte credit. Only340 Cdeclarations/explicit pointer-to-word conversions change;old source isretained. Signed0 call matches selected820 definition,holder/getter APIs match selectedraw32-bit Ccontracts. No global signature rewrites.'])
 target=ROOT/'evidence/matches/mechanics-save-20261102-lane-context-abi476.json';target.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(zeroCreditBytes=340,properParentReturns=400,properHelperReturns=800,helpers=130920,wrongRejects=[200,200],reportSha256=sha(target.read_bytes()))))
if __name__=='__main__':main()
