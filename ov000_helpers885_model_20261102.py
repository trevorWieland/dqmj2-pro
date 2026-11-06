import itertools
import struct
import ov000_helpers885_machine_20261102 as M


def profiles():
    rows = []

    def add(**fields):
        p = dict(ordinal=len(rows), seed=len(rows))
        p.update(fields)
        rows.append(p)

    for count in range(1, 13):
        for offset in range(count):
            add(kind='order', count=count, offset=offset, entry=0x021DA4D4)
    for count, offset in [(25, 0), (25, 12), (25, 24), (49, 24), (0, 0), (0, -1), (-1, 0), (-1, -1), (-2, 1), (-0x80000000, 0)]:
        add(kind='order', count=count, offset=offset, entry=0x021DA4D4)
    patterns = [[1, 2, 3, 4, 5], [0, 0, 0, 0, 0], [2, 0, 1, 0, 3], [-1, 1, -2, 2, 0], [0x7FFFFFFF, 1, -0x80000000, -1, 2]]
    for blocks, sizes, index in itertools.product([-2, -1, 0, 1, 2, 3, 5], patterns, [-0x80000000, -2, -1, 0, 1, 2, 3, 5, 8, 0x7FFFFFFF]):
        add(kind='context', entry=0x021DA57C, blocks=blocks, sizes=sizes, index=index)
    responses = [[0], [-1], [1], [2], [8], [4, 2], [3, 7, 1], [0x7FFFFFFF], [-0x80000000], [2, 3, 4, 5, 6, 7, 8, 9]]
    for limit, plan, index in itertools.product([-2, -1, 0, 1, 2, 3, 5, 8], responses, [0, -1, 0x7FFF, 0x8000, 0x12348000, -0x80000000]):
        add(kind='walk', entry=0x021DBB50, index=index, limit=limit, responses=plan, ignored=[0, 1, -1, -0x80000000, 0x12345678][len(rows) % 5])
    for ignored in [0, 1, -1, -0x80000000, 0x12345678]:
        add(kind='walk', entry=0x021DBB50, index=0x12348000, limit=5, responses=[3, 5, 4], ignored=ignored, seed=0x739, ignoredGroup='fixed-state-r3')
    return rows


def orderModel(profile):
    output = []
    ordinal = 0
    observations = []
    while True:
        distance = (ordinal + 1) // 2
        value = -distance if ordinal & 1 else distance
        observations.append(dict(address='0x21da484', input=ordinal, returnInstruction='0x21da4cc', returnedWord=M.word(value)))
        choice = M.word(profile['offset'] + value)
        ordinal += 1
        if choice <= M.word(profile['count'] - 1):
            output.append(choice & 255)
            if len(output) >= max(1, profile['count']):
                return ordinal, bytes(output), observations
        if ordinal >= 49:
            raise ValueError('885 independent lookup bound')


def contextModel(profile, before):
    result = bytearray(before)
    index = M.word(profile['index'])
    result[0] = 1
    struct.pack_into('<II', result, 8, index, M.TRIANGLES)
    cumulative = 0
    ordinal = 0
    for size in profile['sizes'][:max(0, profile['blocks'])]:
        boundary = M.word(cumulative + size)
        if M.signed(boundary) > M.signed(index):
            index = M.word(index - cumulative)
            break
        cumulative = boundary
        ordinal += 1
    result[1] = ordinal & 255
    struct.pack_into('<I', result, 4, index)
    return bytes(result)


def walkModel(profile, before):
    indices = bytearray(before)
    struct.pack_into('<H', indices, 0, profile['index'] & 0xFFFF)
    calls = []
    previousCount = 1
    step = 0
    while True:
        value = struct.unpack_from('<h', indices, step * 2)[0]
        response = M.response(profile, step)
        mutation = M.suppliedWrite(profile, step)
        calls.append(dict(target=hex(M.PROVIDER), callerWords=[M.word(value), M.TREE, M.INDICES, M.word(previousCount), M.TRIANGLES, M.POINT, M.word(profile['limit'])], suppliedReturn=response, suppliedWrite=dict(address=M.INDICES + 2 * (step + 1), value=mutation)))
        struct.pack_into('<H', indices, (step + 1) * 2, mutation)
        step += 1
        if not step < min(M.signed(response), profile['limit']):
            return step, bytes(indices), calls
        previousCount = M.signed(response)


def model(vm, result):
    p = vm.p
    expectedContext = vm.beforeContext
    expectedOutput = vm.beforeOutput
    expectedIndices = vm.beforeIndices
    helpers = []
    calls = []
    if p['kind'] == 'order':
        returned, ordered, helpers = orderModel(p)
        expectedOutput = ordered + expectedOutput[len(ordered):]
    elif p['kind'] == 'context':
        returned = M.CONTEXT
        expectedContext = contextModel(p, vm.beforeContext)
    else:
        returned, expectedIndices, calls = walkModel(p, vm.beforeIndices)
    expected = dict(contextHex=expectedContext.hex(), outputHex=expectedOutput.hex(), indicesHex=expectedIndices.hex(), meshHex=vm.beforeMesh.hex(), calls=calls, originalHelperReturns=helpers)
    failures = [key for key, value in expected.items() if result[key] != value]
    if result['registers'][0] != returned:
        failures.append('independent return word')
    return failures
