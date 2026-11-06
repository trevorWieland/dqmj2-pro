import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import *

APPLY,RESET,CALLER=0x02036F68,0x0203716C,0x020489C4
CACHE,DMA,TABLE,DATA,STACK,STOP,OAM=0x020F0F08,0x020DCB44,0x020DD810,0x02400000,0x03030000,0x0F000000,0x07000000
R=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
   UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
NATIVE={0x020072D0:28,0x02007308:36,0x020049FC:84,0x02004A50:88,0x02036B94:20,0x02036BA8:16,
        0x02008BF8:28,0x02008C14:20,0x02008C28:24}


def execute(image,bodies,index,connected=False,bound=32768):
    rng=random.Random(0xF685160000+index+int(connected)*0x10000)
    bank=(index//2)%3;fast=[0,1,2,0x80000000,0xFFFFFFFF][index%5]
    if bank==2:fast=1
    first,last=[(0,0),(0,3),(4,7),(16,31),(120,127),(0,127),(8,7),(127,127)][(index//6)%8]
    afirst,alast,acurrent=[(0,0,0),(0,31,0),(4,7,8),(2,1,0),
        (0,0,2),(31,31,31),(4,15,4),(31,31,32)][(index//3)%8]
    current=min(last+1,max(0,first))
    slot=index%2;manager=0x020FBAE8+slot*0x3744+0x520 if connected else DATA+0x100
    entry=CALLER if connected else APPLY
    page=rng.randbytes(4096);record=bytearray(rng.randbytes(28))
    struct.pack_into('<IHHHHHH',record,0,bank,first,last,current,afirst,alast,acurrent)
    struct.pack_into('<I',record,20,fast)
    cache=bytearray(rng.randbytes(0xFC0));oam=bytearray(rng.randbytes(4096))
    expected_cache=bytearray(cache);expected_oam=bytearray(oam);expected_record=bytearray(record)
    expected_calls=[];expected_writes=[]
    def transfer(address,source,offset,length):
        expected_calls.append([address,[source,offset,length]])
        target=bank*0x400+offset
        width=4 if fast else 2
        for step in range(0,length,width):
            value=int.from_bytes(cache[source-CACHE+step:source-CACHE+step+width],'little')
            expected_writes.append([OAM+target+step,width,value])
            expected_oam[target+step:target+step+width]=value.to_bytes(width,'little')
    count=(last-first+1)&0xFFFF
    if fast:
        expected_calls.append([0x02007308,[CACHE+bank*0x540+0x100+first*8,count*8]])
        if bank<2:transfer([0x020049FC,0x02004A50][bank],CACHE+bank*0x540+0x100+first*8,first*8,count*8)
    else:
        for i in range(count):transfer([0x02036BA8,0x02036B94][bank],CACHE+bank*0x540+0x100+(first+i)*8,(first+i)*8,6)
        if acurrent<=alast+1 and afirst<=alast:
            for i in range(afirst,alast+1):
                for field in [6,14,22,30]:transfer([0x02036BA8,0x02036B94][bank],CACHE+bank*0x540+0x100+i*32+field,i*32+field,2)
    if connected:
        length=count*8 if current<=last+1 and first<=last else 0
        target=CACHE+bank*0x540+0x100+first*8
        for step in range(0,length,4 if fast else 8):
            width=4 if fast else 2
            expected_writes.append([target+step,width,192]);expected_cache[target-CACHE+step:target-CACHE+step+width]=(192).to_bytes(width,'little')
        expected_writes.extend([[manager+8,2,first],[manager+14,2,afirst]])
        struct.pack_into('<H',expected_record,8,first);struct.pack_into('<H',expected_record,14,afirst)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.mem_map(0x02000000,0x100000);machine.mem_write(0x02000000,image)
    for address,body in bodies.items():machine.mem_write(address,body)
    machine.mem_write(CACHE,bytes(cache));machine.mem_write(DMA,struct.pack('<I',0xFFFFFFFF))
    assert struct.unpack('<5I',machine.mem_read(TABLE,20))==(0x02036BA8,0x02036B94,0,0,0)
    machine.mem_map(DATA,4096);machine.mem_write(DATA,page);machine.mem_write(manager,bytes(record))
    machine.mem_map(OAM,4096);machine.mem_write(OAM,bytes(oam))
    before_main=bytes(machine.mem_read(0x02000000,0x100000));before_page=bytes(machine.mem_read(DATA,4096))
    machine.mem_map(STACK,4096);stack=rng.randbytes(4096);machine.mem_write(STACK,stack);machine.mem_map(STOP,4096)
    initial=[rng.getrandbits(32)for register in R]
    for register,value in zip(R,initial):machine.reg_write(register,value)
    machine.reg_write(UC_ARM_REG_R0,slot if connected else manager)
    machine.reg_write(UC_ARM_REG_CPSR,0x1F|((index%16)<<28));machine.reg_write(UC_ARM_REG_SP,STACK+2048);machine.reg_write(UC_ARM_REG_LR,STOP)
    own=set();helpers=set();pending=[];returned=[];calls=[];writes=[];reads=[]
    watched=set(NATIVE)|({APPLY,RESET}if connected else set())
    def code(uc,address,size,unused):
        while pending and address==pending[-1][0]:returned.append(pending.pop()[1])
        if address in watched:pending.append((uc.reg_read(UC_ARM_REG_LR),address))
        if any(base<=address<base+len(body)for base,body in bodies.items()):own.add(address)
        else:
            assert any(base<=address<base+length for base,length in NATIVE.items()),hex(address)
            helpers.add(address)
        if address in [0x02007308,0x020049FC,0x02004A50,0x02036BA8,0x02036B94]and not(connected and pending and any(item[1]==RESET for item in pending)):
            words=2 if address==0x02007308 else 3
            calls.append([address,[uc.reg_read(register)for register in R[:words]]])
    def write(uc,access,address,size,value,unused):
        if STACK<=address and address+size<=STACK+4096:assert STACK+1888<=address and address+size<=STACK+2048
        else:
            assert OAM<=address and address+size<=OAM+4096 or CACHE<=address and address+size<=CACHE+0xFC0 or manager<=address and address+size<=manager+28,hex(address)
            writes.append([address,size,value&((1<<(size*8))-1)])
    def read(uc,access,address,size,value,unused):
        if STACK<=address and address+size<=STACK+4096:return
        assert 0x02000000<=address and address+size<=0x02100000 or DATA<=address and address+size<=DATA+4096 or OAM<=address and address+size<=OAM+4096
        reads.append([address,size,bytes(uc.mem_read(address,size)).hex()])
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_WRITE,write);machine.hook_add(UC_HOOK_MEM_READ,read)
    machine.emu_start(entry,STOP,count=bound)
    assert machine.reg_read(UC_ARM_REG_PC)==STOP,'Bounded prefix does not return'
    assert not pending and machine.reg_read(UC_ARM_REG_SP)==STACK+2048
    assert all(machine.reg_read(register)==value for register,value in zip(R[4:12],initial[4:12]))
    after_stack=bytes(machine.mem_read(STACK,4096));assert after_stack[:1888]==stack[:1888]and after_stack[2048:]==stack[2048:]
    after_record=bytes(machine.mem_read(manager,28));after_cache=bytes(machine.mem_read(CACHE,0xFC0));after_oam=bytes(machine.mem_read(OAM,4096))
    after_main=bytearray(machine.mem_read(0x02000000,0x100000));expected_main=bytearray(before_main)
    expected_main[CACHE-0x02000000:CACHE-0x02000000+0xFC0]=expected_cache
    expected_page=bytearray(before_page)
    if connected:expected_main[manager-0x02000000:manager-0x02000000+28]=expected_record
    else:expected_page[0x100:0x11C]=expected_record
    passed=after_main==expected_main and bytes(machine.mem_read(DATA,4096))==expected_page
    passed=passed and after_record==expected_record and after_cache==expected_cache and after_oam==expected_oam
    passed=passed and writes==expected_writes and calls==expected_calls
    if connected:passed=passed and machine.reg_read(UC_ARM_REG_R0)==afirst
    return dict(index=index,connected=connected,actualReturn=True,modelPassed=passed,bank=bank,fast=fast,
        first=first,last=last,affine=[afirst,alast,acurrent],rawR0=machine.reg_read(UC_ARM_REG_R0),
        registers=[machine.reg_read(register)for register in R],cpsr=machine.reg_read(UC_ARM_REG_CPSR),lr=machine.reg_read(UC_ARM_REG_LR),
        actualNestedReturns=len(returned),providedCalls=0,ownedObserved=sorted(own),helperObserved=sorted(helpers),
        calls=calls,writes=writes,reads=reads,mainSha256=hashlib.sha256(after_main).hexdigest(),
        pageSha256=hashlib.sha256(machine.mem_read(DATA,4096)).hexdigest(),oamSha256=hashlib.sha256(after_oam).hexdigest(),
        stackSha256=hashlib.sha256(after_stack).hexdigest(),
        firstWriteMismatch=next(([a,b]for a,b in zip(writes,expected_writes)if a!=b),None))
