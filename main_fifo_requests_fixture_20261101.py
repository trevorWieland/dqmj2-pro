import hashlib
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from main_irq_guarded_getters_fixture_v2_20261101 import REGS, IRQ

GLOBAL, MMIO, STACK, STOP = 0x020E5000, 0x04000000, 0x027F0000, 0x027FF000
ENTRIES = {0x0200F370: 112, 0x0200F418: 116, 0x0200F4C4: 124}
OPERATIONS = {0x0200F370: (0, 0x0200FB70, 0x11), 0x0200F418: (1, 0x0200FB80, 0x12), 0x0200F4C4: (2, 0x0200FB60, 0x10)}
LOWER = {**IRQ, 0x0200FB60: 12, 0x0200FB70: 12, 0x0200FB80: 12, 0x0200FBA0: 40, 0x0200A440: 132}
RETURNS = {0x02008004, 0x0200801C, 0x0200FBC4, 0x0200A48C, 0x0200A4AC, 0x0200A4C0}


def execute(image, entry, body, index, bound=512, require_model=True):
    rng = random.Random(entry * 100000 + index)
    pages = [bytearray(rng.randbytes(4096)) for unused in range(2)]
    values = [0, 1, 0xFFFFFFFF, 0x80000000, 0x7FFFFFFF, rng.getrandbits(32)]
    registers = [rng.getrandbits(32) for unused in REGS]
    registers[:4] = [values[(index // 4 + slot) % len(values)] for slot in range(4)]
    busy = [0, 1, 0xFFFFFFFF, 0][index % 4]
    status = [0, 2, 0x4000, 0x4002, 0x8000, 0x8002, 0xC000, 0xFFFF][index // 4 % 8]
    struct.pack_into('<I', pages[0], 0x444, busy)
    struct.pack_into('<H', pages[1], 0x184, status)
    wanted = [bytearray(page) for page in pages]
    cpsr = (index % 16 << 28) | 0x1F | (index // 2 % 2 << 7) | (index // 7 % 2 << 6)
    expected_calls = [[0x02007FF4, []], [0x02008008, [cpsr & 0x80]]]
    expected_writes = []
    expected_result = 1
    expected_returns = 2
    operation, veneer, command = OPERATIONS[entry]
    if not busy:
        effects = [(0x444, 1), (0x458, operation), (0x45C, 0), (0x44C, registers[0])]
        if operation == 2:
            effects += [(0x450, registers[1]), (0x448, registers[2]), (0x454, registers[3])]
        else:
            effects += [(0x448, registers[1]), (0x454, registers[2])]
        for offset, value in effects:
            struct.pack_into('<I', wanted[0], offset, value)
            expected_writes.append([GLOBAL + offset, 4, value])
        expected_calls += [[veneer, []], [0x0200FBA0, [command]], [0x0200A440, [5, command << 8, 0]]]
        expected_returns += 2
        expected_result = 3 if status & 0x4002 else 0
        if status & 0x4000:
            value = status | 0xC000
            struct.pack_into('<H', wanted[1], 0x184, value)
            expected_writes.append([MMIO + 0x184, 2, value])
        else:
            expected_calls += [[0x02007FF4, []], [0x02008008, [cpsr & 0x80]]]
            expected_returns += 2
            if not status & 2:
                value = command << 14 | 5
                struct.pack_into('<I', wanted[1], 0x188, value)
                expected_writes.append([MMIO + 0x188, 4, value])
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_map(MMIO, 4096)
    machine.mem_write(0x02000000, image)
    machine.mem_write(entry, body)
    for address, page in zip([GLOBAL, MMIO], pages):
        machine.mem_write(address, bytes(page))
    guards = rng.randbytes(8192)
    machine.mem_write(STACK - 4096, guards)
    machine.reg_write(UC_ARM_REG_CPSR, cpsr)
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, writes, stack_writes, observed, helpers, returns = [], [], [], set(), set(), []

    def code(uc, address, size, unused):
        if entry <= address < entry + len(body):
            observed.update(range(address, address + size))
            return
        assert any(start <= address < start + length for start, length in LOWER.items()), hex(address)
        helpers.update(range(address, address + size))
        if address in LOWER:
            count = 0 if address in [0x02007FF4, 0x0200FB60, 0x0200FB70, 0x0200FB80] else 3 if address == 0x0200A440 else 1
            calls.append([address, [uc.reg_read(register) for register in REGS[:count]]])
        if address in RETURNS:
            returns.append(address)

    def write(uc, access, address, size, value, unused):
        if STACK - 4096 <= address and address + size <= STACK + 4096:
            assert STACK - 128 <= address and address + size <= STACK
            stack_writes.append([address, size, value])
            return
        assert GLOBAL <= address and address + size <= GLOBAL + 4096 or MMIO <= address and address + size <= MMIO + 4096
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(entry, STOP, timeout=1000000, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_SP) == STACK
    assert [machine.reg_read(register) for register in REGS[4:12]] == registers[4:12]
    actual = [bytes(machine.mem_read(address, 4096)) for address in [GLOBAL, MMIO]]
    result = machine.reg_read(UC_ARM_REG_R0)
    passed = (actual == wanted and calls == expected_calls and writes == expected_writes and result == expected_result
        and len(returns) == expected_returns and machine.reg_read(UC_ARM_REG_CPSR) & 0xFF == cpsr & 0xFF)
    assert bytes(machine.mem_read(STACK - 4096, 256)) == guards[:256]
    assert bytes(machine.mem_read(STACK + 4096 - 256, 256)) == guards[-256:]
    if require_model:
        assert passed, (hex(entry), index, calls, expected_calls, writes, expected_writes, result, expected_result, returns, expected_returns)
    record = dict(index=index, modelPassed=passed, result=result, calls=calls, writes=writes,
        stackWrites=stack_writes, pagesSha256=hashlib.sha256(b''.join(actual)).hexdigest(),
        completeStackSha256=hashlib.sha256(bytes(machine.mem_read(STACK - 4096, 8192))).hexdigest(),
        registers=[machine.reg_read(register) for register in REGS], cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        linkRegister=machine.reg_read(UC_ARM_REG_LR), actualTopReturns=1,
        actualNativeDependencyReturns=len(returns), physicalDependencyReturnAddresses=returns,
        suppliedCalls=0, observed=sorted(observed), helperObserved=sorted(helpers))
    del machine
    return record
