import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC

FRAME = 0x020e5400
BACKEND = 0x020e5500
DESCRIPTOR = 0x02500000
IDENTITY = 0x020e33e8
STACK = 0x027ff000
STOP = 0x027ff800

def validate(arm, save, matches, root):
    machines = []
    context = {}
    counts = {}
    calls = 0
    touched = set()
    boundaries = {0x02000b64: 'validate', 0x02007ff4: 'irq-disable', 0x02008008: 'irq-restore', 0x020068d4: 'queue-wait', 0x0200ff98: 'schedule', 0x020106b8: 'worker', 0x0200ffd4: 'bus-lock', 0x02010058: 'bus-unlock', 0x02010278: 'poll-complete', 0x0201022c: 'wait-idle'}

    def field(machine, offset):
        return struct.unpack('<I', machine.mem_read(BACKEND + offset, 4))[0]

    def hook(machine, address, size, user):
        role = boundaries[address]
        first = machine.reg_read(UC_ARM_REG_R0)
        second = machine.reg_read(UC_ARM_REG_R1)
        row = {'role': role, 'first': first, 'second': second}
        result = 0
        if role == 'irq-disable':
            result = context['interrupt']
        elif role == 'queue-wait':
            context['waits'] += 1
            if context['waits'] >= context.get('wait-limit', 1):
                machine.mem_write(BACKEND + 0x114, struct.pack('<I', field(machine, 0x114) & ~4))
        elif role == 'irq-restore':
            row['flags'] = field(machine, 0x114)
            row['callback'] = field(machine, 0x38)
            row['argument'] = field(machine, 0x3c)
            row['first-before-request-store'] = field(machine, 0x1c)
        elif role in ('schedule', 'worker'):
            row['request'] = [field(machine, offset) for offset in (0x1c, 0x20, 0x24, 0x38, 0x3c, 0x2c, 0x30, 0x34)]
            if role == 'worker':
                machine.mem_write(DESCRIPTOR, struct.pack('<I', context['worker-status']))
                if context.get('worker-clear', False):
                    machine.mem_write(BACKEND + 0x114, struct.pack('<I', field(machine, 0x114) & ~4))
        elif role == 'poll-complete':
            result = context.get('complete', 0)
        context['trace'].append(row)
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
            machine.hook_add(UC_HOOK_CODE, hook, begin=address, end=address)
        machines.append(machine)

    def check(name, frame, descriptor, expected_frame, expected_descriptor, arguments=(), returned=None, settings=None, inspect=None):
        nonlocal calls
        if name not in matches:
            return
        address = int(matches[name][0]['address'], 16)
        for machine in machines:
            context.clear()
            context.update({'interrupt': 0x12345678, 'worker-status': 0, 'waits': 0, 'trace': []})
            context.update(settings or {})
            machine.mem_write(FRAME, bytes(frame))
            machine.mem_write(DESCRIPTOR, bytes(descriptor))
            machine.mem_write(IDENTITY, struct.pack('<I', 0x87654321))
            values = [*arguments, *([0] * 9)][:9]
            for reg, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), values[:4]):
                machine.reg_write(reg, value & 0xffffffff)
            machine.mem_write(STACK, struct.pack('<IIIII', *values[4:9]))
            machine.reg_write(UC_ARM_REG_SP, STACK)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(address, STOP, count=100000)
            if time.monotonic() - began > 1 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                raise AssertionError((name, 'execution bounds'))
            if bytes(machine.mem_read(FRAME, len(frame))) != expected_frame or bytes(machine.mem_read(DESCRIPTOR, len(descriptor))) != expected_descriptor:
                actual = bytes(machine.mem_read(FRAME, len(frame)))
                differences = [(hex(FRAME + index), a, b) for index, (a, b) in enumerate(zip(actual, expected_frame)) if a != b]
                raise AssertionError((name, 'frame differs', differences[:8]))
            if returned is not None and machine.reg_read(UC_ARM_REG_R0) != returned & 0xffffffff:
                raise AssertionError((name, 'return differs', machine.reg_read(UC_ARM_REG_R0), returned))
            if inspect:
                inspect(context['trace'])
            calls += 1
        counts[name] = counts.get(name, 0) + 1
        touched.add(name)

    rng = random.Random(20261027)
    base = BACKEND - FRAME
    frames = []
    for flags in [0, 4, 0x80000000, 0x80000004, 0xffffffff]:
        frame = bytearray(rng.randbytes(0x400))
        struct.pack_into('<I', frame, base, DESCRIPTOR)
        struct.pack_into('<I', frame, base + 0x114, flags)
        frames.append((flags, frame))
    descriptors = [bytes(0x80), bytes([255]) * 0x80, rng.randbytes(0x80)]
    for flags, frame in frames:
        for descriptor in descriptors:
            check('save_backend_busy', frame, descriptor, frame, descriptor, returned=int(bool(flags)))
            for name, offset in [('save_backend_result', 0), ('save_backend_capacity', 0x18), ('save_backend_page_alternate', 0x1c), ('save_backend_page_size', 0x24)]:
                check(name, frame, descriptor, frame, descriptor, returned=struct.unpack_from('<I', descriptor, offset)[0])
    for completed in [0, 1, 7, 0xffffffff]:
        flags, frame = frames[0]
        descriptor = descriptors[0]
        check('save_backend_completed', frame, descriptor, frame, descriptor, returned=completed, settings={'complete': completed}, inspect=lambda trace: assert_roles(trace, ['poll-complete']))
        check('save_backend_wait_completed', frame, descriptor, frame, descriptor, inspect=lambda trace: assert_roles(trace, ['wait-idle']))
        for identifier in [0, 1, 0x7fff, 0x8000, 0xffff]:
            check('save_backend_lock', frame, descriptor, frame, descriptor, [identifier], inspect=lambda trace, value=identifier: assert_bus(trace, value, False, True))
            roles = ['poll-complete'] + ([] if completed else ['wait-idle']) + ['bus-unlock']
            check('save_backend_unlock', frame, descriptor, frame, descriptor, [identifier], settings={'complete': completed}, inspect=lambda trace, value=identifier, roles=roles: assert_bus(trace, value, roles, False))
    vectors = [[0] * 9, [0xffffffff] * 9, list(range(9)), [0x7100, 0x02510000, 0x70d0, 0x11223344, 0x55667788, 1, 6, 1, 0]]
    vectors.extend([rng.getrandbits(32) for _ in range(9)] for _ in range(32))
    for flags, frame in frames:
        for waits in [1, 3]:
            for asynchronous in [0, 1, 7]:
                for worker_status in [0, 1, 0xffffffff]:
                    for worker_clear in [False, True]:
                        for values in vectors:
                            arguments = list(values)
                            arguments[5] = asynchronous
                            descriptor = descriptors[-1]
                            expected_frame = bytearray(frame)
                            after_wait = flags & ~4 if flags & 4 else flags
                            expected_flags = after_wait | 4
                            if not asynchronous and worker_clear:
                                expected_flags &= ~4
                            struct.pack_into('<I', expected_frame, base + 0x114, expected_flags)
                            for index, at in [(0, 0x1c), (1, 0x20), (2, 0x24), (3, 0x38), (4, 0x3c), (6, 0x2c), (7, 0x30), (8, 0x34)]:
                                struct.pack_into('<I', expected_frame, base + at, arguments[index])
                            expected_descriptor = bytearray(descriptor)
                            if not asynchronous:
                                struct.pack_into('<I', expected_frame, base + 0x104, 0x87654321)
                                struct.pack_into('<I', expected_descriptor, 0, worker_status)
                            old_first = struct.unpack_from('<I', frame, base + 0x1c)[0]
                            settings = {'wait-limit': waits, 'worker-status': worker_status, 'worker-clear': worker_clear}
                            check('save_backend_transfer', frame, descriptor, expected_frame, expected_descriptor, arguments, returned=1 if asynchronous else int(not worker_status), settings=settings, inspect=lambda trace, args=arguments, f=after_wait | 4, old=old_first, n=waits if flags & 4 else 0: assert_transfer(trace, args, f, old, n))
    if touched != set(matches):
        raise AssertionError(('Untested source matches', set(matches) - touched))
    return {'engine': 'Unicorn', 'cases': sum(counts.values()), 'nativeAndRecompiledCalls': calls, 'counts': counts, 'testedFunctions': sorted(touched), 'instructionLimitPerCall': 100000, 'elapsedSecondsLimit': 1, 'returnPcVerified': True, 'independentExpectedBackendAndDescriptorEffects': True, 'platformStubs': {hex(address): role for address, role in boundaries.items()}, 'observations': ['The backend serializesbusy-bit4 under an interrupt-state guard and waits through queue operations before replacing a request.', 'Callback and argument fields are stored before restoring the interrupt state; request payload fields follow that restore.', 'Async requests schedule worker0x020106B8 and return1; sync requests set an identity token, invoke the worker and returnwhether descriptor status is zero.', 'Descriptor accessors preserve raw32-bit status/capacity/page fields; no hardware model is inferred solely from those values.'], 'limitations': ['Interrupt primitives, queue waiting, scheduler, worker, physical bus locks and completion primitives are controlled providers.', 'These tests validate scheduling/control and ABI field effects, not actual interrupt safety, hardware timing or ARM7 communication.', 'Queue waits are tested with bounded provider completion; an indefinitely blocked provider remains a runtime dependency.']}

