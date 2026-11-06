import gzip
import hashlib
import json
from pathlib import Path
import random
import arm7_child_alarm_engine_20261031 as engine

ROOT = Path(__file__).resolve().parent
SIZES = {0x037FDAA0: 124, 0x037FDB1C: 116, 0x037FDB90: 304}
CODES = {0x037FDAA0: 124, 0x037FDB1C: 116, 0x037FDB90: 300}
WORK = ROOT / 'work/arm7-bulk-20261030/lane-child-alarm-abi544-final'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def model_insertion(memory, record, fire, nodes, now):
    mask = (1 << 64) - 1
    queue, io = 0x03805B6C, 0x04000000
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
            put(queue + 0, 4, record)
    else:
        put(record + 24, 4, 0)
        put(queue + 4, 4, record)
        put(record + 20, 4, previous)
        if previous:
            put(previous + 24, 4, record)
        else:
            put(queue + 4, 4, record)
            put(queue + 0, 4, record)
    if not previous:
        put(io + 0x106, 2, 0)
        put(0x03805988, 4, 0x037FD900)
        put(0x03805990, 4, 0)
        old_ie = engine.word(memory, io + 0x210)
        ime = engine.word(memory, io + 0x208) & 0xFFFF
        put(io + 0x208, 2, 0)
        put(io + 0x210, 4, old_ie | 16)
        put(io + 0x208, 2, ime)
        put(0x0380598C, 4, 1)
        delta = (fire - now) & mask
        count = 0xFFFE if delta >> 63 else (~delta & 0xFFFF) if delta < 0x10000 else 0
        put(io + 0x104, 2, count)
        put(io + 0x106, 2, 0xC1)
        put(io + 0x208, 2, 0)
        put(io + 0x210, 4, old_ie | 16)
        put(io + 0x208, 2, ime)
    return {'insertedIndex': index, 'previous': previous, 'following': following, 'expectedOrderedStores': stores}


def cases():
    rows = []
    for start in (0, 1, 0xFFFF, 0x10000, 0x8000000000000000, 0xFFFFFFFFFFFFFFFF):
        for period in (0, 1, 0x82E, 0x100000000, 0xFFFFFFFFFFFFFFFF):
            for nonempty in (False, True):
                rows.append({'entry': 0x037FDAA0, 'counter': 0, 'timer': 0, 'request': 0, 'start': start, 'period': period, 'nonempty': nonempty})
    for delay in (0, 1, 0xFFFF, 0x10000, 0x7FFFFFFFFFFFFFFF, 0x8000000000000000, 0xFFFFFFFFFFFFFFFF):
        for counter in (0, 0xFFFFFFFFFFFF):
            for timer in (0, 0x7FFF, 0x8000, 0xFFFF):
                for request in (0, 8):
                    for nonempty in (False, True):
                        rows.append({'entry': 0x037FDB1C, 'counter': counter, 'timer': timer, 'request': request, 'delay': delay, 'nonempty': nonempty})
    for fire in (0, 1, 0xFFFF, 0x10000, 0x7FFFFFFFFFFFFFFF, 0x8000000000000000, 0xFFFFFFFFFFFFFFFF):
        for nonempty in (False, True):
            rows.append({'entry': 0x037FDB90, 'counter': 0, 'timer': 0, 'request': 0, 'fire': fire, 'nonempty': nonempty})
    return rows


