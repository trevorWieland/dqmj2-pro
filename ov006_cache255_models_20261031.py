import random
import struct
CONTEXT = 35714452
RUNTIME = 34634144
POINTER = 35359456
NATIVE = {33941060: 40, 33941100: 24, 33945052: 24, 33941308: 36, 33941416: 60, 33941524: 48, 33590648: 148}

def recipes():
    return [dict(seed=2445312 + index, argument=argument, kind=kind, variant=variant) for index, (argument, kind, variant) in enumerate(((a, k, v) for a in [0, 1, 15, 2147483647, 2147483648, 4294967295] for k in range(3) for v in range(4)))]

def construct(recipe):
    rng = random.Random(recipe['seed'])
    argument = recipe['argument']
    variant = recipe['variant']
    kind = recipe['kind']
    state = {CONTEXT: bytearray(rng.randbytes(92)), RUNTIME: bytearray(rng.randbytes(312)), POINTER: bytearray(rng.randbytes(8))}
    old = [4294967295, argument, argument ^ 1][kind]

    def word(a, value):
        base = next((b for b, x in state.items() if b <= a < a + 4 <= b + len(x)))
        struct.pack_into('<I', state[base], a - base, value & 4294967295)

    def load(a):
        base = next((b for b, x in state.items() if b <= a < a + 4 <= b + len(x)))
        return struct.unpack_from('<I', state[base], a - base)[0]

    def snapshot():
        return [(a, bytes(b)) for a, b in state.items()]
    word(CONTEXT + 88, old)
    word(RUNTIME + 8, [4294967295, 0, 2147483647, 2147483648][variant])
    word(POINTER + 4, 39911424 + variant * 16)
    initial = snapshot()
    services = []
    native = []

    def provider(address, arguments, result=None):
        effects = [(CONTEXT + 88, rng.randbytes(4)), (CONTEXT + 84, rng.randbytes(4)), (RUNTIME + 8, rng.randbytes(4)), (RUNTIME + 24, rng.randbytes(4))]
        value = rng.getrandbits(32) if result is None else result & 4294967295
        services.append(dict(address=address, arguments=arguments, result=value, effects=effects, before=snapshot()))
        for a, data in effects:
            base = next((b for b, x in state.items() if b <= a and a + len(data) <= b + len(x)))
            state[base][a - base:a - base + len(data)] = data
        return value

    def call(address, arguments, body):
        event = dict(address=address, arguments=arguments, before=snapshot())
        native.append(event)
        value = body() & 4294967295
        event['result'] = value
        return value

    def first():
        value = load(RUNTIME + 8)
        if not value & 2147483648:
            provider(33945076, [value])
        return load(RUNTIME + 8)

    def second():
        value = call(33945052, [], lambda: provider(33782780, [load(POINTER + 4)]))
        word(RUNTIME + 24, value)
        return value

    def third(value):
        result = provider(33943692, [value, 255], [0, 1, 2147483648, 4294967295][variant])
        if result:
            return 1
        provider(33945656, [])
        return 0

    def fourth(value):
        index = provider(33943868, [0, value, 4294967295, 4294967295], [4294967295, 0, 15, 2147483648][variant])
        if not index & 2147483648:
            destination = RUNTIME + 56 + index * 16

            def clear():
                state[RUNTIME][destination - RUNTIME:destination - RUNTIME + 16] = bytes(16)
                return destination + 16
            call(33590648, [destination, 0, 16], clear)
        provider(33945656, [])
        return index

    def replace():
        value = provider(33945356, [0], [0, 2147483647, 2147483648, 4294967295][variant])
        provider(33945248, [0, 0, 15])
        return value
    if old == 4294967295:
        word(CONTEXT + 88, argument)
        call(33941060, [], first)
        call(33941100, [], second)
        value = load(CONTEXT + 88)
        call(33941308, [value], lambda: third(value))
        value = load(CONTEXT + 88)
        result = call(33941416, [0, value], lambda: fourth(value))
    elif old == argument:
        result = argument
    else:
        word(CONTEXT + 88, argument)
        word(CONTEXT + 84, 15)
        result = call(33941524, [0, 0, 15], replace)
    return (initial, snapshot(), services, native, result)
