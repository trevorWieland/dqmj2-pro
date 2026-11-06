import random
SHARED = 35905672
SEPARATE = 35952616
SPECS = {35701564: dict(bytes=184, counter=17, phase=18, service=35701368), 35704408: dict(bytes=184, counter=7, phase=19, service=35704076), 35704716: dict(bytes=184, counter=5, phase=6, service=35704592), 35832444: dict(bytes=188, counter=10, phase=11)}
NATIVE = {35698544: 16, 35698508: 16, 35698580: 16, 35501112: 124}

def recipes(address):
    phases = [0, 10, 100, 255] if address != 35832444 else [0, 20, 30, 100, 255]
    return [dict(seed=2453504 + address + phase * 257 + counter, counter=counter, phase=phase, initialR0=address * counter + phase * 65537 & 4294967295) for phase in phases for counter in range(256)]

def construct(address, recipe):
    rng = random.Random(recipe['seed'])
    spec = SPECS[address]
    base = SHARED if address != 35832444 else SEPARATE
    state = {SHARED: bytearray(rng.randbytes(64)), SEPARATE: bytearray(rng.randbytes(16))}
    state[base][spec['phase']] = recipe['phase']
    state[base][spec['counter']] = recipe['counter']
    if base == SHARED:
        state[SHARED][26] = [0, 1, 2, 3, 4, 255][(recipe['counter'] + recipe['phase']) % 6]
        state[SHARED][27] = recipe['counter']
        state[SHARED][28] = [0, 1, 2, 3, 4, 255][(recipe['counter'] // 6 + recipe['phase']) % 6]

    def snapshot():
        return [(a, bytes(b)) for a, b in state.items()]
    initial = snapshot()
    services = []
    native = []

    def provider(entry, args, result=None):
        effects = [(SHARED, rng.randbytes(64)), (SEPARATE, rng.randbytes(16))]
        if entry == 35831844:
            data = bytearray(effects[1][1])
            data[11] = [20, 100, 0, 30, 255][recipe['counter'] // 4 % 5]
            effects[1] = (SEPARATE, bytes(data))
        value = rng.getrandbits(32) if result is None else result
        services.append(dict(address=entry, arguments=args, result=value, effects=effects, before=snapshot()))
        for a, data in effects:
            state[a][:] = data
        return value

    def getter(entry, offset):
        value = state[SHARED][offset]
        native.append(dict(address=entry, arguments=[], result=value, before=snapshot()))
        return value
    if base == SHARED:
        selector = getter(35698544, 27)
        side = getter(35698508, 26)
        slot = getter(35698580, 28)
        actor = 0
        if slot != 4:
            actor = [35876716, 35873452, 35870188, 35879980][side] + slot * 1088 if side < 4 and slot < 3 else 0
            native.append(dict(address=35501112, arguments=[side, slot], result=actor, before=snapshot()))
        if state[base][spec['phase']] == 0:
            provider(spec['service'], [actor, side, selector])
            state[base][spec['counter']] = 0
            state[base][spec['phase']] = 10
        active_phase = 10
        final_mode_offset = 3
        final_mode = 14
    else:
        if state[base][11] == 0 and provider(35831844, [215, state[base][0], 48], [0, 1, 2147483648, 4294967295][recipe['counter'] % 4]):
            state[base][11] = 20
        if state[base][11] == 20:
            provider(35832256, [215, state[base][0]])
            state[base][10] = 0
            state[base][11] = 30
        active_phase = 30
        final_mode_offset = 1
        final_mode = 7
    if state[base][spec['phase']] == active_phase:
        state[base][spec['counter']] = state[base][spec['counter']] + 1 & 255
        if state[base][spec['counter']] > 45:
            state[base][spec['phase']] = 100
    if state[base][spec['phase']] == 100:
        state[base][spec['phase']] = 0
        state[base][final_mode_offset] = final_mode
    return (initial, snapshot(), services, native, 0)
