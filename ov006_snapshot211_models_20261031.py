import random
import struct

CONTEXT = 0x0221C1B4
CALLS = [0x02003CF8, 0x02003D0C, 0x02003D20, 0x02003D44, 0x02003D68, 0x02003D7C, 0x02003D90,
    0x02003DCC, 0x02003DE0, 0x02003DF4, 0x02003E1C, 0x02003DA4, 0x02003DB8]


def recipes():
    return [dict(seed=0x211000 + index, result=[0, 1, 0x80000000, 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFF0001][index % 6]) for index in range(96)]


def construct(recipe):
    rng = random.Random(recipe['seed'])
    context = bytearray(rng.randbytes(52))
    initial = bytes(context)
    services = []

    def call(address, arguments, result, effects):
        services.append(dict(address=address, arguments=arguments, result=result, effects=effects, expectedContext=bytes(context)))
        for offset, content in effects:
            context[offset:offset + len(content)] = content

    for index, address in enumerate(CALLS):
        result = [0, 1, 0x80000000, 0xFFFFFFFF][(index + recipe['seed']) % 4] ^ rng.getrandbits(32)
        effects = [(4 * index, struct.pack('<I', result ^ 0xFFFFFFFF))]
        if index:
            effects.append((0, struct.pack('<I', rng.getrandbits(32))))
        if index == 12:
            effects.append((44, struct.pack('<I', rng.getrandbits(32))))
        call(address, [], result, effects)
        struct.pack_into('<I', context, index * 4, result)
    saved = struct.unpack_from('<I', context, 44)[0]
    call(0x020037DC, [saved], rng.getrandbits(32), [(44, rng.randbytes(4))])
    call(0x02204740, [], recipe['result'], [(8, rng.randbytes(12))])
    return initial, bytes(context), services
