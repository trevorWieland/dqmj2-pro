import gzip
import json
import random
from pathlib import Path
import arm7_child_alarm_engine_20261031 as engine
import arm7_child_tick324_native_20261031 as ticks
import arm7_child_alarm544_native_20261031 as queue_model
import arm7_child_alarm_programmer156_native_20261031 as programmer_model

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/lane-child-alarm-handler256-proof'
ENTRY = 0x037FD910
MASK = 0xFFFFFFFFFFFFFFFF


def cases():
    return [{'path': path, 'callback': callback, 'counter': counter, 'timer': timer, 'pending': pending}
        for path in ('empty', 'future', 'oneshot-last', 'oneshot-next', 'periodic-last', 'periodic-before', 'periodic-after')
        for callback in (0, 0x037FD7D4) for counter in (0, 0x1234) for timer, pending in ((0, 0), (0, 8), (0x8000, 8))]


def program(memory, entry, stores):
    def put(address, width, value):
        programmer_model.store(memory, address, width, value, stores)
    fire = engine.word(memory, entry + 12) | engine.word(memory, entry + 16) << 32
    delta = (fire - ticks.raw_time(memory)) & MASK
    old_ie = engine.word(memory, 0x04000210)
    ime = engine.word(memory, 0x04000208) & 0xFFFF
    count = 0xFFFE if delta >> 63 else (~delta & 0xFFFF) if delta < 0x10000 else 0
    for address, width, value in [(0x04000106, 2, 0), (0x03805988, 4, 0x037FD900), (0x03805990, 4, 0),
        (0x04000208, 2, 0), (0x04000210, 4, old_ie | 16), (0x04000208, 2, ime), (0x0380598C, 4, 1),
        (0x04000104, 2, count), (0x04000106, 2, 0xC1), (0x04000208, 2, 0),
        (0x04000210, 4, old_ie | 16), (0x04000208, 2, ime)]:
        put(address, width, value)


def setup(bodies, case, seed):
    machine = engine.setup(bodies, seed)
    cpu = machine['cpu']
    first, following = engine.DATA + 0x1000, engine.DATA + 0x1100
    for address, width, value in [(0x03805B60, 8, case['counter']), (0x04000100, 2, case['timer']),
        (0x04000214, 4, case['pending']), (0x04000208, 2, (0, 1, 0xFFFF)[seed % 3]),
        (0x04000210, 4, (0, 0x80000000, 0xFFFFFFFF)[seed % 3]), (0x0380FFF8, 4, (0, 0x80000000, 0xFFFFFFFF)[seed % 3]),
        (0x03805B5C, 4, (0, 1, 0xFFFFFFFF)[seed % 3]), (0x04000102, 2, 0xC1), (0x04000106, 2, 0xFFFF)]:
        cpu.mem_write(address, value.to_bytes(width, 'little'))
    memory = machine['snapshot']()
    now = ticks.raw_time(memory)
    start = (now + 0x1000000) & MASK
    period = 0x10000 if case['path'].startswith('periodic') else 0
    fire = (now + 1) & MASK if case['path'] == 'future' else now
    next_fire = (start + (0x20000 if case['path'] == 'periodic-before' else -0x20000)) & MASK
    has_next = case['path'] in ('oneshot-next', 'periodic-before', 'periodic-after')
    for address in (first, following):
        cpu.mem_write(address, random.Random(seed + address).randbytes(64))
    fields = [case['callback'], engine.DATA + 0x700, 0x12345678, fire & 0xFFFFFFFF, fire >> 32,
        0, following if has_next else 0, period & 0xFFFFFFFF, period >> 32, start & 0xFFFFFFFF, start >> 32]
    cpu.mem_write(first, b''.join(value.to_bytes(4, 'little') for value in fields))
    fields = [0, engine.DATA + 0x704, 0x87654321, next_fire & 0xFFFFFFFF, next_fire >> 32, first, 0, 0, 0, 0, 0]
    cpu.mem_write(following, b''.join(value.to_bytes(4, 'little') for value in fields))
    head = 0 if case['path'] == 'empty' else first
    tail = 0 if case['path'] == 'empty' else following if has_next else first
    cpu.mem_write(0x03805B6C, head.to_bytes(4, 'little') + tail.to_bytes(4, 'little'))
    return machine, first, following, fire, start, next_fire


