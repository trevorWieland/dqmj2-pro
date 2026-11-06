import struct

CONTEXTS = {'statea': (0x0223989C, 0x88), 'stateb': (0x0223E088, 0x30)}
RECORD = 0x02360000
WIDE = [0, 1, 0x80000000, 0xFFFFFFFF]


def recipes(kind):
    phases = (0, 10, 100, 255) if kind == 'statea' else (0, 10, 20, 30, 100, 255)
    counters = (0, 39, 40, 41, 254, 255) if kind == 'statea' else (0, 44, 45, 46, 254, 255)
    variants = range(9) if kind == 'statea' else range(6)
    cases = [dict(seed=0x203000 + i, phase=p, counter=c, variant=v)
        for i, (p, c, v) in enumerate((p, c, v) for p in phases for c in counters for v in variants)]
    for i, row in enumerate(cases):
        row.update(side=(0, 1, 2, 3, 255)[i % 5], slot=(0, 1, 2, 3, 4, 255)[i % 6], nativeId=(0, 1, 47, 255)[i % 4])
    return cases


def initialize(kind, recipe, initial):
    result = bytearray(initial)
    if kind == 'statea':
        result[0x3E], result[0x3D], result[0x10] = recipe['phase'], recipe['counter'], (0, 1, 255)[recipe['variant'] // 3]
        struct.pack_into('<H', result, 0x50, (0, 511, 65535)[recipe['variant'] % 3])
        struct.pack_into('<II', result, 0x80, WIDE[recipe['variant'] % 4], WIDE[(recipe['variant'] + 1) % 4])
    else:
        for offset, key in [(10, 'phase'), (9, 'counter'), (26, 'side'), (27, 'nativeId'), (28, 'slot')]:
            result[offset] = recipe[key]
    return result


def model(kind, recipe, initial, pools):
    base, unused = CONTEXTS[kind]
    result, calls = bytearray(initial), []

    def call(address, arguments, returned=0, writes=()):
        calls.append(dict(address=address, arguments=arguments, result=returned, writes=list(writes)))
        for target, content in writes:
            if base <= target < base + len(result):
                result[target - base:target - base + len(content)] = content

    v = recipe['variant']
    if kind == 'statea':
        native_id = struct.unpack_from('<H', result, 0x50)[0]
        nibble = (0, 1, 15)[v % 3]
        flag = result[0x10] if v % 3 != 1 else (0 if result[0x10] else 255)
        scalar, second = WIDE[v % 4], WIDE[(v + 1) % 4]
        call(0x0207AFEC, [native_id], RECORD, [(RECORD + 8, struct.pack('<H', nibble << 12 | 0xA55)),
            (base + 0x10, bytes([flag])), (base + 0x80, struct.pack('<II', scalar, second))])
        selected = scalar if flag or nibble == 0 else 0
        if result[0x3E] == 0:
            after_flag = (0, 255, 1)[v % 3]
            call(0x021F65D8, [second, selected, native_id], writes=[(base + 0x10, bytes([after_flag])),
                (base + 0x80, struct.pack('<I', 0xDEADBEEF)), (base + 0x3D, bytes([255, 238]))])
            if result[0x10]:
                for i, native_item in enumerate((0xB0, 0xF9, 0x119, 0x10D)):
                    call(0x021F2120, [selected, native_item], writes=[(base + 0x3D, bytes([252, i + 16]))])
            result[0x3E], result[0x3D] = 10, 0
        if result[0x3E] == 10:
            result[0x3D] = (result[0x3D] + 1) & 255
            if result[0x3D] > 40:
                result[0x3E] = 100
        if result[0x3E] == 100:
            result[0x3E] = 0
            if result[0x10] == 0:
                result[0x1B] = 27
            else:
                call(0x021F4210, [], writes=[(base + 0x3D, bytes([75, 238]))])
                result[0x1B] = 3
        return result, calls, 0
    side, slot, native_id = recipe['side'], recipe['slot'], recipe['nativeId']
    pointer = pools[side] + slot * 1088 if side < 4 and slot < 3 else 0
    if result[10] == 0:
        call(0x0220CAB0, [pointer, side, native_id], writes=[(base + 9, bytes([250, 200])),
            (base + 3, b'\x4A'), (base + 26, bytes([170, 187, 204]))])
        result[9], result[10] = 0, 10
    if result[10] == 10:
        result[9] = (result[9] + 1) & 255
        if result[9] > 45:
            result[10] = 20
    if result[10] == 20:
        ready = (0, 1, 0xFFFFFFFF)[v % 3]
        call(0x021DBB14, [pointer, side], ready, [(base + 10, b'\xEE'), (base + 3, b'\x55')])
        result[10] = 30 if ready else 100
    if result[10] == 30:
        finished = (0, 1, 0xFFFFFFFF)[v // 2 % 3]
        after = (30, 100, 0, 255)[v % 4]
        call(0x021DBB9C, [pointer, side], finished, [(base + 10, bytes([after]))])
        if finished:
            result[10] = 100
    if result[10] == 100:
        result[10], result[3] = 0, 14
    return result, calls, 3 + (slot != 4)
