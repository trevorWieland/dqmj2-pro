import hashlib,random,struct
import match_runtime
from project import ROOT
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,DATA,STACK,ENTRY,PROVIDER=0x2000000,0x2300000,0x3000000,0x2087334,0x2087e58
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC]

def run(body,index):
 rng=random.Random(ENTRY+index);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();data=bytearray(rng.randbytes(4096));stack=rng.randbytes(4096);state=[0,5,-1,4,6,0x7fffffff,-2147483648][index%7];values=[0,1,2,3,31,32,127,255]
 fields=[values[(index+k*3)%len(values)]for k in range(5)]
 for at,value in zip([0x33,0x35,0x5d,0x5e,0x5f],fields):data[at]=value
 pointer=DATA+0x800;struct.pack_into('<i',data,0,state);struct.pack_into('<I',data,0x44,pointer);a,b,c,d,e=fields
 if state==5:expected=[pointer,15,((d-2)*8)%256,(((a-c+b-3)*8+4)%256+2)%256,12,10]
 else:expected=[pointer,0,((d-3)*8)%256,(((e-2)*8+4)%256+2)%256,12,10]
 machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946);machine.mem_map(BASE,0x200000);machine.mem_write(BASE,image)
 if body is not None:machine.mem_write(ENTRY,body)
 machine.mem_map(DATA,4096);machine.mem_write(DATA,bytes(data));machine.mem_map(STACK,4096);machine.mem_write(STACK,stack);machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xf0000000]))
 for r in REGS:machine.reg_write(r,rng.getrandbits(32))
 machine.reg_write(UC_ARM_REG_R0,DATA);machine.reg_write(UC_ARM_REG_SP,STACK+2048);machine.reg_write(UC_ARM_REG_LR,0x4000000);reads=[];writes=[];seen=[];stopped=False;actual=[]
 def code(uc,pc,size,user):
  nonlocal stopped,actual
  if pc==PROVIDER:
   sp=uc.reg_read(UC_ARM_REG_SP);actual=[uc.reg_read(r)for r in REGS[:4]]+list(struct.unpack('<II',bytes(uc.mem_read(sp,8))));stopped=True;uc.emu_stop();return
  assert ENTRY<=pc<ENTRY+160;seen.append(pc)
 def read(uc,access,at,size,value,user):reads.append((at,size,int.from_bytes(bytes(uc.mem_read(at,size)),'little')))
 def write(uc,access,at,size,value,user):
  assert STACK<=at and at+size<=STACK+4096;writes.append((at,size,value))
 machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write);machine.emu_start(ENTRY,PROVIDER+4,count=1000);assert stopped
 if body is not None:machine.mem_write(ENTRY,image[ENTRY-BASE:ENTRY-BASE+len(body)])
 assert bytes(machine.mem_read(BASE,len(image)))==image
 return dict(index=index,state=state,fields=fields,expectedArguments=expected,actualArguments=actual,modelPassed=actual==expected,explicitProviderEntryStop=True,actualCallerReturn=False,providerBodyExecuted=False,registers=[machine.reg_read(r)for r in REGS],cpsr=machine.reg_read(UC_ARM_REG_CPSR),reads=reads,writes=writes,dataSha256=hashlib.sha256(bytes(machine.mem_read(DATA,4096))).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,4096))).hexdigest(),instructions=seen,providerSourceOrExecutionCredit=0)

def prove(body):
 cases=[]
 for index in range(28):
  native,source=run(None,index),run(body,index);assert native['modelPassed']and source['modelPassed'];assert native==source;cases.append(native)
 return dict(allPassed=True,cases=cases,caseCount=len(cases),nativeAndSourceExplicitProviderStops=2*len(cases),actualNativeAndSourceCallerReturns=0,providerSourceOrExecutionCredit=0)
