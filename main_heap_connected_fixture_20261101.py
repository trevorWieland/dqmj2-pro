import hashlib
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR

DATA, STACK, STOP, ENTRY = 0x02380000, 0x03030000, 0x0F000000, 0x0202AE9C
HELPERS = {0x0202AD78: 44, 0x0202ADA4: 40, 0x0202ADCC: 48,
           0x0202ADFC: 44, 0x02008C14: 20, 0x0202B9CC: 16}


def execute(original, code, index, search_entry, search_code):
    rng = random.Random(ENTRY * 10000 + index)
    page = bytearray(rng.randbytes(4096))
    heap, block = DATA + 0x40, DATA + 0x300 + index % 8 * 16
    capacity = 256 + index % 5 * 64
    gap = [0, 4, 16, 20, 28, 60, 124][index % 7]
    requested = [0, 4, 20, 64, 128, 640][index // 7 % 6]
    alignment = [1, 2, 4, 8, 16, 32, 64][index // 6 % 7]
    body = block + 16
    backwards = search_entry == 0x0202B0F8
    search_start = ((body + capacity - requested) & ~(alignment - 1)) if backwards else ((body + alignment - 1) & ~(alignment - 1))
    eligible = search_start >= body if backwards else search_start + requested <= body + capacity
    gap = search_start - body if eligible else 0
    start, end = block + 16 + gap, block + 16 + capacity
    used_end, header = start + requested, start - 16
    flags, group, direction = index // 35 % 4, rng.randrange(65536), int(backwards)
    old_used = DATA + 0xC00 if index & 1 else 0
    struct.pack_into('<IIIIIH', page, heap - DATA - 4, flags, block, block, old_used, old_used, group)
    struct.pack_into('<HHIII', page, block - DATA, 0x4652, 0, capacity, 0, 0)
    if old_used:
        struct.pack_into('<HHIII', page, old_used - DATA, 0x5544, 0, 64, 0, 0)
    struct.pack_into('<H', page, heap - DATA + 0x12, rng.randrange(65536))
    expected = bytearray(page)
    free = []
    fill_start = header if gap >= 20 else block
    if gap >= 20:
        free.append((block, header - block - 16))
    if end - used_end >= 20:
        free.append((used_end, end - used_end - 16))
    else:
        used_end = end
    pattern = rng.getrandbits(32)
    if flags & 3:
        word = struct.pack('<I', 0 if flags & 1 else pattern)
        for offset in range(fill_start - DATA, used_end - DATA, 4):
            expected[offset:offset + 4] = word
    for position, (node, size) in enumerate(free):
        previous = free[position - 1][0] if position else 0
        following = free[position + 1][0] if position + 1 < len(free) else 0
        struct.pack_into('<HHIII', expected, node - DATA, 0x4652, 0, size, previous, following)
    struct.pack_into('<II', expected, heap - DATA, free[0][0] if free else 0, free[-1][0] if free else 0)
    attributes = (direction & 1) << 15 | (header - fill_start & 127) << 8 | group & 255
    struct.pack_into('<HHIII', expected, header - DATA, 0x5544, attributes, used_end - header - 16, old_used, 0)
    struct.pack_into('<II', expected, heap - DATA + 8, old_used or header, header)
    if old_used:
        struct.pack_into('<I', expected, old_used - DATA + 12, header)
    if not eligible:
        expected = bytearray(page)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, original)
    uc.mem_write(ENTRY, code)
    uc.mem_write(search_entry, search_code)
    table = struct.unpack_from('<I', original, 0x2B9D8)[0]
    uc.mem_write(table + 4, struct.pack('<I', pattern))
    uc.mem_write(DATA, bytes(page))
    uc.mem_map(STACK, 4096)
    uc.mem_write(STACK, bytes([0xA5]) * 4096)
    uc.mem_write(STACK + 0x800, struct.pack('<I', direction))
    uc.mem_map(STOP, 4096)
    control = 0x10 | (index % 4 << 6)
    uc.reg_write(UC_ARM_REG_CPSR, index % 16 << 28 | control)
    initial = [rng.getrandbits(32) for unused in REGISTERS]
    initial[:4], initial[-2:] = [heap - 0x24, requested, alignment, rng.getrandbits(32)], [STACK + 0x800, STOP | (index & 1)]
    for register, value in zip(REGISTERS, initial):
        uc.reg_write(register, value)
    stopped, active, returns = False, [], []

    def instruction(engine, address, width, user):
        nonlocal stopped
        while active and active[-1][1] == address:
            returns.append(active.pop()[0])
        if address == STOP:
            stopped = True
            engine.emu_stop()
            return
        if address in HELPERS or address == ENTRY:
            active.append((address, engine.reg_read(REGISTERS[-1]) & ~1))
        assert ENTRY <= address < ENTRY + len(code) or search_entry <= address < search_entry + len(search_code) or any(a <= address < a + size for a, size in HELPERS.items()), hex(address)

    def memory(engine, access, address, width, value, user):
        assert DATA <= address and address + width <= DATA + 4096 or STACK + 0x700 <= address and address + width <= STACK + 0x800

    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_WRITE, memory)
    uc.emu_start(search_entry, STOP + 4, count=20000)
    assert stopped and not active and uc.reg_read(REGISTERS[-2]) == STACK + 0x800
    assert all(uc.reg_read(REGISTERS[i]) == initial[i] for i in range(4, 12))
    assert uc.reg_read(UC_ARM_REG_CPSR) & 0xDF == control
    assert bytes(uc.mem_read(STACK, 0x700)) == bytes([0xA5]) * 0x700
    assert bytes(uc.mem_read(STACK + 0x800, 4)) == struct.pack('<I', direction)
    assert bytes(uc.mem_read(STACK + 0x804, 0x7FC)) == bytes([0xA5]) * 0x7FC
    actual = bytes(uc.mem_read(DATA, 4096))
    result = uc.reg_read(REGISTERS[0])
    return dict(modelPassed=actual == bytes(expected) and result == (start if eligible else 0),
        actualReturns=1, actualHelperReturns=len(returns), helperReturns=[hex(a) for a in returns],
        result=result, backingSha256=hashlib.sha256(actual).hexdigest(), expectedBackingSha256=hashlib.sha256(expected).hexdigest(),
        flags=flags, requestedBytes=requested, gap=gap, group=group, direction=direction, alignment=alignment, eligible=eligible, backwards=backwards,
        suppliedCalls=0, existingUsedNode=bool(old_used))
