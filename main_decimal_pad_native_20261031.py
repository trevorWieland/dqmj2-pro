import hashlib
import struct
from project import configuration,native_dependencies
native_dependencies(configuration())
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from match_runtime import REGISTERS
from main_digit_rounding_native_20261031 import model as round_model

ENTRY=0x020236E8
CONVERT=0x02023568
ROUND=0x02022A54
DATA=0x02510000
STACK=0x03020000
STOP=0x0F000000


def cases():
    for first in range(256):yield [4,2,0x7FFF,first,0,False]
    for length in [0,1,2,3,8,32,33,255]:
        for limit in [-32768,-1,0,1,2,7,31,32,33,32767]:
            for exponent in [0,0x7FFF,0x8000,0xFFFF]:
                for pattern in [0,1]:yield [length,limit,exponent,9,pattern,False]
    for length in [0,1,2,32]:
        for limit in [-32768,-1,0,1,2,31,32,32767]:yield [length,limit,0x8000,9,1,True]


def converted(arena,case):
    length,limit,exponent,first,pattern,alias=case
    result=bytearray(arena)
    digits=[9 if pattern==0 else (i*3+2)%10 for i in range(255)];digits[0]=first
    result[0x102:0x104]=struct.pack('<H',exponent);result[0x104]=length;result[0x105:0x204]=bytes(digits)
    return result,digits


def model(arena,case,pointer):
    expected,digits=converted(arena,case)
    return finish_model(expected,case[1],pointer)


def finish_model(arena,limit,pointer):
    expected=bytearray(arena);length=expected[0x104];digits=list(expected[0x105:0x204]);first=digits[0];exponent=struct.unpack_from("<H",expected,0x102)[0]
    if first>9:return bytes(expected),first,0,0
    limit=min(limit,32)
    expected,round_calls,unused=round_model(expected,length,limit,digits,exponent,pointer)
    expected=bytearray(expected)
    while expected[0x104]<limit:
        old=expected[0x104];expected[0x104]=(old+1)&255;expected[0x105+old]=0
    oldexp=struct.unpack_from('<H',expected,0x102)[0]
    struct.pack_into('<H',expected,0x102,(oldexp-(expected[0x104]-1))&0xFFFF)
    for index in range(expected[0x104]):expected[0x105+index]=(expected[0x105+index]+48)&255
    return bytes(expected),expected[0x104],1,round_calls


