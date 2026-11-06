import gzip
import json
from pathlib import Path
import arm7_child_alarm_engine_20261031 as engine

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/lane-child-irq-mask168-final'
SIZES = {0x037FBC50: 60, 0x037FBC8C: 56, 0x037FBCC4: 52}
CODES = {address: size - 8 for address, size in SIZES.items()}


def cases():
    return [{'entry': entry, 'mask': mask, 'oldMask': old, 'master': master}
        for entry in SIZES for mask in (0, 1, 8, 16, 0xFFFFFF, 0x1000000, 0x80000000, 0xFFFFFFFF, 0x55555555, 0xAAAAAAAA)
        for old in (0, 1, 8, 0x1000000, 0x80000000, 0xFFFFFFFF, 0x1234567, 0xAAAAAAAA)
        for master in (0, 1, 2, 0x8000, 0xFFFF)]


def execute(bodies, case, seed, budget=100000):
    machine = engine.setup(bodies, seed)
    cpu = machine['cpu']
    cpu.mem_write(0x04000208, case['master'].to_bytes(2, 'little'))
    cpu.mem_write(0x04000210, case['oldMask'].to_bytes(4, 'little'))
    expected = machine['snapshot']()
    old, mask = case['oldMask'], case['mask']
    value = old & (~mask & 0xFFFFFFFF) if case['entry'] == 0x037FBC50 else old | mask if case['entry'] == 0x037FBC8C else mask
    expected[engine.IO][0x210:0x214] = value.to_bytes(4, 'little')
    result = machine['invoke'](case['entry'], [mask], budget)
    if not result['actualReturn']:
        return {'actualReturn': False, 'case': case, 'execution': result, 'returnCredit': 0}
    stores = [[0x04000208, 2, 0], [0x04000210, 4, value], [0x04000208, 2, case['master']]]
    reads = [[0x04000208, 2], [0x04000210, 4], [0x04000208, 2]]
    actual_stores = [row for row in result['writes'] if not engine.STACK <= row[0] < engine.STACK + 0x4000]
    actual_reads = [row for row in result['reads'] if engine.IO <= row[0] < engine.IO + 0x1000]
    flags = seed % 16 << 28 | (0x53 if seed & 1 else 0xD3)
    if result['registers'][0] != old or result['cpsr'] != flags or actual_stores != stores or actual_reads != reads:
        raise ValueError('Independent unsigned mask/old-value/IME readback/flags/I-O ordering model differs')
    if any(bytes(cpu.mem_read(base, len(data))) != bytes(data) for base, data in expected.items()):
        raise ValueError('Independent complete mapped-memory preservation model differs')
    return {'actualReturn': True, 'case': case, 'expectedReturn': old, 'expectedMask': value,
        'expectedOrderedIOStores': stores, 'expectedOrderedIOReads': reads, 'execution': result,
        'providerReplacements': [], 'physicalHardwareClaim': False}


def oracle(bodies):
    raw = (ROOT / 'extract/utility/runtime/utility-child-arm7-wram.bin').read_bytes()
    originals = {address: raw[address - engine.BASE:address - engine.BASE + size] for address, size in SIZES.items()}
    if set(bodies) != set(SIZES) or any(bodies[address] != originals[address] for address in bodies):
        raise ValueError('Complete three-source IRQ unit outputs do not genuinely match current native bytes')
    records, counts, visited = [], {address: 0 for address in bodies}, {address: set() for address in bodies}
    for index, case in enumerate(cases()):
        native, compiled = execute(originals, case, index), execute(bodies, case, index)
        if native != compiled or not native['actualReturn']:
            raise ValueError('Original/fresh-C IRQ helpers did not return/equal: ' + str(native))
        records.append(native)
        counts[case['entry']] += 2
        for address, size in CODES.items():
            visited[address].update(pc for pc in native['execution']['visited'] if address <= pc < address + size)
    caps = [execute(originals, next(case for case in cases() if case['entry'] == address), 71 + index, 1) for index, address in enumerate(SIZES)]
    if any(row['actualReturn'] for row in caps):
        raise ValueError('IRQ helper cap acquired return credit')
    data = (json.dumps(records, sort_keys=True, separators=(',', ':')) + '\n').encode()
    path = WORK / 'supported-native-records.json.gz'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
    return {'vectors': len(records), 'actualReturnCountsByEntry': {hex(key): value for key, value in counts.items()},
        'freshOriginalAndThreeCompiledCExecutions': True, 'allOwnFlagsPreserved': True,
        'independentFullMemoryExactOrderedIOReadAndStoreModel': True, 'allRawRegistersFlagsAndStackCompared': True,
        'providerReplacements': [], 'originalDependencyOrDataSourceCredit': 0,
        'ownInstructionCoverage': {hex(address): {'visited': sorted(visited[address]),
            'unvisited': sorted(set(range(address, address + CODES[address], 4)) - visited[address])} for address in bodies},
        'trace': {'path': path.relative_to(ROOT).as_posix(), 'compressedSha256': engine.digest(path.read_bytes()),
            'rawSha256': engine.digest(data), 'rawBytes': len(data), 'compressedBytes': path.stat().st_size, 'gzipMtime': 0},
        'unsupportedControls': caps, 'unsupportedReturnCredit': 0,
        'limitations': ['Actual code executes against isolated synthetic MMIO backing; no physical interrupts or hardware synchronization claim',
            'Full input words and raw16-bit IME values are measured, including values outside ordinary hardware bit meaning',
            'The unused volatile IME readback is retained and its access order independently checked',
            'No new data extent, assembly provenance, original SDK version, boot/scene or native Android claim']}
