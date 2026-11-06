import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_ov006_md5_next_build import build
from wave20261106_ov006_md5_next_bindings import negative_controls
from wave20261106_ov006_md5_next_controls import layouts,wrong_source,missing_prototype
from wave20261106_ov006_md5_next_fixtures import prove
from wave20261106_ov006_md5_next_prototypes import verify as prototype_preflight
LANE=ROOT/'evidence/lanes/parallel-wave20261106/ov006-md5-next'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6mn/proof'

def main():
 inputs=read_json(INPUT)
 for pin in inputs['files']:
  if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen MD5 input changed',pin['path']))
 if inputs['romSha256']!=configuration()['romSha256']:raise ValueError('ROM identity changed')
 interface=read_json(LANE/'code-provider-interface.json')
 if interface['extraCalleeCredit']or not interface['rebuiltSelectedProvidersMustBeFreshGenuineCompiledBodies']or not interface['importedOriginalProviderBodiesMayExecuteOnlyAsExplicitZeroCreditRuntimeOracle']:raise ValueError('Selected MD5 provider boundary erased')
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
  address=int(row['address'],0);native=image[address-0x21d7240:address-0x21d7240+row['bytes']];model=prove(row,native,compiled[address],compiled);models.append(model);wrong.append(wrong_source(row,WORK/format(address,'08x')/'wrong-C',compiled));row['actualNativeAndSourceCallerReturns']=model['actualNativeAndSourceCallerReturns'];print('proved MD5 C',row['address'],row['bytes'],model['cases'],flush=True)
 if len(matches)!=3 or sum(r['bytes']for r in matches)!=2322:raise ValueError('Frozen MD5 membership differs')
 row=matches[0];layout=layouts(row,WORK/'layout');badlayout=layouts(row,WORK/'wrong-layout',True);bindings=negative_controls(matches);prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototypes')for row in matches];missing=missing_prototype(row,WORK/'missing-prototype');closure=code_closure([Path(__file__).name])
 limits=['Three complete ordinary-C MD5 update/final/compression functions reproduce full genuine MW-linked native extents. Shared acceptance and complete game/host execution remain separate.','Derived from the RSA Data Security, Inc. MD5 Message-Digest Algorithm; complete unchanged OpenMOHAA-pinned comparative C/header and RSA notice are retained. ROM source revision and original compiler identity remain unproved. One pinned MW2.0/base profile matched without flag/profile/allocation search.','Independent64-step compression derives constants from sine, uses a loop rather than public unrolled expressions, and cross-checks seven standard/hashlib digest vectors. Bounded caller cases cover arbitrary compression states, byte/block/padding boundaries, unaligned byte input/output, prior partial buffers, complete blocks and64-bit bit-count wrap; backing lengths stop at200bytes. Huge input-length top bits and invalid pointers/overlap are not qualified.','Complete context88-byte state/count/buffer layout, sentinel tails, digest output and zeroized context compare against independent models. All GPR/CPSR, stack/callee-saved registers, ordered writes, provider calls and complete observed memory compare. Void routines make no return-value promise.','Selected Update/Final/compression execute original selected bodies in native fixtures and fresh genuine compiled selected bodies in source fixtures. Four original imported Encode/Decode/copy/set helper bodies execute explicitly as zero-credit runtime oracle providers; their source/portable implementation and extra execution credit are zero. Padding source/storage credit is zero.','Original configured main-reference record at021f1dcc is preserved. The actual source object emits scalar0x021ac7f4 without a pointer relocation, equal to negated MD5 step36constant0xfde5380c; native entry-reachable LDR/SUBS/rotate23 use is arithmetic. No main pointer alias/binding/config rewrite; bounded executions assert that address is never dereferenced.','These fixtures do not establish cryptographic security, hardware/provider/device behavior, complete native host ABI or an independently source-only runtime beyond the selected functions. No public binary/original executable object is a compiler/link input.']

 write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='ov006',allPassed=True,matches=matches,matchedFunctions=3,matchedBytes=2322,ordinaryCBytes=2322,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,actualNativeAndSourceCallerReturns=sum(m['actualNativeAndSourceCallerReturns']for m in models),boundedCallerModels=models,suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=badlayout,negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,negativePrototypeEvidence=missing,abiInterfaceEvidence=[dict(path=(LANE/'code-provider-interface.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'code-provider-interface.json'))],portableHostExecutionProven=False,importedOriginalProviderBodiesExecuted=True,importedProviderSourceOrExecutionCredit=0,arithmeticInterfaceEvidence=dict(path=(LANE/'arithmetic-interface.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'arithmetic-interface.json')),generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))
if __name__=='__main__':main()
