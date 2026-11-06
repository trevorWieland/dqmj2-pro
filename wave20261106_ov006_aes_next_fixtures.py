import hashlib,json,struct
import match_runtime as C
import unicorn as U
from unicorn import arm_const as A
from project import ROOT
import wave20261106_ov006_aes_next_model as M
BASE=0x21d7240
RK=0x22f0000
KEY=0x22f1000
INPUT=0x22f2000
OUTPUT=0x22f3000
SP=0x3010000
STOP=0x4000000
EXTENTS={0x21f0944:696,0x21f0bfc:400,0x21f0d8c:956,0x21f1148:956}
TABLES=[(0x2208890,40)]+[(a,1024)for a in [0x22094b8,0x22098b8,0x2209cb8,0x220a0b8,0x220a4b8,0x220a8b8,0x220acb8,0x22088b8,0x2208cb8,0x22090b8]]

def initial(address,v):
 key,plain=M.key_and_plain(v);regions={RK:bytearray([0xa5])*256,KEY:bytearray([0x77])*64,INPUT:bytearray([0x88])*64,OUTPUT:bytearray([0x99])*64};expected={a:bytearray(b)for a,b in regions.items()};bits=v['bits'];offset=v['offset'];rounds=0
 if address in[0x21f0944,0x21f0bfc]:
  regions[KEY][offset:offset+32]=key;words,rounds=(M.schedule if address==0x21f0944 else M.decrypt_schedule)(key,bits);expected={a:bytearray(b)for a,b in regions.items()};expected[RK][:len(words)*4]=b''.join(x.to_bytes(4,'little')for x in words);args=[RK,KEY+offset,bits&0xffffffff];result=rounds
 else:
  words,rounds=(M.schedule if address==0x21f0d8c else M.decrypt_schedule)(key,bits);regions[RK][:len(words)*4]=b''.join(x.to_bytes(4,'little')for x in words);cipher=M.encrypt(key,bits,plain);incoming=plain if address==0x21f0d8c else cipher;outgoing=cipher if address==0x21f0d8c else M.decrypt(key,bits,cipher);regions[INPUT][offset:offset+16]=incoming;expected={a:bytearray(b)for a,b in regions.items()};target=INPUT if v['inplace']else OUTPUT;expected[target][offset:offset+16]=outgoing;args=[RK,rounds,INPUT+offset,target+offset];result=None
 return regions,expected,args,result

def run(address,body,image,compiled,v,seed):
 regions,expected,args,result=initial(address,v);cpu=U.Uc(U.UC_ARCH_ARM,U.UC_MODE_THUMB);cpu.ctl_set_cpu_model(A.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(BASE,image)
 for at,raw in compiled.items():cpu.mem_write(at,raw)
 cpu.mem_write(address,body);cpu.mem_map(SP-0x4000,0x6000);cpu.mem_map(STOP,0x1000)
 for at,raw in regions.items():cpu.mem_write(at,bytes(raw))
 initialregs=[(0x11440000+seed*0x101+i*0x110011)&0xffffffff for i in range(15)];initialregs[:len(args)]=args;initialregs[-2:]=[SP,STOP|1];cpu.reg_write(A.UC_ARM_REG_CPSR,[0x30,0x10000030,0x80000030,0xf0000030][seed%4])
 for reg,value in zip(C.REGISTERS,initialregs):cpu.reg_write(reg,value)
 writes=[];reads=[];calls=[];pcs=[];returned=False
 def code(machine,at,size,user):
  nonlocal returned
  if at==STOP:returned=True;machine.emu_stop();return
  allowed=address<=at<address+len(body)or address==0x21f0bfc and 0x21f0944<=at<0x21f0944+696
  if not allowed or not machine.reg_read(A.UC_ARM_REG_CPSR)&32:raise ValueError(('Unexpected AES code/mode escape',hex(at)))
  if address==0x21f0bfc and at==0x21f0944:calls.append(dict(program='',processor='arm9',module='ov006',mode='thumb',address=hex(at),arguments=[machine.reg_read(r)for r in C.REGISTERS[:3]]))
  pcs.append(at)
 def write(machine,access,at,size,value,user):
  stack=SP-0x4000<=at and at+size<=SP
  allowed=stack or any(a<=at and at+size<=a+len(raw)for a,raw in regions.items())
  if not allowed:raise ValueError(('AES write escaped bounded memory',hex(at),size))
  writes.append((at,size,(value&((1<<(8*size))-1)).to_bytes(size,'little').hex()))
 def read(machine,access,at,size,value,user):
  for base,length in TABLES:
   if base<=at<base+length:
    if size!=4 or(at-base)%4 or at+size>base+length:raise ValueError('AES table access differs from aligned bounded u32')
    reads.append((base,(at-base)//4,int.from_bytes(machine.mem_read(at,4),'little')));break
 cpu.hook_add(U.UC_HOOK_CODE,code);cpu.hook_add(U.UC_HOOK_MEM_WRITE,write);cpu.hook_add(U.UC_HOOK_MEM_READ,read);cpu.emu_start(address|1,STOP+4,count=100000)
 registers=[cpu.reg_read(r)for r in C.REGISTERS];actual={a:bytes(cpu.mem_read(a,len(raw)))for a,raw in expected.items()};passed=returned and actual=={a:bytes(b)for a,b in expected.items()}and(result is None or registers[0]==result)and registers[4:12]==initialregs[4:12]and registers[13]==SP
 if address==0x21f0bfc:passed=passed and len(calls)==1 and calls[0]['arguments']==args
 trace=dict(registers=registers,cpsr=cpu.reg_read(A.UC_ARM_REG_CPSR),writes=writes,tableReads=reads,codeProviderCalls=calls,pcs=pcs,memory={hex(a):b.hex()for a,b in actual.items()})
 return dict(modelPassed=passed,topReturned=returned,traceSha256=hashlib.sha256(json.dumps(trace,sort_keys=True).encode()).hexdigest(),returnValue=registers[0],expectedReturn=result,codeProviderCalls=calls,tableReads=len(reads),memoryPassed=actual=={a:bytes(b)for a,b in expected.items()})

def prove(row,native,source,compiled):
 image=(ROOT/'extract/arm9_overlays/ov006.bin').read_bytes();address=int(row['address'],0);records=[]
 for seed,v in enumerate(M.cases(address)):
  original=run(address,native,image,{},v,seed);rebuilt=run(address,source,image,compiled,v,seed)
  if original!=rebuilt or not original['modelPassed']:raise ValueError(('Independent AES model differs',row['address'],v,original,rebuilt))
  records.append(dict(vector=v,seed=seed,traceSha256=original['traceSha256'],tableReads=original['tableReads'],selectedCodeProviderCalls=original['codeProviderCalls']))
 return dict(address=row['address'],cases=len(records),actualNativeAndSourceCallerReturns=2*len(records),records=records,allGprsCpsrCalleeSavedStackWritesMemoryAndTableAccessesCompared=True,selectedKeyEncProviderExecuted=address==0x21f0bfc,sourceProviderIsFreshGenuineCompiledKeyEnc=address==0x21f0bfc,extraProviderSourceCredit=0,unselectedCodeProvidersExecuted=0,importedTableOrRconStorageCredit=0,model=M.selfcheck())
