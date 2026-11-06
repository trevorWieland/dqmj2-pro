import hashlib
import struct
from ov001_clamp453_machine_20261101 import BASE, STACK, LIMITS

def s16(v):
    return (v + 32768) % 65536 - 32768

def maxima(p):
    classification = ((p['kindWord'] >> 8) & 15) // 3
    low = p['kindWord'] & 15
    progress = (low - 1) // 3 if low else 0
    if classification == 0:
        begin, end = progress + 2, min(p['tag'] + progress + 2, 4)
    elif classification == 1:
        begin, end = progress // 2 + 3, min((p['tag'] + progress) // 2 + 3, 4)
    elif classification == 2:
        begin, end = 4, 4
    else:
        raise ValueError('453 unsupported native class')
    out = []
    for base in p['bases']:
        value = base * (p['tag'] + 8) // 8 & 65535
        if p['tag']:
            for ability in p['abilities'][begin:end]:
                if ability == 0x4C:
                    value = value * 7 // 8 & 65535
                elif ability in [4, 0x4D, 0x78]:
                    value = value * 3 // 4 & 65535
                elif ability == 0x77:
                    value = value * 5 // 8 & 65535
        out.append(value)
    return out

def profiles():
    rows = []
    for kind in [-2, 0, 3, 127]:
        for tag in [0, 1, 7, 255]:
            for feature in [0, 8]:
                for style in range(3):
                    for alias in ['none', 'stats']:
                        index = len(rows)
                        p = dict(name=f'kind{kind}-tag{tag}-feature{feature}-style{style}-{alias}', kind=kind, tag=tag, feature=feature, alias=alias, recordIndex=[0, 49, 99][index % 3], parents=[-32768, 255, 32767, 128], bases=[0, 1, 31, 9999, 32767, 65535], kindWord=[0x0001, 0x0304, 0x0607][index % 3], abilities=[0, 0, 0x4C, 0x78, 0], deltas=[-32768, -1, 0, 1, 32767, 9999, -9999, 1234], raw208=[9998, 9999, 10000][style])
                        mx = maxima(p)
                        p['stats'] = [[s16(v - 1) for v in mx], [s16(v) for v in mx], [32767 if i % 2 else -32768 for i in range(6)]][style]
                        rows.append(p)
    for bit in range(64):
        p = dict(rows[0], name=f'independent-clamp-mask{bit}', bases=[100, 200, 300, 400, 500, 600], tag=0, alias='none', stats=[v + (1 if bit >> i & 1 else -1) for i, v in enumerate([100, 200, 300, 400, 500, 600])], raw208=[32767, -32768][bit % 2])
        rows.append(p)
    return rows

def normalized(data):
    cut = STACK - BASE
    return hashlib.sha256(bytes(data[:cut-65536]) + bytes(data[cut+4096:])).hexdigest()

def model(result):
    p, entry = result['profile'], result['entry']
    expected = bytearray(result['before'])
    subject, delta = result['subject'], result['delta']
    maximaValues = maxima(p)
    fields = [0x1EC, 0x1EE, 0x1F4, 0x1F6, 0x1F8, 0x1FA] if entry == 0x021E4500 else [0x20, 0x22, 0x28, 0x2A, 0x2C, 0x2E]
    def half(address):
        return struct.unpack_from('<h', expected, address - BASE)[0]
    def put(address, value):
        struct.pack_into('<H', expected, address - BASE, value & 65535)
    changed = []
    for index, (field, maximum) in enumerate(zip(fields, maximaValues)):
        current = half(subject + field)
        if current > maximum:
            put(delta + index * 2, half(delta + index * 2) - (current - maximum))
            put(subject + field, maximum)
            changed.append(index)
    if entry == 0x021E4500 and half(subject + 0x208) > 9999:
        put(delta + 14, half(delta + 14) - (half(subject + 0x208) - 9999))
        put(subject + 0x208, 9999)
        changed.append(7)
    words = [p['kind'], p['tag']] + p['parents']
    calls = [dict(entry=a, preparedWords=[v & 0xFFFFFFFF for v in words]) for a in LIMITS]
    if result['calls'] != calls:
        raise ValueError(('453 caller-prepared six-word mismatch', p['name'], result['calls'], calls))
    limitReturns = [r['returnedR0'] for r in result['nativeReturns'] if r['entry'] in LIMITS]
    if limitReturns != maximaValues:
        raise ValueError(('453 independent native limit model differs', p['name'], limitReturns, maximaValues))
    digest = normalized(result['after'])
    if normalized(expected) != digest:
        raise ValueError(('453 complete independent nonstack effects differ', p['name'], hex(entry)))
    return dict(maxima=maximaValues, changedStats=changed, nonstackSha256=digest)
