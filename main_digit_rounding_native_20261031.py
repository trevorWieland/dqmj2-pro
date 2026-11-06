import hashlib
import struct
from project import configuration,native_dependencies
native_dependencies(configuration())
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from match_runtime import REGISTERS

ENTRY=0x02022A54
DATA=0x02510000
STACK=0x03020000
STOP=0x0F000000
HELPERS={0x02022998:108,0x02022A04:80}


def cases():
    for value in range(256):
        for parity,tail in [(0,0),(1,0),(0,1)]:
            digits=[7,parity,value,tail,0,0,0,0]
            yield 8,2,digits,0x7FFF
    for length in [0,1,2,8,255]:
        for count in [-0x80000000,-1,0,1,2,7,254,255,256,0x7FFFFFFF]:
            for exponent in [0,0x7FFF,0x8000,0xFFFF]:
                yield length,count,[9]*255,exponent
    for prefix in [[9,9,5,0],[0,9,5,1],[9,8,6,0],[8,9,4,1]]:
        yield 4,2,prefix,0xFFFF


def model(arena,length,count,digits,exponent,pointer):
    expected=bytearray(arena);calls=0;result=pointer
    if 0<count<length:
        calls=1;digit=digits[count];up=digit>5 or digit==5 and (any(digits[count+1:length]) or digits[count-1]&1)
        expected[0x104]=count
        if not up:result=0xFFFFFFFF
        else:
            calls=2;index=count-1
            while True:
                value=expected[0x105+index]
                if value<9:expected[0x105+index]=value+1;result=value+1;break
                if index==0:
                    expected[0x105]=1;expected[0x102:0x104]=struct.pack('<H',(exponent+1)&0xFFFF);break
                expected[0x105+index]=0;index-=1
    return bytes(expected),calls,result


def execute(arm,case,tag,check=True):
    length,count,digits,exponent=case;arena=bytearray(((i*29+tag)&255) for i in range(4096));arena[0x102:0x104]=struct.pack('<H',exponent);arena[0x104]=length;arena[0x105:0x105+len(digits)]=bytes(digits)
    pointer=DATA+0x100;expected,calls,result=model(arena,length,count,digits,exponent,pointer)
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address in [0x02022000,DATA,STACK,STOP]:uc.mem_map(address,4096)
    uc.mem_write(0x02022000,arm[0x22000:0x23000]);uc.mem_write(DATA,bytes(arena));uc.mem_write(STACK,b'\xB7'*4096);uc.mem_protect(0x02022000,4096,UC_PROT_READ|UC_PROT_EXEC)
    for i,reg in enumerate(REGISTERS):uc.reg_write(reg,(0xA0110000+i*0x101+tag)&0xFFFFFFFF)
    uc.reg_write(REGISTERS[0],pointer);uc.reg_write(REGISTERS[1],count&0xFFFFFFFF);uc.reg_write(UC_ARM_REG_CPSR,((tag&15)<<28)|0x1F);uc.reg_write(UC_ARM_REG_SP,STACK+0xF00);uc.reg_write(UC_ARM_REG_LR,STOP|(tag&1))
    saved=[uc.reg_read(reg) for reg in REGISTERS[4:12]];pcs=set();pending=[];reads=[];writes=[];state={'actualReturn':0,'helperEntries':0,'helperReturns':0,'instructions':0}
    def code(machine,address,size,user):
        state['instructions']+=1
        if pending and address==pending[-1]:pending.pop();state['helperReturns']+=1
        if address==STOP:state['actualReturn']+=1;machine.emu_stop();return
        assert ENTRY<=address<ENTRY+64 or any(a<=address<a+n for a,n in HELPERS.items());pcs.add(address)
        if address in HELPERS:
            assert machine.reg_read(REGISTERS[0])==pointer and machine.reg_read(REGISTERS[1])==count
            pending.append(machine.reg_read(UC_ARM_REG_LR)&~1);state['helperEntries']+=1
    def read(machine,access,address,size,value,user):
        if DATA<=address<DATA+4096:reads.append((address,size));assert pointer<=address and address+size<=pointer+260
    def write(machine,access,address,size,value,user):
        writes.append((address,size,value&((1<<(size*8))-1)))
        assert STACK<=address and address+size<=STACK+4096 or pointer+2<=address and address+size<=pointer+260
    uc.hook_add(UC_HOOK_CODE,code);uc.hook_add(UC_HOOK_MEM_READ,read);uc.hook_add(UC_HOOK_MEM_WRITE,write);uc.emu_start(ENTRY,STOP+4,count=10000)
    assert state['actualReturn']==1 and uc.reg_read(UC_ARM_REG_PC)==STOP and uc.reg_read(UC_ARM_REG_SP)==STACK+0xF00 and not pending
    assert [uc.reg_read(reg) for reg in REGISTERS[4:12]]==saved and state['helperEntries']==state['helperReturns']
    memory=bytes(uc.mem_read(DATA,4096));passed=memory==expected and uc.reg_read(REGISTERS[0])==result
    if check:assert passed and state['helperEntries']==calls,(case,uc.reg_read(REGISTERS[0]),result)
    return {'actualReturn':True,'modelPassed':passed,'state':state,'pcs':sorted(pcs),'memorySha256':hashlib.sha256(memory).hexdigest(),'stackSha256':hashlib.sha256(bytes(uc.mem_read(STACK,4096))).hexdigest(),'registers':[uc.reg_read(reg) for reg in REGISTERS],'cpsr':uc.reg_read(UC_ARM_REG_CPSR),'reads':reads,'writes':writes}
