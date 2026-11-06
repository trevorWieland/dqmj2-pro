import hashlib
from pathlib import Path
import random
import match_runtime
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_TI925T

ROOT = Path(__file__).resolve().parent
BASE = 0x027E0000
ADDRESS = 0x027F5B10
SIZE = 172
CODE = 164
GET = 0x027E94C8
STEP = 0x027E93D4
TABLE = 0x027F7F74
WORD = 0x0380FFF4
WORK = 0x02240000
RECORD = 0x02242000
OUTPUT = 0x02244000
STACK = 0x02300000
RETURN = 0x02500000
MODULE = 'extract/utility/runtime/utility-child-arm7-main.bin'
MODULE_SHA = 'a5838c09ff9e04d2ffbdf780b3d1bbd5b5875dda9f2ea7d7f8eed74a60d1920a'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def crc_step(value, byte):
    value ^= byte
    for unused in range(8):
        value = value >> 1 ^ (0xA001 if value & 1 else 0)
    return value & 0xFFFF


def crc(data):
    value = 0
    for byte in data:
        value = crc_step(value, byte)
    return value


def verify_table(raw):
    values = []
    for index in range(16):
        value = index
        for unused in range(4):
            value = value >> 1 ^ (0xA001 if value & 1 else 0)
        values.append(value)
    generated = b''.join(value.to_bytes(2, 'little') for value in values)
    if raw[TABLE - BASE:TABLE - BASE + 32] != generated:
        raise ValueError('Original nibble table differs from independent polynomial model')
    return {'address': hex(TABLE), 'bytes': 32, 'sha256': digest(generated), 'polynomial': '0xa001',
        'generatedFromFourBitRecurrence': True, 'sourceDataCredit': 0}


def cases():
    return [{'length': length, 'output': output, 'storedDifference': difference, 'pattern': pattern}
        for length in (0, 0xA3, 0xA4, 0xA5, 0x1D5, 0x1D6, 0x1D7, 0xFFFF)
        for output in (False, True) for difference in (0, 0x8001) for pattern in ('zero', 'ones', 'linear', 'random')]


def execute(body, case, seed, budget=100000, null_record=False):
    raw = (ROOT / MODULE).read_bytes()
    if digest(raw) != MODULE_SHA or len(body) != SIZE:
        raise ValueError('Qualified record caller/module extent changed')
    verify_table(raw)
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(BASE, 0x20000)
    cpu.mem_write(BASE, raw)
    cpu.mem_write(ADDRESS, body)
    cpu.mem_map(WORD & ~0xFFF, 0x1000)
    cpu.mem_write(WORD, WORK.to_bytes(4, 'little'))
    for address in (WORK, RECORD, OUTPUT):
        cpu.mem_map(address, 0x1000)
    cpu.mem_map(STACK, 0x4000)
    rng = random.Random(20261031 + seed)
    work, output, stack = bytearray(rng.randbytes(0x1000)), bytearray(rng.randbytes(0x1000)), rng.randbytes(0x4000)
    work[0x318:0x31C] = (0 if null_record else RECORD).to_bytes(4, 'little')
    pattern = case['pattern']
    record = bytearray(bytes(0x1000) if pattern == 'zero' else bytes([255]) * 0x1000 if pattern == 'ones'
        else bytes((index * 37 + seed) & 255 for index in range(0x1000)) if pattern == 'linear' else rng.randbytes(0x1000))
    length = case['length']
    record[2:4] = length.to_bytes(2, 'little')
    supported = 0xA4 <= length <= 0x1D6
    calculated = crc(record[2:2 + length]) if supported else 0
    stored = calculated ^ case['storedDifference']
    record[:2] = stored.to_bytes(2, 'little')
    for address, data in ((WORK, work), (RECORD, record), (OUTPUT, output), (STACK, stack)):
        cpu.mem_write(address, bytes(data))
    initial = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
    initial[0], initial[-2:] = OUTPUT if case['output'] else 0, [STACK + 0x3F00, RETURN]
    cpu.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
    for register, value in zip(match_runtime.REGISTERS, initial):
        cpu.reg_write(register, value)
    visited, writes, frames, reads, steps = set(), [], [], [], []

    def code(machine, pc, size, unused):
        if frames and pc == frames[-1]['return']:
            frame = frames.pop()
            value = machine.reg_read(match_runtime.REGISTERS[0])
            saved = [machine.reg_read(register) for register in match_runtime.REGISTERS[4:12]]
            if saved != frame['saved']:
                raise ValueError('Original primitive changed callee-saved state')
            if frame['entry'] == GET:
                offset = frame['arg0'] - RECORD
                if not 2 <= offset < 2 + length or value != record[offset]:
                    raise ValueError('Original halfword-backed byte getter argument/result differs')
                reads.append([frame['arg0'], value])
            else:
                if value != crc_step(frame['arg1'], frame['arg0']):
                    raise ValueError('Independent bit-polynomial CRC step differs')
                steps.append([frame['arg0'], frame['arg1'], value])
        if pc in (GET, STEP):
            first, second = [machine.reg_read(register) for register in match_runtime.REGISTERS[:2]]
            if frames or pc == STEP and (first > 255 or second > 0xFFFF):
                raise ValueError('Caller primitive ABI input/stack differs')
            frames.append({'entry': pc, 'return': machine.reg_read(match_runtime.REGISTERS[-1]), 'arg0': first, 'arg1': second,
                'saved': [machine.reg_read(register) for register in match_runtime.REGISTERS[4:12]]})
        if not (ADDRESS <= pc < ADDRESS + CODE or GET <= pc < GET + 32 or STEP <= pc < STEP + 112):
            raise ValueError('Record execution escaped the full own/original primitive code scope')
        visited.add(pc)

    def write(machine, access, location, size, value, unused):
        if STACK <= location < STACK + 0x4000:
            if not initial[-2] - 0x100 <= location < initial[-2]:
                raise ValueError('Primitive/caller stack write escaped its bounded frame')
            return
        writes.append([location, size, value & ((1 << (size * 8)) - 1)])

    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    fault = None
    try:
        cpu.emu_start(ADDRESS, RETURN, count=budget, timeout=2000000)
    except UcError as error:
        fault = error.errno
    observed = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
    returned = cpu.reg_read(UC_ARM_REG_PC) == RETURN
    if returned:
        wanted = 2 if not supported else int(calculated != stored)
        predicted_output = bytearray(output)
        predicted_writes = []
        if supported and case['output']:
            packed = stored | calculated << 16
            predicted_output[:4] = packed.to_bytes(4, 'little')
            predicted_writes.append([OUTPUT, 4, packed])
        expected_count = length if supported else 0
        if fault is not None or observed[0] != wanted or frames or len(reads) != expected_count or len(steps) != expected_count:
            raise ValueError('Actual return/primitive-count/header comparison model differs')
        if writes != predicted_writes or bytes(cpu.mem_read(OUTPUT, 0x1000)) != bytes(predicted_output):
            raise ValueError('Optional full-word output/guard model differs')
        if bytes(cpu.mem_read(WORK, 0x1000)) != bytes(work) or bytes(cpu.mem_read(RECORD, 0x1000)) != bytes(record) or bytes(cpu.mem_read(WORD, 4)) != WORK.to_bytes(4, 'little'):
            raise ValueError('Read-only descriptor/header/runtime-word state changed')
        if observed[4:12] != initial[4:12] or observed[-2:] != initial[-2:]:
            raise ValueError('Record caller preserved-register/stack ABI differs')
    return {'actualReturn': returned, 'fault': fault, 'pc': cpu.reg_read(UC_ARM_REG_PC), 'registers': observed,
        'cpsr': cpu.reg_read(UC_ARM_REG_CPSR), 'writes': writes, 'visited': sorted(visited),
        'actualNativeByteGetterReturns': len(reads), 'actualNativeCrcStepReturns': len(steps),
        'nativeGetterTraceSha256': digest(repr(reads).encode()), 'nativeCrcTraceSha256': digest(repr(steps).encode()),
        'calculatedRaw16': calculated, 'storedRaw16': stored, 'outputSha256': digest(bytes(cpu.mem_read(OUTPUT, 0x1000))),
        'workSha256': digest(bytes(cpu.mem_read(WORK, 0x1000))), 'recordSha256': digest(bytes(cpu.mem_read(RECORD, 0x1000))),
        'stackSha256': digest(bytes(cpu.mem_read(STACK, 0x4000)))}


