import hashlib
import json
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

ADDRESS = 0x02011244
BOUNDARY = 0x02011250
BACKEND = 0x020E5500
PAGE = 0x020E5000
STACK = 0x02500000
STOP = 0x027FF800
ARM_TASK = 0x020F0100
THUMB_TASK = 0x020F0201
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]
PROVIDERS = {0x02007FF4: 'irq-disable', 0x02008008: 'irq-restore', 0x020068D4: 'sleep', ARM_TASK: 'task-arm', THUMB_TASK & ~1: 'task-thumb'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(data, address):
    return struct.unpack_from('<I', data, address - PAGE)[0]


def write(data, address, value):
    struct.pack_into('<I', data, address - PAGE, value & 0xFFFFFFFF)


def task(cycle):
    return THUMB_TASK if cycle['thumb'] else ARM_TASK


def model(before, schedule, seed):
    expected = bytearray(before)
    events = []
    for index, cycle in enumerate(schedule):
        events += ['irq-disable', *(['sleep'] * cycle['sleeps']), 'irq-restore', 'task-thumb' if cycle['thumb'] else 'task-arm']
        flags = read(expected, BACKEND + 0x114) & ~8
        if index + 1 < len(schedule):
            flags |= 8 if not schedule[index + 1]['sleeps'] else 0
            write(expected, BACKEND + 0x40, task(schedule[index + 1]))
        write(expected, BACKEND + 0x114, flags)
        write(expected, BACKEND + 0x24, seed ^ ((index + 1) * 0x1234567))
    return bytes(expected), events


def run(body, before, stack, schedule, seed, registers, flags):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_write(ADDRESS, body)
    machine.mem_write(PAGE, before)
    machine.mem_write(STACK, stack)
    machine.reg_write(UC_ARM_REG_CPSR, flags)
    for register, value in zip(REGISTERS, registers):
        machine.reg_write(register, value)
    events, writes, visited = [], [], set()
    state = {'index': 0, 'sleeps': 0, 'savedIrq': 0, 'boundedStop': False}

    def memword(address):
        return struct.unpack('<I', bytes(machine.mem_read(address, 4)))[0]

    def memwrite(address, value):
        uc_value = value & 0xFFFFFFFF
        machine.mem_write(address, struct.pack('<I', uc_value))
        writes.append([address, 4, uc_value])

    def observe(uc, pc, size, data):
        if pc not in PROVIDERS:
            if not ADDRESS <= pc < ADDRESS + 76:
                raise AssertionError(('Task loop escaped its source body', hex(pc)))
            visited.add(pc)
            if pc == BOUNDARY and state['index'] == len(schedule):
                state['boundedStop'] = True
                uc.emu_stop()
            return
        index = state['index']
        if index >= len(schedule):
            raise AssertionError('Task loop entered another provider after scheduled cycles')
        cycle = schedule[index]
        name = PROVIDERS[pc]
        events.append(name)
        result = (seed ^ pc ^ len(events)) & 0xFFFFFFFF
        next_irq = uc.reg_read(UC_ARM_REG_CPSR) & 0x80
        if name == 'irq-disable':
            if state['sleeps'] or bool(memword(BACKEND + 0x114) & 8) != (cycle['sleeps'] == 0):
                raise AssertionError('Task cycle initial ready state differs')
            state['savedIrq'] = next_irq
            result, next_irq = next_irq, 0x80
        elif name == 'sleep':
            if uc.reg_read(UC_ARM_REG_R0) != 0 or not next_irq or memword(BACKEND + 0x114) & 8:
                raise AssertionError('Sleep contract/IRQ/ready state differs')
            state['sleeps'] += 1
            if state['sleeps'] > cycle['sleeps']:
                raise AssertionError('Task loop slept beyond the scheduled readiness transition')
            if state['sleeps'] == cycle['sleeps']:
                memwrite(BACKEND + 0x114, memword(BACKEND + 0x114) | 8)
        elif name == 'irq-restore':
            if uc.reg_read(UC_ARM_REG_R0) != state['savedIrq'] or state['sleeps'] != cycle['sleeps'] or not memword(BACKEND + 0x114) & 8:
                raise AssertionError('Task-loop restore/ready/readiness contract differs')
            next_irq = state['savedIrq']
        else:
            if pc != task(cycle) & ~1 or bool(uc.reg_read(UC_ARM_REG_CPSR) & 0x20) != cycle['thumb']:
                raise AssertionError('ARM/Thumb callback interworking differs')
            if uc.reg_read(UC_ARM_REG_R0) != BACKEND or next_irq != state['savedIrq']:
                raise AssertionError('Task callback argument or restored IRQ differs')
            current = memword(BACKEND + 0x114) & ~8
            if index + 1 < len(schedule):
                current |= 8 if not schedule[index + 1]['sleeps'] else 0
                memwrite(BACKEND + 0x40, task(schedule[index + 1]))
            memwrite(BACKEND + 0x114, current)
            memwrite(BACKEND + 0x24, seed ^ ((index + 1) * 0x1234567))
            state['index'] += 1
            state['sleeps'] = 0
            next_irq = ((seed + index + 1) & 1) << 7
        for number, register in enumerate([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]):
            uc.reg_write(register, (seed ^ pc ^ ((number + 1) * 0x7654321)) & 0xFFFFFFFF)
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_CPSR, ((seed + len(events)) & 15) << 28 | next_irq | 0x10)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR) & ~1)

    def observe_write(uc, access, address, size, value, data):
        if not (STACK <= address and address + size <= STACK + len(stack)):
            raise AssertionError('Native task body wrote outside its retained stack frame')
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, observe)
    machine.hook_add(UC_HOOK_MEM_WRITE, observe_write)
    machine.emu_start(ADDRESS, STOP, count=2000)
    if not state['boundedStop'] or machine.reg_read(UC_ARM_REG_PC) != BOUNDARY or state['index'] != len(schedule):
        raise AssertionError('Task loop did not reach its explicit scheduled-cycle boundary; timeout is failure')
    arena = bytes(machine.mem_read(PAGE, len(before)))
    expected_arena, plan = model(before, schedule, seed)
    expected_stack = bytearray(stack)
    struct.pack_into('<IIII', expected_stack, registers[-2] - STACK - 16, registers[4], registers[5], registers[6], STOP)
    actual_stack = bytes(machine.mem_read(STACK, len(stack)))
    actual_registers = [machine.reg_read(register) for register in REGISTERS]
    if arena != expected_arena or events != plan or actual_stack != bytes(expected_stack):
        raise AssertionError('Independent task-loop arena/stack/call model differs')
    if actual_registers[4:7] != [0, BACKEND, state['savedIrq']] or actual_registers[7:12] != registers[7:12] or actual_registers[-2] != registers[-2] - 16:
        raise AssertionError('Bounded task-loop live register/frame state differs')
    return {'registers': actual_registers, 'pc': machine.reg_read(UC_ARM_REG_PC), 'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'arena': arena, 'stack': actual_stack, 'events': events, 'writes': writes, 'visited': sorted(visited), 'cycles': state['index']}


def validate(arm, save, matches, root):
    if set(matches) != {'saved_20261029_card_task_loop'}:
        raise AssertionError('Exact nonreturning task-loop source is required')
    row, rebuilt = matches['saved_20261029_card_task_loop']
    native = arm[ADDRESS - 0x02000000:ADDRESS - 0x02000000 + 80]
    rng = random.Random(20261029011244)
    hashes, coverage = [], set()
    total_cycles, arm_callbacks, thumb_callbacks = 0, 0, 0
    for seed in range(256):
        schedule = [{'sleeps': 0 if (seed >> (index % 8)) & 1 else 1 + (seed + index) % 4, 'thumb': bool((seed + index) & 1)} for index in range(1 + seed % 6)]
        arena, stack = bytearray(rng.randbytes(4096)), rng.randbytes(0x8000)
        write(arena, BACKEND + 0x114, (read(arena, BACKEND + 0x114) & ~8) | (8 if not schedule[0]['sleeps'] else 0))
        write(arena, BACKEND + 0x40, task(schedule[0]))
        registers = [rng.getrandbits(32) for unused in REGISTERS]
        registers[-2:] = [STACK + len(stack) - 16, STOP]
        flags = rng.getrandbits(4) << 28 | ((seed & 1) << 7) | 0x10
        original = run(native, bytes(arena), stack, schedule, seed, registers, flags)
        compiled = run(rebuilt, bytes(arena), stack, schedule, seed, registers, flags)
        if original != compiled:
            raise AssertionError('Native/source task-loop observations differ')
        coverage.update(original['visited'])
        total_cycles += len(schedule)
        arm_callbacks += sum(not cycle['thumb'] for cycle in schedule)
        thumb_callbacks += sum(cycle['thumb'] for cycle in schedule)
        encoded = {**original, 'arena': sha(original['arena']), 'stack': sha(original['stack'])}
        hashes.append(sha(json.dumps(encoded, sort_keys=True).encode()))
    if set(coverage) != set(range(ADDRESS, ADDRESS + 76, 4)):
        raise AssertionError('Nonreturning task-loop instruction coverage is incomplete')
    return {'cases': 256, 'nativeAndRecompiledExecutions': 512, 'normalReturningCases': 0, 'nativeRoutineReturns': False, 'verifiedReturn': False, 'verifiedScheduledLoopBoundary': True, 'timeoutsCountedAsReturns': False, 'scheduledCycles': total_cycles, 'armTaskCallbacks': arm_callbacks, 'thumbTaskCallbacks': thumb_callbacks, 'instructionLimit': 2000, 'independentMachineStatePerExecution': True, 'stateSha256': hashes, 'nativeInstructionAddressesVisited': sorted(coverage), 'sourceBodiesExecuted': 1, 'retainedNativeCalleeCodeBytes': 0, 'platformProviders': {hex(address): name for address, name in PROVIDERS.items()}, 'observations': ['Every sample stops at02011250 only after all scheduled outer-loop cycles complete; the original routine deliberately never returns.', 'Ready and initially-not-ready paths, one-to-four sleep iterations, full32-bit flags and changing callback pointers are exercised.', 'The task pointer executes controlled ARM or Thumb provider callbacks with backend argument after restoring that cycle saved IRQ state.', 'Repeated cycles retain a single stack frame and preserve non-work callee registers; the complete common arena and stack satisfy an independent model.'], 'limitations': ['Finite scheduled-cycle equivalence is not a proof of liveness, fairness, real task behavior, IRQ safety or concurrent execution.', 'IRQ disable/restore, sleep and synthetic ARM/Thumb callbacks remain explicit providers.', 'No source-recovery or normal-return credit is assigned to the provider implementations.']}
