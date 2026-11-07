import struct


def half(data, offset):
    return struct.unpack_from('<H', data, offset)[0]


def word(data, offset):
    return struct.unpack_from('<I', data, offset)[0]


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
    nodes, unit = patricia(keys), len(values[0])
    entry, names = 8 + 4 * len(nodes), 4 + len(keys) * unit
    data = bytearray(entry + names + 16 * len(keys))
    struct.pack_into('<BBHHH', data, 0, 0, len(keys), len(data), 8, entry)
    for i, node in enumerate(nodes):
        struct.pack_into('<4B', data, 8 + i * 4, *node)
    struct.pack_into('<HH', data, entry, unit, names)
    for i, (key, value) in enumerate(zip(keys, values)):
        data[entry + 4 + i * unit:entry + 4 + (i + 1) * unit] = value
        data[entry + names + i * 16:entry + names + (i + 1) * 16] = key
    return bytes(data), entry + 4, entry + names


def named(prefix, index):
    return (prefix + str(index)).encode().ljust(16, b'\0')


def rotate(color, count):
    return color[count:] + color[:count]


def texture(count, fmt, bank, alpha):
    tv, pv, primary, secondary, palettes = [], [], bytearray(), bytearray(), bytearray()
    for i in range(count):
        tv.append(struct.pack('<II', (fmt << 26) | (alpha << 29) | (len(primary) // 8), 8 | (8 << 11)))
        pv.append(struct.pack('<HH', len(palettes) // 8, 0))
        base = ((31, 0, 0), (0, 31, 0), (0, 0, 31), (31, 31, 31)) if not bank else \
               ((0, 31, 31), (31, 0, 31), (31, 31, 0), (0, 0, 0))
        values = [rotate(value, i % 3) for value in base]
        values.extend([(0, 0, 0)] * ((256 if fmt == 4 else 16) - 4))
        palettes.extend(b''.join(struct.pack('<H', r | (g << 5) | (b << 10) | ((j & 1) << 15)) for j, (r, g, b) in enumerate(values)))
        if fmt == 3:
            primary.extend(bytes([0x10, 0x32, 0x10, 0x32]) * 8)
        elif fmt == 4:
            primary.extend(bytes([0, 1, 2, 3]) * 16)
        else:
            primary.extend(bytes([0xe4]) * 16)
            secondary.extend(b''.join(struct.pack('<H', ((j + i) & 3) << 14) for j in range(4)))
    td, unused, unused2 = dictionary([named('tex_', i) for i in range(count)], tv)
    pd, unused, unused2 = dictionary([named('palette_', i) for i in range(count)], pv)
    data = bytearray(60) + td + pd
    struct.pack_into('<H', data, 14, 60)
    struct.pack_into('<H', data, 52, 60 + len(td))
    for payload, position, size_position in ((primary, 36 if fmt == 5 else 20, 28 if fmt == 5 else 12),
            (secondary, 40, None), (palettes, 56, 48)):
        if payload:
            data.extend(bytes((-len(data)) % 8))
            struct.pack_into('<I', data, position, len(data))
            if size_position is not None:
                struct.pack_into('<H', data, size_position, len(payload) // 8)
            data.extend(payload)
    struct.pack_into('<II', data, 0, 0x30584554, len(data))
    return bytes(data)


def model_set(count):
    models, expected = [], []
    for mi in range(2):
        md, entries, unused = dictionary([named('mat_', i) for i in range(count)], [bytes(4)] * count)
        tx, te, unused = dictionary([named('tex_', i) for i in range(count)], [bytes(4)] * count)
        pl, pe, unused = dictionary([named('palette_', i) for i in range(count)], [bytes(4)] * count)
        material = bytearray(4) + md + tx + pl
        tb, pb = 4 + len(md), 4 + len(md) + len(tx)
        struct.pack_into('<HH', material, 0, tb, pb)
        assigned = [((i + mi + 1) % count, (count - 1 - i + mi) % count) for i in range(count)]
        for kind, base, entry in ((0, tb, te), (1, pb, pe)):
            for i in range(count):
                ids = bytes(j for j, pair in enumerate(assigned) if pair[kind] == i)
                struct.pack_into('<HBB', material, base + entry + i * 4, len(material), len(ids), 0)
                material.extend(ids)
        material.extend(bytes((-len(material)) % 4))
        for i, pair in enumerate(assigned):
            struct.pack_into('<I', material, 4 + entries + i * 4, len(material))
            record = bytearray(44)
            struct.pack_into('<H', record, 2, 44)
            struct.pack_into('<HH', record, 32, 8, 8)
            material.extend(record)
            expected.append((mi, i, *pair))
        mdl = bytearray(96) + material
        struct.pack_into('<I', mdl, 0, len(mdl))
        struct.pack_into('<I', mdl, 8, 96)
        models.append(mdl)
    table, entries, unused = dictionary([named('model_', i) for i in range(2)], [bytes(4)] * 2)
    result = bytearray(8) + table
    for i, mdl in enumerate(models):
        struct.pack_into('<I', result, 8 + entries + i * 4, len(result))
        result.extend(mdl)
    struct.pack_into('<II', result, 0, 0x304c444d, len(result))
    return bytes(result), expected


def file_block(signature, block):
    return struct.pack('<4sHHIHHI', signature, 0xfeff, 2 if signature == b'BMD0' else 1,
                       20 + len(block), 16, 1, 20) + block


def image(models, banks):
    names = [b'model.bin', b'bank-a.bin', b'bank-b.bin']
    fnt = struct.pack('<IHH', 8, 0, 1) + b''.join(bytes([len(name)]) + name for name in names) + b'\0'
    fat = (512 + len(fnt) + 3) & ~3
    payloads = [file_block(b'BMD0', models), *[file_block(b'BTX0', bank) for bank in banks]]
    data = bytearray(1024)
    struct.pack_into('<4I', data, 0x40, 512, len(fnt), fat, 24)
    data[512:512 + len(fnt)] = fnt
    for i, payload in enumerate(payloads):
        data.extend(bytes((-len(data)) % 4))
        start = len(data)
        data.extend(payload)
        struct.pack_into('<II', data, fat + i * 8, start, len(data))
    return bytes(data), payloads


def known_pixels(fmt, texture_index, palette_index, bank, alpha):
    red, green, blue, white, clear = (255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255), (255, 255, 255, 255), (0, 0, 0, 0)
    cyan, magenta, yellow, black = (0, 255, 255, 255), (255, 0, 255, 255), (255, 255, 0, 255), (0, 0, 0, 255)
    modes = ((red, green, blue, clear), (red, green, (123, 123, 0, 255), clear),
             (red, green, blue, white), (red, green, (156, 90, 0, 255), (90, 156, 0, 255))) if not bank else \
            ((cyan, magenta, yellow, clear), (cyan, magenta, (123, 123, 255, 255), clear),
             (cyan, magenta, yellow, black), (cyan, magenta, (90, 156, 255, 255), (156, 90, 255, 255)))
    output = bytearray()
    for y in range(8):
        for x in range(8):
            mode = ((y // 4) * 2 + x // 4 + texture_index) & 3 if fmt == 5 else 2
            value = modes[mode][x & 3]
            rgb = rotate(value[:3], palette_index % 3)
            a = 0 if fmt != 5 and alpha and not (x & 3) else value[3]
            output.extend((*rgb, a))
    return bytes(output)
