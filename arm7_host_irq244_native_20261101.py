import gzip
import json
from pathlib import Path
import arm7_host_irq244_engine_20261101 as engine

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/lane-host-irq244-final'
SIZES = {0x037FB8A4: 52, 0x037FB8D8: 24, 0x037FB8F0: 56, 0x037FB928: 60, 0x037FB964: 52}
CODES = {address: size - 4 for address, size in SIZES.items()}


def cases(address):
    return [{'entry': address, 'mask': mask, 'oldMask': old, 'master': master}
        for mask in (0, 1, 8, 16, 0xFFFFFF, 0x1000000, 0x80000000, 0xFFFFFFFF, 0x55555555, 0xAAAAAAAA)
        for old in (0, 1, 0x80000000, 0xFFFFFFFF) for master in (0, 1, 2, 0x8000, 0xFFFF)]


def execute(bodies, case, seed, budget=100000):
    machine = engine.setup(bodies, seed)
    cpu = machine['cpu']
    cpu.mem_write(0x04000208, case['master'].to_bytes(2, 'little'))
    cpu.mem_write(0x04000210, case['oldMask'].to_bytes(4, 'little'))
    old_flags = case['oldMask'] ^ 0xA5A5A5A5
    cpu.mem_write(0x04000214, old_flags.to_bytes(4, 'little'))
    memory = machine['snapshot']()
    address, old, mask = case['entry'], case['oldMask'], case['mask']
    if address == 0x037FB8D8:
        result_word = case['master']
        stores, reads = [[0x04000208, 2, 0]], [[0x04000208, 2]]
        arguments = []
    else:
        register = 0x04000214 if address == 0x037FB964 else 0x04000210
        result_word = old_flags if address == 0x037FB964 else old
        value = old & (~mask & 0xFFFFFFFF) if address == 0x037FB928 else old | mask if address == 0x037FB8F0 else mask
        stores = [[0x04000208, 2, 0], [register, 4, value], [0x04000208, 2, case['master']]]
        reads, arguments = [[0x04000208, 2], [register, 4], [0x04000208, 2]], [mask]
    for location, width, value in stores:
        memory[engine.IO][location-engine.IO:location-engine.IO+width] = value.to_bytes(width, 'little')
    result = machine['invoke'](address, arguments, budget)
    if not result['actualReturn']:
        return {'actualReturn': False, 'case': case, 'execution': result, 'returnCredit': 0}
    actual = [item for item in result['writes'] if not engine.STACK <= item[0] < engine.STACK + 0x4000]
    io_reads = [item for item in result['reads'] if engine.IO <= item[0] < engine.IO + 0x1000]
    if actual != stores or io_reads != reads or result['registers'][0] != result_word:
        raise ValueError('Independent host IRQ full-word return/IME/IE/IF ordered access model differs')
    expected_cpsr = seed % 16 << 28 | (0x53 if seed & 1 else 0xD3)
    if result['cpsr'] != expected_cpsr:
        raise ValueError('Host IRQ utility changed incoming flags/processor mode')
    if any(bytes(cpu.mem_read(base, len(data))) != bytes(data) for base, data in memory.items()):
        raise ValueError('Complete mapped memory and unrelated register shadow preservation model differs')
    return {'actualReturn': True, 'case': case, 'expectedReturnWord': result_word, 'expectedOrderedWrites': stores,
        'expectedReads': reads, 'execution': result, 'providerReplacements': [], 'physicalHardwareStateInferred': False}


def oracle(bodies):
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    originals = {address: raw[address-engine.BASE:address-engine.BASE+size] for address, size in SIZES.items()}
    if bodies != originals:
        raise ValueError('All five complete fresh host C units must match native bytes')
    records, result = [], {}
    for address in SIZES:
        visited, flags, nested = set(), set(), 0
        for index, case in enumerate(cases(address)):
            native, compiled = execute({}, case, index), execute(bodies, case, index)
            if native != compiled or not native['actualReturn']:
                raise ValueError('Fresh original/five-unit source execution did not return/equal')
            records.append(native)
            visited.update(pc for pc in native['execution']['visited'] if address <= pc < address + CODES[address])
            flags.add(native['execution']['cpsr'] >> 28)
            nested += 2 * sum(item['entry'] == '0x37fb8d8' for item in native['execution']['nestedReturns'])
        cap = execute({}, cases(address)[0], 0, 1)
        if cap['actualReturn']:
            raise ValueError('Exhausted host IRQ prefix acquired normal return credit')
        result[address] = {'vectors': len(cases(address)), 'actualOriginalAndCompiledReturns': 2*len(cases(address)),
            'actualNestedFreshSourceMasterDisableReturnsSeparate': nested,
            'instructionCoverage': {'visited': sorted(visited), 'unvisited': sorted(set(range(address,address+CODES[address],4))-visited)},
            'allSixteenIncomingFlagStatesPreserved': flags == set(range(16)),
            'allRawRegistersFlagsAndStackCompared': True, 'independentFullMemoryAndExactIoModel': True,
            'unsupportedControls': [cap], 'unsupportedReturnCredit': 0, 'providerReplacements': [],
            'limitations': ['Synthetic synchronous CPU/MMIO-shadow context only, no physical timing/interrupt/concurrency proof',
                'REG_IF writes are measured raw bus payloads; mapped-memory shadow is not physical write-one-to-clear emulation',
                'Native full-word return and16-bit IME preservation are measured; no BOOL/status or interrupt legality interpretation']}
    data = (json.dumps(records, sort_keys=True, separators=(',', ':'))+'\n').encode()
    path = WORK / 'supported-native-records.json.gz'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(gzip.compress(data,compresslevel=9,mtime=0))
    trace = {'path': path.relative_to(ROOT).as_posix(), 'rawSha256': engine.digest(data),
        'compressedSha256': engine.digest(path.read_bytes()),'rawBytes':len(data),'compressedBytes':path.stat().st_size,'gzipMtime':0}
    for item in result.values():
        item['trace'] = trace
    return result
