import hashlib
import random
from pathlib import Path
import match_runtime
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_TI925T

ROOT = Path(__file__).resolve().parent
ADDRESS = 0x027F6A48
SIZE = 124
MAIN_BASE = 0x027E0000
WRAM_BASE = 0x037F8000
HELPER = 0x03805184
HELPER_END = 0x03805368
SKIPPED = 0x038051DC
STACK = 0x02300000
RETURN = 0x02500000
MAIN = 'extract/utility/runtime/utility-child-arm7-main.bin'
WRAM = 'extract/utility/runtime/utility-child-arm7-wram.bin'
MAIN_SHA = 'a5838c09ff9e04d2ffbdf780b3d1bbd5b5875dda9f2ea7d7f8eed74a60d1920a'
WRAM_SHA = '13c0f0469f28daf8fa0921ba61bd78bac7427fb872ef191ba234cd2a73f064d6'
MASK = 0xFFFFFFFF


def digest(data):
    return hashlib.sha256(data).hexdigest()


def machine(seed):
    main, wram = (ROOT / MAIN).read_bytes(), (ROOT / WRAM).read_bytes()
    if digest(main) != MAIN_SHA or digest(wram) != WRAM_SHA:
        raise ValueError('Qualified child module changed')
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(MAIN_BASE, 0x20000)
    cpu.mem_write(MAIN_BASE, main)
    cpu.mem_map(WRAM_BASE, 0x14000)
    cpu.mem_write(WRAM_BASE, wram)
    cpu.mem_map(STACK, 0x4000)
    cpu.mem_write(STACK, random.Random(seed + 20261031).randbytes(0x4000))
    return cpu


def helper_cases():
    rows = []
    for divisor in (1, 5, 7, 100, 400):
        for numerator in sorted({0, 1, divisor - 1, divisor, divisor + 1, 0x7FFFFFFF, 0x80000000, MASK}):
            rows.append((numerator, divisor))
    rng = random.Random(20261031)
    rows.extend((rng.getrandbits(32), (1, 5, 7, 100, 400)[index % 5]) for index in range(256))
    return rows


