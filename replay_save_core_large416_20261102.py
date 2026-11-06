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
 b=F.load('evidence/application/save_core_historical_link_20261031.py','large416_link_'+str(index));b.ENTRY,b.LENGTH,b.NAME,b.SOURCE=int(expected['address'],0),expected['bytes'],expected['name'],expected['source'];b.COMPILER,b.COMPILER_HASH,b.FLAGS=expected['compilerPath'],expected['compilerSha256'],list(expected['flags']);b.WORK='work/save-core/large416/'+str(index);prior=b.item_bindings;runtime={**F.RUNTIME,'_u32_div_f':0x02026350}
 assert sha((ROOT/b.SOURCE).read_bytes())==expected['sourceSha256'];native=arm[b.ENTRY-0x02000000:b.ENTRY-0x02000000+b.LENGTH];assert sha(native)==expected['targetSha256']
 def bindings():return {**prior(),**{name:dict(address=hex(address),mode='arm',module='main',processor='arm9',program='',kind='function') for name,address in runtime.items()}}
 b.item_bindings=bindings;row,body=b.build(native);assert not row['exactByteEqual'] and {k:row[k] for k in expected}==expected and sha(body)==expected['linkedBinarySha256'];return row
def main():
 path='evidence/lanes/save-core/large416-identities-20261102.json';s=json.loads((ROOT/path).read_text());history=s['history'];raw=(ROOT/history['path']).read_bytes();assert sha(raw)==history['sha256'] and sha(gzip.decompress(raw))==history['contentSha256'];arm=measured_module('main')[1];rows=[build(x,i,arm) for i,x in enumerate(s['profileRows'])];assert len(rows)==59 and len({x['address'] for x in rows})==24
 files={path,history['path'],'replay_save_core_large416_20261102.py','docs/2026-11-02-larger-preparation-source-breadth.md'}
 for x in s['draftSources']:assert sha((ROOT/x['path']).read_bytes())==x['sha256'];files.add(x['path'])
 for row in rows:
  for x in row.get('sourceDependencies',[]):files.add(x['path'].replace('\\','/'))
 for module in list(sys.modules.values()):
  p=getattr(module,'__file__',None)
  if p:
   p=Path(p).resolve()
   if ROOT in p.parents and p.suffix=='.py' and not any(k in p.relative_to(ROOT).parts for k in ('deps','tools','work')):files.add(p.relative_to(ROOT).as_posix())
 out=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,actualNativeReturns=0,selectedSourceSweep=s['selectedSourceSweep'],genuineLinkedProfiles=59,profiledQualifiedIdentities=24,exactFunctions=0,currentProfileProvenance=rows,history=history,runtimeDependencies=[identity(p) for p in sorted(files)],generatorSha256=sha(Path(__file__).read_bytes()),limits=['The fresh32-function25548B sweep generated29 ordinaryC hypotheses and19 compiling functions/38genuine profiles;one near,zeroexact. Existinghypotheses/refinements are not newlydiscovered native functions oraccepted coverage.','Four measured64-byte buffer profiles, six typed-pointer context profiles andeleven1056B action lifetime/source profiles are separate overlapping hypotheses,not additional decompiled functions. All59 real links replay source/native/flags/linked bytes.','The780-byte compaction old typed C remains closer than current weak regeneration. Undefined saved-register live-ins,duplicate cases,surplus stat-helper arguments andscalar-as-pointer operations stay explicit failures. No arguments deleted,initial values invented orABI padding inserted.','Original449D4/44E18 input fixes are separately frozen in descriptor411 andnot counted here. None ofthese larger source bodies has fullnative-effect ormodule acceptance fromthis packet. Newly used opaque pointer views preserve32-bit width andcaller address arithmetic only;extent,lifetime andownership remain unknown.']);p=ROOT/'evidence/lanes/save-core/large416-20261102.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(profiles=59,identities=24,exact=0,sourceCredit=0,reportSha256=sha(p.read_bytes()))))
if __name__=='__main__':main()
