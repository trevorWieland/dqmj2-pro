import hashlib,struct
from pathlib import Path
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from project import ROOT,sha256,write_json
from wave20261106_mb_local_context_next_register_build import SOURCE,WORK,ADDRESS,SIZE,UPDATE,compile_source,build
from elftools.elf.elffile import ELFFile
HEAP=0x2200000
PARAM=0x2230000
REG=0x2232000
BUF=0x2234000
EXIT=0x23f0000
SP=0x23ee000
CORE=0x20ec36c
STARTED_CORE=0x20ec360
STRIDE=0x5d4
FILE_BASE=0x1788
REG_OFFSET=0x1d40
ACTIVE_OFFSET=0x1d52
COUNT_OFFSET=0x1524
REGISTERS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]

def layout():
 w=WORK/'layout';w.mkdir(parents=True,exist_ok=True)
 expressions=['sizeof(MBGameRegistry)','sizeof(MBGameInfo)','sizeof(MBDownloadFileInfo)','sizeof(MB_BlockInfoTable)','sizeof(MBiCacheList)','sizeof(((MB_CommPWork*)0)->fileinfo[0])','(u32)&((MB_CommPWork*)0)->file_num','(u32)&((MB_CommPWork*)0)->fileinfo[0]','(u32)&((MB_CommPWork*)0)->fileinfo[0].game_reg','(u32)&((MB_CommPWork*)0)->fileinfo[0].active','(u32)&((MB_CommPWork*)0)->fileinfo[0].game_info','(u32)&((MB_CommPWork*)0)->common.user']
 expected=[60,1216,228,20,112,STRIDE,COUNT_OFFSET,FILE_BASE,REG_OFFSET,ACTIVE_OFFSET,FILE_BASE+228,0x1300]
 source=w/'layout.c';source.write_text(f'#include "{(SOURCE/"register.c").as_posix()}"\nconst u32 RegisterLayout[]={{'+','.join(expressions)+'};\n');obj,compiler=compile_source(source,w/'compile')
 with obj.open('rb')as stream:
  e=ELFFile(stream);s=next(s for s in e.get_section_by_name('.symtab').iter_symbols()if s.name=='RegisterLayout');body=e.get_section(s['st_shndx']).data()[s['st_value']:s['st_value']+s['st_size']];actual=list(struct.unpack('<'+'I'*len(expected),body))
 if actual!=expected:raise ValueError(('Measured Register layout mismatch',actual,expected))
 return dict(assertions=[dict(expression=x,actual=a,expected=b)for x,a,b in zip(expressions,actual,expected)],compiler=compiler,object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),diagnosticOnly=True)

def cases():
 result=[]
 for irq in[0,0x80]:
  for started in[0,2,255]:result.append(dict(name=f'not-started-{started}-irq{irq}',started=started,count=0,active=[0]*16,regs=[0]*16,irq=irq))
  for count in[16,255]:result.append(dict(name=f'capacity-{count}-irq{irq}',started=1,count=count,active=[0]*16,regs=[0]*16,irq=irq))
  for duplicate in[0,7,15]:
   regs=[REG+0x100+i*4 for i in range(16)];regs[duplicate]=REG
   result.append(dict(name=f'duplicate-{duplicate}-irq{irq}',started=1,count=15,active=[1]*16,regs=regs,irq=irq))
  result.append(dict(name=f'all-busy-irq{irq}',started=1,count=15,active=[1]*16,regs=[REG+0x100+i*4 for i in range(16)],irq=irq))
  for first in[0,7,15]:result.append(dict(name=f'first-available-{first}-irq{irq}',started=1,count=15,active=[1]*first+[0]+[1]*(15-first),regs=[REG+0x100+i*4 for i in range(16)],irq=irq))
 return result

def expected(case):
 if case['started']!=1 or case['count']>=16:return dict(stop='return',writes=[],result=0)
 for i in range(16):
  if case['regs'][i]==REG:return dict(stop='return',writes=[],result=0)
  if case['active'][i]==0:return dict(stop='provider-boundary',writes=[(HEAP+REG_OFFSET+i*STRIDE,4,REG)],arguments=[HEAP+FILE_BASE+i*STRIDE,BUF])
 return dict(stop='return',writes=[],result=0)

