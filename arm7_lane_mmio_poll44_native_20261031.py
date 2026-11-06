import hashlib
import random
from pathlib import Path
import match_runtime
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_TI925T

ROOT = Path(__file__).resolve().parent
BASE = 0x037F8000
ADDRESS = 0x037FB300
SIZE = 44
CODE = 40
STATUS = 0x0480819C
STACK = 0x02300000
RETURN = 0x02500000
CALLER = 0x037F913C
CALL_RETURN = 0x037F9140
MODULE = 'extract/arm7/runtime/arm7-wram.bin'
MODULE_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    rows = []
    for flags in range(16):
        for ordinal in (1, 2, 3999, 4000, 4001, None):
            rows.append({'flags': flags, 'readyOnRead': ordinal, 'unready': (flags * 0x1111 + 0x407F) & 0xFF7F,
                'ready': (flags * 0x1021 + 0xA580) & 0xFFFF | 0x80})
    rows.extend({'flags': value % 16, 'readyOnRead': ordinal, 'unready': value & 0xFF7F, 'ready': value | 0x80}
        for value in (0, 1, 0x7F, 0x80, 0xFF, 0x7FFF, 0x8000, 0xFF7F, 0xFFFF)
        for ordinal in (1, None))
    return rows


def model(case):
    for count in range(1, 4001):
        ready = case['readyOnRead'] is not None and count >= case['readyOnRead']
        status = case['ready'] if ready else case['unready']
        if status & 0x80:
            return {'reads': count, 'r0': status, 'remaining': 4001 - count, 'apsr': 0x20000000}
    return {'reads': 4000, 'r0': status, 'remaining': 0, 'apsr': 0x60000000}


def execute(body, case, seed, tail=False, budget=50000, map_status=True):
    raw = (ROOT / MODULE).read_bytes()
    if digest(raw) != MODULE_SHA or len(body) != SIZE:
        raise ValueError('Qualified poll module or complete compiled body differs')
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(BASE, 0x14000)
    cpu.mem_write(BASE, raw)
    cpu.mem_write(ADDRESS, body)
    cpu.mem_map(STACK, 0x4000)
    stack = random.Random(20261031 + seed).randbytes(0x4000)
    cpu.mem_write(STACK, stack)
    if map_status:
        cpu.mem_map(STATUS & ~0xFFF, 0x1000)
        cpu.mem_write(STATUS, (0xFFFF ^ case['unready']).to_bytes(2, 'little'))
    rng = random.Random(10202631 + seed)
    initial = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
    initial[-2:] = [STACK + 0x3E00, RETURN]
    restored = [rng.getrandbits(32) for unused in range(5)] + [RETURN]
    if tail:
        cpu.mem_write(initial[-2] + 8, b''.join(value.to_bytes(4, 'little') for value in restored))
        stack = bytes(cpu.mem_read(STACK, 0x4000))
    for register, value in zip(match_runtime.REGISTERS, initial):
        cpu.reg_write(register, value)
    cpu.reg_write(UC_ARM_REG_CPSR, case['flags'] << 28 | 0xD3)
    reads, writes, visited, nested = [], [], set(), []

    def code(machine, pc, size, unused):
        if not ADDRESS <= pc < ADDRESS + CODE and not (tail and CALLER <= pc < 0x037F914C):
            raise ValueError('Poll execution escaped its qualified own/caller-suffix scope')
        if pc == CALL_RETURN:
            nested.append(machine.reg_read(match_runtime.REGISTERS[0]))
        visited.add(pc)

    def read(machine, access, location, size, value, unused):
        if location == STATUS and map_status:
            if size != 2:
                raise ValueError('Poll status read width differs from original LDRH')
            ordinal = len(reads) + 1
            value = case['ready'] if case['readyOnRead'] is not None and ordinal >= case['readyOnRead'] else case['unready']
            machine.mem_write(STATUS, value.to_bytes(2, 'little'))
            reads.append([location, size, value])

    def write(machine, access, location, size, value, unused):
        writes.append([location, size, value & ((1 << (size * 8)) - 1)])

    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_READ, read)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    fault = None
    try:
        cpu.emu_start(CALLER if tail else ADDRESS, RETURN, count=budget, timeout=2000000)
    except UcError as error:
        fault = error.errno
    observed = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
    pc, cpsr = cpu.reg_read(UC_ARM_REG_PC), cpu.reg_read(UC_ARM_REG_CPSR)
    returned = pc == RETURN
    if returned:
        expected = model(case)
        preserved = initial[3:13] if not tail else restored[:5] + initial[8:13]
        expected_sp = initial[-2] + (32 if tail else 0)
        if fault is not None or len(reads) != expected['reads'] or observed[:3] != [expected['r0'], STATUS, expected['remaining']]:
            raise ValueError('Independent poll stop/read-count/zero-extended-word model differs')
        if observed[3:13] != preserved or observed[-2:] != [expected_sp, RETURN] or cpsr != expected['apsr'] | 0xD3:
            raise ValueError('Poll saved-register/caller-tail/APSR contract differs')
        if writes or bytes(cpu.mem_read(STACK, 0x4000)) != stack:
            raise ValueError('Read-only poll or native caller suffix wrote CPU memory')
        if tail and nested != [expected['r0']]:
            raise ValueError('Original caller suffix did not forward the actual poll R0 result')
    return {'actualReturn': returned, 'fault': fault, 'pc': pc, 'registers': observed, 'cpsr': cpsr,
        'writes': writes, 'statusReads': len(reads), 'statusReadTraceSha256': digest(repr(reads).encode()),
        'lastStatus': reads[-1][2] if reads else None, 'nativeCallerTailPollReturns': len(nested),
        'stackSha256': digest(bytes(cpu.mem_read(STACK, 0x4000))), 'visited': sorted(visited)}


