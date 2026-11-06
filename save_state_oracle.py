import itertools
import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

FRAME = 0x021d4c00
STATE = 0x021d4c3c
FLAGS = 0x021d4cd8
IO = 0x021c6bfc
PREFIX = 0x021c6c08
OUTPUT = 0x02500000
STOP = 0x027ff800
PREFIX_DATA = b'BOUNDARY'

def model(initial_state, ticks, flags, output, phase_at, error_at, config):
    state = initial_state
    result = bytearray(output)
    trace = []
    io_status = None
    if state == 0:
        ticks = 0
        trace.append(('read', 0, PREFIX, 8))
        io_status = 0 if config['prefix'] else 2
        state = 10 if config['prefix'] else 100
    if state == 10:
        trace.append(('load-start', 9))
        if config['load-start']:
            trace.append(('message-open', 5, 6, 0x34, 0, 1, 0x52))
            state = 15
        else:
            state = 105
    if state == 15:
        trace.append(('load-poll',))
        if config['load-done']:
            trace.append(('status', config['load-status']))
            state = 20 if not config['load-status'] else 105 if config['load-status'] == 2 else 110
    if state == 20:
        trace.append(('write-start', 9))
        state = 25 if config['write-start'] else 107
    if state == 25:
        trace.append(('write-poll',))
        if config['write-done']:
            trace.append(('status', config['write-status']))
            state = 30 if not config['write-status'] else 107 if config['write-status'] == 1 else 110
    if state == 30:
        result[phase_at] = 19
        state = 150
    if state == 100:
        struct.pack_into('<I', result, error_at, 0x50000000)
        result[phase_at] = 3
        state = 200
    if state == 105:
        struct.pack_into('<I', result, error_at, 0x50000000)
        result[phase_at] = 3
        state = 150
    if state == 107:
        struct.pack_into('<I', result, error_at, 0x20000000)
        result[phase_at] = 3
        state = 150
    ticks = (ticks + 1) & 0xffff
    if state == 110 and ticks > 90:
        result[phase_at] = 16
        state = 150
    if state == 150 and ticks > 90:
        trace.append(('message-close', 0))
        state = 200
    done = int(state == 200)
    if done:
        state = 0
        flags &= ~2
    return state, ticks, flags, bytes(result), trace, done, io_status

