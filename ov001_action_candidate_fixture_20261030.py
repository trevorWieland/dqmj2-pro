import bisect
import hashlib
import random
import struct

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from ov001_award_fixture_20261029 import functions
from ov001_action_candidate_cases_20261030 import MODE, RNG, OUTPUT

BASE, ADDRESS, STACK, STOP = 0x02000000, 0x021E7290, 0x03010000, 0x07000000
TABLES = [('EnmyKindTbl.bin', 0x02300000, 0x020F69F0),
          ('ActTbl.bin', 0x02320000, 0x021C6748),
          ('ItemTbl.bin', 0x02330000, 0x021C2AB4),
          ('EquipTbl.bin', 0x02340000, 0x021C6BF4)]


def execute(main, overlay, code, assets, vector, observe=False):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base, size in ((BASE, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(base, size)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ADDRESS, code)
    for name, address, pointer in TABLES:
        machine.mem_write(address, assets[name][8:])
        machine.mem_write(pointer, struct.pack('<I', address))
    machine.mem_write(0x02310000, assets['AbilityTbl.bin'])
    machine.mem_write(0x02238D58, struct.pack('<I', 0x02310000))
    machine.mem_write(0x020F69E4, bytes(4))
    for address, payload in vector['memory']:
        machine.mem_write(address, payload)
    rng = random.Random(vector['seed'])
    stack = bytearray(rng.randbytes(0x20000))
    initial_sp = STACK + 0xFFF0
    struct.pack_into('<2I', stack, initial_sp - 0x03000000, *vector['arguments'][4:])
    machine.mem_write(0x03000000, bytes(stack))
    registers = vector['arguments'][:4] + [rng.getrandbits(32) for unused in range(9)]
    for position, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + position, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, initial_sp)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    expected = bytearray(machine.mem_read(BASE, 0x400000))
    for address, payload in vector['patches']:
        expected[address - BASE:address - BASE + len(payload)] = payload
    starts, ranges = functions()
    cache, seen, calls, pending_rng, rng_results, pending_validation, validations = {}, set(), [], [], [], [], []
    trace, writes = hashlib.sha256(), hashlib.sha256()
    counts = {'instructions': 0, 'writes': 0}
    modeled_rng = vector['initialRng']

    def step(engine, pc, size, unused):
        nonlocal modeled_rng
        counts['instructions'] += 1
        trace.update(struct.pack('<I', pc))
        if pending_rng and pc == pending_rng[-1]['returnPc']:
            item = pending_rng.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['entrySp'] or engine.reg_read(UC_ARM_REG_R0) != item['result']:
                raise ValueError('Original RNG return differs from independent LCG model')
            if struct.unpack('<I', bytes(engine.mem_read(RNG, 4)))[0] != item['state']:
                raise ValueError('Original RNG state differs from independent LCG model')
            rng_results.append({'limit': item['limit'], 'result': item['result'], 'actualReturn': True})
        if pending_validation and pc == pending_validation[-1]['returnPc']:
            item = pending_validation.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['entrySp']:
                raise ValueError('Original validator did not restore SP')
            validations.append({'action': item['action'], 'result': engine.reg_read(UC_ARM_REG_R0), 'actualReturn': True})
        if pc not in cache:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Candidate escaped qualified native inventory', hex(pc)))
            cache[pc] = ranges[index]
        entry = cache[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Candidate entered a wrong native instruction mode')
        seen.add(entry)
        if pc == entry[0]:
            calls.append(hex(pc))
        if pc == 0x0203D294:
            limit = engine.reg_read(UC_ARM_REG_R0)
            position = len(rng_results)
            if not observe and (position >= len(vector['limits']) or limit != vector['limits'][position]):
                raise ValueError(('Unexpected original RNG branch', vector['branch'], vector['phase'], limit, vector['limits']))
            modeled_rng = (modeled_rng * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
            result = (modeled_rng >> 16) % limit if 0 < limit < 0x80000000 else 0
            pending_rng.append({'limit': limit, 'returnPc': engine.reg_read(UC_ARM_REG_LR),
                                'entrySp': engine.reg_read(UC_ARM_REG_SP), 'result': result, 'state': modeled_rng})
        if pc == 0x021E7484:
            pending_validation.append({'action': engine.reg_read(UC_ARM_REG_R0 + 1),
                                       'returnPc': engine.reg_read(UC_ARM_REG_LR),
                                       'entrySp': engine.reg_read(UC_ARM_REG_SP)})

    def written(engine, access, destination, size, value, unused):
        allowed = [(STACK, 0x10000), (MODE, 1), (RNG, 4), (OUTPUT, 4)]
        if not any(base <= destination and destination + size <= base + length for base, length in allowed):
            raise ValueError(('Candidate wrote outside independent effects', hex(destination), size))
        counts['writes'] += 1
        writes.update(struct.pack('<IIQ', destination, size, value & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ADDRESS, STOP, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != initial_sp or pending_rng or pending_validation:
        raise ValueError('Candidate or native nested helper did not actually return')
    if machine.reg_read(UC_ARM_REG_R0) != 1 or not observe and len(rng_results) != len(vector['limits']):
        raise ValueError('Independent candidate physical result or RNG count differs')
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError('Candidate changed preserved registers')
    ram = bytes(machine.mem_read(BASE, 0x400000))
    if observe:
        expected[OUTPUT - BASE:OUTPUT - BASE + 4] = bytes(machine.mem_read(OUTPUT, 4))
        struct.pack_into('<I', expected, RNG - BASE, modeled_rng)
    if ram != expected:
        differences = [hex(BASE + i) for i, (a, b) in enumerate(zip(ram, expected)) if a != b][:12]
        raise ValueError(('Independent candidate complete RAM model differs', vector['branch'], vector['phase'], differences))
    return {'seed': vector['seed'], 'branch': vector['branch'], 'side': vector['side'],
            'slot': vector['slot'], 'phase': vector['phase'], 'actualReturn': True, **counts,
            'rngReturns': rng_results, 'validatorReturns': validations, 'nativeCallEntries': calls,
            'nativeEntries': [[hex(start), end - start, module, mode] for start, end, module, mode in sorted(seen)],
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'output': bytes(machine.mem_read(OUTPUT, 4)).hex(),
            'outputIndependentlyPredicted': not observe,
            'wholeRamSha256': hashlib.sha256(ram).hexdigest(),
            'wholeStackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'traceSha256': trace.hexdigest(), 'writesSha256': writes.hexdigest()}
