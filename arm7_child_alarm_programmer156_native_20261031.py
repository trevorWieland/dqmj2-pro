import gzip
import json
import random
from pathlib import Path
import arm7_child_alarm_engine_20261031 as engine

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/lane-child-alarm-programmer156-qualified-final'
ENTRY, GETTER = 0x037FDD30, 0x037FD724


def store(memory, address, width, value, stores):
    value &= (1 << (width * 8)) - 1
    for base, data in memory.items():
        if base <= address and address + width <= base + len(data):
            data[address - base:address - base + width] = value.to_bytes(width, 'little')
            stores.append([address, width, value])
            return
    raise ValueError('Independent timer-programmer model escaped mapped memory')


def cases():
    clocks = [(0, 0, 0), (0, 0xFFFF, 8), (0xFFFFFFFFFFFF, 0, 8),
        (0xFFFFFFFFFFFFFFFF, 0x7FFF, 8), (1, 0x8000, 8), (1, 1, 8)]
    return [{'counter': counter, 'sample': sample, 'pending': pending, 'delta': delta}
        for counter, sample, pending in clocks for delta in (0, 1, 0xFFFE, 0xFFFF, 0x10000, 0x7FFFFFFFFFFFFFFF, 0x8000000000000000, 0xFFFFFFFFFFFFFFFF)]


def execute(bodies, case, seed, budget=100000):
    machine = engine.setup(bodies, seed)
    cpu = machine['cpu']
    old_mask = [0, 16, 0x80000000, 0xFFFFFFFF][seed % 4]
    master = [0, 1, 0xFFFF][seed // 4 % 3]
    upper = (case['counter'] & 0xFFFFFFFFFFFF) + (bool(case['pending'] & 8) and not case['sample'] & 0x8000)
    now = ((upper << 16) | case['sample']) & 0xFFFFFFFFFFFFFFFF
    fire = (now + case['delta']) & 0xFFFFFFFFFFFFFFFF
    record = engine.DATA + 0x1000
    data = bytearray(random.Random(seed + 20261031).randbytes(64))
    data[12:20] = fire.to_bytes(8, 'little')
    cpu.mem_write(record, bytes(data))
    for address, width, value in [(0x03805B60, 8, case['counter']), (0x04000100, 2, case['sample']),
        (0x04000214, 4, case['pending']), (0x04000210, 4, old_mask), (0x04000208, 2, master),
        (0x04000104, 2, 0xA123), (0x04000106, 2, 0x9876)]:
        cpu.mem_write(address, value.to_bytes(width, 'little'))
    memory, stores = machine['snapshot'](), []

    def put(address, width, value):
        store(memory, address, width, value, stores)

    count = 0xFFFE if case['delta'] >> 63 else (~case['delta'] & 0xFFFF) if case['delta'] < 0x10000 else 0
    put(0x04000106, 2, 0)
    put(0x03805988, 4, 0x037FD900)
    put(0x03805990, 4, 0)
    put(0x04000208, 2, 0)
    put(0x04000210, 4, old_mask | 16)
    put(0x04000208, 2, master)
    put(0x0380598C, 4, 1)
    put(0x04000104, 2, count)
    put(0x04000106, 2, 0xC1)
    put(0x04000208, 2, 0)
    put(0x04000210, 4, old_mask | 16)
    put(0x04000208, 2, master)
    execution = machine['invoke'](ENTRY, [record], budget)
    if not execution['actualReturn']:
        return {'actualReturn': False, 'case': case, 'execution': execution, 'returnCredit': 0}
    actual = [row for row in execution['writes'] if not engine.STACK <= row[0] < engine.STACK + 0x4000]
    if actual != stores or execution['registers'][0] != old_mask | 16:
        raise ValueError('Independent timer-count/callback/IRQ/store/raw-R0 model differs')
    if any(bytes(cpu.mem_read(base, len(data))) != bytes(data) for base, data in memory.items()):
        raise ValueError('Complete timer-programmer descriptor/data/memory preservation model differs')
    return {'actualReturn': True, 'case': case, 'now': now, 'fire': fire, 'count': count,
        'expectedOrderedStores': stores, 'execution': execution, 'providerReplacements': []}


def oracle(body, getter):
    raw = (ROOT / 'extract/utility/runtime/utility-child-arm7-wram.bin').read_bytes()
    originals = {ENTRY: raw[ENTRY - engine.BASE:ENTRY - engine.BASE + 156], GETTER: raw[GETTER - engine.BASE:GETTER - engine.BASE + 176]}
    bodies = {ENTRY: body, GETTER: getter}
    if bodies != originals:
        raise ValueError('Full programmer and freshly source-linked getter must match native bytes')
    records, visited, helpers, getter_returns = [], set(), {}, 0
    for index, case in enumerate(cases()):
        native, compiled = execute(originals, case, index), execute(bodies, case, index)
        if native != compiled or not native['actualReturn']:
            raise ValueError('Fresh original/programmer-C/getter-C executions did not return/equal: ' + str(native))
        records.append(native)
        visited.update(pc for pc in native['execution']['visited'] if ENTRY <= pc < ENTRY + 140)
        for returned in native['execution']['nestedReturns']:
            address = int(returned['entry'], 0)
            if address == GETTER:
                getter_returns += 2
            else:
                helpers[returned['entry']] = helpers.get(returned['entry'], 0) + 2
    cap = execute(originals, cases()[0], 13, 1)
    if cap['actualReturn']:
        raise ValueError('Programmer prologue exhaustion gained normal return credit')
    data = (json.dumps(records, sort_keys=True, separators=(',', ':')) + '\n').encode()
    path = WORK / 'supported-native-records.json.gz'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
    return {'vectors': len(records), 'actualOriginalAndCompiledReturns': len(records) * 2,
        'actualFreshSourceLinkedGetterReturnsSeparate': getter_returns, 'actualOriginalHelperReturnsSeparate': helpers,
        'allRawRegistersFlagsAndStackCompared': True, 'independentFullMemoryAndExactOrderedStoreModel': True,
        'instructionCoverage': {'visited': sorted(visited), 'unvisited': sorted(set(range(ENTRY, ENTRY + 140, 4)) - visited)},
        'trace': {'path': path.relative_to(ROOT).as_posix(), 'compressedSha256': engine.digest(path.read_bytes()),
            'rawSha256': engine.digest(data), 'rawBytes': len(data), 'compressedBytes': path.stat().st_size, 'gzipMtime': 0},
        'unsupportedControls': [cap], 'unsupportedReturnCredit': 0, 'callbackSourceCredit': 0, 'callbackInvokedByThisProof': False,
        'originalDependencyOrDataSourceCredit': 0, 'providerReplacements': [],
        'limitations': ['Synthetic mapped timer/IRQ context, no physical timing units, asynchronous IRQ or scene reachability',
            'Stored original callback16 is separately boundary-qualified and never counted as reconstructed source',
            'Freshly compiled getter dependency is source-linked with zero additional coverage credit',
            'Unsigned64 subtraction then target signed interpretation is measured for this pinned32-bit compiler, not Android portability']}
