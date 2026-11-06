import hashlib
import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC

START = 0x021b9000
LENGTH = 0x10000
IO = 0x021c6bfc
BUFFER = 0x02500000
ARENA = 0x20000
STOP = 0x027ff800
PARTS = [(0x90, 0x3a68, 0x021bd51c), (0x3a68, 0x3a9c, 0x021b9eb4), (0x3a9c, 0x5d40, 0x021bb278), (0x5d40, 0x70d0, 0x021b9ee8)]
DATE = bytes(range(16))
TIME = bytes(range(0x30, 0x3c))
SUMMARY = bytes((i * 17 + 9) & 255 for i in range(0x60))

def checksum(data, begin, end):
    return sum(struct.unpack_from('<I', data, at)[0] for at in range(begin, end, 4)) & 0xffffffff

def io_state(status=0x55, heap=2, callback=0x0207dac8, pointer=0):
    return struct.pack('<BBHII', status, heap & 255, 0x1234, callback, pointer)

def replace_io(state, value):
    output = bytearray(state)
    output[IO - START:IO - START + 12] = value
    return output

def build_bank(state, arena):
    output = bytearray(arena)
    struct.pack_into('<III', output, 0, 0x5a4953, 0x10000, 0x70d0)
    output[0xc:0x1c] = DATE
    output[0x1c:0x28] = TIME
    output[0x28:0x88] = SUMMARY
    for begin, end, source in PARTS:
        output[begin:end] = state[source - START:source - START + end - begin]
    struct.pack_into('<I', output, 0x88, checksum(output, 0x90, 0x70d0))
    struct.pack_into('<I', output, 0x8c, checksum(output, 0, 0x8c))
    return output

