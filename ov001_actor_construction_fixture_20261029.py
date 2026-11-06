import bisect
import hashlib
import random
import struct

from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_INVALID
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from ov001_award_fixture_20261029 import functions

ADDRESS, TABLE, STACK, STOP = 0x021D9F70, 0x02300000, 0x03010000, 0x07000000
RECORDS = [0x021C0F14, 0x021C1544, 0x021C1B74, 0x021C21A4]
ACTORS = [0x02236F6C, 0x022362AC, 0x022355EC, 0x02237C2C]
GETTERS = [0x020649AC, 0x020649C0, 0x020649D4, 0x020649E8]


def vectors():
    for team in range(4):
        for scene in [0, 1, 2, 3, 4, 8, 9]:
            for mask in [0, 1, 3, 5, 7]:
                index = team * 35 + [0, 1, 2, 3, 4, 8, 9].index(scene) * 5 + [0, 1, 3, 5, 7].index(mask)
                yield {'team': team, 'scene': scene, 'presentMask': mask, 'fallback': index % 2,
                       'ordinal': index, 'emptyTraitsDefaultModifiers': index % 9 == 0,
                       'machineSeed': 202610309970 + index}


def record_set(vector):
    rng = random.Random(vector['machineSeed'] ^ 0x4F)
    records = []
    for slot in range(3):
        data = bytearray(rng.randbytes(0x210))
        struct.pack_into('<h', data, 0x2E, [1, 4, 20][slot] if vector['presentMask'] & (1 << slot) else [0, -1][slot % 2])
        data[0xAD] = 99 if (vector['ordinal'] + slot) % 7 == 0 else 0
        data[0xC:0x2C] = bytes(32)
        selected = [0, 7, 8, 31, 32, 63, 64, 127, 128, 191, 224, 255]
        for number in selected:
            if (number + slot + vector['ordinal']) % 3:
                offset = 0xC + number // 32 * 4
                word = struct.unpack_from('<I', data, offset)[0] | (1 << (number % 32))
                struct.pack_into('<I', data, offset, word)
        data[0x4A:0x8A] = bytes(64)
        values = [0, 1, 9998, 9999, 10000, 32767, -32768, -1]
        for number in range(16):
            struct.pack_into('<h', data, 0x11C + 2 * number, values[(number + slot + vector['ordinal']) % len(values)])
        data[0x202] = 0 if vector['emptyTraitsDefaultModifiers'] else 1
        if vector['emptyTraitsDefaultModifiers']:
            data[0x11C:0x13C] = bytes(32)
            if vector['ordinal'] % 18:
                struct.pack_into('<8h', data, 0x11C, 100 + slot * 50, 50 + slot * 20,
                                 20 + slot * 10, 10 + slot * 5, 30, 40, 50, 60)
        records.append(bytes(data))
    return records


def rank(vector, metadata):
    if vector['team'] != 1:
        return 0
    if metadata == 99:
        return 2
    if vector['scene'] in [0, 8]:
        return 1
    if vector['scene'] == 1:
        return 3
    if vector['scene'] in [3, 4, 5, 6, 7]:
        return 0
    return int(vector['fallback'] == 0)


