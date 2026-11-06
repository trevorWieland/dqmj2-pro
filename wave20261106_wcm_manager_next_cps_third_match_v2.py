import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_wcm_manager_next_cps_third_build import build
from wave20261106_wcm_manager_next_cps_third_bindings import negative_controls
from wave20261106_wcm_manager_next_cps_third_controls import layouts,wrong_source
from wave20261106_wcm_manager_next_cps_third_fixtures_v2 import prove
from wave20261106_wcm_manager_next_cps_third_prototypes import verify as prototype_preflight
LANE=ROOT/'evidence/lanes/parallel-wave20261105/wcm-manager-next/cps-third'
INPUT=LANE/'inputs-v3.json'
WORK=ROOT/'work/w6wc/cps-third/proof'
def main():
 inputs=read_json(INPUT)
 for pin in inputs['files']:
  if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen CPS input changed',pin['path']))
 if inputs['romSha256']!=configuration()['romSha256']:raise ValueError('ROM identity changed')
 interface=read_json(LANE/'cps-interface.json')
 if interface['portableAggregateInteroperabilityResolved']or not interface['publicFullCUnavailable']or not interface['romCompilerIdentityUnproved']:raise ValueError('CPS qualification limits erased')
 image=(ROOT/'extract/arm9/arm9.bin').read_bytes();matches=[];models=[];wrong=[]
 for item in inputs['entries']:
  source=ROOT/item['source']
  for path in [source,*[ROOT/p['path']for p in item['sourceDependencies']]]:
   text=path.read_text()
   if len(text.splitlines())>500 or re.search(r'/\*|//|\b(?:asm|__asm|__asm__)\b',text):raise ValueError('Ordinary C source policy differs')
  directory=WORK/format(int(item['address'],0),'08x');row,body=build(source,directory/'source')
  for key in ['address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compilerPath','compilerSha256','compilerFlags','relocations','nativeSymbolEntries']:
   if row[key]!=item[key]:raise ValueError(('Frozen CPS contract differs',item['address'],key))
  start=int(row['address'],0)-0x2000000;native=image[start:start+row['bytes']]
  if row['compiledBytes']!=item['bytes']or body!=native or not row['realLink']['exactCallerBytes']:raise ValueError('Complete native genuine link differs')
  model=prove(row,native,body);models.append(model);wrong.extend(wrong_source(row,directory/'wrong-C'))
  row.update(program='',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=row['bytes'],justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceProvenance=item['sourceProvenance'],matchingBytesScope='Complete genuine MW-linked native extent including original literal pool',actualNativeAndSourceCallerReturns=model['actualNativeAndSourceCallerReturns'],suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,boundaryReturnContract=item['boundaryReturnContract'])
  matches.append(row);print('proved CPS C',row['address'],row['bytes'],model['cases'],flush=True)
 if len(matches)!=6 or sum(r['bytes']for r in matches)!=884:raise ValueError('Frozen CPS membership changed')
 layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];badlayout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches);prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototypes')for row in matches];closure=code_closure([Path(__file__).name])
 limits=['Six complete ordinary C CPS echo/ARP/ICMP bodies reproduce genuine MW-linked full native extents and original typed ARM/Thumb imports. Shared acceptance remains pending.','Full public CPS C and original ROM compiler identity remain unproved. Published CPS macros/types and hashed public ARM3 metadata are comparative evidence only; no public object is compiled, linked, executed or consumed by a reconstruction generator.','Independent bounded models cover raw echo counter/low16-thread-pointer tokens, network-order packet fields/checksums, ARP header rejection/address classifications and a cached-IP decision after a supplied provider mutation. ICMP models cover route/cache gates, dispatcher checksum/address/type gates and finite thread lists with each receive-match condition, copy capacity clipping and supplied wakeup.','Native/source executions compare all GPRs/CPSR, callee-saved registers, stack, ordered writes, bounded memory and provider tuples, with complete wire snapshots at send boundaries. Providers are opaque and receive zero source/execution credit; no real thread,IRQ,network service/device or game is executed.','Private96-byte global,12-byte thread-list and168-byte thread-node prefixes qualify consumed offsets only. The public100-byte CPSSoc layout and consumed fields are checked; portable aggregate/thread declarations and host pointer-token behavior remain unresolved in mandatory evidence.','Fixtures use initialized aligned headers and payloads,ICMP lengths at least8,finite valid thread lists and stable backing. Invalid pointers,corrupt/cyclic lists,negative or overflowing lengths,unbounded concurrent changes and hardware execution remain outside evidence.']

 write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,matches=matches,matchedFunctions=6,matchedBytes=884,ordinaryCBytes=884,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,actualNativeAndSourceCallerReturns=sum(m['actualNativeAndSourceCallerReturns']for m in models),boundedCallerModels=models,suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=badlayout,negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,abiInterfaceEvidence=[dict(path=(LANE/'cps-interface.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'cps-interface.json'))],portableAggregateInteroperabilityResolved=False,generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))
if __name__=='__main__':main()
