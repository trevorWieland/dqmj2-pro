import gzip
import json
import random
from pathlib import Path
import arm7_child_alarm_engine_20261031 as engine

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/lane-child-alarm-control224-final'
SIZES = {0x037FDA10: 144, 0x037FDCE0: 80}
CODES = {0x037FDA10: 140, 0x037FDCE0: 72}


def store(memory, address, value, trace, width=4):
    value &= (1 << (width * 8)) - 1
    for base, data in memory.items():
        if base <= address and address + width <= base + len(data):
            data[address - base:address - base + width] = value.to_bytes(width, 'little')
            trace.append([address, width, value])
            return
    raise ValueError('Independent child control model escaped mapped backing')


def cases():
    rows = []
    clocks = [(0, 0, 0), (0, 0xFFFF, 0), (0xFFFFFFFFFFFF, 0, 8), (0, 0x8000, 8), (1, 0x7FFF, 8)]
    for counter, timer, request in clocks:
        for length in (1, 3):
            for selected in range(length):
                for active in (False, True):
                    for delta in (0, 1, 0x10000, 0x8000000000000000):
                        rows.append({'entry': 0x037FDA10, 'counter': counter, 'timer': timer, 'request': request,
                            'length': length, 'selected': selected, 'active': active, 'delta': delta})
    for flag in (0, 1, 0x8000, 0xFFFF):
        for reserved in (0, 1, 2, 0xFFFF):
            for ie in (0, 8, 0xFFFFFFFF):
                for ime in (0, 1, 0xFFFF):
                    rows.append({'entry': 0x037FDCE0, 'flag': flag, 'reserved': reserved, 'ie': ie, 'ime': ime})
    return rows


def timer_model(memory, entry, fire, now, stores):
    def put(address, width, value):
        store(memory, address, value, stores, width)

    put(0x04000106, 2, 0)
    put(0x03805988, 4, 0x037FD900)
    put(0x03805990, 4, 0)
    ie = engine.word(memory, 0x04000210)
    ime = engine.word(memory, 0x04000208) & 0xFFFF
    put(0x04000208, 2, 0)
    put(0x04000210, 4, ie | 16)
    put(0x04000208, 2, ime)
    put(0x0380598C, 4, 1)
    delta = (fire - now) & 0xFFFFFFFFFFFFFFFF
    count = 0xFFFE if delta >> 63 else (~delta & 0xFFFF) if delta < 0x10000 else 0
    put(0x04000104, 2, count)
    put(0x04000106, 2, 0xC1)
    put(0x04000208, 2, 0)
    put(0x04000210, 4, ie | 16)
    put(0x04000208, 2, ime)


def execute(bodies, case, seed, budget=100000):
    machine = engine.setup(bodies, seed)
    cpu = machine['cpu']
    mask = 0xFFFFFFFFFFFFFFFF
    records = []
    if case['entry'] == 0x037FDA10:
        cpu.mem_write(0x03805B60, case['counter'].to_bytes(8, 'little'))
        cpu.mem_write(0x04000100, case['timer'].to_bytes(2, 'little'))
        cpu.mem_write(0x04000214, case['request'].to_bytes(4, 'little'))
        upper = (case['counter'] & 0xFFFFFFFFFFFF) + (bool(case['request'] & 8) and not case['timer'] & 0x8000)
        now = ((upper << 16) | case['timer']) & mask
        for index in range(case['length']):
            address = engine.DATA + 0x1000 + index * 64
            data = bytearray(random.Random(seed * 83 + index).randbytes(64))
            fire = (now + case['delta'] + index * 4) & mask
            values = {0: 0x037FD900, 12: fire & 0xFFFFFFFF, 16: fire >> 32,
                20: address - 64 if index else 0, 24: address + 64 if index + 1 < case['length'] else 0}
            for offset, value in values.items():
                data[offset:offset + 4] = value.to_bytes(4, 'little')
            cpu.mem_write(address, bytes(data))
            records.append({'address': address, 'fire': fire})
        entry = records[case['selected']]['address']
        if not case['active']:
            cpu.mem_write(entry, bytes(4))
        cpu.mem_write(0x03805B6C, records[0]['address'].to_bytes(4, 'little'))
        cpu.mem_write(0x03805B70, records[-1]['address'].to_bytes(4, 'little'))
        ie, ime = [0, 8, 0xFFFFFFFF][seed % 3], [0, 1, 0xFFFF][seed % 3]
        arguments = [entry]
    else:
        for address, width, value in [(0x03805B68, 2, case['flag']), (0x03805B54, 2, case['reserved']),
            (0x03805B6C, 4, engine.DATA + 0x1000), (0x03805B70, 4, engine.DATA + 0x2000)]:
            cpu.mem_write(address, value.to_bytes(width, 'little'))
        ie, ime = case['ie'], case['ime']
        arguments = []
    cpu.mem_write(0x04000210, ie.to_bytes(4, 'little'))
    cpu.mem_write(0x04000208, ime.to_bytes(2, 'little'))
    expected, stores = machine['snapshot'](), []

    def put(address, value, width=4):
        store(expected, address, value, stores, width)

    if case['entry'] == 0x037FDA10 and case['active']:
        index = case['selected']
        previous = records[index - 1]['address'] if index else 0
        following = records[index + 1]['address'] if index + 1 < len(records) else 0
        if following:
            put(following + 20, previous)
        else:
            put(0x03805B70, previous)
        if previous:
            put(previous + 24, following)
        else:
            put(0x03805B6C, following)
            if following:
                timer_model(expected, following, records[index + 1]['fire'], now, stores)
        for offset in (0, 28, 32):
            put(entry + offset, 0)
    elif case['entry'] == 0x037FDCE0 and case['flag'] == 0:
        put(0x03805B68, 1, 2)
        put(0x03805B54, case['reserved'] | 2, 2)
        put(0x03805B6C, 0)
        put(0x03805B70, 0)
        put(0x04000208, 0, 2)
        put(0x04000210, ie & ~16)
        put(0x04000208, ime, 2)
    result = machine['invoke'](case['entry'], arguments, budget)
    if not result['actualReturn']:
        return {'actualReturn': False, 'case': case, 'execution': result, 'returnCredit': 0}
    actual_stores = [row for row in result['writes'] if not engine.STACK <= row[0] < engine.STACK + 0x4000]
    if actual_stores != stores or any(bytes(cpu.mem_read(base, len(data))) != bytes(data) for base, data in expected.items()):
        raise ValueError('Independent child unlink/initialization/timer/full-memory/store model differs: ' + str(case))
    return {'actualReturn': True, 'case': case, 'execution': result, 'expectedOrderedStores': stores,
        'logicalQueueContext': records, 'providerReplacements': []}


