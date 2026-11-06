import hashlib
import random
from pathlib import Path
import match_runtime
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_TI925T

ROOT = Path(__file__).resolve().parent
BASE, DATA, STACK, RETURN, CALLEE = 0x037F8000, 0x023D0000, 0x023E0000, 0x023FF000, 0x037FFD90
RAW_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    result = [(flags, seed, (flags + seed) % 16, (0x100, 0x144, 0x180, 0xFFC)[seed], False)
        for flags in range(256) for seed in range(4)]
    result += [(flags, 2, status, 0x100, False) for flags in (0, 1, 3, 127, 255) for status in range(16)]
    result.append((255, 2, 15, 0x180, True))
    return result


def modeled(data, stack, address, registers):
    data, stack, writes = bytearray(data), bytearray(stack), []
    def put(location, size, value):
        value &= (1 << (size * 8)) - 1
        target, offset = (data, location - DATA) if DATA <= location < DATA + len(data) else (stack, location - STACK)
        target[offset:offset + size] = value.to_bytes(size, 'little')
        writes.append([location, size, value])
    put(registers[-2] - 8, 4, registers[4])
    put(registers[-2] - 4, 4, registers[-1])
    put(address + 0x24, 4, 0)
    put(address + 0x28, 4, 0)
    flags = data[address - DATA] | 2
    put(address, 1, flags)
    for bit in (4, 8, 16):
        flags &= ~bit
        put(address, 1, flags)
    flags = (flags & ~32 | 64) & ~128
    put(address, 1, flags)
    for offset, size, value in ((0x3B, 1, 0), (2, 2, 0), (0x12, 1, 64), (4, 1, 127), (5, 1, 127),
            (10, 2, 0), (8, 1, 0), (9, 1, 0), (6, 1, 0), (12, 2, 0), (14, 1, 255), (15, 1, 255),
            (16, 1, 255), (17, 1, 255), (1, 1, 127), (7, 1, 2), (0x14, 1, 60), (0x15, 1, 0),
            (0x16, 2, 0), (0x13, 1, 0), (0x1E, 2, 65535), (0x18, 1, 0), (0x1A, 1, 0),
            (0x1B, 1, 1), (0x19, 1, 16), (0x1C, 2, 0), (0x20, 4, 0), (0x3C, 4, 0)):
        put(address + offset, size, value)
    return bytes(data), bytes(stack), writes


def execute(entry, body, initial_flags, seed, status, offset, reentry=False, budget=256, invalid=False):
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw) != RAW_SHA:
        raise ValueError('Original ARM7 WRAM input changed')
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base, size in ((BASE, 0x10000), (DATA, 0x2000), (STACK, 0x2000), (RETURN, 0x1000)):
        machine.mem_map(base, size)
    address, track = int(entry['address'], 0), DATA + offset
    machine.mem_write(BASE, raw)
    machine.mem_write(address, body)
    rng = random.Random(20261030 + seed)
    data = bytearray(bytes([0 if seed == 0 else 255]) * 0x2000 if seed < 2 else rng.randbytes(0x2000))
    data[offset] = initial_flags
    data = bytes(data)
    stack = rng.randbytes(0x2000)
    machine.mem_write(DATA, data)
    machine.mem_write(STACK, stack)
    writes, visited, pending, nested = [], set(), [False], [0]
    def code(cpu, pc, size, unused):
        if not (address <= pc < address + entry['bytes'] or CALLEE <= pc < CALLEE + 36):
            raise ValueError('Track initializer left own body/qualified original LFO initializer')
        if pc == CALLEE:
            if cpu.reg_read(match_runtime.REGISTERS[0]) != track + 0x18 or pending[0]:
                raise ValueError('Native LFO initializer pointer ABI differs')
            pending[0] = True
        if pc == 0x038009BC and pending[0]:
            pending[0] = False
            nested[0] += 1
        visited.add(pc)
    def write(cpu, access, location, size, value, unused):
        writes.append([location, size, value & ((1 << (size * 8)) - 1)])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    states = []
    for phase in range(2 if reentry else 1):
        registers = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
        registers[0], registers[-2:] = 0x03000000 if invalid else track, [STACK + 0x1F00, RETURN]
        machine.reg_write(UC_ARM_REG_CPSR, status << 28 | 0xD3)
        for register, value in zip(match_runtime.REGISTERS, registers):
            machine.reg_write(register, value)
        first_write, old_nested = len(writes), nested[0]
        fault = None
        try:
            machine.emu_start(address, RETURN, count=budget, timeout=100000)
        except UcError as error:
            fault = error.errno
        returned = machine.reg_read(UC_ARM_REG_PC) == RETURN
        observed = [machine.reg_read(register) for register in match_runtime.REGISTERS]
        if returned:
            data, stack, expected = modeled(data, stack, track, registers)
            if writes[first_write:] != expected or bytes(machine.mem_read(DATA, 0x2000)) != data or bytes(machine.mem_read(STACK, 0x2000)) != stack:
                raise ValueError('Independent initializer flags/defaults/untouched bytes/ordered stores/frame model differs')
            if observed[4:12] != registers[4:12] or observed[-2:] != registers[-2:] or machine.reg_read(UC_ARM_REG_CPSR) != status << 28 | 0xD3:
                raise ValueError('Track initialization callee-saved/stack/flags ABI differs')
            if pending[0] or nested[0] - old_nested != 1:
                raise ValueError('Original LFO initializer did not actually return')
        states.append({'actualReturn': returned, 'fault': fault, 'pc': machine.reg_read(UC_ARM_REG_PC), 'registers': observed,
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'writes': writes[first_write:], 'actualNestedLfoReturns': nested[0] - old_nested,
            'ramSha256': digest(bytes(machine.mem_read(DATA, 0x2000))), 'stackSha256': digest(bytes(machine.mem_read(STACK, 0x2000))),
            'wramSha256': digest(bytes(machine.mem_read(BASE, 0x10000))), 'returnMapSha256': digest(bytes(machine.mem_read(RETURN, 0x1000)))})
        if not returned:
            break
    return {'states': states, 'visited': sorted(visited)}


