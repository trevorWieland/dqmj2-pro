import struct

ROWS, EKT, EKT_STATE, LOOKUP, WORDS = 0x021C3880, 0x02350000, 0x020F69EC, 0x022084F4, 0x0220860C


def recipes():
    return [dict(seed=0x191000 + mask * 8 + variant, enabledMask=mask, variant=variant)
        for mask in range(8) for variant in range(8)]


def model(recipe):
    categories = [(recipe['variant'] + i * 3) % 16 for i in range(6)]
    lookup = [-128, -1, 0, 1, 126, 127]
    count = recipe['enabledMask'].bit_count()
    initial = [(EKT_STATE + 4, struct.pack('<I', EKT)), (LOOKUP, bytes(value & 255 for value in lookup))]
    for i in range(6):
        initial.append((EKT + 100 * i + 4, struct.pack('<H', (categories[i] << 8) | 0xA055)))
    for i in range(3):
        initial.extend([(ROWS + 132 * i + 20, struct.pack('<I', 0xFFFFFFFF if recipe['enabledMask'] >> i & 1 else 0)),
            (ROWS + 132 * i + 24, struct.pack('<h', i))])
    words = [0xFA000000 | recipe['seed'] + i for i in range(11)]
    initial += [(WORDS + 8 * i, struct.pack('<I', value)) for i, value in enumerate(words)]
    calls, total = [], 0
    for i in range(count):
        offset = lookup[categories[i] // 3] + total * 5 + 10
        writes = [(ROWS + 132 * i + 24, struct.pack('<h', i + 3))]
        writes += [(ROWS + 132 * j + 20, struct.pack('<I', 0 if recipe['enabledMask'] >> j & 1 else 0xFFFFFFFF)) for j in range(3)]
        calls.append(dict(address=0x021E7F08, arguments=[7, 9, offset & 0xFFFFFFFF], writes=writes))
        for unused in range(categories[i + 3] // 3 + 1):
            coordinate = 8 + total * 5
            calls.append(dict(address=0x021E7F08, arguments=[0, 3, coordinate], writes=[]))
            calls.append(dict(address=0x021E7F08, arguments=[total + 1, 3, coordinate], writes=[]))
            total += 1
    for i in range(11):
        writes = []
        if i < 10:
            words[i + 1] = 0xCD000000 | i << 16 | recipe['seed'] & 0xFFFF
            writes.append((WORDS + 8 * (i + 1), struct.pack('<I', words[i + 1])))
        calls.append(dict(address=0x021E7608, arguments=[words[i]], writes=writes))
    return initial, calls, 4 + count * 4
