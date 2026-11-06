import bisect
import hashlib
import random
import struct

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from ov001_award_fixture_20261029 import functions
from ov001_action_candidate_cases_20261030 import RNG
from ov001_action_retry_fixture_20261030 import TABLES

BASE, ADDRESS, STACK, STOP = 0x02000000, 0x021E6FD8, 0x03010000, 0x07000000


def execute(main, overlay, assets, vector):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base, size in ((BASE, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(base, size)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    for name, address, pointer in TABLES:
        machine.mem_write(address, assets[name][8:])
        machine.mem_write(pointer, struct.pack('<I', address))
    machine.mem_write(0x02310000, assets['AbilityTbl.bin'])
    machine.mem_write(0x02238D58, struct.pack('<I', 0x02310000))
    machine.mem_write(0x020F69E4, bytes(4))
    for address, payload in vector['memory']:
        machine.mem_write(address, payload)
    rng = random.Random(vector['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    initial_sp = STACK + 0xFFF0
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[:4] = vector['arguments']
    for index, word in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, word)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, initial_sp)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    expected_ram = bytearray(machine.mem_read(BASE, 0x400000))
    for address, payload in vector['patches']:
        expected_ram[address - BASE:address - BASE + len(payload)] = payload
    starts, ranges = functions()
    cache, seen, calls = {}, set(), []
    pending_rng, rng_returns, pending_validator, validator_returns = [], [], [], []
    trace, writes = hashlib.sha256(), hashlib.sha256()
    counts = {'instructions': 0, 'writes': 0}
    model, visited = vector['expected'], []
    array_base = initial_sp - 40 - 32 + 12

    def step(engine, pc, size, unused):
        counts['instructions'] += 1
        trace.update(struct.pack('<I', pc))
        if pending_rng and pc == pending_rng[-1]['returnPc']:
            item = pending_rng.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['entrySp'] or engine.reg_read(UC_ARM_REG_R0) != item['result']:
                raise ValueError('Original policy RNG did not return the independent draw')
            rng_returns.append({'limit': item['limit'], 'result': item['result'], 'actualReturn': True})
        if pending_validator and pc == pending_validator[-1]['returnPc']:
            item = pending_validator.pop()
            value = {'action': item['action'], 'result': engine.reg_read(UC_ARM_REG_R0)}
            if engine.reg_read(UC_ARM_REG_SP) != item['entrySp'] or value != model['validations'][len(validator_returns)]:
                raise ValueError('Original validator differs from restricted action1/action2 model')
            validator_returns.append(value)
        if pc not in cache:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Policy escaped qualified native inventory', hex(pc)))
            cache[pc] = ranges[index]
        entry = cache[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Policy entered the wrong native instruction mode')
        seen.add(entry)
        if pc == entry[0]:
            calls.append(hex(pc))
        if pc == 0x0203D294:
            position = len(rng_returns)
            limit = engine.reg_read(UC_ARM_REG_R0)
            if position >= len(model['limits']) or limit != model['limits'][position]:
                raise ValueError(('Unexpected native policy RNG call', vector['mode'], vector['profile'], limit))
            pending_rng.append({'returnPc': engine.reg_read(UC_ARM_REG_LR),
                                'entrySp': engine.reg_read(UC_ARM_REG_SP), 'limit': limit,
                                'result': model['draws'][position]})
        if pc == 0x021E7484:
            if len(validator_returns) >= len(model['validations']):
                raise ValueError('Unexpected original validator call')
            pending_validator.append({'returnPc': engine.reg_read(UC_ARM_REG_LR),
                                      'entrySp': engine.reg_read(UC_ARM_REG_SP),
                                      'action': engine.reg_read(UC_ARM_REG_R0 + 1)})
        if pc in (0x021E70FC, 0x021E7118, 0x021E7148):
            index = engine.reg_read(UC_ARM_REG_R0 + (4 if pc == 0x021E70FC else 8))
            pointer = engine.reg_read(UC_ARM_REG_R0) - 4
            if not 1 <= index <= 5 or pointer != array_base + (index - 1) * 4:
                raise ValueError('Visited index escaped the actual five-word private stack array')
            if pc == 0x021E7118:
                visited.append(['read', index, struct.unpack('<I', bytes(engine.mem_read(pointer, 4)))[0]])
            else:
                visited.append(['firstWrite' if pc == 0x021E70FC else 'write', index])

    def written(engine, access, destination, size, word, unused):
        allowed = [(STACK, 0x10000), (RNG, 4), (vector['actor'] + 0x35B, 1)]
        if not any(base <= destination and destination + size <= base + length for base, length in allowed):
            raise ValueError(('Policy wrote outside independent effects', hex(destination)))
        counts['writes'] += 1
        writes.update(struct.pack('<IIQ', destination, size, word & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ADDRESS, STOP, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != initial_sp or pending_rng or pending_validator:
        raise ValueError('Policy or original nested helper did not actually return')
    if machine.reg_read(UC_ARM_REG_R0) != model['action'] or len(rng_returns) != len(model['limits']):
        raise ValueError('Independent policy return or RNG count differs')
    if validator_returns != model['validations'] or visited != model['visitedEvents']:
        raise ValueError('Independent validator or visited-slot model differs')
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError('Policy damaged preserved registers')
    ram = bytes(machine.mem_read(BASE, 0x400000))
    if ram != bytes(expected_ram):
        raise ValueError(('Independent full-RAM model differs', vector['mode'], vector['profile'], vector['turn']))
    return {'seed': vector['seed'], 'mode': vector['mode'], 'profile': vector['profile'],
            'side': vector['side'], 'turn': vector['turn'], 'expected': model, 'actualReturn': True,
            **counts, 'rngReturns': rng_returns, 'validatorReturns': validator_returns,
            'visitedEvents': visited, 'nativeCallEntries': calls,
            'nativeEntries': [[hex(a), b - a, m, mode] for a, b, m, mode in sorted(seen)],
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'wholeRamSha256': hashlib.sha256(ram).hexdigest(),
            'wholeStackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'traceSha256': trace.hexdigest(), 'writesSha256': writes.hexdigest()}
