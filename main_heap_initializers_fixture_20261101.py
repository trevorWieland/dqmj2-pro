import hashlib
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from main_list_unlink_fixture_20261101 import REGS

DATA, GLOBAL, STACK, STOP = 0x02380000, 0x020ED000, 0x027F0000, 0x027FF000
HEADER, EXP = 0x0202B914, 0x0202AE28
ENTRIES = {HEADER: 160, EXP: 116}
HELPERS = {HEADER: 160, EXP: 116, 0x0202ADFC: 44, 0x0202B9CC: 16,
           0x0202B9DC: 24, 0x0202B8EC: 40, 0x0202B884: 104,
           0x0202BA20: 84, 0x0202B9F4: 44, 0x0202BB88: 24, 0x02008C14: 20}


def scenario(image, entry, index):
    rng = random.Random(entry * 100000 + index)
    pages = [bytearray(rng.randbytes(4096)) for unused in range(2)]
    heap = DATA + 0x500
    flags = [0, 1, 2, 3, 0x80, 0xFF, 0x100, 0x102, 0xFFFF, 0xFFFFFFFF][index // 6 % 10]
    initialized = [0, 1, 0x100, 0x80000000][index // 60 % 4]
    shape = index % 6 if initialized else 0
    span = [20, 24, 64, 256, 512][index // 240 % 5]
    start = heap + (0x38 if entry == EXP else 0x24)
    end = start + span
    signature = 0x45585048 if entry == EXP else [0, 0x46524D48, 0xFFFFFFFF, rng.getrandbits(32)][index % 4]

    def put(page, offset, value, half=False):
        struct.pack_into('<H' if half else '<I', page, offset, value)

    def initial_list(address, objects):
        page = pages[1] if address >= GLOBAL and address < GLOBAL + 4096 else pages[0]
        offset = address - (GLOBAL if page is pages[1] else DATA)
        put(page, offset, objects[0] if objects else 0)
        put(page, offset + 4, objects[-1] if objects else 0)
        put(page, offset + 8, len(objects), True)
        put(page, offset + 10, 4, True)
        for slot, obj in enumerate(objects):
            put(pages[0], obj - DATA + 4, objects[slot - 1] if slot else 0)
            put(pages[0], obj - DATA + 8, objects[slot + 1] if slot + 1 < len(objects) else 0)

    def existing(obj, begin, finish):
        put(pages[0], obj - DATA + 0x18, begin)
        put(pages[0], obj - DATA + 0x1C, finish)
        initial_list(obj + 0xC, [])

    root = GLOBAL + 0xF78
    target = root
    roots = []
    if shape in [1, 2, 4]:
        parent = DATA + 0x100
        existing(parent, DATA + 0x200, DATA + 0xF00)
        roots = [parent]
        target = parent + 0xC
        if shape == 2:
            child = DATA + 0x300
            existing(child, DATA + 0x400, DATA + 0xE00)
            initial_list(parent + 0xC, [child])
            target = child + 0xC
        elif shape == 4:
            child = DATA + 0x380
            existing(child, DATA + 0x3C0, DATA + 0x480)
            initial_list(parent + 0xC, [child])
    elif shape == 3:
        first, second = DATA + 0x100, DATA + 0x300
        existing(first, DATA + 0x200, DATA + 0x280)
        existing(second, DATA + 0x400, DATA + 0xF00)
        roots = [first, second]
        target = second + 0xC
    elif shape == 5:
        parent = DATA + 0x100
        existing(parent, DATA + 0x200, DATA + 0x300)
        roots = [parent]
    initial_list(root, roots)
    put(pages[1], 0xF74, initialized)
    expected = [bytearray(page) for page in pages]
    put(expected[0], 0x500, signature)
    put(expected[0], 0x518, start)
    put(expected[0], 0x51C, end)
    put(expected[0], 0x520, flags & 255)
    if flags & 2:
        fill = image[0x020DD588 - 0x02000000:0x020DD58C - 0x02000000]
        expected[0][start - DATA:end - DATA] = fill * (span // 4)
    for offset in [0x50C, 0x510]:
        put(expected[0], offset, 0)
    put(expected[0], 0x514, 0, True)
    put(expected[0], 0x516, 4, True)
    if not initialized:
        put(expected[1], 0xF74, 1)
        for offset in [0xF78, 0xF7C]:
            put(expected[1], offset, 0)
        put(expected[1], 0xF80, 0, True)
        put(expected[1], 0xF82, 4, True)
    page = expected[1] if target == root else expected[0]
    offset = target - (GLOBAL if target == root else DATA)
    old_tail = struct.unpack_from('<I', page, offset + 4)[0]
    put(expected[0], 0x504, old_tail)
    put(expected[0], 0x508, 0)
    if old_tail:
        put(expected[0], old_tail - DATA + 8, heap)
    else:
        put(page, offset, heap)
    put(page, offset + 4, heap)
    count = struct.unpack_from('<H', page, offset + 8)[0]
    put(page, offset + 8, (count + 1) & 0xFFFF, True)
    if entry == EXP:
        put(expected[0], 0x534, 0, True)
        put(expected[0], 0x536, 0, True)
        put(expected[0], start - DATA, 0x4652, True)
        put(expected[0], start - DATA + 2, 0, True)
        put(expected[0], start - DATA + 4, span - 16)
        put(expected[0], start - DATA + 8, 0)
        put(expected[0], start - DATA + 12, 0)
        for offset in [0x524, 0x528]:
            put(expected[0], offset, start)
        for offset in [0x52C, 0x530]:
            put(expected[0], offset, 0)
    registers = [rng.getrandbits(32) for unused in REGS]
    registers[:4] = [heap, signature, start, end] if entry == HEADER else [heap, end, flags, registers[3]]
    return pages, expected, registers, flags, heap, rng


def execute(image, entry, replacements, index, bound=20000, require_model=True):
    pages, expected, initial, flags, heap, rng = scenario(image, entry, index)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_write(0x02000000, image)
    for address, body in replacements.items():
        machine.mem_write(address, body)
    for address, page in zip([DATA, GLOBAL], pages):
        machine.mem_write(address, bytes(page))
    guards = bytearray(rng.randbytes(8192))
    if entry == HEADER:
        struct.pack_into('<I', guards, 4096, flags)
    machine.mem_write(STACK - 4096, bytes(guards))
    cpsr = ((index % 16) << 28) | 0x10 | ((index // 2 % 4) << 6)
    machine.reg_write(UC_ARM_REG_CPSR, cpsr)
    for register, value in zip(REGS, initial):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, writes, pending, returned, own, lower = [], [], [], [], set(), set()

    def code(uc, address, size, unused):
        if pending and address == pending[-1][1]:
            returned.append(pending.pop()[0])
        if entry <= address < entry + len(replacements.get(entry, image[entry - 0x02000000:entry - 0x02000000 + ENTRIES[entry]])):
            own.update(range(address, address + size))
            return
        for helper, length in HELPERS.items():
            if helper <= address < helper + len(replacements.get(helper, bytes(length))):
                lower.update(range(address, address + size))
                if address == helper:
                    calls.append([helper, [uc.reg_read(register) for register in REGS[:4]]])
                    pending.append((helper, uc.reg_read(UC_ARM_REG_LR)))
                return
        raise AssertionError(('Unexpected native instruction', hex(address)))

    def write(uc, access, address, size, value, unused):
        if STACK - 4096 <= address and address + size <= STACK + 4096:
            return
        assert any(start <= address and address + size <= start + 4096 for start in [DATA, GLOBAL])
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(entry, STOP, timeout=2000000, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP and not pending
    assert machine.reg_read(UC_ARM_REG_SP) == STACK
    assert [machine.reg_read(register) for register in REGS[4:12]] == initial[4:12]
    assert machine.reg_read(UC_ARM_REG_CPSR) & 0xFF == cpsr & 0xFF
    assert bytes(machine.mem_read(STACK - 4096, 256)) == guards[:256]
    assert bytes(machine.mem_read(STACK + 4096 - 256, 256)) == guards[-256:]
    actual = [bytes(machine.mem_read(address, 4096)) for address in [DATA, GLOBAL]]
    result = machine.reg_read(UC_ARM_REG_R0)
    passed = actual == expected and (entry == HEADER or result == heap)
    if require_model:
        assert passed, (hex(entry), index, result, [a == b for a, b in zip(actual, expected)])
    record = dict(index=index, modelPassed=passed, result=result, calls=calls, writes=writes,
                  pagesSha256=hashlib.sha256(b''.join(actual)).hexdigest(), actualTopReturns=1,
                  suppliedCalls=0, actualNativeDependencyReturns=len(returned), returnedHelpers=returned,
                  observed=sorted(own), helperObserved=sorted(lower),
                  stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK - 4096, 8192))).hexdigest(),
                  registers=[machine.reg_read(register) for register in REGS], cpsr=machine.reg_read(UC_ARM_REG_CPSR))
    del machine
    return record
