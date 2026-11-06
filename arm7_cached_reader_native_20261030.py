import hashlib
import random
from pathlib import Path
import match_runtime
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
BASE, DATA, STACK, RETURN = 0x037F8000, 0x023D0000, 0x023E0000, 0x023FF000
TRACK, STREAM, CACHE, FETCH = DATA + 0x100, DATA + 0x1000, 0x03807EC0, 0x03800784
RAW_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    result = []
    for value in range(256):
        for relation in ('hit', 'miss-low', 'miss-high'):
            result.append({'value': value, 'relation': relation, 'offset': value % 16, 'passes': 1})
    for relation in ('empty', 'high-begin', 'at-end', 'before-begin'):
        for offset in range(32):
            result.append({'value': offset, 'relation': relation, 'offset': offset, 'passes': 1})
    result.append({'value': 255, 'relation': 'hit', 'offset': 15, 'passes': 4})
    return result


def subtraction_flags(left, right):
    value = (left - right) & 0xFFFFFFFF
    return ((value >> 31) << 31) | (int(value == 0) << 30) | (int(left >= right) << 29) | (((left ^ right) & (left ^ value)) >> 31 << 28) | 0xD3


def setup(case, seed):
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw) != RAW_SHA:
        raise ValueError('Original cached-reader ARM7 module changed')
    wram = bytearray(0x10000)
    wram[:len(raw)] = raw
    rng = random.Random(20261030 + seed)
    ram = bytearray(rng.randbytes(0x3000))
    current = STREAM + 0x100 + case['offset']
    begin, end = STREAM + 0x100, STREAM + 0x110
    if case['relation'] in ('miss-low', 'before-begin'):
        begin, end = current + 4, current + 20
    elif case['relation'] in ('miss-high', 'at-end'):
        begin, end = current - 16, current
    elif case['relation'] == 'empty':
        begin = end = 0
    elif case['relation'] == 'high-begin':
        begin = end = 0xFFFFFFFF
    wram[CACHE - BASE:CACHE - BASE + 28] = rng.randbytes(28)
    wram[CACHE - BASE + 4:CACHE - BASE + 8] = begin.to_bytes(4, 'little')
    wram[CACHE - BASE + 8:CACHE - BASE + 12] = end.to_bytes(4, 'little')
    ram[current - DATA] = case['value']
    if begin <= current < end:
        wram[CACHE - BASE + 12 + current - begin] = case['value']
        ram[current - DATA] = case['value'] ^ 255
    ram[TRACK - DATA + 0x28:TRACK - DATA + 0x2C] = current.to_bytes(4, 'little')
    return bytes(ram), bytes(wram)


def modeled(ram, wram, stack, registers):
    ram, wram, stack, writes = bytearray(ram), bytearray(wram), bytearray(stack), []
    def put(address, size, value):
        value &= (1 << (size * 8)) - 1
        if STACK <= address < STACK + len(stack):
            target, offset = stack, address - STACK
        elif BASE <= address < BASE + len(wram):
            target, offset = wram, address - BASE
        else:
            target, offset = ram, address - DATA
        target[offset:offset + size] = value.to_bytes(size, 'little')
        writes.append([address, size, value])
    for index, value in enumerate([registers[3], registers[4], registers[5], registers[-1]]):
        put(registers[-2] - 16 + index * 4, 4, value)
    current = int.from_bytes(ram[TRACK - DATA + 0x28:TRACK - DATA + 0x2C], 'little')
    begin = int.from_bytes(wram[CACHE - BASE + 4:CACHE - BASE + 8], 'little')
    end = int.from_bytes(wram[CACHE - BASE + 8:CACHE - BASE + 12], 'little')
    status = subtraction_flags(current, begin if current < begin else end)
    miss = current < begin or current >= end
    if miss:
        begin, end = current & ~3, (current & ~3) + 16
        put(CACHE + 4, 4, begin)
        put(CACHE + 8, 4, end)
        for offset in range(0, 16, 4):
            value = int.from_bytes(ram[begin - DATA + offset:begin - DATA + offset + 4], 'little')
            put(CACHE + 12 + offset, 4, value)
    index = current - begin
    value = wram[CACHE - BASE + 12 + index]
    put(TRACK + 0x28, 4, current + 1)
    expected = list(registers)
    expected[:3] = [value, current + 1, index]
    return bytes(ram), bytes(wram), bytes(stack), writes, expected, status, miss


