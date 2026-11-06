import hashlib,json,struct
import match_runtime as C
import unicorn as U
from unicorn import arm_const as A
from project import ROOT
MEM=0x22f0000
SP=0x3010000
STOP=0x4000000

def cases(address):
 if address in[0x21f1e40,0x21f1e6c]:
  values=[(0,64,128),(4,64,128),(8,64,128),(16,64,128),(64,64,128),(8,64,64),(8,64,68),(8,68,64),(1,64,128),(3,64,128),(5,64,128)]
  if address==0x21f1e40:values.extend([(8,64,65),(8,64,63)])
  else:values.extend([(8,65,128),(8,65,64)])
  return[dict(length=n,source=s,dest=d,nullZero=False)for n,s,d in values]+[dict(length=0,source=0,dest=0,nullZero=True)]
 if address==0x21f1e98:return[dict(length=n,source=s,dest=d,nullZero=False)for n,s,d in[(0,64,128),(1,64,128),(7,64,128),(64,64,128),(16,64,64),(16,64,65),(16,65,64),(63,65,66)]]+[dict(length=0,source=0,dest=0,nullZero=True)]
 return[dict(length=n,dest=d,value=v,nullZero=False)for n,d,v in[(0,128,1),(1,128,0),(1,129,128),(16,129,-1),(64,128,255),(7,127,256),(16,128,0x12345678),(8,128,0x80000000)]]+[dict(length=0,dest=0,value=0,nullZero=True)]

def initial(address,v):
 raw=bytearray((i*37+19)&255 for i in range(256));expected=bytearray(raw);n=v['length'];d=v['dest'];s=v.get('source',0)
 if address==0x21f1e40:
  for j in range(0,n,4):
   for k in range(4):word=int.from_bytes(expected[s+j:s+j+4],'little');expected[d+j+k]=(word>>(8*k))&255
 elif address==0x21f1e6c:
  for j in range(0,n,4):word=int.from_bytes(expected[s+j:s+j+4],'little');expected[d+j:d+j+4]=word.to_bytes(4,'little')
 elif address==0x21f1e98:
  for j in range(n):expected[d+j]=expected[s+j]
 else:
  for j in range(n):expected[d+j]=v['value']&255
 ptr=lambda offset:0 if v['nullZero']else MEM+offset
 args=[ptr(d),v['value']&0xffffffff,n]if address==0x21f1eb0 else[ptr(d),ptr(s),n]
 return raw,expected,args

def run(address,body,v,seed):
 raw,expected,args=initial(address,v);cpu=U.Uc(U.UC_ARCH_ARM,U.UC_MODE_THUMB);cpu.ctl_set_cpu_model(A.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x21d7240,(ROOT/'extract/arm9_overlays/ov006.bin').read_bytes());cpu.mem_write(MEM,bytes(raw));cpu.mem_write(address,body);cpu.mem_map(SP-0x4000,0x6000);cpu.mem_map(STOP,0x1000);initialregs=[(0x11440000+seed*0x101+i*0x110011)&0xffffffff for i in range(15)];initialregs[:3]=args;initialregs[-2:]=[SP,STOP|1];cpu.reg_write(A.UC_ARM_REG_CPSR,[0x30,0x10000030,0x80000030,0xf0000030][seed%4])
 for reg,value in zip(C.REGISTERS,initialregs):cpu.reg_write(reg,value)
 writes=[];pcs=[];returned=False
 def code(machine,at,size,user):
  nonlocal returned
  if at==STOP:returned=True;machine.emu_stop();return
  if not address<=at<address+len(body)or not machine.reg_read(A.UC_ARM_REG_CPSR)&32:raise ValueError('Leaf helper escaped exact Thumb body')
  pcs.append(at)
 def write(machine,access,at,size,value,user):
  if not(SP-0x4000<=at and at+size<=SP or MEM<=at and at+size<=MEM+256):raise ValueError('Leaf helper write escaped bounded backing')
  writes.append((at,size,(value&((1<<(8*size))-1)).to_bytes(size,'little').hex()))
 cpu.hook_add(U.UC_HOOK_CODE,code);cpu.hook_add(U.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,STOP+4,count=20000);regs=[cpu.reg_read(r)for r in C.REGISTERS];actual=bytes(cpu.mem_read(MEM,256));passed=returned and actual==bytes(expected)and regs[4:12]==initialregs[4:12]and regs[13]==SP;trace=dict(registers=regs,cpsr=cpu.reg_read(A.UC_ARM_REG_CPSR),writes=writes,pcs=pcs,memory=actual.hex(),stack=bytes(cpu.mem_read(SP-128,128)).hex());return dict(modelPassed=passed,topReturned=returned,memoryPassed=actual==bytes(expected),traceSha256=hashlib.sha256(json.dumps(trace,sort_keys=True).encode()).hexdigest(),voidRoutineNoReturnValuePromise=True)

def prove(row,native,source):
 records=[];address=int(row['address'],0)
 for seed,v in enumerate(cases(address)):
  a=run(address,native,v,seed);b=run(address,source,v,seed)
  if a!=b or not a['modelPassed']:raise ValueError(('Independent MD5 helper memory/alias model differs',row['address'],v,a,b))
  records.append(dict(vector=v,traceSha256=a['traceSha256']))
 return dict(address=row['address'],cases=len(records),actualNativeAndSourceCallerReturns=2*len(records),records=records,allGprsCpsrCalleeSavedStackOrderedWritesAndCompleteBackingCompared=True,sourceCodeProviders=0,importedCodeOrStorageCredit=0,zeroLengthNullBackingsNotDereferenced=True)
