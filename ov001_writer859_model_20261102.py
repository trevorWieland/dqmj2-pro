import itertools
import ov001_writer859_machine_20261102 as M


def profiles():
    output = []
    for selector, slot, equal in itertools.product(range(256), range(3), [False, True]):
        n = len(output)
        output.append(dict(ordinal=n, selector=selector, slot=slot, prior=selector if equal else selector ^ 1, flags=(selector * 37 + slot * 17 + int(equal) * 61) & 255))
    return output


def model(vm, result):
    p = vm.p
    state = bytearray(vm.beforeState)
    rows = bytearray(vm.beforeRows)
    actors = bytearray(vm.beforeActors)
    cache = bytearray(vm.beforeCache)
    state[0xA] = 6
    rows[2 * 0xF0 + 0x12] = p['slot']
    rows[2 * 0xF0 + 0x13] = 1
    cache[p['slot']] = p['selector']
    actors[p['slot'] * 0x440 + 0x1FE] = p['selector']
    actors[p['slot'] * 0x440 + 0x35D] = p['flags'] & 251 if p['prior'] == p['selector'] else p['flags'] | 4
    specs = [(0x022028C8, [p['slot']]), (0x021FE74C, [2]), (0x021FE2B8, [1, 1]), (0x022023C4, [0x40])]
    calls = [dict(target=hex(pc), callerWords=args, suppliedReturn=M.word(vm.provider(pc, args))) for pc, args in specs]
    failures = []
    if result['registers'][0] != 1:
        failures.append('case2 caller raw return1')
    if result['calls'] != calls:
        failures.append('ordered consumed callback views')
    for field, expected in [('state', state), ('rows', rows), ('actors', actors), ('cache', cache)]:
        if result[field] != bytes(expected):
            failures.append('independent case2 ' + field + ' effects')
    getter = [row for row in result['nativeEntries'] if row['address'] == '0x2202360']
    resolver = [row for row in result['nativeEntries'] if row['address'] == '0x21db438']
    if [row['rawWords'][0] for row in getter] != [2, 0]:
        failures.append('actual row getter inputs')
    if len(resolver) != 1 or resolver[0]['rawWords'][:2] != [0, p['slot']]:
        failures.append('actual actor resolver inputs')
    return failures
