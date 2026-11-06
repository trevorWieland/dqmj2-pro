import gzip
import hashlib
import json
from pathlib import Path
import arm7_lane_alarm_registration_native_20261031 as fixture
import arm7_alarm_family572_connected_20261031 as insertion
from unicorn import UC_HOOK_CODE

ROOT = Path(__file__).resolve().parent
ADDRESS, SIZE = 0x037FD4DC, 112
WORK = ROOT / 'work/arm7-bulk-20261030/lane-host-oneshot112-final'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    return [{'delay': delay, 'counter': counter, 'timer': timer, 'request': request, 'nonempty': nonempty}
        for delay in (0, 1, 0xFFFF, 0x10000, 0x7FFFFFFFFFFFFFFF, 0x8000000000000000, 0xFFFFFFFFFFFFFFFF)
        for counter in (0, 0xFFFFFFFFFFFF) for timer in (0, 0x7FFF, 0x8000, 0xFFFF)
        for request in (0, 8) for nonempty in (False, True)]


def execute(body, dependency, case, seed, budget=20000):
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    context = dict(case, tick=True, alarm=True, enabled=0, passes=1)
    machine = fixture.setup(fixture.ADDRESS, raw[fixture.ADDRESS - 0x037F8000:fixture.ADDRESS - 0x037F8000 + fixture.SIZE], context, seed)
    cpu = machine['cpu']
    cpu.mem_write(ADDRESS, body)
    cpu.mem_write(0x037FD3B0, dependency)
    record = fixture.ALARM
    cpu.mem_write(record, bytes(4))
    upper = case['counter'] & 0xFFFFFFFFFFFF
    upper += bool(case['request'] & 8) and not case['timer'] & 0x8000
    now = ((upper << 16) | case['timer']) & 0xFFFFFFFFFFFFFFFF
    fire = (now + case['delay']) & 0xFFFFFFFFFFFFFFFF
    values = [(now - 1) & 0xFFFFFFFFFFFFFFFF, (now + 16) & 0xFFFFFFFFFFFFFFFF] if case['nonempty'] else []
    nodes = [(fixture.DATA + 0x1000 + index * 64, value) for index, value in enumerate(values)]
    for index, (address, value) in enumerate(nodes):
        words = [0x037FE65C, 0, 0, value & 0xFFFFFFFF, value >> 32,
            nodes[index - 1][0] if index else 0, nodes[index + 1][0] if index + 1 < len(nodes) else 0, 0, 0, 0, 0]
        cpu.mem_write(address, b''.join(word.to_bytes(4, 'little') for word in words))
    cpu.mem_write(0x038078AC, (nodes[0][0] if nodes else 0).to_bytes(4, 'little'))
    cpu.mem_write(0x038078B0, (nodes[-1][0] if nodes else 0).to_bytes(4, 'little'))
    argument = [0, fixture.DATA + 0x80, 0x80000000, 0xFFFFFFFF][seed % 4]
    expected = fixture.engine.snapshot(machine)
    stores = []
    for offset, value in [(28, 0), (32, 0), (0, 0x037FE65C), (4, argument)]:
        fixture.engine.store(expected, record + offset, value, stores)
    model = insertion.model_insertion(expected, record, fire, nodes)
    if model['previous'] == 0:
        count = 0xFFFE if case['delay'] >> 63 else (~case['delay'] & 0xFFFF) if case['delay'] < 0x10000 else 0
        for store in model['expectedOrderedStores']:
            if store[0] == fixture.IO + 0x104:
                store[2] = count
        expected[fixture.IO][0x104:0x106] = count.to_bytes(2, 'little')
    stores += model['expectedOrderedStores']
    visited = []
    cpu.hook_add(UC_HOOK_CODE, lambda machine, pc, width, unused: visited.append(pc))
    result = machine['invoke'](ADDRESS, [record, case['delay'] & 0xFFFFFFFF, case['delay'] >> 32, 0x037FE65C, argument], True, budget)
    if not result['actualReturn']:
        return {'actualReturn': False, 'execution': result, 'postBoundaryStateExcluded': True}
    checked = fixture.engine.result(machine, result, expected, None, stores)
    if checked['orderedNonstackWrites'] != stores:
        raise ValueError('Independent one-shot ordered stores and original native effect sequence differ')
    return {'actualReturn': True, 'case': case, 'now': now, 'fire': fire, 'argument': argument,
        'insertionModel': model, 'execution': checked,
        'ownVisited': sorted({pc for pc in visited if ADDRESS <= pc < ADDRESS + SIZE}),
        'sourceDependencyVisited': sorted({pc for pc in visited if 0x037FD3B0 <= pc < 0x037FD3B0 + 296})}


def oracle(body, dependency):
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    original = raw[ADDRESS - 0x037F8000:ADDRESS - 0x037F8000 + SIZE]
    original_dependency = raw[0x53B0:0x53B0 + 300]
    if body != original or dependency != original_dependency:
        raise ValueError('One-shot and source-linked insertion must match their complete native bytes')
    records, nested, visited = [], 0, set()
    for index, case in enumerate(cases()):
        native, compiled = execute(original, original_dependency, case, index), execute(body, dependency, case, index)
        if native != compiled or not native['actualReturn']:
            raise ValueError('Original/compiled one-shot effects,64-bit wrap or true return differ')
        records.append(native)
        nested += 2 * native['execution']['actualNestedReturns'].get('0x37fd3b0', 0)
        visited.update(native['ownVisited'])
    cap = execute(original, original_dependency, cases()[0], 91, budget=1)
    if cap['actualReturn']:
        raise ValueError('Exhausted one-shot prologue counted as a return')
    data = (json.dumps(records, sort_keys=True, separators=(',', ':')) + '\n').encode()
    WORK.mkdir(parents=True, exist_ok=True)
    path = WORK / 'supported-native-records.json.gz'
    path.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
    return {'vectors': len(records), 'actualOriginalAndCompiledReturns': 2 * len(records),
        'actualSourceLinkedInsertionReturnsSeparate': nested, 'providerReplacements': [], 'ownVisited': sorted(visited),
        'ownUnvisited': sorted(set(range(ADDRESS, ADDRESS + SIZE, 4)) - visited), 'sourceLinkedDependencyCount': 1,
        'independentFullMemoryAndExactOrderedStoreModel': True, 'allFullRegistersFlagsStackCompared': True,
        'trace': {'path': path.relative_to(ROOT).as_posix(), 'compressedSha256': digest(path.read_bytes()), 'rawSha256': digest(data), 'rawBytes': len(data), 'compressedBytes': path.stat().st_size, 'gzipMtime': 0},
        'unsupportedControls': [cap], 'unsupportedReturnCredit': 0,
        'limitations': ['Native prerequisites and original tick/timer/IRQ helpers execute; no hardware timing or asynchronous callback claim',
            'Delay is an unsigned64 bit pattern; modulo addition and raw signed-difference queue placement do not imply real chronology',
            'Original null/already-owned panic paths and arbitrary cyclic or malformed queue inputs are unsupported',
            'Only112 owned bytes are new coverage; the freshly source-linked300-byte dependency receives no additional credit']}
