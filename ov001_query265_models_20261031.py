import functools
import random
import struct
from project import ROOT
CONTEXT = 35952616
BUFFER = 35952632
POINTER = 35415880
TABLE = 36700160
ENTRY = 35831844
SPECS = {ENTRY: dict(bytes=412)}
NATIVE = {34058220: 20}

@functools.lru_cache(maxsize=1)
def action_table():
    from ndspy.rom import NintendoDSRom
    raw = bytes(NintendoDSRom((ROOT / 'inputs/game.nds').read_bytes()).getFileByName('ActTbl.bin'))
    if raw[:8] != b'ACT\x00\x00\x01\x00\x00' or len(raw) != 8 + 256 * 40:
        raise ValueError('Query265 original ActTbl identity/rows differs')
    return raw

def recipes(address=ENTRY):
    return [dict(seed=2510848 + phase * 257 + counter, phase=phase, counter=counter, action=counter, selection=[0, 1, 127, 255, 256, 305419904, 2147483648, 4294967295][counter % 8], resource=4275878400 + counter & 4294967295, initialR0=counter) for phase in [0, 5, 10, 20, 30, 35, 40, 255] for counter in range(256)]

def construct(address, recipe):
    rng = random.Random(recipe['seed'])
    action = recipe['action']
    selection = recipe['selection']
    resource = recipe['resource']
    row = action * 40
    state = {CONTEXT: bytearray(rng.randbytes(16)), BUFFER: bytearray(rng.randbytes(64)), POINTER: bytearray(struct.pack('<I', TABLE)), TABLE: bytearray(action_table()[8:])}
    state[CONTEXT][12] = recipe['counter']
    state[CONTEXT][13] = recipe['phase']

    def snapshot():
        return [(a, bytes(b)) for a, b in state.items()]

    def word():
        return struct.unpack_from('<h', state[TABLE], row + 12)[0]
    initial = snapshot()
    native = [dict(address=34058220, arguments=[action], result=TABLE + row, before=snapshot())]
    services = []
    result = 0

    def provider(entry, args, returned=None):
        payload = bytearray(rng.randbytes(16))
        payload[13] = [30, 35, 40, 100, 255][recipe['counter'] // 8 % 5]
        effects = [(CONTEXT, bytes(payload)), (BUFFER, rng.randbytes(64)), (TABLE + row + 12, struct.pack('<h', [0, -1, 32767, -32768][recipe['counter'] % 4]))]
        value = rng.getrandbits(32) if returned is None else returned & 4294967295
        services.append(dict(address=entry, arguments=args, result=value, effects=effects, before=snapshot()))
        for a, data in effects:
            base = next((b for b, x in state.items() if b <= a and a + len(data) <= b + len(x)))
            state[base][a - base:a - base + len(data)] = data
        return value
    if state[CONTEXT][13] == 0:
        provider(35487572, [selection])
        provider(35590996, [1, 0, resource, 1])
        provider(35591188, [selection & 255])
        provider(35591224, [])
        state[CONTEXT][12] = 0
        state[CONTEXT][13] = 5
    if state[CONTEXT][13] == 5:
        state[CONTEXT][12] = state[CONTEXT][12] + 1 & 255
        if state[CONTEXT][12] > 30:
            state[CONTEXT][13] = 10
    if state[CONTEXT][13] == 10:
        if word() != 0:
            provider(33729544, [BUFFER])
            provider(35580432, [word() & 4294967295, 0])
        state[CONTEXT][13] = 20
    elif state[CONTEXT][13] == 20:
        if word() != 0:
            provider(33933572, [])
            value = provider(35831636, [action, selection], [0, 127, 128, 255, 2147483649, 4294967295][recipe['counter'] // 8 % 6])
            state[CONTEXT][14] = value & 255
        state[CONTEXT][13] = 30
    if state[CONTEXT][13] == 30:
        if word() == 0 or provider(33937140, [(state[CONTEXT][14] & 127) - (state[CONTEXT][14] & 128) & 4294967295], [0, 1, 2147483648, 4294967295][recipe['counter'] % 4]) == 0:
            state[CONTEXT][13] = 35
    elif state[CONTEXT][13] == 35:
        if word() != 0:
            provider(35580784, [])
            provider(33729612, [BUFFER])
        provider(35591332, [])
        state[CONTEXT][13] = 40
    elif state[CONTEXT][13] == 40:
        state[CONTEXT][13] = 0
        result = 1
    return (initial, snapshot(), services, native, result)
