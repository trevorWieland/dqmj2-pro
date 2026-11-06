import gzip
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]
from link_runtime_unit import measured_module
import replay_save_core_frontier397_20261102 as F


def sha(raw):return hashlib.sha256(raw).hexdigest()
def identity(p):return dict(path=p,sha256=sha((ROOT/p).read_bytes()))


def main():
 path='evidence/lanes/save-core/second399-identities-20261102.json';expected=json.loads((ROOT/path).read_text());h=expected['history'];raw=(ROOT/h['path']).read_bytes();assert sha(raw)==h['sha256'] and sha(gzip.decompress(raw))==h['contentSha256'];arm=measured_module('main')[1];rows=[F.build(x,200+i,arm) for i,x in enumerate(expected['profileRows'])];assert len(rows)==34 and len({r['source'] for r in rows})==17
 for x in expected['draftSources']:assert sha((ROOT/x['path']).read_bytes())==x['sha256']
 files={path,h['path'],'replay_save_core_second399_20261102.py','evidence/application/save_core_historical_link_20261031.py','docs/2026-11-02-second-binary32-source-sweep.md'};files.update(x['path'] for x in expected['draftSources'])
 for module in list(sys.modules.values()):
  p=getattr(module,'__file__',None)
  if p:
   p=Path(p).resolve()
   if ROOT in p.parents and p.suffix=='.py' and not any(k in p.relative_to(ROOT).parts for k in ('deps','tools','work')):files.add(p.relative_to(ROOT).as_posix())
 out=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,selectedFunctions=20,selectedNativeBytes=7772,draftedFunctions=19,compilableFunctions=17,compilableNativeBytes=6692,genuineLinkedProfiles=34,nearFunctions=0,exactFunctions=0,actualParentReturns=0,history=h,currentProfileProvenance=rows,runtimeDependencies=[identity(p) for p in sorted(files)],generatorSha256=sha(Path(__file__).read_bytes()),limits=['This is newlyreviewable ordinaryC source andcurrent local compiler/MWLD evidence only;no fullparent/native behavior orsource recovery acceptance.', 'Known2537C flags,binary32 representation/carrier/field hypotheses are reused only under the guarded tools archived397. Unrecognizedcarry/flags/stack/field/ABI paths remainexplicit failures.', 'The existing138 qualified interval audit findsno overlap. RuntimeRoot object/debug hashes may change;source/native/flags/linked-body identities mustremainexact. Failedsource391styles/undefinedmacro/opaquepointer cases remain inexact-byte history.'])
 p=ROOT/'evidence/lanes/save-core/second399-20261102.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(drafted=19,compiled=17,profiles=34,exact=0,parentReturns=0,reportSha256=sha(p.read_bytes()))))


if __name__=='__main__':main()