def model(records, actions, vector):
    result = bytearray(3 * 0x440)
    present, details = 0, []
    for slot, record in enumerate(records):
        if struct.unpack_from('<h', record, 0x2E)[0] <= 0:
            continue
        present += 1
        actor = bytearray(0x440)
        actor[0x31E], actor[0x31F] = vector['team'], slot
        actor[0x322] = rank(vector, record[0xAD])
        struct.pack_into('<I', actor, 0x1E8, RECORDS[vector['team']] + slot * 0x210 + 4)
        actor[0x22C:0x2A4] = record[0x13C:0x1B4]
        actor[0x39E:0x3DA] = record[0x1C4:0x200]
        actor[0x432:0x43C] = record[0x203:0x20D]
        actor[0x43C] = record[0x20D]
        actor[0x1EC:0x20C] = record[0x11C:0x13C]
        for offset in [0x1EC, 0x1EE, 0x1F0, 0x1F4, 0x1F6, 0x1F8, 0x1FA]:
            struct.pack_into('<h', actor, offset, min(struct.unpack_from('<h', actor, offset)[0], 9999))
        expanded = []
        if actor[0x322] in [0, 3]:
            expanded = [number for number in range(256) if record[0xC + number // 8] & (1 << (number % 8))]
            for first in range(len(expanded)):
                for second in range(first + 1, len(expanded)):
                    if actions[expanded[first] * 40 + 36] > actions[expanded[second] * 40 + 36]:
                        expanded[first], expanded[second] = expanded[second], expanded[first]
            actor[0x323] = len(expanded)
            actor[0x35E:0x35E + len(expanded)] = bytes(expanded)
        if not vector['emptyTraitsDefaultModifiers']:
            actor[0x21C:0x22C] = record[0x1B4:0x1C4]
        actor[0x31C] = 1
        result[slot * 0x440:(slot + 1) * 0x440] = actor
        details.append({'slot': slot, 'rank': actor[0x322], 'expandedSortedBytes': expanded,
                        'nativeStatSetupPath': 'empty-traits-native-stat-normalization' if vector['emptyTraitsDefaultModifiers'] else 'supplied-modifier-block'})
    return bytes(result), present, details


def execute(main, overlay, code, actions, vector, extra_assets):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ADDRESS, code)
    machine.mem_write(TABLE, actions)
    machine.mem_write(0x021C6748, struct.pack('<I', TABLE))
    for name, location, pointer in [('ItemTbl.bin', 0x02310000, 0x021C2AB4),
                                     ('EquipTbl.bin', 0x02320000, 0x021C6BF4),
                                     ('EnmyKindTbl.bin', 0x02330000, 0x020F69F0)]:
        machine.mem_write(location, extra_assets[name][8:])
        machine.mem_write(pointer, struct.pack('<I', location))
    machine.mem_write(0x020F69E8, bytes([vector['scene']]))
    machine.mem_write(0x021C0F04, bytes([vector['fallback']]))
    records = record_set(vector)
    rng = random.Random(vector['machineSeed'])
    for address in ACTORS:
        machine.mem_write(address, rng.randbytes(3 * 0x440))
    machine.mem_write(RECORDS[vector['team']], b''.join(records))
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[0] = vector['team']
    for index, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    output, expected, details = model(records, actions, vector)
    destination = ACTORS[vector['team']]
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_ram[destination - 0x02000000:destination - 0x02000000 + len(output)] = output
    starts, ranges = functions()
    seen, cache, getters = set(), {}, []
    trace, writes = hashlib.sha256(), hashlib.sha256()
    counts = {'instructions': 0, 'writes': 0}
    invalid = []

    def step(engine, pc, size, unused):
        counts['instructions'] += 1
        trace.update(struct.pack('<I', pc))
        if pc not in cache:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Actor constructor escaped native inventory', hex(pc)))
            cache[pc] = ranges[index]
        entry = cache[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Actor constructor entered incorrect native mode')
        seen.add(entry)
        if pc in GETTERS:
            getters.append((pc, engine.reg_read(UC_ARM_REG_R0)))
        if pc == 0x0203D294:
            raise ValueError('Actor constructor entered unsupported random-trait path')

    def write(engine, access, address, size, value, unused):
        if not (STACK <= address < address + size <= STACK + 0x10000 or destination <= address < address + size <= destination + len(output)):
            raise ValueError(('Actor constructor wrote outside declared effects', hex(address)))
        counts['writes'] += 1
        writes.update(struct.pack('<IIQ', address, size, value & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)

    def fault(engine, access, address, size, value, unused):
        invalid.append({'access': access, 'address': hex(address), 'size': size, 'pc': hex(engine.reg_read(UC_ARM_REG_PC))})
        return False

    machine.hook_add(UC_HOOK_MEM_INVALID, fault)
    try:
        machine.emu_start(ADDRESS, STOP, count=100000)
    except UcError as error:
        raise ValueError({'nativeFault': invalid, 'vector': vector,
                          'registers': [hex(machine.reg_read(UC_ARM_REG_R0 + i)) for i in range(13)]}) from error
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError('Actor constructor did not actually return within bound')
    if machine.reg_read(UC_ARM_REG_R0) != expected or getters != [(GETTERS[vector['team']], 0)]:
        raise ValueError('Actor constructor count/getter ABI differs from independent model')
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError('Actor constructor damaged preserved registers')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram):
        actual = bytes(machine.mem_read(destination, len(output)))
        raise ValueError(('Actor constructor effects differ', vector,
                          [(hex(i), expected, actual[i]) for i, expected in enumerate(output) if actual[i] != expected][:32]))
    return {'actualReturn': True, 'vector': vector, 'return': expected, 'slots': details, **counts,
            'nativeEntries': [[hex(start), end - start, module, mode] for start, end, module, mode in sorted(seen)],
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'wholeRamSha256': hashlib.sha256(ram).hexdigest(),
            'wholeStackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'pcTraceSha256': trace.hexdigest(), 'writeTraceSha256': writes.hexdigest()}
