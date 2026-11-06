import hashlib
import json
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

ADDRESS = 0x02010058
BACKEND = 0x020E5500
PAGE = 0x020E5000
DESCRIPTORS = [0x020E54A0, 0x020E58F0]
STACK = 0x02500000
STOP = 0x027FF800
PANIC = 0x02008430
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]
PROVIDERS = {0x02007FF4: 'irq-disable', 0x02008008: 'irq-restore', 0x02006924: 'queue-wake', PANIC: 'panic-boundary'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(data, address):
    return struct.unpack_from('<I', data, address - PAGE)[0]


def write(data, address, value):
    struct.pack_into('<I', data, address - PAGE, value & 0xFFFFFFFF)


def model(before, owner, target, swap):
    expected = bytearray(before)
    reference = read(before, BACKEND + 12)
    events = ['irq-disable']
    if read(before, BACKEND + 8) != owner or not reference or read(before, BACKEND + 24) != target:
        return bytes(expected), events + ['panic-boundary'], 'panic-boundary'
    write(expected, BACKEND + 12, reference - 1)
    if reference == 1:
        write(expected, BACKEND + 8, 0xFFFFFFFD)
        write(expected, BACKEND + 24, 0)
        events.append('queue-wake')
        if swap:
            replacement = DESCRIPTORS[1] if read(before, BACKEND) == DESCRIPTORS[0] else DESCRIPTORS[0]
            write(expected, BACKEND, replacement)
    write(expected, read(expected, BACKEND), 0)
    return bytes(expected), events + ['irq-restore'], 'returned'


def run(body, before, stack, seed, owner, target, swap, registers, flags):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_write(ADDRESS, body)
    machine.mem_write(PAGE, before)
    machine.mem_write(STACK, stack)
    machine.reg_write(UC_ARM_REG_CPSR, flags)
    for register, value in zip(REGISTERS, registers):
        machine.reg_write(register, value)
    events, writes, visited = [], [], set()
    saved_irq = flags & 0x80

    def memword(address):
        return struct.unpack('<I', bytes(machine.mem_read(address, 4)))[0]

    def observe(uc, pc, size, data):
        if pc not in PROVIDERS:
            if not ADDRESS <= pc < ADDRESS + 136:
                raise AssertionError(('Resource unlock escaped its source body', hex(pc)))
            visited.add(pc)
            return
        name = PROVIDERS[pc]
        events.append(name)
        if name == 'panic-boundary':
            uc.emu_stop()
            return
        if name == 'queue-wake':
            if uc.reg_read(UC_ARM_REG_R0) != BACKEND + 16 or [memword(BACKEND + offset) for offset in [8, 12, 24]] != [0xFFFFFFFD, 0, 0]:
                raise AssertionError('Released fields do not precede queue wake')
            if swap:
                replacement = DESCRIPTORS[1] if memword(BACKEND) == DESCRIPTORS[0] else DESCRIPTORS[0]
                uc.mem_write(BACKEND, struct.pack('<I', replacement))
                writes.append([BACKEND, 4, replacement])
        if name == 'irq-restore':
            if uc.reg_read(UC_ARM_REG_R0) != saved_irq or memword(memword(BACKEND)) != 0:
                raise AssertionError('IRQ restore parameter or prior descriptor-result clear differs')
        result = saved_irq if name == 'irq-disable' else (seed ^ pc ^ len(events)) & 0xFFFFFFFF
        for number, register in enumerate([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]):
            uc.reg_write(register, (seed ^ pc ^ ((number + 1) * 0x1234567)) & 0xFFFFFFFF)
        uc.reg_write(UC_ARM_REG_R0, result)
        irq = saved_irq if name == 'irq-restore' else 0x80
        uc.reg_write(UC_ARM_REG_CPSR, ((seed + len(events)) & 15) << 28 | irq | 0x10)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    def observe_write(uc, access, address, size, value, data):
        if not any(start <= address and address + size <= start + length for start, length in [(PAGE, len(before)), (STACK, len(stack))]):
            raise AssertionError(('Resource helper wrote outside explicit state', hex(address), size))
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, observe)
    machine.hook_add(UC_HOOK_MEM_WRITE, observe_write)
    machine.emu_start(ADDRESS, STOP, count=1000)
    expected, plan, outcome = model(before, owner, target, swap)
    pc = machine.reg_read(UC_ARM_REG_PC)
    if pc != (STOP if outcome == 'returned' else PANIC):
        raise AssertionError('Unlock neither actually returned nor reached its declared terminal panic boundary')
    actual_registers = [machine.reg_read(register) for register in REGISTERS]
    if outcome == 'returned' and (actual_registers[4:12] != registers[4:12] or actual_registers[-2] != registers[-2]):
        raise AssertionError('Returning unlock failed preserved-register/SP restoration')
    arena = bytes(machine.mem_read(PAGE, len(before)))
    if arena != expected or events != plan:
        raise AssertionError(('Independent resource RAM/call model differs', events, plan))
    cpsr = machine.reg_read(UC_ARM_REG_CPSR)
    if outcome == 'returned' and cpsr & 0x80 != saved_irq:
        raise AssertionError('Returning caller did not restore the qualified IRQ state')
    return {'registers': actual_registers, 'cpsr': cpsr, 'pc': pc, 'outcome': outcome, 'arena': arena, 'stack': bytes(machine.mem_read(STACK, len(stack))), 'events': events, 'writes': writes, 'visited': sorted(visited)}


