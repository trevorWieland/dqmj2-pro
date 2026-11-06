import bisect
import hashlib
import random
import struct

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from ov001_award_fixture_20261029 import functions

ADDRESS, ACTOR, DATA, STACK, STOP = 0x021E6764, 0x02300000, 0x02301000, 0x03010000, 0x07000000
RANGES, ENTRIES, MASKS, CALLBACKS = 0x022445C8, 0x022449C8, 0x02242EC8, 0x0222F270
NATIVE_CALLBACKS = {0: 0x02218DF4, 2: 0x02218E14, 6: 0x02218E54}


def vectors():
    deltas = [-128, -127, -1, 0, 1, 127]
    for index in range(128):
        rank = [0, 1, 2, 3, 4, 7][index % 6]
        entries = []
        for position in range(index % 4):
            identifier = [0, 2, 6][(index + position) % 3]
            mask = [255, 0, 1 << rank, 1 << ((rank + 1) % 8)][(index // 4 + position) % 4]
            entries.append({'id': identifier, 'trueDelta': deltas[(index + position) % 6],
                            'falseDelta': deltas[(index // 3 + position) % 6], 'mask': mask})
        yield {'ordinal': index, 'seed': 202610306764 + index, 'rank': rank, 'key': 0x42,
               'initial': [0, 1, 0xFFFFFFFF, 0x80000000][index % 4],
               'arg1': (index * 0x12345679) & 0xFFFFFFFF, 'arg2': (0xFFFFFFFF - index * 0x11111111) & 0xFFFFFFFF,
               'arg5': [0, 1, 0xFFFFFFFF, 0x80000000][index // 4 % 4], 'entries': entries}


def model(vector):
    result, calls = vector['initial'], []
    for entry in vector['entries']:
        if not entry['mask'] & (1 << vector['rank']):
            continue
        calls.append(entry['id'])
        test = entry['id'] == 0 or entry['id'] == 6 and vector['arg5'] != 0
        delta = entry['trueDelta'] if test else entry['falseDelta']
        if delta == -128:
            return 0xFFFFFFFF, calls
        result = (result + delta) & 0xFFFFFFFF
    return result, calls


def execute(main, overlay, code, item_table, vector):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(base, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ADDRESS, code)
    machine.mem_write(0x02320000, item_table[8:])
    machine.mem_write(0x021C2AB4, struct.pack('<I', 0x02320000))
    actor, data = bytearray(0x440), bytearray(0xB0)
    struct.pack_into('<I', actor, 0x1E8, DATA)
    actor[0x322], data[0xA9] = 1, vector['rank']
    machine.mem_write(ACTOR, bytes(actor))
    machine.mem_write(DATA, bytes(data))
    machine.mem_write(RANGES + vector['key'] * 4, struct.pack('<HH', 3, 2 + len(vector['entries'])))
    for position, entry in enumerate(vector['entries']):
        machine.mem_write(ENTRIES + (position + 3) * 4, struct.pack('<Hbb', entry['id'], entry['trueDelta'], entry['falseDelta']))
        machine.mem_write(MASKS + entry['id'], bytes([entry['mask']]))
    callback_addresses = {}
    for identifier, address in NATIVE_CALLBACKS.items():
        observed = struct.unpack('<I', machine.mem_read(CALLBACKS + identifier * 4, 4))[0]
        if observed != address:
            raise ValueError('Measured native callback pointer/table changed')
        callback_addresses[address] = identifier
    rng = random.Random(vector['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[:4] = [ACTOR, vector['arg1'], vector['arg2'], vector['key']]
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for index, word in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, word)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.mem_write(STACK + 0xFFF0, struct.pack('<II', vector['initial'], vector['arg5']))
    initial_ram = bytes(machine.mem_read(0x02000000, 0x400000))
    result, expected_calls = model(vector)
    starts, ranges = functions()
    trace, writes = hashlib.sha256(), hashlib.sha256()
    seen, cache, calls = set(), {}, []
    counts = {'instructions': 0, 'writes': 0}

    def step(engine, pc, size, unused):
        counts['instructions'] += 1
        trace.update(struct.pack('<I', pc))
        if pc not in cache:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Condition reducer escaped qualified inventory', hex(pc)))
            cache[pc] = ranges[index]
        entry = cache[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Condition reducer entered incorrect native mode')
        seen.add(entry)
        if pc == 0x0203D294:
            raise ValueError('Forced-rank fixture unexpectedly consumed RNG')
        if pc in callback_addresses:
            pointer = engine.reg_read(UC_ARM_REG_R0)
            context = list(struct.unpack('<7I', engine.mem_read(pointer, 28)))
            expected_context = [ACTOR, vector['arg1'], vector['arg2'], vector['key'], 0, vector['arg5'], 0xFFFFFFFF]
            if pointer != STACK + 0xFFB0 or context != expected_context:
                raise ValueError('Native callback context pointer/word layout differs')
            calls.append({'id': callback_addresses[pc], 'address': hex(pc), 'mode': entry[3], 'context': context})

    def write(engine, access, destination, size, value, unused):
        if not STACK <= destination < destination + size <= STACK + 0x10000:
            raise ValueError('Condition reducer wrote outside bounded stack')
        counts['writes'] += 1
        writes.update(struct.pack('<IIQ', destination, size, value & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ADDRESS, STOP, count=20000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError('Condition reducer did not actually return')
    if machine.reg_read(UC_ARM_REG_R0) != result or [row['id'] for row in calls] != expected_calls:
        raise ValueError('Independent condition selection/delta/sentinel model differs')
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError('Condition reducer changed preserved registers')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != initial_ram:
        raise ValueError('Condition reducer modified non-stack RAM')
    return {'actualReturn': True, 'vector': vector, 'return': result, 'nativeCallbacks': calls, **counts,
            'nativeEntries': [[hex(start), end - start, module, mode] for start, end, module, mode in sorted(seen)],
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'wholeRamSha256': hashlib.sha256(ram).hexdigest(),
            'wholeStackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'pcTraceSha256': trace.hexdigest(), 'writeTraceSha256': writes.hexdigest()}
