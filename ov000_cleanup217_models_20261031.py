import random
import struct

CONTEXT = 0x02236950


def recipes():
    return [dict(seed=0x217000+i) for i in range(128)]


def construct(recipe):
    rng = random.Random(recipe['seed'])
    state = bytearray(rng.randbytes(40))
    initial = bytes(state)
    services = []

    def call(address, arguments):
        effects = [(rng.randrange(0, 10)*4, rng.randbytes(4))]
        event = dict(address=address, arguments=arguments, result=rng.getrandbits(32), effects=effects, expectedContext=bytes(state))
        services.append(event)
        for offset, content in effects:
            state[offset:offset+len(content)] = content

    def word(offset):
        return struct.unpack_from('<I', state, offset)[0]

    call(0x021EAA80, [0x1B2])
    call(0x021EAA80, [0x13B])
    call(0x02028DAC, [word(12)])
    call(0x020410A8, [word(16)])
    call(0x02043070, [2])
    call(0x0207AAD0, [2])
    call(0x02062328, [])
    call(0x0206DEC8, [])
    state[2] = 0
    call(0x020406A8, [0])
    call(0x02061898, [])
    empty_input = services[-1]['result']
    call(0x0202A164, [2])
    for offset in [24, 8, 32, 16, 12, 20]:
        call(0x0202A498, [1, word(offset)])
    call(0x0202A164, [1])
    state[1] = 0
    return initial, bytes(state), services, empty_input
