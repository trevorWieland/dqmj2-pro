import hashlib
from pathlib import Path
import random
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_TI925T

ROOT = Path(__file__).resolve().parent
BASE, DATA, STACK, RETURN = 0x027E0000, 0x02260000, 0x02300000, 0x02500000
MODULE = 'extract/utility/runtime/utility-child-arm7-main.bin'
MODULE_SHA = 'a5838c09ff9e04d2ffbdf780b3d1bbd5b5875dda9f2ea7d7f8eed74a60d1920a'
GETTER, WRITER = 0x027E94C8, 0x027E94E8


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases(address):
    if address == GETTER:
        return [{'word': byte << 8 | (byte ^ 0xA5), 'parity': parity, 'value': 0}
            for byte in range(256) for parity in (0, 1)]
    values = [(value * 0x1E3779B1 & 0xFFFFFF00) | value for value in range(256)]
    values += [0, 1, 255, 256, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF]
    return [{'word': word, 'parity': parity, 'value': value}
        for value in values for parity in (0, 1) for word in (0, 0xFFFF, 0xA55A, 0x5AA5)]


def execute(address, body, case, seed, budget=1000):
    raw = (ROOT / MODULE).read_bytes()
    size = 32 if address == GETTER else 44
    if digest(raw) != MODULE_SHA or address not in (GETTER, WRITER) or len(body) != size:
        raise ValueError('Qualified child halfword-byte scope differs')
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(BASE, 0x20000)
    cpu.mem_write(BASE, raw)
    cpu.mem_write(address, body)
    cpu.mem_map(DATA, 0x1000)
    cpu.mem_map(STACK, 0x1000)
    rng = random.Random(20261031 + seed)
    memory, stack = bytearray(rng.randbytes(0x1000)), rng.randbytes(0x1000)
    cell = 0x100 + seed % 64 * 2
    memory[cell:cell + 2] = case['word'].to_bytes(2, 'little')
    cpu.mem_write(DATA, bytes(memory))
    cpu.mem_write(STACK, stack)
    initial = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
    initial[0], initial[1], initial[-2:] = DATA + cell + case['parity'], case['value'], [STACK + 0xF00, RETURN]
    flags = seed % 16 << 28 | 0xD3
    cpu.reg_write(UC_ARM_REG_CPSR, flags)
    for register, value in zip(match_runtime.REGISTERS, initial):
        cpu.reg_write(register, value)
    reads, writes, visited = [], [], []

    def code(machine, pc, width, unused):
        if not address <= pc < address + size:
            raise ValueError('Primitive escaped its complete code extent')
        visited.append(pc)

    def read(machine, access, location, width, value, unused):
        reads.append([location, width])

    def write(machine, access, location, width, value, unused):
        writes.append([location, width, value & ((1 << (width * 8)) - 1)])

    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_READ, read)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    cpu.emu_start(address, RETURN, count=budget, timeout=200000)
    actual = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
    returned = cpu.reg_read(UC_ARM_REG_PC) == RETURN
    expected_memory = bytearray(memory)
    expected_result = memory[cell + case['parity']] if address == GETTER else initial[0]
    expected_writes = []
    if address == WRITER:
        expected_memory[cell + case['parity']] = case['value'] & 255
        expected_writes = [[DATA + cell, 2, int.from_bytes(expected_memory[cell:cell + 2], 'little')]]
    if returned:
        expected_flags = flags & ~0xC0000000 | (0x40000000 if not case['parity'] else 0)
        if actual[0] != expected_result or cpu.reg_read(UC_ARM_REG_CPSR) != expected_flags:
            raise ValueError('Independent byte-lane return or ANDS NZ/CV semantics differ')
        if actual[4:] != initial[4:] or bytes(cpu.mem_read(STACK, 0x1000)) != stack:
            raise ValueError('Leaf preserved-register/stack state differs')
        if reads != [[DATA + cell, 2]] or writes != expected_writes:
            raise ValueError('Actual aligned halfword read/RMW width or ordered effect differs')
        if bytes(cpu.mem_read(DATA, 0x1000)) != bytes(expected_memory):
            raise ValueError('Independent selected-byte/adjacent-byte/guard model differs')
    return {'actualReturn': returned, 'pc': cpu.reg_read(UC_ARM_REG_PC), 'registers': actual, 'cpsr': cpu.reg_read(UC_ARM_REG_CPSR),
        'reads': reads, 'writes': writes, 'visited': visited, 'memorySha256': digest(bytes(cpu.mem_read(DATA, 0x1000))),
        'stackSha256': digest(bytes(cpu.mem_read(STACK, 0x1000)))}


def oracle(address, original, rebuilt):
    records, visited = [], set()
    for seed, case in enumerate(cases(address)):
        first, second = execute(address, original, case, seed), execute(address, rebuilt, case, seed)
        if not first['actualReturn'] or first != second:
            raise ValueError('Original/fresh C byte primitive differed or failed actual return')
        visited.update(first['visited'])
        records.append({'case': case, 'seed': seed, 'rawResult': first['registers'][0], 'actualOriginalAndCompiledReturns': 2,
            'stateSha256': digest(repr(first).encode())})
    if visited != set(range(address, address + len(original), 4)):
        raise ValueError('Full byte-primitive instruction traversal incomplete')
    exhausted = execute(address, original, cases(address)[0], 0, budget=1)
    if exhausted['actualReturn']:
        raise ValueError('Instruction budget exhaustion received return credit')
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records), 'actualOriginalAndCompiledReturns': len(records) * 2,
        'freshMachinePerExecution': True, 'allOwnInstructionAddressesVisited': sorted(visited), 'providerReplacements': [],
        'actualOriginalCalleeReturns': 0, 'all16InitialApsrCombinations': True, 'instructionLimit': 1000,
        'timeoutMicroseconds': 200000, 'records': records, 'unsupportedBudget': exhausted, 'unsupportedReturnCredit': 0,
        'abiContract': 'Full-word address and writer input; getter zero-extended selected byte; writer returns unchanged address; R1..R3 scratch; R4..LR preserved',
        'memoryContract': 'Exactly one aligned halfword read; writer exactly one aligned halfword write preserving adjacent byte; raw32 input is truncated to low8 for selected byte',
        'limitations': ['Synthetic backed RAM does not establish hardware-device or scene reachability',
            'Integer-address API is original32-bit target behavior; a native Android port requires explicit address abstraction',
            'No whole-module, original-data, BIOS, assembly or source credit for other units']}
