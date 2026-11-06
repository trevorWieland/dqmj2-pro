import hashlib,json,random,struct
import match_runtime as C
import unicorn as U
from unicorn import arm_const as A
from project import ROOT,read_json,write_json,sha256
LANE=ROOT/'evidence/lanes/parallel-wave20261106/ov006-crypto-utility-next'
SIZES={0x2026124:32,0x2026350:484}

def run(address,arguments,seed):
 image=(ROOT/'extract/arm9/arm9.bin').read_bytes();cpu=U.Uc(U.UC_ARCH_ARM,U.UC_MODE_ARM);cpu.ctl_set_cpu_model(A.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x300000);cpu.mem_write(0x2000000,image);cpu.mem_map(0x3000000,0x20000);cpu.mem_map(0x4000000,0x1000);sp=0x3010000;initial=[(0x10203040+i*0x111001+seed)&0xffffffff for i in range(15)];initial[:len(arguments)]=arguments;initial[13:]=[sp,0x4000000];flags=[0x10,0x10000010,0x80000010,0xf0000010][seed%4];cpu.reg_write(A.UC_ARM_REG_CPSR,flags)
 for r,v in zip(C.REGISTERS,initial):cpu.reg_write(r,v)
 pcs=[];writes=[];returned=False
 def code(machine,at,size,user):
  nonlocal returned
  if at==0x4000000:returned=True;machine.emu_stop();return
  if not(address<=at<address+SIZES[address])or machine.reg_read(A.UC_ARM_REG_CPSR)&32:raise ValueError('Native helper escaped exact ARM body')
  pcs.append(at)
 def write(machine,access,at,size,value,user):
  if not sp-64<=at<sp:raise ValueError('Native helper wrote outside bounded stack')
  writes.append((at,size,value))
 cpu.hook_add(U.UC_HOOK_CODE,code);cpu.hook_add(U.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address,0x4000004,count=10000);regs=[cpu.reg_read(r)for r in C.REGISTERS];assert returned and regs[4:12]==initial[4:12]and regs[13]==sp
 if address==0x2026124:expected=(((arguments[0]|arguments[1]<<32)*(arguments[2]|arguments[3]<<32))&((1<<64)-1));assert regs[:2]==[expected&0xffffffff,expected>>32]and cpu.reg_read(A.UC_ARM_REG_CPSR)==flags
 else:assert arguments[1]and regs[:2]==list(divmod(*arguments[:2]))
 return dict(arguments=arguments,r0=regs[0],r1=regs[1],allGprs=regs,cpsr=cpu.reg_read(A.UC_ARM_REG_CPSR),calleeSavedAndStackPointerPreserved=True,orderedWrites=writes,traceSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())

def qualify(symbol,contract):
 expected={'_ll_mul':0x2026124,'_u32_div_f':0x2026350}
 if symbol not in expected or(contract.get('program')or'',contract.get('processor'),contract.get('module'),contract.get('mode'),contract.get('kind'),int(contract.get('address','0'),0))!=('','arm9','main','arm','function',expected[symbol]):raise ValueError('Compiler helper namespace/entry/mode mismatch')
 address=expected[symbol];size=SIZES[address]
 if contract.get('bytes',size)!=size:raise ValueError('Compiler helper complete extent mismatch')
 image=(ROOT/'extract/arm9/arm9.bin').read_bytes();actual=hashlib.sha256(image[address-0x2000000:address-0x2000000+size]).hexdigest()
 if contract.get('nativeSpanSha256',actual)!=actual:raise ValueError('Compiler helper body hash mismatch')
 canonical='func_%08x kind:function(arm,size=0x%x) addr:0x%08x'%(address,size,address)
 if canonical not in(ROOT/'config/arm9/symbols.txt').read_text().splitlines():raise ValueError('Compiler helper original canonical boundary absent')
 return address

def main():
 symbols=(ROOT/'config/arm9/symbols.txt').read_text();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();rng=random.Random(0x2612426350);values=[0,1,2,255,256,0x7fffffff,0x80000000,0xffffffff,0x12345678];out=[]
 for address,size in SIZES.items():
  canonical='func_%08x kind:function(arm,size=0x%x) addr:0x%08x'%(address,size,address);assert canonical in symbols.splitlines();vectors=[]
  if address==0x2026124:
   vals=[0,1,0xffffffff,1<<32,(1<<63)-1,1<<63,(1<<64)-1,0x123456789abcdef0]
   vectors=[[a&0xffffffff,a>>32,b&0xffffffff,b>>32]for a in vals for b in vals]
  else:vectors=[[a,b]for a in values for b in values if b]+[[rng.getrandbits(32),rng.getrandbits(32)or 1]for i in range(32)]
  rows=[run(address,v,i)for i,v in enumerate(vectors)];out.append(dict(program='',processor='arm9',module='main',mode='arm',address=hex(address),bytes=size,canonicalInventoryRecord=canonical,nativeSpanSha256=hashlib.sha256(image[address-0x2000000:address-0x2000000+size]).hexdigest(),model='R0/R1 low/high64-bit product modulo2^64'if address==0x2026124 else'R0 unsigned quotient,R1 unsigned remainder; nonzero divisor only',cases=rows,sourceOrExecutionCredit=0))
 rejected=[]
 for item in out:
  symbol='_ll_mul'if int(item['address'],0)==0x2026124 else'_u32_div_f';contract={k:item[k]for k in['program','processor','module','mode','address','bytes','nativeSpanSha256']};contract['kind']='function';qualify(symbol,contract)
  for field,value in [('program','child'),('processor','arm7'),('module','ov006'),('mode','thumb'),('address',hex(int(item['address'],0)+4)),('address',hex(int(item['address'],0)+8)),('bytes',item['bytes']-4),('nativeSpanSha256','0'*64),('address','0x2026350'if symbol=='_ll_mul'else'0x2026124')]:
   wrong=dict(contract);wrong[field]=value
   try:qualify(symbol,wrong)
   except ValueError as error:rejected.append(dict(address=item['address'],field=field,value=value,rejected=True,reason=str(error)))
   else:raise ValueError('Bad compiler-helper contract passed')
 write_json(LANE/'runtime-helper-abi.json',dict(allPassed=True,helpers=out,negativeExactNamespaceEntryModeExtentControls=rejected,originalMainImage=dict(path='extract/arm9/arm9.bin',sha256=sha256(ROOT/'extract/arm9/arm9.bin')),originalMainInventory=dict(path='config/arm9/symbols.txt',sha256=sha256(ROOT/'config/arm9/symbols.txt')),compilerSymbolNamesRequireActualObjectAndOriginalCallerBranchWitness=True,mainInteriorEntryAliasesAuthorized=False,sourceOrExecutionCredit=0));print(dict(helperCases=sum(len(x['cases'])for x in out),allPassed=True,sha256=sha256(LANE/'runtime-helper-abi.json')))
if __name__=='__main__':main()
