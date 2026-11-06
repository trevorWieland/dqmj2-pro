import hashlib
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from main_irq_guarded_getters_fixture_v2_20261101 import REGS

ENTRY, SIZE = 0x0203A650, 56
LOWER = {0x0203B5D8: 96, 0x020388DC: 68}
DATA, GLOBAL, STACK, STOP = 0x02380000, 0x020F4000, 0x027F0000, 0x027FF000


def execute(image, body, index, bound=2048, require_model=True):
    rng = random.Random(ENTRY * 100000 + index)
    page = bytearray(rng.randbytes(4096))
    global_page = bytearray(rng.randbytes(4096))
    obj = DATA + (0x100 if index % 2 == 0 else 0x800)
    count = [-0x80000000, -1, 0, 1, 2, 4, 8, 16, 32][index // 8 % 9]
    references = [0, 0, 0, 1, 0xFFFFFFFF, 0x80000000, 2, rng.getrandbits(32)][index % 8]
    source = [DATA + 0x500, obj + 0x4C, obj + 0x4B, obj + 0x4D][index // 72 % 4]
    for slot in range(32):
        page[source - DATA + slot] = ((slot * 7 + index) % 32 if (index // 8 + index // 72) % 2 else 32 + (slot * 17 + index) % 224)
    struct.pack_into('<I', page, obj - DATA + 0x120, references)
    wanted = bytearray(page)
    expected_writes, expected_calls = [], []
    mask = 0
    if references == 0:
        expected_calls.append([0x0203B5D8, [obj, count & 0xFFFFFFFF, source]])
        for slot in range(max(count, 0)):
            value = wanted[source - DATA + slot]
            wanted[obj - DATA + 0x4C + slot] = value
            expected_writes.append([obj + 0x4C + slot, 1, value])
            bit = wanted[source - DATA + slot]
            mask |= 1 << bit if bit < 32 else 0
        expected_calls.append([0x020388DC, [mask]])
    reserved = rng.getrandbits(32) | mask
    struct.pack_into('<I', global_page, 0xC40, reserved)
    result = int(references != 0 or mask == 0)
    if references == 0 and result:
        for offset, value in [(0x48, count & 0xFFFFFFFF), (0x44, mask)]:
            struct.pack_into('<I', wanted, obj - DATA + offset, value)
            expected_writes.append([obj + offset, 4, value])
    if result:
        value = (references + 1) & 0xFFFFFFFF
        struct.pack_into('<I', wanted, obj - DATA + 0x120, value)
        expected_writes.append([obj + 0x120, 4, value])
    initial = [rng.getrandbits(32) for unused in REGS]
    initial[:3] = [obj, count & 0xFFFFFFFF, source]
    cpsr = (index % 16 << 28) | 0x1F | (index // 2 % 2 << 7) | (index // 7 % 2 << 6)
    guards = rng.randbytes(8192)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_write(0x02000000, image)
    machine.mem_write(ENTRY, body)
    machine.mem_write(DATA, bytes(page))
    machine.mem_write(GLOBAL, bytes(global_page))
    machine.mem_write(STACK - 4096, guards)
    machine.reg_write(UC_ARM_REG_CPSR, cpsr)
    for register, value in zip(REGS, initial):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    own, helpers, writes, stack_writes, calls, returns, pending = set(), set(), [], [], [], [], []

    def code(uc, address, size, unused):
        if pending and address == pending[-1][1]:
            returns.append(pending.pop()[0])
        if ENTRY <= address < ENTRY + len(body):
            own.update(range(address, address + size))
        else:
            assert any(start <= address < start + width for start, width in LOWER.items()), hex(address)
            helpers.update(range(address, address + size))
        if address in LOWER:
            width = 3 if address == 0x0203B5D8 else 1
            calls.append([address, [uc.reg_read(register) for register in REGS[:width]]])
            pending.append([address, uc.reg_read(UC_ARM_REG_LR)])

    def write(uc, access, address, size, value, unused):
        if STACK - 4096 <= address and address + size <= STACK + 4096:
            assert STACK - 128 <= address and address + size <= STACK
            stack_writes.append([address, size, value])
        else:
            assert DATA <= address and address + size <= DATA + 4096
            writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP, timeout=1000000, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP and not pending
    assert machine.reg_read(UC_ARM_REG_SP) == STACK
    assert [machine.reg_read(register) for register in REGS[4:12]] == initial[4:12]
    assert bytes(machine.mem_read(STACK - 4096, 256)) == guards[:256]
    assert bytes(machine.mem_read(STACK + 4096 - 256, 256)) == guards[-256:]
    actual = bytes(machine.mem_read(DATA, 4096))
    global_after = bytes(machine.mem_read(GLOBAL, 4096))
    actual_result = machine.reg_read(UC_ARM_REG_R0)
    passed = (actual == wanted and global_after == global_page and writes == expected_writes
        and actual_result == result and calls == expected_calls and len(returns) == len(expected_calls)
        and machine.reg_read(UC_ARM_REG_CPSR) & 0xFF == cpsr & 0xFF)
    if require_model:
        assert passed, (index, actual_result, result, calls, expected_calls, writes, expected_writes)
    record = dict(index=index, modelPassed=passed, result=actual_result, calls=calls, writes=writes,
        stackWrites=stack_writes, pagesSha256=hashlib.sha256(actual + global_after).hexdigest(),
        completeStackSha256=hashlib.sha256(bytes(machine.mem_read(STACK - 4096, 8192))).hexdigest(),
        registers=[machine.reg_read(register) for register in REGS], cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        actualTopReturns=1, actualNativeDependencyReturns=len(returns), suppliedCalls=0,
        observed=sorted(own), helperObserved=sorted(helpers))
    del machine
    return record
