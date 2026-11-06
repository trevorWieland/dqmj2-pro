import hashlib,json,struct
import match_runtime as C
import unicorn as U
from unicorn import arm_const as A
from project import ROOT
import wave20261106_ov006_md5_next_model as M
BASE=0x21d7240
CTX=0x22f0000
INPUT=0x22f1000
OUTPUT=0x22f2000
SP=0x3010000
STOP=0x4000000
EXTENTS={0x21f152c:118,0x21f15a4:84,0x21f15f8:2120}
IMPORTED={0x21f1e40:44,0x21f1e6c:42,0x21f1e98:22,0x21f1eb0:22}

def initial(address,v):
 regions={CTX:bytearray([0xa5])*96,INPUT:bytearray([0x77])*512,OUTPUT:bytearray([0x99])*32};offset=v.get('offset',0)
 if address==0x21f15f8:
  style=v['style'];state=M.IV if style<3 else[(0x1020304*(i+1)+style)&M.MASK for i in range(4)];block=bytes(64)if style==0 else bytes([255])*64 if style==1 else M.pattern(64,style);regions[CTX][:16]=struct.pack('<4I',*state);regions[INPUT][offset:offset+64]=block;expected={a:bytearray(b)for a,b in regions.items()};expected[CTX][:16]=struct.pack('<4I',*M.compress(state,block));args=[CTX,INPUT+offset]
 elif address==0x21f152c:
  ctx=M.update(M.context(),M.pattern(v['prefix']));payload=M.pattern(v['length'],2)
  if v['wrap']:ctx[16:24]=struct.pack('<Q',0xfffffffffffffff8)
  regions[CTX][:88]=ctx;regions[INPUT][offset:offset+len(payload)]=payload;expected={a:bytearray(b)for a,b in regions.items()};expected[CTX][:88]=M.update(ctx,payload);args=[CTX,INPUT+offset,len(payload)]
 else:
  message=M.pattern(v['length'],v['style']);ctx=M.update(M.context(),message);regions[CTX][:88]=ctx;expected={a:bytearray(b)for a,b in regions.items()};digest,wiped=M.final(ctx);assert digest==hashlib.md5(message).digest();expected[CTX][:88]=wiped;expected[OUTPUT][offset:offset+16]=digest;args=[OUTPUT+offset,CTX]
 return regions,expected,args

def run(address,body,image,compiled,v,seed):
 regions,expected,args=initial(address,v);cpu=U.Uc(U.UC_ARCH_ARM,U.UC_MODE_THUMB);cpu.ctl_set_cpu_model(A.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(BASE,image)
 for at,raw in compiled.items():cpu.mem_write(at,raw)
 cpu.mem_write(address,body);cpu.mem_map(SP-0x4000,0x6000);cpu.mem_map(STOP,0x1000)
 for at,raw in regions.items():cpu.mem_write(at,bytes(raw))
 initialregs=[(0x11440000+seed*0x101+i*0x110011)&0xffffffff for i in range(15)];initialregs[:len(args)]=args;initialregs[-2:]=[SP,STOP|1];cpu.reg_write(A.UC_ARM_REG_CPSR,[0x30,0x10000030,0x80000030,0xf0000030][seed%4])
 for reg,value in zip(C.REGISTERS,initialregs):cpu.reg_write(reg,value)
 writes=[];calls=[];pcs=[];returned=False;allowedSelected={address}
 if address==0x21f152c:allowedSelected.add(0x21f15f8)
 if address==0x21f15a4:allowedSelected.update(EXTENTS)
 def code(machine,at,size,user):
  nonlocal returned
  if at==STOP:returned=True;machine.emu_stop();return
  allowed=any(a<=at<a+(len(body)if a==address else EXTENTS[a])for a in allowedSelected)or any(a<=at<a+n for a,n in IMPORTED.items())
  if not allowed or not machine.reg_read(A.UC_ARM_REG_CPSR)&32:raise ValueError(('Unexpected MD5 code/mode escape',hex(at)))
  if at in IMPORTED or at in EXTENTS and(len(pcs)>0 or at!=address):calls.append(dict(address=hex(at),arguments=[machine.reg_read(r)for r in C.REGISTERS[:3 if at in IMPORTED or at==0x21f152c else 2]],selectedSamePacket=at in EXTENTS,importedProviderCredit=0))
  pcs.append(at)
 def write(machine,access,at,size,value,user):
  if not(SP-0x4000<=at and at+size<=SP or any(a<=at and at+size<=a+len(raw)for a,raw in regions.items())):raise ValueError(('MD5 write escaped bounded frame',hex(at),size))
  writes.append((at,size,(value&((1<<(8*size))-1)).to_bytes(size,'little').hex()))
 def read(machine,access,at,size,value,user):
  if at<=0x21ac7f4<at+size:raise ValueError('MD5 arithmetic constant dereferenced as main pointer')
 cpu.hook_add(U.UC_HOOK_CODE,code);cpu.hook_add(U.UC_HOOK_MEM_WRITE,write);cpu.hook_add(U.UC_HOOK_MEM_READ,read);cpu.emu_start(address|1,STOP+4,count=200000)
 registers=[cpu.reg_read(r)for r in C.REGISTERS];actual={a:bytes(cpu.mem_read(a,len(raw)))for a,raw in expected.items()};memory=actual=={a:bytes(b)for a,b in expected.items()};passed=returned and memory and registers[4:12]==initialregs[4:12]and registers[13]==SP
 trace=dict(registers=registers,cpsr=cpu.reg_read(A.UC_ARM_REG_CPSR),writes=writes,providerCalls=calls,pcs=pcs,memory={hex(a):b.hex()for a,b in actual.items()})
 return dict(modelPassed=passed,topReturned=returned,traceSha256=hashlib.sha256(json.dumps(trace,sort_keys=True).encode()).hexdigest(),providerCalls=calls,memoryPassed=memory,arithmeticConstantNeverDereferenced=True)

def prove(row,native,source,compiled):
 image=(ROOT/'extract/arm9_overlays/ov006.bin').read_bytes();address=int(row['address'],0);records=[]
 for seed,v in enumerate(M.cases(address)):
  original=run(address,native,image,{},v,seed);rebuilt=run(address,source,image,compiled,v,seed)
  if original!=rebuilt or not original['modelPassed']:raise ValueError(('Independent MD5 model differs',row['address'],v,original,rebuilt))
  records.append(dict(vector=v,seed=seed,traceSha256=original['traceSha256'],providerCalls=original['providerCalls']))
 return dict(address=row['address'],cases=len(records),actualNativeAndSourceCallerReturns=2*len(records),records=records,allGprsCpsrCalleeSavedStackWritesAndMemoryCompared=True,selectedProvidersUseFreshGenuineCompiledBodies=True,unselectedOriginalHelperBodiesExecutedAsOracleProviders=True,importedProviderSourceOrExecutionCredit=0,paddingStorageCredit=0,arithmeticConstantNeverDereferenced=True,model=M.selfcheck())
