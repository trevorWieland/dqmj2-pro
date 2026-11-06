import hashlib,json,struct
import match_runtime as C
import unicorn as U
from unicorn import arm_const as A
from project import ROOT
import wave20261106_ov006_crypto_utility_next_first_model as M
CTX,STATE,INPUT,OUTPUT,TABLE=0x22f0000,0x22f1000,0x22f2000,0x22f3000,0x22f4000
SP,STOP=0x3010000,0x4000000
EXTENTS={0x21ed86c:98,0x21ed8d0:44,0x21ed8fc:62,0x21ed964:54,0x21f08fc:70}

def initial(address,v):
 regions={CTX:bytearray([0xa5])*32,STATE:bytearray([0xa5])*512,INPUT:bytearray((i*37+19)&255 for i in range(256)),OUTPUT:bytearray((i*11+19)&255 for i in range(256)),TABLE:bytearray([0xa5])*1024};result=None
 if address in[0x21ed86c,0x21ed8d0,0x21ed8fc]:
  n=v['n'];key=bytes(range(1,17));regions[INPUT][:16]=key;state=M.ksa(key[:5],n)if n else[];x=v.get('x',0);y=v.get('y',0);regions[CTX][:16]=struct.pack('<4I',x,y,STATE,n);regions[STATE][:n]=bytes(state);expected={a:bytearray(b)for a,b in regions.items()}
  if address==0x21ed86c:
   keyLength=v['keyLength'];expected[CTX][:16]=struct.pack('<4I',0,0,STATE,n);expected[STATE][:n]=bytes(M.ksa(key[:max(1,keyLength)],n));args=[CTX,INPUT,keyLength,n]
  elif address==0x21ed8fc:
   x,y,result=M.step(x,y,state,n);expected[CTX][:8]=struct.pack('<2I',x,y);expected[STATE][:n]=bytes(state);args=[CTX]
  else:
   dest=OUTPUT if v['alias']==0 else INPUT if v['alias']==1 else INPUT+1;args=[CTX,dest,INPUT,v['length']]
   for i in range(v['length']):x,y,b=M.step(x,y,state,n);region=OUTPUT if dest==OUTPUT else INPUT;offset=0 if dest in[INPUT,OUTPUT]else 1;incoming=expected[INPUT][i];expected[region][offset+i]=incoming^b
   expected[CTX][:8]=struct.pack('<2I',x,y);expected[STATE][:n]=bytes(state)
 elif address==0x21ed964:
  data=b'123456789';regions[INPUT][:9]=data;table=M.crc_table();regions[TABLE][:]=struct.pack('<256I',*table)if v['ready']else bytes([0xa5])*1024;expected={a:bytearray(b)for a,b in regions.items()};expected[TABLE][:]=struct.pack('<256I',*table);result=M.crc(v['seed'],bytes(regions[INPUT][:max(0,v['length'])]),table);args=[v['seed'],INPUT,v['length']&0xffffffff,v['ready'],TABLE]
 else:
  alias=v['alias'];offset=v['offset'];dest=[OUTPUT,INPUT,STATE,INPUT+1,STATE+1][alias];regions[STATE][:256]=regions[INPUT];expected={a:bytearray(b)for a,b in regions.items()};args=[INPUT+offset,STATE+offset,dest+offset]
  for i in range(8):region=OUTPUT if dest==OUTPUT else INPUT if dest in[INPUT,INPUT+1]else STATE;outoff=(1 if dest in[INPUT+1,STATE+1]else 0)+offset+i;expected[region][outoff]=expected[INPUT][offset+i]^expected[STATE][offset+i]
 return regions,expected,args,result

