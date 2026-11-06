import struct
import ov005_record670_machine_20261101 as M


def s16(value):
    value &= 65535
    return value - 65536 if value & 32768 else value


def f32(value):
    return struct.unpack('<f', struct.pack('<f', value))[0]


def profiles():
    result = []
    for seed in range(32):
        source = bytearray((index * 17 + seed * 31 + 7) & 255 for index in range(512))
        output = [(index * 11 + seed * 13 + 0xA5) & 255 for index in range(768)]
        metadata = []
        for row in range(3):
            base = 0x1C + row * 0x98
            struct.pack_into('<h', source, base + 0x18, [-32768, -2, -1, 0, 1, 2, 32767][(seed + row) % 7])
            source[base + 0x30] = [0, 1, 2, 5, 127, 128, 129, 255][(seed + row) % 8]
            source[base + 0x31:base + 0x34] = bytes([seed * 3 + row, [0, 1, 127, 128, 255][(seed + row) % 5], 255 - seed * 3 - row])
            source[base + 0x1C] = [0, 1, 128, 255][(seed + row) % 4]
            for stat, offset in enumerate([0x20, 0x22, 0x28, 0x2A, 0x2C, 0x2E]):
                struct.pack_into('<h', source, base + offset, [-32768, -1, 0, 1, 32766, 32767][(seed + row + stat) % 6])
            pattern = [[0, 0, 0, 0, 0], [4, 4, 5, 0, 5], [5, 4, 3, 2, 1], [1, 0, 2, 0, 3]][(seed + row) % 4]
            for slot, identifier in enumerate(pattern):
                source[base + 0x78 + slot * 4] = identifier
                struct.pack_into('<H', source, base + 0x7A + slot * 4, (seed * 1001 + row * 71 + slot * 257) & 65535)
            meta = bytearray(64)
            for stat in range(6):
                struct.pack_into('<H', meta, 0x10 + stat * 2, [0, 1, 32767, 32768, 65534, 65535][(seed + row + stat) % 6])
            metadata.append(list(meta))
        points = [([0, 1, 255, (index * 13 + 7) & 255][seed % 4]) for index in range(256)]
        curve = [(index * 0x10203 + seed * 0x91734521) & 0xFFFFFFFF for index in range(257)]
        result.append(dict(name=f'record-{seed}', input=list(source), output=output, metadata=metadata, points=points, curve=curve, curvePresent=[bool((seed + row) % 3) for row in range(3)], pointsOpened=bool(seed % 3), globalWords=[(seed * 0x129357AF + 0xFFFFFFFF) & 0xFFFFFFFF, (seed * 0x91451231 + 0x87654321) & 0xFFFFFFFF, (seed * 0x319579A3 + 0xFFFFFFFF) & 0xFFFFFFFF]))
    return result


