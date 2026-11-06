import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

CACHE, GUID, DATA, STACK, STOP=0x020F0F08,0x020F0F04,0x02400000,0x03030000,0x0F000000
REGISTERS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,
    UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,
    UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def execute(image,entry,body,index,bound=16384):
    rng=random.Random(0xC781000000+entry+index)
    bank=index%3;variant=(index//3)%12
    manager=DATA+0x100;source=DATA+0x400
    page=bytearray(rng.randbytes(4096));cache=bytearray(rng.randbytes(0xFC0))
    guid=[0,1,0x7FFF,0x8000,0xFFFE,0xFFFF][(index//9)%6]
    expected_page=bytearray(page);expected_cache=bytearray(cache)
    expected_writes=[];expected_calls=[];expected_guid=guid
    def read_half(address):
        array,offset=(expected_cache,address-CACHE)if CACHE<=address<CACHE+0xFC0 else(expected_page,address-DATA)
        return struct.unpack_from('<H',array,offset)[0]
    def store(address,size,value):
        nonlocal expected_guid
        value&=(1<<(size*8))-1;expected_writes.append([address,size,value])
        if address==GUID:expected_guid=value;return
        array,offset=(expected_cache,address-CACHE)if CACHE<=address<CACHE+0xFC0 else(expected_page,address-DATA)
        array[offset:offset+size]=value.to_bytes(size,'little')
    if entry==0x02036C78:
        first,count=[(0,4),(4,4),(0,128),(124,4),(16,32),(32,64)][variant%6]
        last=first+count-1;afirst=first//4;alast=afirst+count//4-1
        for i in range(128):struct.pack_into('<H',cache,bank*0x540+i*2,0xFFFF)
        for i in range(32):struct.pack_into('<H',cache,bank*0x540+0x500+i*2,0xFFFF)
        failure=(index//36)%3
        if failure==1:struct.pack_into('<H',cache,bank*0x540+first*2,guid^0x1357)
        if failure==2:struct.pack_into('<H',cache,bank*0x540+0x500+afirst*2,guid^0x2468)
        expected_cache=bytearray(cache)
        arguments=[manager,first,count,bank]
        result=0
        if failure!=1:
            store(GUID,2,guid+1);store(manager+16,2,guid)
            for offset,value in [(4,first),(6,last),(8,first)]:store(manager+offset,2,value)
            target=CACHE+bank*0x540+first*2
            expected_calls.append([0x02008BE0,[guid,target,count*2]])
            for i in range(count):store(target+i*2,2,guid)
            if failure!=2:
                for offset,value in [(10,afirst),(12,alast),(14,afirst)]:store(manager+offset,2,value)
                target=CACHE+bank*0x540+0x500+afirst*2
                expected_calls.append([0x02008BE0,[guid,target,(alast-afirst+1)*2]])
                for i in range(alast-afirst+1):store(target+i*2,2,guid)
                store(manager+20,4,1);store(manager,4,bank);result=1
    else:
        first,last,current=[(0,0,0),(0,127,0),(0,127,127),(0,127,128),
            (2,1,0),(4,15,16),(16,31,16),(16,31,32),(0,31,40),
            (31,31,31),(0,31,0),(4,15,8)][variant]
        if entry==0x02036EA4:
            last=31 if last==127 else last
            current={127:31,128:32}.get(current,current)
        struct.pack_into('<I',page,0x100,bank)
        offset=4 if entry==0x02036DD4 else 10
        struct.pack_into('<HHH',page,0x100+offset,first,last,current)
        expected_page=bytearray(page)
        capacity=((last-current+1)&0xFFFF)if current<=last+1 and first<=last else 0
        if entry==0x02036DD4:
            count=[0,1,2,4,16,127,128,0x7FFF,0x8000,0xFFFF][(index//36)%10]
            arguments=[manager,source,count]
            result=int(capacity>=count)
            if result:
                assert current+count<=128
                for i in range(count):
                    for field in [0,2,4]:store(CACHE+bank*0x540+0x100+(current+i)*8+field,2,read_half(source+i*8+field))
                    store(manager+8,2,current+i+1)
        else:
            arguments=[manager,source]
            values=[0,1,-1,15,-15,0x7FFFFFFF,-0x80000000,0x12345678,-0x12345678]
            matrix=[values[(index+i)%len(values)]for i in range(4)]
            struct.pack_into('<iiii',page,0x400,*matrix);expected_page=bytearray(page)
            result=current if capacity>=1 else 0xFFFE
            if capacity>=1:
                assert current<32
                for field,value in zip([6,14,22,30],matrix):store(CACHE+bank*0x540+0x100+current*32+field,2,value>>4)
                store(manager+14,2,current+1)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.mem_map(0x02000000,0x100000)
    machine.mem_write(0x02000000,image);machine.mem_write(entry,body)
    machine.mem_write(CACHE,bytes(cache));machine.mem_write(GUID,struct.pack('<H',guid))
    before_main=bytes(machine.mem_read(0x02000000,0x100000))
    machine.mem_map(DATA,4096);machine.mem_write(DATA,bytes(page))
    machine.mem_map(STACK,4096);stack=rng.randbytes(4096);machine.mem_write(STACK,stack)
    machine.mem_map(STOP,4096)
    initial=[rng.getrandbits(32)for register in REGISTERS]
    for register,value in zip(REGISTERS,initial):machine.reg_write(register,value)
    for register,value in zip(REGISTERS,arguments):machine.reg_write(register,value)
    machine.reg_write(UC_ARM_REG_CPSR,0x1F|((index%16)<<28))
    machine.reg_write(UC_ARM_REG_SP,STACK+2048);machine.reg_write(UC_ARM_REG_LR,STOP)
    own=set();helper=set();pending=[];returned=[];calls=[];writes=[]
    def code(uc,address,size,unused):
        if pending and address==pending[-1]:returned.append(pending.pop())
        if entry<=address<entry+len(body):own.add(address);return
        assert 0x02008BE0<=address<0x02008BF8,hex(address)
        helper.add(address)
        if address==0x02008BE0:
            calls.append([address,[uc.reg_read(register)for register in REGISTERS[:3]]])
            pending.append(uc.reg_read(UC_ARM_REG_LR))
    def write(uc,access,address,size,value,unused):
        if STACK<=address and address+size<=STACK+4096:
            assert STACK+1920<=address and address+size<=STACK+2048
        else:
            assert address==GUID or CACHE<=address and address+size<=CACHE+0xFC0 or DATA<=address and address+size<=DATA+4096
            writes.append([address,size,value&((1<<(size*8))-1)])
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP,count=bound)
    assert machine.reg_read(UC_ARM_REG_PC)==STOP,'Bounded prefix is not actual return'
    assert not pending and len(returned)==len(calls)
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+2048
    assert all(machine.reg_read(register)==value for register,value in zip(REGISTERS[4:12],initial[4:12]))
    after_stack=bytes(machine.mem_read(STACK,4096));assert after_stack[:1920]==stack[:1920]and after_stack[2048:]==stack[2048:]
    after_main=bytes(machine.mem_read(0x02000000,0x100000));offset=GUID-0x02000000;end=CACHE-0x02000000+0xFC0
    assert after_main[:offset]==before_main[:offset]and after_main[offset+2:offset+4]==before_main[offset+2:offset+4]and after_main[end:]==before_main[end:]
    after_page=bytes(machine.mem_read(DATA,4096));after_cache=bytes(machine.mem_read(CACHE,0xFC0))
    after_guid=struct.unpack('<H',machine.mem_read(GUID,2))[0]
    passed=after_page==expected_page and after_cache==expected_cache and after_guid==expected_guid
    passed=passed and writes==expected_writes and calls==expected_calls and machine.reg_read(UC_ARM_REG_R0)==result
    return dict(index=index,entry=hex(entry),modelPassed=passed,actualReturn=True,arguments=arguments,
        result=machine.reg_read(UC_ARM_REG_R0),expectedResult=result,actualNativeReturns=len(returned),providedCalls=0,
        ownedObserved=sorted(own),helperObserved=sorted(helper),registers=[machine.reg_read(register)for register in REGISTERS],
        cpsr=machine.reg_read(UC_ARM_REG_CPSR),lr=machine.reg_read(UC_ARM_REG_LR),calls=calls,writes=writes,
        pageSha256=hashlib.sha256(after_page).hexdigest(),cacheSha256=hashlib.sha256(after_cache).hexdigest(),
        stackSha256=hashlib.sha256(after_stack).hexdigest(),guid=after_guid,
        firstWriteMismatch=next(([a,b]for a,b in zip(writes,expected_writes)if a!=b),None))
