import hashlib
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRIES = {0x02006C38: 40, 0x02006CA4: 52}
DATA, GLOBAL, STACK, STOP = 0x02380000, 0x020E3000, 0x027F0000, 0x027FF000
IRQ = {0x02007FF4: 20, 0x02008008: 24}
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def execute(image, entry, body, index, bound=256, require_model=True):
    ENTRY = entry
    GLOBAL = 0x020E3000
    rng = random.Random(ENTRY * 100000 + index)
    pages = [bytearray(rng.randbytes(4096)) for unused in range(2)]
    values = [0, 1, 2, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, rng.getrandbits(32)]
    previous, argument = values[index % 7], values[index // 7 % 7]
    offset = 0x3F0 if entry == 0x02006C38 else 0x3C4
    struct.pack_into('<I', pages[1], offset, previous)
    expected = [bytearray(page) for page in pages]
    expected_result = previous
    expected_writes = []
    if entry == 0x02006C38 or previous:
        replacement = argument if entry == 0x02006C38 else (previous - 1) & 0xFFFFFFFF
        struct.pack_into('<I', expected[1], offset, replacement)
        expected_writes.append([GLOBAL + offset, 4, replacement])
    initial = [rng.getrandbits(32) for unused in REGS]
    initial[0] = argument
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
    calls, writes, stack_writes, observed, helper_observed = [], [], [], set(), set()
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
            assert STACK - 16 <= address and address + size <= STACK
            stack_writes.append([address, size, value])
            return
        assert any(start <= address and address + size <= start + 4096 for start in [DATA, GLOBAL])
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP, timeout=1000000, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_SP) == STACK
    assert [machine.reg_read(register) for register in REGS[4:12]] == initial[4:12]
    assert bytes(machine.mem_read(STACK - 4096, 256)) == guards[:256]
    assert bytes(machine.mem_read(STACK + 4096 - 256, 256)) == guards[-256:]
    actual = [bytes(machine.mem_read(address, 4096)) for address in [DATA, GLOBAL]]
    result = machine.reg_read(UC_ARM_REG_R0)
    expected_calls = [[0x02007FF4, []], [0x02008008, [cpsr & 0x80]]]
    passed = (actual == expected and calls == expected_calls and writes == expected_writes and result == expected_result
              and machine.reg_read(UC_ARM_REG_CPSR) & 0xFF == cpsr & 0xFF)
    assert len(helper_returns) == len(calls)
    if require_model:
        assert passed, (index, calls, expected_calls, hex(result), expected_result)
    record = dict(index=index, modelPassed=passed, result=result, calls=calls, writes=writes,
                  stackWrites=stack_writes,
                  completeStackSha256=hashlib.sha256(bytes(machine.mem_read(STACK - 4096,8192))).hexdigest(),
                  linkRegister=machine.reg_read(UC_ARM_REG_LR),
                  pagesSha256=hashlib.sha256(b''.join(actual)).hexdigest(), actualTopReturns=1,
                  suppliedCalls=0, actualNativeDependencyReturns=len(helper_returns),
                  observed=sorted(observed), helperObserved=sorted(helper_observed),
                  registers=[machine.reg_read(register) for register in REGS], cpsr=machine.reg_read(UC_ARM_REG_CPSR))
    del machine
    return record
