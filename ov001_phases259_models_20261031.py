import functools
import hashlib
import random
import struct
from project import ROOT
SHARED = 35905672
TABLE = 36700160
POINTER = 35400372
DESCRIPTORS = 37224448
SPECS = {35698940: dict(bytes=228, counter=22, phase=0), 35703276: dict(bytes=196, counter=11, phase=12)}
NATIVE = {35698544: 16, 35698508: 16, 35698580: 16, 35501112: 124, 33971592: 24}

@functools.lru_cache(maxsize=1)
def item_table():
    from ndspy.rom import NintendoDSRom
    raw = bytes(NintendoDSRom((ROOT / 'inputs/game.nds').read_bytes()).getFileByName('ItemTbl.bin'))
    if raw[:8] != b'ITEM\x00\x01\x00\x00' or len(raw) != 8 + 256 * 88:
        raise ValueError('Phases259 ItemTbl header/256rows differs')
    return raw

def recipes(address):
    phases = [0, 10, 20, 100, 255] if address == 35698940 else [0, 10, 100, 255]
    return [dict(seed=2461696 + address + phase * 257 + counter, counter=counter, phase=phase, initialR0=address * counter + phase * 65537 & 4294967295) for phase in phases for counter in range(256)]

def construct(address, recipe):
    rng = random.Random(recipe['seed'])
    spec = SPECS[address]
    state = {SHARED: bytearray(rng.randbytes(64))}
    state[SHARED][spec['phase']] = recipe['phase']
    state[SHARED][spec['counter']] = recipe['counter']
    state[SHARED][27] = recipe['counter']

    def snapshot():
        return [(a, bytes(b)) for a, b in state.items()]
    services = []
    native = []

    def provider(entry, args, result=None):
        effects = [(SHARED, bytearray(rng.randbytes(64)))]
        if entry == 35534212:
            effects[0][1][0] = [20, 100, 10, 255][recipe['counter'] // 4 % 4]
        effects = [(a, bytes(data)) for a, data in effects]
        value = rng.getrandbits(32) if result is None else result
        services.append(dict(address=entry, arguments=args, result=value, effects=effects, before=snapshot()))
        for a, data in effects:
            state[a][:] = data
        return value

    def getter(entry, offset):
        value = state[SHARED][offset]
        native.append(dict(address=entry, arguments=[], result=value, before=snapshot()))
        return value
    if address == 35698940:
        initial = snapshot()
        if state[SHARED][0] == 0:
            selected = getter(35698544, 27)
            provider(35590996, [4, 0, selected, 1])
            provider(35698868, [])
            provider(35534180, [24, 1])
            state[SHARED][0] = 10
        if state[SHARED][0] == 10 and provider(35534212, [], [0, 1, 2147483648, 4294967295][recipe['counter'] % 4]):
            provider(35534180, [25, 1])
            state[SHARED][22] = 0
            state[SHARED][0] = 20
        if state[SHARED][0] == 20:
            state[SHARED][22] = state[SHARED][22] + 1 & 255
            if state[SHARED][22] > 30:
                state[SHARED][0] = 100
        if state[SHARED][0] == 100:
            provider(35591332, [])
            state[SHARED][0] = 0
            state[SHARED][3] = 3
    else:
        state[SHARED][26] = recipe['counter'] % 4
        state[SHARED][28] = recipe['counter'] // 4 % 3
        state[POINTER] = bytearray(struct.pack('<I', TABLE))
        state[TABLE] = bytearray(item_table()[8:])
        for side, base in enumerate([35876716, 35873452, 35870188, 35879980]):
            for slot in range(3):
                descriptor = DESCRIPTORS + (side * 3 + slot) * 256
                state[base + slot * 1088 + 488] = bytearray(struct.pack('<I', descriptor))
                state[descriptor] = bytearray(rng.randbytes(192))
        initial = snapshot()
        if state[SHARED][12] == 0:
            selected = getter(35698544, 27)
            side = getter(35698508, 26)
            slot = getter(35698580, 28)
            actor = [35876716, 35873452, 35870188, 35879980][side] + slot * 1088
            native.append(dict(address=35501112, arguments=[side, slot], result=actor, before=snapshot()))
            native.append(dict(address=33971592, arguments=[selected], result=TABLE + selected * 88, before=snapshot()))
            descriptor = struct.unpack('<I', state[actor + 488])[0]
            state[descriptor][176] = state[TABLE][selected * 88 + 42]
            state[SHARED][11] = 0
            state[SHARED][12] = 10
        if state[SHARED][12] == 10:
            state[SHARED][11] = state[SHARED][11] + 1 & 255
            if state[SHARED][11] > 30:
                state[SHARED][12] = 100
        if state[SHARED][12] == 100:
            state[SHARED][12] = 0
            state[SHARED][3] = 14
    return (initial, snapshot(), services, native, 0)