def oracle(original, rebuilt):
    records, visited = [], set()
    for seed, case in enumerate(cases()):
        first, second = execute(original, case, seed), execute(rebuilt, case, seed)
        if first != second or not first['actualReturn']:
            raise ValueError('Original/fresh-C poll native execution differs or did not return')
        visited.update(first['visited'])
        records.append({'case': case, 'seed': seed, 'state': first, 'actualOriginalAndCompiledReturns': 2})
    tails = []
    for seed, case in enumerate(cases()[::6]):
        case = dict(case, readyOnRead=(1, 4000, None)[seed % 3])
        first, second = execute(original, case, seed, True), execute(rebuilt, case, seed, True)
        if first != second or not first['actualReturn'] or first['nativeCallerTailPollReturns'] != 1:
            raise ValueError('Original caller-suffix raw-R0 propagation differs')
        tails.append({'case': case, 'seed': seed, 'state': first, 'actualCallerSuffixReturns': 2, 'actualNestedPollReturns': 2})
    if not set(range(ADDRESS, ADDRESS + CODE, 4)).issubset(visited):
        raise ValueError('Poll own instruction coverage incomplete')
    unsupported = []
    for name, options in (('one-instruction-budget', {'budget': 1}), ('unmapped-status-address', {'map_status': False})):
        first = execute(original, cases()[0], 0, **options)
        second = execute(rebuilt, cases()[0], 0, **options)
        if first != second or first['actualReturn']:
            raise ValueError('Poll unsupported context received a false return')
        unsupported.append({'name': name, 'state': first, 'returnCredit': 0, 'supportedErrorPathCredit': 0})
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records),
        'actualOriginalAndCompiledReturns': len(records) * 2, 'actualOriginalAndCompiledOwnEntryReturns': len(records) * 2,
        'actualSeparatelyObservedNativeCallerSuffixReturns': len(tails) * 2,
        'actualSeparatelyObservedNestedPollReturns': len(tails) * 2,
        'freshMachinePerExecution': True, 'instructionLimit': 50000, 'timeoutMicroseconds': 2000000,
        'originalAndCompiledCodeBytesCompared': True, 'providerFreeReturnCredit': 0,
        'syntheticMmioReadContract': {'address': hex(STATUS), 'width': 2, 'readLimit': 4000,
            'stopPredicate': '(rawStatus & 0x80) != 0', 'physicalHardwareExecuted': False,
            'inputSchedule': 'Explicit synthetic 16-bit values before each original LDRH; ready at1/2/3999/4000/4001 or never'},
        'rawReturnContract': 'R0 is the zero-extended last halfword read, including the genuine 4000-read no-ready exit; no register/device meaning assigned',
        'sourceLocalAssignmentDominance': 'Initial remaining=4000 enters the loop; every early return follows status assignment, and the final return follows at least one iteration; signed decrement stays0..4000',
        'supportedOwnInstructionAddressesVisited': sorted(visited), 'records': records, 'callerSuffixRecords': tails,
        'unsupportedControls': unsupported, 'unsupportedReturnCredit': 0, 'calleeOrDataOrCallerSourceCredit': 0,
        'limitations': ['No physical MMIO/device readiness, timing, firmware, audio or game scene was executed',
            'Caller suffix begins at its real BL with a synthetic saved frame; complete parent caller/prefix reachability is unproved',
            '4001st-read readiness is outside the native4000-read bound; final return still carries its4000th unready raw value']}
