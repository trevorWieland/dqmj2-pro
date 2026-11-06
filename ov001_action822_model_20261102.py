import struct
import ov001_action822_machine_20261102 as M


def u32(value):
    return value & 0xFFFFFFFF


def s32(value):
    value &= 0xFFFFFFFF
    return value - 0x100000000 if value & 0x80000000 else value


def expected(vm):
    p = vm.p
    context = bytearray(vm.beforeContext)
    actors = {key: bytearray(value) for key, value in vm.beforeActors.items()}
    calls = []
    current = vm.current

    def emit(address, *args):
        args = [u32(value) for value in args]
        value = vm.provider(address, args) & 0xFFFFFFFF
        calls.append(dict(target=hex(address), callerWords=args, suppliedReturn=value))
        return value

    def eligible(pointer):
        if not pointer:
            return False
        index = (pointer - M.ACTOR_BASES[p['lookupSide']]) // 0x440
        return bool(p['enabled'][index]) and p['markers'][index] == 0 and p['descriptorFlags'][index] == 0

    def cost(pointer):
        value = struct.unpack_from('<h', actors[pointer], 0x1F2)[0]
        field = p['costField']
        if field == 10000:
            return value if value else 1
        if field == 10001:
            return int((value + 1) / 2) if value else 1
        if field == 10002:
            return max(value, 150)
        descriptor = struct.unpack_from('<I', actors[pointer], 0x1E8)[0]
        return M.s16(emit(0x0207CE3C, descriptor + 0x46, p['moveId'], field))

    def deduct(pointer, amount):
        actor = actors[pointer]
        old = struct.unpack_from('<h', actor, 0x1F2)[0]
        if old >= 10000:
            return
        if amount == 10000:
            value = 0
        elif amount == 10001:
            value = int((old + 1) / 2)
        else:
            value = old - amount
            if value < 0:
                value = 0
            elif value > s32(emit(0x021DBCF0, pointer)):
                value = s32(emit(0x021DBCF0, pointer))
        struct.pack_into('<H', actor, 0x1F2, value & 0xFFFF)

    if context[0xF] == 0:
        emit(0x021F1354, 0x81, 0xFE, 0x8123, 1)
        selected = emit(0x021F1414, p['lookupSide']) if p['selection'] == -1 else p['selection'] & 0xFF
        emit(0x021F1438, selected)
        category = p['moveNibbles'] & 15
        emit(0x021F1D54, category)
        emit(0x021D9494, current, 2 if category == 5 else 3, 1)
        emit(0x02202528, p['lookupSide'], p['currentSlot'])
        context[0xF] = 20 if p['effect'] == 0 else 10
    if context[0xF] == 10:
        emit(0x0202AC08, 0x0223992C)
        emit(0x021EEA10, p['effect'], 0)
        context[0xF] = 15
    elif context[0xF] == 15:
        emit(0x0205C904, p['effect'])
        text = emit(0x0205D790, p['effect'])
        context[6] = emit(0x021EEC7C, p['effect'], current, text) & 0xFF
        emit(0x021F94D8, 0x99, 1)
        context[0xF] = 20
    if context[0xF] == 20:
        six = emit(0x021D9534, current, -1, 6, 0)
        eight = emit(0x021D9534, current, -1, 8, 0)
        progress = u32(s32(p['frameWord']) >> 12)
        if six <= progress:
            context[0xF] = 100
        elif eight <= progress:
            context[0xF] = 110
    if context[0xF] not in [100, 110]:
        return context, actors, calls
    if p['effect']:
        emit(0x0205D718, context[6])
        emit(0x021EEB70, p['effect'])
        emit(0x0202AC4C, 0x0223992C)
    emit(0x021F14A4)
    if context[0xF] == 110:
        context[0x1B] = 26
        context[0xF] = 0
        return context, actors, calls
    pointers = [M.ACTOR_BASES[p['lookupSide']] + index * 0x440 for index in range(3)] if p['lookupSide'] < 4 else [0, 0, 0]
    emit(0x021DCA54, current, 0, 4)
    if p['special'] != 1:
        emit(0x02202540, p['lookupSide'], p['currentSlot'])
    multi = bool(p['halfFlags'] & 0x400)
    allowed = emit(0x021DD02C, current, p['moveId'], int(multi))
    if allowed and p['gate']:
        if not multi:
            amount = cost(current)
            deduct(current, amount)
            struct.pack_into('<I', context, 0x5C, u32(amount))
            emit(0x022024D4, p['lookupSide'], p['currentSlot'], 0)
        else:
            total = 0
            for index, pointer in enumerate(pointers):
                if eligible(pointer):
                    amount = cost(pointer)
                    deduct(pointer, amount)
                    total = u32(total + amount)
                    emit(0x022024D4, actors[pointer][0x31E], index, 0)
            struct.pack_into('<I', context, 0x5C, total)
    flags = p['moveFlags']
    traits = p['traits']
    special = p['special'] == 1
    if traits[0] and flags & 2 and not special:
        phase = 16
    elif not allowed and p['gate'] and not special:
        phase = 17
    elif traits[1] and flags & 8 and not special:
        phase = 18
    elif traits[2] and flags & 0x04000000 and not special:
        phase = 19
    elif traits[3] and flags & 4 and not special:
        phase = 20
    elif traits[4] and flags & 0x02000000 and not special:
        phase = 21
    elif p['policy'] & 1 and flags & 0x20000 and not special:
        phase = 22
    elif traits[5] and (p['moveNibbles'] >> 8) & 15 == 4 and p['moveByte21'] == 0x2B and not special:
        phase = 23
    else:
        phase = 2 if p['moveId'] in [0x34, 0x35, 0xC1] else 3
    context[0x1B] = phase
    context[0xF] = 0
    return context, actors, calls


def model(vm, result):
    context, actors, calls = expected(vm)
    failures = []
    if result['rawR0'] != 0:
        failures.append('raw return zero')
    if result['context'] != context:
        failures.append('complete144-byte supplied context')
    if result['actors'] != actors:
        failures.append('complete12-actor supplied state')
    if result['calls'] != calls:
        failures.append('ordered supplied-call raw-word contracts')
    return failures
