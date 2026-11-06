import hashlib
import random
from pathlib import Path
import match_runtime
import arm7_seq_neighbor_model_20261030 as memory
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_PC, UC_ARM_REG_CPSR

ROOT = Path(__file__).resolve().parent
ADDRESS, CODE = 0x037FFEB8, 52
RAW_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases(address=None):
    lengths, addresses = (0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, 0x12345678), (memory.DATA + 0x100, memory.DATA + 0xFF0)
    result = [{'flags': flags, 'length': lengths[flags % len(lengths)], 'channel': addresses[flags % 2], 'passes': 1} for flags in range(256)]
    result.extend({'flags': flags, 'length': length, 'channel': channel, 'passes': 1}
        for flags in (0, 1, 2, 255) for length in lengths for channel in addresses)
    result.append({'flags': 255, 'length': 0xFFFFFFFF, 'channel': addresses[1], 'passes': 2})
    return result


def setup(case, seed):
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw) != RAW_SHA:
        raise ValueError('Original initializer module differs')
    rng = random.Random(20261030 + seed)
    ram, wram = rng.randbytes(0x4000), bytearray(rng.randbytes(0x14000))
    wram[:len(raw)] = raw
    state = memory.Model(ram, wram)
    state.put(case['channel'] + 3, 1, case['flags'])
    return bytes(state.regions[memory.DATA]), bytes(state.regions[memory.BASE])


def modeled(ram, wram, case):
    state = memory.Model(ram, wram)
    channel = case['channel']
    flags = state.get(channel + 3, 1)
    for offset, size, value in ((0x10, 4, 0xFFFE9680), (2, 1, 0), (0x34, 4, case['length']),
            (0x30, 2, 0), (0x2E, 2, 0), (3, 1, flags | 3)):
        state.put(channel + offset, size, value)
    return bytes(state.regions[memory.DATA]), bytes(state.regions[memory.BASE]), state.writes, flags


def execute(entry, body, case, seed, budget=10000):
    ram, wram = setup(case, seed)
    mutable = bytearray(wram)
    mutable[ADDRESS - memory.BASE:ADDRESS - memory.BASE + len(body)] = body
    wram = bytes(mutable)
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base, size in ((memory.BASE, 0x14000), (memory.DATA, 0x4000), (memory.STACK, 0x4000), (memory.RETURN, 0x1000)):
        cpu.mem_map(base, size)
    cpu.mem_write(memory.BASE, wram)
    cpu.mem_write(memory.DATA, ram)
    cpu.mem_write(ADDRESS, body)
    cpu.mem_write(memory.STACK, random.Random(20261031 + seed).randbytes(0x4000))
    writes, visited = [], set()
    def code(machine, pc, size, unused):
        if not ADDRESS <= pc < ADDRESS + CODE:
            raise ValueError('Initializer escaped complete own instruction range')
        visited.add(pc)
    def write(machine, access, location, size, value, unused):
        if not memory.STACK <= location < memory.STACK + 0x4000:
            writes.append([location, size, value & ((1 << (size * 8)) - 1)])
    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    states = []
    for phase in range(case['passes']):
        rng = random.Random(20261030 + seed + phase * 9000)
        registers = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
        registers[:2] = [0x03000000 if case.get('invalidChannel') else case['channel'], case['length']]
        registers[-2:] = [memory.STACK + 0x3F00, memory.RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
        for register, value in zip(match_runtime.REGISTERS, registers):
            cpu.reg_write(register, value)
        first_write = len(writes)
        fault = None
        try:
            cpu.emu_start(ADDRESS, memory.RETURN, count=budget, timeout=100000)
        except UcError as error:
            fault = error.errno
        returned = cpu.reg_read(UC_ARM_REG_PC) == memory.RETURN
        observed = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if returned:
            expected_ram, expected_wram, expected_writes, flags = modeled(ram, wram, case)
            if writes[first_write:] != expected_writes or bytes(cpu.mem_read(memory.DATA, 0x4000)) != expected_ram or bytes(cpu.mem_read(memory.BASE, 0x14000)) != expected_wram:
                raise ValueError('Independent full-byte-domain player/track flags/IDs/ordered-store model differs')
            predicted = list(registers)
            predicted[:4] = [case['channel'], flags | 3, flags | 2, 0xFFFE9680]
            if observed != predicted or cpu.reg_read(UC_ARM_REG_CPSR) != seed % 16 << 28 | 0xD3:
                raise ValueError('Initializer saved-register/stack/actual-return ABI differs')
            ram, wram = expected_ram, expected_wram
        states.append({'actualReturn': returned, 'fault': fault, 'pc': cpu.reg_read(UC_ARM_REG_PC), 'registers': observed,
            'cpsr': cpu.reg_read(UC_ARM_REG_CPSR), 'writes': writes[first_write:],
            'ramSha256': digest(bytes(cpu.mem_read(memory.DATA, 0x4000))), 'wramAndBssSha256': digest(bytes(cpu.mem_read(memory.BASE, 0x14000))),
            'stackSha256': digest(bytes(cpu.mem_read(memory.STACK, 0x4000)))})
        if not returned:
            break
    return {'states': states, 'visited': sorted(visited)}


def oracle(entry, original, rebuilt):
    records, visited, returns = [], set(), 0
    for seed, case in enumerate(cases()):
        expected, actual = execute(entry, original, case, seed), execute(entry, rebuilt, case, seed)
        if expected != actual or any(not state['actualReturn'] or state['fault'] is not None for state in expected['states']):
            raise ValueError('Initializer original/source complete return/CPU/memory effects differ')
        returns += len(expected['states']) * 2
        visited.update(expected['visited'])
        records.append({'case': case, 'seed': seed, 'actualOriginalAndCompiledReturns': len(expected['states']) * 2,
            'orderedStoresPerCall': [len(row['writes']) for row in expected['states']], 'stateSha256': digest(repr(expected).encode())})
    own = set(range(ADDRESS, ADDRESS + CODE, 4))
    if not own.issubset(visited):
        raise ValueError('Initializer complete own instruction coverage incomplete')
    controls = []
    for name, case, limit in (('single-instruction-budget', cases()[0], 1), ('unmapped-channel', dict(cases()[0], invalidChannel=True), 10000)):
        expected, actual = execute(entry, original, case, 0, limit), execute(entry, rebuilt, case, 0, limit)
        if expected != actual or any(row['actualReturn'] for row in expected['states']):
            raise ValueError('Unsupported channel start received return credit')
        controls.append({'name': name, 'returnCredit': 0, 'state': expected})
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records), 'actualOriginalAndCompiledReturns': returns,
        'actualSeparatelyObservedNestedReturns': {}, 'freshMachinePerScenario': True, 'instructionLimit': 10000,
        'timeoutMicroseconds': 100000, 'cpuModel': 'Unicorn TI925T ARMv4T surrogate', 'allOwnInstructionAddressesVisited': sorted(own),
        'independentFullFlagsLengthAndPartialChannelFieldModel': True, 'providerReplacements': [], 'records': records,
        'unsupportedControls': controls, 'unsupportedReturnCredit': 0,
        'returnContract': 'void; incidental R0 compared only as machine state', 'calleeSourceCredit': 0,
        'limitations': ['Only measured field effects on bounded aligned synthetic channel views; full channel allocation/layout extent not reconstructed',
            'All256 flag-byte values, selected full32-bit length words, page-crossing destination and repeated calls are covered',
            'No physical audio, enclosing caller validity, complete object initialization, data or whole-module source credit']}
