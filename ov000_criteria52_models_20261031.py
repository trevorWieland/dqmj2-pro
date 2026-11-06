import random
import struct

RECORDS, HEADERS, GROUPS = 0x0222BB18, 0x0222E32C, 0x0222FA10
MODE, GATES, SEEN = 0x02102DC0, 0x021C0E20, 0x021C0E68


def recipes():
    return [dict(seed=0x152000 + index, category=category, mode=mode, variant=variant, first=variant, second=variant + 2)
        for index, (category, mode, variant) in enumerate((category, mode, variant) for category in (0, 1, 16, 31)
            for mode in (0, 1, 2, 5, 255) for variant in range(2))]


def inputs(recipe, group_table):
    rng = random.Random(recipe['seed'])
    records = bytearray(rng.randbytes(768 * 12))
    gates = rng.getrandbits(64)
    seen = bytearray(rng.randbytes(96))
    wanted = 1 if recipe['category'] in (0, 16) else struct.unpack('<b', bytes([group_table[recipe['category']]]))[0]
    for index in range(768):
        group = wanted & 255 if index % 5 else (wanted + 1) & 255
        kind = (0, 1, 1, 3, 3, 3, 2, 255, 128)[index % 9]
        a, b = ((recipe['second'], 0), (recipe['first'], recipe['second']), (recipe['second'], recipe['first']),
            (-1, -1), (index % 64, -1), (index % 64, (index + 17) % 64), (0, 0), (0, 0), (0, 0))[index % 9]
        records[index * 12] = group
        records[index * 12 + 2] = kind
        struct.pack_into('<ii', records, index * 12 + 4, a, b)
    return bytes(records), gates.to_bytes(8, 'little'), bytes(seen)


def model(recipe, records, gate_bytes, seen_bytes, group_table):
    seen, changed = bytearray(seen_bytes), []
    if recipe['mode'] not in (1, 2, 5):
        return bytes(seen), changed
    wanted = 1 if recipe['category'] in (0, 16) else struct.unpack('<b', bytes([group_table[recipe['category']]]))[0]
    gates = int.from_bytes(gate_bytes, 'little')
    for index in range(768):
        if seen[index // 8] >> (index % 8) & 1:
            continue
        record = records[index * 12:index * 12 + 12]
        if record[0] != wanted:
            continue
        kind = struct.unpack('<b', record[2:3])[0]
        a, b = struct.unpack_from('<ii', record, 4)
        pair = kind == 1 and ((a, b) == (recipe['first'], recipe['second']) or (a, b) == (recipe['second'], recipe['first']))
        scalar = kind == 0 and a == recipe['second']
        gated = kind == 3 and (a == -1 or gates >> a & 1) and (b == -1 or gates >> b & 1)
        if pair or scalar or gated:
            seen[index // 8] |= 1 << (index % 8)
            changed.append(index)
    return bytes(seen), changed