def expected(profile):
    source, target = bytes(profile['input']), bytearray(profile['output'])
    rd16 = lambda offset: struct.unpack_from('<H', source, offset)[0]
    def put16(offset, value):
        struct.pack_into('<H', target, offset, value & 65535)
    def put32(offset, value):
        struct.pack_into('<I', target, offset, value & 0xFFFFFFFF)
    target[:4] = bytes(4)
    target[0xA8:0xAE], target[0xAE:0xB0] = source[:6], source[6:8]
    target[0xB0:0xC4], target[:0x14] = source[8:0x1C], source[8:0x1C]
    records = []
    for row in range(3):
        src, dst = 0x1C + row * 0x98, 0xC4 + row * 0x84
        target[dst:dst + 0x14] = source[src:src + 0x14]
        target[dst + 0x14:dst + 0x1A] = source[src + 0x14:src + 0x1A]
        target[dst + 0x1B] = source[src + 0x1A]
        target[dst + 0x1C] = target[dst + 0x1E] = source[src + 0x1B]
        target[dst + 0x1D] = int(source[src + 0x1C] != 0)
        target[dst + 0x30] = source[src + 0x30]
        target[dst + 0x32], target[dst + 0x33], target[dst + 0x31] = source[src + 0x31:src + 0x34]
        raw_id = struct.unpack_from('<h', source, src + 0x18)[0]
        normalized, variant = s16(raw_id * 3 + 7), (raw_id ^ 5) & 3
        put16(dst + 0x18, normalized)
        target[dst + 0x1A] = variant
        identifiers = []
        for slot in range(5):
            identifier = source[src + 0x78 + slot * 4]
            identifiers.append(identifier)
            target[dst + 0x7A + slot * 2] = identifier
            target[dst + 0x7B + slot * 2] = source[src + 0x7A + slot * 4]
        count = sum(value != 0 for value in identifiers)
        if not count:
            identifiers[0] = 0x8E
        else:
            for i in range(4):
                for j in range(i + 1, 5):
                    if identifiers[i] == identifiers[j]:
                        identifiers[j] = 0
            for i in range(4):
                if identifiers[i] == 0:
                    for j in range(i + 1, 5):
                        if identifiers[j] != 0:
                            identifiers[i], identifiers[j] = identifiers[j], 0
                            break
        for slot, identifier in enumerate(identifiers):
            target[dst + 0x7A + slot * 2] = identifier
        total = 0
        if profile['pointsOpened']:
            for value in profile['points'][:source[src + 0x30]]:
                total = s16(total + value)
            numerator = total * count + 4
            points = s16(abs(numerator) // 5 * (-1 if numerator < 0 else 1))
        else:
            points = 0
        put16(dst + 0x3C, points)
        factor = f32(f32(f32(2.0) + f32(float(variant))) / f32(2.0))
        limits = []
        for index, offset in enumerate([0x20, 0x22, 0x28, 0x2A, 0x2C, 0x2E]):
            field = struct.unpack_from('<h', source, src + offset)[0]
            bound = struct.unpack_from('<H', bytes(profile['metadata'][row]), 0x10 + index * 2)[0]
            cap = s16(int(f32(f32(float(bound)) * factor)))
            put16(dst + offset, min(field, cap))
            limits.append(cap)
        target[dst + 0x24:dst + 0x28] = target[dst + 0x20:dst + 0x24]
        level = source[src + 0x30]
        put32(dst + 0x34, profile['curve'][level] if profile['curvePresent'][row] else 0)
        put32(dst + 0x38, profile['curve'][level + 1] if profile['curvePresent'][row] else 0)
        target[dst + 0x40:dst + 0x7A] = bytes(0x3A)
        records.append(dict(row=row, rawInputId=raw_id, normalizedId=normalized, variant=variant, countBeforeIdNormalization=count, finalIds=identifiers, signed16Points=points, factor=factor, signed16Caps=limits, suppliedSourceByte32=source[src + 0x32], expectedTargetByte33=target[dst + 0x33]))
    target[0x254:0x262] = source[0x1E4:0x1F2]
    word = struct.unpack_from('<I', target, 0x14)[0]
    word = (word & ~0xFFF) | (profile['globalWords'][0] & 0xFFF)
    word = (word & ~0xF000) | ((profile['globalWords'][1] & 15) << 12)
    word = (word & ~0x1F0000) | ((profile['globalWords'][2] & 31) << 16)
    put32(0x14, word)
    target[0x262] = 0
    put16(0x264, 0)
    snapshot = bytes(target[:0x268])
    checksum = sum(struct.unpack_from('<307H', target)) & 65535
    put16(0x266, checksum)
    put32(0x250, rd16(0x1E4) + rd16(0x1E6) + rd16(0x1E8))
    put16(0x256, rd16(0x1E6))
    return bytes(target), snapshot, dict(records=records, checksumBeforeFinalFooterSum=checksum, finalFooterSum=rd16(0x1E4) + rd16(0x1E6) + rd16(0x1E8), expectedPhysicalR0=0xE670F00D)


def model(result):
    target, snapshot, detail = expected(result['profile'])
    if result['output'] != target:
        differences = [hex(i) for i, (a, b) in enumerate(zip(result['output'], target)) if a != b]
        raise ValueError(('670 independent complete output differs', result['profile']['name'], differences[:20]))
    if result['checksumSnapshot'] != snapshot:
        raise ValueError('670 checksum pre-final-sum snapshot differs')
    if result['coreRegistersAndCpsr'][0] != 0xE670F00D:
        raise ValueError('670 physical exit-boundary R0 differs')
    expected_calls = [dict(entry=0x020CF620, preparedWords=[1])]
    for row, record in enumerate(detail['records']):
        raw = record['rawInputId']
        expected_calls.append(dict(entry=0x020CF590, inputWord=raw & 0xFFFFFFFF, effects=[struct.pack('<H', record['normalizedId'] & 65535).hex(), bytes([record['variant']]).hex()]))
        for slot in range(5):
            pointer = M.OUTPUT + 0xC4 + row * 0x84 + 0x7A + slot * 2
            expected_calls.append(dict(entry=0x020CF6A4, preparedWords=[pointer, pointer]))
        expected_calls.append(dict(entry=0x0203CC2C, preparedWords=[0x021E7894, 1]))
        if result['profile']['pointsOpened']:
            expected_calls.append(dict(entry=0x0203CF9C, preparedWords=[1, M.POINTS]))
        expected_calls.append(dict(entry=0x020449D4, preparedWords=[record['normalizedId'] & 0xFFFFFFFF]))
        expected_calls.append(dict(entry=0x021E65EC, preparedWords=[record['normalizedId'] & 0xFFFFFFFF, record['variant'], 1]))
        expected_calls.append(dict(entry=0x0202A498, preparedWords=[1, M.CURVE + 4 if result['profile']['curvePresent'][row] else 0]))
    expected_calls.append(dict(entry=0x020CF658, preparedWords=[]))
    actual_calls = []
    for call in result['providedCalls']:
        if call['entry'] == 0x020CF590:
            actual_calls.append(dict(entry=call['entry'], inputWord=call['preparedWords'][0], effects=[effect['bytes'] for effect in call['ramEffects']]))
        else:
            actual_calls.append(dict(entry=call['entry'], preparedWords=call['preparedWords']))
    if actual_calls != expected_calls:
        raise ValueError('670 independently expected service order/word/effects differs')
    before, after = result['before'], result['after']
    allowed = [(M.OUTPUT - M.BASE, M.OUTPUT - M.BASE + len(target)), (M.STACK - 65536 - M.BASE, M.STACK + 256 - M.BASE)]
    cursor = 0
    for lo, hi in sorted(allowed):
        if before[cursor:lo] != after[cursor:lo]:
            raise ValueError('670 independent non-output/non-stack RAM changed')
        cursor = hi
    if before[cursor:] != after[cursor:]:
        raise ValueError('670 trailing non-output/non-stack RAM changed')
    return detail
