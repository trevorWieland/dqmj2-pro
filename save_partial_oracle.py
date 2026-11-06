import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC

START = 0x021b9000
LENGTH = 0x10000
MAIN = 0x021bd51c
IO = 0x021c6bfc
BUFFER = 0x02500000
STOP = 0x027ff800
PARTS = [(0x90, 0x3a68, MAIN), (0x3a68, 0x3a9c, 0x021b9eb4), (0x3a9c, 0x5d40, 0x021bb278), (0x5d40, 0x70d0, 0x021b9ee8)]

def io_bytes(status=0x55, heap=2, pointer=0):
    return struct.pack('<BBHII', status, heap & 255, 0x1234, 0x0207dac8, pointer)

def set_io(state, status=0x55, heap=2, pointer=0):
    result = bytearray(state)
    result[IO - START:IO - START + 12] = io_bytes(status, heap, pointer)
    return result

def copy_sections(state, bank, partial=False):
    result = bytearray(state)
    for begin, end, destination in PARTS[:1] if partial else PARTS:
        result[destination - START:destination - START + end - begin] = bank[begin:end]
    return result

def validate(arm, save, matches, root):
    machines = []
    context = {}
    calls = 0
    counts = {}
    touched = set()
    boundaries = {0x0202a37c: 'allocate', 0x0202a498: 'free', 0x02027d8c: 'read', 0x02027c44: 'write', 0x02027e44: 'read-async', 0x02027ef4: 'poll', 0x020c225c: 'error-present'}

    def hook(machine, address, size, user):
        role = boundaries[address]
        arguments = [machine.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)]
        row = {'role': role, 'arguments': arguments}
        result = 0
        if role == 'allocate':
            result = BUFFER if context.get('allocate', True) else 0
        elif role == 'read':
            result = int(context.get('read', True))
            if result:
                length = arguments[2] or 0x70d0
                machine.mem_write(arguments[1], context['bank'][:length])
        elif role == 'read-async':
            result = int(context.get('async-start', True))
        elif role == 'poll':
            machine.mem_write(arguments[0], bytes([context.get('error', 0)]))
            result = int(context.get('complete', True))
        elif role == 'write':
            row['data'] = bytes(machine.mem_read(arguments[1], arguments[2]))
            result = int(context.get('write', True))
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

    def check(name, state, expected, first=0, second=0, returned=None, settings=None, expected_errors=(), invalidate=False, expected_bank=None):
        nonlocal calls
        if name not in matches:
            return
        address = int(matches[name][0]['address'], 16)
        for machine in machines:
            context.clear()
            context.update(settings or {})
            context['trace'] = []
            machine.mem_write(START, bytes(state))
            initial_buffer = context.get('buffer', bytes([0xa5]) * 0x10000)
            machine.mem_write(BUFFER, initial_buffer)
            machine.reg_write(UC_ARM_REG_R0, first & 0xffffffff)
            machine.reg_write(UC_ARM_REG_R1, second & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(address, STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                raise AssertionError((name, 'execution bounds'))
            actual = bytes(machine.mem_read(START, LENGTH))
            if actual != expected:
                differences = [(hex(START + i), a, b) for i, (a, b) in enumerate(zip(actual, expected)) if a != b]
                raise AssertionError((name, 'RAM effect differs', differences[:8]))
            if returned is not None and machine.reg_read(UC_ARM_REG_R0) != returned & 0xffffffff:
                raise AssertionError((name, 'Return differs'))
            errors = [row['arguments'][0] for row in context['trace'] if row['role'] == 'error-present']
            if errors != list(expected_errors):
                raise AssertionError((name, 'Error presentation differs', errors, expected_errors))
            writes = [row for row in context['trace'] if row['role'] == 'write']
            if len(writes) != int(invalidate) or writes and (writes[0]['arguments'][0] != 0 or writes[0]['arguments'][2] != 0x90 or writes[0]['data'] != bytes(0x90)):
                raise AssertionError((name, 'Header invalidation differs'))
            if expected_bank is not None and bytes(machine.mem_read(BUFFER, len(expected_bank))) != expected_bank:
                raise AssertionError((name, 'Bank buffer differs'))
            calls += 1
        counts[name] = counts.get(name, 0) + 1
        touched.add(name)

    rng = random.Random(20261027)
    banks = [('valid', save[:0x7100], 0)]
    for label, offset, status in [('marker', 0, 3), ('length', 4, 4), ('payload-length', 8, 7), ('payload-sum', 0x88, 6), ('header-sum', 0x8c, 5)]:
        bank = bytearray(save[:0x7100])
        bank[offset] ^= 1
        banks.append((label, bytes(bank), status))
    for label, bank, bank_status in banks:
        for allocate in (False, True):
            for read in (False, True):
                state = set_io(rng.randbytes(LENGTH))
                loaded = allocate and read and not bank_status
                status = 0x55 if not allocate else 2 if not read else bank_status
                settings = {'allocate': allocate, 'read': read, 'bank': bank}
                expected_buffer = bank[:0x70d0] + bytes([0xa5]) * (0x10000 - 0x70d0) if allocate and read else bytes([0xa5]) * 0x10000
                for heap in [-1, 2, 9]:
                    expected = copy_sections(state, bank, partial=True) if loaded else bytearray(state)
                    expected = set_io(expected, status)
                    check('save_reload_main', state, expected, 1, heap, returned=int(loaded), settings=settings, expected_bank=expected_buffer)
                expected = copy_sections(state, bank, partial=True) if loaded else bytearray(state)
                metadata_start = MAIN - START + 8
                expected[metadata_start:metadata_start + 0x14] = state[metadata_start:metadata_start + 0x14]
                expected = set_io(expected, status)
                errors = [] if loaded else [0x20000000 if status == 2 else 0x60000000]
                check('save_reload_preserving_metadata', state, expected, settings=settings, expected_errors=errors)
                expected = copy_sections(state, bank) if loaded else bytearray(state)
                expected = set_io(expected, status)
                errors = [] if loaded else [0x50000000 if status == 2 else 0x60000000]
                check('save_load_primary_checked', state, expected, settings=settings, expected_errors=errors)
    state = set_io(rng.randbytes(LENGTH))
    check('save_main_metadata_pointer', state, state, returned=MAIN + 8)
    for allocate in (False, True):
        for start in (False, True):
            for heap in [-1, 2, 9, 127, 255]:
                expected = set_io(state, 8 if not allocate else 0 if start else 2, heap if allocate else 2, BUFFER if allocate and start else 0)
                check('save_load_primary_async_checked', state, expected, heap, settings={'allocate': allocate, 'async-start': start}, expected_errors=[] if allocate and start else [0x50000000])
    for write in (False, True):
        expected = set_io(state, 0 if write else 1)
        check('save_header_invalidate_again', state, expected, settings={'write': write}, returned=int(write), invalidate=True)
    for label, bank, status in banks:
        for complete in (False, True):
            for error in (0, 1, 255):
                for has_buffer in (False, True):
                    for write in (False, True):
                        state = set_io(rng.randbytes(LENGTH), pointer=BUFFER if has_buffer else 0)
                        loaded = complete and not error and has_buffer and not status
                        invalidate = complete and not error and (not has_buffer or bool(status))
                        current_status = 0 if not complete else 2 if error else status if has_buffer else 8
                        if invalidate:
                            current_status = 0 if write else 1
                        pointer = BUFFER if has_buffer and (not complete or error) else 0
                        expected = copy_sections(state, bank) if loaded else bytearray(state)
                        expected = set_io(expected, current_status, pointer=pointer)
                        errors = [] if not complete or loaded else [0x50000000 if error else 0x60000000]
                        settings = {'complete': complete, 'error': error, 'write': write, 'buffer': bank + bytes(0x10000 - len(bank))}
                        check('save_load_poll_checked', state, expected, returned=int(complete), settings=settings, expected_errors=errors, invalidate=invalidate)
    if touched != set(matches):
        raise AssertionError(('Untested source matches', set(matches) - touched))
    return {'engine': 'Unicorn', 'cases': sum(counts.values()), 'nativeAndRecompiledCalls': calls, 'counts': counts, 'testedFunctions': sorted(touched), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedRamAndErrorEffects': True, 'boundaryStubs': {hex(address): role for address, role in boundaries.items()}, 'observations': ['The partial loader replaces only the0x39D8-byte main section after validating the entire bank.', 'The preserving wrapper retains exactly20 main-state bytes at RAM0x021BD524 across reload.', 'The checked completion wrapper invalidates primary header bytes for validation failures outside the device-read-error case.', 'Header invalidation and error presentation here affect only simulated requests and RAM, never ordinary save files.'], 'limitations': ['Allocation, device I/O/completion and error presentation are controlled providers; visible failure UI and nonreturning presentation paths are not executed.', 'The preserved20-byte region has no newly asserted text or player-identity semantics.', 'Allocation-failure status preservation and retained async-error buffers are native behavior within this bounded path; wider cleanup is not established.']}
