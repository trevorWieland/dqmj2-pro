import bisect
import hashlib
import random
import struct

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from ov001_award_fixture_20261029 import functions

ADDRESS, ACTOR, RECORD, RNG = 0x021D9A04, 0x02320000, 0x02330000, 0x020F6044
STACK, STOP = 0x03010000, 0x07000000


def short(value):
    return (value + 0x8000) % 0x10000 - 0x8000


def divide(value, denominator):
    return abs(value) // abs(denominator) * (-1 if (value < 0) != (denominator < 0) else 1)


def vectors():
    for index in range(280):
        yield {'ordinal': index, 'traitsMask': index % 256, 'supplied': index >= 256,
               'rngState': ([0, 1, 0xFFFFFFFF, 0x80000000, 0x12345678, 0x7FFFFFFF][index % 6] ^ (index * 0x9E3779B9)) & 0xFFFFFFFF,
               'machineSeed': 202610319904 + index}


def initial(vector):
    rng = random.Random(vector['machineSeed'] ^ 0x58)
    actor, record = bytearray(rng.randbytes(0x440)), bytearray(rng.randbytes(0x210))
    struct.pack_into('<I', actor, 0x1E8, RECORD + 4)
    actor[0x1EC:0x20C] = bytes(32)
    values = [0, 1, 10, 100, 9999]
    index = vector['ordinal']
    base = [values[(index + shift) % len(values)] for shift in range(6)]
    hp = 0 if index % 3 == 0 else base[0] // 2 if base[0] else 1
    mp = base[1] // 2 if base[1] else 1
    stats = [base[0], base[1], hp, mp, *base[2:]]
    struct.pack_into('<8h', actor, 0x1EC, *stats)
    record[0x202] = int(vector['supplied'])
    record[0x4A:0x8A] = bytes(64)
    traits = [0x4F + number for number in range(8) if vector['traitsMask'] & (1 << number)]
    record[0x4A:0x4A + len(traits)] = bytes(traits)
    return bytes(actor), bytes(record), base, hp, mp


def model(actor, record, base, hp, mp, vector):
    output, state, draws = bytearray(actor), vector['rngState'], []
    if vector['supplied']:
        output[0x21C:0x22C] = record[0x1B4:0x1C4]
        return bytes(output), state, RECORD + 0x1C4, draws
    delta = [0] * 8
    for number in range(6):
        if vector['traitsMask'] & (1 << number):
            before = state
            state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
            value = (state >> 16) % base[number] if base[number] > 0 else 0
            draws.append({'bound': base[number], 'stateBefore': before, 'stateAfter': state, 'value': value})
            delta[number] = short(value - divide(base[number], 2))
    if vector['traitsMask'] & 64:
        delta[0] = short(delta[0] + short(divide(min(base[0] + delta[0], 9999), 2)))
        delta[3], delta[2] = short(1 - base[3]), short(1 - base[2])
    if vector['traitsMask'] & 128:
        delta[1] = short(delta[1] + short(divide(min(base[1] + delta[1], 9999), 2)))
        delta[2], delta[5] = short(1 - base[2]), short(1 - base[5])
    output[0x21C:0x22C] = struct.pack('<8h', *delta)
    if hp:
        final_hp = 0 if base[0] == 0 else max(1, divide(hp * min(base[0] + delta[0], 9999), base[0]))
        struct.pack_into('<h', output, 0x1F0, short(final_hp))
    final_mp = 0 if base[1] == 0 else divide(mp * min(base[1] + delta[1], 9999), base[1])
    struct.pack_into('<h', output, 0x1F2, short(final_mp))
    return bytes(output), state, final_mp & 0xFFFFFFFF, draws


