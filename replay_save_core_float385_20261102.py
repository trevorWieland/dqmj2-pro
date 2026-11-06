import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]


def sha(raw):return hashlib.sha256(raw).hexdigest()
def identity(p):return dict(path=p,sha256=sha((ROOT/p).read_bytes()))


def main():
 producers=['evidence/application/save_core_float_q12_380_20261102.py',*[f'evidence/application/save_core_float_callers{x}_build_20261102.py' for x in (381,382,383,386)],'evidence/application/save_core_float_callers384_fixtures_20261102.py']
 for i,p in enumerate(producers):
  spec=importlib.util.spec_from_file_location('float385_'+str(i),ROOT/p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.main()
 expected=json.loads((ROOT/'evidence/lanes/save-core/float385-identities-20261102.json').read_text())['profileRows'];paths=[f'evidence/lanes/save-core/float-callers{x}-profiles-20261102.json' for x in (381,382,383,386)];current=[]
 for p in paths:
  for r in json.loads((ROOT/p).read_text())['rows']:
   assert not r.get('failure') and not r['exactByteEqual'];current.append({k:r[k] for k in expected[0]});assert sha((ROOT/r['source']).read_bytes())==r['sourceSha256']
 assert current==expected and len(current)==14 and len({r['source'] for r in current})==4
 qpath='evidence/abi/save-core-float-q12-380-20261102.json';cpath='evidence/application/save-core-float-callers384-20261102.json';q,c=[json.loads((ROOT/p).read_text()) for p in (qpath,cpath)];assert (q['actualCompiledReturns'],q['actualOriginalHelperReturns'],q['providedCalls'])==(1000,4000,0)
 assert (c['pairs'],c['actualOriginalReturns'],c['actualCompiledReturns'],c['actualWrongReturns'],c['actualOriginalAndPreferredHelperReturns'],c['providedOriginalAndPreferredRendererCalls'],c['wrongRejects'],c['wrongPositives'])==(128,128,128,128,12800,256,128,0)
 for r in (q,c):
  raw=(ROOT/r['sidecar']['path']).read_bytes();assert sha(raw)==r['sidecar']['sha256'] and sha(gzip.decompress(raw))==r['sidecar']['caseSha256']
 files=set(producers+paths+[qpath,cpath,'evidence/lanes/save-core/float385-identities-20261102.json','replay_save_core_float385_20261102.py','nonmatching/save-core/20261102-float-q12-380/compiler_probe.c','nonmatching/save-core/20261102-float-callers384-controls/source.c','evidence/application/save_core_historical_link_20261031.py','docs/2026-11-02-native-q12-and-four-vector-caller.md','provenance/seed-manifest.json']);files.update(r['source'] for r in current);files.update(r['sidecar']['path'] for r in (q,c))
 for m in list(sys.modules.values()):
  p=getattr(m,'__file__',None)
  if p:
   p=Path(p).resolve()
   if ROOT in p.parents and p.suffix=='.py' and not any(k in p.relative_to(ROOT).parts for k in ('deps','tools','work')):files.add(p.relative_to(ROOT).as_posix())
 output=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,uniqueOriginalFunctions=1,uniqueOriginalBytes=904,sourceHypotheses=4,compiledHypotheses=4,genuineOriginalCallerProfiles=14,nearUnits=1,exactUnits=0,preferredCompilerProfile=dict(processor='arm946e',matchingBytes=886,compiledBytes=904),alternativeArm9NoInterworking=dict(matchingBytes=889,compiledBytes=904,behaviorUnqualifiedThisProfile=True),syntheticQ12Returns=1000,actualOriginalHelpersUnderQ12=4000,actualOriginalCallerReturns=128,actualCompiledCallerReturns=128,actualWrongCallerReturns=128,actualOriginalAndPreferredHelperReturns=12800,providedOriginalAndPreferredRendererCalls=256,wrongReturningRejects=128,wrongReturningPositives=0,q12CaseSha256=q['sidecar']['caseSha256'],callerCaseSha256=c['sidecar']['caseSha256'],runtimeDependencies=[identity(p) for p in sorted(files)],reports=[identity(p) for p in paths+[qpath,cpath]],generatorSha256=sha(Path(__file__).read_bytes()),limits=q['limits']+c['limits']+['Alternate CPU/interworking/1.2 profiles remain experiments,not original compiler-setting claims.1.2 emits1100B andArm9interworking908B;NoInterworking904/889 remains nonmatching.','All twelve scalar conversion blocks already match;remaining mismatch is unsigned-size multiplication choice and tail load/register scheduling. Earlier cached-row892B and word-reload904B sources stay separate;no source opcode padding or register forcing.'])
 p=ROOT/'evidence/lanes/save-core/float385-20261102.json';p.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(dict(hypotheses=4,profiles=14,exact=0,q12Returns=1000,callerReturns=256,nativeHelpers=16800,wrongReturningRejects=128,reportSha256=sha(p.read_bytes()))))


if __name__=='__main__':main()
