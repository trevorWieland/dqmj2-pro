import hashlib
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR

DATA, STACK, STOP, ENTRY = 0x02380000, 0x03030000, 0x0F000000, 0x0202B1A8
HELPERS = {0x0202ADA4: 40, 0x0202ADCC: 48, 0x0202ADFC: 44, 0x02008C14: 20, 0x0202B9CC: 16}


def fixture(index):
    rng = random.Random(ENTRY * 10000 + index)
    page = bytearray(rng.randbytes(4096))
    heap, region, begin = DATA + 0x40, DATA + 0xF00, DATA + 0x500
    length = [0, 4, 12, 16, 20, 32, 64, 128][index % 8]
    end = begin + length
    flags = index // 8 % 4
    left, right = bool(index // 32 & 1), bool(index // 64 & 1)
    left_adjacent, right_adjacent = bool(index // 128 & 1), bool(index // 256 & 1)
    nodes = []
    if index // 512 & 1:
        nodes.append((DATA + 0x200, 32))
    if left:
        nodes.append((DATA + 0x380, begin - (DATA + 0x380) - (16 if left_adjacent else 48)))
    if right:
        nodes.append((end + (0 if right_adjacent else 64), 64))
    nodes.append((DATA + 0xA00, 32))
    if index // 1024 & 1:
        nodes = []
    struct.pack_into('<III', page, heap - DATA - 4, flags, nodes[0][0] if nodes else 0, nodes[-1][0] if nodes else 0)
    struct.pack_into('<II', page, region - DATA, begin, end)
    for position, (address, size) in enumerate(nodes):
        previous = nodes[position - 1][0] if position else 0
        following = nodes[position + 1][0] if position + 1 < len(nodes) else 0
        struct.pack_into('<HHIII', page, address - DATA, 0x4652, 0, size, previous, following)
    expected = bytearray(page)
    combined_begin, combined_end, remaining = begin, end, list(nodes)
    patterns = [rng.getrandbits(32) for unused in range(3)]
    after = next((node for node in nodes if node[0] >= begin), None)
    if after and after[0] == end:
        combined_end = after[0] + 16 + after[1]
        remaining.remove(after)
        if flags & 2:
            expected[after[0] - DATA:after[0] - DATA + 16] = struct.pack('<I', patterns[0]) * 4
    before = [node for node in nodes if node[0] < begin]
    if before and before[-1][0] + 16 + before[-1][1] == begin:
        combined_begin = before[-1][0]
        remaining.remove(before[-1])
    success = combined_end - combined_begin >= 16
    if success:
        if flags & 2:
            expected[begin - DATA:end - DATA] = struct.pack('<I', patterns[2]) * (length // 4)
        remaining.append((combined_begin, combined_end - combined_begin - 16))
        remaining.sort()
    for position, (address, size) in enumerate(remaining):
        previous = remaining[position - 1][0] if position else 0
        following = remaining[position + 1][0] if position + 1 < len(remaining) else 0
        if success and address == combined_begin:
            struct.pack_into('<HHI', expected, address - DATA, 0x4652, 0, size)
        struct.pack_into('<II', expected, address - DATA + 8, previous, following)
    struct.pack_into('<II', expected, heap - DATA, remaining[0][0] if remaining else 0, remaining[-1][0] if remaining else 0)
    return rng, page, expected, heap, region, patterns, int(success)


def execute(original, code, index):
    rng, page, expected, heap, region, patterns, outcome = fixture(index)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, original)
    uc.mem_write(ENTRY, code)
    table = struct.unpack_from('<I', original, 0x2B9D8)[0]
    uc.mem_write(table, struct.pack('<III', *patterns))
    uc.mem_write(DATA, bytes(page))
    uc.mem_map(STACK, 4096)
    uc.mem_write(STACK, bytes([0xA5]) * 4096)
    uc.mem_map(STOP, 4096)
    control = 0x10 | (index % 4 << 6)
    uc.reg_write(UC_ARM_REG_CPSR, index % 16 << 28 | control)
    initial = [rng.getrandbits(32) for unused in REGISTERS]
    initial[:2], initial[-2:] = [heap, region], [STACK + 0x800, STOP | (index & 1)]
    for register, value in zip(REGISTERS, initial):
        uc.reg_write(register, value)
    stopped, active, returned, own = False, [], [], set()

    def instruction(engine, address, width, user):
        nonlocal stopped
        while active and active[-1][1] == address:
            returned.append(active.pop()[0])
        if address == STOP:
            stopped = True
            engine.emu_stop()
            return
        if address in HELPERS:
            active.append((address, engine.reg_read(REGISTERS[-1]) & ~1))
        if ENTRY <= address < ENTRY + len(code):
            own.add(address)
        else:
            assert any(a <= address < a + size for a, size in HELPERS.items()), hex(address)

    def memory(engine, access, address, width, value, user):
        assert DATA <= address and address + width <= DATA + 4096 or STACK + 0x700 <= address and address + width <= STACK + 0x800

    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_WRITE, memory)
    uc.emu_start(ENTRY, STOP + 4, count=20000)
    assert stopped and not active and uc.reg_read(REGISTERS[-2]) == STACK + 0x800
    assert all(uc.reg_read(REGISTERS[i]) == initial[i] for i in range(4, 12))
    assert uc.reg_read(UC_ARM_REG_CPSR) & 0xDF == control
    assert bytes(uc.mem_read(STACK, 0x700)) == bytes([0xA5]) * 0x700
    assert bytes(uc.mem_read(STACK + 0x800, 0x800)) == bytes([0xA5]) * 0x800
    actual, result = bytes(uc.mem_read(DATA, 4096)), uc.reg_read(REGISTERS[0])
    return dict(modelPassed=actual == bytes(expected) and result == outcome, result=result,
        backingSha256=hashlib.sha256(actual).hexdigest(), expectedBackingSha256=hashlib.sha256(expected).hexdigest(),
        actualReturns=1, actualHelperReturns=len(returned), suppliedCalls=0, observedOwnPcs=sorted(own))
