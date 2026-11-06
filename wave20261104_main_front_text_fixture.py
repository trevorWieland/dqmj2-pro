import random
import struct
import sys
from project import ROOT
sys.path.insert(0,str(ROOT/'deps/native'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_946
from wave20261104_main_front_compiler import REGISTERS

BASE=0x02000000
TEXT=0x02310000
STACK=0x02380000
STOP=0x023f0000
FREE=0x0202a498
IMAGE=(ROOT/'extract/arm9/arm9.bin').read_bytes()


def cases(address):
    if address==0x0204708c:
        pairs=[struct.unpack_from('<HH',IMAGE,0x020d932c-BASE+i*4) for i in range(23)]
        values=[0,0x60,0x7b,0xffff,0x10000,0xffffffff,*range(0x61,0x7b),*[a for a,b in pairs]]
        values+=random.Random(4708).sample(range(0x100000000),20)
        rows=[]
        for value in values:
            expected=value-32 if 0x61<=value<=0x7a else next((b for a,b in pairs if a==value),value)
            wrong=value-33 if 0x61<=value<=0x7a else value
            rows.append(dict(argument=value,expected=expected,wrong=wrong))
        return rows
    if address==0x020470fc:
        rows=[dict(argument=0,expected=0,words=None,wrong=0)]
        for length in [0,1,2,3,7,15,31,127,255,510,511,512]:
            words=[0x300+(i%0x100) for i in range(514)]
            if length<512:words[length]=0
            rows.append(dict(argument=TEXT,expected=length if length<512 else 0,words=words,wrong=length))
        return rows
    assert address==0x020470e4
    return [dict(argument=p,expected=0xdec0a501 if p else 0,wrongHeap=7) for p in [0,TEXT,TEXT+4,TEXT+0x100]]


def run(address,code,case):
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(BASE,(len(IMAGE)+4095)&~4095);uc.mem_write(BASE,IMAGE)
    uc.mem_write(address,code)
    uc.mem_map(TEXT,0x2000);uc.mem_map(STACK,0x10000);uc.mem_map(STOP,0x1000)
    if case.get('words') is not None:uc.mem_write(TEXT,struct.pack('<514H',*case['words']))
    initial=[(0x01234567+i*0x01010101)&0xffffffff for i in range(15)]
    initial[0]=case['argument'];initial[13]=STACK+0x8000;initial[14]=STOP
    uc.reg_write(UC_ARM_REG_CPSR,0x20000010)
    for register,value in zip(REGISTERS,initial):uc.reg_write(register,value)
    writes=[];calls=[];ended=[]
    def write(machine,kind,where,size,value,unused):
        assert STACK<=where<STACK+0x10000,(hex(where),size)
        writes.append((where,size,value))
    def step(machine,pc,size,unused):
        if pc==STOP:
            ended.append(True);machine.emu_stop();return
        if pc==FREE and address==0x020470e4:
            arguments=[machine.reg_read(r) for r in REGISTERS[:4]]
            calls.append(arguments[:2])
            for index in [0,1,2,3,12]:machine.reg_write(REGISTERS[index],(0xdec0a501+index*0x111111)&0xffffffff)
            machine.reg_write(UC_ARM_REG_CPSR,0xa0000010)
            machine.reg_write(UC_ARM_REG_PC,machine.reg_read(REGISTERS[14]));return
        assert address<=pc<address+len(code),hex(pc)
    uc.hook_add(UC_HOOK_MEM_WRITE,write);uc.hook_add(UC_HOOK_CODE,step)
    uc.emu_start(address,STOP+4,count=50000)
    assert ended and uc.reg_read(REGISTERS[0])==case['expected'],(hex(address),case)
    assert calls==([[6,case['argument']]] if address==0x020470e4 and case['argument'] else [])
    final=[uc.reg_read(r) for r in REGISTERS]
    assert final[4:12]==initial[4:12] and final[13]==initial[13]
    assert bytes(uc.mem_read(TEXT,0x2000))==(struct.pack('<514H',*case['words'])+bytes(0x2000-1028) if case.get('words') is not None else bytes(0x2000))
    return dict(registers=final,cpsr=uc.reg_read(UC_ARM_REG_CPSR),writes=writes,calls=calls,stack=bytes(uc.mem_read(STACK,0x10000)))


def execute(address,native,source,bindings):
    vectors=cases(address)
    rejected=0;equivalent=0
    for case in vectors:
        a=run(address,native,case);b=run(address,source,case);assert a==b
        if address==0x020470e4:
            if case['argument']:
                assert a['calls'][0][0]!=case['wrongHeap'];rejected+=1
            else:equivalent+=1
        elif case['wrong']!=case['expected']:
            assert a['registers'][0]!=case['wrong'];rejected+=1
        else:equivalent+=1
    return dict(passed=True,cases=len(vectors),actualNativeReturns=len(vectors),actualSourceReturns=len(vectors),allGprsCpsrOrderedStackWritesAndInputMemoryCompared=True,calleeSavedAndStackAbiChecked=True,semanticModelControlsRejected=rejected,semanticModelControlEquivalentInputs=equivalent,wrongModels='ASCII minus33 or omitted pair mapping; capped scan reports full unterminated length; wrong release allocator class7',nativeCalleeBodiesExecuted=0,providedFreeContractCases=3 if address==0x020470e4 else 0,retainedOriginalTableDataSourceCredit=0,hardwareOrGameExecutionCredit=0)
