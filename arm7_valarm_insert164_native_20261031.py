import gzip
import hashlib
import json
from pathlib import Path
import random
import arm7_lane_alarm_registration_native_20261031 as fixture
from unicorn import UC_HOOK_CODE

ROOT = Path(__file__).resolve().parent
ADDRESS, SIZE, CODE = 0x037FD7A8, 164, 160
WORK = ROOT / 'work/arm7-bulk-20261030/lane-host-valarm-insert164-final'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    return [{'key': key, 'scan': scan, 'nodes': nodes}
        for key in (0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF)
        for scan in (0, 1, 127, 255, 256, 511, 32767, -1, -32768)
        for nodes in ([], [(0, 0)], [(0xFFFFFFFF, -32768)], [(0, 0), (1, 255), (1, 511)])]


def execute(body, case, seed, budget=20000):
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    machine = fixture.setup(fixture.ADDRESS, raw[0x65C0:0x65C0 + 156],
        {'tick': True, 'alarm': True, 'enabled': 0, 'counter': 0, 'timer': 0, 'request': 0, 'passes': 1}, seed)
    if not machine['invoke'](0x037FD74C)['actualReturn']:
        raise ValueError('Original vertical-alarm initialization did not return')
    cpu = machine['cpu']
    cpu.mem_write(ADDRESS, body)
    record = fixture.DATA + 0x200
    nodes = [(fixture.DATA + 0x400 + index * 64, key, scan) for index, (key, scan) in enumerate(case['nodes'])]
    for address, key, scan in [(record, case['key'], case['scan']), *nodes]:
        data = bytearray(random.Random(address + seed).randbytes(64))
        data[12:16] = key.to_bytes(4, 'little')
        data[16:18] = (scan & 0xFFFF).to_bytes(2, 'little')
        cpu.mem_write(address, bytes(data))
    for index, (address, key, scan) in enumerate(nodes):
        cpu.mem_write(address + 20, (nodes[index - 1][0] if index else 0).to_bytes(4, 'little'))
        cpu.mem_write(address + 24, (nodes[index + 1][0] if index + 1 < len(nodes) else 0).to_bytes(4, 'little'))
    cpu.mem_write(0x038078C0, (nodes[0][0] if nodes else 0).to_bytes(4, 'little'))
    cpu.mem_write(0x038078C4, (nodes[-1][0] if nodes else 0).to_bytes(4, 'little'))
    disp = [0, 0xFFFF, 0xA55A, 0x5AA5][seed % 4]
    ie = [0, 4, 8, 0xFFFFFFFF][seed % 4]
    ime = [0, 1, 0xFFFF][seed % 3]
    cpu.mem_write(fixture.IO + 4, disp.to_bytes(2, 'little'))
    cpu.mem_write(fixture.IO + 0x210, ie.to_bytes(4, 'little'))
    cpu.mem_write(fixture.IO + 0x208, ime.to_bytes(2, 'little'))
    expected = fixture.engine.snapshot(machine)
    stores = []

    def put(address, width, value):
        for base, data in expected.items():
            if base <= address and address + width <= base + len(data):
                data[address - base:address - base + width] = value.to_bytes(width, 'little')
                stores.append([address, width, value])
                return
        raise ValueError('Independent signed-key insertion model escaped backing')

    index = next((index for index, (address, key, scan) in enumerate(nodes) if (key, scan) > (case['key'], case['scan'])), len(nodes))
    previous = nodes[index - 1][0] if index else 0
    following = nodes[index][0] if index < len(nodes) else 0
    put(record + 20, 4, previous)
    put(record + 24, 4, following)
    if following:
        put(following + 20, 4, record)
        if previous:
            put(previous + 24, 4, record)
        else:
            put(0x038078C0, 4, record)
    else:
        put(0x038078C4, 4, record)
        if previous:
            put(previous + 24, 4, record)
        else:
            put(0x038078C0, 4, record)
    if not previous:
        control = (disp & 0x3F) | ((case['scan'] & 0xFF) << 8) | ((case['scan'] & 0x100) >> 1)
        put(0x0380756C, 4, 0x037FDAF8)
        put(fixture.IO + 4, 2, control)
        put(fixture.IO + 4, 2, control | 0x20)
        put(fixture.IO + 0x208, 2, 0)
        put(fixture.IO + 0x210, 4, ie | 4)
        put(fixture.IO + 0x208, 2, ime)
    visited = []
    cpu.hook_add(UC_HOOK_CODE, lambda machine, pc, width, unused: visited.append(pc))
    result = machine['invoke'](ADDRESS, [record], True, budget)
    if not result['actualReturn']:
        return {'actualReturn': False, 'execution': result, 'postFaultOrBoundaryStateExcluded': True}
    checked = fixture.engine.result(machine, result, expected, None, stores)
    if checked['orderedNonstackWrites'] != stores:
        raise ValueError('Independent original vertical-alarm insertion store order differs')
    return {'actualReturn': True, 'case': case, 'insertedIndex': index, 'previous': previous, 'following': following,
        'dispstatBefore': disp, 'ieBefore': ie, 'imeBefore': ime, 'execution': checked,
        'ownVisited': sorted({pc for pc in visited if ADDRESS <= pc < ADDRESS + CODE}),
        'separatelyObservedNativeProgrammerReturns': machine['helperReturns'].get(0x037FD9B8, 0)}


