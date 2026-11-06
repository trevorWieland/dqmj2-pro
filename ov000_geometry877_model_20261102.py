import itertools
import ov000_geometry874_model_20261102 as B
import ov000_geometry877_machine_20261102 as M


def profiles():
    rows = B.profiles()
    for (sx, sz), x, z, reverse, normal in itertools.product([(1, 0), (0, 1), (-1, 1)], [-16384, -8192, -4096, 0, 4096, 8192, 16384], [-16384, -8192, -4096, 0, 4096, 8192, 16384], [False, True], [2048, 4096]):
        rows.append(dict(ordinal=len(rows), point=(x, 0, z), reverse=reverse, zeroNormal=False, normalMagnitude=normal, flag=1, mask=1, count=1, nullOutput=False, slopeX=sx, slopeZ=sz))
    return rows


def model(vm, result):
    p = vm.p
    x, y, z = p['point']
    targetY = p.get('slopeX', 0) * x + p.get('slopeZ', 0) * z
    travel = y + 4096 - targetY
    eligible = p['count'] > 0 and not p['zeroNormal'] and (p['flag'] & p['mask']) != 0
    hit = eligible and travel >= 0 and travel * travel // 4096 <= 0x4000 and B.inside(x, z)
    expectedOutput = M.pack([x, targetY, z]) if hit and not p['nullOutput'] else vm.beforeOutput
    failures = []
    if result['registers'][0] != int(hit):
        failures.append('independent plane-projected triangle hit/miss')
    if result['outputHex'] != expectedOutput.hex():
        failures.append('independent plane projection/null preservation')
    if result['meshHex'] != vm.beforeMesh.hex() or result['contextHex'] != vm.beforeContext.hex():
        failures.append('synthetic mesh/list unchanged')
    expectedTargets = ([0x0200235C] if eligible else []) + ([0x021DA57C] if hit else [])
    if [int(row['target'], 0) for row in result['calls']] != expectedTargets:
        failures.append('ordered supplied boundary path')
    for row in result['calls']:
        if row['target'] == '0x200235c':
            normalY = p['normalMagnitude'] if p['reverse'] else -p['normalMagnitude']
            if row['callerWords'] != [M.word((-travel * normalY) // 4096), M.word(-normalY)]:
                failures.append('independent plane/dot division input words')
        if row['target'] == '0x21da57c' and row['callerWords'] != [M.CONTEXT, 0, M.RECORD, M.MESH]:
            failures.append('supplied hit notification input words')
    return failures
