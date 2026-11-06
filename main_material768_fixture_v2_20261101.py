import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

DATA,STACK,STOP=0x02400000,0x03030000,0x0F000000
R=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
 UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
SPECS={0x0202F520:(168,None,None),0x0202F5C8:(120,15,0),0x0202F640:(120,0x30,4),
 0x0202F6B8:(120,0xC0,6),0x0202F730:(120,0x3F000000,24),0x0202F7A8:(120,0x1F0000,16)}


def execute(image,entry,body,index,bound=32768):
    rng=random.Random(0x768F0000+index)
    count=[1,2,7,16,31,64,127,255][index%8]
    if entry==0x0202F520 and index%9==0:count=0
    chosen=[0,max(0,count-1),count//2][(index//8)%3]
    page=bytearray(rng.randbytes(65536));mdl=DATA+0x100;mat=DATA+0x1000;dictionary=mat+4
    struct.pack_into('<I',page,0x108,mat-mdl);page[0x118]=count
    page[0x1005]=count;struct.pack_into('<H',page,0x100A,0x100)
    unit=[4,8,12,16][(index//24)%4];header=dictionary+0x100
    struct.pack_into('<HH',page,header-DATA,unit,4+count*unit)
    offsets=[]
    for i in range(count):
        target=DATA+0x4000+i*64;offsets.append(target)
        struct.pack_into('<I',page,header-DATA+4+i*unit,target-mat)
    assert header+4+count*unit<=DATA+0x4000
    expected=bytearray(page);writes=[];mask,shift=SPECS[entry][1:]
    if entry==0x0202F520:
        enabled=[0,1,2,0x80000000,0xFFFFFFFF][index%5]
        value=[0,1,0x80000000,0xFFFFFFFF,0xA55A1234][(index//5)%5]
        arguments=[mdl,enabled,value]
        for target in offsets:
            old=struct.unpack_from('<I',expected,target-DATA+16)[0]
            new=(old|value)if enabled else(old&~value)
            struct.pack_into('<I',expected,target-DATA+16,new&0xFFFFFFFF);writes.append([target+16,4,new&0xFFFFFFFF])
    else:
        maximum=mask>>shift
        value=[0,1,maximum//2,maximum][(index//24)%4]
        arguments=[mdl,chosen,value]
        target=offsets[chosen]+12;old=struct.unpack_from('<I',expected,target-DATA)[0]
        new=(old&~mask)|(value<<shift)
        struct.pack_into('<I',expected,target-DATA,new);writes.append([target,4,new])
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.mem_map(0x02000000,0x100000);machine.mem_write(0x02000000,image);machine.mem_write(entry,body)
    before_main=bytes(machine.mem_read(0x02000000,0x100000))
    machine.mem_map(DATA,65536);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,4096)
    stack=rng.randbytes(4096);machine.mem_write(STACK,stack);machine.mem_map(STOP,4096)
    initial=[rng.getrandbits(32)for register in R]
    for register,value in zip(R,initial):machine.reg_write(register,value)
    for register,value in zip(R,arguments):machine.reg_write(register,value)
    machine.reg_write(UC_ARM_REG_CPSR,0x1F|((index%16)<<28));machine.reg_write(UC_ARM_REG_SP,STACK+2048);machine.reg_write(UC_ARM_REG_LR,STOP)
    own=set();observed_writes=[];reads=[]
    def code(uc,address,size,unused):
        assert entry<=address<entry+len(body),hex(address)
        own.add(address)
    def read(uc,access,address,size,value,unused):
        if STACK<=address and address+size<=STACK+4096:return
        assert entry<=address and address+size<=entry+len(body)or DATA<=address and address+size<=DATA+65536,hex(address)
        reads.append([address,size,bytes(uc.mem_read(address,size)).hex()])
    def write(uc,access,address,size,value,unused):
        if STACK<=address and address+size<=STACK+4096:assert STACK+1920<=address and address+size<=STACK+2048
        else:
            assert DATA<=address and address+size<=DATA+65536
            observed_writes.append([address,size,value&((1<<(size*8))-1)])
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP,count=bound)
    assert machine.reg_read(UC_ARM_REG_PC)==STOP,'Bounded prefix is not actual return'
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+2048
    assert all(machine.reg_read(register)==value for register,value in zip(R[4:12],initial[4:12]))
    assert bytes(machine.mem_read(0x02000000,0x100000))==before_main
    after=bytes(machine.mem_read(DATA,65536));after_stack=bytes(machine.mem_read(STACK,4096))
    assert after_stack[:1920]==stack[:1920]and after_stack[2048:]==stack[2048:]
    return dict(index=index,count=count,chosen=chosen,arguments=arguments,unit=unit,
        actualReturn=True,modelPassed=after==expected and observed_writes==writes,rawR0=machine.reg_read(UC_ARM_REG_R0),
        registers=[machine.reg_read(register)for register in R],cpsr=machine.reg_read(UC_ARM_REG_CPSR),lr=machine.reg_read(UC_ARM_REG_LR),
        reads=reads,writes=observed_writes,ownedObserved=sorted(own),providedCalls=0,actualHelperReturns=0,
        pageSha256=hashlib.sha256(after).hexdigest(),stackSha256=hashlib.sha256(after_stack).hexdigest())
