import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE, DATA, STACK, STOP = 0x02000000, 0x02400000, 0x03030000, 0x0F000000
OWN = {0x0202EA64: 104, 0x0202FA04: 104, 0x0202EBC0: 84}
HELPERS = {0x0202EB4C: 116}
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
    UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
    UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def inputs(index):
    rng = random.Random(0x292000 + index)
    page = bytearray(rng.randbytes(65536))
    expected = bytearray(page)
    entry = list(OWN)[index % 3]
    counts = [0, 1, 2, 31, 32, 33, 63, 64, 127, 128, 255]
    if entry != 0x0202EBC0:
        length = [0, 1, 2, 4, 7][index // 3 % 5]
        nodes = [0x2000 + i * 0x400 for i in range(length)]
        words = [0 if index // 15 % 3 == 0 else 0xFFFFFFFF if index // 15 % 3 == 1 else rng.getrandbits(32)
            for _ in range(8)]
        struct.pack_into('<8I', page, 0x200, *words)
        maps = []
        for i, node in enumerate(nodes):
            count = counts[(index // 45 + i) % len(counts)]
            struct.pack_into('<I', page, node + 16, DATA + nodes[i + 1] if i + 1 < length else 0)
            page[node + 27] = count
            values = [rng.getrandbits(16) for _ in range(count)]
            for j, value in enumerate(values): struct.pack_into('<H', page, node + 28 + j * 2, value)
            maps.append(values)
        expected = bytearray(page)
        for values in maps:
            for bit, value in enumerate(values):
                if value & 0x100: words[bit // 32] |= 1 << (bit % 32)
        struct.pack_into('<8I', expected, 0x200, *words)
        return page, bytes(expected), entry, [DATA + 0x200, DATA + nodes[0] if nodes else 0], dict(length=length, mapCounts=[len(v) for v in maps], initialVectorKind=index // 15 % 3)
    groups = []
    for group in range(3):
        length = [0, 1, 2, 4, 7][(index // 3 + group) % 5]
        nodes = [0x2000 + (group * 7 + i) * 0x400 for i in range(length)]
        for i, node in enumerate(nodes):
            struct.pack_into('<I', page, node + 16, DATA + nodes[i + 1] if i + 1 < length else 0)
        struct.pack_into('<I', page, 0x100 + 8 + group * 8, DATA + nodes[0] if nodes else 0)
        groups.append(nodes)
    kind = index // 15 % 7
    target = [0xE000, 0, 0xFFFFFFFF, 0x0240FFFE][max(0, kind - 3)] if kind >= 3 else (
        DATA + groups[kind][index // 105 % len(groups[kind])] if groups[kind] else DATA + 0xE000)
    expected = bytearray(page)
    removed = False
    for group, nodes in enumerate(groups):
        if target - DATA not in nodes: continue
        position = nodes.index(target - DATA)
        following = DATA + nodes[position + 1] if position + 1 < len(nodes) else 0
        destination = 0x100 + 8 + group * 8 if position == 0 else nodes[position - 1] + 16
        struct.pack_into('<I', expected, destination, following)
        struct.pack_into('<I', expected, target - DATA + 16, 0)
        flags = struct.unpack_from('<I', page, 0x100)[0]
        struct.pack_into('<I', expected, 0x100, flags | 16)
        removed = True
        break
    return page, bytes(expected), entry, [DATA + 0x100, target], dict(groupLengths=[len(v) for v in groups],
        targetKind=kind, target=target, removed=removed)


def execute(image, bodies, index, bound=20000):
    page, expected, entry, args, context = inputs(index)
    rng = random.Random(0x436F000 + index)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE, 0x100000)
    machine.mem_write(BASE, image)
    for address, body in bodies.items():
        machine.mem_write(address, body)
    machine.mem_map(DATA, 65536)
    machine.mem_write(DATA, bytes(page))
    machine.mem_map(STACK, 8192)
    machine.mem_write(STACK, rng.randbytes(8192))
    machine.mem_map(STOP, 4096)
    machine.reg_write(UC_ARM_REG_CPSR, 0x10 | (index % 16 << 28))
    for reg in REGS:
        machine.reg_write(reg, rng.getrandbits(32))
    for reg, value in zip(REGS, args):
        machine.reg_write(reg, value)
    machine.reg_write(UC_ARM_REG_SP, STACK + 4096)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    spans = {**OWN, **HELPERS, **{a: len(b) for a, b in bodies.items()}}
    seen, reads, writes, pending, calls = set(), [], [], [], []
    returned, nested, helpers = False, 0, 0
    def code(uc, address, size, user):
        nonlocal returned, nested, helpers
        if pending and address == pending[-1][0]:
            _, kind = pending.pop()
            if kind == 'own': nested += 1
            else: helpers += 1
        if address == STOP:
            assert not pending
            returned = True
            uc.emu_stop()
            return
        assert any(a <= address < a + n for a, n in spans.items()), hex(address)
        if address in spans:
            calls.append(dict(address=address, args=[uc.reg_read(r) for r in REGS[:4]]))
            if address != entry:
                pending.append((uc.reg_read(UC_ARM_REG_LR), 'own' if address in OWN else 'helper'))
        if any(a <= address < a + n for a, n in OWN.items()): seen.add(address)
    def read(uc, access, address, size, value, user):
        reads.append((address, size, bytes(uc.mem_read(address, size)).hex()))
    def write(uc, access, address, size, value, user):
        assert DATA <= address and address + size <= DATA + 65536 or STACK <= address and address + size <= STACK + 8192
        writes.append((address, size, value & ((1 << (size * 8)) - 1)))
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_READ, read)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(entry, STOP + 4, count=bound)
    assert returned and machine.reg_read(UC_ARM_REG_SP) == STACK + 4096, ('no actual return', index)
    output = bytes(machine.mem_read(DATA, 65536))
    for address, body in bodies.items():
        machine.mem_write(address, image[address - BASE:address - BASE + len(body)])
    assert bytes(machine.mem_read(BASE, len(image))) == image
    return dict(index=index, context=context, actualReturn=True, modelPassed=output == expected,
        registers=[machine.reg_read(r) for r in [*REGS, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC]],
        cpsr=machine.reg_read(UC_ARM_REG_CPSR), dataSha256=hashlib.sha256(output).hexdigest(),
        stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK, 8192))).hexdigest(),
        reads=reads, writes=writes, calls=calls, ownObserved=sorted(seen),
        actualSelectedNestedReturns=nested, actualNativeHelperReturns=helpers, providers=0)
