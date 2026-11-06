import gzip
import json
import random
from pathlib import Path
import arm7_host_irq244_engine_20261101 as engine

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/lane-host-timer-callback76-final'
ENTRY, ENABLE = 0x037FB858, 0x037FB8F0


def cases():
    return [{'index': index, 'functionBits': function, 'argumentBits': argument, 'mask': mask, 'master': master}
        for index in range(4) for function in (0, 0x037FD1B4, 0x037FD1B5, 0xFFFFFFFF)
        for argument in (0, engine.DATA + 0x200, 0x12345678, 0x80000000, 0xFFFFFFFF)
        for mask in (0, 0x80000000, 0xFFFFFFFF) for master in (0, 1, 0xFFFF)]


def execute(bodies, case, seed, budget=100000, native_only=False):
    machine = engine.setup(bodies, seed)
    cpu = machine['cpu']
    first, size = 0x03807680 - 16, 9 * 12 + 32
    cpu.mem_write(first, random.Random(seed + 301).randbytes(size))
    cpu.mem_write(0x04000208, case['master'].to_bytes(2, 'little'))
    cpu.mem_write(0x04000210, case['mask'].to_bytes(4, 'little'))
    memory = machine['snapshot']()
    offset = (case['index'] * 12) & 0xFFFFFFFF
    target = (0x038076B0 + offset) & 0xFFFFFFFF
    shift = (case['index'] + 3) & 0xFF
    bit = (1 << shift) & 0xFFFFFFFF if shift < 32 else 0
    stores = [[target, 4, case['functionBits']], [(target + 8) & 0xFFFFFFFF, 4, case['argumentBits']],
        [0x04000208, 2, 0], [0x04000210, 4, case['mask'] | bit], [0x04000208, 2, case['master']],
        [(target + 4) & 0xFFFFFFFF, 4, 1]]
    for address, width, value in stores:
        for base, data in memory.items():
            if base <= address and address + width <= base + len(data):
                data[address - base:address - base + width] = value.to_bytes(width, 'little')
                break
        else:
            raise ValueError('Callback model escaped qualified mapped backing')
    result = machine['invoke'](ENTRY, [case['index'], case['functionBits'], case['argumentBits']], budget)
    if not result['actualReturn']:
        return {'actualReturn': False, 'case': case, 'execution': result, 'sourceReturnCredit': 0}
    actual = [row for row in result['writes'] if not engine.STACK <= row[0] < engine.STACK + 0x4000]
    reads = [row for row in result['reads'] if engine.IO <= row[0] < engine.IO + 0x1000]
    if actual != stores or reads != [[0x04000208, 2], [0x04000210, 4], [0x04000208, 2]] or result['registers'][0] != 0x038076B4:
        raise ValueError('Independent callback-record/stride/IRQ-order/raw-R0 model differs')
    if any(bytes(cpu.mem_read(base, len(data))) != bytes(data) for base, data in memory.items()):
        raise ValueError('Complete callback/neighbor/guard/mapped-memory model differs')
    return {'actualReturn': True, 'case': case, 'selectedRecord': hex(target), 'expectedOrderedStores': stores,
        'execution': result, 'callbacksInvoked': False, 'originalOnlyOutOfContract': native_only,
        'sourceReturnCredit': 0 if native_only else 1, 'providerReplacements': []}


def oracle(body, enable_body):
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    originals = {ENTRY: raw[ENTRY - engine.BASE:ENTRY - engine.BASE + 76], ENABLE: raw[ENABLE - engine.BASE:ENABLE - engine.BASE + 56]}
    bodies = {ENTRY: body, ENABLE: enable_body}
    if bodies != originals:
        raise ValueError('Callback writer and freshly source-linked enable helper must fully match current bytes')
    records, visited, helper_returns = [], set(), 0
    for seed, case in enumerate(cases()):
        native, compiled = execute(originals, case, seed), execute(bodies, case, seed)
        if native != compiled or not native['actualReturn']:
            raise ValueError('Original/source callback writer did not actually return/equal: ' + str(native))
        records.append(native)
        visited.update(pc for pc in native['execution']['visited'] if ENTRY <= pc < ENTRY + 64)
        helper_returns += 2 * sum(int(row['entry'], 0) == ENABLE for row in native['execution']['nestedReturns'])
    outside = [execute(originals, {'index': index, 'functionBits': 0x037FD1B4, 'argumentBits': 0x12345678,
        'mask': 0, 'master': 1}, 1000 + i, native_only=True) for i, index in enumerate((4, 0xFFFFFFFF, 0x80000000))]
    cap = execute(originals, cases()[0], 11, budget=1)
    if cap['actualReturn'] or any(row['sourceReturnCredit'] for row in outside):
        raise ValueError('Cap or native-only out-of-contract run obtained defined-C credit')
    data = (json.dumps(records, sort_keys=True, separators=(',', ':')) + '\n').encode()
    path = WORK / 'supported-native-records.json.gz'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
    return {'vectors': len(records), 'actualOriginalAndCompiledReturns': len(records) * 2,
        'actualFreshSourceLinkedEnableReturnsSeparate': helper_returns, 'definedCIndexDomain': [0, 3],
        'independentFullMemoryAndExactOrderedIORecordModel': True, 'allRawRegistersFlagsAndStackCompared': True,
        'instructionCoverage': {'visited': sorted(visited), 'unvisited': sorted(set(range(ENTRY, ENTRY + 64, 4)) - visited)},
        'trace': {'path': path.relative_to(ROOT).as_posix(), 'compressedSha256': engine.digest(path.read_bytes()),
            'rawSha256': engine.digest(data), 'rawBytes': len(data), 'compressedBytes': path.stat().st_size, 'gzipMtime': 0},
        'nativeOnlyOutOfContract': outside, 'outOfContractCSourceCredit': 0, 'oneInstructionCap': cap, 'unsupportedReturnCredit': 0,
        'callbackBodyOrDataSourceCredit': 0, 'providerReplacements': [],
        'limitations': ['Only timer indexes0..3 are paired as supported defined-C inputs; no original validation guard is invented',
            'Original-only index4/FFFFFFFF/80000000 behavior is recorded separately and grants no C portability or source-return credit',
            'Callback and argument are raw32-bit stored words, never invoked or dereferenced; no callback ABI/meaning claim',
            'Incomplete extern array is a measured minimum timer subview of the full callback table, not an original allocation/array-extent assertion',
            'Synthetic loader BSS/MMIO context proves no physical interrupts, boot/scene reachability, concurrency or Android equivalence']}
