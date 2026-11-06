import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY,DATA,STACK,STOP=0x0202C84C,0x02400000,0x03030000,0x0F000000
STATE,CACHE=0x020EE1F4,0x020EE1F8
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
 UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def inputs(index):
    rng=random.Random(0xC84C336+index);page=bytearray(rng.randbytes(65536));cache=bytearray(rng.randbytes(11520))
    result,scale,command,rs=DATA+0x100,DATA+0x800,DATA+0x900+index%4,DATA+0x2000
    node=index%64;alias=(index//64)%4
    parent=[node,node^1,node^32,[0,31,32,63][(index//16)%4]][alias]
    op=((index//256)%4)|((index//8)%64)<<2
    one=index//1024;flag=(rng.getrandbits(32)&~4)|(one*4)
    page[command-DATA:command-DATA+4]=bytes([rng.randrange(256),node,parent,op])
    edges=[0,1,0xFFFFFFFF,0x7FFFFFFF,0x80000000,4096,0xFFFFF000,0x12345678]
    values=[edges[(index+i)%8]if index%2 else rng.getrandbits(32)for i in range(6)]
    struct.pack_into('<6I',page,scale-DATA,*values)
    expected_page=bytearray(page);expected_cache=bytearray(cache)
    initial=struct.unpack_from('<I',page,result-DATA)[0];expected_flag=initial|16
    bitmap=int.from_bytes(page[rs-DATA+196:rs-DATA+204],'little')
    if one:
        expected_flag|=1
        if op&2:bitmap|=1<<node
    else:
        struct.pack_into('<3I',expected_page,result-DATA+4,*values[:3])
        if op&2:
            bitmap&=~(1<<node)
            struct.pack_into('<3I',expected_cache,3596+node*24,*values[3:])
    expected_page[rs-DATA+196:rs-DATA+204]=bitmap.to_bytes(8,'little')
    if op&1:
        expected_flag|=32
        if bitmap&(1<<parent):expected_flag|=8
        else:expected_page[result-DATA+16:result-DATA+28]=expected_cache[3596+parent*24:3608+parent*24]
    struct.pack_into('<I',expected_page,result-DATA,expected_flag)
    pointer=0 if one and index%8==0 else scale
    return page,cache,expected_page,expected_cache,[result,pointer,command,flag],rs,


def execute(image,body,index,bound=4096):
    page,cache,expected_page,expected_cache,args,rs=inputs(index);rng=random.Random(0x336ABCDE+index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000,0x100000);machine.mem_write(0x02000000,image);machine.mem_write(ENTRY,body)
    machine.mem_write(STATE,struct.pack('<I',rs));machine.mem_write(CACHE,bytes(cache))
    before_main=bytes(machine.mem_read(0x02000000,0x100000));expected_main=bytearray(before_main)
    expected_main[CACHE-0x02000000:CACHE-0x02000000+11520]=expected_cache
    machine.mem_map(DATA,65536);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,4096);machine.mem_map(STOP,4096)
    stack=rng.randbytes(4096);machine.mem_write(STACK,stack);initial=[rng.getrandbits(32)for r in REGS]
    for register,value in zip(REGS,initial):machine.reg_write(register,value)
    for register,value in zip(REGS,args):machine.reg_write(register,value)
    machine.reg_write(UC_ARM_REG_CPSR,0x1F|((index%16)<<28));machine.reg_write(UC_ARM_REG_SP,STACK+2048);machine.reg_write(UC_ARM_REG_LR,STOP)
    own=set();reads=[];writes=[]
    def code(uc,address,size,unused):
        assert ENTRY<=address<ENTRY+len(body),hex(address)
        own.add(address)
    def read(uc,access,address,size,value,unused):
        assert 0x02000000<=address and address+size<=0x02100000 or DATA<=address and address+size<=DATA+65536 or STACK<=address and address+size<=STACK+4096
        reads.append([address,size,bytes(uc.mem_read(address,size)).hex()])
    def write(uc,access,address,size,value,unused):
        assert STACK+1536<=address and address+size<=STACK+2048 or DATA<=address and address+size<=DATA+65536 or CACHE<=address and address+size<=CACHE+11520
        writes.append([address,size,value&((1<<(size*8))-1)])
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(ENTRY,STOP,count=bound);assert machine.reg_read(UC_ARM_REG_PC)==STOP,'Prefix is not actual return'
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+2048
    assert all(machine.reg_read(r)==value for r,value in zip(REGS[4:12],initial[4:12]))
    after_page=bytes(machine.mem_read(DATA,65536));after_main=bytes(machine.mem_read(0x02000000,0x100000));after_stack=bytes(machine.mem_read(STACK,4096))
    assert after_stack[:1536]==stack[:1536]and after_stack[2048:]==stack[2048:]
    return dict(index=index,args=args,actualReturn=True,modelPassed=after_page==expected_page and after_main==expected_main,
     registers=[machine.reg_read(r)for r in REGS],cpsr=machine.reg_read(UC_ARM_REG_CPSR),lr=machine.reg_read(UC_ARM_REG_LR),
     ownedObserved=sorted(own),reads=reads,writes=writes,providedCalls=0,actualNativeHelperReturns=0,
     dataSha256=hashlib.sha256(after_page).hexdigest(),mainSha256=hashlib.sha256(after_main).hexdigest(),stackSha256=hashlib.sha256(after_stack).hexdigest())
