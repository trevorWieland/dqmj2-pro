import gzip
import hashlib
import json
from pathlib import Path
import arm7_lane_alarm_registration_native_20261031 as fixture
from unicorn import UC_HOOK_CODE

ROOT = Path(__file__).resolve().parent
SIZES = {0x037FD3B0: 300, 0x037FD54C: 116, 0x037FE5C0: 156}
CODES = {0x037FD3B0: 296, 0x037FD54C: 116, 0x037FE5C0: 140}
WORK = ROOT / 'work/arm7-bulk-20261030/lane-host-alarm-family572-final'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def model_insertion(memory, record, fire, nodes):
    mask = (1 << 64) - 1
    queue, io = 0x038078A8, 0x04000000
    stores = []

    def put(address, width, value):
        for base, data in memory.items():
            if base <= address and address + width <= base + len(data):
                data[address - base:address - base + width] = (value & ((1 << (8 * width)) - 1)).to_bytes(width, 'little')
                stores.append([address, width, value & ((1 << (8 * width)) - 1)])
                return
        raise ValueError('Independent insertion model escaped mapped backing')

    index = next((index for index, row in enumerate(nodes) if ((fire - row[1]) & mask) >> 63), len(nodes))
    previous = nodes[index - 1][0] if index else 0
    following = nodes[index][0] if index < len(nodes) else 0
    put(record + 12, 4, fire)
    put(record + 16, 4, fire >> 32)
    if following:
        put(record + 20, 4, previous)
        put(following + 20, 4, record)
        put(record + 24, 4, following)
        if previous:
            put(previous + 24, 4, record)
        else:
            put(queue + 4, 4, record)
    else:
        put(record + 24, 4, 0)
        put(queue + 8, 4, record)
        put(record + 20, 4, previous)
        if previous:
            put(previous + 24, 4, record)
        else:
            put(queue + 8, 4, record)
            put(queue + 4, 4, record)
    if not previous:
        put(io + 0x106, 2, 0)
        put(0x038076BC, 4, 0x037FD648)
        put(0x038076C4, 4, 0)
        old_ie = fixture.engine.word(memory, io + 0x210)
        ime = fixture.engine.word(memory, io + 0x208) & 0xFFFF
        put(io + 0x208, 2, 0)
        put(io + 0x210, 4, old_ie | 16)
        put(io + 0x208, 2, ime)
        put(0x038076C0, 4, 1)
        count = 0xFFFE if fire >> 63 else (~fire & 0xFFFF) if fire < 0x10000 else 0
        put(io + 0x104, 2, count)
        put(io + 0x106, 2, 0xC1)
        put(io + 0x208, 2, 0)
        put(io + 0x210, 4, old_ie | 16)
        put(io + 0x208, 2, ime)
    return {'insertedIndex': index, 'previous': previous, 'following': following, 'expectedOrderedStores': stores}


def direct_insertion(bodies, fire, fires, seed):
    case = {'tick': True, 'alarm': True, 'enabled': 0, 'counter': 0, 'timer': 0, 'request': 0, 'passes': 1}
    machine = fixture.setup(fixture.ADDRESS, bodies[fixture.ADDRESS], case, seed)
    cpu = machine['cpu']
    for address, body in bodies.items():
        cpu.mem_write(address, body)
    record, base = fixture.ALARM, fixture.DATA + 0x200
    nodes = [(base + index * 64, value) for index, value in enumerate(fires)]
    cpu.mem_write(record, bytes(44))
    for index, (address, value) in enumerate(nodes):
        words = [0x037FE65C, 0, 0, value & 0xFFFFFFFF, value >> 32,
            nodes[index - 1][0] if index else 0, nodes[index + 1][0] if index + 1 < len(nodes) else 0, 0, 0, 0, 0]
        cpu.mem_write(address, b''.join(word.to_bytes(4, 'little') for word in words))
    cpu.mem_write(0x038078AC, (nodes[0][0] if nodes else 0).to_bytes(4, 'little'))
    cpu.mem_write(0x038078B0, (nodes[-1][0] if nodes else 0).to_bytes(4, 'little'))
    expected = fixture.engine.snapshot(machine)
    model = model_insertion(expected, record, fire, nodes)
    visited = []
    cpu.hook_add(UC_HOOK_CODE, lambda machine, pc, width, unused: visited.append(pc))
    result = machine['invoke'](0x037FD3B0, [record, fire & 0xFFFFFFFF, fire >> 32], True, 20000)
    if not result['actualReturn']:
        raise ValueError('Bounded direct insertion did not return: ' + str(result))
    checked = fixture.engine.result(machine, result, expected, None, model['expectedOrderedStores'])
    if checked['orderedNonstackWrites'] != model['expectedOrderedStores']:
        raise ValueError('Independent exact nonstack store order differs')
    return {'fire': fire, 'existingFires': fires, 'model': model, 'execution': checked,
        'ownVisited': sorted({pc for pc in visited if 0x037FD3B0 <= pc < 0x037FD3B0 + 296})}


