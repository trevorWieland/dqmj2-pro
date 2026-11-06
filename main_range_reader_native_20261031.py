import hashlib
import struct
from project import configuration,native_dependencies
native_dependencies(configuration())
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from match_runtime import REGISTERS

ENTRY=0x020369E0
DATA=0x02510000
STACK=0x03020000
STOP=0x0F000000
CALL_A=0x02600000
CALL_B=CALL_A+0x100
HELPERS={0x02036830:196,0x0203694C:68,0x02036994:76}


def cases():
    for seed in range(256):yield [1,0],1,seed,False,True,seed&1
    sequences=[[0],[10],[1,2,0],[1,10,2,0],[0xFFFFFFFF,65535,200,201,0],[2,1,65535,10,0]]
    for keys in sequences:
        for spacing in [0,1,0x7FFFFFFF,0x80000000,0xFFFFFFFF]:
            for seed in [0,127,128]:
                for mutate in [False,True]:
                    for output in [False,True]:
                        for thumb in [0,1]:yield keys,spacing,seed,mutate,output,thumb


def make_arena(tag,seed,thumb):
    arena=bytearray((i*29+tag)&255 for i in range(0x4000))
    reader=DATA+0x20;first=DATA+0x100;second=DATA+0x200
    struct.pack_into('<II',arena,0x20,first,CALL_A|thumb)
    for at,fallback,metric,node,width in [(0x100,3,0x80,DATA+0x400,DATA+0x1000),(0x200,65535,0x7F,DATA+0x800,DATA+0x1800)]:
        struct.pack_into('<HH',arena,at,0xA5A5,fallback);arena[at+6]=metric;struct.pack_into('<II',arena,at+12,width,node)
    struct.pack_into('<HHHHIH',arena,0x400,0,65535,0,0xA5A5,0,10)
    pairs=[(1,100),(2,101),(200,110),(65535,65535)]
    struct.pack_into('<HHHHI',arena,0x800,0,65535,2,0xA5A5,0);struct.pack_into('<H',arena,0x80C,len(pairs))
    for i,(key,value) in enumerate(pairs):struct.pack_into('<HH',arena,0x80E+4*i,key,value)
    struct.pack_into('<HHI',arena,0x1000,0,31,0);struct.pack_into('<HHI',arena,0x1800,100,110,0)
    for key in range(32):arena[0x1008+key*3+2]=(key*13+seed)&255
    for key in range(100,111):arena[0x1808+(key-100)*3+2]=((key-100)*17+(255-seed))&255
    return arena


def metric(key,base,seed):
    if base==0:
        mapped=(key+10)&65535 if key<=65535 else 65535
        if mapped==65535:mapped=3
        raw=(mapped*13+seed)&255 if mapped<=31 else 0x80
    else:
        mapped={1:100,2:101,200:110,65535:65535}.get(key,65535)
        if mapped==65535:mapped=65535
        raw=((mapped-100)*17+(255-seed))&255 if 100<=mapped<=110 else 0x7F
    return raw if raw<128 else raw-256


def model(case,tag,arena):
    keys,spacing,seed,mutate,output,thumb=case;expected=bytearray(arena);cursor=(0xFFFFFFF0+tag*0x123)&0xFFFFFFFF;total=0;calls=[]
    for index,key in enumerate(keys):
        calls.append(cursor);cursor=(cursor+0x10001+index*7)&0xFFFFFFFF
        base=index%2 if mutate else 0
        if mutate:struct.pack_into('<II',expected,0x20,DATA+0x100+base*0x100,CALL_B|(1-thumb))
        if key in [0,10]:break
        total=(total+spacing+metric(key,base,seed))&0xFFFFFFFF
    else:raise ValueError('Fixture lacks a terminating key')
    if output:struct.pack_into('<I',expected,0x40,cursor if key==10 else 0)
    if 0<total<0x80000000:total=(total-spacing)&0xFFFFFFFF
    return bytes(expected),total,calls