def run(address,body,compiled,v,seed):
 regions,expected,args,result=initial(address,v);cpu=U.Uc(U.UC_ARCH_ARM,U.UC_MODE_THUMB);cpu.ctl_set_cpu_model(A.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,(ROOT/'extract/arm9/arm9.bin').read_bytes());cpu.mem_write(0x21d7240,(ROOT/'extract/arm9_overlays/ov006.bin').read_bytes())
 for at,raw in compiled.items():cpu.mem_write(at,raw)
 cpu.mem_write(address,body);cpu.mem_map(SP-0x4000,0x6000);cpu.mem_map(STOP,0x1000)
 for at,raw in regions.items():cpu.mem_write(at,bytes(raw))
 if len(args)>4:cpu.mem_write(SP,struct.pack('<I',args[4]))
 initialregs=[(0x11440000+seed*0x101+i*0x110011)&0xffffffff for i in range(15)];initialregs[:min(4,len(args))]=args[:4];initialregs[-2:]=[SP,STOP|1];cpu.reg_write(A.UC_ARM_REG_CPSR,[0x30,0x10000030,0x80000030,0xf0000030][seed%4])
 for reg,value in zip(C.REGISTERS,initialregs):cpu.reg_write(reg,value)
 writes=[];calls=[];pcs=[];returned=False;ranges={address:len(body)}
 if address==0x21ed8d0:ranges[0x21ed8fc]=62
 if address==0x21ed964:ranges[0x21ed99c]=56
 def code(machine,at,size,user):
  nonlocal returned
  if at==STOP:returned=True;machine.emu_stop();return
  arm=0x2026350<=at<0x2026350+484;thumb=any(a<=at<a+n for a,n in ranges.items())
  if not(arm or thumb)or bool(machine.reg_read(A.UC_ARM_REG_CPSR)&32)!=thumb:raise ValueError(('Crypto namespace/mode escape',hex(at)))
  if at in[0x2026350,0x21ed99c]or at==0x21ed8fc and address!=at:calls.append(dict(address=hex(at),arguments=[machine.reg_read(r)for r in C.REGISTERS[:2 if at in[0x2026350,0x21ed99c]else 1]],mode='arm'if arm else'thumb',importedProviderSourceOrExecutionCredit=0))
  pcs.append(at)
 def write(machine,access,at,size,value,user):
  if not(SP-0x4000<=at and at+size<=SP or any(a<=at and at+size<=a+len(raw)for a,raw in regions.items())):raise ValueError(('Crypto write escaped bounded frame',hex(at),size))
  writes.append((at,size,(value&((1<<(8*size))-1)).to_bytes(size,'little').hex()))
 cpu.hook_add(U.UC_HOOK_CODE,code);cpu.hook_add(U.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,STOP+4,count=300000);registers=[cpu.reg_read(r)for r in C.REGISTERS];actual={a:bytes(cpu.mem_read(a,len(raw)))for a,raw in expected.items()};memory=actual=={a:bytes(b)for a,b in expected.items()};passed=returned and memory and(result is None or registers[0]==result)and registers[4:12]==initialregs[4:12]and registers[13]==SP
 trace=dict(registers=registers,cpsr=cpu.reg_read(A.UC_ARM_REG_CPSR),writes=writes,providerCalls=calls,pcs=pcs,memory={hex(a):b.hex()for a,b in actual.items()},stack=bytes(cpu.mem_read(SP-512,528)).hex());return dict(modelPassed=passed,topReturned=returned,memoryPassed=memory,expectedReturn=result,actualReturn=registers[0],traceSha256=hashlib.sha256(json.dumps(trace,sort_keys=True).encode()).hexdigest(),providerCalls=calls)

def prove(row,native,source,compiled):
 address=int(row['address'],0);records=[]
 for seed,v in enumerate(M.cases(address)):
  a=run(address,native,{},v,seed);b=run(address,source,compiled,v,seed)
  if a!=b or not a['modelPassed']:raise ValueError(('Independent crypto caller model differs',row['address'],v,a,b))
  records.append(dict(vector=v,traceSha256=a['traceSha256'],providerCalls=a['providerCalls']))
 return dict(address=row['address'],cases=len(records),actualNativeAndSourceCallerReturns=2*len(records),records=records,independentModel=M.selfcheck(),allGprsCpsrStackWritesMemoryAndProviderCallsCompared=True,importedProviderSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0)
