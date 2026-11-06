import hashlib
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, SIZE = 0x0200B7C8, 132
DATA, GLOBAL, STACK, STOP = 0x02380000, 0x020E5000, 0x027F0000, 0x027FF000
IRQ = {0x02007FF4: 20, 0x02008008: 24}
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def execute(image, body, index, bound=256, require_model=True):
    rng = random.Random(ENTRY * 100000 + index)
    pages = [bytearray(rng.randbytes(4096)) for unused in range(2)]
    node = DATA + 0x100
    active = [0, 1, 0xFFFFFFFF, 0x80000000][index % 4]
    previous, following = [(0, 0), (DATA + 0x200, 0), (0, DATA + 0x300),
                            (DATA + 0x200, DATA + 0x300), (DATA + 0x200, DATA + 0x200)][index // 4 % 5]
    flags = [0, 1, 0xFFFFFFFF, 0x80000000, rng.getrandbits(32)][index // 20 % 5]
    struct.pack_into('<3I', pages[0], 0x100, active, previous, following)
    struct.pack_into('<I', pages[0], 0x11C, flags)
    fallback = [0, DATA + 0x380, node, 0xFFFFFFFF][index // 100 % 4]
    root = [node, 0, DATA + 0x500][index // 400 % 3]
    struct.pack_into('<2I', pages[1], 0x348, fallback, root)
    expected = [bytearray(page) for page in pages]
    if active:
        if previous:
            struct.pack_into('<I', expected[0], previous - DATA + 8, following)
        if following:
            struct.pack_into('<I', expected[0], following - DATA + 4, previous)
        for offset in [0x100, 0x108, 0x104]:
            struct.pack_into('<I', expected[0], offset, 0)
        struct.pack_into('<I', expected[0], 0x11C, flags & ~1)
        if root == node:
            struct.pack_into('<I', expected[1], 0x34C, fallback)
            struct.pack_into('<I', expected[1], 0x354, 0)
            struct.pack_into('<H', expected[1], 0x352, 0)
            struct.pack_into('<H', expected[1], 0x350, 0)
    initial = [rng.getrandbits(32) for unused in REGS]
    initial[0] = node
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
    expected_calls = [[0x02007FF4, []], [0x02008008, [cpsr & 0x80]]] if active else []
    passed = actual == expected and calls == expected_calls and result == (0x80 if active else 0)
    assert len(helper_returns) == len(calls)
    if require_model:
        assert passed, (index, calls, expected_calls, hex(result), active)
    record = dict(index=index, modelPassed=passed, result=result, calls=calls, writes=writes,
                  pagesSha256=hashlib.sha256(b''.join(actual)).hexdigest(), actualTopReturns=1,
                  suppliedCalls=0, actualNativeDependencyReturns=len(helper_returns),
                  observed=sorted(observed), helperObserved=sorted(helper_observed),
                  registers=[machine.reg_read(register) for register in REGS], cpsr=machine.reg_read(UC_ARM_REG_CPSR))
    del machine
    return record
