import struct
import ov000_geometry877_model_20261102 as B
import ov000_geometry902_machine_20261102 as M


def profiles():
    rows = []
    for p in B.profiles():
        x, y, z = p['point']
        travel = y + 4096 - p.get('slopeX', 0) * x - p.get('slopeZ', 0) * z
        if not p['reverse'] and travel >= 0:
            rows.append(dict(p, ordinal=len(rows), capacityRaw=1, indexWord=0))
    for capacity in range(256):
        rows.append(dict(ordinal=len(rows), point=(0, 0, 0), reverse=False, zeroNormal=False, normalMagnitude=4096, flag=1, mask=1, count=-91, nullOutput=False, capacityRaw=capacity, indexWord=[0, 0x12340000, 0x7FFF0000, 0xFFFF0000][capacity % 4]))
    return rows


def model(vm, result):
    p = vm.p
    x, y, z = p['point']
    target = p.get('slopeX', 0) * x + p.get('slopeZ', 0) * z
    travel = y + 4096 - target
    eligible = not p['zeroNormal'] and bool(p['flag'] & p['mask'])
    hit = eligible and travel >= 0 and travel * travel // 4096 <= 0x4000 and B.B.inside(x, z)
    context = bytearray(vm.beforeContext)
    struct.pack_into('<H', context, 0x12, 0)
    context[0x11] = 1
    writes = [[M.SP, 4, p['mask']], [M.CONTEXT + 0x12, 2, 0], [M.CONTEXT + 0x12, 2, 0], [M.CONTEXT + 0x11, 1, 1]]
    calls = [dict(target='0x21dbbb8', callerWords=[M.CONTEXT, M.B.POINT], nativeExecution=True, actualReturnWord=1)]
    entries = [0x021DBBB8, 0x021DBB50, 0x021DB968]
    returns = [0x021DB968, 0x021DBB50, 0x021DBBB8]
    if eligible:
        normalY = -p['normalMagnitude']
        calls.append(dict(target='0x200235c', callerWords=[M.B.word((-travel * normalY) // 4096), M.B.word(-normalY)], nativeExecution=True, actualReturnWord=travel))
        entries += [0x0200235C, 0x02002458, 0x020023C4]
        returns += [0x02002458, 0x020023C4, 0x0200235C]
    if hit:
        context[0] = 1
        struct.pack_into('<II', context, 8, 0, M.RECORD)
        context[1] = 0
        struct.pack_into('<I', context, 4, 0)
        writes += [[M.CONTEXT, 1, 1], [M.CONTEXT + 8, 4, 0], [M.CONTEXT + 0xC, 4, M.RECORD], [M.CONTEXT + 1, 1, 0], [M.CONTEXT + 4, 4, 0]]
        calls.append(dict(target='0x21da57c', callerWords=[M.CONTEXT, 0, M.RECORD, M.MESH], nativeExecution=True, actualReturnWord=M.CONTEXT))
        entries.append(0x021DA57C)
        returns.append(0x021DA57C)
    output = vm.beforeOutput
    if hit and not p['nullOutput']:
        output = M.B.pack([x, target, z])
        writes += [[M.B.OUTPUT + i * 4, 4, M.B.word(value)] for i, value in enumerate([x, target, z])]
    expected = dict(outputHex=output.hex(), contextHex=context.hex(), meshHex=vm.beforeMesh.hex(), calls=calls, writes=writes)
    failures = [key for key, value in expected.items() if ([list(row) for row in result[key]] if key == 'writes' else result[key]) != value]
    if result['registers'][0] != int(hit):
        failures.append('independent prepared-query hit/miss')
    if [int(row['entry'], 0) for row in result['nativeHelperEntries']] != entries:
        failures.append('actual native entry chain')
    if [int(row['entry'], 0) for row in result['nativeHelperPhysicalReturns']] != returns:
        failures.append('actual native physical return chain')
    capacity = p['capacityRaw']
    capacity = capacity - 256 if capacity & 128 else capacity
    lowerWords = [0, M.MESH + 0x180, M.CONTEXT + 0x12, 1, M.RECORD, M.B.POINT, M.B.word(capacity)]
    for row in result['nativeHelperEntries']:
        if row['entry'] in ['0x21dbb50', '0x21db968'] and row['callerWords'] != lowerWords:
            failures.append('prepared seven-word lower call view')
    return failures
