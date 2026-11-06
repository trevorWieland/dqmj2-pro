import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry
from match_mechanics_save_20261029_item_use import data_entry
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
from source_dependencies import dependencies_current
SOURCE='src/mechanics_save/20261102_lane_state_dispatch/native_main_0206157c.c'
SOURCE_SHA='42c907c4ef62d20f1fadbb4b0e20ad2429ef4a045ca13dd668ad0cef166f52bd'
REPORT='evidence/application/save-core-dispatch374-20261102.json'
INTERFACES='evidence/abi/save-core-dispatch375-source-interfaces-20261102.json'


def parameters(text):
 args=text[text.index('(')+1:text.rindex(')')].split(',');return [re.sub(r'\s+[A-Za-z_]\w*$','',p.strip()) for p in args]


def main():
 verify_inputs();assert sha((ROOT/SOURCE).read_bytes())==SOURCE_SHA
 producer='evidence/application/save_core_dispatch374_fixtures_20261102.py';p=subprocess.run([sys.executable,'-I','-S',str(ROOT/producer),'--source',SOURCE],cwd=ROOT,capture_output=True,text=True,timeout=600);assert p.returncode==0,p.stdout+p.stderr
 oracle=json.loads((ROOT/REPORT).read_text());assert (oracle['pairs'],oracle['actualOriginalReturns'],oracle['actualCompiledReturns'],oracle['actualWrongReturns'],oracle['wrongReturningRejects'],oracle['wrongReturningPositives'],oracle['wrongBoundaryFailures'],oracle['providedOriginalAndCompiledCalls'],oracle['providedCallbackCalls'])==(3208,3208,3208,3064,0,3064,144,19248,306)
 sidecar=oracle['sidecar'];packed=(ROOT/sidecar['path']).read_bytes();assert sha(packed)==sidecar['sha256'] and sha(gzip.decompress(packed))==sidecar['caseSha256']
 audit=json.loads((ROOT/INTERFACES).read_text());own=(ROOT/SOURCE).read_text();assert len(audit['selectedInterfaces'])==18
 for item in audit['selectedInterfaces']:
  assert sha((ROOT/item['source']).read_bytes())==item['sourceSha256'];assert item['definition'] in (ROOT/item['source']).read_text()
  address=item['identity']['address'];decl=re.search(r'extern\s+(\w+)\s+native_fn_'+format(address,'08x')+r'\([^;]*\);',own)
  if decl:
   assert decl.group(1)==item['definition'].split()[0] and parameters(decl.group())==parameters(item['definition'])
  else:assert item['definition'].startswith('u32 ') and item['definition'].endswith('(void)')
 row=dict(oracle['candidate']);row.update(row['realLinkSnapshot']);assert row['source']==SOURCE and row['sourceSha256']==SOURCE_SHA and row['bytes']==row['compiledBytes']==796 and row['exactByteEqual'] and dependencies_current(row)
 for path,digest in [('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[path]).read_bytes())==row[digest]
 cache={};entries={row['name']:native_entry('main',0x0206157C,cache)};meta,arm,_=cache['main'];body=(ROOT/row['isolatedCallerBinary']).read_bytes();validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
 assert body==arm[0x6157C:0x61898] and validation['exactCallerBytes'] and validation['sourceObjectSha256']==row['objectSha256'] and validation['sourceSha256']==SOURCE_SHA
 assert validation['linkedCallerSha256']==validation['nativeSpanSha256']==sha(body) and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode']==0
 assert sha(arm[0xDAC94:0xDAC94+108])==oracle['callbackTableOriginalSha256']
 for relocation in row['relocations']:entries[relocation['symbol']]=(data_entry if relocation['kind']=='data' else native_entry)('main',int(relocation['target'],0),cache)
 row.update(outputSha256=sha(body),linked=False,exactBytes=796,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,oracle=dict(supported=True,cases=3208,actualReturns=6416,report=REPORT,reportSha256=sha((ROOT/REPORT).read_bytes()),limits=oracle['limits']),returnContract=dict(sourceReturnType='u32',physicalR0Compared=True,apiReturnProven=True,qualifiedReturn='0 or1 across bounded state/provider matrix;no named success meaning'),callbackContracts=dict(selectedSourceAudit=INTERFACES,unselectedTargetsUnresolved=True,actualCallbackExecution=False))
 deps=runtime_files()|{SOURCE,REPORT,INTERFACES,producer,sidecar['path'],'evidence/application/save_core_historical_link_20261031.py','match_mechanics_save_20261102_lane_state_dispatch.py','provenance/seed-manifest.json','nonmatching/save-core/20261102-breadth371/native_main_0206157c.c','docs/2026-11-02-state-dispatch-word-callback-recovery.md'}
 deps.update(item['source'] for item in audit['selectedInterfaces']);deps.update(v[0]['symbolsFile'] for v in cache.values());verify_inputs()
 output=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=[row],matchedFunctions=1,matchedBytes=796,nativeSymbolEntries=entries,nativeSymbols={name:x['address'] for name,x in entries.items()},nativeSymbolModules={},sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],oracle=dict(pairs=3208,actualOriginalReturns=3208,actualCompiledReturns=3208,providedDirectAndCallbackCalls=19248,providedCallbacks=306,nativeCaseDigest=sidecar['caseSha256']),negativeControls=dict(actualWrongReturns=3064,returningPositiveControls=3064,returningRejections=0,memoryFaultControls=144,noPostfaultStateCredit=True),selectedInterfaceAudit=dict(path=INTERFACES,sha256=sha((ROOT/INTERFACES).read_bytes()),selectedDirectAndCallbackSourceRows=18),wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limits'])
 path=ROOT/'evidence/matches/mechanics-save-20261102-lane-state-dispatch.json';path.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(dict(matchedBytes=796,properReturns=6416,wrongReturns=3064,wrongMemoryFaults=144,reportSha256=sha(path.read_bytes()))))


if __name__=='__main__':main()
