import gzip
import json
from pathlib import Path
import arm7_child_alarm_engine_20261031 as engine

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/lane-child-tick324-final'
SIZES = {0x037FD724: 176, 0x037FD86C: 148}
CODES = {0x037FD724: 160, 0x037FD86C: 124}


def store(memory, address, value, trace, width=4):
    value &= (1 << (width * 8)) - 1
    for base, data in memory.items():
        if base <= address and address + width <= base + len(data):
            data[address - base:address - base + width] = value.to_bytes(width, 'little')
            trace.append([address, width, value])
            return
    raise ValueError('Independent child tick model escaped qualified memory')


def counter(memory):
    return engine.word(memory, 0x03805B60) | engine.word(memory, 0x03805B64) << 32


def initialize(memory, stores):
    def put(address, value, width=4):
        store(memory, address, value, stores, width)

    if engine.word(memory, 0x03805B58) & 0xFFFF:
        return
    put(0x03805B58, 1, 2)
    put(0x03805B54, (engine.word(memory, 0x03805B54) & 0xFFFF) | 1, 2)
    put(0x03805B60, 0)
    put(0x03805B64, 0)
    put(0x04000102, 0, 2)
    put(0x04000100, 0, 2)
    put(0x04000102, 0xC1, 2)
    put(0x0380597C, 0x037FD7D4)
    put(0x03805984, 0)
    put(0x03805980, 1)
    irq_enable(memory, stores)
    put(0x03805B5C, 0)


def irq_enable(memory, stores):
    ie = engine.word(memory, 0x04000210)
    ime = engine.word(memory, 0x04000208) & 0xFFFF
    store(memory, 0x04000208, 0, stores, 2)
    store(memory, 0x04000210, ie | 8, stores)
    store(memory, 0x04000208, ime, stores, 2)


def callback(memory, stores):
    value = (counter(memory) + 1) & 0xFFFFFFFFFFFFFFFF
    store(memory, 0x03805B60, value & 0xFFFFFFFF, stores)
    store(memory, 0x03805B64, value >> 32, stores)
    if engine.word(memory, 0x03805B5C):
        store(memory, 0x04000102, 0, stores, 2)
        store(memory, 0x04000100, 0, stores, 2)
        store(memory, 0x04000102, 0xC1, stores, 2)
        store(memory, 0x03805B5C, 0, stores)
    store(memory, 0x0380597C, 0x037FD7D4, stores)
    store(memory, 0x03805984, 0, stores)
    irq_enable(memory, stores)
    store(memory, 0x03805980, 1, stores)


def raw_time(memory):
    upper = counter(memory) & 0xFFFFFFFFFFFF
    sample = engine.word(memory, 0x04000100) & 0xFFFF
    pending = engine.word(memory, 0x04000214)
    if pending & 8 and not sample & 0x8000:
        upper += 1
    return ((upper << 16) | sample) & 0xFFFFFFFFFFFFFFFF


def cases():
    rows = []
    for value in (0, 1, 0xFFFFFFFF, 0x100000000, 0xFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF):
        for sample in (0, 0x7FFF, 0x8000, 0xFFFF):
            for pending in (0, 8):
                for prefix in ('none', 'callback0', 'callback1', 'callbackFFFFFFFF', 'initialize'):
                    rows.append({'entry': 0x037FD724, 'counter': value, 'timer': sample, 'request': pending, 'prefix': prefix,
                        'flag': 0, 'reserved': 0xA5A4, 'reset': {'callback1': 1, 'callbackFFFFFFFF': 0xFFFFFFFF}.get(prefix, 0)})
    for flag in (0, 1, 0x8000, 0xFFFF):
        for reserved in (0, 1, 2, 0xFFFF):
            for ie in (0, 8, 0xFFFFFFFF):
                for ime in (0, 1, 0xFFFF):
                    rows.append({'entry': 0x037FD86C, 'counter': 0xFEDCBA9876543210, 'timer': 0x9876, 'request': 8,
                        'prefix': 'none', 'flag': flag, 'reserved': reserved, 'reset': 0xFFFFFFFF, 'ie': ie, 'ime': ime})
    return rows