def execute(bodies, case, seed, budget=100000):
    machine = engine.setup(bodies, seed)
    cpu = machine['cpu']
    cpu.mem_write(0x03805B60, case['counter'].to_bytes(8, 'little'))
    cpu.mem_write(engine.IO + 0x100, case['timer'].to_bytes(2, 'little'))
    cpu.mem_write(engine.IO + 0x214, case['request'].to_bytes(4, 'little'))
    ie = [0, 8, 0x80000000, 0xFFFFFFFF][seed % 4]
    ime = [0, 1, 0xFFFF][seed % 3]
    cpu.mem_write(engine.IO + 0x210, ie.to_bytes(4, 'little'))
    cpu.mem_write(engine.IO + 0x208, ime.to_bytes(2, 'little'))
    upper = (case['counter'] & 0xFFFFFFFFFFFF) + (bool(case['request'] & 8) and not case['timer'] & 0x8000)
    now = ((upper << 16) | case['timer']) & 0xFFFFFFFFFFFFFFFF
    record = engine.DATA + 0x100
    data = bytearray(random.Random(seed + 713).randbytes(44))
    data[:4] = bytes(4)
    cpu.mem_write(record, bytes(data))
    values = [(now - 1) & 0xFFFFFFFFFFFFFFFF, (now + 16) & 0xFFFFFFFFFFFFFFFF] if case['nonempty'] else []
    nodes = [(engine.DATA + 0x1000 + index * 64, value) for index, value in enumerate(values)]
    for index, (address, value) in enumerate(nodes):
        words = [0, 0, 0, value & 0xFFFFFFFF, value >> 32,
            nodes[index - 1][0] if index else 0, nodes[index + 1][0] if index + 1 < len(nodes) else 0, 0, 0, 0, 0]
        cpu.mem_write(address, b''.join(word.to_bytes(4, 'little') for word in words))
    cpu.mem_write(0x03805B6C, (nodes[0][0] if nodes else 0).to_bytes(4, 'little'))
    cpu.mem_write(0x03805B70, (nodes[-1][0] if nodes else 0).to_bytes(4, 'little'))
    expected = machine['snapshot']()
    stores = []
    handler, argument = (0, 0x037FD900)[seed % 2], (0, engine.DATA + 0x200, 0x80000000, 0xFFFFFFFF)[seed % 4]

    def put(address, value):
        engine.store(expected, address, value, stores)

    if case['entry'] == 0x037FDAA0:
        period, start = case['period'], case['start']
        for offset, value in [(28, period & 0xFFFFFFFF), (32, period >> 32), (36, start & 0xFFFFFFFF), (40, start >> 32), (0, handler), (4, argument)]:
            put(record + offset, value)
        fire = ((start + period * (((now - start) // period) + 1)) & 0xFFFFFFFFFFFFFFFF) if period and start < now else start if period else 0
        arguments = [record, start & 0xFFFFFFFF, start >> 32, period & 0xFFFFFFFF, period >> 32, handler, argument]
    elif case['entry'] == 0x037FDB1C:
        delay = case['delay']
        for offset, value in [(28, 0), (32, 0), (0, handler), (4, argument)]:
            put(record + offset, value)
        fire = (now + delay) & 0xFFFFFFFFFFFFFFFF
        arguments = [record, delay & 0xFFFFFFFF, delay >> 32, handler, argument]
    else:
        cpu.mem_write(record + 28, bytes(8))
        expected = machine['snapshot']()
        fire = case['fire']
        arguments = [record, fire & 0xFFFFFFFF, fire >> 32]
    model = model_insertion(expected, record, fire, nodes, now)
    stores += model['expectedOrderedStores']
    result = machine['invoke'](case['entry'], arguments, budget)
    if not result['actualReturn']:
        return {'actualReturn': False, 'case': case, 'execution': result, 'returnCredit': 0}
    actual_stores = [row for row in result['writes'] if not engine.STACK <= row[0] < engine.STACK + 0x4000]
    if actual_stores != stores or any(bytes(cpu.mem_read(base, len(data))) != bytes(data) for base, data in expected.items()):
        raise ValueError('Independent child queue/64-bit clock/store/memory model differs: ' + str(case))
    return {'actualReturn': True, 'case': case, 'now': now, 'fire': fire, 'handlerPointerBits': handler, 'opaqueArgument': argument,
        'model': model, 'execution': result, 'bssContext': 'Zero-filled measured loader BSS; no kernel/boot initialization path claim'}


def oracle(bodies):
    raw = (ROOT / 'extract/utility/runtime/utility-child-arm7-wram.bin').read_bytes()
    originals = {address: raw[address - engine.BASE:address - engine.BASE + size] for address, size in SIZES.items()}
    if set(bodies) != set(SIZES) or any(bodies[address] != originals[address] for address in bodies):
        raise ValueError('All child source-linked units must genuinely match complete native bytes')
    records, counts, visited = [], {address: 0 for address in bodies}, {address: set() for address in bodies}
    for index, case in enumerate(cases()):
        native, compiled = execute(originals, case, index), execute(bodies, case, index)
        if native != compiled or not native['actualReturn']:
            raise ValueError('Original/new child C group did not actually return/equal: ' + str(native))
        records.append(native)
        counts[case['entry']] += 2
        for returned in native['execution']['nestedReturns']:
            address = int(returned['entry'], 0)
            if address in counts:
                counts[address] += 2
        for address, code_bytes in CODES.items():
            visited[address].update(pc for pc in native['execution']['visited'] if address <= pc < address + code_bytes)
    cap = execute(originals, cases()[0], 91, budget=1)
    elapsed = execute(originals, {'entry': 0x037FDAA0, 'counter': 0, 'timer': 1, 'request': 0, 'start': 0, 'period': 1, 'nonempty': False}, 13)
    if elapsed['actualReturn'] or elapsed['execution']['pc'] != '0x3805330' or 'instruction scope' not in str(elapsed['execution']['error']):
        raise ValueError('Unclassified original division-tail refusal differs')
    if cap['actualReturn']:
        raise ValueError('Child prologue exhaustion gained return credit')
    data = (json.dumps(records, sort_keys=True, separators=(',', ':')) + '\n').encode()
    WORK.mkdir(parents=True, exist_ok=True)
    path = WORK / 'supported-native-records.json.gz'
    path.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
    return {'vectors': len(records), 'actualReturnCountsByEntry': {hex(key): value for key, value in counts.items()},
        'freshOriginalAndThreeSourceLinkedCExecutions': True, 'independentFullMemoryAndExactOrderedStoreModel': True,
        'allRawRegistersFlagsAndStackCompared': True, 'providerReplacements': [],
        'ownInstructionCoverage': {hex(address): {'visited': sorted(visited[address]), 'unvisited': sorted(set(range(address, address + CODES[address], 4)) - visited[address])} for address in bodies},
        'trace': {'path': path.relative_to(ROOT).as_posix(), 'compressedSha256': digest(path.read_bytes()), 'rawSha256': digest(data), 'compressedBytes': path.stat().st_size, 'rawBytes': len(data), 'gzipMtime': 0},
        'unsupportedControls': [cap, elapsed], 'unsupportedReturnCredit': 0, 'originalDependencyOrDataSourceCredit': 0,
        'limitations': ['Measured child loader BSS is explicitly zero-filled; no original child boot/kernel/scene reachability claimed',
            'Elapsed periodic probe stops at unclassified division instruction03805330 with no return/post-boundary credit; panic paths unexecuted; full bytes match',
            'Callbacks are opaque pointer bits stored but never invoked; no callback ABI or asynchronous hardware claim',
            'Child queue is head0/tail4 at03805B6C, distinct from the host12-byte view; no original allocation extent/data credit',
            'Time inputs are raw unsigned64 values and modular signed-difference order; no physical timing or Android portability claim']}

