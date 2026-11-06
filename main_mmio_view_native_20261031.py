import struct
from project import configuration,native_dependencies
native_dependencies(configuration())
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from match_runtime import REGISTERS

ENTRY=0x0200427C
STACK=0x03020000
STOP=0x0F000000


def cases():
    for mode in range(8):
        for enabled in range(2):
            for index in range(16):
                for pattern in [0,1,2,3,0x100,0x4000,0x8000,0xFFFF]:
                    yield mode,(pattern&~0xBC)|(enabled<<7)|(index<<2)


def execute(arm,mode,half,tag,check=True):
    control=((tag*0x9E3779B8)&0xFFFFFFF8)|mode
    permitted=mode in [0,1,2] or mode in [3,4,5] and half&0x80==0
    expected=0x06200000+((half>>2)&15)*16384 if permitted else 0
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address in [0x02004000,0x04001000,STACK,STOP]:uc.mem_map(address,4096)
    uc.mem_write(0x02004000,arm[0x4000:0x5000]);uc.mem_write(STACK,b'\xB7'*4096)
    io=bytearray(((tag+i*29)&255) for i in range(4096));io[:4]=struct.pack('<I',control);io[14:16]=struct.pack('<H',half);uc.mem_write(0x04001000,bytes(io))
    uc.mem_protect(0x02004000,4096,UC_PROT_READ|UC_PROT_EXEC);uc.mem_protect(0x04001000,4096,UC_PROT_READ)
    for i,reg in enumerate(REGISTERS):uc.reg_write(reg,(0xA0110000+i*0x101+tag)&0xFFFFFFFF)
    uc.reg_write(REGISTERS[0],0xFFFFFFFF-tag);uc.reg_write(UC_ARM_REG_CPSR,((tag&15)<<28)|0x1F);uc.reg_write(UC_ARM_REG_SP,STACK+0xF00);uc.reg_write(UC_ARM_REG_LR,STOP|(tag&1))
    saved=[uc.reg_read(reg) for reg in REGISTERS[4:12]];state={'returns':0,'instructions':0};pcs=[];reads=[]
    def code(machine,address,size,user):
        state['instructions']+=1
        if address==STOP:state['returns']+=1;machine.emu_stop();return
        assert ENTRY<=address<ENTRY+68;pcs.append(address)
    def read(machine,access,address,size,value,user):reads.append((address,size))
    def write(machine,access,address,size,value,user):raise AssertionError(('Unexpected write',hex(address),size))
    uc.hook_add(UC_HOOK_CODE,code);uc.hook_add(UC_HOOK_MEM_READ,read);uc.hook_add(UC_HOOK_MEM_WRITE,write)
    uc.emu_start(ENTRY,STOP+4,count=200)
    assert state['returns']==1 and uc.reg_read(UC_ARM_REG_PC)==STOP and uc.reg_read(UC_ARM_REG_SP)==STACK+0xF00
    assert [uc.reg_read(reg) for reg in REGISTERS[4:12]]==saved
    assert reads==[(0x020042C0,4),(0x04001000,4),(0x0400100E,2)]
    assert bytes(uc.mem_read(0x04001000,4096))==bytes(io) and bytes(uc.mem_read(STACK,4096))==b'\xB7'*4096
    actual=uc.reg_read(REGISTERS[0]);passed=actual==expected
    if check:assert passed,(mode,half,hex(actual),hex(expected))
    return {'actualReturn':True,'control':control,'configuration':half,'expected':expected,'result':actual,'modelPassed':passed,'registers':[uc.reg_read(reg) for reg in REGISTERS],'cpsr':uc.reg_read(UC_ARM_REG_CPSR),'state':state,'pcs':pcs,'reads':reads,'writes':[]}
