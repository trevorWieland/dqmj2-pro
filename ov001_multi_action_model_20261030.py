import random
import struct

CONTEXT, ACTOR, OPPONENTS = 0x02238D7C, 0x02360000, 0x02362000
MOTION, MOTION_INFO, DESCRIPTOR = 0x02366000, 0x02367000, 0x02368000
FLAGS, TIMER = 0x02238E44, 0x02238E14


def signed(value, bits):
    return ((value & ((1 << bits) - 1)) ^ (1 << (bits - 1))) - (1 << (bits - 1))


def vectors():
    result = []
    for state in (0, 10, 20, 50, 60, 100, 200, 1, 255):
        for shape in range(32):
            seed = 710000 + len(result)
            rng = random.Random(seed)
            context = bytearray(rng.randbytes(0x98))
            context[0], context[3], context[0xB] = (0, 1, 255)[shape % 3], state, (0, 1, 3, 127, 255, 128)[shape % 6]
            context[0x15], context[0x1F] = (0, 254, 255)[shape % 3], shape % 2
            struct.pack_into('<h', context, 0x30, (-32768, -1, 0, 1, 32767)[shape % 5])
            struct.pack_into('<H', context, 0x36, (0, 1, 255, 65535)[shape % 4])
            struct.pack_into('<I', context, 0x4C, shape % 2)
            struct.pack_into('<I', context, 0x60, ACTOR)
            actor = bytearray(rng.randbytes(1088))
            actor[0x31E] = (0, 1, 2, 255)[shape % 4]
            struct.pack_into('<I', actor, 0x60, MOTION)
            for index in range(3):
                struct.pack_into('<h', actor, 0x34E + index * 2, (-32768, -1, 0, 1, 32767)[(shape + index) % 5])
            frame = (-2, -1, 0, 1, 7, 15, 16, 32767)[shape % 8]
            clock = frame * 4096 + (shape * 97 % 4096)
            opponents = []
            for index in range(3):
                data = bytearray(rng.randbytes(1088))
                data[0x31E], data[0x31F] = (shape + index) % 4, (shape + index) % 3
                struct.pack_into('<I', data, 0x33C, (0, 1, 2, 3)[(shape + index) % 4])
                opponents.append(bytes(data))
            returns = {0x021EC670: shape % 3, 0x021F14E4: shape % 2,
                       0x021DBB14: shape % 3 == 0, 0x0220F868: shape % 3 == 1,
                       0x021DBB9C: shape % 4 != 0, 0x022168E8: shape % 4 != 1,
                       0x021E9D70: shape % 5 != 0}
            result.append({'seed': seed, 'context': bytes(context), 'actor': bytes(actor),
                           'opponents': opponents, 'flags': rng.randbytes(3),
                           'clock': clock, 'frames': (0, 1, 2, 16, 65535)[shape % 5],
                           'song': (-32768, -1, 0, 1, 32767)[shape % 5],
                           'eventHit': frame if shape % 4 == 0 else frame + 1,
                           'eventEnd': frame if shape % 4 == 1 else frame - 1,
                           'valid': [int((shape + index) % 3 != 0) for index in range(3)],
                           'spent': [int((shape + index) % 2 != 0) for index in range(3)],
                           'returns': returns})
    return result


