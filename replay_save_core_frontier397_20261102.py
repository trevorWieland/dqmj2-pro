import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from link_runtime_unit import measured_module
RUNTIME={'_fgr':0x0202537C,'_fmul':0x02025AB8,'_fadd':0x02024E0C,'_fsub':0x02025CA4,'_ffix':0x020259B4,'_ffixu':0x020259E8,'_fflt':0x02025A28,'_fdiv':0x02025578}


def sha(raw):return hashlib.sha256(raw).hexdigest()
def identity(path):return dict(path=path,sha256=sha((ROOT/path).read_bytes()))


def load(path,name):
 spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def build(expected,index,arm):
 b=load('evidence/application/save_core_historical_link_20261031.py','frontier397_link_'+str(index));b.ENTRY,b.LENGTH,b.NAME,b.SOURCE=int(expected['address'],0),expected['bytes'],expected['name'],expected['source'];b.COMPILER,b.COMPILER_HASH,b.FLAGS=expected['compilerPath'],expected['compilerSha256'],list(expected['flags']);b.WORK='work/save-core/frontier397/'+str(index);prior=b.item_bindings
 assert sha((ROOT/b.SOURCE).read_bytes())==expected['sourceSha256'];native=arm[b.ENTRY-0x02000000:b.ENTRY-0x02000000+b.LENGTH];assert sha(native)==expected['targetSha256']
 def bindings():return {**prior(),**{name:dict(address=hex(address),mode='arm',module='main',processor='arm9',program='',kind='function') for name,address in RUNTIME.items()}}
 b.item_bindings=bindings;row,body=b.build(native);assert not row['exactByteEqual'];assert {k:row[k] for k in expected}==expected;assert sha(body)==expected['linkedBinarySha256'];return row


def main():
 spec_path='evidence/lanes/save-core/frontier397-identities-20261102.json';spec=json.loads((ROOT/spec_path).read_text());h=spec['history'];raw=(ROOT/h['path']).read_bytes();assert sha(raw)==h['sha256'] and sha(gzip.decompress(raw))==h['contentSha256'];arm=measured_module('main')[1];rows=[build(e,i,arm) for i,e in enumerate(spec['profileRows'])]
 profile_producer='evidence/application/save_core_float_predicate398_profiles_20261102.py';load(profile_producer,'frontier397_profiles').main()
 producer='evidence/application/save_core_float_callers396_fixtures_20261102.py';load(producer,'frontier397_caller').main();report='evidence/application/save-core-float-callers396-20261102.json';r=json.loads((ROOT/report).read_text());assert (r['pairs'],r['actualOriginalReturns'],r['actualCompiledReturns'],r['actualWrongReturns'],r['actualOriginalAndPreferredHelperReturns'],r['providedOriginalAndPreferredCalls'],r['wrongRejects'],r['wrongPositives'])==(512,512,512,512,18688,2048,512,0)
 sidecar=r['sidecar'];data=(ROOT/sidecar['path']).read_bytes();assert sha(data)==sidecar['sha256'] and sha(gzip.decompress(data))==sidecar['caseSha256']==spec['callerCaseSha256']
 files={'evidence/application/save_core_historical_link_20261031.py',spec_path,h['path'],producer,report,profile_producer,'evidence/lanes/save-core/predicate398-identities-20261102.json','evidence/attempts/save-core-float-predicate398-profile-controls-20261102.json',sidecar['path'],'replay_save_core_frontier397_20261102.py','docs/2026-11-02-guarded-float-frontier-and-native-callers.md'};files.update(x['source'] for x in rows)
 files.update(x['source'] for x in json.loads((ROOT/'evidence/lanes/save-core/predicate398-identities-20261102.json').read_text())['rows'])
 for address in (0x02055088,0x02055360,0x020554E0,0x02055660):files.add('nonmatching/save-core/20261102-float-callers396-controls/native_main_'+format(address,'08x')+'.c')
 for module in list(sys.modules.values()):
  path=getattr(module,'__file__',None)
  if path:
   p=Path(path).resolve()
   if ROOT in p.parents and p.suffix=='.py' and not any(part in p.relative_to(ROOT).parts for part in ('deps','tools','work')):files.add(p.relative_to(ROOT).as_posix())
 out=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,draftedFunctions=10,draftedNativeBytes=4616,compilableFunctions=10,genuineLinkedProfiles=20,sameSourceProfileControls=8,nearFunctions=1,exactFunctions=0,modeledFunctions=4,modeledNativeBytes=1552,properOriginalAndPreferredParentReturns=1024,properWrongParentReturns=512,actualOriginalAndPreferredHelperReturns=18688,providedOriginalAndPreferredCalls=2048,wrongReturningRejects=512,wrongReturningPositives=0,history=h,currentProfileProvenance=rows,callerReport=identity(report),callerCaseSha256=sidecar['caseSha256'],runtimeDependencies=[identity(p) for p in sorted(files)],generatorSha256=sha(Path(__file__).read_bytes()),limits=r['limits']+['Ten distinct functions compile fromnew ordinary C hypotheses;allsource remains nonmatching andzeroacceptedcredit. Failed387/388flags/bitcasts,389outlining,390inline-auto,391operator,and392parserfailure records remain archived with alloriginal negative results.','Only known2537C unchanged flag flow is lowered;no generic carry/flag suppression.32-bit carrierpromotion requires everyuseasexplicitbinary32 andeverywriteaswordloadorverifiedfloatresult;ordinaryintegeruses reject.','Generated integerboolean materialization alone added12B percomparison in393;394removesgeneratedbool temporaries only acrosslocalRAMloadswithoutcalls/stores. No original volatile qualifier or concurrent memory guarantee follows.','Current compiler/object/link provenance is regenerated locally;only source/native/span/flags/linked-body identities are compared across worktrees. Historical raw disassembly/output remains generated scaffolding.'])
 path=ROOT/'evidence/lanes/save-core/frontier397-20261102.json';path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(drafted=10,compiled=10,profiles=20,near=1,exact=0,modeled=4,properParentReturns=1024,wrongReturns=512,reportSha256=sha(path.read_bytes()))))


if __name__=='__main__':main()
