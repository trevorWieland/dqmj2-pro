import itertools
import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, u32, put

GLOBAL = 0x020e5500
FIRST = 0x02510080
SECOND = 0x02520080
STOP = 0x027ff800
FILL = 0x02008d78

def expected(original, raw_type, redirected):
    memory = {address: bytearray(data) for address, data in original.items()}
    descriptor = u32(memory, GLOBAL)
    write(memory, descriptor + 0x18, bytes(0x48))
    if redirected:
        put(memory, GLOBAL, SECOND)
    put(memory, descriptor + 4, raw_type)
    put(memory, descriptor + 0x58, 0x203f)
    if raw_type == 0:
        return memory
    exponent = (raw_type >> 8) & 255
    capacity = 1 << exponent if exponent < 32 else 0
    category = raw_type & 255
    subtype = (raw_type >> 16) & 255
    put(memory, descriptor + 0x18, capacity)
    write(memory, descriptor + 0x54, b'\xff')
    values = None
    byte54 = 255
    flags = 0x203f
    if category == 1:
        entries = {0x200: (16, 1, 5, 240), 0x2000: (32, 2, 5, 0), 0x10000: (128, 2, 10, 0), 0x20000: (256, 3, 5, 0)}
        if capacity in entries:
            page, width, pause, byte54 = entries[capacity]
            values = {0x24: page, 0x28: width, 0x2c: pause, 0x1c: page}
            flags |= 0x4340
    elif category == 2:
        entries = {
            0x40000: ({0x30: 25, 0x34: 300, 0x50: 300, 0x40: 5000}, 255, 0x480),
            0x80000: ({0x30: 25, 0x34: 300, 0x50: 300, 0x40: 5000}, 255, 0x480),
            0x100000: ({0x30: 25, 0x34: 300, 0x50: 300, 0x40: 5000}, 255, 0x480),
            0x200000: ({0x30: 23, 0x34: 300, 0x40: 500, 0x44: 5000, 0x38: 10000, 0x3c: 60000}, 0, 0x5480),
            0x400000: ({0x40: 600, 0x44: 3000, 0x48: 70, 0x4c: 150, 0x38: 23000, 0x3c: 800000, 0x20: 4096}, 0, 0xd000)
        }
        if capacity in entries:
            values, byte54, extra = entries[capacity]
            values = dict(values)
            flags |= extra
        elif capacity == 0x800000:
            values = {}
            if subtype in (0, 1):
                values = {0x40: 1000, 0x44: 3000, 0x38: 68000, 0x3c: 160000}
                byte54 = 0x84 if subtype else 0
                flags |= 0x5000
        if values is not None:
            values.update({0x1c: 65536, 0x24: 256, 0x28: 3, 0x2c: 5})
            flags |= 0xb40
    elif category == 3 and capacity in (0x2000, 0x8000):
        values = {0x24: capacity, 0x1c: capacity, 0x28: 2}
        byte54 = 0
        flags |= 0x4340
    if values is None:
        put(memory, descriptor + 4, 0)
        put(memory, descriptor + 0x18, 0)
        put(memory, u32(memory, GLOBAL), 3)
    else:
        for offset, value in values.items():
            put(memory, descriptor + offset, value)
        write(memory, descriptor + 0x54, bytes([byte54]))
        put(memory, descriptor + 0x58, flags)
    return memory

def validate(arm, save, matches, root):
    if 'save_backend_descriptor_select' not in matches:
        return {'cases': 0, 'nativeAndRecompiledCalls': 0, 'limitations': ['Descriptor selection source did not match.']}
    record, code = matches['save_backend_descriptor_select']
    context = {}
    machines = []

    def fill(machine, address, size, user):
        destination, value, count = [machine.reg_read(register) for register in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)]
        if (destination, value, count) != (FIRST + 0x18, 0, 0x48):
            raise AssertionError('Descriptor fill contract differs')
        context['fills'] += 1
        machine.mem_write(destination, bytes([value & 255]) * count)
        if context['redirect']:
            machine.mem_write(GLOBAL, struct.pack('<I', SECOND))
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            machine.mem_write(int(record['address'], 16), code)
        machine.hook_add(UC_HOOK_CODE, fill, begin=FILL, end=FILL)
        machines.append(machine)
    rng = random.Random(20261027)
    exponents = [0, 8, 9, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 31, 32, 33, 255]
    vectors = [(category | (exponent << 8) | (subtype << 16) | high, redirect) for category, exponent, subtype, high, redirect in itertools.product([0, 1, 2, 3, 255], exponents, [0, 1, 2, 255], [0, 0xff000000], [False, True])]
    vectors += [(rng.getrandbits(32), bool(index & 1)) for index in range(512)]
    calls = 0
    for raw_type, redirect in vectors:
        original = {0x020e5400: bytearray(rng.randbytes(0x1000)), 0x02510000: bytearray(rng.randbytes(0x1000)), 0x02520000: bytearray(rng.randbytes(0x1000))}
        put(original, GLOBAL, FIRST)
        reference = expected(original, raw_type, redirect)
        for machine in machines:
            for address, data in original.items():
                machine.mem_write(address, bytes(data))
            context.update({'redirect': redirect, 'fills': 0})
            machine.reg_write(UC_ARM_REG_R0, raw_type)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(int(record['address'], 16), STOP, count=100000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or context['fills'] != 1:
                raise AssertionError(('Descriptor bounds/fill count', hex(raw_type)))
            for address, data in reference.items():
                actual = bytes(machine.mem_read(address, len(data)))
                if actual != data:
                    differences = [(hex(address + index), actual[index], value) for index, value in enumerate(data) if actual[index] != value]
                    raise AssertionError(('Descriptor RAM differs', hex(raw_type), redirect, differences[:8]))
            calls += 1
    return {'engine': 'Unicorn', 'cases': len(vectors), 'nativeAndRecompiledCalls': calls, 'testedFunctions': ['save_backend_descriptor_select'], 'instructionLimitPerCall': 100000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedDescriptorAndGuardRam': True, 'platformStubs': {hex(FILL): 'byte-fill'}, 'observations': ['Type zero clears descriptor0x18..0x60 and writes type/flags while preserving prior status.', 'Type encoding uses category low byte, capacity exponent byte1 and subtype byte2; accepted category/capacity branches are recorded without hardware-model names.', 'Unsupported categories/capacities zero the selected descriptor type/capacity and set current global descriptor status3.', 'Category2 capacity0x800000 accepts other subtypes without populating subtype-specific parameters.', 'A fill-provider global-pointer mutation verifies the cached descriptor initialization and current-global status write are distinct.'], 'limitations': ['Byte fill is a controlled provider; all selection/branch/store logic executes natively and recompiled.', 'Exponent values32..255 are isolated ARM machine-behavior probes; the corresponding C shift has no portable language-level meaning and is not a legal device-type claim.', 'No physical device detection, actual configuration handshake or hardware-model identity is established.']}
