import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

DATA,QUERY,STACK,STOP=0x02400000,0x02410000,0x03030000,0x0F000000
R=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
   UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
COUNTS=[0,1,2,7,15,16,17,31,64,127,128,254,255]


def bit(key,index):
    return(key[index//8]>>(index%8))&1


def patricia(keys):
    nodes=[[127,0,0,0]]
    for index,key in enumerate(keys):
        if not index:
            nodes.append([0,1,1,0]);nodes[0][1]=1;continue
        parent=0;current=nodes[0][1]
        while nodes[parent][0]>nodes[current][0]:
            parent=current;current=nodes[current][1+bit(key,nodes[current][0])]
        previous=keys[nodes[current][3]]
        difference=max(i for i in range(128)if bit(previous,i)!=bit(key,i))
        parent=0;current=nodes[0][1]
        while nodes[parent][0]>nodes[current][0]and nodes[current][0]>difference:
            parent=current;current=nodes[current][1+bit(key,nodes[current][0])]
        fresh=len(nodes);direction=bit(key,difference)
        nodes.append([difference,current if direction else fresh,fresh if direction else current,index])
        nodes[parent][1 if parent==0 else 1+bit(key,nodes[parent][0])]=fresh
    assert len(nodes)==len(keys)+1 and len(nodes)<=256
    return nodes


def execute(image,entry,body,index,bound=32768):
    rng=random.Random(0xD1C7000000+index)
    count=COUNTS[index%len(COUNTS)];variant=(index//len(COUNTS))%12
    unit=[1,2,3,4,7,16,31,32][(index//7)%8]
    base=bytearray(rng.randbytes(16));base[15]&=127
    keys=[bytes([i])+bytes(base[1:])for i in range(count)]
    nodes=patricia(keys)
    empty_root=variant==9
    if empty_root:nodes[0][1]=0
    data=bytearray(rng.randbytes(65536));query_page=bytearray(rng.randbytes(4096))
    entry_offset=0x800;names_offset=(4+count*unit+15)&~15
    total=entry_offset+names_offset+count*16
    struct.pack_into('<BBHHH',data,0,0,count,total,0,entry_offset)
    for i,node in enumerate(nodes):struct.pack_into('<4B',data,8+i*4,*node)
    struct.pack_into('<HH',data,entry_offset,unit,names_offset)
    for i,key in enumerate(keys):data[entry_offset+names_offset+i*16:entry_offset+names_offset+(i+1)*16]=key
    chosen=[0,max(0,count-1),count//2][variant%3]
    query=bytearray(keys[chosen]if count else bytes(base))
    if variant in [3,4,5,6]:query[(variant-3)*4]^=0x80
    if variant==7:query[0]=255
    null_name=variant==8
    query_page[:16]=query
    found=next((i for i,key in enumerate(keys)if key==bytes(query)),None)
    if count>=16 and empty_root:found=None
    if null_name:found=None
    expected=(0 if found is None else DATA+entry_offset+4+unit*found)if entry==0x0202BBB4 else(0xFFFFFFFF if found is None else found)
    alias=variant in [10,11]and count>0
    name_address=DATA+entry_offset+names_offset+chosen*16 if alias else QUERY
    if null_name:name_address=0
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.mem_map(0x02000000,0x100000);machine.mem_write(0x02000000,image);machine.mem_write(entry,body)
    machine.mem_map(DATA,65536);machine.mem_write(DATA,bytes(data));machine.mem_map(QUERY,4096);machine.mem_write(QUERY,bytes(query_page))
    machine.mem_map(STACK,4096);stack=rng.randbytes(4096);machine.mem_write(STACK,stack);machine.mem_map(STOP,4096)
    initial=[rng.getrandbits(32)for register in R]
    for register,value in zip(R,initial):machine.reg_write(register,value)
    machine.reg_write(UC_ARM_REG_R0,DATA);machine.reg_write(UC_ARM_REG_R1,name_address)
    machine.reg_write(UC_ARM_REG_SP,STACK+2048);machine.reg_write(UC_ARM_REG_LR,STOP);machine.reg_write(UC_ARM_REG_CPSR,0x1F|((index%16)<<28))
    before_main=bytes(machine.mem_read(0x02000000,0x100000));own=set();reads=[]
    def code(uc,address,size,unused):
        assert entry<=address<entry+len(body),hex(address)
        own.add(address)
    def read(uc,access,address,size,value,unused):
        if STACK<=address and address+size<=STACK+4096:return
        assert entry<=address and address+size<=entry+len(body) or DATA<=address and address+size<=DATA+65536 or QUERY<=address and address+size<=QUERY+4096,hex(address)
        reads.append([address,size,bytes(uc.mem_read(address,size)).hex()])
    def write(uc,access,address,size,value,unused):
        assert STACK+1888<=address and address+size<=STACK+2048,hex(address)
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP,count=bound)
    assert machine.reg_read(UC_ARM_REG_PC)==STOP,'Bounded prefix is not actual return'
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+2048
    assert all(machine.reg_read(register)==value for register,value in zip(R[4:12],initial[4:12]))
    assert bytes(machine.mem_read(0x02000000,0x100000))==before_main
    assert bytes(machine.mem_read(DATA,65536))==data and bytes(machine.mem_read(QUERY,4096))==query_page
    after_stack=bytes(machine.mem_read(STACK,4096));assert after_stack[:1888]==stack[:1888]and after_stack[2048:]==stack[2048:]
    return dict(index=index,count=count,variant=variant,unit=unit,emptyRoot=empty_root,nullName=null_name,queryAliasesStoredName=alias,
        actualReturn=True,modelPassed=machine.reg_read(UC_ARM_REG_R0)==expected,result=machine.reg_read(UC_ARM_REG_R0),expected=expected,
        registers=[machine.reg_read(register)for register in R],cpsr=machine.reg_read(UC_ARM_REG_CPSR),lr=machine.reg_read(UC_ARM_REG_LR),
        reads=reads,ownedObserved=sorted(own),actualNativeReturns=0,providedCalls=0,
        dataSha256=hashlib.sha256(data).hexdigest(),querySha256=hashlib.sha256(query_page).hexdigest(),stackSha256=hashlib.sha256(after_stack).hexdigest())