def oracle(bodies):
    raw = (ROOT / 'extract/utility/runtime/utility-child-arm7-wram.bin').read_bytes()
    originals = {address: raw[address - engine.BASE:address - engine.BASE + size] for address, size in SIZES.items()}
    if set(bodies) != set(SIZES) or any(bodies[address] != originals[address] for address in bodies):
        raise ValueError('Two full current native/C child units must genuinely match')
    records, counts, visited = [], {address: 0 for address in bodies}, {address: set() for address in bodies}
    nested = {}
    for index, case in enumerate(cases()):
        native, compiled = execute(originals, case, index), execute(bodies, case, index)
        if native != compiled or not native['actualReturn']:
            raise ValueError('Fresh original/compiled child control units did not return/equal: ' + str(native))
        records.append(native)
        counts[case['entry']] += 2
        for returned in native['execution']['nestedReturns']:
            nested[returned['entry']] = nested.get(returned['entry'], 0) + 2
        for address, size in CODES.items():
            visited[address].update(pc for pc in native['execution']['visited'] if address <= pc < address + size)
    cap = execute(originals, cases()[0], 37, budget=1)
    if cap['actualReturn']:
        raise ValueError('Child control prologue exhaustion gained return credit')
    data = (json.dumps(records, sort_keys=True, separators=(',', ':')) + '\n').encode()
    path = WORK / 'supported-native-records.json.gz'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
    return {'vectors': len(records), 'actualReturnCountsByEntry': {hex(key): value for key, value in counts.items()},
        'actualOriginalHelperReturnsSeparate': nested, 'freshOriginalAndTwoSourceLinkedCExecutions': True,
        'independentFullMemoryAndExactOrderedStoreModel': True, 'allRawRegistersFlagsAndStackCompared': True,
        'providerReplacements': [], 'ownInstructionCoverage': {hex(address): {'visited': sorted(visited[address]),
            'unvisited': sorted(set(range(address, address + CODES[address], 4)) - visited[address])} for address in bodies},
        'trace': {'path': path.relative_to(ROOT).as_posix(), 'compressedSha256': engine.digest(path.read_bytes()),
            'rawSha256': engine.digest(data), 'rawBytes': len(data), 'compressedBytes': path.stat().st_size, 'gzipMtime': 0},
        'unsupportedControls': [cap], 'unsupportedReturnCredit': 0, 'originalDependencyOrDataSourceCredit': 0,
        'limitations': ['Fresh synthetic loader BSS and finite disposable queue contexts; no boot/scene/lifecycle reachability',
            'Nonempty queue with an inactive record is deliberate raw-state coverage, not a supported lifecycle assertion',
            'Active cancellation clears handler and 64-bit period but preserves start/tag and its own stored links',
            'Initializer passes actual reservation index 1 and disables IRQ mask 16; no physical timing or interrupts',
            'Original programmer and IRQ/tick helpers retain zero source credit; callback bits are not invoked',
            'No null/malformed/cyclic queue, asynchronous concurrency, callback-ABI or native Android claim']}
