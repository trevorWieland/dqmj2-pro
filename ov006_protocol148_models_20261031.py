import struct

ROOT_STATE, PACKET = 0x0221C164, 0x02350000
OBJECTS = [0x02360000, 0x02360100]
CALLBACKS = [0, 0x02390000, 0x023A0001]


def recipes():
    output = []
    for v in range(120):
        kind = v % 6
        output.append(dict(seed=0x148000 + v, variant=v, status=[1, 0x8000, 0xFFFF, 0, 0, 0][kind],
            callback=0 if kind < 4 else CALLBACKS[kind - 3], oldState=[0, 9, 10, 11][v // 6 % 4],
            sequence=[1, 16, 31, 32][(v // 24 + v // 6) % 4], value=0x1234 + v * 7, relation=v // 24 % 3,
            bitmap=[0, 0x8000, 1, 0xFFFF, 0x80000000][v // 6 % 5], requestReturn=[2, 24, 0, 0xFFFFFFFF, 0x10002][v // 24]))
    output += [dict(seed=0x148100 + i, variant=120 + i, status=0, callback=0, oldState=0, sequence=1, value=0x2222, relation=i % 3, bitmap=0xFFFF, requestReturn=result)
        for i, result in enumerate([0, 2, 24, 0xFFFFFFFF, 0x10002])]
    return output


def construct(recipe, raw_packet, raw_objects):
    v = recipe['variant']
    packet = bytearray(raw_packet)
    objects = [bytearray(raw_objects[i * 128:(i + 1) * 128]) for i in range(2)]
    struct.pack_into('<H', packet, 2, recipe['status'])
    struct.pack_into('<HH', packet, 8, recipe['sequence'], recipe['value'])
    sequence = recipe['sequence'] % 32 + 1 if recipe['callback'] else recipe['sequence']
    value = 0x8000 + v * 13 if recipe['callback'] else recipe['value']
    minimum = [value - 1, value, value + 1][recipe['relation']]
    for record in objects:
        struct.pack_into('<I', record, 0x40, recipe['oldState'])
        struct.pack_into('<HH', record, 0x5E, minimum, 0xA5A5)
    initial = [(ROOT_STATE, struct.pack('<II', recipe['callback'], OBJECTS[0])), (PACKET, bytes(packet))]
    initial += [(address, bytes(record)) for address, record in zip(OBJECTS, objects)]
    plan, pointer = [], 0

    def native(address, arguments):
        plan.append(dict(kind='native', address=address, arguments=arguments))

    def provided(address, arguments, result=0, effects=()):
        plan.append(dict(kind='provided', address=address, arguments=arguments, result=result, effects=list(effects)))

    def error(code):
        native(0x022012C0, [code])
        if struct.unpack_from('<I', objects[pointer], 0x40)[0] not in (9, 10):
            struct.pack_into('<I', objects[pointer], 0x54, code)

    def state(code):
        native(0x02201270, [code])
        struct.pack_into('<I', objects[pointer], 0x40, code)
        return OBJECTS[pointer]

    if recipe['status']:
        error(recipe['status'])
        result = state(9)
    else:
        if recipe['callback']:
            provided(recipe['callback'] & ~1, [0x08000000, 0x0220E7B8, recipe['sequence'], recipe['value']],
                0xFFFFFFFF, [(PACKET + 8, struct.pack('<HH', sequence, value)), (ROOT_STATE, struct.pack('<II', 0, OBJECTS[1]))])
            packet[8:12] = struct.pack('<HH', sequence, value)
            pointer = 1
        mask = (1 << (sequence - 1)) & 65535
        if minimum > value:
            struct.pack_into('<HH', objects[pointer], 0x5E, value, mask)
        elif minimum == value:
            struct.pack_into('<H', objects[pointer], 0x60, 0xA5A5 | mask)
        native(0x022018BC, [(sequence + 1) & 65535])
        if v & 1:
            pointer ^= 1
        provided(0x02012290, [], recipe['bitmap'], [(ROOT_STATE + 4, struct.pack('<I', OBJECTS[pointer]))])
        bitmap = recipe['bitmap']
        if bitmap in (0, 0x8000):
            error(22 if bitmap == 0 else 3)
            state(9)
            helper = 24 if bitmap == 0 else 3
        else:
            next_sequence = (sequence + 1) & 65535

            def bit(index):
                amount = (index - 1) & 255
                return (1 << amount) & 0xFFFFFFFF if amount < 32 else 0

            found = bool(bit(next_sequence) & bitmap)
            while not found:
                next_sequence = (next_sequence + 1) & 65535
                if next_sequence > 16:
                    break
                found = bool(bit(next_sequence) & bitmap)
            if not found:
                helper = 24
            else:
                pointer ^= 1
                provided(0x022019BC, [0x0220192D, next_sequence], recipe['requestReturn'],
                    [(ROOT_STATE + 4, struct.pack('<I', OBJECTS[pointer]))])
                helper = recipe['requestReturn'] & 65535
        result = state(7) if helper == 24 else state(9) if helper != 2 else 2
    expected = [(PACKET, bytes(packet))] + [(address, bytes(record)) for address, record in zip(OBJECTS, objects)]
    expected += [(ROOT_STATE, struct.pack('<II', 0 if recipe['callback'] and recipe['status'] == 0 else recipe['callback'], OBJECTS[pointer]))]
    return initial, expected, plan, result
