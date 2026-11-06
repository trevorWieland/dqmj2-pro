import random
import struct
from ov001_reward458_machine_20261101 import BASE, STACK, OUTPUT, RNG

def profiles():
    rows = []
    rates = [0, 1, 2, 3, 4, 5, 6, 7, 8, 255]
    for index in range(256):
        rng = random.Random(458000 + index)
        enemies = []
        for slot in range(3):
            enemies.append(dict(ready=rng.choice([0, 1, 128, 255]), flag=rng.choice([0, 1, 255]), fallback=rng.choice([0, 1, 255]), ac=rng.choice([0, 1, 255]), suppressed=int(rng.randrange(5) == 0), firstItem=rng.choice([0, 7, 90, 65535]), secondItem=rng.choice([0, 1, 700, 65535]), fallbackItem=rng.choice([0, 4, 500, 65535]), firstRate=rates[(index+slot) % 10], secondRate=rates[(index//10+slot*3) % 10], fallbackRate=rates[(index//4+slot) % 10]))
        rows.append(dict(name=f'mixed-{index}', seed=([0, 1, 0xFFFFFFFF, 0x80000000, 0x12345678, 0x7FFFFFFF][index % 6] ^ (index * 0x9E3779B9)) & 0xFFFFFFFF, mask=0x20000 if index & 1 else 0, bonusActors=index % 4, enemies=enemies))
    for fallback in [False, True]:
        for item in [0, 65535]:
            e = dict(ready=1, flag=0 if fallback else 1, fallback=1, ac=1, suppressed=0, firstItem=item, secondItem=0, fallbackItem=item, firstRate=0, secondRate=0, fallbackRate=0)
            rows.append(dict(name=f'all-append-fallback{fallback}-item{item}', seed=0xFFFFFFFF, mask=0, bonusActors=0, enemies=[dict(e) for unused in range(3)]))
    return rows

def model(result):
    p = result['profile']
    state = p['seed']
    calls, output = [], []
    def attempt(rate, first):
        nonlocal state
        for unused in range(p['bonusActors']):
            if 2 <= rate <= 6:
                rate -= 1
        if rate == 0:
            value = 0
        elif rate <= 6:
            bound = 1 << (rate + 2)
            calls.append(dict(bound=bound, stateBefore=state))
            state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
            value = (state >> 16) % bound
        else:
            value = 1
        return value == 0 or not first and bool(p['mask'] & 0x20000)
    for e in p['enemies']:
        if e['ready'] and e['flag']:
            item = 0
            if not e['suppressed']:
                if e['firstItem'] and attempt(e['firstRate'], True):
                    item = e['firstItem']
                elif e['secondItem'] and attempt(e['secondRate'], False):
                    item = e['secondItem']
            if item:
                output.append(item)
        elif e['fallback'] and e['ready'] and e['ac'] and attempt(e['fallbackRate'], False):
            output.append(e['fallbackItem'])
    expected = bytearray(result['before'])
    struct.pack_into('<3H', expected, OUTPUT - BASE, *(output + [0] * (3-len(output))))
    struct.pack_into('<I', expected, RNG - BASE, state)
    cut = STACK - BASE
    if expected[:cut-65536] != result['after'][:cut-65536] or expected[cut+4096:] != result['after'][cut+4096:]:
        raise ValueError(('458 independent complete nonstack effects differ', p['name']))
    if result['returnedR0'] != int(bool(output)) or result['calls'] != calls:
        raise ValueError(('458 independent return/RNG order differs', p['name'], result['returnedR0'], output, result['calls'], calls))
    actualRngReturns = sum(row['entry'] == 0x0203D294 for row in result['nativeReturns'])
    if actualRngReturns != len(calls):
        raise ValueError('458 RNG did not actually return')
    return dict(appendedWords=output, outputWords=output + [0] * (3-len(output)), rngFinal=state, actualRngReturnsWithinDependencyTotal=actualRngReturns)
