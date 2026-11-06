import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_g3d_blendvis_next_build import build
from wave20261106_g3d_blendvis_next_bindings import negative_controls,callback
from wave20261106_g3d_blendvis_next_controls import layout,wrong_source,prototype_negative
from wave20261106_g3d_blendvis_next_fixtures import prove
from wave20261106_g3d_blendvis_next_prototypes import verify as prototype_preflight
LANE=ROOT/'evidence/lanes/parallel-wave20261106/g3d-blendvis-next'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6bv/proof'

def main():
 inputs=read_json(INPUT)
 for pin in inputs['files']:
  if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen BlendVis input changed',pin['path']))
 if inputs['romSha256']!=configuration()['romSha256']:raise ValueError('ROM identity changed')
 item,=inputs['entries'];source=ROOT/item['source']
 for p in[source,*[ROOT/x['path']for x in item['sourceDependencies']]]:
  text=p.read_text()
  if len(text.splitlines())>500 or re.search(r'/\*|//|\b(?:asm|__asm|__asm__)\b',text):raise ValueError('Ordinary C source policy differs')
 row,body=build(source,WORK/'source',0x202e260)
 for key in['address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compilerPath','compilerSha256','compilerFlags','relocations','nativeSymbolEntries']:
  if row[key]!=item[key]:raise ValueError(('Frozen BlendVis contract differs',key))
 image=(ROOT/'extract/arm9/arm9.bin').read_bytes()
 if row['compiledBytes']!=128 or row['bytes']!=128 or body!=image[0x2e260:0x2e2e0]:raise ValueError('Complete BlendVis genuine link differs')
 provider=callback(read_json(LANE/'native-inputs.json')['callbackProvider']);model=prove(body);wrong=wrong_source(row,WORK/'wrong-C');positive=layout(row,WORK/'layout');negative=layout(row,WORK/'wrong-layout',True);bindings=negative_controls([row]);proto=prototype_preflight(row,WORK/'prototypes');arity=prototype_negative(row,WORK/'wrong-prototype');closure=code_closure([Path(__file__).name])
 row.update(program='',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=128,justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceProvenance=item['sourceProvenance'],matchingBytesScope='Complete genuine MW-linked original128B ARM extent',suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,boundaryReturnContract='BOOL int32: at least one callback ran',actualNativeAndSourceCallerReturns=model['actualNativeAndSourceCallerReturns'])
 limits=['One128B complete ordinary-C NNSi_G3dAnmBlendVis body reproduces the whole native ARM extent with genuine pinned MW link and no direct relocations/imported objects. Only selected caller source bytes receive pending credit.','Complete published primary C/type header is retained. Explicit measured source-version delta: native accepts EXIST0x100 even if DISABLED0x200 is set. Current-public predicate is a genuine C mutant that fails native bytes and independent tag/list/mask model;0x100/0x300/high tags remain distinct measured cases. Original SDK/compiler revision identity is unproved.','32bounded cases give64 actual native/source caller returns and26 original callback returns. Model checks finite1-3-node lists, zero/bounded map counts, low/high/unsigned node IDs, NULL callback, map lowbyte, raw bitmask OR, zero-mask callback still returning callerTRUE, full backing/stack/GPR/CPSR/ordered reads/writes and selected target-memory overlap.','Only actual canonical mainARM2034448/56 callback executes, with0 imported provider/source/execution credit. Nonnegative frame<=3, sufficient resource/map backing and initial nonNULL object are required. No arbitrary/cyclic list/callback, resource parser, device/network/game/native-host execution or portable ABI completion claim. Result/frame overlap is measured target behavior, not a portable typed-aliasing guarantee.','Strict explicit callback/export prototypes and real target widths/layouts are checked; wrong arity/layout/caller/mode/provider/hash controls reject. No algorithmASM, instruction/object patch, supplied executable scaffolding, data/padding or original callback source credit.']
 write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,matches=[row],matchedFunctions=1,matchedBytes=128,ordinaryCBytes=128,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,actualNativeAndSourceCallerReturns=model['actualNativeAndSourceCallerReturns'],boundedCallerModels=model,suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=positive,negativeLayoutEvidence=negative,negativeEvidence=[wrong],negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=[proto],negativePrototypeEvidence=arity,originalCallbackQualification=provider,abiInterfaceEvidence=[dict(path=(LANE/'code-provider-interface.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'code-provider-interface.json'))],portableHostExecutionProven=False,importedOriginalProviderBodiesExecuted=True,importedProviderSourceOrExecutionCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))
 print('BlendVis128B;32models/64returns/26original callback returns;15identity controls',flush=True)
if __name__=='__main__':main()
