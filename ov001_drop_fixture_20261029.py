import bisect
import hashlib
import random
import struct

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from ov001_award_fixture_20261029 import functions

ADDRESS, ACTOR, DATA, RNG, STACK, STOP = 0x021E3EEC, 0x02310000, 0x02311000, 0x020F6044, 0x03010000, 0x07000000


def vectors():
    rates = [0, 1, 2, 3, 4, 5, 6, 7, 8, 255]
    for index in range(256):
        yield {'ordinal': index, 'machineSeed': 202610303396 + index,
               'rngState': ([0, 1, 0xFFFFFFFF, 0x80000000, 0x12345678, 0x7FFFFFFF][index % 6] ^ (index * 0x9E3779B9)) & 0xFFFFFFFF,
               'mode': [0, 1, 0xFFFFFFFF][(index + index // 100) % 3],
               'firstRate': rates[index % 10], 'secondRate': rates[(index // 10 + index * 3) % 10],
               'firstItem': 0 if index % 11 == 0 else [7, 90, 65535][index % 3],
               'secondItem': 0 if index % 13 == 0 else [1, 700, 65535][index % 3],
               'suppressed': index % 17 == 0, 'bonusActors': index // 7 % 4,
               'forceSecond': index // 2 % 2 == 1}


def model(vector):
    state, draws = vector['rngState'], []

    def attempt(rate, first):
        nonlocal state
        if vector['mode'] == 0:
            for unused in range(vector['bonusActors']):
                if 2 <= rate <= 6:
                    rate -= 1
        if rate == 0:
            result = 255 if vector['mode'] else 0
        elif 1 <= rate <= 6:
            bound = 1 << (rate + 2)
            before = state
            state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
            result = (state >> 16) % bound
            draws.append({'bound': bound, 'stateBefore': before, 'stateAfter': state, 'value': result})
        else:
            result = 1
        if vector['mode']:
            return result < 4
        return result == 0 or not first and vector['forceSecond']

    selected = 0
    if not vector['suppressed']:
        if vector['firstItem'] and attempt(vector['firstRate'], True):
            selected = vector['firstItem']
        elif vector['secondItem'] and attempt(vector['secondRate'], False):
            selected = vector['secondItem']
    return selected, state, draws


def execute(main, overlay, code, vector):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base, size in ((0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(base, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ADDRESS, code)
    actor, data = bytearray(0x440), bytearray(0xD0)
    struct.pack_into('<I', actor, 0x1E8, DATA)
    data[0xB1] = int(vector['suppressed'])
    struct.pack_into('<HB', data, 0xC6, vector['firstItem'], vector['firstRate'])
    struct.pack_into('<HB', data, 0xCA, vector['secondItem'], vector['secondRate'])
    machine.mem_write(ACTOR, bytes(actor))
    machine.mem_write(DATA, bytes(data))
    for index in range(3):
        actor, data = bytearray(0x440), bytearray(0xB0)
        data_address = 0x02312000 + index * 0x100
        struct.pack_into('<I', actor, 0x1E8, data_address)
        actor[0x31C] = 1
        data[0x46] = 0x36 if index < vector['bonusActors'] else 0
        machine.mem_write(0x02236F6C + index * 0x440, bytes(actor))
        machine.mem_write(data_address, bytes(data))
    machine.mem_write(RNG, struct.pack('<I', vector['rngState']))
    machine.mem_write(0x020F69E4, struct.pack('<I', 0x20000 if vector['forceSecond'] else 0))
    rng = random.Random(vector['machineSeed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[:2] = [ACTOR, vector['mode']]
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for index, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    initial = bytes(machine.mem_read(0x02000000, 0x400000))
    result, state, draws = model(vector)
    expected_ram = bytearray(initial)
    struct.pack_into('<I', expected_ram, RNG - 0x02000000, state)
    starts, ranges = functions()
    seen, cache, observed = set(), {}, []
    trace, writes = hashlib.sha256(), hashlib.sha256()
    counts = {'instructions': 0, 'writes': 0}

    def step(engine, pc, size, unused):
        counts['instructions'] += 1
        trace.update(struct.pack('<I', pc))
        if pc not in cache:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Drop selector escaped native inventory', hex(pc)))
            cache[pc] = ranges[index]
        entry = cache[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Drop selector entered wrong native mode')
        seen.add(entry)
        if pc == 0x0203D294:
            observed.append({'bound': engine.reg_read(UC_ARM_REG_R0), 'stateBefore': struct.unpack('<I', engine.mem_read(RNG, 4))[0]})

    def write(engine, access, destination, size, value, unused):
        if not (STACK <= destination < destination + size <= STACK + 0x10000 or destination == RNG and size == 4):
            raise ValueError('Drop selector wrote outside stack/RNG word')
        counts['writes'] += 1
        writes.update(struct.pack('<IIQ', destination, size, value & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ADDRESS, STOP, count=20000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError('Drop selector did not actually return within bound')
    if machine.reg_read(UC_ARM_REG_R0) != result:
        raise ValueError(('Drop result differs from independent model', vector, result))
    if observed != [{key: draw[key] for key in ('bound', 'stateBefore')} for draw in draws]:
        raise ValueError(('Native RNG draw order differs', vector, observed, draws))
    if any(machine.reg_read(UC_ARM_REG_R0 + index) != registers[index] for index in range(4, 12)):
        raise ValueError('Drop selector damaged preserved registers')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram):
        raise ValueError('Drop RNG/memory effects differ from independent model')
    return {'actualReturn': True, 'vector': vector, 'return': result, 'rngFinal': state,
            'independentDraws': draws, **counts,
            'nativeEntries': [[hex(start), end - start, module, mode] for start, end, module, mode in sorted(seen)],
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'wholeRamSha256': hashlib.sha256(ram).hexdigest(),
            'wholeStackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'pcTraceSha256': trace.hexdigest(), 'writeTraceSha256': writes.hexdigest()}
