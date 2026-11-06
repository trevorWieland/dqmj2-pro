import hashlib,random,struct,re
import match_runtime
from project import ROOT
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,ENTRY,DATA,STACK,MMIO,STOP=0x2000000,0x2031b44,0x2300000,0x3000000,0x4000000,0x5000000
PROVIDERS={0x2031ef0:140,0x202e300:92,0x2004668:48,0x2008d4c:44,0x200197c:52,0x202e434:228,0x2008c40:24}
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC]

def cases():return list(range(13))

def run(body,index):
 rng=random.Random(ENTRY+index);original=(ROOT/'extract/arm9/arm9.bin').read_bytes();image=bytearray(original+bytes(0x100000-len(original)));struct.pack_into('<III',image,0xedf84,0,0,0);initial=bytes(image);data=bytearray(rng.randbytes(16384));data[0x400:0x800]=bytes(1024);active=index>=5;flag=[0,2,0x200,0x201,0x80000200][index]if not active else 1;stream=DATA+0x2000;material=DATA+0x1000;texmode=(index-5)%4 if active else 0;width=[0,1,16,31,256,512,2048,65535][(index-5)%8];height=[0,1,2,7,16,255,1024,65535][(index-5)%8];tex=(texmode<<30)|0x12345
 struct.pack_into('<I',data,0x400,stream);struct.pack_into('<I',data,0x408,flag);struct.pack_into('<I',data,0x4b0,material);struct.pack_into('<I',data,0x1010,tex);struct.pack_into('<HH',data,0x102c,width,height);expectedData=bytearray(data);expectedImage=bytearray(initial);expectedFifo=[]
 if active:
  expectedFifo=[0x13,30]
  if texmode!=3:tex=(tex&0x3fffffff)|0xc0000000;struct.pack_into('<I',expectedData,0x1010,tex);struct.pack_into('<I',expectedImage,0xdd694,tex);expectedFifo.extend([0x2a,tex])
  for off,value in[(0,width<<15),(20,(-height<<15)&0xffffffff),(48,width<<15),(52,height<<15)]:struct.pack_into('<I',expectedImage,0xdd6c0+off,value&0xffffffff)
 else:struct.pack_into('<I',expectedData,0x400,stream+3)
 machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946);machine.mem_map(BASE,0x200000);machine.mem_write(BASE,initial)
 if body is not None:machine.mem_write(ENTRY,body)
 machine.mem_map(DATA,16384);machine.mem_write(DATA,bytes(data));machine.mem_map(STACK,16384);machine.mem_write(STACK,rng.randbytes(16384));machine.mem_map(MMIO,65536);machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1');clip=[rng.randrange(-65536,65537)for _ in range(16)];machine.mem_write(MMIO+0x640,struct.pack('<16i',*clip));machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xf0000000]))
 for r in REGS:machine.reg_write(r,rng.getrandbits(32))
 machine.reg_write(UC_ARM_REG_R0,DATA+0x400);machine.reg_write(UC_ARM_REG_R1,rng.getrandbits(32));machine.reg_write(UC_ARM_REG_SP,STACK+8192);machine.reg_write(UC_ARM_REG_LR,STOP);reads=[];writes=[];fifowrites=[];seen=set();pending=[];returns=[];returned=False;stopped=False;args=[];matrixOutput=None
 def code(uc,pc,size,user):
  nonlocal returned,stopped,args,matrixOutput
  if pending and pc==pending[-1]['lr']:
   call=pending.pop();returns.append(call['entry'])
   if call['entry']==0x2031ef0:
    matrixOutput=list(struct.unpack('<12i',bytes(uc.mem_read(call['args'][0],48))))
  if pc==STOP:assert not pending;returned=True;uc.emu_stop();return
  if pc==0x202e434 and uc.reg_read(UC_ARM_REG_LR)==ENTRY+0x124:
   args=[uc.reg_read(r)for r in REGS[:3]];stopped=True;uc.emu_stop();return
  assert ENTRY<=pc<ENTRY+940 or any(a<=pc<a+n for a,n in PROVIDERS.items()),hex(pc);seen.add(pc)
  if pc in PROVIDERS:pending.append(dict(entry=pc,lr=uc.reg_read(UC_ARM_REG_LR),args=[uc.reg_read(r)for r in REGS[:4]]))
 def read(uc,access,at,size,value,user):reads.append((at,size,int.from_bytes(bytes(uc.mem_read(at,size)),'little')))
 def write(uc,access,at,size,value,user):
  assert DATA<=at and at+size<=DATA+16384 or STACK<=at and at+size<=STACK+16384 or MMIO<=at and at+size<=MMIO+65536 or 0x20dd690<=at and at+size<=0x20dd698 or 0x20dd6c0<=at and at+size<=0x20dd700,(hex(at),size)
  writes.append((at,size,value))
  if at==MMIO+0x400:fifowrites.append(value)
 machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write);machine.emu_start(ENTRY,STOP+4,count=20000);assert returned or stopped,('no declared endpoint',index)
 if body is not None:machine.mem_write(ENTRY,initial[ENTRY-BASE:ENTRY-BASE+len(body)])
 actualImage=bytes(machine.mem_read(BASE,len(initial)));actualData=bytes(machine.mem_read(DATA,16384));expectedMatrix=[clip[j]for j in[0,1,2,4,5,6,8,9,10,12,13,14]]
 passed=(actualImage==expectedImage and actualData==expectedData and fifowrites==expectedFifo and returned==(not active) and stopped==active)
 if active:passed=passed and args==[0x16,0x20dd6c0,16]and matrixOutput==expectedMatrix
 return dict(index=index,active=active,flag=flag,width=width,height=height,textureMode=texmode,actualCallerReturn=returned,explicitMatrixProviderEntryStop=stopped,modelPassed=passed,matrixProviderArguments=args,actualGetCurrentMatrix=matrixOutput,expectedCurrentMatrix=expectedMatrix if active else None,geometryFifoWrites=fifowrites,expectedFifoWrites=expectedFifo,registers=[machine.reg_read(r)for r in REGS],cpsr=machine.reg_read(UC_ARM_REG_CPSR),reads=reads,writes=writes,observedInstructions=sorted(seen),originalProviderReturns=returns,boundedMainRamSha256=hashlib.sha256(actualImage).hexdigest(),dataSha256=hashlib.sha256(actualData).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,16384))).hexdigest(),mmioSha256=hashlib.sha256(bytes(machine.mem_read(MMIO,65536))).hexdigest(),providerSourceOrExecutionCredit=0,actualGraphicsHardwareExecution=False)

def prove(body):
 records=[]
 for index in cases():
  native,source=run(None,index),run(body,index);assert native['modelPassed']and source['modelPassed'],('matrix model',index,native['modelPassed'],source['modelPassed']);assert native==source,('native/source',index);records.append(native)
 return dict(allPassed=True,cases=records,caseCount=len(records),actualNativeAndSourceCallerReturns=2*sum(r['actualCallerReturn']for r in records),nativeAndSourceExplicitProviderStops=2*sum(r['explicitMatrixProviderEntryStop']for r in records),originalProviderSourceOrExecutionCredit=0,limits=['Fixed bounded CPU/MMIO-memory fixture, not graphics hardware emulation or GPU rendering.','Active paths stop before the real matrix-command provider; later material/effect/global-matrix/callback phases unexecuted.','Original GetCurrentMtx/clip/copy/command-provider code executes with zero new source or device-execution credit.'])
