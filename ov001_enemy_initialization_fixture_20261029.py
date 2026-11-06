import bisect
import hashlib
import random
import struct

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from ov001_award_fixture_20261029 import functions

ADDRESS, DESTINATION, ROW, KIND = 0x021E88E4, 0x02320000, 0x02310000, 0x02300000
STACK, STOP, RNG = 0x03010000, 0x07000000, 0x020F6044


def signed(value):
    return (value + 0x80000000) % 0x100000000 - 0x80000000


def truncate(value, denominator):
    return abs(value) // denominator * (-1 if value < 0 else 1)


def scaled(value, factor, width):
    product = signed(value * factor)
    rounded = signed(product + (-2048 if product < 0 else 2048))
    limit = (1 << (width * 8 - 2)) - 1
    return min(truncate(rounded, 4096), limit)


def vectors(enemies):
    count = (len(enemies) - 8) // 100
    for index in range(192):
        enemy_id = index * 47 % count
        row = bytearray(enemies[8 + enemy_id * 100:8 + (enemy_id + 1) * 100])
        if index >= 96:
            for number, offset in enumerate([0x30, 0x32, 0x34, 0x36, 0x38, 0x3A, 0x3C, 0x40, 0x42, 0x44, 0x46, 0x48, 0x4A]):
                struct.pack_into('<h', row, offset, [0, 1, 16383, 16384, 32767, -32768, -1][(index + number) % 7])
            struct.pack_into('<II', row, 0x24, [0, 32767, 65535, 0xFFFFFFFF][index % 4],
                             [0, 65535, 65536, 0x12345678, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF][index % 7])
            row[0x2C] = [0, 1, 63, 64, 100, 255][index % 6]
            for number in range(2):
                struct.pack_into('<HB', row, 0x1C + number * 4, 0 if index % 9 == number else 65535,
                                 [0, 1, 2, 3, 6, 7, 255][(index + number) % 7])
            row[0x63] = 1 if index % 11 == 0 else 0
        yield {'ordinal': index, 'enemyId': enemy_id, 'rawRow': bytes(row).hex(),
               'componentDomain': 'measured-enemy-row' if index < 96 else 'synthetic-width-and-cap-boundaries',
               'negativeIdentityGuard': index % 17 == 0,
               'variant': [0, 0, 1, 2, 255][index % 5],
               'enhancementFlag': index % 4 != 0,
               'rngState': ([0, 1, 0xFFFFFFFF, 0x80000000, 0x12345678, 0x7FFFFFFF][index % 6] ^ (index * 0x9E3779B9)) & 0xFFFFFFFF,
               'machineSeed': 202610308884 + index}


def initial(vector):
    row = bytes.fromhex(vector['rawRow'])
    destination = bytearray(random.Random(vector['machineSeed'] ^ 0xA1).randbytes(0x210))
    struct.pack_into('<i', destination, 0, -1 if vector['negativeIdentityGuard'] else vector['enemyId'])
    destination[0x2E:0x30] = row[:2]
    destination[0x30] = vector['variant']
    return row, bytes(destination)


def model(destination, row, kinds, vector):
    output, state, draws, calls = bytearray(destination), vector['rngState'], [], []
    if vector['negativeIdentityGuard']:
        return bytes(output), state, 0, draws, calls
    for source, target in [(0x30, 0x11C), (0x32, 0x11E), (0x34, 0x124), (0x36, 0x126), (0x38, 0x128), (0x3A, 0x12A),
                           (0x3C, 0x32), (0x40, 0x36), (0x42, 0x38), (0x44, 0x3A), (0x46, 0x3C), (0x48, 0x3E), (0x4A, 0x40)]:
        output[target:target + 2] = row[source:source + 2]
    for source, target, count in [(0x28, 8, 4), (0x24, 0x2C, 2), (0x1C, 0xCA, 8), (0x5E, 0xD2, 4),
                                   (0x2F, 0xAA, 1), (0x2C, 0x12C, 1), (0x58, 0x44, 4)]:
        output[target:target + count] = row[source:source + count]
    if vector['enhancementFlag'] and row[0x63] == 0:
        species = struct.unpack_from('<h', destination, 0x2E)[0]
        variant = output[0x30]
        group = struct.unpack_from('<H', kinds, species * 100 + 4)[0] & 15
        group = (group + variant * 3) & 255
        if variant:
            group = (truncate(group - 1, 3) * 3 + 1) & 255
        if group <= 3:
            before = state
            state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
            value = (state >> 16) % 2
            draws.append({'bound': 2, 'stateBefore': before, 'stateAfter': state, 'value': value})
            if value == 0:
                output[0x30] = (variant + 1) & 255
        factor = 0x1800 if output[0x30] == 0 else 0x2000
        fields = [(offset, factor, 2) for offset in [0x11C, 0x11E, 0x124, 0x126, 0x128, 0x12A]]
        fields += [(0x12C, factor, 1), (8, factor, 4), (0x2C, factor, 2), (0x32, 0x800, 2)]
        fields += [(offset, 0x1000, 2) for offset in [0x36, 0x38, 0x3A, 0x3C, 0x3E, 0x40]]
        for offset, multiplier, width in fields:
            value = output[offset] if width == 1 else struct.unpack_from('<h' if width == 2 else '<i', output, offset)[0]
            result = scaled(value, multiplier, width)
            calls.append({'arguments': [value & 0xFFFFFFFF, multiplier, width], 'expectedReturnBits': hex(result & 0xFFFFFFFF)})
            output[offset:offset + width] = (result & ((1 << (width * 8)) - 1)).to_bytes(width, 'little')
        for offset in [0xCA, 0xCE]:
            if struct.unpack_from('<H', output, offset)[0] and 2 <= output[offset + 2] <= 6:
                output[offset + 2] -= 1
    output[0x120:0x124] = output[0x11C:0x120]
    return bytes(output), state, 1, draws, calls


