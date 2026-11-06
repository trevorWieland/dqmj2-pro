import struct
import ov006_record610_machine_20261101 as M


def signed16(value):
    return ((value + 32768) & 65535) - 32768


def profiles():
    cases = []
    levels = [0, 1, 2, 50, 51, 75, 76, 100, 255]
    seeds = [0, 1, 0x80000000, 0xFFFFFFFF]
    for mask in range(32):
        for salt in range(3):
            index = len(cases)
            cases.append(dict(name='raw-mask-%02d-%d' % (mask, salt), species=[-32768, -1, 0, 32767][index % 4], variant=[0, 1, 255][salt], level=levels[index % len(levels)], rawFive=[([1, 127, 255][(j + salt) % 3] if mask & (1 << j) else 0) for j in range(5)], seed=seeds[index % 4], argument=[0, 0x7FFFFFFF, 0xFFFFFFFF][salt], category=index % 6, callbackSalt=salt, bases=[(0xA1000000 + j * 0x10000 + [0, 32767, 32768, 65535][(j + index) % 4]) & 0xFFFFFFFF for j in range(6)], caps=[(0xB1000000 + j * 0x10000 + [32767, 0, 32768, 65535][(j + index) % 4]) & 0xFFFFFFFF for j in range(6)], abilityPresent=salt != 1, pointsPresent=salt != 2, curvePresent=(index % 3) != 0))
    for outcome in [0, 8, 16]:
        seed = next(value for value in range(1000) if ((((value * 0x41C64E6D + 0x3039) & 0xFFFFFFFF) >> 16) % 17) == outcome)
        p = dict(cases[-1])
        p.update(name='rng-outcome-%d' % outcome, seed=seed, level=2, rawFive=[1, 2, 3, 4, 5], abilityPresent=True, pointsPresent=True, curvePresent=True)
        cases.append(p)
    return cases


def model(result):
    p = result['profile']
    expected = bytearray(result['before'])
    def store(address, fmt, *values):
        raw = struct.pack(fmt, *values)
        expected[address - M.BASE:address - M.BASE + len(raw)] = raw
    def record(offset, fmt, *values):
        store(M.RECORD + offset, fmt, *values)
    record(0x30, '<B', p['level'])
    category_calls, callback_calls = [], []
    stats = []
    for stat in range(6):
        value = signed16(p['bases'][stat])
        if p['abilityPresent']:
            category_calls.append([p['species'] & 0xFFFFFFFF])
            if p['level']:
                for step in range(p['level']):
                    callback = (stat + step + 1 + p['callbackSalt']) % 3
                    callback_calls.append((M.CALLBACKS[stat], [p['species'] & 0xFFFFFFFF, p['variant'], step + 1], callback))
                    increment = signed16((p['category'] + 1) * M.ability_bytes()[100 * callback + step])
                    value = signed16(value + increment)
        value = min(value, signed16(p['caps'][stat]))
        stats.append(value)
    for offset, value in zip([0x20, 0x22, 0x28, 0x2A, 0x2C, 0x2E], stats):
        record(offset, '<h', value)
    record(0x24, '<h', stats[0])
    record(0x26, '<h', stats[1])
    record(0x1C, '<B', 10 if p['level'] > 75 else 4 if p['level'] > 50 else 0)
    curve = M.curve_words()
    record(0x34, '<II', curve[p['level']] if p['curvePresent'] else 0, curve[p['level'] + 1] if p['curvePresent'] else 0)
    count = sum(value != 0 for value in p['rawFive'])
    total = 0
    if p['pointsPresent']:
        for value in M.point_bytes()[:p['level']]:
            total = signed16(total + value)
        dividend = total * count + 4
        total = signed16((abs(dividend) // 5) * (-1 if dividend < 0 else 1))
    record(0x3C, '<h', total)
    for slot in range(count):
        record(0x7A + 2 * slot, '<BB', p['rawFive'][slot], 0)
    state = (p['seed'] * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
    outcome = (state >> 16) % 17
    selector = 0 if outcome < 8 else 1 if outcome > 8 else 2
    record(0x1B, '<B', selector)
    store(M.RNGSTATE, '<I', state)
    store(M.CONTEXT + 8, '<I', p['argument'])
    store(M.CONTEXT + 0x10, '<I', M.UID)
    lo, hi = M.STACK - 65536 - M.BASE, M.STACK + 4096 - M.BASE
    if bytes(expected[:lo]) != result['after'][:lo] or bytes(expected[hi:]) != result['after'][hi:]:
        differences = [hex(M.BASE + index) for index, (a, b) in enumerate(zip(expected, result['after'])) if a != b and not lo <= index < hi]
        raise ValueError(('610 independent complete nonstack RAM model differs', p['name'], differences[:16]))
    callbacks = [(event['entry'], event['preparedWords'], event['providedR0']) for event in result['providedCalls'] if event['entry'] in M.CALLBACKS]
    if callbacks != callback_calls:
        raise ValueError('610 callback words/order differ from independent growth model')
    categories = [event['preparedWords'] for event in result['providedCalls'] if event['entry'] == 0x02044CDC]
    if categories != category_calls:
        raise ValueError('610 category-call prerequisites differ')
    notifications = [event['preparedWords'] for event in result['providedCalls'] if event['entry'] == 0x0207AEBC]
    wanted = [[p['species'] & 0xFFFFFFFF, p['rawFive'][slot], 0] for slot in range(count)]
    if notifications != wanted:
        raise ValueError('610 skill-pair notification contract differs')
    rng = [ret for ret in result['nativeReturns'] if ret['entry'] == 0x0203D294]
    if len(rng) != 1 or rng[0]['preparedWords'][0] != 17 or rng[0]['returnedWords'][0] != outcome:
        raise ValueError('610 actual RNG entry/return differs')
    if result['coreRegistersAndCpsr'][0] != 0xE61083E4:
        raise ValueError('610 final supplied cleanup result was not physically returned')
    return dict(record=bytes(expected[M.RECORD - M.BASE:M.RECORD - M.BASE + 256]).hex(), rngState=state, selector=selector, count=count, statWords=stats, points=total, callbackCalls=len(callback_calls), contextWords=[p['argument'], M.UID])
