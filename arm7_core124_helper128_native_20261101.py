import hashlib
import itertools
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from match_runtime import REGISTERS
MAIN,WRAM,DATA,STACK,IO,STOP,WORD=0x027e0000,0x037f8000,0x023c0000,0x03030000,0x04808000,0x0f000000,0x0380fff4
TOP=0x027e9bd8
FUNCTIONS={TOP:(128,116),0x027f4e1c:(96,92),0x027ea584:(76,72),0x027ead30:(44,44),0x027ead5c:(28,28)}


def cases():
    return [dict(mode=mode,flags=flag,io=port,sourceEnabled=enabled,inputHalfword=value,contextOffset=(0x40,0x800)[i%2])for i,(mode,flag,port,enabled,value)in enumerate(itertools.product((0,1,2,65535),(0,1),(0,2,65535),(0,1),(0,65535,0xe2e2,0x6060,0x6161,0x8000,0x100,1)))]


def run(main,wram,case,index,budget=200000):
    rng=random.Random(0x9bd800+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(0x8000),STACK:rng.randbytes(0x4000),IO:rng.randbytes(0x1000),STOP:bytes(0x1000)}
    for base,raw in regions.items():cpu.mem_map(base,len(raw));cpu.mem_write(base,raw)
    context=DATA+case['contextOffset'];cpu.mem_write(DATA+0x7000,struct.pack('<I',context));phase='prefix';prefix=[];reads=[];writes=[];visited=[];active=[];helpers=[];returned=[False]
    def code(machine,pc,size,user):
        if phase=='prefix':
            if not(0x027e89ec<=pc<0x027e8a10 or 0x037fe014<=pc<0x037fe014+92):raise ValueError('Original prefix escaped constructor/fill')
            return
        if pc==STOP:
            if active:raise ValueError('Top returned with unfinished native helper')
            returned[0]=True;machine.emu_stop();return
        while active and active[-1]['lr']==pc and active[-1]['sp']==machine.reg_read(REGISTERS[-2]):
            item=active.pop();item.update(actualReturn=True,result=machine.reg_read(REGISTERS[0]),abiPreserved=[machine.reg_read(r)for r in REGISTERS[4:12]]==item['saved']);helpers.append(item)
        if size!=4 or machine.reg_read(UC_ARM_REG_CPSR)&32 or not any(start<=pc<start+code for start,(extent,code)in FUNCTIONS.items()):raise ValueError('Helper128 fetched outside qualified original ARM code or into pool')
        visited.append(pc)
        if pc in FUNCTIONS and pc!=TOP:active.append(dict(entry=hex(pc),lr=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),incoming=[machine.reg_read(r)for r in REGISTERS[:4]],saved=[machine.reg_read(r)for r in REGISTERS[4:12]],sourceCredit=0))
    def store(machine,access,address,width,value,user):
        row=[address,width,value&((1<<(8*width))-1)]
        if phase=='prefix':prefix.append(row);return
        if not(STACK<=address and address+width<=STACK+0x4000)and not(address==IO+0x140 and width==2):raise ValueError('Helper128 wrote outside actual private frames/word and output halfword')
        writes.append(row)
    def load(machine,access,address,width,value,user):
        if phase=='prefix':return
        reads.append([address,width])
        if address==WORD and width==4:return
        if any(start+code<=address and address+width<=start+extent and width==4 for start,(extent,code)in FUNCTIONS.items()):return
        if DATA<=address and address+width<=DATA+0x8000 and width in(1,2,4):return
        if STACK<=address and address+width<=STACK+0x4000 and width in(2,4):return
        if address==IO+0xbc and width==2:return
        raise ValueError('Helper128 read outside qualified word/fields/bytes/frames/port/pools')
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,store);cpu.hook_add(UC_HOOK_MEM_READ,load);cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(REGISTERS[0],DATA+0x7000);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(0x27e89ec,0x27e8a10,count=10000)
    nonstack=[x for x in prefix if not STACK<=x[0]<STACK+0x4000]
    if cpu.reg_read(UC_ARM_REG_PC)!=0x27e8a10 or nonstack!=[[WORD,4,context]]+[[context+i,4,0]for i in range(0,0x694,4)]:raise ValueError('Original descriptor write/clear/fill return differs')
    for off,value in[(0x330,case['mode']),(0x3a4,case['flags'])]:cpu.mem_write(context+off,struct.pack('<H',value))
    cpu.mem_write(context+0x318,struct.pack('<I',DATA+0x2000 if case['sourceEnabled']else 0));cpu.mem_write(DATA+0x202e,struct.pack('<H',case['inputHalfword']));cpu.mem_write(IO+0xbc,struct.pack('<H',case['io']));expected={base:bytearray(cpu.mem_read(base,len(raw)))for base,raw in regions.items()};initial=[rng.getrandbits(32)for unused in REGISTERS];initial[-2:]=[STACK+0x3800,STOP|(index&1)];mode=0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,((index%16)<<28)|mode)
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    phase='target';cpu.emu_start(TOP,STOP+4,count=budget)
    if not returned[0]:raise ValueError('Helper128 did not actually return within budget')
    slot=initial[-2]-8;call_frame=slot-16;expected_writes=[[slot,4,initial[3]],[slot+4,4,initial[-1]],[slot,4,0xe2e2]]+[[call_frame+4*i,4,value]for i,value in enumerate([initial[4],initial[5],initial[6],0x027e9bf4])];value=0xe2e2
    if case['sourceEnabled']:
        value=(value&0xff00)|(case['inputHalfword']&255);expected_writes.append([slot,2,value]);value=case['inputHalfword'];expected_writes.append([slot,2,value])
    value=(value+0x202)&0xffffffff;expected_writes.append([slot,4,value]);getter=10 if case['mode']==1 or(case['mode']==0 and case['flags']&1)else 20
    if getter==20:
        value=(value-0x6161)&0xffffffff;expected_writes.append([slot,4,value])
        if case['io']&2:value=(value-0x6060)&0xffffffff;expected_writes.append([slot,4,value])
    expected_writes.append([IO+0x140,2,value&65535])
    for address,width,stored in expected_writes:
        base=STACK if STACK<=address<STACK+0x4000 else IO;expected[base][address-base:address-base+width]=stored.to_bytes(width,'little')
    expected_entries=[0x027f4e1c,0x027ea584]+([0x027ead5c,0x027ead30]*2 if case['sourceEnabled']else[]);flags=8 if getter==10 else 2 if case['io']&2 else 6;checks=dict(result=cpu.reg_read(REGISTERS[0])==IO+0x140,restoredPrivateWordInR3=cpu.reg_read(REGISTERS[3])==value,flags=cpu.reg_read(UC_ARM_REG_CPSR)>>28==flags,abi=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(REGISTERS[-2])==initial[-2]and cpu.reg_read(REGISTERS[-1])==initial[-1]and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode,orderedAllWrites=writes==expected_writes,allMemory=all(bytes(cpu.mem_read(base,len(raw)))==bytes(raw)for base,raw in expected.items()),helperEntries=sorted(int(x['entry'],0)for x in helpers)==sorted(expected_entries),helperAbi=all(x['abiPreserved']for x in helpers),pointerWordPreserved=int.from_bytes(cpu.mem_read(WORD,4),'little')==context)
    if any(x['entry']=='0x27f4e1c'and x['incoming'][:3]!=[0x58,2,slot]for x in helpers)or any(x['entry']=='0x27ea584'and x['result']!=getter for x in helpers):raise ValueError('Actual three-word transfer or zero-input getter ABI differs')
    return dict(actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,rawResult=cpu.reg_read(REGISTERS[0]),privateWord=value,rawRegisters=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedReads=reads,orderedWrites=writes,helpers=helpers,scopedHelperReturns=len(helpers),visited=sorted(set(visited)),instructions=len(visited),producer=dict(actualFillReturn=True,constructorActualReturn=False,descriptorWord0=context,clearBytes=0x694),providerReplacements=[],physicalHardwareOrGameContextProven=False)
