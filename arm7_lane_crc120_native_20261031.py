import hashlib
from pathlib import Path
import random
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_TI925T

ROOT = Path(__file__).resolve().parent
BASE, ADDRESS, SIZE, CODE = 0x027E0000, 0x027E93D4, 120, 112
TABLE, STACK, RETURN = 0x027F7F74, 0x02300000, 0x02500000
MODULE = 'extract/utility/runtime/utility-child-arm7-main.bin'
MODULE_SHA = 'a5838c09ff9e04d2ffbdf780b3d1bbd5b5875dda9f2ea7d7f8eed74a60d1920a'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def step(byte, previous):
    value = (previous & 0xFFFF) ^ (byte & 255)
    for unused in range(8):
        value = value >> 1 ^ (0xA001 if value & 1 else 0)
    return value & 0xFFFF


def table(raw):
    values = []
    for index in range(16):
        value = index
        for unused in range(4):
            value = value >> 1 ^ (0xA001 if value & 1 else 0)
        values.append(value)
    expected = b''.join(value.to_bytes(2, 'little') for value in values)
    if raw[TABLE - BASE:TABLE - BASE + 32] != expected:
        raise ValueError('Original indexed halfword table differs from independent four-bit recurrence')
    return {'address': hex(TABLE), 'bytes': 32, 'sha256': digest(expected), 'polynomial': '0xa001', 'sourceDataCredit': 0}


def cases():
    rows = [(byte, previous) for byte in range(256) for previous in (0, 1, 0x8000, 0xFFFF)]
    rng = random.Random(20261031)
    rows += [(rng.getrandbits(32), rng.getrandbits(32)) for unused in range(256)]
    rows += [(byte, previous) for byte in (0x100, 0x80000000, 0xFFFFFFFF, 0x7FFFFFFF)
        for previous in (0x10000, 0x80000000, 0xFFFFFFFF, 0x7FFFFFFF)]
    return rows


def execute(body, values, seed, budget=1000):
    raw = (ROOT / MODULE).read_bytes()
    if digest(raw) != MODULE_SHA or len(body) != SIZE:
        raise ValueError('Qualified CRC module/body scope differs')
    table(raw)
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(BASE, 0x20000)
    cpu.mem_write(BASE, raw)
    cpu.mem_write(ADDRESS, body)
    cpu.mem_map(STACK, 0x1000)
    rng = random.Random(20261031 + seed)
    stack = rng.randbytes(0x1000)
    cpu.mem_write(STACK, stack)
    initial = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
    initial[0], initial[1], initial[-2:] = values[0], values[1], [STACK + 0xF00, RETURN]
    flags = seed % 16 << 28 | 0xD3
    cpu.reg_write(UC_ARM_REG_CPSR, flags)
    for register, value in zip(match_runtime.REGISTERS, initial):
        cpu.reg_write(register, value)
    visited, reads, writes = [], [], []

    def code(machine, pc, width, unused):
        if not ADDRESS <= pc < ADDRESS + CODE:
            raise ValueError('CRC escaped its actual own code extent')
        visited.append(pc)

    def read(machine, access, location, width, value, unused):
        if not ((location in (ADDRESS + CODE, ADDRESS + CODE + 4) and width == 4)
            or TABLE <= location < TABLE + 32 and location % 2 == 0 and width == 2):
            raise ValueError('CRC read escaped qualified own literal/16-halfword table')
        reads.append([location, width])

    def write(machine, access, location, width, value, unused):
        writes.append([location, width, value])

    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_READ, read)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    cpu.emu_start(ADDRESS, RETURN, count=budget, timeout=200000)
    actual = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
    returned = cpu.reg_read(UC_ARM_REG_PC) == RETURN
    if returned:
        if actual[0] != step(*values) or cpu.reg_read(UC_ARM_REG_CPSR) != flags:
            raise ValueError('Independent full-word/low-byte16 polynomial or APSR model differs')
        if actual[4:12] != initial[4:12] or actual[-2:] != initial[-2:] or writes or bytes(cpu.mem_read(STACK, 0x1000)) != stack:
            raise ValueError('CRC pure-memory/preserved-register/stack effects differ')
        if sum(width == 2 for location, width in reads) != 4 or sum(width == 4 for location, width in reads) != 2:
            raise ValueError('CRC actual table/literal access counts differ')
    return {'actualReturn': returned, 'pc': cpu.reg_read(UC_ARM_REG_PC), 'registers': actual, 'cpsr': cpu.reg_read(UC_ARM_REG_CPSR),
        'reads': reads, 'writes': writes, 'visited': visited, 'stackSha256': digest(bytes(cpu.mem_read(STACK, 0x1000)))}


def oracle(original, rebuilt):
    records, visited, indexes = [], set(), set()
    for seed, values in enumerate(cases()):
        first, second = execute(original, values, seed), execute(rebuilt, values, seed)
        if not first['actualReturn'] or first != second:
            raise ValueError('Original/fresh C CRC differs or failed actual return')
        visited.update(first['visited'])
        indexes.update((address - TABLE) // 2 for address, width in first['reads'] if width == 2)
        records.append({'inputWords': list(values), 'rawResult': first['registers'][0], 'seed': seed,
            'actualOriginalAndCompiledReturns': 2, 'stateSha256': digest(repr(first).encode())})
    if visited != set(range(ADDRESS, ADDRESS + CODE, 4)) or indexes != set(range(16)):
        raise ValueError('Full CRC code/table-index traversal incomplete')
    exhausted = execute(original, (0, 0), 0, budget=1)
    if exhausted['actualReturn']:
        raise ValueError('Instruction exhaustion received normal-return credit')
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records), 'actualOriginalAndCompiledReturns': len(records) * 2,
        'actualOriginalCalleeReturns': 0, 'freshMachinePerExecution': True, 'allOwnInstructionAddressesVisited': sorted(visited),
        'all16TableIndexesRead': sorted(indexes), 'all16InitialApsrCombinations': True, 'providerReplacements': [],
        'abiContract': 'Raw32 input words; result equals reflectedA001 recurrence on low8 byte and low16 prior value; unsigned16 zero-extended result; R1..R3/IP scratch',
        'sourceSignedShiftContract': 'Matching C uses target signed-word inputs/right shifts; pinned MWCC ARM two-complement behavior is measured; a broader portable rewrite is separate',
        'table': table((ROOT / MODULE).read_bytes()), 'sourceDataCredit': 0, 'records': records,
        'instructionLimit': 1000, 'timeoutMicroseconds': 200000, 'unsupportedBudget': exhausted, 'unsupportedReturnCredit': 0,
        'limitations': ['Original32-byte table remains an initialized-data dependency with zero reconstructed-source credit',
            'No full-image, enclosing-caller/game-meaning, physical-hardware or Android execution claim']}
