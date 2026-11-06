import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, SIZE = 0x0203716C, 296
CACHE, DMA, DATA, STACK, STOP = 0x020F0F08, 0x020DCB44, 0x02400000, 0x03030000, 0x0F000000
NATIVE = {0x020072D0:28, 0x02008C14:20}
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
    UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def execute(image, body, index, bound=8192):
    rng = random.Random(0x3716C0000 + index)
    bank, fast = (index // 5) % 3, [0,1,2,0x80000000,0xFFFFFFFF][index % 5]
    first, last, current = [(0,0,0),(2,1,0),(0,127,128),(127,127,128),
        (1,15,17),(16,31,16),(0,15,0),(120,127,0)][(index // 15) % 8]
    dma = [0xFFFFFFFF,0,1,2,3][(index // 120) % 5]
    affine = [0,1,127,0x7FFF,0x8000,0xFFFF][(index // 3) % 6]
    manager = DATA + 0x100
    page = bytearray(rng.randbytes(4096))
    struct.pack_into('<IHHHH', page, 0x100, bank, first, last, current, affine)
    struct.pack_into('<I', page, 0x114, fast)
    cache = bytearray(rng.randbytes(0xFC0))
    expected_page, expected_cache = bytearray(page), bytearray(cache)
    target = CACHE + bank * 0x540 + 0x100 + first * 8
    count = (last - first + 1) & 0xFFFF
    length = count * 8 if current <= last + 1 and first <= last else 0
    writes, expected_writes, calls, expected_calls = [], [], [], []
    def expected_write(address, size, value):
        expected_writes.append([address,size,value])
        if CACHE <= address < CACHE + 0xFC0:
            expected_cache[address-CACHE:address-CACHE+size] = value.to_bytes(size,'little')
        else:
            expected_page[address-DATA:address-DATA+size] = value.to_bytes(size,'little')
    if fast:
        expected_calls.append(dict(address=0x020072D0, words=[target,length], originalNative=True))
        if dma != 0xFFFFFFFF:
            expected_calls.append(dict(address=0x0200845C, words=[dma,target,192,length], originalNative=False))
        else:
            expected_calls.append(dict(address=0x02008C14, words=[192,target,length], originalNative=True))
        for offset in range(0,length,4):
            expected_write(target+offset,4,192)
    else:
        for offset in range(count):
            expected_write(target+offset*8,2,192)
    expected_write(manager+8,2,first)
    expected_write(manager+14,2,affine)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000,0x100000)
    machine.mem_write(0x02000000,image)
    machine.mem_write(ENTRY,body)
    machine.mem_write(CACHE,bytes(cache))
    machine.mem_write(DMA,struct.pack('<I',dma))
    initial_main = bytes(machine.mem_read(0x02000000,0x100000))
    machine.mem_map(DATA,4096)
    machine.mem_write(DATA,bytes(page))
    machine.mem_map(STACK,4096)
    stack = rng.randbytes(4096)
    machine.mem_write(STACK,stack)
    machine.mem_map(STOP,4096)
    machine.reg_write(UC_ARM_REG_CPSR,0x1F | ((index % 16) << 28))
    initial = [rng.getrandbits(32) for register in REGISTERS]
    for register,value in zip(REGISTERS,initial):machine.reg_write(register,value)
    machine.reg_write(UC_ARM_REG_R0,manager)
    machine.reg_write(UC_ARM_REG_SP,STACK+2048)
    machine.reg_write(UC_ARM_REG_LR,STOP)
    own, helpers, pending, returned = set(), set(), [], []
    def code(uc,address,size,unused):
        if pending and address == pending[-1][0]:returned.append(pending.pop()[1])
        if ENTRY <= address < ENTRY + len(body):
            own.add(address)
            return
        if address == 0x0200845C:
            words = [uc.reg_read(register) for register in REGISTERS[:4]]
            calls.append(dict(address=address,words=words,originalNative=False))
            for offset in range(0,words[3],4):
                location = words[1]+offset
                assert CACHE <= location and location+4 <= CACHE+0xFC0
                uc.mem_write(location,struct.pack('<I',words[2]))
                writes.append([location,4,words[2]])
            for register in REGISTERS[1:4]+[UC_ARM_REG_R12]:uc.reg_write(register,rng.getrandbits(32))
            uc.reg_write(UC_ARM_REG_R0,rng.getrandbits(32))
            uc.reg_write(UC_ARM_REG_CPSR,0x1F | (((index+len(calls))%16)<<28))
            uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
            return
        assert any(base <= address < base+length for base,length in NATIVE.items()),hex(address)
        helpers.add(address)
        if address in NATIVE:
            count = 2 if address == 0x020072D0 else 3
            calls.append(dict(address=address,words=[uc.reg_read(register) for register in REGISTERS[:count]],originalNative=True))
            pending.append((uc.reg_read(UC_ARM_REG_LR),address))
    def write(uc,access,address,size,value,unused):
        if STACK <= address and address+size <= STACK+4096:
            assert STACK+1984 <= address and address+size <= STACK+2048
        else:
            assert CACHE <= address and address+size <= CACHE+0xFC0 or DATA <= address and address+size <= DATA+4096
            writes.append([address,size,value & ((1<<(size*8))-1)])
    machine.hook_add(UC_HOOK_CODE,code)
    machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(ENTRY,STOP,count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP,'Bounded prefix is not actual return'
    assert not pending and len(returned) == sum(item['originalNative'] for item in calls)
    assert machine.reg_read(UC_ARM_REG_SP) == STACK+2048
    assert all(machine.reg_read(register)==value for register,value in zip(REGISTERS[4:12],initial[4:12]))
    after_stack = bytes(machine.mem_read(STACK,4096))
    assert after_stack[:1984]==stack[:1984] and after_stack[2048:]==stack[2048:]
    after_main = bytes(machine.mem_read(0x02000000,0x100000))
    offset=CACHE-0x02000000
    assert after_main[:offset]==initial_main[:offset] and after_main[offset+0xFC0:]==initial_main[offset+0xFC0:]
    after_page = bytes(machine.mem_read(DATA,4096))
    after_cache = bytes(machine.mem_read(CACHE,0xFC0))
    passed = after_page==expected_page and after_cache==expected_cache and writes==expected_writes
    passed = passed and calls==expected_calls and machine.reg_read(UC_ARM_REG_R0)==affine
    return dict(modelPassed=passed,actualReturn=True,index=index,bank=bank,fast=fast,dma=dma,
        first=first,last=last,current=current,affine=affine,result=machine.reg_read(UC_ARM_REG_R0),
        registers=[machine.reg_read(register)for register in REGISTERS],cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        lr=machine.reg_read(UC_ARM_REG_LR),calls=calls,writes=writes,
        actualNativeReturns=len(returned),providedCalls=sum(not item['originalNative'] for item in calls),
        ownedObserved=sorted(own),helperObserved=sorted(helpers),
        pageSha256=hashlib.sha256(after_page).hexdigest(),cacheSha256=hashlib.sha256(after_cache).hexdigest(),
        stackSha256=hashlib.sha256(after_stack).hexdigest())
