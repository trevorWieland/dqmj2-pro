import hashlib
import random
from pathlib import Path
import match_runtime
import arm7_seq_neighbor_model_20261030 as memory
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_PC, UC_ARM_REG_CPSR

ROOT = Path(__file__).resolve().parent
ADDRESS, CODE, PLAYERS = 0x037FFEF0, 92, 0x03808420
RAW_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases(address=None):
    return [{'flags': value, 'passes': 1} for value in range(256)] + [{'flags': 255, 'passes': 2}]


def setup(case, seed):
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw) != RAW_SHA:
        raise ValueError('Original initializer module differs')
    rng = random.Random(20261030 + seed)
    ram, wram = rng.randbytes(0x4000), bytearray(rng.randbytes(0x14000))
    wram[:len(raw)] = raw
    state = memory.Model(ram, wram)
    for index in range(16):
        state.put(PLAYERS + index * 36, 1, case['flags'] + index * 37)
        state.put(PLAYERS + index * 36 + 1, 1, case['flags'] ^ index ^ 0xA5)
    for index in range(32):
        state.put(memory.TRACKS + index * 64, 1, case['flags'] + index * 61)
    return bytes(state.regions[memory.DATA]), bytes(state.regions[memory.BASE])


def modeled(ram, wram):
    state = memory.Model(ram, wram)
    for index in range(16):
        player = PLAYERS + index * 36
        state.put(player, 1, state.get(player, 1) & ~1)
        state.put(player + 1, 1, index)
    for index in range(32):
        track = memory.TRACKS + index * 64
        state.put(track, 1, state.get(track, 1) & ~1)
    return bytes(state.regions[memory.DATA]), bytes(state.regions[memory.BASE]), state.writes


def execute(entry, body, case, seed, budget=10000):
    ram, wram = setup(case, seed)
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
        registers[-2:] = [memory.STACK + 0x3F00, memory.RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
        for register, value in zip(match_runtime.REGISTERS, registers):
            cpu.reg_write(register, value)
        first_write = len(writes)
        cpu.emu_start(ADDRESS, memory.RETURN, count=budget, timeout=100000)
        returned = cpu.reg_read(UC_ARM_REG_PC) == memory.RETURN
        observed = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if returned:
            expected_ram, expected_wram, expected_writes = modeled(ram, wram)
            if writes[first_write:] != expected_writes or bytes(cpu.mem_read(memory.DATA, 0x4000)) != expected_ram or bytes(cpu.mem_read(memory.BASE, 0x14000)) != expected_wram:
                raise ValueError('Independent full-byte-domain player/track flags/IDs/ordered-store model differs')
            if observed[4:12] != registers[4:12] or observed[-2:] != registers[-2:]:
                raise ValueError('Initializer saved-register/stack/actual-return ABI differs')
            ram, wram = expected_ram, expected_wram
        states.append({'actualReturn': returned, 'pc': cpu.reg_read(UC_ARM_REG_PC), 'registers': observed,
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
        if expected != actual or any(not state['actualReturn'] for state in expected['states']):
            raise ValueError('Initializer original/source complete return/CPU/memory effects differ')
        returns += len(expected['states']) * 2
        visited.update(expected['visited'])
        records.append({'case': case, 'seed': seed, 'actualOriginalAndCompiledReturns': len(expected['states']) * 2,
            'orderedStoresPerCall': [len(row['writes']) for row in expected['states']], 'stateSha256': digest(repr(expected).encode())})
    own = set(range(ADDRESS, ADDRESS + CODE, 4))
    if not own.issubset(visited):
        raise ValueError('Initializer complete own instruction coverage incomplete')
    expected, actual = execute(entry, original, cases()[0], 0, 1), execute(entry, rebuilt, cases()[0], 0, 1)
    if expected != actual or any(row['actualReturn'] for row in expected['states']):
        raise ValueError('Exhausted initializer received return credit')
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records), 'actualOriginalAndCompiledReturns': returns,
        'actualSeparatelyObservedNestedReturns': {}, 'freshMachinePerScenario': True, 'instructionLimit': 10000,
        'timeoutMicroseconds': 100000, 'cpuModel': 'Unicorn TI925T ARMv4T surrogate', 'allOwnInstructionAddressesVisited': sorted(own),
        'independentCompleteByteDomainFlagIdAndOrderedStoreModel': True, 'providerReplacements': [], 'records': records,
        'unsupportedControls': [{'name': 'single-instruction-budget', 'returnCredit': 0, 'state': expected}], 'unsupportedReturnCredit': 0,
        'returnContract': 'void; incidental R0 compared only as machine state', 'calleeSourceCredit': 0,
        'limitations': ['Only fixed16-player/32-track initialized BSS record effects, not enclosing caller/audio/gameplay semantics',
            'All256 original flag-byte values are covered per record with deterministic varied neighboring data',
            'BSS/source-module bytes outside the measured stores remain unchanged; no data or whole-module source credit']}
