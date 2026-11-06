import itertools
import struct

SPECS = {'020d2e68': {}}
SP, STOP = 0x027f0000, 0x027e0000
STATE, TEXT, CONTEXT = 0x021d7098, 0x021d70a4, 0x021c9698
POSITION, DESCRIPTOR = SP - 52, SP - 48
HANDLES, OBJECTS = 0x02402000, 0x02404000


def fixtures(name):
    return [dict(values=values, packed=packed, mutate=mutate, alternateHandles=alternate)
            for values, packed, mutate, alternate in itertools.product(range(6), range(7), [False, True], [False, True])]


def state_data(fixture, phase):
    n = phase if fixture['mutate'] else 0
    raw = bytearray((j * 37 + fixture['values'] * 19 + n * 11) & 255 for j in range(64))
    choices = [[0, 0, 0, 0], [1, 1, 1, 1], [99999, 99999, 99999, 99999], [100000, 100000, 100000, 100000],
               [0, 99999, 100000, 0xffffffff], [0xffffffff, 0, 1, 99998]]
    values = choices[(fixture['values'] + n) % len(choices)]
    for offset, value in zip([52, 40, 44, 48], values):
        struct.pack_into('<I', raw, offset, value)
    numbers = [0, 511, 512, 998, 999, 1000, 1023]
    fields = [numbers[(fixture['packed'] + n + i * 2) % len(numbers)] for i in range(4)]
    struct.pack_into('<2H', raw, 32, (0x8123 + n * 17 + fixture['values']) & 65535, (0x9abc + n * 29 + fixture['packed']) & 65535)
    struct.pack_into('<I', raw, 36, (0x92340000 + n * 97 + fixture['packed']) & 0xffffffff)
    struct.pack_into('<I', raw, 56, fields[0] | fields[1] << 10 | fields[2] << 20 | (n % 4) << 30)
    struct.pack_into('<I', raw, 60, fields[3] | 0xdead0000 & ~1023)
    return bytes(raw)


def scenario(fixture):
    regions = {
        STATE: bytearray(state_data(fixture, 0)),
        HANDLES: bytearray(256),
        OBJECTS: bytearray((i * 23 + 0x51) & 255 for i in range(1536)),
    }
    for bank in range(2):
        for i in range(22):
            obj = OBJECTS + bank * 512 + i * 16
            struct.pack_into('<I', regions[HANDLES], bank * 128 + i * 4, obj)
            struct.pack_into('<I', regions[OBJECTS], obj - OBJECTS + 4, 0x02410000 + bank * 0x1000 + i * 0x20)
    initial = {base: bytes(raw) for base, raw in regions.items()}
    actions = []
    position = bytes(4)
    descriptor = None
    exposed = False

    def write(at, data):
        for base, raw in regions.items():
            if base <= at and at + len(data) <= base + len(raw):
                raw[at - base:at - base + len(data)] = data
                return
        raise ValueError('Independent state mutation escaped its measured view')

    def provider(address, args, returned=None, extras=(), checks=(), output=None):
        nonlocal position, descriptor
        n = len(actions)
        mutations = []
        if fixture['mutate']:
            data = state_data(fixture, n + 1)
            write(STATE, data)
            mutations.append((STATE, data))
        for at, data in extras:
            write(at, data)
            mutations.append((at, data))
        if output is not None:
            descriptor = output
            mutations.append((DESCRIPTOR, output))
        if exposed and fixture['mutate']:
            position = struct.pack('<2H', (n * 31 + fixture['packed']) & 65535, (n * 17 + fixture['values']) & 65535)
            mutations.append((POSITION, position))
            descriptor = bytes((v + n + 1) & 255 for v in descriptor)
            mutations.append((DESCRIPTOR, descriptor))
        result = returned if returned is not None else (0xa5100000 + n * 257 + fixture['values']) & 0xffffffff
        actions.append(dict(address=address, args=list(args), returned=result, mutations=mutations, checks=list(checks)))
        return result

    for phase in range(2):
        for i in range(22):
            bank = phase if fixture['alternateHandles'] else 0
            handle = HANDLES + bank * 128 + i * 4
            object_bank = (bank + int(fixture['mutate']) + phase) % 2
            obj = OBJECTS + object_bank * 512 + i * 16
            provider(0x02061dcc, [i + 6], handle, extras=[(handle, struct.pack('<I', obj))])
            if phase == 0:
                other = OBJECTS + (1 - object_bank) * 512 + i * 16
                provider(0x02049f4c, [handle], extras=[(handle, struct.pack('<I', other))] if fixture['mutate'] else [])
            else:
                content = struct.unpack_from('<I', regions[OBJECTS], obj - OBJECTS + 4)[0]
                provider(0x02049ffc, [content])
    before_text = bytes(regions[STATE][12:28])
    formatted = b''.join(struct.pack('<H', value + 0x4100) for value in before_text)
    provider(0x02046af4, [CONTEXT, TEXT, 16, 0, DESCRIPTOR, 255], checks=[(POSITION, position), (TEXT, before_text)], output=formatted)
    provider(0x0204ab98, [6, POSITION, 1, DESCRIPTOR, 0], checks=[(POSITION, position), (DESCRIPTOR, descriptor)])
    exposed = True

    def draw(tag, style, token, flag):
        provider(0x0204aaf0, [tag, POSITION, 15, style, token, 1, flag], checks=[(POSITION, position)])

    draw(8, 12, 16, 0)
    draw(7, 15, struct.unpack_from('<H', regions[STATE], 34)[0], 1)
    for label, tag, token, offset in [(15, 16, 20, 52), (9, 10, 17, 40), (11, 12, 18, 44), (13, 14, 19, 48)]:
        draw(label, 12, token, 0)
        value = struct.unpack_from('<I', regions[STATE], offset)[0]
        if value == 0:
            draw(tag, 2, 122, 1)
        else:
            provider(0x02048094, [min(value, 99999), 0])
            draw(tag, 12, 22, 1)
    draw(17, 12, 23, 0)

    def packed(offset, shift, tag, token):
        value = struct.unpack_from('<I', regions[STATE], offset)[0] >> shift & 1023
        provider(0x02048094, [min(value, 999), 0])
        draw(tag, 12, token, 1)

    packed(56, 0, 18, 13)
    packed(56, 10, 19, 14)
    draw(20, 12, 24, 0)
    packed(60, 0, 21, 13)
    draw(22, 12, 25, 0)
    packed(56, 20, 23, 15)
    draw(24, 12, 26, 1)
    provider(0x020d28cc, [25, struct.unpack_from('<I', regions[STATE], 36)[0]])
    draw(26, 12, 27, 1)
    result = provider(0x020d2a14, [27, struct.unpack_from('<H', regions[STATE], 32)[0]])
    return dict(initial=initial, regions={base: bytes(raw) for base, raw in regions.items()}, actions=actions, result=result,
                position=position, descriptor=descriptor, nativeCalleeBodiesExecuted=0)
