import struct


def patricia(keys):
    nodes = [[127, 0, 0, 0]]
    def bit(key, position):
        return (key[position // 8] >> (position % 8)) & 1
    for index, key in enumerate(keys):
        if not index:
            nodes.append([0, 1, 1, 0])
            nodes[0][1] = 1
            continue
        parent, current = 0, nodes[0][1]
        while nodes[parent][0] > nodes[current][0]:
            parent, current = current, nodes[current][1 + bit(key, nodes[current][0])]
        other = keys[nodes[current][3]]
        difference = max(i for i in range(128) if bit(key, i) != bit(other, i))
        parent, current = 0, nodes[0][1]
        while nodes[parent][0] > nodes[current][0] and nodes[current][0] > difference:
            parent, current = current, nodes[current][1 + bit(key, nodes[current][0])]
        fresh, direction = len(nodes), bit(key, difference)
        nodes.append([difference, current if direction else fresh, fresh if direction else current, index])
        nodes[parent][1 if not parent else 1 + bit(key, nodes[parent][0])] = fresh
    return nodes


def dictionary(keys, values):
    unit = len(values[0])
    nodes = patricia(keys)
    entry = (8 + 4 * len(nodes) + 15) & ~15
    names = (4 + unit * len(keys) + 15) & ~15
    data = bytearray(entry + names + len(keys) * 16)
    struct.pack_into('<BBHHH', data, 0, 0, len(keys), len(data), 0, entry)
    for i, node in enumerate(nodes):
        struct.pack_into('<4B', data, 8 + 4 * i, *node)
    struct.pack_into('<HH', data, entry, unit, names)
    for i, (key, value) in enumerate(zip(keys, values)):
        data[entry + 4 + unit * i:entry + 4 + unit * (i + 1)] = value
        data[entry + names + 16 * i:entry + names + 16 * (i + 1)] = key
    return bytes(data), entry + 4, entry + names


def texture(count, format_code, variant):
    keys = [f'material_{i:03}'.encode().ljust(16, b'\0') for i in range(count)]
    tex_values, palette_values = [], []
    for i in range(count):
        param = (((format_code + i) & 7) << 26) | ((i * 37 + 41) & 0xffff)
        extra = ((0, 1, 128, 2047)[(format_code + i) & 3] |
                 ((2047, 128, 1, 0)[(format_code + i) & 3] << 11) | 0xa0000000)
        tex_values.append(struct.pack('<II', param, extra))
        palette_values.append(struct.pack('<HH', 0xffff - i, 0xa550 | ((format_code + i) & 1)))
    tex, entry, names = dictionary(keys, tex_values)
    palette, unused_entry, unused_names = dictionary(keys, palette_values)
    data = bytearray(60) + tex + palette
    key_values = (0x91be0000, 0xdeadffff, 0x12341234)
    struct.pack_into('<II', data, 0, 0x30584554, len(data))
    for offset, value in ((8, key_values[variant]), (24, key_values[(variant + 1) % 3]), (44, key_values[variant])):
        struct.pack_into('<I', data, offset, value)
    struct.pack_into('<H', data, 52, 60 + len(tex))
    return bytes(data), keys, tex_values, palette_values, 60 + entry, 60 + names


def image(material):
    root = bytes([8]) + b'root.bin' + bytes([5]) + b'empty' + bytes([0x84]) + b'data' + struct.pack('<H', 0xf001) + b'\0'
    child = bytes([12]) + b'material.bin' + b'\0'
    fnt = struct.pack('<IHHIHH', 16, 2, 2, 16 + len(root), 4, 0xf000) + root + child
    fat = (512 + len(fnt) + 3) & ~3
    root_data = bytes((i * 37 + 11) & 255 for i in range(513))
    start = 1024 + len(root_data) + 7
    data = bytearray(start + len(material))
    struct.pack_into('<4I', data, 0x40, 512, len(fnt), fat, 40)
    data[512:512 + len(fnt)] = fnt
    ranges = [(0, 0), (0, 0), (1024, 1024 + len(root_data)), (0, 0), (start, start + len(material))]
    for i, pair in enumerate(ranges):
        struct.pack_into('<II', data, fat + i * 8, *pair)
    data[1024:1024 + len(root_data)], data[start:] = root_data, material
    return bytes(data), ranges, root_data


def material_result(initial, tex_value, palette_value, keys):
    result = bytearray(initial)
    param, extra = struct.unpack('<II', tex_value)
    key = keys[1 if (param & 0x1c000000) == 0x14000000 else 0] & 0xffff
    before = struct.unpack_from('<I', result, 16)[0]
    struct.pack_into('<I', result, 16, (before & 0xc00f0000) | ((param + key) & 0xffffffff))
    struct.pack_into('<HHII', result, 44, extra & 0x7ff, (extra >> 11) & 0x7ff, 4096, 4096)
    texture_result = bytes(result)
    base, flag = struct.unpack('<HH', palette_value)
    shift = 0 if flag & 1 else 1
    struct.pack_into('<I', result, 20, (base >> shift) + ((keys[2] & 0xffff) >> shift))
    return texture_result, bytes(result)
