import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

DATA, GLOBAL, IO, STACK, STOP = 0x02380000, 0x020ED000, 0x04000000, 0x027F0000, 0x027FF000
ENTRIES = {0x0202AD78: 44, 0x02029D5C: 40, 0x02029E68: 40}
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def scenario(entry, index):
    rng = random.Random(entry * 10000 + index)
    pages = [bytearray(rng.randbytes(4096)) for unused in range(3)]
    expected = [bytearray(page) for page in pages]
    initial = [rng.getrandbits(32) for unused in range(13)]
    ordered = []
    if entry == 0x0202AD78:
        source = DATA + 0x500
        destination = [DATA + 0x100, source, source - 4, source + 4, source + 8][index % 5]
        initial[:2] = [destination, source]
        struct.pack_into('<H', pages[0], 0x502, index * 127 & 0xFFFF)
        struct.pack_into('<I', pages[0], 0x504, [0, 1, 0xFFFFFFFF, 0x80000000, rng.getrandbits(32)][index // 5 % 5])
        expected[0][:] = pages[0]
        begin = source - ((struct.unpack_from('<H', expected[0], 0x502)[0] >> 8) & 127)
        struct.pack_into('<I', expected[0], destination - DATA, begin)
        length = struct.unpack_from('<I', expected[0], 0x504)[0]
        end = (source + 16 + length) & 0xFFFFFFFF
        struct.pack_into('<I', expected[0], destination - DATA + 4, end)
        result = destination
        ordered = [[destination, 4, begin], [destination + 4, 4, end]]
    else:
        offset, hardware = (0xD24, 0x354) if entry == 0x02029D5C else (0xD1A, 0x35C)
        raw = [0, 1, 0xFFFF, 0x10000, 0xFFFF0000, 0x80000000, 0xFFFFFFFF, rng.getrandbits(32)][index % 8]
        initial[0] = raw
        old = index * 257 & 0xFFFF
        struct.pack_into('<H', pages[1], offset, old)
        expected[1][:] = pages[1]
        struct.pack_into('<H', expected[1], offset, raw & 0xFFFF)
        struct.pack_into('<H', expected[2], hardware, raw & 0xFFFF)
        ordered = [[GLOBAL + offset, 2, raw & 0xFFFF], [IO + hardware, 2, raw & 0xFFFF]]
        if entry == 0x02029E68:
            ordered.reverse()
        result = old
    return pages, expected, initial, result, ordered


def execute(image, entry, body, index, bound=128, require_model=True):
    pages, expected, initial, expected_result, expected_writes = scenario(entry, index)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_map(IO, 4096)
    machine.mem_write(0x02000000, image)
    machine.mem_write(entry, body)
    for address, page in zip([DATA, GLOBAL, IO], pages):
        machine.mem_write(address, bytes(page))
    machine.reg_write(UC_ARM_REG_CPSR, ((index % 16) << 28) | 0x10)
    for register, value in zip(REGS, initial):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    writes, observed = [], set()

    def code(uc, address, size, unused):
        assert entry <= address < entry + len(body), hex(address)
        observed.update(range(address, address + size))

    def write(uc, access, address, size, value, unused):
        assert any(start <= address and address + size <= start + 4096 for start in [DATA, GLOBAL, IO])
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(entry, STOP, timeout=1000000, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_SP) == STACK and machine.reg_read(UC_ARM_REG_LR) == STOP
    assert [machine.reg_read(register) for register in REGS[4:12]] == initial[4:12]
    assert machine.reg_read(UC_ARM_REG_CPSR) & 0x3F == 0x10
    actual = [bytes(machine.mem_read(address, 4096)) for address in [DATA, GLOBAL, IO]]
    result = machine.reg_read(UC_ARM_REG_R0)
    passed = all(a == b for a,b in zip(actual, expected)) and result == expected_result and writes == expected_writes
    if require_model:
        assert passed, (hex(entry), index, result, expected_result, writes, expected_writes)
    record = dict(index=index, result=result, modelPassed=passed, writes=writes,
        pagesSha256=hashlib.sha256(b''.join(actual)).hexdigest(), actualTopReturns=1,
        suppliedCalls=0, actualNativeDependencyReturns=0, observed=sorted(observed),
        registers=[machine.reg_read(register) for register in REGS], cpsr=machine.reg_read(UC_ARM_REG_CPSR))
    del machine
    return record
