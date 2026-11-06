import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_ov006_crypto_utility_next_first_build import build
from wave20261106_ov006_crypto_utility_next_first_bindings import negative_controls
from wave20261106_ov006_crypto_utility_next_first_controls import layouts,wrong_source,missing_prototype
from wave20261106_ov006_crypto_utility_next_first_fixtures import prove
from wave20261106_ov006_crypto_utility_next_first_prototypes import verify as prototype_preflight
LANE=ROOT/'evidence/lanes/parallel-wave20261106/ov006-crypto-utility-next/first'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6cu/first/proof'

def main():
 inputs=read_json(INPUT)
 for pin in inputs['files']:
  if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen crypto input changed',pin['path']))
 if inputs['romSha256']!=configuration()['romSha256']:raise ValueError('ROM identity changed')
 interface=read_json(LANE/'code-provider-interface.json')
 if interface['extraCalleeCredit']or not interface['selectedSourceProvidersMustBeFreshCompiled']:raise ValueError('Crypto provider boundary erased')
 image=(ROOT/'extract/arm9_overlays/ov006.bin').read_bytes();matches=[];compiled={};models=[];wrong=[]
 for item in inputs['entries']:
  source=ROOT/item['source']
  for path in[source,*[ROOT/p['path']for p in item['sourceDependencies']]]:
   text=path.read_text()
   if len(text.splitlines())>500 or re.search(r'/\*|//|\b(?:asm|__asm|__asm__)\b',text):raise ValueError('Ordinary C source policy differs')
  address=int(item['address'],0);directory=WORK/format(address,'08x');row,body=build(source,directory/'source',address)
  for key in['address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compilerPath','compilerSha256','compilerFlags','relocations','nativeSymbolEntries']:
   if row[key]!=item[key]:raise ValueError(('Frozen crypto contract differs',item['address'],key))
  start=address-0x21d7240;native=image[start:start+row['bytes']]
  if row['compiledBytes']!=item['bytes']or body!=native or not row['realLink']['exactCallerBytes']:raise ValueError('Complete native crypto genuine link differs')
  compiled[address]=body;row.update(program='',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=row['bytes'],justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceProvenance=item['sourceProvenance'],matchingBytesScope='Complete genuine MW-linked native extent including original literal pool',suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,boundaryReturnContract=item['boundaryReturnContract']);matches.append(row)
 for row in matches:
  address=int(row['address'],0);native=image[address-0x21d7240:address-0x21d7240+row['bytes']];model=prove(row,native,compiled[address],compiled);models.append(model);wrong.append(wrong_source(row,WORK/format(address,'08x')/'wrong-C',compiled));row['actualNativeAndSourceCallerReturns']=model['actualNativeAndSourceCallerReturns'];print('proved crypto C',row['address'],row['bytes'],model['cases'],flush=True)
 if len(matches)!=5 or sum(r['bytes']for r in matches)!=328:raise ValueError('Frozen crypto membership differs')
 row=matches[0];layout=layouts(row,WORK/'layout');badlayout=layouts(row,WORK/'wrong-layout',True);bindings=negative_controls(matches);prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototypes')for row in matches];missing=missing_prototype(row,WORK/'missing-prototype');closure=code_closure([Path(__file__).name])
 limits=['Five complete ordinary-C stream initialization/PRGA/XOR, rawCRC updater and fixed8byte XOR functions reproduce full genuine MW-linked native extents. No whole game/host execution or shared source acceptance is implied.','Complete pinned GameSpy RC4 and SDK CRC source are comparative. Native generalized dynamicN/16bytecontext, KSA memory order and five-word CRC API differ; original source version and ROM compiler identity remain unproved. One pinned MW2.0/base profile and bounded measured dataflow/type adjustments were used, without allocator/profile sweeps.','Independent permutation/CRC models cover N0initialization,N1/2/16/255/256/300, key lengths including the measured zero-length repeated-first-byte case, state/index overflow, byte and exact/partial in-place XOR, signed zero/negative CRC length, initialized/raw table and seed cases. RFC6229 RC4 and standardCRC32 known answers cross-check models.','All GPR/CPSR, callee-saved registers, stack, ordered writes, bounded complete memory and provider tuples compare. Positive actual target16bytecontext layout and explicit declarations are checked. Pointer aliases across context/state/table backing and invalid buffers are excluded; these target layouts do not prove portable host interoperability.','Selected stream XOR executes fresh genuine compiled selected PRGA. Original main ARM unsigned division/remainder and ov006 Thumb CRC table generator execute as explicit zero-credit runtime oracle providers. Full original32/484byte ARM helper entries/ABIs were separately measured over168 cases before binding; only division is actually imported by this subset.','Original object and split relocation types/addends/encoded H bits remain unchanged. The old prenormalizer BLX mismatch is preserved as diagnostic; complete genuine typed-ARM MW linking must reproduce every native byte. No main interior entry/fake alias, patched object or instruction exists.','CRC generator56 and wrap/unwrap880 remain outside this selected packet; their drafts/negative shapes receive zero credit. No initialized storage, hardware/network provider behavior or cryptographic-security claim is made.']

 write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='ov006',allPassed=True,matches=matches,matchedFunctions=5,matchedBytes=328,ordinaryCBytes=328,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,actualNativeAndSourceCallerReturns=sum(m['actualNativeAndSourceCallerReturns']for m in models),boundedCallerModels=models,suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=badlayout,negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,negativePrototypeEvidence=missing,abiInterfaceEvidence=[dict(path=(LANE/'code-provider-interface.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'code-provider-interface.json'))],portableHostExecutionProven=False,importedOriginalProviderBodiesExecuted=True,importedProviderSourceOrExecutionCredit=0,helperAbiEvidence=dict(path=(LANE.parent/'runtime-helper-abi.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE.parent/'runtime-helper-abi.json')),generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))
if __name__=='__main__':main()