def assert_roles(trace, roles):
    if [row['role'] for row in trace] != roles:
        raise AssertionError(('Backend call roles differ', trace, roles))

def assert_bus(trace, identifier, roles, locking):
    expected = ['bus-lock'] if locking else roles
    assert_roles(trace, expected)
    row = trace[-1]
    if row['first'] != identifier or row['second'] != 2:
        raise AssertionError('Physical lock arguments differ')

def assert_transfer(trace, arguments, flags, previous_first, waits):
    roles = ['validate', 'irq-disable', *(['queue-wait'] * waits), 'irq-restore', 'schedule' if arguments[5] else 'worker']
    assert_roles(trace, roles)
    if trace[0]['first'] != 0x02000b8c or any(row['first'] != BACKEND + 0x10c for row in trace if row['role'] == 'queue-wait'):
        raise AssertionError('Backend validation/queue pointer differs')
    restored = next(row for row in trace if row['role'] == 'irq-restore')
    if restored['first'] != 0x12345678 or restored['flags'] != flags or restored['callback'] != arguments[3] or restored['argument'] != arguments[4] or restored['first-before-request-store'] != previous_first:
        raise AssertionError('IRQ restoration ordering or captured request metadata differs')
    row = trace[-1]
    if row['first'] != (0x020106b8 if arguments[5] else BACKEND) or row['request'] != [arguments[index] for index in (0, 1, 2, 3, 4, 6, 7, 8)]:
        raise AssertionError('Scheduled or synchronous request fields differ')
