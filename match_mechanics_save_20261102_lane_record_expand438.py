import gzip
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
SOURCE='src/mechanics_save/20261102_lane_record_expand/native_main_020ae0e4.c'
PRODUCER='evidence/application/save_core_record_expand436_fixtures_20261102.py'
REPORT='evidence/application/save-core-record-expand436-20261102.json'
AUDIT='audit_save_core_record437_callers_20261102.py'
AUDIT_REPORT='evidence/abi/save-core-record437-callers-20261102.json'
def main():
 verify_inputs()
 for script in (PRODUCER,AUDIT):
  p=subprocess.run([sys.executable,'-I','-S',str(ROOT/script)],cwd=ROOT,capture_output=True,text=True,timeout=600);assert p.returncode==0,p.stdout+p.stderr
 r=json.loads((ROOT/REPORT).read_text());audit=json.loads((ROOT/AUDIT_REPORT).read_text());assert len(audit['callerRows'])==2;assert (r['pairs'],r['properOriginalAndSourceReturns'],r['properWrongReturns'],r['actualHelperReturns'],r['providedFunctions'])==(512,1024,1024,26624,0) and r['wrongRejects']==[256,512] and r['wrongPositiveControls']==[256,0];side=r['sidecar'];packed=(ROOT/side['path']).read_bytes();assert sha(packed)==side['sha256'] and sha(gzip.decompress(packed))==side['caseSha256'];row=dict(r['candidate']);row.update(row['realLinkSnapshot']);assert row['source']==SOURCE and row['sourceSha256']==sha((ROOT/SOURCE).read_bytes()) and row['compiledBytes']==row['bytes']==512 and row['mode']=='thumb' and row['exactByteEqual'] and dependencies_current(row)
 for key,digest in [('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[key]).read_bytes())==row[digest]
 body=(ROOT/row['isolatedCallerBinary']).read_bytes();v=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text());assert v['exactCallerBytes'] and v['sourceObjectSha256']==row['objectSha256'] and v['sourceSha256']==row['sourceSha256'] and v['linkedCallerSha256']==v['nativeSpanSha256']==sha(body) and v['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and v['linkerAttempt']['exitCode']==0;cache={};entries={row['name']:native_entry('main',0x020AE0E4,cache)};meta,arm,cfg=cache['main'];assert body==arm[0xAE0E4:0xAE2E4]
 for relocation in row['relocations']:entries[relocation['symbol']]=native_entry('main',int(relocation['target'],0),cache)
 row.update(outputSha256=sha(body),linked=False,exactBytes=512,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,oracle=dict(supported=True,cases=512,actualReturns=1024,report=REPORT,reportSha256=sha((ROOT/REPORT).read_bytes()),limits=r['limits']),returnContract=dict(sourceReturnType='void',rawPhysicalR0Compared=True,apiReturnClaim=False,callerAudit=AUDIT_REPORT,qualification='Bothobserveddirectcallers overwriteR0 beforeuse;indirect callers/universal originalCsignature unproved'),ordinaryCReconstruction=True)
 selected='src/runtime/runtime08/native_main_0201d780.c';selectedSha='3b6cccd2d61888cf2a9d5519e1cce25365bb5a33bc41ecb7bb46a261b65c7cdb';assert sha((ROOT/selected).read_bytes())==selectedSha;deps=runtime_files()|{SOURCE,PRODUCER,REPORT,AUDIT,AUDIT_REPORT,side['path'],selected,'evidence/application/save_core_thumb_unit425_20261102.py','match_mechanics_save_20261102_lane_record_expand438.py','docs/2026-11-02-bounded-record-expansion-matching-source.md','nonmatching/save-core/20261102-breadth434/native_main_020ae0e4.c'};deps.update(x['source'] for x in r['controls']);deps.update(x[0]['symbolsFile'] for x in cache.values());verify_inputs();out=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=[row],matchedFunctions=1,matchedBytes=512,nativeSymbolEntries=entries,nativeSymbols={name:x['address'] for name,x in entries.items()},nativeSymbolModules={},sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],oracle=dict(actualOriginalAndSourceReturns=1024,actualWrongReturns=1024,actualNativeHelperReturns=26624,providedFunctions=0,nativeCaseDigest=side['caseSha256']),negativeControls=dict(rejects=[256,512],positiveControls=[256,0]),callerAudit=dict(path=AUDIT_REPORT,sha256=sha((ROOT/AUDIT_REPORT).read_bytes()),directCallers=2),wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limits=r['limits']);p=ROOT/'evidence/matches/mechanics-save-20261102-lane-record-expand438.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(matchedBytes=512,properReturns=1024,wrongReturns=1024,helpers=26624,providedFunctions=0,reportSha256=sha(p.read_bytes()))))
if __name__=='__main__':main()
