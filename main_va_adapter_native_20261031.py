import hashlib
import struct
from project import configuration,native_dependencies
native_dependencies(configuration())
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from match_runtime import REGISTERS

ENTRY=0x020211C0
LOWER=0x020211E8
DATA=0x02510000
STACK=0x03020000
STOP=0x0F000000


def cases():
    for pointer in [DATA+0x100,0,0xFFFFFFFF]:
        for limit in [-0x80000000,-1,0,1,65535,0x7FFFFFFF]:
            for count in range(9):
                for bias in [0,4]:
                    for mutate in [False,True]:yield pointer,limit,count,bias,mutate


def execute(arm,case,tag,check=True):
    pointer,limit,count,bias,mutate=case;format=DATA+0x500;sp=STACK+0x900+bias;lr=STOP|(tag&1)
    arguments=[(0x80000000+i*0x10001+tag*31)&0xFFFFFFFF for i in range(max(1,count))];first=arguments[0]
    returned=[0,1,0xFFFFFFFF,0x80000000,0xDEADBEEF][tag%5]
    arena=bytes((i*29+tag)&255 for i in range(4096));stack=bytearray(b'\xB7'*4096)
    for index,value in enumerate(arguments[1:]):struct.pack_into('<I',stack,sp-STACK+index*4,value)
    expected=bytearray(stack);writes=[]
    for address,value in [(sp-16,pointer),(sp-12,limit&0xFFFFFFFF),(sp-8,format),(sp-4,first),(sp-24,first),(sp-20,lr)]:
        struct.pack_into('<I',expected,address-STACK,value);writes.append((address,4,value))
    if mutate:struct.pack_into('<I',expected,sp-4-STACK,0x76543210)
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address in [0x02021000,DATA,STACK,STOP]:uc.mem_map(address,4096)
    uc.mem_write(0x02021000,arm[0x21000:0x22000]);uc.mem_protect(0x02021000,4096,UC_PROT_READ|UC_PROT_EXEC)
    uc.mem_write(DATA,arena);uc.mem_protect(DATA,4096,UC_PROT_READ);uc.mem_write(STACK,bytes(stack))
    for index,reg in enumerate(REGISTERS):uc.reg_write(reg,(0xA0110000+index*0x101+tag)&0xFFFFFFFF)
    for reg,value in zip(REGISTERS[:4],[pointer,limit&0xFFFFFFFF,format,first]):uc.reg_write(reg,value)
    uc.reg_write(UC_ARM_REG_CPSR,((tag&15)<<28)|0x1F);uc.reg_write(UC_ARM_REG_SP,sp);uc.reg_write(UC_ARM_REG_LR,lr)
    saved=[uc.reg_read(r) for r in REGISTERS[4:12]];pcs=set();observed=[];reads=[];events=[];state={'actualTopReturns':0,'lowerProviders':0,'instructions':0}
    def code(machine,address,size,user):
        state['instructions']+=1
        if address==STOP:state['actualTopReturns']+=1;machine.emu_stop();return
        if address==LOWER:
            state['lowerProviders']+=1;args=[machine.reg_read(r) for r in REGISTERS[:4]]
            assert STACK<=args[3] and args[3]+count*4<=STACK+4096
            words=list(struct.unpack('<'+'I'*count,bytes(machine.mem_read(args[3],count*4)))) if count else []
            events.append({'arguments':args,'variableWords':words})
            if mutate:machine.mem_write(sp-4,struct.pack('<I',0x76543210))
            target=machine.reg_read(UC_ARM_REG_LR)
            for index in [1,2,3,12]:machine.reg_write(REGISTERS[index],(0xC0710000+tag*17+index)&0xFFFFFFFF)
            machine.reg_write(UC_ARM_REG_CPSR,((tag*3&15)<<28)|0x1F);machine.reg_write(REGISTERS[0],returned);machine.reg_write(UC_ARM_REG_PC,target);return
        assert ENTRY<=address<ENTRY+40;pcs.add(address)
    def read(machine,access,address,size,value,user):
        assert STACK<=address and address+size<=STACK+4096;reads.append((address,size))
    def write(machine,access,address,size,value,user):
        assert STACK<=address and address+size<=STACK+4096;observed.append((address,size,value&((1<<(size*8))-1)))
    uc.hook_add(UC_HOOK_CODE,code);uc.hook_add(UC_HOOK_MEM_READ,read);uc.hook_add(UC_HOOK_MEM_WRITE,write);uc.emu_start(ENTRY,STOP+4,count=100)
    assert state['actualTopReturns']==1 and uc.reg_read(UC_ARM_REG_PC)==STOP and uc.reg_read(UC_ARM_REG_SP)==sp and [uc.reg_read(r) for r in REGISTERS[4:12]]==saved
    stack_result=bytes(uc.mem_read(STACK,4096));passed=state['lowerProviders']==1 and events==[{'arguments':[pointer,limit&0xFFFFFFFF,format,sp-4],'variableWords':arguments[:count]}] and uc.reg_read(REGISTERS[0])==returned and uc.reg_read(REGISTERS[3])==first and stack_result==bytes(expected) and observed==writes and reads==[(sp-8,4),(sp-24,4),(sp-20,4)]
    if check:assert passed,(case,events,observed,reads)
    return {'actualReturn':True,'modelPassed':passed,'state':state,'events':events,'pcs':sorted(pcs),'writes':observed,'reads':reads,'stackSha256':hashlib.sha256(stack_result).hexdigest(),'memorySha256':hashlib.sha256(bytes(uc.mem_read(DATA,4096))).hexdigest(),'registers':[uc.reg_read(r) for r in REGISTERS],'cpsr':uc.reg_read(UC_ARM_REG_CPSR)}
