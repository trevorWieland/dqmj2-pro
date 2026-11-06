import bisect
import hashlib
import random
import struct

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from ov001_award_fixture_20261029 import functions
from ov001_action_candidate_cases_20261030 import RNG

BASE, ADDRESS, STACK, STOP = 0x02000000, 0x021DA124, 0x03010000, 0x07000000


def execute(main, overlay, vector):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base, size in ((BASE, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(base, size)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    for address, payload in vector['memory']:
        machine.mem_write(address, payload)
    rng = random.Random(vector['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    initial_sp = STACK + 0xFFF0
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[0] = vector['initialize']
    for index, word in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, word)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, initial_sp)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    expected_ram = bytearray(machine.mem_read(BASE, 0x400000))
    for address, payload in vector['patches']:
        expected_ram[address - BASE:address - BASE + len(payload)] = payload
    starts, ranges = functions()
    cache, seen, calls, pending_rng, rng_returns = {}, set(), [], [], []
    trace, writes = hashlib.sha256(), hashlib.sha256()
    counts = {'instructions': 0, 'writes': 0}
    phase_slots = []

    def step(engine, pc, size, unused):
        counts['instructions'] += 1
        trace.update(struct.pack('<I', pc))
        if pending_rng and pc == pending_rng[-1]['returnPc']:
            item = pending_rng.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['entrySp'] or engine.reg_read(UC_ARM_REG_R0) != item['draw']:
                raise ValueError('Original phase RNG did not return the independently predicted draw')
            rng_returns.append(item)
        if pc not in cache:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Phase setup escaped native inventory', hex(pc)))
            cache[pc] = ranges[index]
        entry = cache[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Phase setup entered the wrong native mode')
        seen.add(entry)
        if pc == entry[0]:
            calls.append(hex(pc))
        if pc == 0x021E6D58:
            phase_slots.append(engine.reg_read(UC_ARM_REG_R0))
        if pc == 0x0203D294:
            index = len(rng_returns)
            limit = engine.reg_read(UC_ARM_REG_R0)
            if index >= len(vector['limits']) or limit != vector['limits'][index]:
                raise ValueError('Original phase RNG order/limit differs')
            pending_rng.append({'returnPc': engine.reg_read(UC_ARM_REG_LR), 'limit': limit,
                                'entrySp': engine.reg_read(UC_ARM_REG_SP), 'draw': vector['draws'][index]})

    def written(engine, access, destination, size, word, unused):
        allowed = [(STACK, 0x10000)] + [(address, len(payload)) for address, payload in vector['patches']]
        if not any(base <= destination and destination + size <= base + length for base, length in allowed):
            raise ValueError(('Phase setup wrote outside independent effects', hex(destination)))
        counts['writes'] += 1
        writes.update(struct.pack('<IIQ', destination, size, word & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ADDRESS, STOP, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != initial_sp or pending_rng:
        raise ValueError('Phase setup or original RNG did not actually return')
    if machine.reg_read(UC_ARM_REG_R0) != len(vector['eligibleSlots']) or len(rng_returns) != len(vector['limits']):
        raise ValueError('Phase setup return/count differs from independent model')
    expected_slots = vector['eligibleSlots'] if vector['initialize'] else []
    if phase_slots != expected_slots:
        raise ValueError('Original per-slot phase initialization order differs')
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError('Phase setup damaged preserved registers')
    ram = bytes(machine.mem_read(BASE, 0x400000))
    if ram != bytes(expected_ram):
        raise ValueError('Phase setup full-RAM effects differ from independent model')
    recipe = {key: value for key, value in vector.items() if key not in ('memory', 'patches')}
    return {**recipe, 'actualReturn': True, **counts, 'phaseSlots': phase_slots, 'rngReturns': rng_returns,
            'nativeCallEntries': calls, 'nativeEntries': [[hex(a), b - a, m, mode] for a, b, m, mode in sorted(seen)],
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'wholeRamSha256': hashlib.sha256(ram).hexdigest(),
            'wholeStackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'traceSha256': trace.hexdigest(), 'writesSha256': writes.hexdigest()}
