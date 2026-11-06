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
from match_mechanics_save_20261029_item_use import data_entry
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
from source_dependencies import dependencies_current
NATIVE='evidence/application/save-core-draw-forward352-20261102.json'
PORT='evidence/ports/save-core-draw-windows353-20261102.json'
CASE='e853f74f16380cda67fe03f55dd558a88ca876fd8ce97bbba5168570fedd4f4d'
WIN_CASE='4381bccd279b16a546378b047e5ec74b4b43d9d69586aaa93cb2919cc80eb49b'
SOURCE='src/mechanics_save/20261102_lane_draw_forward/native_main_02061c1c.c'
SOURCE_SHA='59f18e6dcd4279d337789939c6a29c1a25a84433aae72e1fae75383dc714eca3'
OLD='src/runtime/runtime09/native_main_02061c1c.c'
OLD_SHA='1415b293183555253ab688658fd41d55ea74a32e16cd89311ab0afb4faf9f9f9'


def sidecar(row,digest):
 raw=(ROOT/row['path']).read_bytes();assert sha(raw)==row['sha256'] and sha(gzip.decompress(raw))==digest


def main():
 verify_inputs();assert sha((ROOT/SOURCE).read_bytes())==SOURCE_SHA and sha((ROOT/OLD).read_bytes())==OLD_SHA
 expected=(ROOT/OLD).read_text().replace('extern u32 native_fn_02061dcc();','extern u32 native_fn_02061dcc(s32);').replace('temp_r0 = native_fn_02061dcc();','temp_r0 = native_fn_02061dcc((s32)arg0);')
 assert (ROOT/SOURCE).read_text()==expected and expected!=(ROOT/OLD).read_text()
 producers=['evidence/application/save_core_draw_forward352_fixtures_20261102.py','check_save_core_draw_windows353_20261102.py']
 for producer in producers:
  p=subprocess.run([sys.executable,'-I','-S',str(ROOT/producer)],cwd=ROOT,capture_output=True,text=True,timeout=600);assert p.returncode==0,p.stdout+p.stderr
 native,port=[json.loads((ROOT/p).read_text()) for p in (NATIVE,PORT)]
 assert (native['pairs'],native['actualTopReturns'],native['actualPhysicalHelperReturns'],native['logicalHelperEntryCompletions'],native['providedCalls'])==(1024,2048,2048,4096,2048)
 assert native['sidecar']['caseSha256']==CASE and port['nativeCaseSha256']==CASE and port['sidecar']['caseSha256']==WIN_CASE
 sidecar(native['sidecar'],CASE);sidecar(port['sidecar'],WIN_CASE)
 assert (port['totalActualPublicCalls'],port['actualRecoveredHelperCalls'],port['providedLowerCalls'],port['wrongContractRejects'],port['wrongContractPositives'],port['wrongSemanticRejects'],port['wrongSemanticPositives'])==(2048,4096,2048,1023,1,1020,4)
 for build in (port['preferred'],port['wrong']):
  for item in build['objects']:assert sha((ROOT/item['source']).read_bytes())==item['sourceSha256'] and sha((ROOT/item['object']).read_bytes())==item['objectSha256']
  assert sha((ROOT/build['binary']).read_bytes())==build['binarySha256']
 row=dict(native['candidate']);row.update(row['realLinkSnapshot']);assert row['source']==SOURCE and row['sourceSha256']==SOURCE_SHA and row['bytes']==row['compiledBytes']==236 and row['exactByteEqual'] and dependencies_current(row)
 for path,digest in [('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[path]).read_bytes())==row[digest]
 cache={};entries={row['name']:native_entry('main',0x02061C1C,cache)}
 meta,arm,_=cache['main'];linked=(ROOT/row['isolatedCallerBinary']).read_bytes();validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
 assert linked==arm[0x61C1C:0x61D08] and validation['exactCallerBytes'] and validation['sourceObjectSha256']==row['objectSha256'] and validation['sourceSha256']==SOURCE_SHA
 assert validation['linkedCallerSha256']==validation['nativeSpanSha256']==sha(linked) and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode']==0
 for relocation in row['relocations']:entries[relocation['symbol']]=(data_entry if relocation['kind']=='data' else native_entry)('main',int(relocation['target'],0),cache)
 row.update(outputSha256=sha(linked),linked=False,exactBytes=236,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,primaryReplacementCandidate=True,netNewFunctions=0,netNewBytes=0,oldSource=OLD,oldSourceSha256=OLD_SHA,
  oracle=dict(supported=True,cases=1024,actualReturns=2048,report=NATIVE,reportSha256=sha((ROOT/NATIVE).read_bytes()),limits=native['limits']),
  returnContract=dict(sourceReturnType='u32',physicalR0Compared=True,apiReturnProven=True,qualifiedReturn='retained raw holder-address word from actual61DCC/49AD0 under supplied11-word lowerUI boundary'))
 deps=runtime_files()|set(producers)|{NATIVE,PORT,SOURCE,OLD,'src/runtime/runtime07/native_main_02061dcc.c','src/runtime/runtime08/native_main_02049ad0.c','ports/windows-native/draw353_storage.c','nonmatching/save-core/20261102-draw-forward353-controls/source.c','evidence/application/save_core_historical_link_20261031.py','match_mechanics_save_20261102_lane_draw_forward.py','provenance/seed-manifest.json',native['sidecar']['path'],port['sidecar']['path']}
 deps.update(v[0]['symbolsFile'] for v in cache.values());verify_inputs()
 output=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=[row],matchedFunctions=1,matchedBytes=236,netNewFunctions=0,netNewBytes=0,primaryReplacementCandidate=True,
  nativeSymbolEntries=entries,nativeSymbols={name:value['address'] for name,value in entries.items()},nativeSymbolModules={},sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],
  oracle=dict(actualTopReturns=2048,actualPhysicalHelperReturns=2048,logicalHelperEntryCompletions=4096,providedLowerCalls=2048,nativeCaseDigest=CASE),
  portableValidation=dict(report=PORT,sha256=sha((ROOT/PORT).read_bytes()),actualPreferredPublicCalls=1024,actualWrongPublicCalls=1024,actualRecoveredHelperCalls=4096,wrongContractRejects=1023,wrongContractPositives=1,wrongSemanticRejects=1020,wrongSemanticPositives=4,windowsCaseDigest=WIN_CASE),
  wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=native['limits']+port['limits'])
 path=ROOT/'evidence/matches/mechanics-save-20261102-lane-draw-forward.json';path.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(dict(matchedBytes=236,netNewBytes=0,nativeSourceReturns=2048,windowsReturns=2048,reportSha256=sha(path.read_bytes()))))


if __name__=='__main__':main()
