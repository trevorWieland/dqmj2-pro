import struct
import ov001_scalar626_machine_20261101 as M


def words(value):
    return list(struct.unpack('<2I', struct.pack('<d', value)))


def profiles():
    values = set(range(65))
    values.update(range(52380, 52411))
    values.update([99, 100, 101, 255, 256, 32767, 32768, 65534, 65535, 65536, 65537, 3435973795, 3435973796])
    for bit in range(32):
        values.update(value for value in [(1 << bit) - 1, 1 << bit, (1 << bit) + 1] if value <= 3435973796)
    return [dict(name='row%d-scalar%d' % (row, value), case=3 * index + row, row=row, scalar=value, withinUnsigned16CallerDomain=value <= 65535) for index, value in enumerate(sorted(values)) for row in range(3)]


def model(result):
    p = result['profile']
    converted = float(p['scalar'])
    product = 1.25 * converted
    total = 50.0 + product
    integral = int(total)
    if not 0 <= integral <= 0xFFFFFFFF:
        raise ValueError('626 model called outside the qualified unsigned conversion domain')
    low = integral & 65535
    stored = min(low, 100)
    expected = bytearray(result['before'])
    address = M.ROWS + p['row'] * 132 + 0x30
    expected[address - M.BASE] = stored
    lo, hi = M.STACK - 65536 - M.BASE, M.STACK + 256 - M.BASE
    if bytes(expected[:lo]) != result['after'][:lo] or bytes(expected[hi:]) != result['after'][hi:]:
        raise ValueError(('626 independent complete nonstack RAM model differs', p['name']))
    returns = result['nativeReturns']
    if [record['entry'] for record in returns] != M.WATCH:
        raise ValueError('626 actual native helper return order differs')
    if returns[0]['preparedWords'][0] != p['scalar'] or returns[0]['returnedWords'][:2] != words(converted):
        raise ValueError('626 native unsigned32-to-binary64 contract differs')
    if returns[1]['preparedWords'] != words(1.25) + words(converted) or returns[1]['returnedWords'][:2] != words(product):
        raise ValueError('626 native binary64 multiplication contract differs')
    if returns[2]['preparedWords'] != words(50.0) + words(product) or returns[2]['returnedWords'][:2] != words(total):
        raise ValueError('626 native binary64 addition contract differs')
    if returns[3]['preparedWords'][:2] != words(total) or returns[3]['returnedWords'][0] != integral:
        raise ValueError('626 native finite unsigned32 conversion contract differs')
    if result['actualTopReturnedWords'][0] != M.ROWS + 0x30:
        raise ValueError('626 physical R0 is not the original base-address residue')
    return dict(row=p['row'], scalar=p['scalar'], fullIntegral=integral, low16=low, storedByte=stored, binary64InputsAndResults=[words(converted), words(product), words(total)], withinUnsigned16CallerDomain=p['withinUnsigned16CallerDomain'])