def execute(main, overlay, code, native_code, blobs, vector):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ADDRESS, code)
    for name, address, pointer in [('ItemTbl.bin', 0x02300000, 0x021C2AB4),
                                    ('EquipTbl.bin', 0x02340000, 0x021C6BF4),
                                    ('EnmyKindTbl.bin', 0x02350000, 0x020F69F0)]:
        machine.mem_write(address, blobs[name][8:])
        machine.mem_write(pointer, struct.pack('<I', address))
    machine.mem_write(0x020F69E4, bytes(4))
    machine.mem_write(RNG, struct.pack('<I', vector['rngState']))
    actor, record, base, hp, mp = initial(vector)
    machine.mem_write(ACTOR, actor)
    machine.mem_write(RECORD, record)
    rng = random.Random(vector['machineSeed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[:2] = [RECORD, ACTOR]
    for index, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    output, state, expected, draws = model(actor, record, base, hp, mp, vector)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_ram[ACTOR - 0x02000000:ACTOR - 0x02000000 + len(output)] = output
    struct.pack_into('<I', expected_ram, RNG - 0x02000000, state)
    starts, ranges = functions()
    seen, cache, pending, observed = set(), {}, [], []
    trace, writes = hashlib.sha256(), hashlib.sha256()
    counts = {'instructions': 0, 'writes': 0}

    def step(engine, pc, size, unused):
        counts['instructions'] += 1
        trace.update(struct.pack('<I', pc))
        if pc not in cache:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Stat initializer escaped native inventory', hex(pc)))
            cache[pc] = ranges[index]
        entry = cache[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Stat initializer entered incorrect native mode')
        seen.add(entry)
        if pending and pc == pending[0]:
            expected_draw = draws[len(observed)]
            if engine.reg_read(UC_ARM_REG_R0) != expected_draw['value'] or struct.unpack('<I', engine.mem_read(RNG, 4))[0] != expected_draw['stateAfter']:
                raise ValueError('Native stat RNG result/state differs from independent LCG model')
            observed.append(expected_draw)
            pending.clear()
        if pc == 0x0203D294:
            if len(observed) >= len(draws) or pending:
                raise ValueError('Native stat initializer made unexpected RNG calls')
            draw = draws[len(observed)]
            if engine.reg_read(UC_ARM_REG_R0) != draw['bound'] or struct.unpack('<I', engine.mem_read(RNG, 4))[0] != draw['stateBefore']:
                raise ValueError('Native stat RNG bound/order differs from independent model')
            pending.append(engine.reg_read(UC_ARM_REG_LR))

    def write(engine, access, address, size, value, unused):
        allowed = STACK <= address < address + size <= STACK + 0x10000
        allowed |= ACTOR + 0x21C <= address < address + size <= ACTOR + 0x22C
        allowed |= ACTOR + 0x1F0 <= address < address + size <= ACTOR + 0x1F4
        allowed |= address == RNG and size == 4
        if not allowed:
            raise ValueError(('Stat initializer wrote outside declared effects', hex(address)))
        counts['writes'] += 1
        writes.update(struct.pack('<IIQ', address, size, value & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ADDRESS, STOP, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError('Stat initializer did not actually return within bound')
    if machine.reg_read(UC_ARM_REG_R0) != expected or pending or observed != draws:
        raise ValueError(('Stat initializer physical R0/draw completion differs', vector, expected, machine.reg_read(UC_ARM_REG_R0)))
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError('Stat initializer damaged preserved registers')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram):
        actual = bytes(machine.mem_read(ACTOR, len(actor)))
        raise ValueError(('Stat initializer independent effects differ', vector,
                          [(hex(i), value, actual[i]) for i, value in enumerate(output) if actual[i] != value][:32]))
    normalized = bytearray(ram)
    normalized[ADDRESS - 0x02000000:ADDRESS - 0x02000000 + len(native_code)] = native_code
    return {'actualReturn': True, 'vector': vector, 'physicalR0': hex(expected),
            'semanticReturnMeaningEstablished': False, 'rngFinal': state, 'independentDraws': draws,
            'finalModifierWords': list(struct.unpack_from('<8h', output, 0x21C)),
            'finalCurrentHpMp': list(struct.unpack_from('<2h', output, 0x1F0)), **counts,
            'nativeEntries': [[hex(start), end - start, module, mode] for start, end, module, mode in sorted(seen)],
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'wholeRamWithOnlyKnownCallerCodeNormalizedSha256': hashlib.sha256(normalized).hexdigest(),
            'wholeStackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'pcTraceSha256': trace.hexdigest(), 'writeTraceSha256': writes.hexdigest()}
