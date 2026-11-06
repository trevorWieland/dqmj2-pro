import gzip
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from link_runtime_unit import measured_module
import replay_save_core_frontier397_20261102 as F
def sha(raw):return hashlib.sha256(raw).hexdigest()
def identity(path):return dict(path=path,sha256=sha((ROOT/path).read_bytes()))
def build(expected,index,arm):
 b=F.load('evidence/application/save_core_historical_link_20261031.py','large422_link_'+str(index));b.ENTRY,b.LENGTH,b.NAME,b.SOURCE=int(expected['address'],0),expected['bytes'],expected['name'],expected['source'];b.COMPILER,b.COMPILER_HASH,b.FLAGS=expected['compilerPath'],expected['compilerSha256'],list(expected['flags']);b.WORK='work/save-core/large422/'+str(index);prior=b.item_bindings;runtime={**F.RUNTIME,'_u32_div_f':0x02026350}
 assert sha((ROOT/b.SOURCE).read_bytes())==expected['sourceSha256'];native=arm[b.ENTRY-0x02000000:b.ENTRY-0x02000000+b.LENGTH];assert sha(native)==expected['targetSha256']
 def bindings():return {**prior(),**{name:dict(address=hex(address),mode='arm',module='main',processor='arm9',program='',kind='function') for name,address in runtime.items()}}
 b.item_bindings=bindings;row,body=b.build(native);assert not row['exactByteEqual'] and {k:row[k] for k in expected}==expected and sha(body)==expected['linkedBinarySha256'];return row
def main():
 path='evidence/lanes/save-core/large422-identities-20261102.json';s=json.loads((ROOT/path).read_text());history=s['history'];raw=(ROOT/history['path']).read_bytes();assert sha(raw)==history['sha256'] and sha(gzip.decompress(raw))==history['contentSha256'];arm=measured_module('main')[1];rows=[build(x,i,arm) for i,x in enumerate(s['profileRows'])];assert len(rows)==41 and len({x['address'] for x in rows})==15
 producer='evidence/application/save_core_dialog421_fixtures_20261102.py';F.load(producer,'large422_native').main();report='evidence/application/save-core-dialog421-20261102.json';native=json.loads((ROOT/report).read_text());assert (native['pairs'],native['properOriginalAndSourceReturns'],native['properWrongReturns'],native['actualHelperReturns'],native['suppliedCalls'],native['wrongRejects'],native['wrongPositiveControls'])==(150,300,150,1062,3630,144,6);side=native['sidecar'];packed=(ROOT/side['path']).read_bytes();assert sha(packed)==side['sha256'] and sha(gzip.decompress(packed))==side['caseSha256']==s['nativeCaseSha256']
 files={path,history['path'],'replay_save_core_large422_20261102.py',producer,report,side['path'],'docs/2026-11-02-dialog-counter-width-and-larger-source.md'}
 for x in s['draftSources']:assert sha((ROOT/x['path']).read_bytes())==x['sha256'];files.add(x['path'])
 for row in rows:
  for x in row.get('sourceDependencies',[]):files.add(x['path'].replace('\\','/'))
 for module in list(sys.modules.values()):
  p=getattr(module,'__file__',None)
  if p:
   p=Path(p).resolve()
   if ROOT in p.parents and p.suffix=='.py' and not any(k in p.relative_to(ROOT).parts for k in ('deps','tools','work')):files.add(p.relative_to(ROOT).as_posix())
 out=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,properOriginalAndSourceReturns=300,properWrongReturns=150,actualHelperReturns=1062,suppliedCalls=3630,wrongRejects=144,wrongPositiveControls=6,selectedSourceSweep=s['selectedSourceSweep'],genuineLinkedProfiles=41,profiledQualifiedIdentities=15,exactFunctions=0,currentProfileProvenance=rows,history=history,runtimeDependencies=[identity(p) for p in sorted(files)],generatorSha256=sha(Path(__file__).read_bytes()),limits=native['limits']+['Fresh26-function18004B sweep:23 C refinements,15 compiling/30genuine profiles,one near,zeroexact. Eleven overlapping1292B width/cache/lifetime profiles are separate hypotheses;all41 replay original source/native/flags/linked hashes.','Unsigned word counter,minimum16-byte state object andcached before-store reads improve1292 matching from1170 to1270. Remaining22 differing bytes largely register roles;boundednatural variants preserve failures. None isaccepted source coverage.','Native model covers144 state0 initialization andsix14/3C busy-byte contexts,includingwordwrap andactual GUIwordOR2. State28 active input andordinary reachability remainunsupported. Final20 lowerUI/text boundaries aresupplied;allclobber,arity,orderedwrite andfailure limits remain explicit.']);p=ROOT/'evidence/lanes/save-core/large422-20261102.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(profiles=41,identities=15,exact=0,sourceCredit=0,reportSha256=sha(p.read_bytes()))))
if __name__=='__main__':main()
