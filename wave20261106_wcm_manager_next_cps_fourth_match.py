import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_wcm_manager_next_cps_fourth_build import build
from wave20261106_wcm_manager_next_cps_fourth_bindings import negative_controls
from wave20261106_wcm_manager_next_cps_fourth_controls import layouts,wrong_source
from wave20261106_wcm_manager_next_cps_fourth_fixtures import prove
from wave20261106_wcm_manager_next_cps_fourth_prototypes import verify as prototype_preflight
LANE=ROOT/'evidence/lanes/parallel-wave20261105/wcm-manager-next/cps-fourth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6wc/cps-fourth/proof'
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
 if len(matches)!=8 or sum(r['bytes']for r in matches)!=1402:raise ValueError('Frozen CPS membership changed')
 layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];badlayout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches);prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototypes')for row in matches];closure=code_closure([Path(__file__).name])
 limits=['Eight complete ordinary C CPS TCP selection/handshake/reset/state handlers reproduce genuine MW-linked full native extents, including the496-byte ACK handler and original ABS32 addressing-anchor addends64/68. Shared acceptance remains pending.','Full public CPS C and original ROM compiler identity remain unproved. Published CPS types/macros and public ARM3 debug metadata are comparative evidence only; no public object is compiled, linked, executed or consumed by the reconstruction generator.','Independent bounded models cover tuple/state selection, five-word send-call preservation, reset-object byte construction, SYN/SYN-ACK routing and wakeup order, every ACK state class, signed modular acknowledgement updates, buffer clipping/zero capacity, FIN transitions and sequence/counter wrap. Explicit required state3/state4 zero-payload FIN paths are asserted separately.','All GPRs/CPSR, stack, callee-saved registers, ordered writes, bounded memory and provider tuples/socket snapshots compare. Providers are opaque; no real scheduler, interrupt, network service/device or complete transmitted packet is executed. Reset construction leaves state zero as native does; successful reset transmission is not claimed.','Original native handshake passes a fifth u16 urgent word that the412-byte send_tcp body does not consume; the distinct public archive lists four formals. New source preserves the measured caller boundary while original portable signature and failed send_tcp body remain unresolved/uncredited.','Reset/global/thread target views qualify consumed offsets only; prefix168/12/168 and CPSSoc100 layouts do not establish full original storage or unified portable host interfaces. Fixtures exclude malformed pointers/lists, receive-used beyond capacity, overflowing memory lengths and unbounded concurrent/provider changes.']

 write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,matches=matches,matchedFunctions=8,matchedBytes=1402,ordinaryCBytes=1402,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,actualNativeAndSourceCallerReturns=sum(m['actualNativeAndSourceCallerReturns']for m in models),boundedCallerModels=models,suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=badlayout,negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,abiInterfaceEvidence=[dict(path=(LANE/'cps-interface.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'cps-interface.json'))],portableAggregateInteroperabilityResolved=False,generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))
if __name__=='__main__':main()
