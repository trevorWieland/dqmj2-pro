import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_g2d_canvas_next_third_build import build
from wave20261106_g2d_canvas_next_third_bindings import negative_controls
from wave20261106_g2d_canvas_next_third_controls import layout,wrong_source,missing_prototype
from wave20261106_g2d_canvas_next_third_fixtures import prove
from wave20261106_g2d_canvas_next_third_prototypes import verify as prototype_preflight
LANE=ROOT/'evidence/lanes/parallel-wave20261106/g2d-canvas-next/third'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6gc/third/proof'

def main():
 inputs=read_json(INPUT)
 for pin in inputs['files']:
  if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen raw wrapper input changed',pin['path']))
 if inputs['romSha256']!=configuration()['romSha256']:raise ValueError('ROM identity changed')
 item,=inputs['entries'];source=ROOT/item['source']
 for p in[source,*[ROOT/x['path']for x in item['sourceDependencies']]]:
  text=p.read_text()
  if len(text.splitlines())>500 or re.search(r'/\*|//|\b(?:asm|__asm|__asm__)\b',text):raise ValueError('Ordinary C source policy differs')
 row,body=build(source,WORK/'source',0x2087334)
 for key in['address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compilerPath','compilerSha256','compilerFlags','relocations','nativeSymbolEntries']:
  if row[key]!=item[key]:raise ValueError(('Frozen raw wrapper contract differs',key))
 image=(ROOT/'extract/arm9/arm9.bin').read_bytes()
 if row['compiledBytes']!=160 or row['bytes']!=160 or body!=image[0x87334:0x873d4]:raise ValueError('Complete raw wrapper genuine link differs')
 model=prove(body);wrong=wrong_source(row,WORK/'wrong-C');positive=layout(row,WORK/'layout');negative=layout(row,WORK/'wrong-layout',True);bindings=negative_controls([row]);proto=prototype_preflight(row,WORK/'prototypes');missing=missing_prototype(row,WORK/'missing-proto');closure=code_closure([Path(__file__).name])
 row.update(program='',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=160,justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceProvenance=item['sourceProvenance'],matchingBytesScope='Complete genuine MW-linked original native extent',suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,boundaryReturnContract='void',actualNativeAndSourceCallerReturns=0,explicitProviderEntryStops=model['nativeAndSourceExplicitProviderStops'])
 limits=['One160B raw-field wrapper reproduces complete native ARM body/relocations with genuine pinned MW link from ordinary C; no imported provider or callback source credit. This is measured game-code reconstruction, not a complete published SDK C correspondence.','28independent raw-field cases compare56 native/source explicit stops at actual configured mainARM02087e58 before its first instruction. All six formed arguments, GPR/CPSR, stack, reads, ordered writes and backing compare. State5 and alternative signed states, byte underflow/overflow and modulo256 arithmetic are covered.','Actual provider44B forwards first4 registers, consumes low unsigned bytes from stack arguments5/6, then dispatches indirectly through object+0x14/vtable+8. Provider/callback executes zero instructions in these tests;0 actual caller returns. No callback target, behavior, return contract, hardware/game/native-host execution or portable ABI completion is established.','Raw measured word/byte offsets remain raw; no inferred UI or game semantics. Source/layout/prototype/binding mutants reject. Original object/relocations, compiler flags and native/config bytes remain unchanged; no algorithmASM, fake callees, object/instruction patches, executable scaffolding or storage credit.']
 write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,matches=[row],matchedFunctions=1,matchedBytes=160,ordinaryCBytes=160,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,actualNativeAndSourceCallerReturns=0,explicitProviderEntryStops=model['nativeAndSourceExplicitProviderStops'],boundedCallerModels=model,suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=positive,negativeLayoutEvidence=negative,negativeEvidence=[wrong],negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=[proto],negativePrototypeEvidence=missing,abiInterfaceEvidence=[dict(path=(LANE/'code-provider-interface.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'code-provider-interface.json'))],portableHostExecutionProven=False,importedOriginalProviderBodiesExecuted=False,importedProviderSourceOrExecutionCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))
 print('G2D raw wrapper160B;28cases/56explicit stops;0returns/provider credit',flush=True)
if __name__=='__main__':main()