def oracle(original, rebuilt):
    records, visited, getter_returns, step_returns = [], set(), 0, 0
    for seed, case in enumerate(cases()):
        first, second = execute(original, case, seed), execute(rebuilt, case, seed)
        if first != second or not first['actualReturn']:
            raise ValueError('Original/fresh complete C record caller differed or failed return')
        visited.update(first['visited'])
        getter_returns += first['actualNativeByteGetterReturns'] * 2
        step_returns += first['actualNativeCrcStepReturns'] * 2
        records.append({'case': case, 'seed': seed, 'stateSha256': digest(repr(first).encode()),
            'rawResult': first['registers'][0], 'rawStored16': first['storedRaw16'], 'rawCalculated16': first['calculatedRaw16'],
            'actualOriginalAndCompiledReturns': 2, 'actualSeparatelyObservedByteGetterReturns': first['actualNativeByteGetterReturns'] * 2,
            'actualSeparatelyObservedCrcStepReturns': first['actualNativeCrcStepReturns'] * 2})
    own = set(range(ADDRESS, ADDRESS + CODE, 4))
    if not own.issubset(visited):
        raise ValueError('Full record caller own instruction traversal incomplete')
    unsupported = []
    case = dict(cases()[0], length=0xA4)
    for name, options in (('one-instruction-budget', {'budget': 1}), ('null-record-pointer', {'null_record': True})):
        first, second = execute(original, case, 0, **options), execute(rebuilt, case, 0, **options)
        if first != second or first['actualReturn']:
            raise ValueError('Unsupported raw context received normal-return credit')
        unsupported.append({'name': name, 'state': first, 'returnCredit': 0, 'supportedErrorPathCredit': 0})
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records), 'actualOriginalAndCompiledReturns': len(records) * 2,
        'actualSeparatelyObservedByteGetterReturns': getter_returns, 'actualSeparatelyObservedCrcStepReturns': step_returns,
        'freshMachinePerExecution': True, 'providerReplacements': [], 'cpuModel': 'Unicorn TI925T ARMv4T surrogate',
        'instructionLimit': 100000, 'timeoutMicroseconds': 2000000, 'allOwnInstructionAddressesVisited': sorted(own),
        'actualOriginalPrimitiveInstructionAddressesVisited': sorted(visited - own), 'records': records,
        'unsupportedControls': unsupported, 'unsupportedReturnCredit': 0, 'calleeOrTableDataSourceCredit': 0,
        'rawRecordContract': 'Descriptor+318 points to record; countu16 at+2, inclusiveA4..1D6; process count bytes beginning+2; compare stored16 at+0; optional pack stored|(computed<<16); results0/1/2 measured only',
        'limitations': ['Synthetic descriptor/record/output contexts do not establish native scene reachability, file/save/bank meanings or physical-device behavior',
            'Global0380FFF4 is a qualified absolute incoming-descriptor pointer word with no module BSS or original-data credit',
            'Original byte/CRC routines and polynomial table remain zero-credit native dependencies']}