def execute(bodies, case, seed, budget=100000):
    machine = engine.setup(bodies, seed)
    cpu = machine['cpu']
    for address, width, value in [(0x03805B60, 8, case['counter']), (0x03805B58, 2, case['flag']),
        (0x03805B54, 2, case['reserved']), (0x03805B5C, 4, case['reset']), (0x04000100, 2, case['timer']),
        (0x04000102, 2, 0xA123), (0x04000214, 4, case['request']),
        (0x04000210, 4, case.get('ie', [0, 8, 0xFFFFFFFF][seed % 3])),
        (0x04000208, 2, case.get('ime', [0, 1, 0xFFFF][seed % 3]))]:
        cpu.mem_write(address, value.to_bytes(width, 'little'))
    expected = machine['snapshot']()
    prefixes = []

    def verify(execution, stores):
        if not execution['actualReturn']:
            return False
        actual = [row for row in execution['writes'] if not engine.STACK <= row[0] < engine.STACK + 0x4000]
        if actual != stores or any(bytes(cpu.mem_read(base, len(data))) != bytes(data) for base, data in expected.items()):
            raise ValueError('Independent child full-memory, clock or ordered-store model differs: ' + str(case))
        return True

    if case['prefix'] != 'none':
        stores = []
        if case['prefix'] == 'initialize':
            initialize(expected, stores)
            entry, arguments, source_credit = 0x037FD86C, [], 'owned-matching-C'
        else:
            callback(expected, stores)
            entry, arguments, source_credit = 0x037FD7D4, [0xFFFFFFFF], 'original-callback-zero-source-credit'
        raw_initializer_return = 0x03805B5C if case['flag'] == 0 else 0x03805B58
        result = machine['invoke'](entry, arguments)
        if entry == 0x037FD86C and result['actualReturn'] and result['registers'][0] != raw_initializer_return:
            raise ValueError('Independent initializer-prefix raw R0 address-bit result differs')
        if not verify(result, stores):
            raise ValueError('Required original/linked-C producer did not actually return: ' + str(result))
        prefixes.append({'entry': hex(entry), 'sourceClass': source_credit, 'execution': result, 'expectedOrderedStores': stores})
    stores, expected_return = [], None
    if case['entry'] == 0x037FD86C:
        expected_return = 0x03805B5C if not engine.word(expected, 0x03805B58) & 0xFFFF else 0x03805B58
        initialize(expected, stores)
    else:
        expected_return = raw_time(expected)
    result = machine['invoke'](case['entry'], [], budget)
    if not verify(result, stores):
        return {'actualReturn': False, 'case': case, 'prefixes': prefixes, 'execution': result, 'returnCredit': 0}
    actual_return = result['registers'][0] | (result['registers'][1] << 32 if case['entry'] == 0x037FD724 else 0)
    if expected_return is not None and actual_return != expected_return:
        raise ValueError('Independent raw unsigned64 clock or raw32 initializer return model differs')
    return {'actualReturn': True, 'case': case, 'prefixes': prefixes, 'execution': result,
        'expectedRawReturn': expected_return, 'returnWidth': 64 if case['entry'] == 0x037FD724 else 32, 'expectedOrderedStores': stores,
        'providerReplacements': [], 'nativeCallbackAdditionalCredit': 0}


def oracle(bodies):
    raw = (ROOT / 'extract/utility/runtime/utility-child-arm7-wram.bin').read_bytes()
    originals = {address: raw[address - engine.BASE:address - engine.BASE + size] for address, size in SIZES.items()}
    if set(bodies) != set(SIZES) or any(bodies[address] != originals[address] for address in bodies):
        raise ValueError('Both complete child tick C outputs must genuinely match native bytes')
    counts, visited = {address: 0 for address in bodies}, {address: set() for address in bodies}
    records, nested, original_callback_returns = [], {}, 0
    for index, case in enumerate(cases()):
        native, compiled = execute(originals, case, index), execute(bodies, case, index)
        if native != compiled or not native['actualReturn']:
            raise ValueError('Original/compiled child tick context failed full return/effect equality: ' + str(native))
        records.append(native)
        counts[case['entry']] += 2
        executions = [native['execution']]
        for prefix in native['prefixes']:
            executions.append(prefix['execution'])
            address = int(prefix['entry'], 0)
            if address in counts:
                counts[address] += 2
            else:
                original_callback_returns += 2
        for execution in executions:
            for returned in execution['nestedReturns']:
                nested[returned['entry']] = nested.get(returned['entry'], 0) + 2
            for address, size in CODES.items():
                visited[address].update(pc for pc in execution['visited'] if address <= pc < address + size)
    unsupported = [execute(originals, cases()[0], 37, budget=1), execute(originals, cases()[-1], 38, budget=1)]
    if any(row['actualReturn'] for row in unsupported):
        raise ValueError('Child tick prologue exhaustion gained return credit')
    data = (json.dumps(records, sort_keys=True, separators=(',', ':')) + '\n').encode()
    path = WORK / 'supported-native-records.json.gz'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
    return {'vectors': len(records), 'actualOuterReturns': len(records) * 2,
        'actualReturnCountsByEntry': {hex(key): value for key, value in counts.items()},
        'actualOriginalCallbackPrefixReturnsSeparate': original_callback_returns, 'actualOriginalHelperReturnsSeparate': nested,
        'freshOriginalAndTwoSourceLinkedCExecutions': True, 'independentFullMemoryAndExactOrderedStoreModel': True,
        'allRawRegistersFlagsAndStackCompared': True, 'providerReplacements': [],
        'ownInstructionCoverage': {hex(address): {'visited': sorted(visited[address]),
            'unvisited': sorted(set(range(address, address + CODES[address], 4)) - visited[address])} for address in bodies},
        'trace': {'path': path.relative_to(ROOT).as_posix(), 'compressedSha256': engine.digest(path.read_bytes()),
            'rawSha256': engine.digest(data), 'rawBytes': len(data), 'compressedBytes': path.stat().st_size, 'gzipMtime': 0},
        'unsupportedControls': unsupported, 'unsupportedReturnCredit': 0, 'originalDependencyOrDataSourceCredit': 0,
        'limitations': ['Fresh synthetic loader BSS and explicitly seeded register/memory contexts; no original boot or scene reachability',
            'Original callback037FD7D4 executes as a separately counted producer and receives zero source credit',
            'Initializer stores that measured original callback; no claim that its nonmatching C hypothesis is linked',
            'Clock math uses raw 48-bit counter, 16-bit sample and pending-bit correction, not physical timing units',
            'Initializer preserves observed raw R0 address bits without assigning original API, status or pointer purpose',
            'No asynchronous interrupts, counter race/atomicity, undocumented callbacks, malformed memory or Android portability claim']}