def execute(entry, body, case, seed, budget=256, invalid=False):
    ram, wram = setup(case, seed)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for first, size in ((BASE, 0x10000), (DATA, 0x3000), (STACK, 0x2000), (RETURN, 0x1000)):
        machine.mem_map(first, size)
    address = int(entry['address'], 0)
    machine.mem_write(BASE, wram)
    machine.mem_write(address, body)
    if invalid:
        ram = bytearray(ram)
        ram[TRACK - DATA + 0x28:TRACK - DATA + 0x2C] = (0x03000000).to_bytes(4, 'little')
        ram = bytes(ram)
    machine.mem_write(DATA, ram)
    rng = random.Random(20261031 + seed)
    stack = rng.randbytes(0x2000)
    machine.mem_write(STACK, stack)
    writes, visited, pending, nested, fetch_arguments = [], set(), [False], [0], []
    def code(cpu, pc, size, unused):
        if not (address <= pc < address + entry['codeBytes'] or FETCH <= pc < FETCH + 56):
            raise ValueError('Cached reader escaped own/qualified fetch code ranges')
        if pc == FETCH:
            if pending[0]:
                raise ValueError('Unexpected nested fetch depth')
            pending[0] = True
            fetch_arguments.append(cpu.reg_read(match_runtime.REGISTERS[0]))
        if pc == 0x038002C0 and pending[0]:
            pending[0] = False
            nested[0] += 1
        visited.add(pc)
    def write(cpu, access, location, size, value, unused):
        writes.append([location, size, value & ((1 << (size * 8)) - 1)])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    states = []
    for phase in range(case['passes']):
        registers = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
        registers[0], registers[-2:] = TRACK, [STACK + 0x1F00, RETURN]
        machine.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
        for register, value in zip(match_runtime.REGISTERS, registers):
            machine.reg_write(register, value)
        first_write, old_nested = len(writes), nested[0]
        old_args = len(fetch_arguments)
        fault = None
        try:
            machine.emu_start(address, RETURN, count=budget, timeout=100000)
        except UcError as error:
            fault = error.errno
        returned = machine.reg_read(UC_ARM_REG_PC) == RETURN
        observed = [machine.reg_read(register) for register in match_runtime.REGISTERS]
        miss = None
        if returned:
            old_current = int.from_bytes(ram[TRACK - DATA + 0x28:TRACK - DATA + 0x2C], 'little')
            ram, wram, stack, expected_writes, expected_regs, expected_status, miss = modeled(ram, wram, stack, registers)
            if observed != expected_regs or machine.reg_read(UC_ARM_REG_CPSR) != expected_status or writes[first_write:] != expected_writes:
                raise ValueError('Independent cache/full-byte/pointer/register/flags/ordered-store model differs')
            if bytes(machine.mem_read(DATA, 0x3000)) != ram or bytes(machine.mem_read(BASE, 0x10000)) != wram or bytes(machine.mem_read(STACK, 0x2000)) != stack:
                raise ValueError('Independent complete cache RAM/BSS/frame model differs')
            if pending[0] or nested[0] - old_nested != int(miss) or fetch_arguments[old_args:] != ([old_current] if miss else []):
                raise ValueError('Real original fetch argument/actual nested return contract differs')
        states.append({'actualReturn': returned, 'fault': fault, 'pc': machine.reg_read(UC_ARM_REG_PC), 'registers': observed,
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'writes': writes[first_write:], 'cacheMiss': miss, 'actualNestedFetchReturns': nested[0] - old_nested,
            'fetchArguments': fetch_arguments[old_args:], 'ramSha256': digest(bytes(machine.mem_read(DATA, 0x3000))),
            'wramAndBssSha256': digest(bytes(machine.mem_read(BASE, 0x10000))), 'stackSha256': digest(bytes(machine.mem_read(STACK, 0x2000)))})
        if not returned:
            break
    return {'states': states, 'visited': sorted(visited)}


def oracle(entry, original, rebuilt):
    records, visited, outer, nested, values = [], set(), 0, 0, set()
    for seed, case in enumerate(cases()):
        expected, actual = execute(entry, original, case, seed), execute(entry, rebuilt, case, seed)
        if expected != actual or any(not row['actualReturn'] or row['fault'] is not None for row in expected['states']):
            raise ValueError('Cached byte-reader original/source complete effects/return differ')
        outer += len(expected['states']) * 2
        nested += sum(row['actualNestedFetchReturns'] for row in expected['states']) * 2
        values.update(row['registers'][0] for row in expected['states'])
        visited.update(expected['visited'])
        records.append({'case': case, 'seed': seed, 'actualOriginalAndCompiledReturns': len(expected['states']) * 2,
            'actualNestedFetchReturns': sum(row['actualNestedFetchReturns'] for row in expected['states']) * 2,
            'cacheMisses': [row['cacheMiss'] for row in expected['states']], 'stateSha256': digest(repr(expected).encode())})
    own = set(range(int(entry['address'], 0), int(entry['address'], 0) + entry['codeBytes'], 4))
    if not own.issubset(visited) or not set(range(FETCH, FETCH + 56, 4)).issubset(visited) or values != set(range(256)):
        raise ValueError('Reader own/fetch instruction or byte-value coverage incomplete')
    controls = []
    for name, options in (('budget-exhaustion', {'budget': 10}), ('unmapped-current', {'invalid': True})):
        expected = execute(entry, original, cases()[1], 0, **options)
        actual = execute(entry, rebuilt, cases()[1], 0, **options)
        if expected != actual or any(row['actualReturn'] for row in expected['states']):
            raise ValueError('Unsupported cache path received return credit')
        controls.append({'name': name, 'returnCredit': 0, 'state': expected})
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records), 'actualOriginalAndCompiledReturns': outer,
        'actualSeparatelyObservedNestedFetchReturns': nested, 'freshMachinePerScenario': True, 'instructionLimit': 256,
        'timeoutMicroseconds': 100000, 'cpuModel': 'Unicorn TI925T ARMv4T surrogate', 'independentByteCachePointerFlagsWholeStateOrderedStoreModel': True,
        'records': records, 'allOwnInstructionAddressesVisited': sorted(own), 'byteReturnCoverage': sorted(values),
        'unsupportedControls': controls, 'unsupportedReturnCredit': 0, 'originalCallee': {'program': '', 'processor': 'arm7', 'module': 'arm7-wram',
            'mode': 'arm', 'address': hex(FETCH), 'instructionBytes': 56, 'generatedLiteralBytes': 4, 'providerReplacement': False, 'sourceCredit': 0},
        'returnContract': 'u8 zero-extended to full R0; not an int sentinel', 'originalDataSourceCredit': 0,
        'limitations': ['Disposable synthetic stream/cache/track contexts; no enclosing sequence validity, physical audio or ownership claim',
            'Malformed extents permitting indexes outside the16-byte cache and aliased track/cache/stream objects remain unsupported',
            'Budget/fault paths have no return/error-result credit; fixed32-bit pointer comparisons need a separate Android address model']}
