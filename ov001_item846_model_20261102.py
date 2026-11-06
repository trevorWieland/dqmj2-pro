import itertools
import struct
import ov001_item846_machine_20261102 as M


def profiles():
    output = []

    def add(**changes):
        ordinal = len(output)
        p = dict(ordinal=ordinal, phase=100, item=ordinal % 256, side=ordinal % 4, slot=ordinal % 3, kind=ordinal % 16, subtype=ordinal % 256, resource=[0, 1, 32768, 65535][ordinal % 4], tokenWord=[0, 127, 128, 255, 0x12348001, 0xFFFFFFFF][ordinal % 6], halfWord=[0, 1, 0xFFFF, 0x10000, 0xABCD8000, 0xFFFFFFFF][ordinal % 6], timerWord=[0, 1, 0xFFFFFFFF][ordinal % 3], oldHalf=[0, 1, 32768, 65535][ordinal % 4], oldToken=[0, 127, 128, 255][ordinal % 4])
        p.update(changes)
        output.append(p)

    for phase, kind, subtype in itertools.product([0, 10, 15, 20, 25, 100, 127, 128, 255], [0, 1, 2, 8, 9, 10, 11, 12, 13, 14, 255], [0, 47, 255]):
        add(phase=phase, kind=kind, subtype=subtype)
    for phase, token, timer in itertools.product([15, 20], [0, 127, 128, 255, 0x12348001, 0xFFFFFFFF], [0, 1, 0xFFFFFFFF]):
        add(phase=phase, tokenWord=token, timerWord=timer)
    for side, slot in itertools.product([0, 1, 2, 3, 4, 255], [0, 1, 2, 3, 255]):
        add(side=side, slot=slot)
    return output


def signed_byte(value):
    value &= 255
    return value - 256 if value & 128 else value


def model(vm, result):
    p = vm.p
    state = bytearray(vm.beforeState)
    calls = []

    def emit(pc, *args):
        args = list(map(M.word, args))
        calls.append(dict(target=hex(pc), callerWords=args, suppliedReturn=M.word(vm.provider(pc, args))))

    if state[0x15] == 0:
        emit(0x0220B9E0)
        emit(0x021E3544, 0, 1)
        state[0x15] = 10
    if state[0x15] == 10:
        emit(0x0202AC08, M.STATE + 0x20)
        if p['resource']:
            emit(0x021EEA10, p['resource'], 0)
            state[0x15] = 15
        else:
            state[0x15] = 100
    elif state[0x15] == 15:
        emit(0x0205C904, p['resource'])
        emit(0x0220BBB8, p['resource'])
        state[0x14] = p['tokenWord'] & 255
        emit(0x0220BD30, p['side'], p['slot'], p['item'], 1)
        emit(0x0220BF30, p['item'], p['side'])
        struct.pack_into('<H', state, 0x18, p['halfWord'] & 65535)
        state[0x15] = 20
    if state[0x15] == 20:
        emit(0x0205D6F4, signed_byte(state[0x14]))
        if p['timerWord'] == 0:
            emit(0x0220BD30, p['side'], p['slot'], p['item'], 0)
            state[0x15] = 25
        else:
            emit(0x0220BDE8, p['side'], p['slot'], p['item'])
    elif state[0x15] == 25:
        emit(0x021EEB70, p['resource'])
        emit(0x0202AC4C, M.STATE + 0x20)
        if struct.unpack_from('<H', state, 0x18)[0]:
            emit(0x021F14A4)
        state[0x15] = 100
    if state[0x15] == 100:
        state[3] = {1: 6, 2: 7, 8: 8, 11: 9, 10: 10, 12: 11, 9: 12, 13: 13}.get(p['kind'], 13 if p['subtype'] == 47 else 6)
        state[0x15] = 0
    failures = []
    if result['registers'][0] != 0:
        failures.append('proper zero caller return')
    if result['calls'] != calls:
        failures.append('ordered raw-word service contracts')
    if result['state'] != bytes(state):
        failures.append('independent phase/token/halfword/raw selector transitions')
    if result['table'] != vm.beforeTable:
        failures.append('synthetic table unchanged')
    resolver = [row for row in result['nativeEntries'] if row['address'] == '0x21db438']
    if len(resolver) != 1 or resolver[0]['rawWords'][:2] != [p['side'], p['slot']]:
        failures.append('actual two-word resolver input')
    return failures
