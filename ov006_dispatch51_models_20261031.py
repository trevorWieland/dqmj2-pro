import struct

STATE, OUTPUT, TABLE = 0x0221C06C, 0x0221C098, 0x0220DA64
REG_A, REG_B, NEXT = 0x0400100A, 0x0400000A, 0x021F59D9
CALLBACKS = [(0x0220DAB8, 0x02004F78), (0x0220DACC, 0x020048F4), (0x0220DAE0, 0x02004B00),
    (0x0220DAF8, 0x020049A4), (0x0220DB10, 0x02004FD8), (0x0220DB28, 0x020048A0),
    (0x0220DB40, 0x02004AA8), (0x0220DB58, 0x0200494C)]


def recipes():
    return [dict(seed=0x151000 + len_index, selector=selector, flags=flags, objectWord=(0xF00D0011 + len_index * 0x12345) & 0xFFFFFFFF,
        handles=[(0x12345678 + len_index) & 0xFFFFFFFF, (0xFFFFFFFF - len_index) & 0xFFFFFFFF])
        for len_index, (selector, flags) in enumerate((selector, flags) for selector in range(7)
            for flags in (0, 1, 2, 15, 0x20, 0x21, 0xFFFFFFFF))]


def protocol(recipe, table):
    calls = [dict(address=a, arguments=[], result=0x80000000 | index) for index, a in enumerate((0x021FED84, 0x021F5394, 0x021F2920, 0x021F2A74, 0x021F26E4))]
    choice = 0x0220DA80 if recipe['selector'] == 1 and recipe['flags'] & 0x20 else table[recipe['selector']]
    calls.append(dict(address=0x021F53C8, arguments=[choice], result=recipe['objectWord']))
    for index, descriptor in enumerate((0x0220DA90, 0x0220DAA4)):
        calls.append(dict(address=0x021F2798, arguments=[descriptor], result=recipe['handles'][index]))
        calls.append(dict(address=0x02202FB8, arguments=[1 - index, recipe['handles'][index]], result=0x70000000 | index))
    callbacks = CALLBACKS + ([(0x0220DB70 if recipe['flags'] & 15 == 0 else 0x0220DB84, 0x02004C78)] if recipe['flags'] & 15 in (0, 1) else [])
    calls.extend(dict(address=0x021F27D4, arguments=list(pair), result=0x60000000 | index) for index, pair in enumerate(callbacks))
    return calls


def expected(recipe, initial_ram, initial_io):
    ram, io = bytearray(initial_ram), bytearray(initial_io)
    ram[STATE - 0x02000000] = recipe['selector']
    struct.pack_into('<I', ram, STATE - 0x02000000 + 8, recipe['flags'])
    struct.pack_into('<I', ram, STATE - 0x02000000 + 12, NEXT)
    struct.pack_into('<I', ram, OUTPUT - 0x02000000, recipe['objectWord'])
    for address in (REG_A, REG_B):
        offset = address - 0x04000000
        struct.pack_into('<H', io, offset, struct.unpack_from('<H', io, offset)[0] | 3)
    for offset in (0, 0x1000):
        struct.pack_into('<I', io, offset, struct.unpack_from('<I', io, offset)[0] | 0x200)
    return ram, io
