import random
import struct

CONTEXT = 0x0221C0EC
TABLE = 0x0220B73E
OBJECTS = [0x023D0000, 0x023D0100]


def recipes():
    return [dict(seed=0x218000+i, index=[0, 1, 7, 14, 28][i%5], rawInput=[0, 1, 28, 29, 65535][i//5%5], result=[0, 1, 0x80000000, 0xFFFFFFFF][i%4]) for i in range(160)]


def construct(recipe, table):
    rng = random.Random(recipe['seed'])
    state = {CONTEXT:bytearray(rng.randbytes(16)), **{a:bytearray(rng.randbytes(32))for a in OBJECTS}}
    struct.pack_into('<H', state[CONTEXT], 4, recipe['rawInput'])
    struct.pack_into('<I', state[CONTEXT], 8, OBJECTS[0])
    initial = [(a, bytes(b))for a,b in state.items()]
    services = []

    def word(address, offset):
        return struct.unpack_from('<I', state[address], offset)[0]

    def object_word(offset):
        return word(word(CONTEXT, 8), offset)

    def call(address, arguments, result=None):
        effects = [(CONTEXT+8, struct.pack('<I', OBJECTS[(len(services)+1)%2])),
            (OBJECTS[0]+8, rng.randbytes(4)), (OBJECTS[1]+8, rng.randbytes(4)),
            (OBJECTS[0]+20, rng.randbytes(4)), (OBJECTS[1]+20, rng.randbytes(4))]
        services.append(dict(address=address, arguments=arguments, result=rng.getrandbits(32)if result is None else result,
            effects=effects, expectedState=[(a, bytes(b))for a,b in state.items()]))
        for a,b in effects:
            base=next(base for base,data in state.items()if base<=a and a+len(b)<=base+len(data))
            state[base][a-base:a-base+len(b)]=b

    index=recipe['index']
    call(0x02002480, [recipe['rawInput'], 29], index)
    call(0x0220383C, [object_word(20), 0])
    for slot in range(5):
        call(0x021FAC5C, [index+slot, slot])
    call(0x021FE510, [(object_word(8)+table[index]*2)&0xFFFFFFFF, 0, 30, 19])
    for slot in range(5):
        call(0x021FAD68, [index+slot, slot])
    call(0x021FE4FC, [])
    call(0x022038AC, [object_word(20)])
    call(0x021FB080, [], recipe['result'])
    return initial, [(a,bytes(b))for a,b in state.items()], services
