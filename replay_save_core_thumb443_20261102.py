import gzip
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
import replay_save_core_frontier397_20261102 as F
from link_runtime_unit import measured_module

def sha(raw):return hashlib.sha256(raw).hexdigest()
def identity(path):return dict(path=path,sha256=sha((ROOT/path).read_bytes()))

def build(expected,index,arm):
 b=F.load('evidence/application/save_core_thumb_unit425_20261102.py','thumb443_link_'+str(index))
 b.ENTRY,b.LENGTH,b.NAME,b.SOURCE=int(expected['address'],0),expected['bytes'],expected['name'],expected['source']
 b.COMPILER,b.COMPILER_HASH,b.FLAGS=expected['compilerPath'],expected['compilerSha256'],list(expected['flags'])
 b.WORK='work/save-core/thumb443/'+str(index)
 prior=b.item_bindings
 def bindings():return {**prior(),**{name:dict(address=hex(address),mode='arm',module='main',processor='arm9',program='',kind='function') for name,address in {**F.RUNTIME,'_u32_div_f':0x02026350}.items()}}
 b.item_bindings=bindings
 assert sha((ROOT/b.SOURCE).read_bytes())==expected['sourceSha256']
 native=arm[b.ENTRY-0x02000000:b.ENTRY-0x02000000+b.LENGTH]
 assert sha(native)==expected['targetSha256']
 row,body=b.build(native)
 for key in ('name','module','processor','mode','address','bytes','compiledBytes','targetSha256','source','sourceSha256','compilerSha256','compilerPath','flags','linkedBinarySha256','sameOffsetBytes','exactByteEqual'):
  assert row[key]==expected[key],(index,key,row[key],expected[key])
 assert not row['exactByteEqual'] and sha(body)==expected['linkedBinarySha256']
 return row

def main():
 path='evidence/lanes/save-core/thumb443-identities-20261102.json';s=json.loads((ROOT/path).read_text());h=s['history'];packed=(ROOT/h['path']).read_bytes()
 assert sha(packed)==h['sha256'] and sha(gzip.decompress(packed))==h['contentSha256']
 archive=json.loads(gzip.decompress(packed))['archive'];assert any(p.endswith('/input.s') for p in archive)
 for item in s['draftSources']:assert sha((ROOT/item['path']).read_bytes())==item['sha256']
 arm=measured_module('main')[1];rows=[build(r,i,arm) for i,r in enumerate(s['profileRows'])];assert len(rows)==37
 F.load('probe_save_core_thumb445_native_20261102.py','thumb445_native').main();native=json.loads((ROOT/'evidence/verification/save-core-thumb445-native-20261102.json').read_text())
 assert (native['nativeArithmeticSingleSteps'],native['nativeLocalBlSingleSteps'],native['properFunctionReturns'])==(1024,64,0)
 import recover_escaped_stack439_20261102 as A
 import recover_escaped_stack441_20261102 as B
 assert A.controls()==B.controls()==5
 current=json.dumps(rows,sort_keys=True,separators=(',',':')).encode();side=ROOT/'evidence/vectors/save-core-thumb443-current-provenance-20261102.json.gz';side.write_bytes(gzip.compress(current,mtime=0))
 files={path,h['path'],'replay_save_core_thumb443_20261102.py','probe_save_core_thumb445_native_20261102.py','evidence/verification/save-core-thumb445-native-20261102.json',native['sidecar']['path'],'docs/2026-11-02-thumb-flags-bounded-stack-and-source-breadth.md','recover_escaped_stack439_20261102.py','recover_escaped_stack441_20261102.py','lower_thumb_internal_branches424_20261102.py','restore_thumb_flags426_20261102.py'}
 for family in (423,427,434,440,442):
  files.update({'run_save_core_breadth'+str(family)+'_20261102.py','evidence/application/save_core_breadth'+str(family)+'_worker_20261102.py','evidence/lanes/save-core/breadth'+str(family)+'-queue-20261102.json','evidence/lanes/save-core/breadth'+str(family)+'-20261102.json','evidence/vectors/save-core-breadth'+str(family)+'-20261102.json.gz'})
 for item in s['draftSources']:files.add(item['path'])
 for module in list(sys.modules.values()):
  p=getattr(module,'__file__',None)
  if p:
   p=Path(p).resolve()
   if ROOT in p.parents and p.suffix=='.py' and not any(k in p.relative_to(ROOT).parts for k in ('deps','tools','work')):files.add(p.relative_to(ROOT).as_posix())
 out=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,qualifiedIdentities=len({r['address'] for r in rows}),genuineLinkedProfiles=len(rows),exactMatches=0,archivedDraftSourceFiles=len(s['draftSources']),passes=s['passes'],nativeArithmeticSingleSteps=1024,nativeLocalBlSingleSteps=64,properFunctionReturns=0,history=h,currentProfileProvenance=dict(path=side.relative_to(ROOT).as_posix(),sha256=sha(side.read_bytes()),contentSha256=sha(current)),runtimeDependencies=[identity(p) for p in sorted(files)],generatorSha256=sha(Path(__file__).read_bytes()),limits=['64 distinct larger Thumb targets selected across two32-function sweeps. Historical and refined sources remain separate;54 source files are not54 newly recovered functions. Exact820 and512 corrections are separate frozen packets432/438 and receive no credit here.','37 current genuine compiler/MWLD replays retain exact source,compiler version,flags,native andlinked hashes. Object/debug provenance is regenerated in a separate compressed sidecar. Many low-similarity drafts may still be incorrect.','1024 arithmetic instructions and64 localBL instructions are native single steps,not proper function returns. Full carry semantics,M2C lowering andparent behavior remain separately unproved.','Escaped byte-array extents are bounded hypotheses from literal call capacity,original SP allocation andnearest named slot. Actual callee behavior,unnamed overlaps,aggregate identity andordinary paths remain unproved. Void-pointer dereference correction inAB96C remains a width hypothesis.','All frozen accepted sources,reports andapplication files remain unchanged. No opcodepatching,forced registers,assembly orpadding. Unknown save bytes andbank arbitration meanings remain unknown.'])
 target=ROOT/'evidence/lanes/save-core/thumb443-20261102.json';target.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(profiles=len(rows),identities=out['qualifiedIdentities'],draftFiles=len(s['draftSources']),functionReturns=0,sourceCredit=0,reportSha256=sha(target.read_bytes()))))
if __name__=='__main__':main()
