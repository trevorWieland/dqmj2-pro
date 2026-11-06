import hashlib
import random
import struct
import match_runtime
from main_resource_dictionary_fixture_v4_20261101 import patricia
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE, DATA, STACK, STOP = 0x02000000, 0x02400000, 0x03030000, 0x0F000000
OWN = {0x02034248: 216, 0x02034320: 104, 0x02034388: 116}
HELPERS = {0x0202BBB4: 448, 0x0202BF88: 44, 0x0202BFB4: 44,
    0x0202BFE0: 116, 0x0202C054: 52}
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
    UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
    UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def dictionary(page, offset, names, values, stride):
    entry, names_offset = 0x100, (4 + len(names) * stride + 15) & ~15
    struct.pack_into('<BBHHH', page, offset, 0, len(names), entry + names_offset + len(names) * 16, 0, entry)
    for i, node in enumerate(patricia(names)):
        struct.pack_into('<4B', page, offset + 8 + 4 * i, *node)
    struct.pack_into('<HH', page, offset + entry, stride, names_offset)
    for i, (name, value) in enumerate(zip(names, values)):
        page[offset + entry + 4 + i * stride:offset + entry + 4 + (i + 1) * stride] = value
        page[offset + entry + names_offset + i * 16:offset + entry + names_offset + (i + 1) * 16] = name


def inputs(index):
    rng = random.Random(0x436000 + index)
    page = bytearray(rng.randbytes(65536))
    entry = list(OWN)[index % 3]
    count = [1, 2, 7, 15, 16, 31][index // 3 % 6]
    texture, result, animation, obj = 0x1000, 0x200, 0x5000, 0x600
    names = [bytes([i]) + bytes.fromhex('123456789abcdef00123456789abcd') for i in range(count)]
    tex_values = [(rng.getrandbits(32) & ~0x1C000000) | ((index + i) % 8 << 26) for i in range(count)]
    extras = [rng.getrandbits(32) for _ in range(count)]
    palettes = [(rng.randrange(65536), rng.randrange(65536)) for _ in range(count)]
    dictionary(page, texture + 60, names, [struct.pack('<II', a, b) for a, b in zip(tex_values, extras)], 8)
    dictionary(page, texture + 0x800, names, [struct.pack('<HH', *p) for p in palettes], 4)
    keys = [rng.getrandbits(32) for _ in range(3)]
    struct.pack_into('<I', page, texture + 8, keys[0])
    struct.pack_into('<I', page, texture + 24, keys[1])
    struct.pack_into('<I', page, texture + 44, keys[2])
    struct.pack_into('<H', page, texture + 52, 0x800)
    chosen = index // 18 % count
    query = rng.randrange(64)
    frame_count = [1, 2, 7, 16, 31][index // 108 % 5]
    times = [i * 2 for i in range(frame_count)]
    selected = max((i for i, time in enumerate(times) if time <= query), default=0)
    frames = [(time, (chosen + i) % count, 255 if (index + i) % 3 == 0 else (chosen + 2 * i) % count)
        for i, time in enumerate(times)]
    frame_array = 0x6000
    for i, record in enumerate(frames):
        struct.pack_into('<HBB', page, frame_array + i * 4, *record)
    item = index // 540 % 3
    dictionary(page, animation + 12, names[:3] if count >= 3 else [bytes([i]) + names[0][1:] for i in range(3)],
        [struct.pack('<HHhH', frame_count, 0, 0, frame_array - animation)] * 3, 8)
    struct.pack_into('<HH', page, animation + 4, 64, count | count << 8)
    struct.pack_into('<HH', page, animation + 8, 0x800, 0xA00)
    for i, name in enumerate(names):
        page[animation + 0x800 + i * 16:animation + 0x800 + (i + 1) * 16] = name
        page[animation + 0xA00 + i * 16:animation + 0xA00 + (i + 1) * 16] = name
    struct.pack_into('<iII', page, obj, query << 12 | rng.randrange(4096), rng.getrandbits(32), DATA + animation)
    struct.pack_into('<I', page, obj + 20, DATA + texture)
    page[0x100:0x110] = names[chosen]
    args = [DATA + texture, DATA + 0x100, DATA + result]
    tex_index, pal_index = chosen, chosen
    if entry == 0x02034388:
        tex_index, pal_index = frames[selected][1:]
        args = [DATA + result, DATA + obj, item | (rng.getrandbits(16) << 16)]
    expected = bytearray(page)
    if entry != 0x02034320:
        param = tex_values[tex_index]
        base = keys[1 if param >> 26 & 7 == 5 else 0] & 65535
        previous = struct.unpack_from('<I', page, result + 16)[0]
        struct.pack_into('<I', expected, result + 16, (previous & 0xC00F0000) | ((param + base) & 0xFFFFFFFF))
        extra = extras[tex_index]
        struct.pack_into('<HHii', expected, result + 44, extra & 2047, extra >> 11 & 2047, 4096, 4096)
    if entry == 0x02034320 or entry == 0x02034388 and pal_index != 255:
        offset, flag = palettes[pal_index]
        base = keys[2] & 65535
        if not flag & 1:
            offset >>= 1
            base >>= 1
        struct.pack_into('<I', expected, result + 20, offset + base)
    return page, bytes(expected), entry, args, dict(count=count, chosen=chosen, query=query,
        frameCount=frame_count, selectedFrame=selected, textureIndex=tex_index, paletteIndex=pal_index,
        textureKeys=keys, dataIndex=item)


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
