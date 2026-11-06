import itertools
import struct

FLAG, QUERY_ROOT, READY_ROOT, STATE = 0x0221C0CC, 0x0221C180, 0x0221C008, 0x0221C06C
QUERY, READY = 0x02350000, 0x02360000


def recipes(kind):
    if kind == 'predicate':
        return [dict(seed=0x130000 + value, value=value, null=value == 256) for value in range(257)]
    result = []
    for q0, q1, flag, readiness, after, final in itertools.product([0, 1, 128, 255], [0, 255], [0, 255], [0, 1, 2], [0, 255], [0, 255]):
        result.append(dict(seed=0x131000 + len(result), q0=q0, q1=q1, flag=flag, readiness=readiness, after=after, final=final))
    return result


def construct(kind, recipe):
    calls, writes = [], []
    if kind == 'predicate':
        value = recipe['value'] & 255
        initial = [(READY_ROOT, struct.pack('<I', 0 if recipe['null'] else READY)), (READY + 24, bytes([value ^ 1, value]))]
        return initial, writes, calls, int(recipe['null'] or value == 0), 0
    initial = [(FLAG, bytes([recipe['flag']])), (QUERY_ROOT, struct.pack('<I', QUERY)),
        (READY_ROOT, struct.pack('<I', 0 if recipe['readiness'] == 0 else READY)),
        (QUERY + 9, bytes([recipe['q1']])), (QUERY + 21, bytes([recipe['q0']])),
        (READY + 25, bytes([255 if recipe['readiness'] == 2 else 0]))]

    def call(address, arguments=(), effects=()):
        calls.append(dict(address=address, arguments=list(arguments), effects=list(effects), result=recipe['seed'] ^ address))
        writes.extend(effects)

    native = 1
    if recipe['q0']:
        return initial, writes, calls, recipe['q0'], native
    if recipe['flag'] == 0:
        native += 1
        if recipe['q1']:
            return initial, writes, calls, recipe['q1'], native
    native += 1
    if recipe['readiness'] == 2:
        return initial, writes, calls, 0, native
    call(0x021F4EB8, [int(recipe['flag'] != 0)], [(FLAG, bytes([recipe['flag'] ^ 255])), (QUERY + 21, b'\xEE')])
    call(0x021F221C, effects=[(FLAG, bytes([recipe['flag']])), (READY + 25, b'\xFF')])
    call(0x02203690, [0], [(FLAG, bytes([recipe['after']]))])
    if recipe['after'] == 0:
        call(0x021F2774, effects=[(FLAG, b'\x80')])
        call(0x02203954, [1, 1], [(FLAG, b'\x01')])
    call(0x02203954, [0, 21], [(FLAG, bytes([recipe['final']]))])
    callback = 0x021FD11D if recipe['final'] == 0 else 0x021F7DA5
    selector, enabled = (2, 1) if recipe['final'] == 0 else (0, 0)
    writes += [(STATE + 16, struct.pack('<II', selector, enabled)), (STATE + 12, struct.pack('<I', callback))]
    return initial, writes, calls, callback, native + 2
