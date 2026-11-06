import hashlib
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRIES = {0x020099E0: 44, 0x02011EB4: 48, 0x02011EE4: 48}
DATA, GLOBAL, STACK, STOP = 0x02380000, 0x020E3000, 0x027F0000, 0x027FF000
IRQ = {0x02007FF4: 20, 0x02008008: 24}
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def execute(image, entry, body, index, bound=256, require_model=True):
    ENTRY = entry
    GLOBAL = 0x020E3000 if entry == 0x020099E0 else 0x020E5000
    rng = random.Random(ENTRY * 100000 + index)
    pages = [bytearray(rng.randbytes(4096)) for unused in range(2)]
    if entry == 0x020099E0:
        selector = [0, 1, 2, 0xFFFFFFFF, 0x80000000][index % 5]
        first, second = rng.getrandbits(32), rng.getrandbits(32)
        struct.pack_into('<3I', pages[1], 0x780, rng.getrandbits(32), first, selector)
        struct.pack_into('<I', pages[1], 0x7A0, second)
        expected_result = second if selector else first
    else:
        pointer = 0 if index % 4 == 0 else DATA + 0x100
        struct.pack_into('<I', pages[1], 0xD84, pointer)
        value = [0, 1, 0xFF, 0x100, 0xFFFF, 0x10000, 0xFFFFFFFF, rng.getrandbits(32)][index // 4 % 8]
        struct.pack_into('<I', pages[0], 0x24C, value)
        struct.pack_into('<H', pages[0], 0x250, value & 0xFFFF)
        expected_result = value & 0xFFFF if pointer else 0
    expected = [bytearray(page) for page in pages]
    initial = [rng.getrandbits(32) for unused in REGS]
    initial[0] = rng.getrandbits(32)
    cpsr = ((index % 16) << 28) | 0x1F | ((index // 2 % 2) << 7) | ((index // 7 % 2) << 6)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_write(0x02000000, image)
    machine.mem_write(ENTRY, body)
    for address, page in zip([DATA, GLOBAL], pages):
        machine.mem_write(address, bytes(page))
    guards = rng.randbytes(8192)
    machine.mem_write(STACK - 4096, guards)
    machine.reg_write(UC_ARM_REG_CPSR, cpsr)
    for register, value in zip(REGS, initial):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, writes, observed, helper_observed = [], [], set(), set()
    helper_returns = []

    def code(uc, address, size, unused):
        if ENTRY <= address < ENTRY + len(body):
            observed.update(range(address, address + size))
            return
        for entry, length in IRQ.items():
            if entry <= address < entry + length:
                helper_observed.update(range(address, address + size))
                if address == entry:
                    calls.append([address, [] if entry == 0x02007FF4 else [uc.reg_read(UC_ARM_REG_R0)]])
                if address == entry + length - 4:
                    helper_returns.append(entry)
                return
        raise AssertionError(('Unexpected native instruction', hex(address)))

    def write(uc, access, address, size, value, unused):
        if STACK - 4096 <= address and address + size <= STACK + 4096:
            return
        assert any(start <= address and address + size <= start + 4096 for start in [DATA, GLOBAL])
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP, timeout=1000000, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_SP) == STACK
    assert [machine.reg_read(register) for register in REGS[4:12]] == initial[4:12]
    assert machine.reg_read(UC_ARM_REG_CPSR) & 0xFF == cpsr & 0xFF
    assert bytes(machine.mem_read(STACK - 4096, 256)) == guards[:256]
    assert bytes(machine.mem_read(STACK + 4096 - 256, 256)) == guards[-256:]
    actual = [bytes(machine.mem_read(address, 4096)) for address in [DATA, GLOBAL]]
    result = machine.reg_read(UC_ARM_REG_R0)
    expected_calls = [[0x02007FF4, []], [0x02008008, [cpsr & 0x80]]]
    passed = actual == expected and calls == expected_calls and result == expected_result
    assert len(helper_returns) == len(calls)
    if require_model:
        assert passed, (index, calls, expected_calls, hex(result), expected_result)
    record = dict(index=index, modelPassed=passed, result=result, calls=calls, writes=writes,
                  pagesSha256=hashlib.sha256(b''.join(actual)).hexdigest(), actualTopReturns=1,
                  suppliedCalls=0, actualNativeDependencyReturns=len(helper_returns),
                  observed=sorted(observed), helperObserved=sorted(helper_observed),
                  registers=[machine.reg_read(register) for register in REGS], cpsr=machine.reg_read(UC_ARM_REG_CPSR))
    del machine
    return record
