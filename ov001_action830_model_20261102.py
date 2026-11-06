import struct
import ov001_action822_machine_20261102 as M
import ov001_action830_machine_20261102 as A


def expected(vm):
    p = vm.p
    context = bytearray(vm.beforeContext)
    calls = []

    def emit(pc, *args):
        args = [value & 0xFFFFFFFF for value in args]
        result = vm.provider(pc, args) & 0xFFFFFFFF
        calls.append(dict(target=hex(pc), callerWords=args, suppliedReturn=result))
        return result

    category = (p['moveNibbles'] >> 8) & 15
    movePointer = M.MOVES + p['moveId'] * 40
    target = vm.current
    if context[9] == 0:
        if context[0x10] == 0 or context[0x13] != 0:
            if category in [7, 9] or p['moveId'] == 0xB6:
                emit(0x021D7F54, p['lookupSide'])
            else:
                emit(0x021F1F1C, movePointer)
        else:
            emit(0x021D7E80, target)
        struct.pack_into('<I', context, 0x6C, 0)
        context[9] = 5
    if context[9] == 5:
        emit(0x021F34C8, category)
        context[9] = 10
    if context[9] == 10:
        if p['effect']:
            emit(0x0202AC08, 0x0223992C)
            emit(0x021EEA10, p['effect'], 0)
        context[9] = 15
    elif context[9] == 15:
        if p['effect']:
            emit(0x0205C904, p['effect'])
            context[0] = emit(0x021F32B4, p['moveId'], target) & 0xFF
        emit(0x021F30CC, target, p['moveId'], 1)
        if p['moveByte21']:
            emit(0x021D8DEC, p['moveByte21'])
            if p['rowHalf']:
                emit(0x021F1354, 1, 0, p['rowHalf'], 1)
        context[9] = 20
    if context[9] == 20:
        token = context[0] - 256 if context[0] & 0x80 else context[0]
        if p['effect'] == 0 or emit(0x0205D6F4, token) == 0:
            emit(0x021F30CC, target, p['moveId'], 0)
            context[9] = 25
        else:
            emit(0x021F3178, target, p['moveId'])
    elif context[9] == 25:
        if p['effect']:
            emit(0x021EEB70, p['effect'])
            emit(0x0202AC4C, 0x0223992C)
        context[9] = 30
    if context[9] == 30:
        if emit(0x021F14E4):
            emit(0x021F14A4)
        context[9] = 100
    if context[9] == 100:
        scanSide = 1 if p['lookupSide'] == 0 else 0
        flags = p.get('flagsBySide', [p['opponentFlags']] * 4)[scanSide]
        opponent = any(p['enabled'][index] and p['markers'][index] == 0 and p['descriptorFlags'][index] == 0 and flags[index] != 0 for index in range(3))
        if opponent and p['halfFlags'] & 0x8000:
            phase = 25
        else:
            phase = {1: 4, 2: 5, 3: 7, 4: 6, 5: 8, 6: 9, 7: 10, 8: 11, 9: 12, 10: 13}.get(category, 4)
        context[0x1B] = phase
        context[9] = 0
    return context, calls


def model(vm, result):
    context, calls = expected(vm)
    failures = []
    if result['rawR0'] != 0:
        failures.append('physical return0')
    if result['context'] != context:
        failures.append('complete144-byte supplied context')
    if result['actors'] != vm.beforeActors:
        failures.append('actor buffers unchanged under supplied no-effect services')
    if result['calls'] != calls:
        failures.append('ordered raw-word service contracts')
    return failures
