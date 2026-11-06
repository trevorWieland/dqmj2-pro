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
 producers=['evidence/application/save_core_record_width355_build_20261102.py','evidence/application/save_core_resource_buffers358_build_20261102.py','evidence/application/save_core_record_width356_fixtures_20261102.py','check_save_core_record_windows357_20261102.py']
 for i,p in enumerate(producers):
  spec=importlib.util.spec_from_file_location('frontier359_'+str(i),ROOT/p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.main()
 expected=json.loads((ROOT/'evidence/lanes/save-core/frontier359-identities-20261102.json').read_text());current=[]
 profiles=['evidence/lanes/save-core/record-width355-profiles-20261102.json','evidence/lanes/save-core/resource-buffers358-profiles-20261102.json']
 for p in profiles:
  for r in json.loads((ROOT/p).read_text())['rows']:
   assert not r.get('failure') and not r['exactByteEqual'];current.append({k:r[k] for k in expected['profileRows'][0]});assert sha((ROOT/r['source']).read_bytes())==r['sourceSha256']
 assert current==expected['profileRows'] and len(current)==16 and len({r['source'] for r in current})==8
 native_path='evidence/application/save-core-record-width356-20261102.json';windows_path='evidence/ports/save-core-record-windows357-20261102.json';native=json.loads((ROOT/native_path).read_text());port=json.loads((ROOT/windows_path).read_text())
 assert (native['pairs'],native['actualNativeSourceReturns'],native['actualWrongSourceReturns'],native['actualNativeMetricReturns'],native['wrongRejects'])==(512,1024,512,4608,512)
 assert (port['actualPublicCalls'],port['actualRecoveredCategoryCalls'],port['wrongRejects'],port['wrongPositives'])==(1024,3072,384,128)
 assert port['nativeCaseSha256']==native['sidecar']['caseSha256']
 for x in (native,port):
  raw=(ROOT/x['sidecar']['path']).read_bytes();assert sha(raw)==x['sidecar']['sha256'] and sha(gzip.decompress(raw))==x['sidecar']['caseSha256']
 files=set(producers+profiles+[native_path,windows_path,'evidence/lanes/save-core/frontier359-identities-20261102.json','replay_save_core_frontier359_20261102.py','ports/windows-native/record357_storage.c','evidence/application/save_core_historical_link_20261031.py','src/mechanics_save/library.c','src/mechanics_save/20261030_roster_resource_pair.c','nonmatching/save-core/20261101-app-large339/native_main_0206c88c.c','nonmatching/save-core/20261101-app-large339/native_main_0206d3d8.c','evidence/attempts/save-core-record-width355-initial-flag-20261102.json','docs/2026-11-02-record-width-and-resource-buffer-frontier.md','provenance/seed-manifest.json'])
 files.update(r['source'] for r in current);files.update(x['sidecar']['path'] for x in (native,port))
 for m in list(sys.modules.values()):
  p=getattr(m,'__file__',None)
  if p:
   p=Path(p).resolve()
   if ROOT in p.parents and p.suffix=='.py' and not any(k in p.relative_to(ROOT).parts for k in ('deps','tools','work')):files.add(p.relative_to(ROOT).as_posix())
 output=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,uniqueNativeFunctions=2,uniqueNativeBytes=844,sourceHypotheses=8,compilableHypotheses=8,genuineLinkedProfiles=16,nearUnits=0,exactUnits=0,preferredRecordSameOffsetBytes=221,preferredRecordLinkedBytes=296,preferredLoaderSameOffsetBytes=413,preferredLoaderLinkedBytes=548,nativeSourceReturns=1024,wrongSourceReturns=512,actualNativeCategoryReturns=4608,windowsPublicCalls=1024,windowsCategoryCalls=3072,nativeCaseSha256=native['sidecar']['caseSha256'],windowsCaseSha256=port['sidecar']['caseSha256'],reports=[identity(p) for p in profiles+[native_path,windows_path]],runtimeDependencies=[identity(p) for p in sorted(files)],generatorSha256=sha(Path(__file__).read_bytes()),limits=native['limits']+port['limits']+['548-byte loader has compile/link evidence only. Two32-byte stack objects follow measured SP+4/+24/+44 boundaries;formatter bounds,all loader paths and lower effects remain unproved. Historical scalar buffers remain frozen known-unsafe hypotheses.','Eight hypotheses share two native identities;no unique source or executable credit. No forced register,inserted instruction,assembly or hidden work dependency.'])
 path=ROOT/'evidence/lanes/save-core/frontier359-20261102.json';path.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(dict(hypotheses=8,compiled=8,profiles=16,exact=0,nativeSourceReturns=1024,windowsCalls=1024,reportSha256=sha(path.read_bytes()))))


if __name__=='__main__':main()
