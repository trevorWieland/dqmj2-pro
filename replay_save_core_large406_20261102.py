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
def identity(p):return dict(path=p,sha256=sha((ROOT/p).read_bytes()))


def build(expected,index,arm):
 b=F.load('evidence/application/save_core_historical_link_20261031.py','large406_link_'+str(index));b.ENTRY,b.LENGTH,b.NAME,b.SOURCE=int(expected['address'],0),expected['bytes'],expected['name'],expected['source'];b.COMPILER,b.COMPILER_HASH,b.FLAGS=expected['compilerPath'],expected['compilerSha256'],list(expected['flags']);b.WORK='work/save-core/large406/'+str(index);prior=b.item_bindings;runtime={**F.RUNTIME,'_u32_div_f':0x02026350}
 assert sha((ROOT/b.SOURCE).read_bytes())==expected['sourceSha256'];native=arm[b.ENTRY-0x02000000:b.ENTRY-0x02000000+b.LENGTH];assert sha(native)==expected['targetSha256']
 def bindings():return {**prior(),**{name:dict(address=hex(address),mode='arm',module='main',processor='arm9',program='',kind='function') for name,address in runtime.items()}}
 b.item_bindings=bindings;row,body=b.build(native);assert not row['exactByteEqual'] and {k:row[k] for k in expected}==expected and sha(body)==expected['linkedBinarySha256'];return row


def main():
 path='evidence/lanes/save-core/large406-identities-20261102.json';s=json.loads((ROOT/path).read_text());h=s['history'];raw=(ROOT/h['path']).read_bytes();assert sha(raw)==h['sha256'] and sha(gzip.decompress(raw))==h['contentSha256'];arm=measured_module('main')[1];rows=[build(x,i,arm) for i,x in enumerate(s['profileRows'])];assert len(rows)==26 and len({r['source'] for r in rows})==13
 producer='evidence/application/save_core_allocation405_fixtures_20261102.py';F.load(producer,'large406_native').main();report='evidence/application/save-core-allocation405-20261102.json';r=json.loads((ROOT/report).read_text());assert (r['pairs'],r['actualOriginalParentReturns'],r['actualCompiledParentReturns'],r['actualWrongParentReturns'],r['actualSetupReturns'],r['wrongReturningRejects'])==(128,128,128,128,624,128);side=r['sidecar'];raw=(ROOT/side['path']).read_bytes();assert sha(raw)==side['sha256'] and sha(gzip.decompress(raw))==side['caseSha256']==s['caseSha256']
 files={path,h['path'],producer,report,side['path'],'replay_save_core_large406_20261102.py','docs/2026-11-02-larger-controller-source-and-allocation-proof.md','evidence/application/save_core_historical_link_20261031.py','nonmatching/save-core/20261102-allocation405-controls/source.c','evidence/application/allocation-constructor-arm7-20261030.py','evidence/application/allocation-constructor-arm7-20261030-setup.py'}
 for x in s['draftSources']:assert sha((ROOT/x['path']).read_bytes())==x['sha256'];files.add(x['path'])
 for row in rows:
  for dep in row.get('sourceDependencies',[]):files.add(dep['path'].replace('\\','/'))
 for module in list(sys.modules.values()):
  p=getattr(module,'__file__',None)
  if p:
   p=Path(p).resolve()
   if ROOT in p.parents and p.suffix=='.py' and not any(k in p.relative_to(ROOT).parts for k in ('deps','tools','work')):files.add(p.relative_to(ROOT).as_posix())
 out=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,selectedFunctions=20,selectedNativeBytes=37964,refinedDraftFunctions=19,compilableFunctions=13,compilableNativeBytes=sum(r['bytes'] for r in rows[::2]),genuineLinkedProfiles=26,exactFunctions=0,nearFunctions=0,sourceModeledFunctions=1,sourceModeledNativeBytes=1516,properOriginalAndPreferredParentReturns=256,properWrongParentReturns=128,actualNativeSetupReturns=624,wrongReturningRejects=128,history=h,currentProfileProvenance=rows,callerReport=identity(report),caseSha256=side['caseSha256'],runtimeDependencies=[identity(p) for p in sorted(files)],generatorSha256=sha(Path(__file__).read_bytes()),limits=r['limits']+['The twenty large candidates useexisting earlier hypotheses;new403/404 files are refinements,not nineteen newlydiscovered functions. Source compile/link metrics remain separatefrom fullnativeeffect andexact module evidence.','Feature pair typedef/casts follow frozen features/projection API;descriptor table LDRword andrank/record LDRB views follow actual instructions. No aggregate capacity,discarded surplus arguments,new formal registers orsaved-reg initialization inferred.','Unresolved44E44-family extra wordsetup,physical saved_reg inputs,unknown pointer/data/stack paths remain preserved failures. No originalaccepted source/framework/registry/UI changed.'])
 p=ROOT/'evidence/lanes/save-core/large406-20261102.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(refinedDrafts=19,compiled=13,profiles=26,exact=0,modeled=1,parentReturns=256,wrongReturns=128,setupReturns=624,reportSha256=sha(p.read_bytes()))))


if __name__=='__main__':main()
