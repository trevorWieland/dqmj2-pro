import re,hashlib
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_g3d_context_next_first_build import build
from wave20261106_g3d_context_next_first_bindings import negative_controls
from wave20261106_g3d_context_next_first_controls import layout,wrong_source,coalesced_context,missing_prototype
from wave20261106_g3d_context_next_first_fixtures import prove
from wave20261106_g3d_context_next_first_prototypes import verify as prototype_preflight
LANE=ROOT/'evidence/lanes/parallel-wave20261106/g3d-context-next/first'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6gn/first/proof'

def main():
 inputs=read_json(INPUT)
 for pin in inputs['files']:
  if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen G3D input changed',pin['path']))
 if inputs['romSha256']!=configuration()['romSha256']:raise ValueError('ROM identity changed')
 item,=inputs['entries'];source=ROOT/item['source']
 for p in[source,*[ROOT/x['path']for x in item['sourceDependencies']]]:
  text=p.read_text()
  if len(text.splitlines())>500 or re.search(r'/\*|//|\b(?:asm|__asm|__asm__)\b',text):raise ValueError('Ordinary C source policy differs')
 row,body=build(source,WORK/'source',0x2031b44)
 for key in['address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compilerPath','compilerSha256','compilerFlags','relocations','nativeSymbolEntries']:
  if row[key]!=item[key]:raise ValueError(('Frozen G3D contract differs',key))
 image=(ROOT/'extract/arm9/arm9.bin').read_bytes();interface=read_json(LANE/'code-provider-interface.json');inventory=(ROOT/'config/arm9/symbols.txt').read_text().splitlines()
 for p in interface['boundedOriginalExecutedProviders']:
  a=int(p['address'],0)
  if(p['program'],p['processor'],p['module'],p['mode'],p['sourceOrExecutionCredit'])!=('','arm9','main','arm',0)or p['canonicalInventoryRecord']not in inventory or hashlib.sha256(image[a-0x2000000:a-0x2000000+p['bytes']]).hexdigest()!=p['bodySha256']:raise ValueError('Original oracle provider entry/body/scope differs')
 if row['compiledBytes']!=940 or row['bytes']!=940 or body!=image[0x31b44:0x31ef0]:raise ValueError('Complete G3D genuine link differs')
 model=prove(body);wrong=wrong_source(row,WORK/'wrong-C');coalesced=coalesced_context(row,WORK/'coalesced-context');positive=layout(row,WORK/'layout');negative=layout(row,WORK/'wrong-layout',True);bindings=negative_controls([row]);proto=prototype_preflight(row,WORK/'prototypes');missing=missing_prototype(row,WORK/'missing-proto');closure=code_closure([Path(__file__).name])
 row.update(program='',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=940,justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceProvenance=item['sourceProvenance'],matchingBytesScope='Complete genuine MW-linked original native extent including pool',suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,boundaryReturnContract='void',actualNativeAndSourceCallerReturns=model['actualNativeAndSourceCallerReturns'],explicitProviderEntryStops=model['nativeAndSourceExplicitProviderStops'])
 limits=['One complete940B ordinary-C NNSi_G3dFuncSbc_PRJMAP body reproduces native ARM extent/relocations using genuine pinned MW links. Only selected caller bytes receive pending source credit; imported cmd8/mtx64/global storage and all providers receive0credit.','Complete published NitroSystem primary C is pinned; algorithms/statements unchanged. Individually typed cmd and mtx objects preserve original distinct references. A genuine same-algorithm coalesced-section-context control grows944B and fails byte equality. Original-ROM SDK/compiler source revision identity remains unproved.','13bounded cases give10 actual native/source caller returns on flag-bypass paths and16 explicit stops before actual matrix-command provider at31c64->202e434. Independent model checks c+3 bypass, texture-bit replacement, exact cmd word, four matrix fields for u16 width/height extremes and command op/args/count, full backing and source/native GPR/CPSR/stack/ordered writes/reads.','Seven original whole ARM providers execute only in a bounded CPU/MMIO-memory fixture to read supplied clip words, convert/copy matrix values and write command FIFO words. This is not graphics hardware emulation, rendering, device/network or whole-game execution. All original code providers get0source/execution credit. Static source negative-left-shift expressions retain measured pinned-target behavior; portable ISO-C/host arithmetic behavior is not claimed.','Active fixtures stop before loading the newly written matrix through the next command provider; later effect-material/global-matrix/callback phases and shader output are unexecuted. Callback entries stayNULL; no fake callback bodies. This partial bounded behavior proof does not imply whole-function dynamic behavior coverage.','Exact target widths/layouts, strict prototype presence, meaningful source/context/layout/original-binding negatives and fresh source-only copied-root replay qualify this packet. No algorithmASM, patched instructions/objects, supplied executable scaffolding, whole-game/native-Windows or portable-host ABI completion claim.']
 write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,matches=[row],matchedFunctions=1,matchedBytes=940,ordinaryCBytes=940,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,actualNativeAndSourceCallerReturns=model['actualNativeAndSourceCallerReturns'],explicitProviderEntryStops=model['nativeAndSourceExplicitProviderStops'],boundedCallerModels=model,suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=positive,negativeLayoutEvidence=negative,negativeEvidence=[wrong],negativeSourceContextEvidence=coalesced,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=[proto],negativePrototypeEvidence=missing,abiInterfaceEvidence=[dict(path=(LANE/n).relative_to(ROOT).as_posix(),sha256=sha256(LANE/n))for n in['code-provider-interface.json','negative-fixture-correction.json','provider-scope-correction.json']],portableHostExecutionProven=False,importedOriginalProviderBodiesExecuted=True,importedProviderSourceOrExecutionCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))
 print('G3D940B;13models/10returns/16stops;216bindingnegatives;source/layout/context/prototype controls',flush=True)
if __name__=='__main__':main()
