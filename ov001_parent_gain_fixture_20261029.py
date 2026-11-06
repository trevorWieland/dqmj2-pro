import bisect
import hashlib
import random
import struct

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from ov001_award_fixture_20261029 import functions

ADDRESS, ABILITY, STACK, STOP = 0x021E409C, 0x02410000, 0x03010000, 0x07000000


def vectors():
    index = 0
    for present in range(4):
        for first_variant in range(3):
            for second_variant in range(3):
                for level in (1, 10, 11, 40, 50, 51, 100):
                    for missing_table in (False, True):
                        yield {'seed': 202610304096 + index, 'present': present,
                               'variants': [first_variant, second_variant], 'level': level,
                               'curves': [index % 33, index * 7 % 33], 'missingTable': missing_table}
                        index += 1


def truncate(value, denominator):
    return (abs(value) // denominator) * (-1 if value < 0 else 1)


def model(ability, vector):
    total = 0
    for index in range(2):
        if vector['present'] & (1 << index):
            value = -1 if vector['missingTable'] else ability[vector['curves'][index] * 100 + vector['level'] - 1]
            total += truncate(value * (1, 3, 2)[vector['variants'][index]], (1, 2, 1)[vector['variants'][index]])
            total = (total + 0x8000) % 0x10000 - 0x8000
    return truncate(total + 3, 4) & 0xFFFFFFFF


def execute(main, overlay, code, ability, vector):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for start, length in ((0x02000000, 0x800000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(start, length)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ADDRESS, code)
    machine.mem_write(ABILITY, ability)
    machine.mem_write(0x02238D58, struct.pack('<I', 0 if vector['missingTable'] else ABILITY))
    rng = random.Random(vector['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[:4] = [int(bool(vector['present'] & 1)), int(bool(vector['present'] & 2)), *vector['variants']]
    for index, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    initial_sp = STACK + 0xFFF0
    machine.mem_write(initial_sp, struct.pack('<3I', *vector['curves'], vector['level']))
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, initial_sp)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    initial_ram = bytes(machine.mem_read(0x02000000, 0x800000))
    starts, ranges = functions()
    seen, cache = set(), {}
    trace, writes = hashlib.sha256(), hashlib.sha256()
    counts = {'instructions': 0, 'writes': 0}

    def step(engine, pc, size, unused):
        counts['instructions'] += 1
        trace.update(struct.pack('<I', pc))
        if pc not in cache:
            position = bisect.bisect_right(starts, pc) - 1
            if position < 0 or not ranges[position][0] <= pc < ranges[position][1]:
                raise ValueError('Parent gain escaped qualified native inventory')
            cache[pc] = ranges[position]
        entry = cache[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Parent gain entered wrong native mode')
        seen.add(entry)

    def write(engine, access, destination, size, value, unused):
        if not STACK <= destination < destination + size <= STACK + 0x10000:
            raise ValueError('Pure parent gain wrote outside stack')
        counts['writes'] += 1
        writes.update(struct.pack('<IIQ', destination, size, value & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ADDRESS, STOP, count=10000)
    expected = model(ability, vector)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != initial_sp:
        raise ValueError('Parent gain did not return within bound')
    if machine.reg_read(UC_ARM_REG_R0) != expected:
        raise ValueError(('Parent gain differs from independent signed/narrowing model', vector, expected))
    if any(machine.reg_read(UC_ARM_REG_R0 + index) != registers[index] for index in range(4, 12)):
        raise ValueError('Parent gain damaged preserved registers')
    ram = bytes(machine.mem_read(0x02000000, 0x800000))
    if ram != initial_ram:
        raise ValueError('Pure parent gain changed RAM')
    return {'actualReturn': True, 'vector': vector, 'return': expected, **counts,
            'nativeEntries': [[hex(start), end - start, module, mode] for start, end, module, mode in sorted(seen)],
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'wholeRamSha256': hashlib.sha256(ram).hexdigest(),
            'wholeStackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'pcTraceSha256': trace.hexdigest(), 'writeTraceSha256': writes.hexdigest()}
