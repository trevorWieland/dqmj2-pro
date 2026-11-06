import hashlib
import struct
from project import configuration,native_dependencies
native_dependencies(configuration())
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from match_runtime import REGISTERS

ENTRY=0x02036994
DATA=0x02500000
STACK=0x03020000
STOP=0x0F000000
SIZE=0xC2000


def cases():
    layouts=[[],[(0,0)],[(1,1)],[(0,65535)],[(65534,65535)],[(255,256)],[(10,9)],[(10,20),(0,65535)],[(0,10),(5,20),(15,30)],[(100,99),(255,256),(65535,65535)]]
    keys=[0,1,2,4,5,9,10,11,15,20,21,30,31,99,100,255,256,257,65534,65535,65536,0x7FFFFFFF,0x80000000,0xFFFFFFFF]
    for layout in layouts:
        for key in keys:yield layout,key


def execute(arm,case,tag,check=True):
    layout,key=case;base=DATA+0x100;holder=DATA+0x20;nodes=[DATA+0x1000+index*0x40000 for index in range(len(layout))]
    arena=bytearray(bytes([tag&255])*SIZE);arena[0x20:0x24]=struct.pack('<I',base);arena[0x10C:0x110]=struct.pack('<I',nodes[0] if nodes else 0)
    for index,(first,last) in enumerate(layout):
        at=nodes[index]-DATA;arena[at:at+8]=struct.pack('<HHI',first,last,nodes[index+1] if index+1<len(nodes) else 0)
    expected=base+4;reads=[(holder,4),(base+12,4)]
    for node,(first,last) in zip(nodes,layout):
        reads.append((node,2))
        if first<=key:
            reads.append((node+2,2))
            if key<=last:expected=node+8+(key-first)*3;break
        reads.append((node+4,4))
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02036000,4096);uc.mem_map(DATA,SIZE);uc.mem_map(STACK,4096);uc.mem_map(STOP,4096)
    uc.mem_write(0x02036000,arm[0x36000:0x37000]);uc.mem_write(DATA,bytes(arena));uc.mem_write(STACK,b'\xB7'*4096)
    uc.mem_protect(0x02036000,4096,UC_PROT_READ|UC_PROT_EXEC);uc.mem_protect(DATA,SIZE,UC_PROT_READ)
    for i,reg in enumerate(REGISTERS):uc.reg_write(reg,(0xA0110000+i*0x101+tag)&0xFFFFFFFF)
    uc.reg_write(REGISTERS[0],holder);uc.reg_write(REGISTERS[1],key);uc.reg_write(UC_ARM_REG_CPSR,((tag&15)<<28)|0x1F);uc.reg_write(UC_ARM_REG_SP,STACK+0xF00);uc.reg_write(UC_ARM_REG_LR,STOP|(tag&1))
    saved=[uc.reg_read(reg) for reg in REGISTERS[4:12]];observed=[];pcs=set();state={'returns':0,'instructions':0}
    def code(machine,address,size,user):
        state['instructions']+=1
        if address==STOP:state['returns']+=1;machine.emu_stop();return
        assert ENTRY<=address<ENTRY+76;pcs.add(address)
    def read(machine,access,address,size,value,user):observed.append((address,size))
    def write(machine,access,address,size,value,user):raise AssertionError(('Unexpected write',address,size))
    uc.hook_add(UC_HOOK_CODE,code);uc.hook_add(UC_HOOK_MEM_READ,read);uc.hook_add(UC_HOOK_MEM_WRITE,write);uc.emu_start(ENTRY,STOP+4,count=1000)
    assert state['returns']==1 and uc.reg_read(UC_ARM_REG_PC)==STOP and uc.reg_read(UC_ARM_REG_SP)==STACK+0xF00
    assert [uc.reg_read(reg) for reg in REGISTERS[4:12]]==saved
    assert bytes(uc.mem_read(DATA,SIZE))==bytes(arena) and bytes(uc.mem_read(STACK,4096))==b'\xB7'*4096
    actual=uc.reg_read(REGISTERS[0]);passed=actual==expected
    if check:assert passed and observed==reads,(case,hex(actual),hex(expected))
    return {'actualReturn':True,'modelPassed':passed,'expected':expected,'result':actual,'state':state,'pcs':sorted(pcs),'reads':observed,'writes':[],'registers':[uc.reg_read(reg) for reg in REGISTERS],'cpsr':uc.reg_read(UC_ARM_REG_CPSR),'memorySha256':hashlib.sha256(bytes(arena)).hexdigest()}