def execute(arm,case,tag,check=True,real_bits=None):
    length,limit,exponent,first,pattern,alias=case
    pointer=DATA+0x100;settings=pointer if alias else DATA+0x20
    arena=bytearray((i*29+tag)&255 for i in range(4096));struct.pack_into('<h',arena,settings-DATA+2,limit)
    supplied,digits=converted(arena,case);expected,result,round_calls,leaf_calls=model(arena,case,pointer)
    low=(0xC0432000+tag*31)&0xFFFFFFFF;high=(0x3FF10000+tag*67)&0xFFFFFFFF
    if real_bits is not None:low=real_bits&0xFFFFFFFF;high=real_bits>>32
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address in [DATA,STACK,STOP]:uc.mem_map(address,4096)
    code_size=(len(arm)+4095)&~4095
    uc.mem_map(0x02000000,code_size);uc.mem_write(0x02000000,arm);uc.mem_protect(0x02000000,code_size,UC_PROT_READ|UC_PROT_EXEC)
    uc.mem_write(DATA,bytes(arena));uc.mem_write(STACK,b'\xB7'*4096)
    for i,reg in enumerate(REGISTERS):uc.reg_write(reg,(0xA0110000+i*0x101+tag)&0xFFFFFFFF)
    for reg,value in zip(REGISTERS[:4],[settings,low,high,pointer]):uc.reg_write(reg,value)
    uc.reg_write(UC_ARM_REG_CPSR,((tag&15)<<28)|0x1F);uc.reg_write(UC_ARM_REG_SP,STACK+0xF00);uc.reg_write(UC_ARM_REG_LR,STOP|(tag&1))
    saved=[uc.reg_read(r) for r in REGISTERS[4:12]];pcs=set();pending=[];reads=[];writes=[];events=[]
    state={'actualReturns':0,'converterProviders':0,'converterEntries':0,'converterReturns':0,'roundEntries':0,'roundReturns':0,'leafEntries':0,'leafReturns':0,'instructions':0}
    def code(machine,address,size,user):
        nonlocal expected,result,round_calls,leaf_calls
        state['instructions']+=1
        if pending and address==pending[-1][0]:
            unused,kind=pending.pop();state[kind+'Returns']+=1
            if kind=='converter':
                observed=bytes(machine.mem_read(DATA,4096));image=bytearray(arena);image[0x100:0x204]=observed[0x100:0x204]
                assert bytes(image)==observed
                expected,result,round_calls,leaf_calls=finish_model(image,limit,pointer)
                events.append(('actual-converter-output',hashlib.sha256(observed[0x100:0x204]).hexdigest()))
        if address==STOP:state['actualReturns']+=1;machine.emu_stop();return
        if address==CONVERT:
            args=[machine.reg_read(r) for r in REGISTERS[:3]];assert args==[pointer,low,high]
            events.append(('converter',args))
            if real_bits is not None:
                pending.append((machine.reg_read(UC_ARM_REG_LR)&~1,'converter'));state['converterEntries']+=1;return
            state['converterProviders']+=1
            machine.mem_write(pointer+2,bytes(supplied[0x102:0x204]));lr=machine.reg_read(UC_ARM_REG_LR)
            for index in [0,1,2,3,12]:machine.reg_write(REGISTERS[index],(0xC0710000+tag*17+index)&0xFFFFFFFF)
            machine.reg_write(UC_ARM_REG_CPSR,((tag*3&15)<<28)|0x1F);machine.reg_write(UC_ARM_REG_PC,lr);return
        assert real_bits is not None and any(kind=='converter' for unused,kind in pending) and 0x02000000<=address<0x02000000+len(arm) or ENTRY<=address<ENTRY+168 or ROUND<=address<ROUND+64 or 0x02022998<=address<0x02022A04 or 0x02022A04<=address<ROUND,hex(address)
        if ENTRY<=address<ENTRY+168:pcs.add(address)
        if address in [ROUND,0x02022998,0x02022A04] and not any(kind=='converter' for unused,kind in pending):
            kind='round' if address==ROUND else 'leaf';state[kind+'Entries']+=1
            assert [machine.reg_read(r) for r in REGISTERS[:2]]==[pointer,min(limit,32)&0xFFFFFFFF]
            pending.append((machine.reg_read(UC_ARM_REG_LR)&~1,kind))
    def read(machine,access,address,size,value,user):
        if DATA<=address<DATA+4096:
            reads.append((address,size));assert settings+2==address and size==2 or pointer<=address and address+size<=pointer+260
    def write(machine,access,address,size,value,user):
        writes.append((address,size,value&((1<<(size*8))-1)))
        assert STACK<=address and address+size<=STACK+4096 or (pointer if real_bits is not None and any(kind=="converter" for unused,kind in pending) else pointer+2)<=address and address+size<=pointer+260,(hex(address),size,case)
    uc.hook_add(UC_HOOK_CODE,code);uc.hook_add(UC_HOOK_MEM_READ,read);uc.hook_add(UC_HOOK_MEM_WRITE,write);uc.emu_start(ENTRY,STOP+4,count=100000)
    assert state['converterEntries']==state['converterReturns'] and state['converterEntries']==int(real_bits is not None)
    assert state['actualReturns']==1 and uc.reg_read(UC_ARM_REG_PC)==STOP and uc.reg_read(UC_ARM_REG_SP)==STACK+0xF00 and not pending
    assert [uc.reg_read(r) for r in REGISTERS[4:12]]==saved and state['roundEntries']==state['roundReturns'] and state['leafEntries']==state['leafReturns']
    memory=bytes(uc.mem_read(DATA,4096));passed=memory==expected and uc.reg_read(REGISTERS[0])==result and state['roundEntries']==round_calls and state['leafEntries']==leaf_calls
    if check:assert passed,(case,state,uc.reg_read(REGISTERS[0]),result)
    return {'actualReturn':True,'modelPassed':passed,'state':state,'pcs':sorted(pcs),'events':events,'memorySha256':hashlib.sha256(memory).hexdigest(),'stackSha256':hashlib.sha256(bytes(uc.mem_read(STACK,4096))).hexdigest(),'registers':[uc.reg_read(r) for r in REGISTERS],'cpsr':uc.reg_read(UC_ARM_REG_CPSR),'reads':reads,'writes':writes}
