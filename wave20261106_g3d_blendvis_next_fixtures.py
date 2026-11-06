import hashlib,random,struct
import match_runtime
from project import ROOT
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,ENTRY,CALLBACK,DATA,STACK,STOP=0x2000000,0x202e260,0x2034448,0x2300000,0x3000000,0x5000000
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC]

def run(body,index):
 rng=random.Random(ENTRY+index);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();data=bytearray(rng.randbytes(16384));count=1+index%3;node=[0,1,3,7,255,0xffffffff][index%6];tags=[0,0x100,0x200,0x300,0xffff,0x8100,0x8200,0x8300];objects=[]
 for k in range(count):
  obj=0x400+k*0x400;res=0x2000+k*0x400;objects.append(obj);frame=(index+k)%4;numNodes=256;struct.pack_into('<IIIIIIBB',data,obj,(frame<<12)|(index&4095),0,DATA+res,CALLBACK if(index+k)%5 else 0,DATA+obj+0x400 if k+1<count else 0,0,0,[0,1,4,8,255][(index+k)%5]);struct.pack_into('<H',data,res+6,numNodes)
  for j in range(255):struct.pack_into('<H',data,obj+26+2*j,tags[(index+k+j)%len(tags)]|((index*17+k*31+j)%256))
  if index%7==0:data[res+12:res+12+128]=bytes(128)
 result=DATA+objects[0]if index%9==0 else DATA+0x100;expected=bytearray(data);struct.pack_into('<I',expected,result-DATA,0);p=DATA+objects[0];expectedCalls=[];retval=0
 while p:
  at=p-DATA;n=expected[at+25]
  if node<n:
   tag=struct.unpack_from('<H',expected,at+26+2*node)[0];fn=struct.unpack_from('<I',expected,at+12)[0]
   if tag&0x100 and fn:
    resource=struct.unpack_from('<I',expected,at+8)[0]-DATA;frame=struct.unpack_from('<i',expected,at)[0]>>12;numNodes=struct.unpack_from('<H',expected,resource+6)[0];pos=frame*numNodes+(tag&255);word=struct.unpack_from('<I',expected,resource+12+4*(pos//32))[0];mask=word&(1<<(pos%32));prior=struct.unpack_from('<I',expected,result-DATA)[0];struct.pack_into('<I',expected,result-DATA,prior|mask);retval=1;expectedCalls.append(dict(object=p,index=tag&255,mask=mask,tag=tag))
  p=struct.unpack_from('<I',expected,at+16)[0]
 machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946);machine.mem_map(BASE,0x200000);machine.mem_write(BASE,image)
 if body is not None:machine.mem_write(ENTRY,body)
 machine.mem_map(DATA,16384);machine.mem_write(DATA,bytes(data));machine.mem_map(STACK,8192);machine.mem_write(STACK,rng.randbytes(8192));machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1');machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xf0000000]))
 for r in REGS:machine.reg_write(r,rng.getrandbits(32))
 for r,v in zip(REGS[:3],[result,DATA+objects[0],node]):machine.reg_write(r,v)
 machine.reg_write(UC_ARM_REG_SP,STACK+4096);machine.reg_write(UC_ARM_REG_LR,STOP);reads=[];writes=[];calls=[];pending=[];seen=set();returned=False
 def code(uc,pc,size,user):
  nonlocal returned
  if pending and pc==pending[-1]['lr']:
   item=pending.pop();calls.append(dict(object=item['args'][1],index=item['args'][2],mask=struct.unpack('<I',bytes(uc.mem_read(item['args'][0],4)))[0],tag=struct.unpack('<H',bytes(uc.mem_read(item['args'][1]+26+2*node,2)))[0]))
  if pc==STOP:assert not pending;returned=True;uc.emu_stop();return
  assert ENTRY<=pc<ENTRY+(len(body)if body is not None else 128)or CALLBACK<=pc<CALLBACK+56,hex(pc);seen.add(pc)
  if pc==CALLBACK:pending.append(dict(lr=uc.reg_read(UC_ARM_REG_LR),args=[uc.reg_read(r)for r in REGS[:3]]))
 def read(uc,access,at,size,value,user):reads.append((at,size,int.from_bytes(bytes(uc.mem_read(at,size)),'little')))
 def write(uc,access,at,size,value,user):
  assert DATA<=at and at+size<=DATA+16384 or STACK<=at and at+size<=STACK+8192;writes.append((at,size,value))
 machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write);machine.emu_start(ENTRY,STOP+4,count=10000);assert returned;assert machine.reg_read(UC_ARM_REG_SP)==STACK+4096
 output=bytes(machine.mem_read(DATA,16384))
 if body is not None:machine.mem_write(ENTRY,image[ENTRY-BASE:ENTRY-BASE+len(body)])
 assert bytes(machine.mem_read(BASE,len(image)))==image
 return dict(index=index,listLength=count,node=node,resultAliasesFirstFrame=result==DATA+objects[0],actualReturn=True,modelPassed=output==expected and machine.reg_read(UC_ARM_REG_R0)==retval and calls==expectedCalls,returnValue=machine.reg_read(UC_ARM_REG_R0),callbacks=calls,expectedCallbacks=expectedCalls,registers=[machine.reg_read(r)for r in REGS],cpsr=machine.reg_read(UC_ARM_REG_CPSR),reads=reads,writes=writes,observedInstructions=sorted(seen),dataSha256=hashlib.sha256(output).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,8192))).hexdigest(),providerSourceOrExecutionCredit=0)

def prove(body):
 records=[]
 for index in range(32):
  native,source=run(None,index),run(body,index);assert native['modelPassed']and source['modelPassed'],('tag/list model',index,native['modelPassed'],source['modelPassed']);assert native==source;records.append(native)
 assert any((c['tag']&0x300)==0x300 for r in records for c in r['callbacks']);assert any(r['returnValue']==1 and r['callbacks']and not any(c['mask']for c in r['callbacks'])for r in records)
 return dict(allPassed=True,cases=records,caseCount=len(records),actualNativeAndSourceCallerReturns=2*len(records),actualOriginalCallbackReturns=sum(len(r['callbacks'])for r in records)*2,providerSourceOrExecutionCredit=0)