def execute(body,case):
 image=(ROOT/'extract/arm9/arm9.bin').read_bytes();uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(0x2000000,0x200000);uc.mem_map(HEAP,0x40000);uc.mem_map(0x23e0000,0x20000);uc.mem_write(0x2000000,image);uc.mem_write(ADDRESS,body);uc.mem_write(CORE,struct.pack('<I',HEAP));uc.mem_write(STARTED_CORE+8,struct.pack('<I',PARAM));uc.mem_write(PARAM+0x50d,bytes([case['started']]));uc.mem_write(HEAP+COUNT_OFFSET,bytes([case['count']]));uc.mem_write(UPDATE,b'\x91');uc.mem_write(REG,bytes((i*13+7)&255 for i in range(64)));uc.mem_write(BUF,bytes((i*11+3)&255 for i in range(512)))
 for i in range(16):uc.mem_write(HEAP+REG_OFFSET+i*STRIDE,struct.pack('<I',case['regs'][i]));uc.mem_write(HEAP+ACTIVE_OFFSET+i*STRIDE,bytes([case['active'][i]]))
 uc.reg_write(UC_ARM_REG_CPSR,0xa0000013|case['irq'])
 for i,r in enumerate(REGISTERS[:13]):uc.reg_write(r,0x61600000+i*0x1111)
 uc.reg_write(UC_ARM_REG_SP,SP);uc.reg_write(UC_ARM_REG_LR,EXIT);uc.reg_write(UC_ARM_REG_R0,REG);uc.reg_write(UC_ARM_REG_R1,BUF)
 reads=[];writes=[];steps=[];stop=[];helpers=[(0x2007ff4,20),(0x2008008,24),(0x2018990,32)]
 def code(u,address,size,_):
  if address==EXIT:stop.append('return');u.emu_stop();return
  if address==0x2015f00:stop.append('provider-boundary');u.emu_stop();return
  if not(ADDRESS<=address<ADDRESS+SIZE or any(a<=address<a+n for a,n in helpers)):raise ValueError(('Unqualified Register execution target',hex(address)))
  steps.append(address)
 def memory(u,access,address,size,value,_):
  if access==16:reads.append((address,size,bytes(u.mem_read(address,size)).hex()))
  else:writes.append((address,size,value))
 uc.hook_add(UC_HOOK_CODE,code);uc.hook_add(UC_HOOK_MEM_READ|UC_HOOK_MEM_WRITE,memory);uc.emu_start(ADDRESS,0,count=4000)
 if len(stop)!=1:raise ValueError('Register fixture did not reach explicit stop')
 registers=[uc.reg_read(r)for r in REGISTERS];effect=[r for r in writes if not 0x23e0000<=r[0]<0x2400000];model=expected(case)
 if stop[0]!=model['stop']or effect!=model['writes']:raise ValueError(('Independent Register state model failed',case['name'],stop,effect,model))
 if stop[0]=='return'and(registers[0]!=0 or registers[-1]&0x80!=case['irq']):raise ValueError('Register return/interrupt restoration model failed')
 if stop[0]=='provider-boundary'and registers[:2]!=model['arguments']:raise ValueError('Register first-provider argument model failed')
 if bytes(uc.mem_read(UPDATE,1))!=b'\x91':raise ValueError('Register touched update before first provider')
 return dict(stop=stop[0],registers=registers,reads=reads,writes=writes,steps=steps,model=model)

def prove(body=None):
 if body is None:_,_,_,body=build()
 native=(ROOT/'extract/arm9/arm9.bin').read_bytes()[ADDRESS-0x2000000:ADDRESS-0x2000000+SIZE];rows=[]
 for case in cases():
  actual=execute(native,case);fresh=execute(body,case)
  if actual!=fresh:raise ValueError(('Native/source Register execution differs',case['name']))
  rows.append(dict(name=case['name'],stop=actual['stop'],sourceAndNativeGprCpsrStackReadsOrderedWritesEqual=True,model=actual['model'],steps=len(actual['steps']),traceSha256=hashlib.sha256(repr(actual).encode()).hexdigest()))
 return dict(cases=len(rows),runs=2*len(rows),actualReturnsPerNativeOrSource=sum(r['stop']=='return'for r in rows),providerBoundaryStopsPerNativeOrSource=sum(r['stop']=='provider-boundary'for r in rows),rows=rows,unexecutedRegistrationProviderBodyInstructions=0,registrationSuccessBehaviorProven=False,updateIncrementOrWrapExecutionProven=False,boundedScope='Actual early rejection paths and first available record write/MakeDownload arguments only. Original interrupt helpers and IsStarted execute with zero source credit. Stop before MakeDownload; no download/game/task provider body runs.',layout=layout())

if __name__=='__main__':write_json(WORK/'fixtures.json',prove());print('Register fixtures passed')
