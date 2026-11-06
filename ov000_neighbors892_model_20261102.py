import itertools
import struct
import ov000_neighbors892_machine_20261102 as M


def profiles():
    rows = []
    arrays = [[-1, 0, 1, 255, 256, -32768, 32767, 2], [0] * 8, [1, 1, 2, 2, 3, 3, 4, 4]]
    needles = [-0x80000000, -32768, -2, -1, 0, 1, 2, 255, 256, 32767, 0x10001, 0x7FFFFFFF]
    for count, values, needle in itertools.product([-1, 0, 1, 2, 4, 8], arrays, needles):
        rows.append(dict(ordinal=len(rows), kind='find', count=count, indices=values + [0x5555] * 24, needle=needle, node=0, neighbors=[-1, -1, -1], deltas={}, point=[0, 0, 0], limit=8))
    neighbors = [[-1, -2, -32768], [1, 2, 3], [1, 1, 2], [0, 1, 2], [257, 2, 32767], [2, -1, 1], [3, 2, 1]]
    states = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (4, 4), (3, 1)]
    near = [0, 0, 0]
    below = [65535, 0, 0]
    boundary = [65536, 0, 0]
    above = [65537, 0, 0]
    patterns = [[near] * 3, [below] * 3, [boundary] * 3, [above] * 3, [boundary, below, above], [below, above, boundary], [[46340, 46340, 0], [46341, 46341, 0], near], [[-0x80000000, 0, 0]] * 3, [[-0x80000000, -0x80000000, 0]] * 3, [[-0x80000000] * 3] * 3]
    for adjacent, (count, limit), pattern in itertools.product(neighbors, states, patterns):
        deltas = {str(index): pattern[index % 3] for index in adjacent if index >= 0}
        rows.append(dict(ordinal=len(rows), kind='neighbors', count=count, limit=limit, indices=[0, 2, 5, 1] + [0x5555] * 28, node=len(rows) % 4, neighbors=adjacent, deltas=deltas, point=[0, 0, 0]))
    for count, limit in [(-1, -2), (-1, -1), (0, -1), (1, 0)]:
        rows.append(dict(ordinal=len(rows), kind='neighbors', count=count, limit=limit, indices=[0x5555] * 32, node=0, neighbors=[-1, -1, -1], deltas={}, point=[0, 0, 0], invalidUnused=True))
    return rows


def signed64(value):
    value &= 0xFFFFFFFFFFFFFFFF
    return value - 0x10000000000000000 if value & 0x8000000000000000 else value


def contains(needle, indices, count):
    return int(needle in indices[:max(0, count)])


def neighbors(profile):
    values = list(profile['indices'])
    count = profile['count']
    calls, returns, writes = [], [], []
    for neighbor in profile['neighbors']:
        if count >= profile['limit']:
            break
        if neighbor < 0:
            continue
        found = contains(neighbor, values, count)
        calls.append(dict(target=hex(M.FIND), callerWords=[neighbor, M.INDICES, M.word(count)]))
        returns.append(dict(returnInstruction='0x21db964', returnedWord=found))
        if found:
            continue
        delta = profile['deltas'][str(neighbor)]
        sumBits = sum(component * component for component in delta) & 0xFFFFFFFFFFFFFFFF
        if signed64(sumBits) >> 12 < 0x100000:
            values[count] = neighbor
            writes.append([M.INDICES + count * 2, 2, neighbor & 0xFFFF])
            if count + 1 < profile['limit']:
                count += 1
    return M.word(count), values, calls, returns, writes


def model(vm, result):
    p = vm.p
    if p['kind'] == 'find':
        returned = contains(p['needle'], p['indices'], p['count'])
        values, calls, returns, writes = p['indices'], [], [], []
    else:
        returned, values, calls, returns, writes = neighbors(p)
    expectedIndices = b''.join(struct.pack('<H', value & 0xFFFF) for value in values)
    expected = dict(indicesHex=expectedIndices.hex(), calls=calls, originalHelperPhysicalReturns=returns, writes=writes)
    failures = [key for key, value in expected.items() if result[key] != value]
    if result['registers'][0] != returned:
        failures.append('independent return word')
    return failures