def execute(main, overlay, code, kinds, vector):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ADDRESS, code)
    machine.mem_write(KIND, kinds)
    machine.mem_write(0x020F69F0, struct.pack('<I', KIND))
    machine.mem_write(0x020F69E4, struct.pack('<I', 8 if vector['enhancementFlag'] else 0))
    machine.mem_write(RNG, struct.pack('<I', vector['rngState']))
    row, destination = initial(vector)
    machine.mem_write(ROW, row)
    machine.mem_write(DESTINATION, destination)
    rng = random.Random(vector['machineSeed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[:2] = [DESTINATION, ROW]
    for index, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    output, state, result, draws, calls = model(destination, row, kinds, vector)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_ram[DESTINATION - 0x02000000:DESTINATION - 0x02000000 + len(output)] = output
    struct.pack_into('<I', expected_ram, RNG - 0x02000000, state)
    starts, ranges = functions()
    seen, cache, observed_draws, observed_calls, observed_returns = set(), {}, [], [], []
    pending_return = []
    trace, writes = hashlib.sha256(), hashlib.sha256()
    counts = {'instructions': 0, 'writes': 0}

    def step(engine, pc, size, unused):
        counts['instructions'] += 1
        trace.update(struct.pack('<I', pc))
        if pc not in cache:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Enemy initializer escaped native inventory', hex(pc)))
            cache[pc] = ranges[index]
        entry = cache[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Enemy initializer entered incorrect native mode')
        seen.add(entry)
        if pending_return and pc == pending_return[0]:
            expected_return = calls[len(observed_returns)]['expectedReturnBits']
            actual_return = hex(engine.reg_read(UC_ARM_REG_R0))
            if actual_return != expected_return:
                raise ValueError('Native fixed-point scale return differs from independent wrapped-word model')
            observed_returns.append(actual_return)
            pending_return.clear()
        if pc == 0x0203D294:
            observed_draws.append({'bound': engine.reg_read(UC_ARM_REG_R0), 'stateBefore': struct.unpack('<I', engine.mem_read(RNG, 4))[0]})
        if pc == 0x021E88A4:
            observed_calls.append([engine.reg_read(UC_ARM_REG_R0 + index) for index in range(3)])
            pending_return.append(engine.reg_read(UC_ARM_REG_LR))

    def write(engine, access, address, size, value, unused):
        if not (STACK <= address < address + size <= STACK + 0x10000 or
                DESTINATION <= address < address + size <= DESTINATION + len(destination) or address == RNG and size == 4):
            raise ValueError(('Enemy initializer wrote outside declared effects', hex(address)))
        counts['writes'] += 1
        writes.update(struct.pack('<IIQ', address, size, value & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ADDRESS, STOP, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError('Enemy initializer did not actually return within bound')
    if machine.reg_read(UC_ARM_REG_R0) != result:
        raise ValueError('Enemy initializer result differs from independent model')
    if observed_draws != [{key: row[key] for key in ['bound', 'stateBefore']} for row in draws]:
        raise ValueError('Enemy initializer RNG invocation/order differs from independent model')
    if observed_calls != [row['arguments'] for row in calls]:
        raise ValueError('Enemy initializer scale argument widths/order differ from independent model')
    if pending_return or len(observed_returns) != len(calls):
        raise ValueError('Native fixed-point scale did not return at each qualified call site')
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError('Enemy initializer damaged preserved registers')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram):
        actual = bytes(machine.mem_read(DESTINATION, len(destination)))
        raise ValueError(('Enemy initializer effects differ from independent model', vector,
                          [(hex(i), expected, actual[i]) for i, expected in enumerate(output) if actual[i] != expected]))
    return {'actualReturn': True, 'vector': vector, 'return': result, 'rngFinal': state,
            'independentDraws': draws, 'independentScaleCalls': calls, **counts,
            'nativeScaleReturnBits': observed_returns,
            'nativeEntries': [[hex(start), end - start, module, mode] for start, end, module, mode in sorted(seen)],
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'wholeRamSha256': hashlib.sha256(ram).hexdigest(),
            'wholeStackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'pcTraceSha256': trace.hexdigest(), 'writeTraceSha256': writes.hexdigest()}
