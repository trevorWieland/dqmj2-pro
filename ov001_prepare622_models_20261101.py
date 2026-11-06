import struct
import ov001_prepare622_machine_20261101 as M


def profiles():
    result = []
    for row in range(3):
        for kind in range(16):
            for mode in [0, 49, 50, 51, 99, 100, 101, 102, 255]:
                index = len(result)
                result.append(dict(name='row%d-kind%d-mode%d' % (row, kind, mode), row=row, header=([0, 0xA5B0, 0xFFF0][row] | kind), mode=mode, id=[0, 0xFFFFFFFF, 0x80008000, 0xABCD0001][index % 4], seed=[0, 1, 0xFFFFFFFF][index % 3]))
    return result


def model(result):
    p = result['profile']
    expected = bytearray(result['before'])
    row = M.ROWS + p['row'] * 132
    state, draws = p['seed'], []
    def draw(limit):
        nonlocal state
        state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
        value = (state >> 16) % limit
        draws.append((limit, value))
        return value
    def store(address, raw):
        expected[address - M.BASE:address - M.BASE + len(raw)] = raw
    store(row + 0x18, struct.pack('<H', p['id'] & 65535))
    kind = p['header'] & 15
    branch = (kind - 1) // 3 if 1 <= kind <= 6 else -1
    variant = 0xCC
    if branch < 0:
        variant = 0
    elif p['mode'] == 50:
        variant = 1 - branch
    elif p['mode'] in [100, 101]:
        variant = draw(2) + 1 - branch
    store(row + 0x1A, bytes([variant]))
    final_draw = draw(3)
    store(row + 0x1B, bytes([final_draw]))
    store(M.RNGSTATE, struct.pack('<I', state))
    lo, hi = M.STACK - 65536 - M.BASE, M.STACK + 4096 - M.BASE
    if bytes(expected[:lo]) != result['after'][:lo] or bytes(expected[hi:]) != result['after'][hi:]:
        raise ValueError(('622 independent complete nonstack RAM model differs', p['name']))
    wanted = [[row, p['id'], 0], [p['id']]]
    if [event['preparedWords'] for event in result['providedCalls']] != wanted:
        raise ValueError('622 actual initializer/lookup preparation differs')
    observed = [(ret['preparedWords'][0], ret['returnedWords'][0]) for ret in result['nativeReturns'] if ret['entry'] == M.RNG]
    if observed != draws:
        raise ValueError('622 actual native RNG order/bounds/returns differ')
    if result['coreRegistersAndCpsr'][0] != final_draw:
        raise ValueError('622 physical R0 does not forward final native RNG result')
    return dict(row=p['row'], idLow16=p['id'] & 65535, rawKind=kind, rawMode=p['mode'], rawVariant=variant, finalRawByte=final_draw, rngState=state, draws=draws)
