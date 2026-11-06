import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_g2d_canvas_next_first_build import build
from wave20261106_g2d_canvas_next_first_bindings import negative_controls
from wave20261106_g2d_canvas_next_first_controls import layouts,glyph_layout,wrong_source,missing_prototype
from wave20261106_g2d_canvas_next_first_fixtures import compare
from wave20261106_g2d_canvas_next_first_prototypes import verify as prototype_preflight
LANE=ROOT/'evidence/lanes/parallel-wave20261106/g2d-canvas-next/first'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6gc/first/proof'

def main():
 inputs=read_json(INPUT)
 for pin in inputs['files']:
  if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen canvas input changed',pin['path']))
 if inputs['romSha256']!=configuration()['romSha256']:raise ValueError('ROM identity changed')
 interface=read_json(LANE/'code-provider-interface.json')
 if len(interface['importedCodeProviders'])!=1 or interface['importedCodeProviders'][0]['sourceOrExecutionCredit']!=0:raise ValueError('Canvas provider scope erased')
 image=(ROOT/'extract/arm9/arm9.bin').read_bytes();matches=[];compiled={}
 for item in inputs['entries']:
  source=ROOT/item['source']
  for path in[source,*[ROOT/p['path']for p in item['sourceDependencies']]]:
   text=path.read_text()
   if len(text.splitlines())>500 or re.search(r'/\*|//|\b(?:asm|__asm|__asm__)\b',text):raise ValueError('Ordinary C source policy differs')
  address=int(item['address'],0);row,body=build(source,WORK/format(address,'08x')/'source',address)
  for key in['address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compilerPath','compilerSha256','compilerFlags','relocations','nativeSymbolEntries']:
   if row[key]!=item[key]:raise ValueError(('Frozen canvas contract differs',item['address'],key))
  native=image[address-0x2000000:address-0x2000000+row['bytes']]
  if row['compiledBytes']!=item['bytes']or body!=native or not row['realLink']['exactCallerBytes']:raise ValueError('Complete native canvas genuine link differs')
  compiled[address]=body;row.update(program='',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=row['bytes'],justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceProvenance=item['sourceProvenance'],matchingBytesScope='Complete genuine MW-linked native extent including original literal pool',suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,boundaryReturnContract='void');matches.append(row)
 if len(matches)!=2 or sum(r['bytes']for r in matches)!=984:raise ValueError('Frozen canvas membership differs')
 models=compare(compiled);wrong=[wrong_source(row,compiled,WORK/row['address']/'wrong-C')for row in matches]
 for row in matches:row['actualNativeAndSourceCallerReturns']=sum(2 for c in models['cases']if c['address']==row['address'])
 layout=layouts(matches[0],WORK/'layout');badlayout=layouts(matches[0],WORK/'wrong-layout',True);glyph=glyph_layout(matches[1],WORK/'glyph-layout');bindings=negative_controls(matches);prototypes=[prototype_preflight(row,WORK/row['address']/'prototypes')for row in matches];missing=missing_prototype(matches[1],WORK/'missing-prototype');closure=code_closure([Path(__file__).name])
 limits=['Two complete ordinary-C LetterChar/DrawGlyphLine bodies reproduce984 initialized native bytes with genuine pinned MW links; original relocations/symbol extents/modes stay unchanged. Only selected complete bodies receive pending source credit.','Independent MSB-first glyph-bit and per-pixel low-nibble/byte tile model covers source BPP1/2/4/8 <= destination4/8, transparency, palette-bounded color sums, clipped intersections, padded tile-row stride and bounded valid backing. Native/source GPR/CPSR, stack, ordered writes, provider args, reads and complete backing compare;42cases84 actual top returns. Both functions returnvoid; no register-return promise.','Direct LetterChar requires nonnegative signed intersection ends before unsigned conversion. A preserved out-of-domain original invocation exceeded the instruction bound; it is uncredited and is not silently modeled as empty. DrawGlyphLine separately tests fully clipped negative rectangles using its actual early-return boundary.','DrawGlyphLine source calls fresh selected LetterChar. Original96-byte mainARM bit-reader executes with zero imported provider/source/execution credit. No font parser, GPU, scene, network/device, whole-game or native-host ABI completion claim.','Comparative complete published NitroSystem source and prior exact lexical/type contexts are pinned. Original-ROM source/compiler revision identity is unproved; two per-body profiles were independently measured, with no flag/allocation sweep. No algorithmASM, instruction/object patches, supplied executable scaffolding or storage credit.']
 write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,matches=matches,matchedFunctions=2,matchedBytes=984,ordinaryCBytes=984,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,actualNativeAndSourceCallerReturns=models['actualNativeAndSourceReturns'],boundedCallerModels=models,suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=[layout,glyph],negativeLayoutEvidence=badlayout,negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,negativePrototypeEvidence=missing,abiInterfaceEvidence=[dict(path=(LANE/name).relative_to(ROOT).as_posix(),sha256=sha256(LANE/name))for name in['code-provider-interface.json','direct-letter-domain-negative.json']],portableHostExecutionProven=False,importedOriginalProviderBodiesExecuted=True,importedProviderSourceOrExecutionCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))
 print('G2D genuine full984B;42cases/84returns;2compiledmutants;45bindingnegatives',flush=True)
if __name__=='__main__':main()
