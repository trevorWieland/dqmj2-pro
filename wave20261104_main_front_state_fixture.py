import itertools
import struct
import sys
from project import ROOT
sys.path.insert(0,str(ROOT/'deps/native'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_946
from wave20261104_main_front_compiler import REGISTERS

BASE=0x02000000
RAM=0x02310000
STACK=0x02380000
STOP=0x023f0000
QUERY=0x02042d58
PAYLOAD=0x0205e7a8
IMAGE=(ROOT/'extract/arm9/arm9.bin').read_bytes()
PAIRS=[(0x19a,0xf6),(0x267,0x148),(0x668,0x19a),(0x802,0x1ec),(0xcd0,0x267),(0x1004,0x2e2),(0x1806,0x4ce),(0x4812,0x668),(0x5348,0x802)]


def cases(address):
    if address==0x02042e30:
        return [dict(selector=s,alias=a,expected=PAIRS[s] if s<9 else (0x19a,0x19a)) for s,a in itertools.product([*range(9),9,0xffffffff,0x80000000],[False,True])]
    assert address==0x02042aac
    sequences=[[],[(1,0xffff)],[(2,0)],[(2,0x8000)],[(2,0x7fff),(2,0xffff)],[(0,1),(2,0x1234),(3,0)]]
    return [dict(entries=entries,flag=flag,frame=frame,key=0x87654321) for entries,flag,frame in itertools.product(sequences,[0,1,255],[0x1000,0xfffff000,0x7fffffff])]


def run(address,code,case):
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(BASE,(len(IMAGE)+4095)&~4095);uc.mem_write(BASE,IMAGE);uc.mem_write(address,code)
    uc.mem_map(RAM,0x2000);uc.mem_map(STACK,0x10000);uc.mem_map(STOP,0x1000)
    memory=bytearray((i*29+7)&255 for i in range(0x2000))
    initial=[(0x01234567+i*0x01010101)&0xffffffff for i in range(15)]
    initial[13]=STACK+0x8000;initial[14]=STOP
    if address==0x02042e30:
        first=RAM+0x100;second=first if case['alias'] else RAM+0x104
        initial[:3]=[case['selector'],first,second]
    else:
        initial[0]=RAM
        struct.pack_into('<I',memory,0x60,RAM+0x600)
        struct.pack_into('<I',memory,0x164,case['key'])
        struct.pack_into('<I',memory,0x600,case['frame'])
        memory[0x1df]=case['flag']
        for i,(kind,payload) in enumerate(case['entries']):struct.pack_into('<HHH',memory,0x800+i*8,0x6666,kind,payload)
    uc.mem_write(RAM,bytes(memory))
    expected=bytearray(memory);expected_calls=[]
    if address==0x02042e30:
        a,b=case['expected'];struct.pack_into('<I',expected,0x100,a);struct.pack_into('<I',expected,0x100 if case['alias'] else 0x104,b)
        returned=b
    else:
        returned=4 if any(kind==2 for kind,p in case['entries']) else 0
        expected[0x1dc]=255
        for kind,payload in case['entries']:
            if kind==2 and case['flag']:expected[0x1dc]=0x80|(payload&0x7f)
    uc.reg_write(UC_ARM_REG_CPSR,0x60000010)
    for register,value in zip(REGISTERS,initial):uc.reg_write(register,value)
    writes=[];calls=[];ended=[];query_index=0
    def store(machine,kind,where,size,value,unused):
        assert STACK<=where<STACK+0x10000 or RAM<=where<RAM+0x2000
        writes.append(('caller',where,size,value))
    def step(machine,pc,size,unused):
        nonlocal query_index
        if pc==STOP:ended.append(True);machine.emu_stop();return
        if pc in [QUERY,PAYLOAD] and address==0x02042aac:
            values=[machine.reg_read(r) for r in REGISTERS[:4]]
            if pc==QUERY:
                frame=case['frame'] if case['frame']<0x80000000 else case['frame']-0x100000000
                assert values[:2]==[case['key'],(frame>>12)&0xffffffff]
                cursor=values[2];assert STACK<=cursor<STACK+0x10000
                current=struct.unpack('<i',machine.mem_read(cursor,4))[0]
                assert current==query_index
                calls.append(('query',values[0],values[1],current))
                if query_index<len(case['entries']):
                    result=RAM+0x800+query_index*8
                    next_index=query_index+1 if query_index+1<len(case['entries']) else -1
                    machine.mem_write(cursor,struct.pack('<i',next_index));writes.append(('provided',cursor,4,next_index&0xffffffff))
                else:result=0
                query_index+=1
            else:
                assert values[0]==0xffffffff
                kind,payload=case['entries'][query_index-1]
                assert kind==2 and case['flag'] and values[1]==payload
                calls.append(('payload',values[0],values[1]))
                result=0xffffff80|(payload&0x7f)
            for i in [0,1,2,3,12]:machine.reg_write(REGISTERS[i],(0xabcd0000+i*0x1111)&0xffffffff)
            machine.reg_write(REGISTERS[0],result)
            machine.reg_write(UC_ARM_REG_CPSR,0xa0000010)
            machine.reg_write(UC_ARM_REG_PC,machine.reg_read(REGISTERS[14]));return
        assert address<=pc<address+len(code),hex(pc)
    uc.hook_add(UC_HOOK_MEM_WRITE,store);uc.hook_add(UC_HOOK_CODE,step)
    uc.emu_start(address,STOP+4,count=50000)
    assert ended and uc.reg_read(REGISTERS[0])==returned
    final=[uc.reg_read(r) for r in REGISTERS]
    assert final[4:12]==initial[4:12] and final[13]==initial[13]
    assert bytes(uc.mem_read(RAM,0x2000))==bytes(expected)
    if address==0x02042e30:
        expected_writes=[('caller',first,4,case['expected'][0]),('caller',second,4,case['expected'][1])]
        assert writes==expected_writes
    else:
        expected_payloads=[('payload',0xffffffff,p) for kind,p in case['entries'] if kind==2 and case['flag']]
        assert [c for c in calls if c[0]=='payload']==expected_payloads
        assert len([c for c in calls if c[0]=='query'])==max(1,len(case['entries']))
    return dict(registers=final,cpsr=uc.reg_read(UC_ARM_REG_CPSR),writes=writes,calls=calls,ram=bytes(uc.mem_read(RAM,0x2000)),stack=bytes(uc.mem_read(STACK,0x10000)))


def execute(address,native,source,bindings):
    vectors=cases(address);rejected=0;equivalent=0
    for case in vectors:
        a=run(address,native,case);b=run(address,source,case);assert a==b
        if address==0x02042e30:
            if case['expected'][0]!=case['expected'][1]:
                assert a['registers'][0]!=case['expected'][0];rejected+=1
            else:equivalent+=1
        else:
            wrong=[('payload',0xffffffff,p&255) for kind,p in case['entries'] if kind==2 and case['flag']]
            actual=[c for c in a['calls'] if c[0]=='payload']
            if wrong!=actual:rejected+=1
            else:equivalent+=1
    return dict(passed=True,cases=len(vectors),actualNativeReturns=len(vectors),actualSourceReturns=len(vectors),allGprsCpsrOrderedWritesAndRamCompared=True,calleeSavedAndStackAbiChecked=True,semanticModelControlsRejected=rejected,semanticModelEquivalentInputs=equivalent,wrongModels='Swap selector output words or narrow the payload boundary from16 to8bits',nativeCalleeBodiesExecuted=0,providedQueryAndPayloadContracts=address==0x02042aac,hardwareOrGameExecutionCredit=0)
