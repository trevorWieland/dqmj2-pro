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
 producers=['evidence/application/save_core_float_flags377_20261102.py','evidence/application/save_core_float_compare378_20261102.py']
 for i,p in enumerate(producers):
  spec=importlib.util.spec_from_file_location('float379_'+str(i),ROOT/p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.main()
 reports=['evidence/abi/save-core-float-flags377-20261102.json','evidence/abi/save-core-float-compare378-20261102.json'];native,probe=[json.loads((ROOT/p).read_text()) for p in reports];assert native['actualNativeReturns']==8256 and probe['actualCompiledProbeReturns']==probe['actualOriginalHelperReturns']==8320 and native['providedCalls']==probe['providedCalls']==0
 assert probe['nativeFlagsCaseSha256']==native['sidecar']['caseSha256']
 for r in (native,probe):
  raw=(ROOT/r['sidecar']['path']).read_bytes();assert sha(raw)==r['sidecar']['sha256'] and sha(gzip.decompress(raw))==r['sidecar']['caseSha256']
 for row in probe['syntheticCompilerProbes']:
  for p,h in [('source','sourceSha256'),('object','objectSha256'),('caller','callerSha256'),('binary','binarySha256'),('lcf','lcfSha256')]:assert sha((ROOT/row[p]).read_bytes())==row[h]
 files=set(producers+reports+['replay_save_core_float379_20261102.py','nonmatching/save-core/20261102-float-compare378/compiler_probe.c','docs/2026-11-02-binary32-flag-return-and-compiler-probes.md','provenance/seed-manifest.json']);files.update(r['sidecar']['path'] for r in (native,probe))
 for m in list(sys.modules.values()):
  p=getattr(m,'__file__',None)
  if p:
   p=Path(p).resolve()
   if ROOT in p.parents and p.suffix=='.py' and not any(k in p.relative_to(ROOT).parts for k in ('deps','tools','work')):files.add(p.relative_to(ROOT).as_posix())
 output=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,originalNativeFlagReturns=8256,syntheticCompiledPredicateReturns=8320,originalHelperReturnsUnderCompiledPredicates=8320,providedCalls=0,qualifiedSymbol=dict(symbol='_fgr',processor='arm9',program='',module='main',mode='arm',address='0x0202537c',nativeSpanSha256=native['nativeSpanSha256'],scope='measured raw binary32 greater relation and HI/LS flags under pinnedcompiler profile'),nativeCaseSha256=native['sidecar']['caseSha256'],compiledCaseSha256=probe['sidecar']['caseSha256'],reports=[identity(p) for p in reports],runtimeDependencies=[identity(p) for p in sorted(files)],generatorSha256=sha(Path(__file__).read_bytes()),limits=native['limits']+probe['limits'])
 p=ROOT/'evidence/abi/save-core-float379-20261102.json';p.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(dict(nativeFlagReturns=8256,compiledReturns=8320,helperReturns=8320,providers=0,sourceCredit=0,reportSha256=sha(p.read_bytes()))))


if __name__=='__main__':main()
