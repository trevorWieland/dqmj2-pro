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
 b=F.load('evidence/application/save_core_historical_link_20261031.py','mechanics475_link_'+str(index))
 b.ENTRY,b.LENGTH,b.NAME,b.SOURCE=int(expected['address'],0),expected['bytes'],expected['name'],expected['source']
 b.COMPILER,b.COMPILER_HASH,b.FLAGS=expected['compilerPath'],expected['compilerSha256'],list(expected['flags'])
 b.WORK='work/save-core/mechanics475/'+str(index)
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
 path='evidence/lanes/save-core/mechanics475-identities-20261102.json';s=json.loads((ROOT/path).read_text());h=s['history'];packed=(ROOT/h['path']).read_bytes()
 assert sha(packed)==h['sha256'] and sha(gzip.decompress(packed))==h['contentSha256']
 archive=json.loads(gzip.decompress(packed));assert any(p.endswith('/input.s') for p in archive)
 for item in s['draftSources']:assert sha((ROOT/item['path']).read_bytes())==item['sha256']
 arm=measured_module('main')[1];rows=[build(r,i,arm) for i,r in enumerate(s['profileRows'])];assert len(rows)==45
 F.load('evidence/application/save_core_allocation471_fixtures_20261102.py','mechanics471_native').main();native=json.loads((ROOT/'evidence/application/save-core-allocation471-20261102.json').read_text());assert native['completePairs']==192 and native['properTopReturns']==native['properOwnEntryReturns']==384 and native['suppliedMmioDivisionResults']==0 and not native['failures'];bad=native['byteTableControls'];assert len(bad)==1 and not bad[0]['returned'] and bad[0]['faults'][0]['address']=='0x4e' and bad[0]['nativePointerWord']=='0x2510044'
 current=json.dumps(rows,sort_keys=True,separators=(',',':')).encode();side=ROOT/'evidence/vectors/save-core-mechanics475-current-provenance-20261102.json.gz';side.write_bytes(gzip.compress(current,mtime=0))
 files={path,h['path'],'replay_save_core_mechanics475_20261102.py','evidence/application/save_core_allocation471_fixtures_20261102.py','evidence/application/save-core-allocation471-20261102.json',native['sidecar']['path'],'evidence/lanes/save-core/allocation471-build-profile-20261102.json','docs/2026-11-02-allocation-caller-pointer-and-state-evidence.md'}
 for family in (463,464,468,469):
  files.update({'run_save_core_mechanics'+str(family)+'_20261102.py','evidence/application/save_core_mechanics'+str(family)+'_worker_20261102.py','evidence/lanes/save-core/mechanics'+str(family)+'-queue-20261102.json','evidence/lanes/save-core/mechanics'+str(family)+'-20261102.json','evidence/vectors/save-core-mechanics'+str(family)+'-20261102.json.gz'})
 for item in s['draftSources']:files.add(item['path'])
 for module in list(sys.modules.values()):
  p=getattr(module,'__file__',None)
  if p:
   p=Path(p).resolve()
   if ROOT in p.parents and p.suffix=='.py' and not any(k in p.relative_to(ROOT).parts for k in ('deps','tools','work')):files.add(p.relative_to(ROOT).as_posix())
 out=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,qualifiedIdentities=len({r['address'] for r in rows}),genuineLinkedProfiles=len(rows),exactMatches=0,archivedDraftSourceFiles=len(s['draftSources']),passes=s['passes'],completeNativeSourcePairs=192,properOwnEntryReturns=384,suppliedLowerBoundaries=9,actualMmioDivisionResults=0,knownIncorrectByteTableControl=bad,history=h,currentProfileProvenance=dict(path=side.relative_to(ROOT).as_posix(),sha256=sha(side.read_bytes()),contentSha256=sha(current)),runtimeDependencies=[identity(p) for p in sorted(files)],generatorSha256=sha(Path(__file__).read_bytes()),limits=['Seven static caller-family functions7084nativebytes selected withinthree reverse ARMcall edges ofallocation76D70/slot62F3C/rebuild78978/library7AEBC. Allseven compileaftertypedpointer/source-emission repairs;45 overlappingprofile replays acrosssevenidentities arezero exact/source credit.','Known context pointer declarations mustsurvive finalCemission. Old468 source withbyte-table declaration isknownincorrect fordescriptorlookup evenwhen itcompiles. MeasuredLDRLSL2 pointer-table source469 passes192 fullpaired contexts butstill doesnotmatch native1000B source extent.','Original77A24 state writer remainsreal. Independent models verify state3/7,previousstate andrequestword pluspoint wrapping/debit/librarywrites. Nine lower widget/object/notification boundaries remainexplicit providers withlegal volatileclobbers;their internal sideeffects/ordinary availability areunproved.','Synthetic species1/slot0,eightoriginalSkillTbl rows,zero priorpoint andempty transientlists,six targets,two states/knownflags. Zero-free contexts stilldebit/wrap;this isbounded kernel/caller capability,not ordinary eligibility/import rule.','Experimental468/469 signed32 return view of76D4C differs fromselectedunsigned32 Cdefinition carryingthe samebits;complete Cinterface portability isnot claimed. New481 views alignthese separately. The36-byte helper isalready accepted andisreuse only.','Prior failed463 metadataNameError,compiler negatives,oldbyte-table source andbounded natural kernel address-lifetime/optimization trials arepreserved. Accepted sources,application adapters andunknownsave meanings remainunchanged.']);target=ROOT/'evidence/lanes/save-core/mechanics475-20261102.json';target.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(profiles=len(rows),identities=out['qualifiedIdentities'],pairs=192,properOwnReturns=384,sourceCredit=0,reportSha256=sha(target.read_bytes()))))

if __name__=='__main__':main()
