import hashlib
import struct
from project import configuration,native_dependencies
native_dependencies(configuration())
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from match_runtime import REGISTERS

ENTRY=0x020343FC
GLOBAL=0x020DD5F8
DATA=0x02510000
STACK=0x03020000
STOP=0x0F000000


def cases():
    for count in range(256):
        for alias in range(5):
            for pattern in range(2):yield count,alias,pattern


def execute(arm,case,tag,check=True):
    count,alias,pattern=case;destination=DATA+0x100
    source=[DATA+0x800,destination+2,destination-11,destination-15,GLOBAL-23][alias]
    raw=((tag*0x9E3779B9)^0xA591E700)&0xFFFFFFFF;word=(0xFFFFFFFF if pattern else 0x80000000)^tag
    arenas={DATA:bytearray(((i*29+tag)&255) for i in range(4096)),0x020DD000:bytearray(((i*17+tag)&255) for i in range(4096))}
    def place(address,payload):
        base=address&~4095;offset=address-base;arenas[base][offset:offset+len(payload)]=payload
    place(source+23,bytes([count]));place(GLOBAL,struct.pack('<I',raw))
    initial={base:bytes(value) for base,value in arenas.items()};expected={base:bytearray(value) for base,value in arenas.items()};ordered=[]
    def load(address,size):return bytes(expected[address&~4095][address&4095:(address&4095)+size])
    def store(address,size,value):
        expected[address&~4095][address&4095:(address&4095)+size]=value.to_bytes(size,'little');ordered.append((address,size,value))
    store(destination+12,4,raw);actual_count=load(source+23,1)[0];store(destination+25,1,actual_count);store(destination+8,4,word)
    for index in range(actual_count):store(destination+26+2*index,2,index|0x100)
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address in [0x02034000,0x020DD000,DATA,STACK,STOP]:uc.mem_map(address,4096)
    uc.mem_write(0x02034000,arm[0x34000:0x35000]);uc.mem_protect(0x02034000,4096,UC_PROT_READ|UC_PROT_EXEC)
    for base,value in initial.items():uc.mem_write(base,value)
    uc.mem_write(STACK,b'\xB7'*4096)
    for index,register in enumerate(REGISTERS):uc.reg_write(register,(0xA0110000+index*0x101+tag)&0xFFFFFFFF)
    for register,value in zip(REGISTERS[:3],[destination,word,source]):uc.reg_write(register,value)
    uc.reg_write(UC_ARM_REG_CPSR,((tag&15)<<28)|0x1F);uc.reg_write(UC_ARM_REG_SP,STACK+0xF00);uc.reg_write(UC_ARM_REG_LR,STOP|(tag&1))
    saved=[uc.reg_read(reg) for reg in REGISTERS[4:12]];reads=[];writes=[];pcs=set();state={'returns':0,'instructions':0}
    def code(machine,address,size,user):
        state['instructions']+=1
        if address==STOP:state['returns']+=1;machine.emu_stop();return
        assert ENTRY<=address<ENTRY+72;pcs.add(address)
    def read(machine,access,address,size,value,user):reads.append((address,size))
    def write(machine,access,address,size,value,user):
        assert DATA<=address and address+size<=DATA+4096;writes.append((address,size,value&((1<<(size*8))-1)))
    uc.hook_add(UC_HOOK_CODE,code);uc.hook_add(UC_HOOK_MEM_READ,read);uc.hook_add(UC_HOOK_MEM_WRITE,write);uc.emu_start(ENTRY,STOP+4,count=10000)
    assert state['returns']==1 and uc.reg_read(UC_ARM_REG_PC)==STOP and uc.reg_read(UC_ARM_REG_SP)==STACK+0xF00
    assert [uc.reg_read(reg) for reg in REGISTERS[4:12]]==saved and uc.reg_read(REGISTERS[0])==destination
    memory={base:bytes(uc.mem_read(base,4096)) for base in initial};passed=all(memory[base]==bytes(expected[base]) for base in expected) and writes==ordered
    if check:
        assert passed,(case,actual_count)
        assert reads==[(ENTRY+72,4),(GLOBAL,4),(source+23,1)]+[(destination+25,1)]*(actual_count+1)
    assert bytes(uc.mem_read(STACK,4096))==b'\xB7'*4096
    return {'actualReturn':True,'modelPassed':passed,'input':list(case),'actualCount':actual_count,'state':state,'pcs':sorted(pcs),'registers':[uc.reg_read(reg) for reg in REGISTERS],'cpsr':uc.reg_read(UC_ARM_REG_CPSR),'reads':reads,'writes':writes,'memoryHashes':{hex(base):hashlib.sha256(value).hexdigest() for base,value in memory.items()}}