def helper_run(numerator, divisor, seed, budget=1000):
    cpu = machine(seed)
    rng = random.Random(seed + 20261101)
    initial = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
    initial[:2], initial[-2:] = [numerator, divisor], [STACK + 0x3F00, RETURN]
    cpu.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
    for register, value in zip(match_runtime.REGISTERS, initial):
        cpu.reg_write(register, value)
    visited, writes, transfers = set(), [], []

    def code(machine, pc, size, unused):
        if not HELPER <= pc < HELPER_END or pc == SKIPPED:
            raise ValueError('Division execution escaped measured code or entered the skipped NOP')
        if pc == 0x038051D8:
            selector = machine.reg_read(match_runtime.REGISTERS[2])
            target = pc + 8 + (selector << 2)
            if selector not in range(0, 85, 12) or not 0x038051E0 <= target < HELPER_END:
                raise ValueError('Native computed divide target escaped the decoded unrolled instructions')
            transfers.append({'pc': hex(pc), 'selector': selector, 'actualTarget': hex(target)})
        visited.add(pc)

    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_WRITE, lambda machine, access, address, size, value, unused: writes.append([address, size, value]))
    fault = None
    try:
        cpu.emu_start(HELPER, RETURN, count=budget, timeout=2000000)
    except UcError as error:
        fault = error.errno
    observed = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
    returned = cpu.reg_read(UC_ARM_REG_PC) == RETURN
    if returned:
        expected = [numerator // divisor, numerator % divisor] if divisor else [numerator, 0]
        if fault is not None or observed[:2] != expected or observed[4:] != initial[4:] or writes:
            raise ValueError('Independent native quotient/remainder two-register ABI differs')
    return {'actualReturn': returned, 'fault': fault, 'r0': observed[0], 'r1': observed[1],
        'packedU64': observed[0] | observed[1] << 32, 'preservedRegisters': observed[4:],
        'cpsr': cpu.reg_read(UC_ARM_REG_CPSR), 'visited': sorted(visited), 'writes': writes, 'computedTransfers': transfers}


def own_cases():
    words = (0, 1, 2, 3, 12, 0x7FFFFFFF, 0x80000000, MASK)
    rows = [(first, second, third) for first in (0, 1, 400, 0x80000000, MASK) for second in words for third in words]
    rng = random.Random(20261101)
    rows.extend(tuple(rng.getrandbits(32) for unused in range(3)) for index in range(128))
    return rows


def model(words):
    first, second, third = words
    if (second - 1) & MASK <= 1:
        first, second = (first - 1) & MASK, (second + 12) & MASK
    quotient400, quotient100 = first // 400, first // 100
    small = ((second * 13 + 8) & MASK) // 5
    total = (third + quotient400 + first + (first >> 2) - quotient100 + small) & MASK
    return total % 7


def execute(body, words, seed, budget=5000):
    if len(body) != SIZE:
        raise ValueError('Full compiled124 caller extent differs')
    cpu = machine(seed)
    cpu.mem_write(ADDRESS, body)
    rng = random.Random(seed + 20261102)
    initial = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
    initial[:3], initial[-2:] = words, [STACK + 0x3F00, RETURN]
    cpu.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
    for register, value in zip(match_runtime.REGISTERS, initial):
        cpu.reg_write(register, value)
    visited, writes, frames, completed = set(), [], [], []

    def code(machine, pc, size, unused):
        if frames and pc == frames[-1]['return']:
            frame = frames.pop()
            observed = [machine.reg_read(register) for register in match_runtime.REGISTERS]
            if observed[:2] != [frame['numerator'] // frame['divisor'], frame['numerator'] % frame['divisor']] or observed[4:13] != frame['saved']:
                raise ValueError('Actual original divide returned an invalid quotient/remainder/callee-saved pair')
            completed.append({'numerator': frame['numerator'], 'divisor': frame['divisor'], 'quotient': observed[0], 'remainder': observed[1]})
        if pc == HELPER:
            numerator, divisor = [machine.reg_read(register) for register in match_runtime.REGISTERS[:2]]
            if divisor not in (400, 100, 5, 7) or frames:
                raise ValueError('Caller escaped the qualified nonzero dual-register divide contract')
            frames.append({'return': machine.reg_read(match_runtime.REGISTERS[-1]), 'numerator': numerator, 'divisor': divisor,
                'saved': [machine.reg_read(register) for register in match_runtime.REGISTERS[4:13]]})
        if not ADDRESS <= pc < ADDRESS + SIZE and not HELPER <= pc < HELPER_END or pc == SKIPPED:
            raise ValueError('Own caller/division actual code scope escaped')
        visited.add(pc)

    def write(machine, access, location, size, value, unused):
        if not initial[-2] - 0x100 <= location < initial[-2]:
            raise ValueError('Caller wrote outside bounded temporary stack frame')
        writes.append([location, size, value & ((1 << (size * 8)) - 1)])

    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    fault = None
    try:
        cpu.emu_start(ADDRESS, RETURN, count=budget, timeout=2000000)
    except UcError as error:
        fault = error.errno
    observed = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
    pc, cpsr = cpu.reg_read(UC_ARM_REG_PC), cpu.reg_read(UC_ARM_REG_CPSR)
    returned = pc == RETURN
    if returned:
        if fault is not None or observed[0] != model(words) or observed[4:13] != initial[4:13] or observed[-2:] != initial[-2:] or frames:
            raise ValueError('Full-word wrap/return/ABI model differs')
        if [row['divisor'] for row in completed] != [400, 100, 5, 7]:
            raise ValueError('Caller did not actually return through four original native divide entries')
    return {'actualReturn': returned, 'fault': fault, 'registers': observed, 'cpsr': cpsr,
        'pc': pc, 'writes': writes, 'visited': sorted(visited), 'actualNativeDivideReturns': completed,
        'remainingFrames': frames, 'stackSha256': digest(bytes(cpu.mem_read(STACK, 0x4000)))}


def oracle(original, rebuilt):
    records, own_visited, helper_visited = [], set(), set()
    for seed, words in enumerate(own_cases()):
        first, second = execute(original, words, seed), execute(rebuilt, words, seed)
        if first != second or not first['actualReturn']:
            raise ValueError('Original/fresh linked C caller differed or failed actual return')
        own_visited.update(pc for pc in first['visited'] if ADDRESS <= pc < ADDRESS + SIZE)
        helper_visited.update(pc for pc in first['visited'] if HELPER <= pc < HELPER_END)
        records.append({'words': list(words), 'seed': seed, 'stateSha256': digest(repr(first).encode()),
            'r0': first['registers'][0], 'actualOwnOriginalAndCompiledReturns': 2,
            'actualSeparatelyObservedOriginalDivideReturns': 8, 'nativeDivideContracts': first['actualNativeDivideReturns']})
    if own_visited != set(range(ADDRESS, ADDRESS + SIZE, 4)):
        raise ValueError('Complete124 caller instruction traversal incomplete')
    unsupported = []
    for body in (original, rebuilt):
        state = execute(body, own_cases()[0], 0, budget=1)
        if state['actualReturn']:
            raise ValueError('Budget exhaustion received caller return credit')
        unsupported.append(state)
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records),
        'actualOriginalAndCompiledReturns': len(records) * 2, 'actualSeparatelyObservedNativeDivideReturns': len(records) * 8,
        'freshMachinePerExecution': True, 'cpuModel': 'Unicorn TI925T ARMv4T surrogate', 'instructionLimit': 5000,
        'timeoutMicroseconds': 2000000, 'providerReplacements': [], 'allOwnInstructionAddressesVisited': sorted(own_visited),
        'actualZeroCreditHelperInstructionAddressesVisited': sorted(helper_visited), 'records': records,
        'unsupportedBudgetStates': unsupported, 'unsupportedReturnCredit': 0, 'calleeSourceCredit': 0,
        'abiContract': 'Original helper returns quotient in R0 and remainder in R1 for measured nonzero divisors; a C u64 packs the two ABI words, not a generic64-bit division result',
        'wordArithmetic': 'Unsigned32-bit arguments, adjustment, multiplication and additions wrap before final nonzero-divisor remainder',
        'limitations': ['No calendar/story/access meaning, valid-input constraints or enclosing caller reachability inferred',
            'Original divide code is a zero-credit dependency with a separately documented configured8-byte versus actual484-byte code-scope gap']}