def validate(arm, save, matches, root):
    machines = []
    context = {}
    touched = set()
    cases = 0
    calls = 0
    boundaries = {0x02027d8c: 'read', 0x0207e32c: 'load-start', 0x0207e340: 'load-poll', 0x0207e3f8: 'status', 0x0207dd5c: 'write-start', 0x0207dea8: 'write-poll', 0x020c22c4: 'message-open', 0x020c2330: 'message-close'}

    def boundary(machine, address, size, user):
        role = boundaries[address]
        first = machine.reg_read(UC_ARM_REG_R0)
        result = 0
        if role == 'read':
            second = machine.reg_read(UC_ARM_REG_R1)
            third = machine.reg_read(UC_ARM_REG_R2)
            context['trace'].append((role, first, second, third))
            result = context['prefix']
            if result:
                machine.mem_write(second, PREFIX_DATA[:third])
        elif role in ('load-start', 'write-start'):
            context['trace'].append((role, first))
            result = context[role]
        elif role in ('load-poll', 'write-poll'):
            context['trace'].append((role,))
            context['active-status'] = context['load-status' if role == 'load-poll' else 'write-status']
            result = context['load-done' if role == 'load-poll' else 'write-done']
        elif role == 'status':
            result = context['active-status']
            context['trace'].append((role, result))
        elif role == 'message-open':
            registers = [machine.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
            extra = struct.unpack('<II', machine.mem_read(machine.reg_read(UC_ARM_REG_SP), 8))
            context['trace'].append(tuple([role, *registers, *extra]))
        else:
            context['trace'].append((role, first))
        machine.reg_write(UC_ARM_REG_R0, result)
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for record, code in matches.values():
                machine.mem_write(int(record['address'], 16), code)
        for address in boundaries:
            machine.hook_add(UC_HOOK_CODE, boundary, begin=address, end=address)
        machines.append(machine)

    def execute(machine, address, first, second):
        machine.reg_write(UC_ARM_REG_R0, first)
        machine.reg_write(UC_ARM_REG_R1, second)
        machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        began = time.monotonic()
        machine.emu_start(address, STOP, count=100000)
        if machine.reg_read(UC_ARM_REG_PC) != STOP or time.monotonic() - began > 1:
            raise AssertionError('Recovery controller execution bounds exceeded')
        return machine.reg_read(UC_ARM_REG_R0)

    rng = random.Random(20261027)
    base_config = {'prefix': 1, 'load-start': 1, 'load-done': 1, 'load-status': 0, 'write-start': 1, 'write-done': 1, 'write-status': 0}
    configurations = [dict(base_config)]
    for key, value in [('prefix', 0), ('load-start', 0), ('load-done', 0), ('load-status', 2), ('load-status', 6), ('write-start', 0), ('write-done', 0), ('write-status', 1), ('write-status', 8), ('load-status', 255), ('write-status', 255)]:
        configurations.append(dict(base_config, **{key: value}))
    vectors = [(state, ticks, phase_at, config) for state, ticks, phase_at, config in itertools.product([0, 10, 15, 20, 25, 30, 100, 105, 107, 110, 150, 200, 1, 255], [0, 89, 90, 91, 65534, 65535], [0x10, 0x20, 0x21, 0x23], configurations)]
    for _ in range(256):
        config = {key: rng.choice([0, 1, 7]) if 'status' not in key else rng.choice([0, 1, 2, 6, 8, 255]) for key in base_config}
        vectors.append((rng.randrange(256), rng.randrange(65536), rng.choice([0x10, 0x20, 0x21, 0x23]), config))
    if 'save_recovery_update' in matches:
        address = int(matches['save_recovery_update'][0]['address'], 16)
        for state, ticks, phase_at, config in vectors:
            frame = bytearray(rng.randbytes(0x200))
            flags = rng.getrandbits(32)
            frame[STATE - FRAME] = state
            struct.pack_into('<H', frame, STATE - FRAME + 2, ticks)
            struct.pack_into('<I', frame, FLAGS - FRAME, flags)
            output = rng.randbytes(0x100)
            io = bytearray(rng.randbytes(0x20))
            expected = model(state, ticks, flags, output, phase_at, 0x20, config)
            expected_frame = bytearray(frame)
            expected_frame[STATE - FRAME] = expected[0]
            struct.pack_into('<H', expected_frame, STATE - FRAME + 2, expected[1])
            struct.pack_into('<I', expected_frame, FLAGS - FRAME, expected[2])
            expected_io = bytearray(io)
            if expected[6] is not None:
                expected_io[0] = expected[6]
                if config['prefix']:
                    expected_io[PREFIX - IO:PREFIX - IO + 8] = PREFIX_DATA
            for machine in machines:
                context.clear()
                context.update(config)
                context['trace'] = []
                machine.mem_write(FRAME, bytes(frame))
                machine.mem_write(OUTPUT, output)
                machine.mem_write(IO, bytes(io))
                result = execute(machine, address, OUTPUT + phase_at, OUTPUT + 0x20)
                if result != expected[5] or bytes(machine.mem_read(FRAME, 0x200)) != expected_frame or bytes(machine.mem_read(OUTPUT, 0x100)) != expected[3] or bytes(machine.mem_read(IO, 0x20)) != expected_io:
                    raise AssertionError(('Recovery state transition differs', state, ticks, phase_at, config))
                if context['trace'] != expected[4]:
                    raise AssertionError(('Recovery call sequence differs', context['trace'], expected[4]))
                calls += 1
            cases += 1
        touched.add('save_recovery_update')
    if 'save_recovery_prefix_read' in matches:
        address = int(matches['save_recovery_prefix_read'][0]['address'], 16)
        for success in [0, 1, 7]:
            initial = rng.randbytes(0x20)
            expected = bytearray(initial)
            expected[0] = 0 if success else 2
            if success:
                expected[PREFIX - IO:PREFIX - IO + 8] = PREFIX_DATA
            for machine in machines:
                context.clear()
                context.update({'prefix': success, 'trace': []})
                machine.mem_write(IO, initial)
                result = execute(machine, address, 0, 0)
                if result != int(bool(success)) or bytes(machine.mem_read(IO, 0x20)) != expected or context['trace'] != [('read', 0, PREFIX, 8)]:
                    raise AssertionError('Prefix read result differs')
                calls += 1
            cases += 1
        touched.add('save_recovery_prefix_read')
    if touched != set(matches):
        raise AssertionError(('Untested source matches', set(matches) - touched))
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': sorted(touched), 'instructionLimitPerCall': 100000, 'elapsedSecondsLimit': 1, 'returnPcVerified': True, 'independentExpectedStateAndTrace': True, 'counterBoundaries': [0, 89, 90, 91, 65534, 65535], 'outputAliasCases': ['separate', 'same-word-byte0', 'same-word-byte1', 'same-word-byte3'], 'boundaryStubs': {hex(address): role for address, role in boundaries.items()}, 'observations': ['This controller explicitly loads backup bank1 through the accepted wrapper, then initiates dual-bank writing on success.', 'Recovery state can advance through several phases in one call; the counter increments once per call and wraps as u16.', 'Completion/error presentation waits until the counter exceeds90, while one prefix-read failure path completes immediately.', 'These raw states and error outputs do not establish any chronology-based bank selection rule.'], 'limitations': ['Load/write providers and message presentation are controlled dependency stubs in this controller-specific oracle.', 'The prefix helper executes around a stubbed device reader; full hardware I/O and a visible recovery UI are not run.', 'State numbers and output codes are preserved as raw native identities without inferring undocumented player facts.']}
