import hashlib
import importlib.util
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]
from link_runtime_unit import measured_module


def sha(raw):return hashlib.sha256(raw).hexdigest()
def identity(p):return dict(path=p,sha256=sha((ROOT/p).read_bytes()))


def main():
 producers=['evidence/application/save_core_resource_buffers360_build_20261102.py','evidence/application/save_core_resource_buffers361_build_20261102.py','evidence/application/save_core_projection_buffers362_build_20261102.py'];paths=['evidence/lanes/save-core/resource-buffers360-profiles-20261102.json','evidence/lanes/save-core/resource-buffers361-profiles-20261102.json','evidence/lanes/save-core/projection-buffers362-profiles-20261102.json']
 expected=json.loads((ROOT/'evidence/lanes/save-core/buffer363-identities-20261102.json').read_text())['profileRows'];current=[]
 for i,p in enumerate(producers):
  spec=importlib.util.spec_from_file_location('buffer363_'+str(i),ROOT/p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.main()
 for p in paths:
  for r in json.loads((ROOT/p).read_text())['rows']:
   assert not r.get('failure') and not r['exactByteEqual'];current.append({k:r[k] for k in expected[0]});assert sha((ROOT/r['source']).read_bytes())==r['sourceSha256']
 assert current==expected and len(current)==18 and len({r['source'] for r in current})==9
 arm=measured_module('main')[1];sites=[(0x6D3DC,0xE24DD044),(0x6D438,0xE28D0024),(0x6D44C,0xE28D0004),(0x6D600,0xE24DD040),(0x70D08,0xE24DD060)]
 for offset,word in sites:assert int.from_bytes(arm[offset:offset+4],'little')==word
 projection=(ROOT/'src/mechanics_save/projection.c').read_text();assert 'void saved_projection_with_features(int species, int variant, const u8 *features, u8 *output)' in projection and 'native_fill(output, 0, 32);' in projection
 pair=(ROOT/'src/mechanics_save/20261030_roster_resource_pair.c').read_text();assert 'native_fn_0206d3d8(s32 species, u32 flag, u32 offset, s32 option, s32 zero)' in pair and 'native_fn_0206d5fc(s32 species, u32 flag, s32 firstOffset, s32 option, s32 zero)' in pair
 files=set(producers+paths+['replay_save_core_buffer363_20261102.py','evidence/lanes/save-core/buffer363-identities-20261102.json','src/mechanics_save/projection.c','src/mechanics_save/features.c','src/mechanics_save/20261030_roster_resource_pair.c','src/mechanics_save/library.c','docs/2026-11-02-bounded-stack-buffer-family.md','provenance/seed-manifest.json'])
 files.update(r['source'] for r in current)
 for entry in ('0206d3d8','0206d5fc','02070d04'):files.add('nonmatching/save-core/20261101-app-large339/native_main_'+entry+'.c')
 files.add('evidence/application/save_core_historical_link_20261031.py')
 for m in list(sys.modules.values()):
  p=getattr(m,'__file__',None)
  if p:
   p=Path(p).resolve()
   if ROOT in p.parents and p.suffix=='.py' and not any(k in p.relative_to(ROOT).parts for k in ('deps','tools','work')):files.add(p.relative_to(ROOT).as_posix())
 out=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,uniqueNativeFunctions=3,uniqueNativeBytes=1632,sourceHypotheses=9,compiledHypotheses=9,genuineLinkedProfiles=18,nearUnits=0,exactUnits=0,actualNativeReturns=0,actualCompiledReturns=0,measuredStackWords=[dict(address=hex(0x02000000+p),word=hex(w)) for p,w in sites],reports=[identity(p) for p in paths],runtimeDependencies=[identity(p) for p in sorted(files)],generatorSha256=sha(Path(__file__).read_bytes()),limits=['Three native identities reuse older339 drafts;all nine new alternatives/18 profiles remain nonmatching and unexecuted. No new unique recovery or source credit.', 'Two32-byte loader buffers follow native stack-neighbor boundaries;ordinary formatting bounds and lower effects remain unsupported.508-byte loader regresses from the unsafe scalar draft despite improved object extents:512/516 bytes,64/172 matches. Source safety is not proximity.', '576-byte preparation/projection caller had a one-byte sp0 object plus separate sp1 scalar despite original helper output32 bytes and observed reads through index28. Unified32-byte output and64-byte feature buffers plus typed helpers are new hypotheses. Global29-entry extent follows the original clear loop,not a save-record layout.', 'Selected6D2E0 declarations establish candidate own formal views for the two loaders;70D04 helper inputs/outputs are source-hash-qualified but full caller/return ABI and native behavior still require execution.', 'Typed-array global362 improves131to283 same-offset bytes at564 compiled/native576. Speed reaches576 bytes but only198 matches. No forced padding,registers,opcode changes,assembly or accepted-source modifications.'])
 path=ROOT/'evidence/lanes/save-core/buffer363-20261102.json';path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(hypotheses=9,compiled=9,profiles=18,exact=0,nativeReturns=0,reportSha256=sha(path.read_bytes()))))


if __name__=='__main__':main()
