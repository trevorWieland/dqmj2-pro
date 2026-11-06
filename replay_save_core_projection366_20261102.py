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
 producers=['replay_save_core_buffer363_20261102.py','evidence/application/save_core_projection_context364_build_20261102.py','evidence/application/save_core_projection365_fixtures_20261102.py']
 for i,p in enumerate(producers):
  spec=importlib.util.spec_from_file_location('projection366_'+str(i),ROOT/p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.main()
 family=json.loads((ROOT/'evidence/lanes/save-core/buffer363-20261102.json').read_text());expected=json.loads((ROOT/'evidence/lanes/save-core/projection366-identities-20261102.json').read_text())['rows'];rows=json.loads((ROOT/'evidence/lanes/save-core/projection-context364-profiles-20261102.json').read_text())['rows']
 assert [{k:r[k] for k in expected[0]} for r in rows]==expected and len(rows)==4
 native_path='evidence/application/save-core-projection365-20261102.json';native=json.loads((ROOT/native_path).read_text());assert (native['pairs'],native['actualOriginalReturns'],native['actualCompiledReturns'],native['actualWrongReturns'],native['wrongBoundaryFailures'],native['providedOriginalAndPreferredCalls'])==(227,227,227,19,208,888)
 s=native['sidecar'];raw=(ROOT/s['path']).read_bytes();assert sha(raw)==s['sha256'] and sha(gzip.decompress(raw))==s['caseSha256'];vectors=json.loads(gzip.decompress(raw));faults=[x for x in vectors if not x['control']['returned']];assert len(faults)==208 and all(json.loads(x['control']['boundaryFailure'])['details']['address']=='0x74' and json.loads(x['control']['boundaryFailure'])['details']['size']==4 for x in faults)
 files={x['path'] for x in family['runtimeDependencies']};files.update(producers+[native_path,s['path'],'evidence/lanes/save-core/buffer363-20261102.json','evidence/lanes/save-core/projection366-identities-20261102.json','evidence/lanes/save-core/projection-context364-profiles-20261102.json','replay_save_core_projection366_20261102.py','docs/2026-11-02-projection-context-word-native-comparison.md']);files.update(r['source'] for r in rows)
 incorrect=[]
 for label in ('buffer_merge','typed_buffers','typed_array_global'):
  p='nonmatching/save-core/20261102-projection-buffers362/'+label+'/source.c';text=(ROOT/p).read_text();assert '(u8) native_data_021c4f60' in text;incorrect.append(dict(**identity(p),scope='full-context-pointer paths;byte cast truncates full native address',acceptedSource=False))
 out=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,uniqueNativeFunctions=3,uniqueNativeBytes=1632,sourceHypotheses=11,compiledHypotheses=11,genuineLinkedProfiles=22,nearUnits=0,exactUnits=0,actualOriginalReturns=227,actualPreferredCompiledReturns=227,actualWrongReturns=19,wrongReturningPositives=native['returningWrongPositives'],wrongReturningRejects=native['returningWrongRejects'],wrongUnmappedReadFailures=208,providedOriginalAndPreferredCalls=888,caseSha256=s['caseSha256'],knownIncorrectUnacceptedDrafts=incorrect,runtimeDependencies=[identity(p) for p in sorted(files)],reports=[identity(p) for p in ('evidence/lanes/save-core/buffer363-20261102.json','evidence/lanes/save-core/projection-context364-profiles-20261102.json',native_path)],generatorSha256=sha(Path(__file__).read_bytes()),limits=native['limits']+family['limits']+['362 hypotheses are archival known-incorrect for full-context pointer paths. New364 source retains full32-bit context words;raw physical R0 is compared,without public status/return meaning. All adopted sources remain unchanged.'])
 path=ROOT/'evidence/lanes/save-core/projection366-20261102.json';path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(hypotheses=11,compiled=11,profiles=22,exact=0,properReturns=454,wrongReturns=19,wrongMemoryFaults=208,reportSha256=sha(path.read_bytes()))))


if __name__=='__main__':main()