def oracle(entry, original, rebuilt):
    records, visited, outer, nested = [], set(), 0, 0
    for initial_flags, seed, status, offset, reentry in cases():
        expected = execute(entry, original, initial_flags, seed, status, offset, reentry)
        actual = execute(entry, rebuilt, initial_flags, seed, status, offset, reentry)
        if expected != actual or any(not row['actualReturn'] or row['fault'] is not None for row in expected['states']):
            raise ValueError('Track initializer original/source full effects/ABI/return differ')
        count = len(expected['states']) * 2
        outer += count
        nested += sum(row['actualNestedLfoReturns'] for row in expected['states']) * 2
        visited.update(expected['visited'])
        records.append({'initialFlags': initial_flags, 'seed': seed, 'nzcv': status, 'objectOffset': offset, 'reentry': reentry,
            'actualOriginalAndCompiledReturns': count, 'actualNestedLfoReturns': count, 'stateSha256': digest(repr(expected).encode())})
    own = set(range(int(entry['address'], 0), int(entry['address'], 0) + entry['bytes'], 4))
    if not own.issubset(visited) or not set(range(CALLEE, CALLEE + 36, 4)).issubset(visited):
        raise ValueError('Initializer own/callee instruction coverage incomplete')
    controls = []
    for label, options in (('budget-exhaustion', {'budget': 10}), ('invalid-object', {'invalid': True})):
        expected = execute(entry, original, 255, 2, 15, 0x100, **options)
        actual = execute(entry, rebuilt, 255, 2, 15, 0x100, **options)
        if expected != actual or any(row['actualReturn'] for row in expected['states']):
            raise ValueError('Initializer unsupported path received return credit')
        controls.append({'name': label, 'returnCredit': 0, 'state': expected})
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records), 'actualOriginalAndCompiledReturns': outer,
        'actualSeparatelyObservedNestedLfoReturns': nested, 'freshMachinePerScenario': True, 'instructionLimit': 256,
        'timeoutMicroseconds': 100000, 'cpuModel': 'Unicorn TI925T ARMv4T surrogate', 'independentFlagsDefaultsUntouchedBytesOrderedStoresFrameModel': True,
        'records': records, 'allOwnInstructionAddressesVisited': sorted(own), 'unsupportedControls': controls, 'unsupportedReturnCredit': 0,
        'originalCallee': {'processor': 'arm7', 'program': '', 'module': 'arm7-wram', 'mode': 'arm', 'address': hex(CALLEE), 'bytes': 36,
            'providerReplacement': False, 'sourceCredit': 0}, 'returnContract': 'void; raw R0 compared only as machine state',
        'limitations': ['Synthetic aligned64-byte objects, all initial flag bytes and selected object page boundaries, no enclosing caller/physical sound claim',
            'Budget exhaustion and bad pointers have no return/error-result credit; target bitfield layout is independently fixed by native bytes']}
