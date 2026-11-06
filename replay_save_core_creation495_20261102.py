import base64
import gzip
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
import replay_save_core_frontier397_20261102 as F

def sha(raw):return hashlib.sha256(raw).hexdigest()
def identity(path):return dict(path=path,sha256=sha((ROOT/path).read_bytes()))

def main():
 history_path='evidence/lanes/save-core/creation495-history-20261102.json'
 history=json.loads((ROOT/history_path).read_text())
 raw=(ROOT/history['path']).read_bytes()
 assert sha(raw)==history['sha256'] and sha(gzip.decompress(raw))==history['contentSha256']
 archive=json.loads(gzip.decompress(raw))
 assert len(archive)==history['archivedFiles'] and any(p.endswith('/input.s') for p in archive)
 assert all(base64.b64decode(value) is not None for value in archive.values())
 F.load('evidence/application/save_core_creation494_fixtures_20261102.py','creation495_fixture').main()
 report_path='evidence/application/save-core-creation494-20261102.json'
 current=json.loads((ROOT/report_path).read_text())
 assert current['pairs']==240 and current['properOwnReturns']==480 and current['actualHelperReturns']==5712
 assert current['suppliedCalls']==3120 and current['suppliedBoundaryKinds']==6
 assert current['wrongProperReturns']==240 and current['wrongRejected']==64 and current['wrongPositive']==176
 assert len(current['unsupported'])==3 and all(not row['actualReturn'] and not row['postFaultStateClaim'] for row in current['unsupported'])
 assert current['build']['compiledBytes']==304 and current['build']['sameOffsetBytes']==264 and not current['build']['exactByteEqual']
 interface_path='evidence/lanes/save-core/creation495-selected-interfaces-20261102.json'
 interfaces=json.loads((ROOT/interface_path).read_text())['definitions']
 assert len(interfaces)==8
 for entry in interfaces:assert sha((ROOT/entry['source']).read_bytes())==entry['sourceSha256']
 files={interface_path,*[entry['source'] for entry in interfaces],history_path,history['path'],report_path,current['sidecar']['path'],'replay_save_core_creation495_20261102.py','evidence/application/save_core_creation494_fixtures_20261102.py','evidence/attempts/save-core-creation492-20261102.json','nonmatching/save-core/20261102-creation492/coherent.c','nonmatching/save-core/20261102-creation494/missing_float.c','docs/2026-11-02-creation-float-input-and-saved-field-chain.md'}
 for module in list(sys.modules.values()):
  path=getattr(module,'__file__',None)
  if path:
   path=Path(path).resolve()
   if ROOT in path.parents and path.suffix=='.py' and not any(p in path.relative_to(ROOT).parts for p in ('work','tools','deps')):files.add(path.relative_to(ROOT).as_posix())
 for name in ('run_save_core_mechanics485_20261102.py','evidence/application/save_core_mechanics485_worker_20261102.py','evidence/lanes/save-core/mechanics485-queue-20261102.json','evidence/lanes/save-core/mechanics485-20261102.json','evidence/vectors/save-core-mechanics485-20261102.json.gz'):files.add(name)
 for path in (ROOT/'nonmatching/save-core/20261102-mechanics485').glob('*'):
  if path.is_file():files.add(path.relative_to(ROOT).as_posix())
 out=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,broadTargets=6,broadNativeBytes=4752,broadDrafts=6,broadCompiles=5,broadRealProfiles=10,preferredNativeBytes=304,preferredCompiledBytes=304,preferredEqualBytes=264,completePairs=240,properOwnReturns=480,observedHelperReturns=5712,suppliedLowerCalls=3120,suppliedBoundaryKinds=6,wrongProperReturns=240,wrongRejected=64,wrongPositive=176,unsupported=current['unsupported'],caseDigest=current['sidecar']['contentSha256'],history=history,limitations=current['limitations'],runtimeDependencies=[identity(p) for p in sorted(files)])
 target=ROOT/'evidence/lanes/save-core/creation495-20261102.json'
 target.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(dict(pairs=240,properOwnReturns=480,wrongProperReturns=240,sourceCredit=0,reportSha256=sha(target.read_bytes()))))

if __name__=='__main__':main()
