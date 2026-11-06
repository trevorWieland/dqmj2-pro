import hashlib
import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC

CONTROL = 0x020edcf0
FRAME = 0x020edc00
DEVICE = 0x020dd4b8
BUFFER = 0x02500000
ERROR = 0x02510000
STOP = 0x027ff800
TABLES = {'save_block_write': 0x020dd550, 'save_block_write_async': 0x020dd568, 'save_block_read': 0x020dd4c0, 'save_block_read_async': 0x020dd508}
RESULT_CODES = {0: 0, 1: 13, 2: 13, 3: 3, 4: 14, 6: 15, 7: 16}

def set_u32(data, offset, value):
    struct.pack_into('<I', data, offset, value & 0xffffffff)

def make_frame(locked=0, page_size=0x100, payload=0x70d0, blocks=2, stride=0x7100, capacity=0x10000):
    data = bytearray(bytes([0xa5]) * 0x200)
    values = struct.pack('<BBBBIIIIII', 0x55, locked, 1, 0x66, 0x71, payload, blocks, page_size, stride, capacity)
    data[CONTROL - FRAME:CONTROL - FRAME + 28] = values
    return data

def validate(arm, save, matches, root):
    machines = []
    context = {}
    calls = 0
    counts = {}
    touched = set()
    table_values = {name: [struct.unpack_from('<I', arm, address - 0x02000000 + index * 4)[0] for index in range(6)] for name, address in TABLES.items()}
    dispatch_addresses = {address for values in table_values.values() for address in values}
    platform = {0x020102fc: 'lock', 0x0201030c: 'unlock', 0x02010b10: 'completed', 0x020102b0: 'result'}
    pattern = bytes(range(256)) * 256

    def boundary(machine, address, size, user):
        values = [machine.reg_read(register) for register in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        if address in dispatch_addresses:
            trace = {'role': 'dispatch', 'address': address, 'arguments': values, 'lockedDuringCall': machine.mem_read(CONTROL + 1, 1)[0]}
            if context['function'].endswith('_async'):
                trace['fifth'] = struct.unpack('<I', machine.mem_read(machine.reg_read(UC_ARM_REG_SP), 4))[0]
            context['trace'].append(trace)
            if context['function'].startswith('save_block_read'):
                machine.mem_write(values[1], pattern[:values[2]])
            result = context['dispatchResult']
        else:
            role = platform[address]
            context['trace'].append({'role': role, 'arguments': values})
            if role == 'completed':
                result = context.get('completed', 0)
            elif role == 'result':
                result = context.get('result', 0)
            else:
                result = 0
        machine.reg_write(UC_ARM_REG_R0, result & 0xffffffff)
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for record, code in matches.values():
                machine.mem_write(int(record['address'], 16), code)
        for address in dispatch_addresses | set(platform):
            machine.hook_add(UC_HOOK_CODE, boundary, begin=address, end=address)
        machines.append(machine)

    def check(name, initial, expected, arguments=(), result=None, settings=None, expected_trace=None, expected_buffer=None, expected_error=None, device_type=2, lock_id=0x1234abcd):
        nonlocal calls
        if name not in matches:
            return
        address = int(matches[name][0]['address'], 16)
        for machine in machines:
            context.clear()
            context.update({'function': name, 'dispatchResult': 1})
            context.update(settings or {})
            context['trace'] = []
            machine.mem_write(FRAME, bytes(initial))
            device = struct.pack('<BBBBI', device_type & 255, 0x12, 0x34, 0x56, lock_id & 0xffffffff)
            machine.mem_write(DEVICE, device)
            machine.mem_write(BUFFER, bytes([0xcc]) * 0x10000)
            machine.mem_write(ERROR, bytes([0x99]) * 0x20)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), [*arguments, 0, 0, 0, 0][:4]):
                machine.reg_write(register, value & 0xffffffff)
            machine.mem_write(0x027ff000, struct.pack('<I', arguments[4] & 0xffffffff if len(arguments) > 4 else 0))
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(address, STOP, count=100000)
            if time.monotonic() - began > 1 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                raise AssertionError((name, 'execution bounds'))
            if bytes(machine.mem_read(FRAME, len(initial))) != expected:
                actual = bytes(machine.mem_read(FRAME, len(initial)))
                diff = [(hex(FRAME + i), a, b) for i, (a, b) in enumerate(zip(actual, expected)) if a != b]
                raise AssertionError((name, arguments, 'control frame differs', diff[:8]))
            if bytes(machine.mem_read(DEVICE, len(device))) != device:
                raise AssertionError('Backup device identity mutated')
            if result is not None and machine.reg_read(UC_ARM_REG_R0) != result & 0xffffffff:
                raise AssertionError((name, arguments, 'return differs', machine.reg_read(UC_ARM_REG_R0), result))
            if expected_trace:
                expected_trace(context['trace'])
            expected_buffer = expected_buffer if expected_buffer is not None else bytes([0xcc]) * 0x10000
            if bytes(machine.mem_read(BUFFER, 0x10000)) != expected_buffer:
                raise AssertionError((name, 'buffer effect differs'))
            error_bytes = bytes([0x99]) * 0x20 if expected_error is None else bytes([expected_error]) + bytes([0x99]) * 0x1f
            if bytes(machine.mem_read(ERROR, 0x20)) != error_bytes:
                raise AssertionError((name, 'error output differs'))
            calls += 1
        counts[name] = counts.get(name, 0) + 1
        touched.add(name)

    offset = CONTROL - FRAME
    for locked in [0, 1, 255]:
        initial = make_frame(locked)
        check('save_block_locked', initial, initial, result=locked)
        check('save_block_stride', initial, initial, result=0x7100)
        expected = bytearray(initial)
        expected[offset + 1] = 0
        check('save_block_unlock', initial, expected, result=int(bool(locked)), expected_trace=lambda trace, active=bool(locked): assert_lock_trace(trace, active, 0xabcd, 'unlock'))
        expected = bytearray(initial)
        if not locked:
            expected[offset + 1] = 1
        check('save_block_lock', initial, expected, result=int(not locked), expected_trace=lambda trace, active=not locked: assert_lock_trace(trace, active, 0xabcd, 'lock'))
    for page_size in [0, 1, 2, 0x100, 0x200, 0x1000]:
        for payload in [0, 1, 0x70d0, 0x7100, 0x7200, 0xffffffff]:
            for capacity in [0, 0x10000, 0x20000, 0xffffffff]:
                initial = make_frame(page_size=page_size, capacity=capacity)
                expected = bytearray(initial)
                numerator = (payload + page_size - 1) & 0xffffffff
                stride = (page_size * (numerator // page_size if page_size else numerator)) & 0xffffffff
                pages = stride // page_size if page_size else stride
                blocks = capacity // stride if stride else capacity
                for at, value in [(4, pages), (8, payload), (12, blocks), (20, stride)]:
                    set_u32(expected, offset + at, value)
                check('save_block_payload_set', initial, expected, [payload], result=0x70d0)
    for name in TABLES:
        asynchronous = name.endswith('_async')
        reading = name.startswith('save_block_read')
        for device_type in range(6):
            for index in [0, 1, 2, 0xffffffff]:
                for byte_count in [0, 1, 0x90, 0x70d0, 0x70d1, 0xe200, 0xffffffff]:
                    for locked in [0, 1]:
                        for dispatch_result in [0, 1, 7]:
                            initial = make_frame(locked)
                            expected = bytearray(initial)
                            accepted = index < 2 and (byte_count <= 0x70d0 or name == 'save_block_write_async')
                            status = 4 if index >= 2 else 11 if not accepted else 0 if asynchronous or dispatch_result else 9 if reading else 8
                            expected[offset] = status
                            if accepted:
                                expected[offset + 1] = 1 if asynchronous else 0
                            effective = byte_count if byte_count else 0x70d0
                            expected_buffer = bytearray(bytes([0xcc]) * 0x10000)
                            if accepted and reading:
                                expected_buffer[:effective] = pattern[:effective]
                            arguments = [index, BUFFER, byte_count, 0x11223344, 0x55667788]
                            check(name, initial, expected, arguments, result=int(accepted and (asynchronous or dispatch_result != 0)), settings={'dispatchResult': dispatch_result}, device_type=device_type, expected_buffer=expected_buffer, expected_trace=lambda trace, accept=accepted, n=name, t=device_type, i=index, length=effective, lock=locked: assert_dispatch(trace, accept, n, table_values[n][t], i, length, lock))
    for function in ['save_block_poll_result', 'save_block_poll']:
        for completed in [0, 1, 7]:
            for native_result in [0, 1, 2, 3, 4, 5, 6, 7, 8, 255, 256, 0xffffffff]:
                for locked in [0, 1]:
                    for error_pointer in [0, ERROR]:
                        initial = make_frame(locked)
                        expected = bytearray(initial)
                        error = RESULT_CODES.get(native_result & 255, 17)
                        expected[offset] = 10 if not completed else error if function == 'save_block_poll_result' else 0
                        if completed and function == 'save_block_poll':
                            expected[offset + 1] = 0
                        result = completed if function == 'save_block_poll_result' else int(bool(completed))
                        check(function, initial, expected, [error_pointer], result=result, settings={'completed': completed, 'result': native_result}, expected_error=error if completed and error_pointer else None)
    if touched != set(matches):
        raise AssertionError(('Untested source matches', set(matches) - touched))
    return {'engine': 'Unicorn', 'cases': sum(counts.values()), 'nativeAndRecompiledCalls': calls, 'counts': counts, 'testedFunctions': sorted(touched), 'instructionLimitPerCall': 100000, 'elapsedSecondsLimit': 1, 'returnPcVerified': True, 'independentExpectedControlAndBufferEffects': True, 'dispatchTables': {name: [hex(value) for value in values] for name, values in table_values.items()}, 'platformStubs': {hex(address): role for address, role in platform.items()}, 'observations': ['Payload0x70D0 and page size0x100 produce stride0x7100 and two blocks for capacity0x10000.', 'Zero byte count selects configured payload length; physical offset is index times stride.', 'Asynchronous write accepts counts larger than one payload, while synchronous operations and asynchronous read reject them.', 'Asynchronous dispatch results are ignored by the wrapper; completion status is checked separately.'], 'limitations': ['The platform lock/completion providers and dispatch destinations are isolated stubs; hardware timing and device authenticity are untested.', 'Synthetic division-by-zero and overflow cases record native helper behavior, not a legal save-device configuration.', 'The unmatched lock draft, when absent from the accepted set, remains a native dependency of other source-matched functions.']}

def assert_lock_trace(trace, active, identifier, role):
    if len(trace) != int(active) or active and (trace[0]['role'] != role or trace[0]['arguments'][0] != identifier):
        raise AssertionError(('Lock trace differs', trace))

def assert_dispatch(trace, accepted, name, address, index, length, initially_locked):
    dispatch = [row for row in trace if row['role'] == 'dispatch']
    if len(dispatch) != int(accepted):
        raise AssertionError(('Dispatch count', trace))
    if not accepted:
        if trace:
            raise AssertionError('Rejected request reached a platform provider')
        return
    row = dispatch[0]
    if row['address'] != address or row['arguments'][:3] != [(index * 0x7100) & 0xffffffff, BUFFER, length] or row['lockedDuringCall'] != 1:
        raise AssertionError(('Dispatch request differs', row))
    if name.endswith('_async') and (row['arguments'][3] != 0x11223344 or row['fifth'] != 0x55667788):
        raise AssertionError('Async arguments differ')
    expected_roles = ([] if initially_locked else ['lock']) + ['dispatch'] + ([] if name.endswith('_async') else ['unlock'])
    if [row['role'] for row in trace] != expected_roles:
        raise AssertionError(('Dispatch lock lifecycle differs', trace, expected_roles))
