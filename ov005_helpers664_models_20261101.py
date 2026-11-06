import struct
import ov005_helpers664_machine_20261101 as M


def signed(value, bits):
    value &= (1 << bits) - 1
    return value - (1 << bits) if value >> (bits - 1) else value


def profiles():
    result = []
    words = [((index * 0x91734521) ^ 0xA6641234) & 0xFFFFFFFF for index in range(32)]
    payload = struct.pack('<32I', *words)
    for index in [-3, -2, -1, 0, 1, 2, 3, 4, 5, 8, 12, 20]:
        result.append(dict(name='curve-' + str(index), entry=0x021E664C, data=list(payload), words=[M.DATA + 16, index]))
    for index in [0, 1, -1, -2147483648, 2147483647]:
        result.append(dict(name='curve-null-' + str(index), entry=0x021E664C, data=list(payload), words=[0, index]))
    patterns = [bytes(512), bytes([1]) * 512, bytes([255]) * 512, bytes((index * 17 + 31) & 255 for index in range(512))]
    for pattern, payload in enumerate(patterns):
        for level in [-2147483648, -1, 0, 1, 2, 5, 127, 128, 129, 255, 256, 257, 512]:
            for count in [-65535, -1, 0, 1, 2, 5, 255, 65535]:
                result.append(dict(name=f'points-{pattern}-{level}-{count}', entry=0x021E6678, data=list(payload), words=[level, count, [0, 1, 0xFFFFFFFF][(pattern + level) % 3]], opened=True))
    for level, count in [(0, 0), (0x7FFFFFFF, 0x7FFFFFFF), (0x80000000, 0xFFFFFFFF)]:
        result.append(dict(name=f'points-null-{level}-{count}', entry=0x021E6678, data=list(patterns[0]), words=[level, count, 0xFFFFFFFF], opened=False))
    return result


def model(result):
    profile = result['profile']
    words = profile['words']
    if profile['entry'] == 0x021E664C:
        index = signed(words[1], 32)
        offset = 16 + (index - 1) * 4
        expected = struct.unpack_from('<I', bytes(profile['data']), offset)[0] if words[0] else 0
        reads = [[offset, 4, bytes(profile['data'][offset:offset + 4]).hex()]] if words[0] else []
        calls = []
    else:
        opened, level, count = profile['opened'], signed(words[0], 32), signed(words[1], 32)
        total = 0
        reads = []
        if opened:
            for index in range(max(0, level)):
                total = signed(total + profile['data'][index], 16)
                reads.append([index, 1, bytes([profile['data'][index]]).hex()])
        numerator = total * count + 4
        if not -2147483648 <= numerator <= 2147483647:
            raise ValueError('664 supplied C signed product/add would overflow')
        quotient = abs(numerator) // 5 * (-1 if numerator < 0 else 1)
        expected = signed(quotient, 16) & 0xFFFFFFFF if opened else 0
        calls = [dict(entry=M.OPEN, preparedWords=[M.NAME, words[2] & 0xFFFFFFFF])]
        if opened:
            calls.append(dict(entry=M.CLOSE, preparedWords=[words[2] & 0xFFFFFFFF, M.DATA]))
    got = [dict(entry=item['entry'], preparedWords=item['preparedWords']) for item in result['providedCalls']]
    if result['coreRegistersAndCpsr'][0] != expected or result['payloadReads'] != reads or got != calls:
        raise ValueError(('664 independent result/read/service model differs', profile['name'], result['coreRegistersAndCpsr'][0], expected))
    before, after = result['before'], result['after']
    lo, hi = M.STACK - 65536 - M.BASE, M.STACK + 256 - M.BASE
    if before[:lo] != after[:lo] or before[hi:] != after[hi:]:
        raise ValueError('664 independent nonstack RAM model differs')
    return dict(expectedR0=expected, payloadReadCount=len(reads), providedCalls=len(calls), nonstackRamUnchanged=True)