def oracle(bodies):
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    originals = {address: raw[address - 0x037F8000:address - 0x037F8000 + size] for address, size in SIZES.items()}
    if set(bodies) != set(SIZES) or any(bodies[address] != originals[address] for address in SIZES):
        raise ValueError('Every source-linked family body must genuinely match complete native bytes')
    records, visited, returns = [], {address: set() for address in SIZES}, {address: 0 for address in SIZES}

    def execute(group, case, seed):
        machine = fixture.setup(fixture.ADDRESS, group[fixture.ADDRESS], case, seed)
        for address, body in group.items():
            machine['cpu'].mem_write(address, body)

        def code(cpu, pc, width, unused):
            for address, code_bytes in CODES.items():
                if address <= pc < address + code_bytes:
                    visited[address].add(pc)

        machine['cpu'].hook_add(UC_HOOK_CODE, code)
        return fixture.execute(machine)

    for index, case in enumerate(fixture.cases(fixture.ADDRESS)):
        for flags in range(4):
            seed = index * 4 + flags
            native, compiled = execute(originals, case, seed), execute(bodies, case, seed)
            if native != compiled or len(native['states']) != 2 or any(not row['actualReturn'] for row in native['states']):
                raise ValueError('Connected original/new three-C definition ABI/memory/return proof failed')
            records.append(native)
            returns[fixture.ADDRESS] += 4
            for state in native['states']:
                for address in (0x037FD3B0, 0x037FD54C):
                    returns[address] += 2 * state['actualOriginalHelperReturns'].get(hex(address), 0)
    direct = []
    for fire in (0, 1, 0xFFFF, 0x10000, 0x7FFFFFFFFFFFFFFF, 0x8000000000000000, 0xFFFFFFFFFFFFFFFF):
        for fires in ([], [0], [0xFFFFFFFFFFFFFFFF], [0, 2, 0x10000], [0xFFFFFFFFFFFFFFFF, 0]):
            native = direct_insertion(originals, fire, fires, len(direct))
            compiled = direct_insertion(bodies, fire, fires, len(direct))
            if native != compiled:
                raise ValueError('Original/source full-word intrusive-queue insertion differs')
            direct.append(native)
            visited[0x037FD3B0].update(native['ownVisited'])
            returns[0x037FD3B0] += 2
    WORK.mkdir(parents=True, exist_ok=True)
    data = (json.dumps({'connected': records, 'directInsertion': direct}, sort_keys=True, separators=(',', ':')) + '\n').encode()
    path = WORK / 'native-supported-records.json.gz'
    path.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
    return {'sourceLinkedDefinitions': 3, 'connectedContexts': len(records), 'directInsertionContexts': len(direct),
        'actualReturnCountsByEntry': {hex(key): value for key, value in returns.items()},
        'ownInstructionCoverage': {hex(address): {'visited': sorted(visited[address]),
            'unvisited': sorted(set(range(address, address + CODES[address], 4)) - visited[address])} for address in SIZES},
        'originalVsFreshCExactCpuMemoryStoreAndReturnComparison': True, 'providersReplaced': [],
        'independentConnectedModel': 'Preserved BOOL/seven physical words/full mapped memory model from frozen registration fixture',
        'independentInsertionModel': 'Full nonstack memory and exact ordered store multiplicity plus raw64 signed-difference head/middle/tail/empty queue effects; period0',
        'trace': {'path': path.relative_to(ROOT).as_posix(), 'compressedSha256': digest(path.read_bytes()), 'rawSha256': digest(data),
            'compressedBytes': path.stat().st_size, 'rawBytes': len(data), 'gzipMtime': 0},
        'originalCalleeAndDataCredit': 0, 'wholeModuleAdopted': False,
        'limitations': ['Elapsed periodic rescheduling through the64-bit division helper is byte-matched but not executed by this supported corpus',
            'Invalid/already-owned alarm panic paths, asynchronous timer/callback execution and physical timing remain unsupported',
            'The signed64 difference cast follows pinned MW target behavior; this is not an Android portability claim',
            'Direct synthetic queue values characterize the code, not legal game states or chronological reachability']}
