import random
import struct
ACTOR = 36704256
RNG_STATE = 34562116
ENTRY = 35833600
GETTER = 35503344
RNG = 33804948
DIVIDE = 33710928

def recipes():
    return [dict(seed=2564096 + i * 8 + j, stat=stat, rngWord=word) for i, stat in enumerate([-2147483648, -32768, -9999, -11, -10, -9, -1, 0, 1, 9, 10, 11, 99, 100, 9999, 32767, 2147483647]) for j, word in enumerate([0, 1, 2, 2147483647, 2147483648, 4294967295, 305419896, 3735928559])]

def construct(recipe):
    rng = random.Random(recipe['seed'])
    state = {ACTOR: bytearray(rng.randbytes(64)), RNG_STATE: bytearray(struct.pack('<I', recipe['rngWord'] ^ 4294967295))}

    def snapshot():
        return [(a, bytes(b)) for a, b in state.items()]
    initial = snapshot()
    effects = [(ACTOR, rng.randbytes(64)), (RNG_STATE, struct.pack('<I', recipe['rngWord']))]
    services = [dict(address=GETTER, arguments=[ACTOR], result=recipe['stat'] & 4294967295, effects=effects, before=snapshot())]
    for a, b in effects:
        state[a][:] = b
    bound = abs(recipe['stat']) // 10 * (-1 if recipe['stat'] < 0 else 1)
    after = recipe['rngWord'] * 1103515245 + 12345 & 4294967295
    value = 0 if bound <= 0 else (after >> 16) % bound
    native = [dict(address=RNG, arguments=[bound & 4294967295], result=value, before=snapshot())]
    state[RNG_STATE][:] = struct.pack('<I', after)
    if bound > 0:
        native.append(dict(address=DIVIDE, arguments=[after >> 16, bound], result=(after >> 16) // bound, remainder=value, before=snapshot()))
    return (initial, snapshot(), services, native, value + 1)
