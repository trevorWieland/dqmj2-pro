import itertools
import struct
import ov000_geometry872_machine_20261102 as M


def profiles():
    result = []

    def add(**changes):
        n = len(result)
        p = dict(ordinal=n, point=(0, 0, 0), reverse=False, zeroNormal=False, normalMagnitude=4096, flag=1, mask=1, count=1, nullOutput=False)
        p.update(changes)
        result.append(p)

    for x, z, reverse, normal in itertools.product([-16384, -8192, -4096, 0, 4096, 8192, 16384], [-16384, -8192, -4096, 0, 4096, 8192, 16384], [False, True], [2048, 4096]):
        add(point=(x, 0, z), reverse=reverse, normalMagnitude=normal)
    for y, reverse, normal in itertools.product([-12288, -8192, -4096, 0, 4096, 8192], [False, True], [1, 17, 2048, 4096, 8192]):
        add(point=(0, y, 0), reverse=reverse, normalMagnitude=normal)
    for flag, mask, count, zero, null in itertools.product([0, 1, 2, 3, 255], [0, 1, 2], [0, 1, -1], [False, True], [False, True]):
        add(flag=flag, mask=mask, count=count, zeroNormal=zero, nullOutput=null)
    return result


def inside(x, z):
    vertices = [(-8192, -8192), (8192, -8192), (0, 8192)]
    cross = []
    for (a, b), (c, d) in zip(vertices, vertices[1:] + vertices[:1]):
        cross.append((c - a) * (z - b) - (d - b) * (x - a))
    return all(value >= 0 for value in cross) or all(value <= 0 for value in cross)


def model(vm, result):
    p = vm.p
    x, y, z = p['point']
    shifted = y + 4096
    eligible = p['count'] > 0 and not p['zeroNormal'] and (p['flag'] & p['mask']) != 0
    hit = eligible and shifted >= 0 and shifted * shifted // 4096 <= 0x4000 and inside(x, z)
    expectedOutput = M.pack([x, 0, z]) if hit and not p['nullOutput'] else vm.beforeOutput
    failures = []
    if result['registers'][0] != int(hit):
        failures.append('independent horizontal-triangle hit/miss')
    if result['outputHex'] != expectedOutput.hex():
        failures.append('independent output point/null preservation')
    if result['meshHex'] != vm.beforeMesh.hex() or result['contextHex'] != vm.beforeContext.hex():
        failures.append('synthetic mesh/list unchanged')
    expectedTargets = ([0x0200235C] if eligible else []) + ([0x021DA57C] if hit else [])
    if [int(row['target'], 0) for row in result['calls']] != expectedTargets:
        failures.append('ordered supplied boundary path')
    for row in result['calls']:
        if row['target'] == '0x200235c':
            normal = p['normalMagnitude'] if p['reverse'] else -p['normalMagnitude']
            expected = [M.word((-shifted * normal) // 4096), M.word(-normal)]
            if row['callerWords'] != expected:
                failures.append('native normal/dot fixed-point division inputs')
        if row['target'] == '0x21da57c' and row['callerWords'] != [M.CONTEXT, 0, M.RECORD, M.MESH]:
            failures.append('supplied hit notification input words')
    return failures
