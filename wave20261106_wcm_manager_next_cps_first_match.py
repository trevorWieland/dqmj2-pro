import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_wcm_manager_next_cps_first_build import build
from wave20261106_wcm_manager_next_cps_first_bindings import negative_controls
from wave20261106_wcm_manager_next_cps_first_controls import layouts,wrong_source
from wave20261106_wcm_manager_next_cps_first_fixtures import prove
from wave20261106_wcm_manager_next_cps_first_prototypes import verify as prototype_preflight
LANE=ROOT/'evidence/lanes/parallel-wave20261105/wcm-manager-next/cps-first'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6wc/cps-first/proof'
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
 if len(matches)!=7 or sum(r['bytes']for r in matches)!=684:raise ValueError('Frozen CPS membership changed')
 layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];badlayout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches);prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototypes')for row in matches];closure=code_closure([Path(__file__).name])
 limits=['Seven complete ordinary C CPS checksum/address/IPv4-fragment/UDP bodies reproduce genuine MW-linked full native extents and original typed ARM/Thumb imports. Source acceptance remains pending.','Full public CPS C and original ROM compiler identity remain unproved. Published CPS header macros/types and hashed public archive parameter/type metadata are comparative evidence only; no public object is compiled, linked, executed or used as a reconstruction generator input.','Independent bounded checksum models exercise odd/even backing, carry folding, zero/odd lengths and seeded wrapping; address models exercise multicast boundaries and each MAC byte. Packet models check exact network-order lengths, fragment offsets, checksum words, UDP ports and provider arguments.','Native/source executions compare all GPRs/CPSR, callee-saved registers, stack, ordered writes, bounded memory and provider tuples. All supplied provider bodies remain opaque and receive zero source/execution credit; no real IRQ, thread, network device/service or game behavior is established.','Only private consumed target-layout views are qualified. Public CPSSoc size and consumed offsets are checked; the 84-byte global view is a prefix, not the full global object. Cross-TU aggregate declarations remain unresolved in mandatory interface evidence.','Fixture packet buffers are bounded to valid initialized backing; actual checksum/address helper provider contracts do not establish their execution in callers. Negative lengths, invalid pointers, unbounded fragmentation, concurrency and real wireless hardware remain outside evidence.']
 write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,matches=matches,matchedFunctions=7,matchedBytes=684,ordinaryCBytes=684,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,actualNativeAndSourceCallerReturns=sum(m['actualNativeAndSourceCallerReturns']for m in models),boundedCallerModels=models,suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=badlayout,negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,abiInterfaceEvidence=[dict(path=(LANE/'cps-interface.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'cps-interface.json'))],portableAggregateInteroperabilityResolved=False,generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))
if __name__=='__main__':main()
