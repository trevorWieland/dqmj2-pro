import hashlib
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from main_irq_guarded_getters_fixture_v2_20261101 import REGS

ENTRY, SIZE, LOWER, LOWER_SIZE = 0x02001114, 52, 0x02000D0C, 192
DATA, STACK, STOP = 0x02380000, 0x027F0000, 0x027FF000


def signed(value):
    return value - 0x100000000 if value & 0x80000000 else value


def execute(image, body, index, bound=512, require_model=True):
    rng = random.Random(ENTRY * 100000 + index)
    page = bytearray(rng.randbytes(4096))
    source = DATA + 0x100
    destination = [DATA + 0x200, source, source + 4, source - 4, source + 12][index % 5]
    values = [0, 1, 0xFFFFFFFF, 0x1000, 0xFFFFF000, 0x7FFFFFFF, 0x80000000, rng.getrandbits(32)]
    scales = [values[(index // 5 + slot * 3) % len(values)] for slot in range(3)]
    for slot in range(12):
        struct.pack_into('<I', page, 0x100 + slot * 4, values[(index + slot) % len(values)])
    wanted = bytearray(page)
    expected_writes = []
    for slot in range(12):
        value = struct.unpack_from('<I', wanted, source - DATA + slot * 4)[0]
        if slot < 9:
            value = (signed(value) * signed(scales[slot // 3]) >> 12) & 0xFFFFFFFF
        struct.pack_into('<I', wanted, destination - DATA + slot * 4, value)
        expected_writes.append([destination + slot * 4, 4, value])
    result_word = value
    initial = [rng.getrandbits(32) for unused in REGS]
    initial[:4] = [source, destination, *scales[:2]]
    cpsr = (index % 16 << 28) | 0x1F | (index // 2 % 2 << 7) | (index // 7 % 2 << 6)
    guards = bytearray(rng.randbytes(8192))
    struct.pack_into('<I', guards, 4096, scales[2])
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_write(0x02000000, image)
    machine.mem_write(ENTRY, body)
    machine.mem_write(DATA, bytes(page))
    machine.mem_write(STACK - 4096, bytes(guards))
    machine.reg_write(UC_ARM_REG_CPSR, cpsr)
    for register, value in zip(REGS, initial):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    own, lower, writes, stack_writes, calls, returns = set(), set(), [], [], [], []

    def code(uc, address, size, unused):
        if ENTRY <= address < ENTRY + len(body):
            own.update(range(address, address + size))
        else:
            assert LOWER <= address < LOWER + LOWER_SIZE, hex(address)
            lower.update(range(address, address + size))
            if address == LOWER:
                fifth = struct.unpack('<I', uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 4))[0]
                calls.append([uc.reg_read(register) for register in REGS[:4]] + [fifth])
            if address == LOWER + LOWER_SIZE - 4:
                returns.append(address)

    def write(uc, access, address, size, value, unused):
        if STACK - 4096 <= address and address + size <= STACK + 4096:
            assert STACK - 64 <= address and address + size <= STACK
            stack_writes.append([address, size, value])
        else:
            assert DATA <= address and address + size <= DATA + 4096
            writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP, timeout=1000000, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_SP) == STACK
    assert [machine.reg_read(register) for register in REGS[4:12]] == initial[4:12]
    assert bytes(machine.mem_read(STACK - 4096, 256)) == bytes(guards[:256])
    assert bytes(machine.mem_read(STACK + 4096 - 256, 256)) == bytes(guards[-256:])
    actual = bytes(machine.mem_read(DATA, 4096))
    result = machine.reg_read(UC_ARM_REG_R0)
    passed = (actual == wanted and writes == expected_writes and result == result_word
        and calls == [[source, destination, *scales]] and len(returns) == 1
        and machine.reg_read(UC_ARM_REG_CPSR) == cpsr)
    if require_model:
        assert passed, (index, result, result_word, calls, writes, expected_writes)
    record = dict(index=index, modelPassed=passed, result=result, calls=calls, writes=writes,
        stackWrites=stack_writes, pagesSha256=hashlib.sha256(actual).hexdigest(),
        completeStackSha256=hashlib.sha256(bytes(machine.mem_read(STACK - 4096, 8192))).hexdigest(),
        registers=[machine.reg_read(register) for register in REGS], cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        actualTopReturns=1, actualNativeDependencyReturns=len(returns), suppliedCalls=0,
        observed=sorted(own), helperObserved=sorted(lower))
    del machine
    return record
