import random
import struct

INPUT, ENTITY = 0x023E0000, 0x023E1000
STATES = {
    0x021E54A0: (0x20, [0, 1, 2, 3, 12, 19, 4, 255]),
    0x021E5638: (0x18, [0, 10, 20, 30, 35, 40, 50, 60, 70, 100, 255]),
    0x021E5E04: (0x10, [0, 5, 10, 20, 100, 255]),
    0x021E5F88: (0x0E, [0, 10, 20, 50, 60, 70, 100, 255]),
    0x021E634C: (9, [0, 1, 15, 16, 17, 18, 19, 255]),
}


def signed8(value):
    return (value & 127) - (value & 128)


def signed32(value):
    return value if value < 0x80000000 else value - 0x100000000


def vectors(address):
    offset, states = STATES[address]
    for state in states:
        for variant in range(64):
            seed = 2026102941000 + address + state * 64 + variant
            rng = random.Random(seed)
            context = bytearray(rng.randbytes(0x38))
            for field in (3, 13, 15):
                context[field] = [0, 1, 2, 59, 60, 61, 254, 255][variant % 8]
            context[6] = context[0x19] = [0, 1, 17, 18, 127, 128, 254, 255][(variant // 3) % 8]
            context[10] = (variant // 8) & 1
            struct.pack_into('<h', context, 0x28, [-32768, -1, 0, 1, 179, 180, 32767, 2][variant % 8])
            context[offset] = state
            returns = {0x0202A634: INPUT, 0x021F1A44: ENTITY,
                0x0205E7A8: [0, 127, 128, 255][(variant // 2) % 4],
                0x021E3BE4: [0, 127, 128, 255][variant % 4],
                0x02041800: [0, 1, 2, 0xFFFFFFFF][variant % 4],
                0x02041814: [0, 1, 2, 0xFFFFFFFF][(variant // 2) % 4],
                0x021F14E4: variant & 1, 0x021D774C: (variant // 2) & 1,
                0x0205F2D8: (variant // 4) & 1, 0x021DB8B8: variant & 1,
                0x021DB578: [0xFFFFFFFF, 0, 1, 0x7FFFFFFF][variant % 4],
                0x021D80C0: variant & 1}
            yield {'seed': seed, 'context': bytes(context), 'argument': [0, 1, 8, 9, 10, 11, 0xFFFFFFFF, 0x80000000][variant // 8],
                   'keys': [0, 1, 8, 16, 0x1000, 0x8000, 0xFF7, 0xFFFF][variant // 8],
                   'entityWord': [0, 1, 0xFFFFFFFF, 0x80000000][(variant // 2) % 4], 'returns': returns}


def model(address, vector):
    c = bytearray(vector['context'])
    entity = bytearray(0x40)
    struct.pack_into('<I', entity, 0x1C, vector['entityWord'])
    entity[0x23] = 7
    calls = []
    arg, keys = vector['argument'], vector['keys'] & 0xFF7

    def call(target, *arguments):
        calls.append({'address': target, 'arguments': [value & 0xFFFFFFFF for value in arguments]})
        return vector['returns'].get(target, 0)

    def start():
        call(0x021D75D4, 46)
        call(0x021D7D58, 46, 0)
        call(0x021D7DC4, 46, 0)

    def fade(ticks=30, mode=2):
        call(0x02041510, 1, 2, ticks)
        call(0x022139E8, mode)

    if address == 0x021E54A0:
        call(0x0202A634)
        if c[0x20] == 0:
            for target, arguments in [(0x021D75D4, (42,)), (0x021D94CC, (1, 0)),
                (0x021E3564, (20, 1)), (0x02202654, ()), (0x021DC8E8, (0,))]:
                call(target, *arguments)
            c[0x1F], c[0x20] = 0, 1
        state = c[0x20]
        if state == 1 and c[10]:
            c[0x1C] = call(0x0205E7A8, -1, 58) & 255
            c[0x1B], c[0x20], c[0x19] = 20, 3, 18
            call(0x021F1354, 1, 0, 11, 1)
            call(0x02212858, signed8(c[0x1C]))
        elif state == 3 and keys:
            call(0x021F14A4)
            c[0x20] = 2
        elif state == 2 and signed8(c[0x19]) <= 0:
            call(0x02041510, 1, 2, 30)
            c[0x20] = 12
            call(0x022023C4, 0x400)
        elif state == 12 and call(0x02041800) != 1:
            c[0x20] = 19
        if c[0x20] == 19:
            c[0x16], c[0x20] = 17, 0
        if signed8(c[0x19]) > 0:
            c[0x19] -= 1
    elif address in (0x021E5638, 0x021E5F88):
        long_path = address == 0x021E5638
        state_offset, counter, handle = (0x18, 3, 0) if long_path else (14, 13, 12)
        state = c[state_offset]
        if state == 0:
            start()
            c[counter], c[state_offset] = 0, 10
        elif state == 10:
            c[counter] = (c[counter] + 1) & 255
            if c[counter]:
                c[state_offset] = 20
        elif long_path and state == 20:
            call(0x021D75D4, 48)
            call(0x021D77B0, -1, 0xB4000)
            call(0x021D94CC, 1, 0)
            call(0x021F1354, 1, 0, 10, 1)
            c[counter], c[state_offset] = 0, 30
        elif long_path and state == 30:
            c[counter] = (c[counter] + 1) & 255
            if c[counter] > 60:
                call(0x021F14A4)
                c[state_offset] = 35
        elif long_path and state == 35:
            if call(0x021F14E4) == 0:
                c[state_offset] = 40
        elif state == (40 if long_path else 20):
            call(0x021D75D4, 42)
            if long_path:
                message, scene, text = (20, 11, 58) if arg == 8 else (21, 12, 59) if arg == 9 else (20, 13, 58)
            else:
                message, scene, text = (20, 14, 58) if arg == 11 else (21, 15, 59) if arg == 10 else (21, 16, 58)
            call(0x021E3564, message, 1)
            call(0x021F1354, 1, 0, scene, 1)
            c[handle] = call(0x0205E7A8, -1, text) & 255
            c[state_offset] = 50
        elif state == 50:
            call(0x0202A634)
            if keys:
                c[state_offset] = 60
            if call(0x021D774C, -1) == 0:
                c[state_offset] = 60
        elif state == 60 and call(0x0205F2D8, signed8(c[handle])) == 0:
            call(0x0205F210, signed8(c[handle]), 30)
            call(0x02041510, 1, 2, 30)
            call(0x021F14A4)
            call(0x022139E8, 2)
            c[state_offset] = 70
        elif state == 70 and call(0x02041800) != 1:
            c[state_offset] = 100
        if c[state_offset] == 100:
            if long_path:
                if arg in (8, 9):
                    c[2] = arg - 8
            elif arg == 11:
                c[2] = 0
            elif arg != 10:
                c[2] = 5
            else:
                call(0x020443EC)
                c[2] = 2
            c[0x16], c[state_offset] = 17, 0
    elif address == 0x021E5E04:
        if c[16] == 0:
            start()
            if arg:
                call(0x021F1354, 1, 0, 17, 0)
                available = call(0x021DB8B8, 0) != 0 and signed32(call(0x021DB578, 2)) > 0
                call(0x021F1438, 0 if available else 1)
                c[15], c[16] = 0, 5
            else:
                c[16] = 10
        if c[16] == 5:
            c[15] = (c[15] + 1) & 255
            if c[15] > 60:
                call(0x021F14A4)
                c[16] = 10
        if c[16] == 10:
            fade(15, 1)
            c[16] = 20
        if c[16] == 20 and call(0x02041800) != 1 and call(0x02041814) != 1:
            c[16] = 100
        if c[16] == 100:
            c[2], c[0x16], c[16] = 6, 17, 0
    elif address == 0x021E634C:
        call(0x0202A634)
        if c[9] == 0:
            call(0x021E3B34)
            call(0x021D75D4, 42)
            call(0x021D94CC, 1, 0)
            call(0x021E3564, 20, 1)
            call(0x02202654)
            call(0x021DC8E8, 0)
            call(0x021DC8E8, 2)
            c[9] = 1
        state = c[9]
        if state == 1 and c[10]:
            c[8] = call(0x021E3BE4) & 255
            c[7] = call(0x0205E7A8, -1, 58) & 255
            call(0x021F1354, 1, 0, 11, 1)
            c[9], c[6] = 15, 18
            struct.pack_into('<h', c, 0x28, 180)
            call(0x02212858, signed8(c[7]))
        elif state == 15 and c[6] == 0 and (struct.unpack_from('<h', c, 0x28)[0] == 0 or keys):
            c[9] = 16
            call(0x021F14A4)
            call(0x021D75D4, 46)
        if c[9] == 16 and call(0x021D80C0):
            call(0x022139E8, 2)
            call(0x02041510, 1, 2, 30)
            c[9] = 17
        if c[9] == 17 and call(0x02041800) != 1:
            c[9] = 18
            call(0x021F1A44, signed8(c[8]))
            entity[0x23] = 0
        if c[9] == 18:
            call(0x021F1A44, signed8(c[8]))
            if vector['entityWord'] == 0:
                c[9] = 19
        if c[9] == 19:
            call(0x021E3BD0)
            c[0x16], c[9] = 15, 0
        if signed8(c[6]) > 0:
            c[6] -= 1
        timer = struct.unpack_from('<h', c, 0x28)[0]
        if timer > 0:
            struct.pack_into('<h', c, 0x28, timer - 1)
    else:
        raise ValueError('Unowned reward entry')
    call(0x0204437C)
    call(0x0204439C)
    return bytes(c), bytes(entity), calls