def execute(bodies, case, seed, budget=100000):
    machine, first, following, fire, start, next_fire = setup(bodies, case, seed)
    memory, stores = machine['snapshot'](), []
    def put(address, width, value):
        programmer_model.store(memory, address, width, value, stores)
    old_ie, ime = engine.word(memory, 0x04000210), engine.word(memory, 0x04000208) & 0xFFFF
    put(0x04000106, 2, 0)
    put(0x04000208, 2, 0)
    put(0x04000210, 4, old_ie & ~16)
    put(0x04000208, 2, ime)
    put(0x0380FFF8, 4, engine.word(memory, 0x0380FFF8) | 16)
    path = case['path']
    if path == 'future':
        program(memory, first, stores)
    elif path != 'empty':
        has_next = path in ('oneshot-next', 'periodic-before', 'periodic-after')
        put(0x03805B6C, 4, following if has_next else 0)
        if has_next:
            put(following + 20, 4, 0)
        else:
            put(0x03805B70, 4, 0)
        if not path.startswith('periodic'):
            put(first, 4, 0)
        if case['callback']:
            ticks.callback(memory, stores)
        if path.startswith('periodic'):
            if start < ticks.raw_time(memory):
                raise ValueError('Selected model would enter unqualified elapsed-period division')
            put(first, 4, case['callback'])
            nodes = [(following, next_fire)] if has_next else []
            inserted = queue_model.model_insertion(memory, first, start, nodes, ticks.raw_time(memory))
            stores.extend(inserted['expectedOrderedStores'])
        head = engine.word(memory, 0x03805B6C)
        if head:
            program(memory, head, stores)
    result = machine['invoke'](ENTRY, [], budget)
    if not result['actualReturn']:
        return {'actualReturn': False, 'case': case, 'execution': result, 'returnCredit': 0}
    actual = [item for item in result['writes'] if not engine.STACK <= item[0] < engine.STACK + 0x4000]
    if actual != stores:
        mismatch = next((i for i, pair in enumerate(zip(actual, stores)) if pair[0] != pair[1]), min(len(actual), len(stores)))
        raise ValueError({'orderedStoreMismatch': mismatch, 'actual': actual[mismatch:mismatch+3], 'model': stores[mismatch:mismatch+3], 'case': case})
    if any(bytes(machine['cpu'].mem_read(base, len(data))) != bytes(data) for base, data in memory.items()):
        raise ValueError('Independent complete handler/queue/callback/platform-word model differs')
    if [item for item in result['reads'] if item[0] == 0x0380FFF8] != [[0x0380FFF8, 4]]:
        raise ValueError('Original platform word access width/count differs')
    return {'actualReturn': True, 'case': case, 'expectedOrderedStores': stores, 'execution': result,
        'runtimeWordReadWidth': 4, 'providerReplacements': []}


def oracle(body):
    raw = (ROOT / 'extract/utility/runtime/utility-child-arm7-wram.bin').read_bytes()
    original = raw[ENTRY-engine.BASE:ENTRY-engine.BASE+256]
    if original != body:
        raise ValueError('Complete compiled handler must equal all native code/pool bytes')
    records, visited, helpers = [], set(), {}
    for index, case in enumerate(cases()):
        native, compiled = execute({}, case, index), execute({ENTRY: body}, case, index)
        if native != compiled or not native['actualReturn']:
            raise ValueError('Fresh original/compiled handler failed actual return/equality: ' + str(native))
        records.append(native)
        visited.update(pc for pc in native['execution']['visited'] if ENTRY <= pc < ENTRY + 244)
        for returned in native['execution']['nestedReturns']:
            helpers[returned['entry']] = helpers.get(returned['entry'], 0) + 2
    cap = execute({}, cases()[0], 0, 1)
    if cap['actualReturn']:
        raise ValueError('Exhausted handler prefix acquired normal return credit')
    excluded = []
    for name in ('elapsed-period-division', 'malformed-queue-head'):
        case = next(item for item in cases() if item['path'] == 'periodic-last' and item['counter'] == 0x1234 and item['callback'] == 0)
        machine, first, unused, fire, start, next_fire = setup({}, case, 99)
        if name == 'elapsed-period-division':
            machine['cpu'].mem_write(first + 36, bytes(8))
        else:
            machine['cpu'].mem_write(0x03805B6C, (0xFFFFFFFF).to_bytes(4, 'little'))
        result = machine['invoke'](ENTRY, [], 100000)
        if result['actualReturn'] or result['postFaultOrBoundaryStateExcluded'] is not True:
            raise ValueError('Unsupported dependency/malformed context acquired return or post-boundary credit')
        excluded.append({'name': name, 'actualReturn': False, 'execution': result, 'sourceReturnCredit': 0})
    data = (json.dumps(records, sort_keys=True, separators=(',', ':')) + '\n').encode()
    path = WORK / 'supported-native-records.json.gz'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
    return {'vectors': len(records), 'actualOriginalAndCompiledReturns': 2 * len(records),
        'actualOriginalHelperReturnsSeparate': helpers, 'instructionCoverage': {'visited': sorted(visited),
            'unvisited': sorted(set(range(ENTRY, ENTRY+244, 4)) - visited)},
        'trace': {'path': path.relative_to(ROOT).as_posix(), 'rawSha256': engine.digest(data),
            'compressedSha256': engine.digest(path.read_bytes()), 'rawBytes': len(data), 'compressedBytes': path.stat().st_size, 'gzipMtime': 0},
        'allRawRegistersFlagsStackAndFullMemoryCompared': True, 'independentExactOrderedStoreAndQueueModel': True,
        'allLowerFunctionsOriginal': True, 'sourceLinkedDependencyAdditionalCredit': 0,
        'originalTickCallbackAndCallback16SourceCredit': 0, 'providerReplacements': [],
        'unsupportedControls': [cap, *excluded], 'unsupportedReturnCredit': 0,
        'limitations': ['Synthetic queue/IRQ/tick context, no actual asynchronous IRQ or scene reachability',
            'Original callback136 runs in positive contexts but receives zero source credit',
            'Periodic starts are at/after sampled time; elapsed-period native division remains a separate unsupported dependency',
            'Callback mutation/reentry and malformed pointers are not generalized from the selected original callback']}
