import copy,hashlib
from project import ROOT,read_json,sha256
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/fourteenth'

def check(value,image):
 if(value['program'],value['processor'],value['module'],value['mode'],value['caller'],value['callee'],value['originalCallOrigin'])!=('','arm9','main','thumb','0x209ad08','0x2096900','0x209addc'):raise ValueError('Original startup ABI namespace/entry differs')
 if value['originalImageSha256']!=hashlib.sha256(image).hexdigest()or value['calleeNativeExtent']!=72 or value['calleeNativeSha256']!=hashlib.sha256(image[0x96900:0x96948]).hexdigest():raise ValueError('Full original ABI source extent/hash differs')
 c=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
 def instruction(address):
  i=next(c.disasm(image[address-0x2000000:address-0x2000000+4],address));return i.mnemonic,i.op_str
 if instruction(0x209add6)!=('movs','r1, #1')or instruction(0x209addc)!=('bl','#0x2096900')or instruction(0x2096904)!=('adds','r4, r1, #0')or instruction(0x2096930)!=('movs','r0, #0x79')or instruction(0x2096934)!=('lsls','r0, r0, #4')or instruction(0x2096936)!=('str','r4, [r2, r0]')or instruction(0x209693c)!=('movs','r0, #1'):raise ValueError('Original incoming-word preservation/store/return differs')
 if value['secondWordSetup']['rawR1']!=1 or value['secondWordSetup']['address']!='0x209add6'or value['incomingR1Save']['offset']!=4 or value['incomingWordStore']['offset']!=0x36:raise ValueError('Declared startup raw-word witness differs')
 header=ROOT/'deps/reference/nitrodwc-inet-ac-9136bfa0bf3a5123ce560e6cd47017456e4c130b/include/ac/dwc_ac.h'
 if value['publishedOneArgumentDeclaration']not in header.read_text()or value['measuredSourceDeclaration']!='BOOL native_fn_02096900(DWCWDSData*,int);'or value['calleeBodySourceOrExecutionCredit']!=0:raise ValueError('Explicit old-header disagreement/zero-credit boundary differs')

def verify():
 value=read_json(LANE/'abi.json');image=(ROOT/'extract/arm9/arm9.bin').read_bytes();check(value,image);cases=[]
 for key,wrong in [('callee','0x2096902'),('originalCallOrigin','0x209adde'),('processor','arm7')]:
  bad=copy.deepcopy(value);bad[key]=wrong
  try:check(bad,image)
  except ValueError as error:cases.append(dict(case=key,rejected=True,reason=str(error)))
  else:raise ValueError('Wrong startup boundary accepted')
 bad=copy.deepcopy(value);bad['secondWordSetup']['rawR1']=0
 try:check(bad,image)
 except ValueError as error:cases.append(dict(case='wrong-second-word',rejected=True,reason=str(error)))
 else:raise ValueError('Wrong startup raw word accepted')
 return dict(allPassed=True,originalCallerAndIncomingWordFlowVerified=True,publicOneArgumentDisagreementPreserved=True,negativeControls=cases,proofSha256=sha256(LANE/'abi.json'),calleeSourceOrExecutionCredit=0)