def oracle(body):
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    original = raw[ADDRESS - 0x037F8000:ADDRESS - 0x037F8000 + SIZE]
    if body != original:
        raise ValueError('Complete ordinary C insertion must genuinely link every native byte')
    records, visited, nested = [], set(), 0
    for index, case in enumerate(cases()):
        native, compiled = execute(original, case, index), execute(body, case, index)
        if native != compiled or not native['actualReturn']:
            raise ValueError('Original/new signed-halfword-key insertion effects/return differ')
        records.append(native)
        visited.update(native['ownVisited'])
        nested += 2 * native['separatelyObservedNativeProgrammerReturns']
    if visited != set(range(ADDRESS, ADDRESS + CODE, 4)):
        raise ValueError('Native/source corpus missed own insertion instructions')
    cap = execute(original, cases()[0], 91, budget=1)
    if cap['actualReturn']:
        raise ValueError('Bound exhaustion gained ordinary C return credit')
    WORK.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(records, sort_keys=True, separators=(',', ':')) + '\n').encode()
    path = WORK / 'supported-native-records.json.gz'
    path.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
    return {'vectors': len(records), 'actualOriginalAndCompiledReturns': len(records) * 2,
        'actualSeparatelyObservedProgrammerReturns': nested, 'allOwnInstructionsVisited': True,
        'ownInstructionAddresses': sorted(visited), 'providerReplacements': [],
        'independentFullMemoryAndOrderedStoreModel': True, 'fullRegistersFlagsStackCompared': True,
        'trace': {'path': path.relative_to(ROOT).as_posix(), 'compressedSha256': digest(path.read_bytes()), 'rawSha256': digest(data), 'rawBytes': len(data), 'compressedBytes': path.stat().st_size, 'gzipMtime': 0},
        'unsupportedControls': [cap], 'unsupportedReturnCredit': 0, 'originalHelperAndDataSourceCredit': 0,
        'limitations': ['Raw unsigned32 and signed16 keys are measured; source frame/scan names do not establish game chronology or valid hardware positions',
            'Original native prerequisites, setter, handler-table write and IRQ helpers execute; no asynchronous callback or device claim',
            'The uniquely named28-byte node and20-byte queue views are minimum measured extents; full original allocations are unproved',
            'Finite synthetic intrusive lists and opaque guard bytes are checked; malformed/cyclic pointers and enclosing call reachability are unsupported']}
