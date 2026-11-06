import struct

STATE = 0x021E9818


def recipes():
    result = []
    for scroll in (0, 1, 255, 256, 511, 512, 0xFFFFFFFF, 0x80000000, 0x7FFFFFFF):
        for mode in (0, 1, 2, 0xFFFFFFFF):
            for flag in (0, 1, 2, 0xFFFFFFFF):
                result.append(dict(seed=0x520000 + len(result), scroll=scroll, mode=mode, flag=flag,
                    objectType=(0, 2, 0xFFFFFFFF)[len(result) % 3]))
    return result


def model(recipe, initial_ram, initial_io):
    ram, io, writes, io_writes = bytearray(initial_ram), bytearray(initial_io), [], []

    def word(address, value):
        value &= 0xFFFFFFFF
        struct.pack_into('<I', ram, address - 0x02000000, value)
        writes.append((address, 4, value))

    def flags(address, enabled):
        value = struct.unpack_from('<I', ram, address - 0x02000000)[0]
        word(address, value | 2 if enabled else value & ~2)

    def position(address, x, y):
        word(address + 0x6C, x)
        word(address + 0x70, y)

    scroll = recipe['scroll'] & 511
    for address in (0x04000010, 0x04000014, 0x0400001C):
        struct.pack_into('<I', io, address - 0x04000000, scroll)
        io_writes.append((address, 4, scroll))
    word(STATE + 0x2C, scroll)
    flags(0x021E9B48 + 0x7C, recipe['flag'] == 1)
    if recipe['mode'] == 1:
        value = struct.unpack_from('<I', io, 0)[0] & ~0x1F00 | 0x1400
        struct.pack_into('<I', io, 0, value)
        io_writes.append((0x04000000, 4, value))
        scroll = 256
        word(STATE + 0x2C, scroll)
        position(0x021E9EA8, 0x80, 0x80)
        flags(0x021E9A28 + 0x7C, False)
    else:
        position(0x021E9EA8, 0xD0 - scroll, 0xB8)
    position(0x021E9CF8, 0x80 - scroll, 0x60)
    position(0x021E9BD8, 0x80 - scroll, 0x60)
    position(0x021E9AB8, 0x80 - scroll, 0x50)
    for index in range(3):
        for base, y in [(0x021EA298, 0x38), (0x021EA0E8, 0x34), (0x021E9F38, 0x34)]:
            position(base + index * 0x90, 0x10 + index * 0x30 - scroll, y)
    return dict(ram=bytes(ram), io=bytes(io), nativeRamWrites=writes, nativeIoWrites=io_writes,
                returnWord=0x021E9F38 + 2 * 0x90)