def model(vector):
    context = bytearray(vector['context'])
    actor = bytearray(vector['actor'])
    opponents = [bytearray(item) for item in vector['opponents']]
    flags = bytearray(vector['flags'])
    calls = []

    def get(offset, kind='B'):
        return struct.unpack_from('<' + kind, context, offset)[0]

    def put(offset, value, kind='B'):
        if kind == 'B':
            value &= 255
        elif kind == 'h':
            value = signed(value, 16)
        struct.pack_into('<' + kind, context, offset, value)

    def call(address, *arguments):
        words = [value & 0xFFFFFFFF for value in arguments]
        calls.append({'address': address, 'arguments': words})
        if address == 0x0207AFEC:
            return DESCRIPTOR
        if address == 0x021D9534:
            return vector['eventHit'] if arguments[2] == 1 else vector['eventEnd']
        if address == 0x021DB438:
            return OPPONENTS + arguments[1] * 1088
        if address in (0x021DB8D0, 0x021DBD24):
            index = (arguments[0] - OPPONENTS) // 1088
            return vector['valid' if address == 0x021DB8D0 else 'spent'][index]
        return int(vector['returns'].get(address, 0))

    action = get(0x36, 'H')
    call(0x0207AFEC, action)
    other = int(actor[0x31E] == 0)
    call(0x021EAB48, actor[0x31E])
    if get(3) == 0:
        call(0x021D75D4, 19 if actor[0x31E] == 0 else 20)
        value = call(0x02042C2C, ACTOR)
        call(0x021D77B0, -1, value)
        call(0x021D94CC, 1, 1)
        if get(0) == 0:
            call(0x0202AC08, TIMER)
            if vector['song']:
                call(0x021EEA10, vector['song'], 0)
            if action == 0:
                call(0x021EEA10, 180, 0)
        put(0x30, vector['clock'] >> 12, 'h')
        put(0x15, 0)
        put(3, 10)
        put(0x4C, 0, 'I')
    if get(3) == 10:
        hit = call(0x021D9534, ACTOR, -1, 1, get(0x30, 'h'))
        end = call(0x021D9534, ACTOR, -1, 6, get(0x30, 'h'))
        frame = vector['clock'] >> 12
        if hit == frame:
            call(0x021EC03C, ACTOR, action)
            put(0x30, frame + 1, 'h')
            put(0x15, get(0x15) + 1)
            if call(0x021EC670, other) and get(0x4C, 'I') == 0:
                if call(0x021F14E4):
                    call(0x021EAA88, action)
                call(0x021EAB0C, 11, 0, 48, 2)
                put(0x4C, 1, 'I')
        elif frame == end:
            put(3, 20)
        elif frame >= vector['frames'] - 2:
            target = call(0x021DB438, int(actor[0x31E] == 0), 0)
            for index in range(3):
                data = opponents[index]
                if call(0x021DB8D0, target):
                    amount = struct.unpack_from('<h', actor, 0x34E + data[0x31F] * 2)[0]
                    call(0x0220F600, ACTOR, target, action, amount, 1)
                    if struct.unpack_from('<I', data, 0x33C)[0] & 2:
                        call(0x022024D4, data[0x31E], data[0x31F], 0)
                    call(0x021EA428, target, action)
                if struct.unpack_from('<h', actor, 0x34E + index * 2)[0] > 0:
                    call(0x021E2390, target)
                target += 1088
            if get(0xB, 'b') > 0:
                call(0x021EA398, 0, 249)
                put(0x19, 1)
            else:
                put(0x19, 0)
            put(3, 50)
    if get(3) == 20:
        if call(0x021F14E4):
            call(0x021F14A4)
        call(0x021EC620, ACTOR)
        put(3, 0)
        put(0, get(0) + 1)
        put(0x13, 7)
    if get(3) == 50:
        if call(0x021F14E4):
            call(0x021F14A4)
        if call(0x021DBB14, 0, other):
            put(3, 60)
        else:
            put(3, 60 if call(0x0220F868, int(actor[0x31E] == 0)) else 100)
        for index in range(3):
            target = call(0x021DB438, other, index)
            if call(0x021DB8D0, target) and call(0x021DBD24, target) == 0:
                flags[index] = 1
    if get(3) == 60:
        waiting = call(0x021DBB9C, 0, other) == 0
        waiting |= call(0x022168E8, 0, other) == 0
        if not waiting:
            put(3, 100)
    if get(3) == 100 and call(0x021E9D70):
        put(3, 200)
    if get(3) == 200:
        for index in range(3):
            target = call(0x021DB438, other, index)
            if call(0x021DB8D0, target):
                call(0x021DC5D4, target)
                struct.pack_into('<H', opponents[index], 0x34C, 0)
        call(0x021EAB34)
        put(3, 0)
        put(0, 0)
        if vector['song']:
            call(0x021EEB70, vector['song'])
        if action == 0:
            call(0x021EEB70, 180)
        call(0x0202AC4C, TIMER)
        if get(0x1F) == 0:
            call(0x021DC940, ACTOR, 8)
        put(0x13, 12)
    return bytes(context), [bytes(item) for item in opponents], bytes(flags), calls
