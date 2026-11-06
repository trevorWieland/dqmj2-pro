import itertools
import struct

ACTOR, INFO_A, INFO_B = 0x023A8000, 0x023A9000, 0x023A9200


def recipes():
    return [dict(seed=0x198000 + index, variant=index, selector=selector, family=family, early=early,
        final=[0, 1, 2, 128, 255][(index // 5) % 5], result=[0, 1, 0x80000000, 0xFFFFFFFF][index % 4])
        for index, (selector, family, early) in enumerate(itertools.product(
            [0, 1, 2, 3, 0x80000000, 0xFFFFFFFF], [0, 1, 2, 63, 0x80000000, 0xFFFFFFFF], [0, 1, 2, 128, 255]))]


def construct(recipe, rng):
    actor = bytearray(rng.randbytes(1088))
    a, b = bytearray(rng.randbytes(256)), bytearray(rng.randbytes(256))
    first_id = [-32768, -1, 0, 255, 32767][recipe['variant'] % 5]
    second_id = [32767, 255, 0, -1, -32768][recipe['variant'] % 5]
    struct.pack_into('<h', a, 0x2A, first_id)
    struct.pack_into('<h', b, 0x2A, second_id)
    struct.pack_into('<I', actor, 0x1E8, INFO_A)
    initial = [(ACTOR, bytes(actor)), (INFO_A, bytes(a)), (INFO_B, bytes(b))]
    services = []
    scalar = (recipe['variant'] * 0xE1020401) & 0xFFFFFFFF
    vector0, vector1 = rng.randbytes(12), rng.randbytes(12)

    def call(address, arguments, result, effects=(), expected_vector=None):
        services.append(dict(address=address, arguments=arguments, result=result, effects=list(effects), expectedVector=expected_vector))
        for address, content in effects:
            actor[address - ACTOR:address - ACTOR + len(content)] = content

    call(0x02044CDC, [first_id & 0xFFFFFFFF], recipe['selector'], [(ACTOR + 0x1E8, struct.pack('<I', INFO_B))])
    call(0x02044D14, [second_id & 0xFFFFFFFF], recipe['family'], [(ACTOR + 0x31E, bytes([recipe['early']]))])
    family = 0 if recipe['family'] == 63 else recipe['family']
    if family:
        identifier = 0x12 if recipe['early'] == 0 else 0x11
    else:
        identifier = {1: 0xF, 2: 0x10}.get(recipe['selector'], 0xE)
    call(0x021D75D4, [identifier], 0xFFFFFFFF,
        [(ACTOR + 0x8C, struct.pack('<I', scalar)), (ACTOR + 0x70, vector0), (ACTOR + 0x31E, b'\x80')])
    call(0x021D77B0, [0xFFFFFFFF, scalar], 0x80000000, [(ACTOR + 0x70, vector1)])
    call(0x021D7814, [0xFFFFFFFF, ACTOR + 0x70], 0,
        [(ACTOR + 0x31E, bytes([recipe['final']]))], vector1)
    call(0x021D94CC, [int(recipe['final'] == 0), int(recipe['final'] == 1)], recipe['result'], [(ACTOR + 0x31E, b'\xFE')])
    native = [dict(address='0x21db9e0', arguments=[ACTOR], result=recipe['selector']),
        dict(address='0x21dbaac', arguments=[ACTOR], result=family),
        dict(address='0x2042c2c', arguments=[ACTOR], result=scalar),
        dict(address='0x2041f74', arguments=[ACTOR, 0], result=ACTOR + 0x70)]
    return initial, bytes(actor), services, native