def validate(arm, save, matches, root):
    machines = []
    counts = {}
    touched = set()
    calls = 0
    context = {}
    boundaries = {0x02027b48: 'type', 0x02027be0: 'size', 0x0200f3e0: 'date', 0x0200f48c: 'time', 0x0202a44c: 'allocate', 0x0202a498: 'free', 0x02027cf8: 'write-async', 0x02027c44: 'write', 0x02027d8c: 'read', 0x02027ef4: 'poll', 0x0207db94: 'summary'}

    def boundary(machine, address, size, user):
        role = boundaries[address]
        registers = [machine.reg_read(register) for register in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        trace = {'role': role, 'arguments': registers}
        result = 0
        if role == 'date':
            machine.mem_write(registers[0], DATE)
        elif role == 'time':
            machine.mem_write(registers[0], TIME)
        elif role == 'summary':
            machine.mem_write(registers[0], SUMMARY)
        elif role == 'allocate':
            result = BUFFER if context.get('allocate', True) else 0
        elif role in ('write', 'write-async'):
            trace['data'] = bytes(machine.mem_read(registers[1], registers[2]))
            if role == 'write-async':
                trace['fifth'] = struct.unpack('<I', machine.mem_read(machine.reg_read(UC_ARM_REG_SP), 4))[0]
            result = int(context.get('write', True))
        elif role == 'read':
            result = int(context.get('read', True))
            if result:
                machine.mem_write(registers[1], context['headers'][registers[0]][:registers[2]])
        elif role == 'poll':
            machine.mem_write(registers[0], bytes([context.get('error', 0)]))
            result = int(context.get('complete', True))
        context['trace'].append(trace)
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

    def check(name, state, arena, expected_state, expected_arena, first=0, second=0, result=None, category=None, settings=None, inspect=None):
        nonlocal calls
        if name not in matches:
            return
        address = int(matches[name][0]['address'], 16)
        for machine in machines:
            context.clear()
            context.update(settings or {})
            context['trace'] = []
            machine.mem_write(START, bytes(state))
            machine.mem_write(BUFFER, bytes(arena))
            machine.mem_write(0x020edd04, struct.pack('<I', context.get('stride', 0x7100)))
            machine.reg_write(UC_ARM_REG_R0, first & 0xffffffff)
            machine.reg_write(UC_ARM_REG_R1, second & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(address, STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                raise AssertionError((name, 'execution bounds'))
            actual_state = bytes(machine.mem_read(START, LENGTH))
            actual_arena = bytes(machine.mem_read(BUFFER, ARENA))
            if actual_state != expected_state or actual_arena != expected_arena:
                state_diff = [hex(START + i) for i, (a, b) in enumerate(zip(actual_state, expected_state)) if a != b]
                arena_diff = [hex(BUFFER + i) for i, (a, b) in enumerate(zip(actual_arena, expected_arena)) if a != b]
                raise AssertionError((name, 'RAM effects', state_diff[:8], arena_diff[:8]))
            if result is not None and machine.reg_read(UC_ARM_REG_R0) != result & 0xffffffff:
                raise AssertionError((name, 'return', machine.reg_read(UC_ARM_REG_R0), result))
            if inspect:
                inspect(context['trace'])
            calls += 1
        counts[category or name] = counts.get(category or name, 0) + 1
        touched.add(name)

    rng = random.Random(20261027)
    states = [('zero', bytes(LENGTH)), ('ff', bytes([255]) * LENGTH)]
    for bank_index in range(2):
        state = bytearray(LENGTH)
        bank = save[bank_index * 0x7100:(bank_index + 1) * 0x7100]
        for begin, end, destination in PARTS:
            state[destination - START:destination - START + end - begin] = bank[begin:end]
        states.append((f'real-bank-{bank_index}', bytes(state)))
    states.extend((f'deterministic-{i}', rng.randbytes(LENGTH)) for i in range(4))
    arena = rng.randbytes(ARENA)
    for label, original_state in states:
        state = replace_io(original_state, io_state(pointer=BUFFER))
        expected = replace_io(state, io_state(pointer=0))
        check('save_write_initialize', state, arena, expected, arena, inspect=lambda trace: assert_roles(trace, ['type', 'size'], [[2], [0x70d0]]))
        expected_arena = bytearray(arena)
        struct.pack_into('<III', expected_arena, 0, 0x5a4953, 0x10000, 0x70d0)
        expected_arena[0xc:0x1c] = DATE
        expected_arena[0x1c:0x28] = TIME
        check('save_header_initialize', state, arena, state, expected_arena, BUFFER)
        check('save_write_status', state, arena, state, arena, result=0x55)
        check('save_alternate_validator_set', state, arena, replace_io(state, io_state(callback=0x0207dae8, pointer=BUFFER)), arena)
        check('save_serialized_buffer_get', state, arena, state, arena, result=BUFFER)
        for heap in [-1, 2, 127, 255]:
            for pointer in [0, BUFFER]:
                current = replace_io(state, io_state(heap=heap, pointer=pointer))
                expected = replace_io(current, io_state(heap=heap, pointer=0))
                check('save_serialized_buffer_free', current, arena, expected, arena, inspect=lambda trace, h=heap, p=pointer: assert_roles(trace, ['free'], [[signed_byte(h), p]]))
        for stride in [0x7100, 0x7200]:
            for heap in [-1, 2, 9]:
                for allocate in [False, True]:
                    settings = {'allocate': allocate, 'stride': stride}
                    expected_arena = build_bank(state, arena) if allocate else bytearray(arena)
                    expected = replace_io(state, io_state(heap=heap, pointer=BUFFER if allocate else 0))
                    check('save_serialize_allocate', state, arena, expected, expected_arena, heap, result=stride if allocate else 0, settings=settings)
                    for write in [False, True]:
                        expected_arena = build_bank(state, arena) if allocate else bytearray(arena)
                        if allocate:
                            expected_arena[stride:stride + 0x70d0] = expected_arena[:0x70d0]
                        status = 8 if not allocate else 0 if write else 1
                        expected = replace_io(state, io_state(status=status, heap=heap if allocate else 2, pointer=BUFFER if allocate else 0))
                        settings['write'] = write
                        check('save_write_start', state, arena, expected, expected_arena, heap, result=int(allocate and write), settings=settings, inspect=lambda trace, a=allocate, b=stride * 2, h=heap, data=expected_arena: inspect_write(trace, a, b, h, data))
        for complete in [False, True]:
            for error in [0, 1, 255]:
                for pointer in [0, BUFFER]:
                    current = replace_io(state, io_state(heap=255, pointer=pointer))
                    status = 0 if not complete else 1 if error else 0 if pointer else 8
                    expected_pointer = 0 if complete and pointer else pointer
                    expected = replace_io(current, io_state(status=status, heap=255, pointer=expected_pointer))
                    check('save_write_poll', current, arena, expected, arena, result=int(complete), settings={'complete': complete, 'error': error})
    headers = []
    for label, offset, value, status in [('valid', None, None, 0), ('marker', 0, 0, 3), ('total-length', 4, 0, 4), ('payload-length', 8, 0, 7), ('checksum', 0x8c, 0x12345678, 5)]:
        header = bytearray(save[:0x90])
        if offset is not None:
            struct.pack_into('<I', header, offset, value)
        headers.append((label, bytes(header), status))
    for index in [0, 1]:
        for label, header, status in headers:
            for read in [False, True]:
                for output in [0, BUFFER + 0x18000]:
                    state = replace_io(states[-1][1], io_state())
                    expected_status = status if read else 2
                    expected = replace_io(state, io_state(status=expected_status))
                    expected_arena = bytearray(arena)
                    if output and not expected_status:
                        expected_arena[0x18000:0x18090] = header
                    check('save_read_header', state, arena, expected, expected_arena, index, output, result=int(not expected_status), settings={'read': read, 'headers': {index: header}})
        for write in [False, True]:
            state = replace_io(states[-1][1], io_state())
            expected = replace_io(state, io_state(status=0 if write else 1))
            check('save_header_invalidate', state, arena, expected, arena, index, result=int(write), settings={'write': write}, inspect=lambda trace, i=index: inspect_invalidate(trace, i))
    if touched != set(matches):
        raise AssertionError(('Untested matches', sorted(set(matches) - touched)))
    return {'engine': 'Unicorn', 'cases': sum(counts.values()), 'nativeAndRecompiledCalls': calls, 'counts': counts, 'testedFunctions': sorted(touched), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'scratchBytesComparedPerCall': LENGTH + ARENA, 'stateVectors': [{'name': name, 'sha256': hashlib.sha256(data).hexdigest()} for name, data in states], 'boundaryStubs': {hex(address): role for address, role in boundaries.items()}, 'limitations': ['Date/time, header summary, allocation/free and device operations are controlled boundary stubs; real device timing and header-summary internals are not established by these tests.', 'All four serialized payload copies and both additive checks execute natively or as accepted recompiled functions; expected buffer bytes and checksums are calculated independently.', 'Original bank trailers and padding remain unchanged in these serializers; their meanings remain unknown.', 'A 0x7200 synthetic stride tests alignment behavior and is not an observed retail save format.']}

def signed_byte(value):
    value &= 255
    return (value - 256 if value >= 128 else value) & 0xffffffff

def assert_roles(trace, roles, arguments):
    if [row['role'] for row in trace] != roles:
        raise AssertionError(('boundary roles', trace, roles))
    for row, expected in zip(trace, arguments):
        if row['arguments'][:len(expected)] != expected:
            raise AssertionError(('boundary arguments', row, expected))

def inspect_write(trace, allocate, bytes_count, heap, arena):
    allocation = next(row for row in trace if row['role'] == 'allocate')
    if allocation['arguments'][:3] != [heap & 0xffffffff, bytes_count, 4]:
        raise AssertionError(('allocation arguments', allocation))
    writes = [row for row in trace if row['role'] == 'write-async']
    if len(writes) != int(allocate):
        raise AssertionError(('write count', writes))
    if writes and (writes[0]['arguments'] != [0, BUFFER, bytes_count, 0] or writes[0]['fifth'] != 0 or writes[0]['data'] != arena[:bytes_count]):
        raise AssertionError('Asynchronous duplicate-bank request differs')

def inspect_invalidate(trace, index):
    writes = [row for row in trace if row['role'] == 'write']
    if len(writes) != 1 or writes[0]['arguments'][:3] != [index, 0x027fef68, 0x90] or writes[0]['data'] != bytes(0x90):
        if len(writes) != 1 or writes[0]['arguments'][0] != index or writes[0]['arguments'][2] != 0x90 or writes[0]['data'] != bytes(0x90):
            raise AssertionError('Header invalidation request differs')
