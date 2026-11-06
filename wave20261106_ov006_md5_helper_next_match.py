import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_ov006_md5_helper_next_build import build
from wave20261106_ov006_md5_helper_next_bindings import negative_controls
from wave20261106_ov006_md5_helper_next_controls import layouts,wrong_source,missing_prototype
from wave20261106_ov006_md5_helper_next_fixtures import prove
from wave20261106_ov006_md5_helper_next_prototypes import verify as prototype_preflight
LANE=ROOT/'evidence/lanes/parallel-wave20261106/ov006-md5-helper-next'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6mh/proof'

def main():
 inputs=read_json(INPUT)
 for pin in inputs['files']:
  if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen MD5 input changed',pin['path']))
 if inputs['romSha256']!=configuration()['romSha256']:raise ValueError('ROM identity changed')
 interface=read_json(LANE/'code-provider-interface.json')
 if interface['importedCodeProviders']or not interface['noCallerOrPaddingCredit']:raise ValueError('MD5 helper scope erased')
 image=(ROOT/'extract/arm9_overlays/ov006.bin').read_bytes();matches=[];compiled={};models=[];wrong=[]
 for item in inputs['entries']:
  source=ROOT/item['source']
  for path in[source,*[ROOT/p['path']for p in item['sourceDependencies']]]:
   text=path.read_text()
   if len(text.splitlines())>500 or re.search(r'/\*|//|\b(?:asm|__asm|__asm__)\b',text):raise ValueError('Ordinary C source policy differs')
  address=int(item['address'],0);directory=WORK/format(address,'08x');row,body=build(source,directory/'source',address)
  for key in['address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compilerPath','compilerSha256','compilerFlags','relocations','nativeSymbolEntries']:
   if row[key]!=item[key]:raise ValueError(('Frozen MD5 contract differs',item['address'],key))
  start=address-0x21d7240;native=image[start:start+row['bytes']]
  if row['compiledBytes']!=item['bytes']or body!=native or not row['realLink']['exactCallerBytes']:raise ValueError('Complete native MD5 genuine link differs')
  compiled[address]=body;row.update(program='',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=row['bytes'],justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceProvenance=item['sourceProvenance'],matchingBytesScope='Complete genuine MW-linked native extent including original literal pool',suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,boundaryReturnContract=item['boundaryReturnContract']);matches.append(row)
 for row in matches:
  address=int(row['address'],0);native=image[address-0x21d7240:address-0x21d7240+row['bytes']];model=prove(row,native,compiled[address]);models.append(model);wrong.append(wrong_source(row,WORK/format(address,'08x')/'wrong-C'));row['actualNativeAndSourceCallerReturns']=model['actualNativeAndSourceCallerReturns'];print('proved MD5 C',row['address'],row['bytes'],model['cases'],flush=True)
 if len(matches)!=4 or sum(r['bytes']for r in matches)!=130:raise ValueError('Frozen MD5 membership differs')
 row=matches[0];layout=layouts(row,WORK/'layout');badlayout=layouts(row,WORK/'wrong-layout',True);bindings=negative_controls(matches);prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototypes')for row in matches];missing=missing_prototype(row,WORK/'missing-prototype');closure=code_closure([Path(__file__).name])
 limits=['Four complete ordinary-C MD5 Encode/Decode/forward-byte-copy/byte-set helpers reproduce full genuine MW-linked native extents. Only130new helper bytes receive pending source credit; previous MD5 callers, AES, padding and data receive zero additional credit.','Derived from the RSA Data Security, Inc. MD5 Message-Digest Algorithm; raw complete pinned OpenMOHAA C/header and RSA notice remain. Encode/Decode retain published statements; copy/set activate the complete alternative byte-loop forms retained in published comments instead of standard-libc wrappers. Original source version/compiler identity remain unproved.','Independent mutable-byte models qualify aligned32-bit words/little-endian byte views, unaligned byte pointers, exact and both-direction partial aliases with sequential visibility, forward-copy propagation, signedint-to-lowbyte fill, whole backing/sentinel preservation and zero-length null pointers without dereferences.','Encode/Decode reference assumes lengths divisible by4. Additional nonmultiple1/3/5 fixtures measure original rounded4-byte group behavior only with enough backing; no general-safe short-buffer API promise. Word pointers stay4-aligned and tested lengths are at most64bytes.','All GPR/CPSR, callee-saved registers, stack, ordered writes and complete bounded backing compare. All four returnvoid; matching observed registers does not create a return-value promise. Strict C99 prototypes and target word/pointer widths are checked.','These are leaf functions with no source/object relocations, imported code/data/provider execution, algorithmASM or object/instruction patches. No whole game/host execution, portable host ABI completion, storage or cryptographic-security claim is made.']

 write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='ov006',allPassed=True,matches=matches,matchedFunctions=4,matchedBytes=130,ordinaryCBytes=130,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,actualNativeAndSourceCallerReturns=sum(m['actualNativeAndSourceCallerReturns']for m in models),boundedCallerModels=models,suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=badlayout,negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,negativePrototypeEvidence=missing,abiInterfaceEvidence=[dict(path=(LANE/'code-provider-interface.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'code-provider-interface.json'))],portableHostExecutionProven=False,importedOriginalProviderBodiesExecuted=False,importedProviderSourceOrExecutionCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))
if __name__=='__main__':main()
