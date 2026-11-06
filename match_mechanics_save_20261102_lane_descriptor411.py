import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry
from match_mechanics_save_20261102_lane_state_dispatch import runtime_files
from source_dependencies import dependencies_current
IDENTITIES='evidence/lanes/save-core/descriptor411-identities-20261102.json'
PRODUCER='evidence/application/save_core_descriptor411_fixtures_20261102.py'
REPORT='evidence/application/save-core-descriptor411-20261102.json'
WINDOWS='check_save_core_descriptor_windows412_20261102.py'
WIN_REPORT='evidence/ports/save-core-descriptor-windows412-20261102.json'
def main():
 verify_inputs();identity=json.loads((ROOT/IDENTITIES).read_text());items=identity['zeroCreditMigrations'];assert len(items)==6
 for item in items:
  for p,k in [('source','sourceSha256'),('historicalSource','historicalSourceSha256')]:assert sha((ROOT/item[p]).read_bytes())==item[k]
 for producer in (PRODUCER,WINDOWS):
  result=subprocess.run([sys.executable,'-I','-S',str(ROOT/producer)],cwd=ROOT,capture_output=True,text=True,timeout=600);assert result.returncode==0,result.stdout+result.stderr
 oracle=json.loads((ROOT/REPORT).read_text());windows=json.loads((ROOT/WIN_REPORT).read_text());assert (oracle['pairs'],oracle['properOriginalAndSourceReturns'],oracle['properWrongReturns'],oracle['wrongReturningRejects'],oracle['wrongPositiveControls'],oracle['actualLookupAndScaleReturns'])==(1152,2304,1152,1116,36,6912)
 sidecar=oracle['sidecar'];packed=(ROOT/sidecar['path']).read_bytes();assert sha(packed)==sidecar['sha256'] and sha(gzip.decompress(packed))==sidecar['caseSha256'];assert windows['nativeCaseSha256']==sidecar['caseSha256'] and (windows['actualPreferredWindowsReturns'],windows['actualWrongWindowsReturns'],windows['wrongRejects'],windows['wrongPositiveControls'])==(1152,1152,1116,36)
 cache={};entries={};matches=[];deps=runtime_files()|{IDENTITIES,PRODUCER,REPORT,WINDOWS,WIN_REPORT,sidecar['path'],'match_mechanics_save_20261102_lane_descriptor411.py','ports/windows-native/descriptor412_runner.c','docs/2026-11-02-descriptor-index-forwarding-alternatives.md'}
 for item,candidate in zip(items,oracle['matches']):
  row=dict(candidate);row.update(row['realLinkSnapshot']);assert row['sourceSha256']==item['sourceSha256'] and row['bytes']==row['compiledBytes']==row['exactBytes']==44 and row['exactByteEqual'] and dependencies_current(row)
  for key,digest in [('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[key]).read_bytes())==row[digest]
  body=(ROOT/row['isolatedCallerBinary']).read_bytes();validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text());own=native_entry('main',int(item['address'],0),cache);assert validation['exactCallerBytes'] and validation['sourceObjectSha256']==row['objectSha256'] and validation['sourceSha256']==item['sourceSha256'];assert validation['linkedCallerSha256']==validation['nativeSpanSha256']==sha(body) and validation['linkerAttempt']['exitCode']==0 and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74';entries[row['name']]=own
  for relocation in row['relocations']:entries[relocation['symbol']]=native_entry('main',int(relocation['target'],0),cache)
  row.update(outputSha256=sha(body),linked=False,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,zeroAdditionalCoverage=True,oracle=dict(cases=192,actualOriginalAndCompiledReturns=384,report=REPORT,reportSha256=sha((ROOT/REPORT).read_bytes()),limits=oracle['limits']),qualifiedSignature='u32(u32,u32); explicit s32 index forwarding to selected449D4(s32); bounded nonnegative index/level only')
  matches.append(row);deps.update((item['source'],item['historicalSource'],'nonmatching/save-core/20261102-descriptor411-controls/'+Path(item['source']).name))
 deps.update(x['path'] for x in windows['helperSources']);deps.update(v[0]['symbolsFile'] for v in cache.values());verify_inputs();output=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=matches,matchedFunctions=6,matchedBytes=264,newFunctions=0,newBytes=0,zeroCreditPrimaryMigrations=6,nativeSymbolEntries=entries,nativeSymbols={name:x['address'] for name,x in entries.items()},nativeSymbolModules={},sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],oracle=dict(actualOriginalAndSourceReturns=2304,actualWrongReturns=1152,actualLookupAndScaleReturns=6912,suppliedFinalCalls=3456,nativeCaseDigest=sidecar['caseSha256']),windows=dict(preferredReturns=1152,wrongReturns=1152,wrongRejects=1116,wrongPositiveControls=36,actualLookupCAndScaleCReturns=4608,report=WIN_REPORT,reportSha256=sha((ROOT/WIN_REPORT).read_bytes())),registrationPerformedByThisScript=False,wholeLinkedRebuild=False,inputsUnchanged=True,limitations=oracle['limits']+windows['limits']);p=ROOT/'evidence/matches/mechanics-save-20261102-lane-descriptor411.json';p.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(dict(migrationBytes=264,newBytes=0,nativeProperReturns=2304,windowsPreferredReturns=1152,reportSha256=sha(p.read_bytes()))))
if __name__=='__main__':main()
