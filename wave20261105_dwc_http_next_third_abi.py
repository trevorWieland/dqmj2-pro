import hashlib,re
from project import ROOT,read_json,sha256
from wave20261105_dwc_http_next_third_bindings import inputs
from wave20261105_dwc_http_next_third_division import verify as division_proof
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
EXPECTED={0x209a738:260,0x209a83c:244}
def verify(rows):
 value,image,inventory,records,imports=inputs()
 if {int(r['address'],0):r['bytes']for r in rows}!=EXPECTED:raise ValueError('Full custom codec membership differs')
 refs=read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/base64-reference.json')
 if refs['classification']!='independent-reconstructed-C-not-original-SDK-text':raise ValueError('Comparative provenance differs')
 for pin in refs['files']:
  if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Actual base64 reference input changed')
 arithmetic=division_proof();providers={}
 for row in rows:
  text='\n'.join((ROOT/pin['path']).read_text()for pin in row['sourceDependencies']if pin['path'].endswith('.h'))
  if '-lang'not in row['compilerFlags']or row['compilerFlags'][row['compilerFlags'].index('-lang')+1]!='c99'or not row['compilerPath'].endswith('2.0/sp1p5/mwccarm.exe'):raise ValueError('Actual C99/compiler revision differs')
  for symbol,binding in row['nativeSymbolEntries'].items():
   if binding['kind']!='function':continue
   at=int(binding['address'],0);mode=binding['mode'];canonical=next((x for x in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(%s,size=0x[0-9a-f]+\) addr:0x%08x'%(mode,at),x)),None)
   if canonical is None:raise ValueError('Actual original support entry/extent/mode absent')
   size=int(re.search(r'size=(0x[0-9a-f]+)',canonical)[1],0)
   if symbol in ['_u32_div_f','_s32_div_f']:
    expected=0x2026350 if symbol=='_u32_div_f'else 0x2026144
    if at!=expected or mode!='arm'or not any(p['entry']==hex(at)for p in arithmetic['providers']):raise ValueError('Qualified compiler arithmetic identity differs')
    declaration='Compiler-emitted quotient/remainder support for visible ordinary C / and% operators; no authored call/ASM substitutes'
   else:
    declarations=re.findall(r'\bextern\s+[^;{}]*\b'+re.escape(symbol)+r'\s*\([^;{}]*\)\s*;',text)
    if len(declarations)!=1:raise ValueError('Actual selected copy/fill prototype absent')
    declaration=declarations[0]
   providers[symbol]=dict(binding=binding,canonicalInventoryRecord=canonical,bytes=size,bodySha256=hashlib.sha256(image[at-0x2000000:at-0x2000000+size]).hexdigest(),declaration=declaration,sourceCredit=0)
 d=Cs(CS_ARCH_ARM,CS_MODE_THUMB);evidence=[]
 for at,mnemonic in [(0x209a74c,'cmp'),(0x209a762,'adds'),(0x209a768,'cmp'),(0x209a7a6,'add'),(0x209a7aa,'movs'),(0x209a7be,'ldrb'),(0x209a7c4,'ldrsb'),(0x209a888,'pop'),(0x209a896,'ldrsb')]:
  raw=image[at-0x2000000:at-0x2000000+2];ins=list(d.disasm(raw,at))
  if len(ins)!=1 or ins[0].mnemonic!=mnemonic:raise ValueError(('Original codec instruction differs',hex(at),mnemonic))
  evidence.append(dict(origin=hex(at),instruction=raw.hex(),mnemonic=mnemonic,operands=ins[0].op_str))
 return dict(status='passed',callerExtents=EXPECTED,providers=providers,arithmeticQualification=arithmetic,nativeInstructionEvidence=evidence,actualReferenceInputs=refs,
  sourceProvenance='Pinned independent reconstructed C plus actual native zero-length no-write and measured2.0sp1p5 profile; not original SDK C. Base revision and forced-volatile alternatives remain uncredited.',
  algorithm='Standard6-bit encoding translated to alphabetABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.- with* padding; independent Python stdlib translation encoder and bitstream decoder verify original behavior.',
  nativeQuirks='Decode rejects nonmultiple4 length. Null output queries required byte count. Zero input leaves output untouched. Nonempty allpadding predicts0 but original loop still writes/returns1 on provided physical output even with advertised capacity0; malformed inputs map unknown signed bytes to0. These are bounded raw effects,not capacity/allocation safety guarantees.',
  supportBoundary='Two original ARM compiler helpers return R0 quotient/R1 remainder;96 actual bounded original support probes verify those results,callee-saved registers,SP/LR,ARM modes and no writes. Caller fixtures supply those verified arithmetic contracts with caller-saved/CPSR stress. Runtime bodies and original alphabet add zero additional source/execution/data credit.',
  ordinaryAlgorithmAssemblyBytes=0,additionalProviderSourceExecutionOrOriginalAlphabetCredit=0)
