import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_ov006_aes_next_build import build
from wave20261106_ov006_aes_next_bindings import negative_controls
from wave20261106_ov006_aes_next_controls import layouts,wrong_source,missing_prototype
from wave20261106_ov006_aes_next_fixtures import prove
from wave20261106_ov006_aes_next_prototypes import verify as prototype_preflight
LANE=ROOT/'evidence/lanes/parallel-wave20261106/ov006-aes-next'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6an/proof'

def main():
 inputs=read_json(INPUT)
 for pin in inputs['files']:
  if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen AES input changed',pin['path']))
 if inputs['romSha256']!=configuration()['romSha256']:raise ValueError('ROM identity changed')
 interface=read_json(LANE/'code-provider-interface.json')
 if interface['extraCalleeCredit']or interface['unselectedCodeProvidersExecuted']or not interface['rebuiltExecutionRequiresFreshGenuineCompiledKeyEnc']:raise ValueError('Selected AES provider boundary erased')
 image=(ROOT/'extract/arm9_overlays/ov006.bin').read_bytes();matches=[];compiled={};models=[];wrong=[]
 for item in inputs['entries']:
  source=ROOT/item['source']
  for path in[source,*[ROOT/p['path']for p in item['sourceDependencies']]]:
   text=path.read_text()
   if len(text.splitlines())>500 or re.search(r'/\*|//|\b(?:asm|__asm|__asm__)\b',text):raise ValueError('Ordinary C source policy differs')
  address=int(item['address'],0);directory=WORK/format(address,'08x');row,body=build(source,directory/'source',address)
  for key in['address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compilerPath','compilerSha256','compilerFlags','relocations','nativeSymbolEntries']:
   if row[key]!=item[key]:raise ValueError(('Frozen AES contract differs',item['address'],key))
  start=address-0x21d7240;native=image[start:start+row['bytes']]
  if row['compiledBytes']!=item['bytes']or body!=native or not row['realLink']['exactCallerBytes']:raise ValueError('Complete native AES genuine link differs')
  compiled[address]=body;row.update(program='',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=row['bytes'],justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceProvenance=item['sourceProvenance'],matchingBytesScope='Complete genuine MW-linked native extent including original literal pool',suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,boundaryReturnContract=item['boundaryReturnContract']);matches.append(row)
 for row in matches:
  address=int(row['address'],0);native=image[address-0x21d7240:address-0x21d7240+row['bytes']];model=prove(row,native,compiled[address],compiled);models.append(model);wrong.append(wrong_source(row,WORK/format(address,'08x')/'wrong-C',compiled));row['actualNativeAndSourceCallerReturns']=model['actualNativeAndSourceCallerReturns'];print('proved AES C',row['address'],row['bytes'],model['cases'],flush=True)
 if len(matches)!=4 or sum(r['bytes']for r in matches)!=3008:raise ValueError('Frozen AES membership differs')
 row=matches[0];layout=layouts(row,WORK/'layout');badlayout=layouts(row,WORK/'wrong-layout',True);bindings=negative_controls(matches);prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototypes')for row in matches];missing=missing_prototype(row,WORK/'missing-prototype');closure=code_closure([Path(__file__).name])
 limits=['Four complete ordinary-C AES functions reproduce full genuine MW-linked native extents. Shared acceptance and complete game/host execution remain separate.','Complete pinned Heimdal rijndael3.0-lineage public C supplies comparative source. The ROM source revision and original compiler identity remain unproved; the first pinned MW2.0/base profile matched without a flag/profile/allocation search.','Independent GF(2^8) arithmetic derives substitution and key expansion without original tables, validating AES128/192/256 known answers, block encryption/decryption, zero/high-bit/pattern vectors, unaligned byte inputs and in-place output. Standard valid rounds10/12/14 only; round-key words are aligned.','Invalid key sizes0/64/129/512/-1 return0 after reading32key bytes and writing8big-endian-loaded words. Fixtures supply readable32-byte backing; invalid sizes do not promise untouched output. Complete output/tail/input memory, all GPR/CPSR, stack, ordered writes and table-access traces compare.','KeyDec executes the selected full original KeyEnc in native fixtures and freshly compiled genuinely linked KeyEnc in rebuilt fixtures. Both are separately credited only once as selected complete functions; extra code-provider/callee credit is zero.','Ten original AES tables and rcon are imported original ov006 data with explicit original relocation/mode/entry witnesses. Their initialized-storage source credit in this packet is zero; table reconstruction belongs to a separate worker. No public binary or original executable object is a compiler/link input.','These bounded functional fixtures do not establish cryptographic security, side-channel properties, invalid-pointer safety, arbitrary round-count behavior, hardware/network provider behavior or complete portable host execution.']
 write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='ov006',allPassed=True,matches=matches,matchedFunctions=4,matchedBytes=3008,ordinaryCBytes=3008,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,actualNativeAndSourceCallerReturns=sum(m['actualNativeAndSourceCallerReturns']for m in models),boundedCallerModels=models,suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=badlayout,negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,negativePrototypeEvidence=missing,abiInterfaceEvidence=[dict(path=(LANE/'code-provider-interface.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'code-provider-interface.json'))],portableHostExecutionProven=False,generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))
if __name__=='__main__':main()
