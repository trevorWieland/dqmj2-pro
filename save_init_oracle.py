import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

CONTROL = 0x020edcf0
FRAME = 0x020edc00
DEVICE = 0x020dd4b8
STOP = 0x027ff800

def validate(arm, save, matches, root):
    machines = []
    context = {}
    touched = set()
    calls = 0
    cases = 0
    boundaries = {0x02010294: 'busy', 0x02011194: 'wait', 0x020060e4: 'allocate-lock', 0x020102fc: 'lock', 0x0201030c: 'unlock', 0x020109cc: 'configure', 0x02010990: 'capacity', 0x020109b8: 'page-size'}
    table = [struct.unpack_from('<I', arm, 0xd9044 + index * 4)[0] for index in range(6)]

    def boundary(machine, address, size, user):
        role = boundaries[address]
        argument = machine.reg_read(UC_ARM_REG_R0)
        context['trace'].append((role, argument))
        result = context.get(role, 0)
        machine.reg_write(UC_ARM_REG_R0, result & 0xffffffff)
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

    def check(name, frame, device, expected_frame, expected_device, first, expected_result, settings, expected_roles, expected_arguments):
        nonlocal cases, calls
        if name not in matches:
            return
        address = int(matches[name][0]['address'], 16)
        for machine in machines:
            context.clear()
            context.update(settings)
            context['trace'] = []
            machine.mem_write(FRAME, bytes(frame))
            machine.mem_write(DEVICE, bytes(device))
            machine.reg_write(UC_ARM_REG_R0, first & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(address, STOP, count=100000)
            if time.monotonic() - began > 1 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                raise AssertionError('Backup initialization exceeded execution bounds')
            if bytes(machine.mem_read(FRAME, len(frame))) != expected_frame or bytes(machine.mem_read(DEVICE, len(device))) != expected_device or machine.reg_read(UC_ARM_REG_R0) != expected_result:
                raise AssertionError((name, first, 'RAM or return differs'))
            if [role for role, argument in context['trace']] != expected_roles:
                raise AssertionError(('Platform sequence differs', context['trace'], expected_roles))
            for role, expected in expected_arguments.items():
                seen = [argument for name, argument in context['trace'] if name == role]
                if seen != expected:
                    raise AssertionError(('Platform arguments differ', role, seen, expected))
            calls += 1
        cases += 1
        touched.add(name)

    rng = random.Random(20261027)
    offset = CONTROL - FRAME
    for lock_id in [-3, 0, 1, 0x1234abcd, -1]:
        for locked in [0, 1, 255]:
            for device_type in range(6):
                for configure in [0, 1, 7]:
                    for capacity, page_size in [(0x10000, 0x100), (0x20000, 0x200), (0xffffffff, 0)]:
                        frame = bytearray(rng.randbytes(0x200))
                        frame[offset] = 0x55
                        frame[offset + 1] = locked
                        device = bytearray(struct.pack('<BBBBI', 255, 0x12, 0x34, 0x56, lock_id & 0xffffffff))
                        expected_frame = bytearray(frame)
                        expected_device = bytearray(device)
                        if lock_id == -3:
                            expected_frame[offset] = 2
                            roles = []
                            arguments = {}
                        else:
                            expected_frame[offset] = 0 if configure else 3
                            expected_frame[offset + 1] = 0
                            roles = ([] if locked else ['lock']) + ['configure'] + (['capacity', 'page-size'] if configure else []) + ['unlock']
                            arguments = {'configure': [table[device_type]], 'unlock': [lock_id & 0xffff]}
                            if not locked:
                                arguments['lock'] = [lock_id & 0xffff]
                            if configure:
                                expected_device[0] = device_type
                                struct.pack_into('<I', expected_frame, offset + 0x18, capacity)
                                struct.pack_into('<I', expected_frame, offset + 0x10, page_size)
                        settings = {'configure': configure, 'capacity': capacity, 'page-size': page_size}
                        check('save_device_type_set', frame, device, expected_frame, expected_device, device_type, int(lock_id != -3 and bool(configure)), settings, roles, arguments)
    for initialized in [0, 1, 127, 128, 255]:
        for busy in [0, 1, 7]:
            for lock_id in [-3, 0, 1, 0x1234abcd, -1]:
                frame = bytearray(rng.randbytes(0x200))
                frame[offset] = 0x55
                frame[offset + 2] = initialized
                device = rng.randbytes(8)
                expected_frame = bytearray(frame)
                expected_device = bytearray(device)
                roles = []
                if initialized:
                    expected_frame[offset] = 12
                    expected_result = 0
                else:
                    expected_frame[offset + 1] = 0
                    roles = ['busy'] + (['wait'] if busy else []) + ['allocate-lock']
                    struct.pack_into('<I', expected_device, 4, lock_id & 0xffffffff)
                    expected_result = int(lock_id != -3)
                    if lock_id == -3:
                        expected_frame[offset] = 1
                    else:
                        expected_frame[offset] = 0
                        expected_frame[offset + 2] = 1
                        expected_frame[offset + 4:offset + 28] = bytes(24)
                        expected_device[0] = 255
                check('save_device_initialize', frame, device, expected_frame, expected_device, 0, expected_result, {'busy': busy, 'allocate-lock': lock_id}, roles, {})
    if touched != set(matches):
        raise AssertionError(('Untested source matches', set(matches) - touched))
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': sorted(touched), 'instructionLimitPerCall': 100000, 'elapsedSecondsLimit': 1, 'returnPcVerified': True, 'independentExpectedControlAndDeviceEffects': True, 'configurationValues': table, 'platformStubs': {hex(address): role for address, role in boundaries.items()}, 'limitations': ['Hardware busy/wait, lock-ID allocation, physical device configuration and capacity/page-size providers are controlled stubs.', 'A byte-level initialization draft is not accepted unless its complete native span matches.', 'No physical backup type is inferred solely from a synthetic configuration value.']}