def validate(arm, save, matches, root):
    if set(matches) != {'saved_20261029_card_resource_unlock'}:
        raise AssertionError('Exact resource unlock source is required')
    row, rebuilt = matches['saved_20261029_card_resource_unlock']
    native = arm[ADDRESS - 0x02000000:ADDRESS - 0x02000000 + 140]
    rng = random.Random(20261029010058)
    hashes, coverage = [], set()
    outcomes = {'returned': 0, 'panic-boundary': 0}

    def compare(before, stack, owner, target, swap, seed):
        registers = [rng.getrandbits(32) for unused in REGISTERS]
        registers[0:2] = [owner, target]
        registers[-2:] = [STACK + len(stack) - 16, STOP]
        flags = rng.getrandbits(4) << 28 | ((seed & 1) << 7) | 0x10
        original = run(native, before, stack, seed, owner, target, swap, registers, flags)
        compiled = run(rebuilt, before, stack, seed, owner, target, swap, registers, flags)
        if original != compiled:
            raise AssertionError('Native/source resource unlock differs')
        outcomes[original['outcome']] += 1
        coverage.update(original['visited'])
        encoded = {**original, 'arena': sha(original['arena']), 'stack': sha(original['stack'])}
        hashes.append(sha(json.dumps(encoded, sort_keys=True).encode()))
        return original

    def fixture(owner, target, reference, swap, seed, mismatch=None):
        arena = bytearray(rng.randbytes(4096))
        for address, value in [(BACKEND, DESCRIPTORS[seed & 1]), (BACKEND + 8, owner ^ (1 if mismatch == 'owner' else 0)), (BACKEND + 12, 0 if mismatch == 'zero' else reference), (BACKEND + 24, target ^ (1 if mismatch == 'target' else 0))]:
            write(arena, address, value)
        return compare(bytes(arena), rng.randbytes(0x8000), owner, target, swap, seed)

    cases = 0
    for owner in [0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, 0xFFFFFFFD]:
        for reference in [1, 2, 3, 4, 255, 65535, 0x7FFFFFFF]:
            for target in [0, 1, 2, 0x80000000, 0xFFFFFFFF]:
                for swap in [False, True]:
                    fixture(owner, target, reference, swap, cases)
                    cases += 1
    for seed in range(128):
        fixture(rng.getrandbits(32), rng.getrandbits(32), rng.randrange(1, 0x80000000), bool(seed & 1), cases)
        cases += 1
    for seed in range(64):
        for mismatch in ['owner', 'zero', 'target']:
            fixture(rng.getrandbits(32), rng.getrandbits(32), 1 if seed & 1 else 3, bool(seed & 1), cases, mismatch)
            cases += 1
    for seed in range(16):
        owner, target = rng.getrandbits(32), rng.getrandbits(32)
        result = fixture(owner, target, 2, bool(seed & 1), cases)
        cases += 1
        for unused in range(2):
            result = compare(result['arena'], result['stack'], owner, target, bool(seed & 1), cases)
            cases += 1
    pcs = sorted(coverage)
    unreachable = [0x0201008C]
    if len(pcs) != 33 or set(pcs) != set(range(ADDRESS, ADDRESS + 136, 4)) - set(unreachable):
        raise AssertionError('Resource-helper qualified instruction coverage differs')
    return {'cases': cases, 'nativeAndRecompiledCalls': cases * 2, 'normalReturningCases': outcomes['returned'], 'terminalPanicBoundaryCases': outcomes['panic-boundary'], 'verifiedReturnForNormalCases': True, 'verifiedTerminalBoundaryForFailureCases': True, 'timeoutsCountedAsReturns': False, 'instructionLimit': 1000, 'independentMachineStatePerExecution': True, 'stateSha256': hashes, 'nativeInstructionAddressesVisited': pcs, 'unreachableUnderTerminalPanicProvider': unreachable, 'retainedNativeCalleeCodeBytes': 0, 'sourceBodiesExecuted': 1, 'platformProviders': {hex(address): name for address, name in PROVIDERS.items()}, 'observations': ['Matching lock identity, a positive reference count and matching target decrement the count; only the transition to zero releases identity/target and wakes the queue.', 'Descriptor result zeroing uses the descriptor pointer observed after the qualified wake provider, including controlled pointer changes.', 'The normal paths actually return, restore preserved registers/SP and restore the qualified saved IRQ state.', 'Owner mismatch, zero reference and target mismatch reach the declared terminal panic provider before descriptor clearing or IRQ restore.', 'Repeated calls progress from reference two to one, release at zero, and then reach the terminal invalid-unlock boundary.'], 'limitations': ['Panic implementation is not executed; reaching its provider boundary is separately classified and never counted as a normal return.', 'Physical queue wake and interrupt behavior remain explicit synthetic boundaries.', 'Signed refcounts below zero and signed arithmetic overflow are outside the supported normal reference-count domain.', 'The void API has no semantic return-value promise; architectural results are compared.']}
