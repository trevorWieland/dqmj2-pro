import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_wcm_manager_next_cps_second_build import build
from wave20261106_wcm_manager_next_cps_second_bindings import negative_controls
from wave20261106_wcm_manager_next_cps_second_controls import layouts,wrong_source
from wave20261106_wcm_manager_next_cps_second_fixtures import prove
from wave20261106_wcm_manager_next_cps_second_prototypes import verify as prototype_preflight
LANE=ROOT/'evidence/lanes/parallel-wave20261105/wcm-manager-next/cps-second'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6wc/cps-second/proof'
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
 if len(matches)!=8 or sum(r['bytes']for r in matches)!=1140:raise ValueError('Frozen CPS membership changed')
 layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];badlayout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches);prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototypes')for row in matches];closure=code_closure([Path(__file__).name])
 limits=['Eight complete ordinary C CPS packet-ring/ARP/Ethernet bodies reproduce genuine MW-linked full native extents and original typed ARM/Thumb imports, including actual original ABS32 addend10 for the ARP timestamp field. Shared acceptance remains pending.','Full public CPS C and ROM compiler identity remain unproved. Header and public ARM3 archive type metadata are comparative evidence only; no public object is compiled, linked, executed or consumed by a reconstruction generator.','Independent bounded models cover the measured1508-byte input limit, queue empty/full/wrap/drop and padding behavior, supplied sleep/wakeup boundaries, exact42-byte ARP requests, cache hit/empty/age-wrap/eviction and multicast MAC/network-order Ethernet fields.','Native/source executions compare all GPRs/CPSR, stack, callee-saved registers, ordered writes, bounded memory and provider tuples, with complete wire bytes captured at send boundaries. Providers remain opaque; no actual interrupt/thread/network service or device execution is established.','Measured repeated queue accesses use explicit volatile target-view fields. The distinct public archive has plain scalar/pointer globals, so it does not prove original ROM qualifiers or version. Private96-byte global and8-byte thread prefixes do not establish full storage or cross-TU aggregate compatibility.','Queue fixtures use initialized valid packet backing and bounded supplied sleep events; invalid pointers, accepted header lengths below8, corrupt cycles, unsigned-overflow totals, unbounded concurrency, changing backing pointers and real hardware are excluded.']

 write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,matches=matches,matchedFunctions=8,matchedBytes=1140,ordinaryCBytes=1140,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,actualNativeAndSourceCallerReturns=sum(m['actualNativeAndSourceCallerReturns']for m in models),boundedCallerModels=models,suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=badlayout,negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,abiInterfaceEvidence=[dict(path=(LANE/'cps-interface.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'cps-interface.json'))],portableAggregateInteroperabilityResolved=False,generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))
if __name__=='__main__':main()