def execute(arm,case,tag,check=True):
    keys,spacing,seed,mutate,output,thumb=case;arena=make_arena(tag,seed,thumb);expected,result,expected_calls=model(case,tag,arena)
    reader=DATA+0x20;out=DATA+0x40 if output else 0;cursor=(0xFFFFFFF0+tag*0x123)&0xFFFFFFFF;sp=STACK+0xF00;local=sp-40
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address in [0x02036000,DATA,DATA+0x1000,DATA+0x2000,DATA+0x3000,STACK,STOP,CALL_A]:uc.mem_map(address,4096)
    uc.mem_write(0x02036000,arm[0x36000:0x37000]);uc.mem_protect(0x02036000,4096,UC_PROT_READ|UC_PROT_EXEC);uc.mem_write(DATA,bytes(arena));uc.mem_write(STACK,b'\xB7'*4096)
    for i,reg in enumerate(REGISTERS):uc.reg_write(reg,(0xA0110000+i*0x101+tag)&0xFFFFFFFF)
    for reg,value in zip(REGISTERS[:4],[reader,spacing,cursor,out]):uc.reg_write(reg,value)
    uc.reg_write(UC_ARM_REG_CPSR,((tag&15)<<28)|0x1F);uc.reg_write(UC_ARM_REG_SP,sp);uc.reg_write(UC_ARM_REG_LR,STOP|(tag&1))
    saved=[uc.reg_read(r) for r in REGISTERS[4:12]];pcs=set();pending=[];reads=[];writes=[];calls=[];state={'actualTopReturns':0,'originalHelperEntries':0,'originalHelperReturns':0,'callbackProviders':0,'instructions':0};running=cursor
    def code(machine,address,size,user):
        nonlocal running
        state['instructions']+=1
        if pending and address==pending[-1]:pending.pop();state['originalHelperReturns']+=1
        if address==STOP:state['actualTopReturns']+=1;machine.emu_stop();return
        if address in [CALL_A,CALL_B]:
            index=len(calls);assert index<len(keys)
            actual_cursor=struct.unpack('<I',bytes(machine.mem_read(local,4)))[0]
            calls.append({'address':address,'mode':bool(machine.reg_read(UC_ARM_REG_CPSR)&32),'pointer':machine.reg_read(REGISTERS[0]),'cursor':actual_cursor})
            running=(running+0x10001+index*7)&0xFFFFFFFF;machine.mem_write(local,struct.pack('<I',running))
            if mutate:machine.mem_write(reader,struct.pack('<II',DATA+0x100+(index%2)*0x100,CALL_B|(1-thumb)))
            lr=machine.reg_read(UC_ARM_REG_LR)
            for register in [1,2,3,12]:machine.reg_write(REGISTERS[register],(0xC0710000+tag*17+register)&0xFFFFFFFF)
            machine.reg_write(UC_ARM_REG_CPSR,((tag*3&15)<<28)|0x1F);machine.reg_write(REGISTERS[0],keys[index]);machine.reg_write(UC_ARM_REG_PC,lr);state['callbackProviders']+=1;return
        assert not machine.reg_read(UC_ARM_REG_CPSR)&32 and size==4
        assert ENTRY<=address<ENTRY+168 or any(a<=address<a+n for a,n in HELPERS.items()),hex(address)
        if ENTRY<=address<ENTRY+168:pcs.add(address)
        if address in HELPERS:pending.append(machine.reg_read(UC_ARM_REG_LR)&~1);state['originalHelperEntries']+=1
    def read(machine,access,address,size,value,user):
        if DATA<=address<DATA+0x4000:reads.append((address,size))
    def write(machine,access,address,size,value,user):
        assert STACK<=address and address+size<=STACK+4096 or output and address==out and size==4
        writes.append((address,size,value&((1<<(size*8))-1)))
    uc.hook_add(UC_HOOK_CODE,code);uc.hook_add(UC_HOOK_MEM_READ,read);uc.hook_add(UC_HOOK_MEM_WRITE,write);uc.emu_start(ENTRY,STOP+4,count=2000)
    assert state['actualTopReturns']==1 and uc.reg_read(UC_ARM_REG_PC)==STOP and uc.reg_read(UC_ARM_REG_SP)==sp and not pending
    assert [uc.reg_read(r) for r in REGISTERS[4:12]]==saved and state['originalHelperEntries']==state['originalHelperReturns']
    memory=bytes(uc.mem_read(DATA,0x4000));expected_events=[{'address':CALL_A,'mode':bool(thumb),'pointer':local,'cursor':x} for x in expected_calls]
    passed=memory==expected and uc.reg_read(REGISTERS[0])==result and calls==expected_events
    if check:assert passed,(case,calls,expected_events,hex(uc.reg_read(REGISTERS[0])),hex(result))
    return {'actualReturn':True,'modelPassed':passed,'state':state,'events':calls,'pcs':sorted(pcs),'reads':reads,'writes':writes,'memorySha256':hashlib.sha256(memory).hexdigest(),'stackSha256':hashlib.sha256(bytes(uc.mem_read(STACK,4096))).hexdigest(),'registers':[uc.reg_read(r) for r in REGISTERS],'cpsr':uc.reg_read(UC_ARM_REG_CPSR)}
