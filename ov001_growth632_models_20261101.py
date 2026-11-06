import math
import struct
import ov001_growth632_machine_20261101 as M


def f32(value):
    return struct.unpack('<f', struct.pack('<f', value))[0]


def floating(word):
    return struct.unpack('<f', struct.pack('<I', word))[0]


def bits(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def signed(word):
    return ((word + 0x80000000) & 0xFFFFFFFF) - 0x80000000


def signed16(word):
    return ((word + 32768) & 65535) - 32768


def profiles():
    result = []
    for category in [0, 1, 2]:
        for present in [False, True]:
            for level in [0, 1, 4]:
                for modifier in [0, 39, 40, 41, 140, 1000]:
                    index = len(result)
                    result.append(dict(name='category%d-open%d-level%d-mod%d' % (category, present, level, modifier), case=index, row=index % 3, id=[0, 0xFFFFFFFF, 0x80008000, 0xABCD0001][index % 4], category=category, variant=[0, 1, 2, 255][index % 4], level=level, modifier=modifier, growthPresent=present, seed=[0, 1, 0x80000000, 0xFFFFFFFF][index % 4], salt=index % 3, bases=([100, 200, 300, 400, 500, 600] if index % 2 == 0 else [65535, 32768, 10000, 9999, 1, 0]), featureWords=[0xA1000000 + (j << 16) + [0, 32767, 32768, 65535][(index + j) % 4] for j in range(6)]))
    for category in [0, 1, 2]:
        for modifier in [0, 1000]:
            index = len(result)
            profile = dict(result[0])
            profile.update(name='all-upper-caps-category%d-mod%d' % (category, modifier), case=index, row=index % 3, category=category, modifier=modifier, bases=[65535] * 6)
            result.append(profile)
    return result


def model(result):
    p = result['profile']
    growth = [0] * 6
    expected_provider = [(0x0222D8E0, [])]
    if p['growthPresent']:
        for step in range(p['level']):
            for stat in range(6):
                callback = (stat + step + p['salt']) % 4
                normalized = (callback * 3 + step + p['salt']) % 7
                delta = (p['variant'] + 2 * normalized + 1) % 9
                growth[stat] += delta
                expected_provider += [(M.CALLBACKS[stat], [p['id'], 0, step]), (0x0222D91C, [callback, step]), (0x0222D964, [p['variant'], normalized])]
        expected_provider.append((0x0222D93C, []))
    expected_provider.append((0x02044CDC, [p['id']]))
    state = (p['seed'] * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
    draw = (state >> 16) % 20
    factor = f32(f32(90.0 + f32(float(draw))) / 100.0)
    coefficient = f32([1.0, 1.15, 1.25][p['category']])
    values = []
    for stat in range(6):
        expected_provider.append((0x020449D4, [p['id']]))
        amount = f32(factor * f32(f32(f32(float(growth[stat])) * coefficient) + f32(float(p['bases'][stat]))))
        if stat == 2:
            amount = f32(f32(0.65 if p['category'] == 1 else 1.0) * amount)
        values.append(int(amount))
    if p['modifier'] >= 40:
        scale = f32(1.0 + f32(f32(0.012) * f32(float(p['modifier'] - 40))))
        values = [int(f32(f32(float(value)) * scale)) for value in values]
    capped = [min(value, 9999) for value in values]
    expected = bytearray(result['before'])
    row, output = M.ROWS + 132 * p['row'], M.OUTPUT + 64 * p['row']
    def store(address, fmt, *values):
        raw = struct.pack(fmt, *values)
        expected[address - M.BASE:address - M.BASE + len(raw)] = raw
    store(M.RNGSTATE, '<I', state)
    initial_stats = [capped[0], capped[1], capped[0], capped[1]] + capped[2:]
    store(row + 0x20, '<8h', *initial_stats)
    snapshots = []
    for index, entry in enumerate(M.FEATURES):
        expected_provider.append((entry, [row + 0x20, output]))
        snapshots.append(list(struct.unpack('<8H', bytes(expected[row - M.BASE + 0x20:row - M.BASE + 0x30]))))
        store(row + [0x24, 0x26, 0x28, 0x2A, 0x2C, 0x2E][index], '<h', signed16(p['featureWords'][index]))
    lo, hi = M.STACK - 65536 - M.BASE, M.STACK + 256 - M.BASE
    if bytes(expected[:lo]) != result['after'][:lo] or bytes(expected[hi:]) != result['after'][hi:]:
        raise ValueError(('632 independent complete nonstack RAM model differs', p['name']))
    if [(event['entry'], event['preparedWords']) for event in result['providedCalls']] != expected_provider:
        raise ValueError('632 provider input preparation/order differs from model')
    if [event['observedRowStatHalfwordsBeforeCall'] for event in result['providedCalls'] if event['entry'] in M.FEATURES] != snapshots:
        raise ValueError('632 intermediate calculated/capped stat values differ before feature calls')
    if result['actualTopReturnedWords'][0] != p['featureWords'][-1]:
        raise ValueError('632 physical full-word final helper forwarding differs')
    for record in result['nativeReturns']:
        entry, words, returned = record['entry'], record['preparedWords'], record['returnedWords']
        if entry == 0x02025A28:
            wanted = bits(f32(float(signed(words[0]))))
        elif entry == 0x02025A70:
            wanted = bits(f32(float(words[0])))
        elif entry == 0x02024E0C:
            wanted = bits(f32(floating(words[0]) + floating(words[1])))
        elif entry == 0x02025578:
            wanted = bits(f32(floating(words[0]) / floating(words[1])))
        elif entry == 0x02025AB8:
            wanted = bits(f32(floating(words[0]) * floating(words[1])))
        elif entry == 0x020259B4:
            value = floating(words[0])
            if not math.isfinite(value) or not -2147483648 <= value < 2147483648:
                raise ValueError('632 signed conversion left finite qualified range')
            wanted = int(value) & 0xFFFFFFFF
        elif entry == 0x0203D294:
            if words[0] != 20 or returned[0] != draw:
                raise ValueError('632 actual RNG bound/return differs')
            continue
        else:
            continue
        if returned[0] != wanted:
            raise ValueError(('632 actual finite native float contract differs', hex(entry)))
    return dict(growth=growth, randomFactorWord=bits(factor), calculatedValues=values, cappedValues=capped, featureSnapshots=snapshots, rngState=state, finalReturnedWord=p['featureWords'][-1])
