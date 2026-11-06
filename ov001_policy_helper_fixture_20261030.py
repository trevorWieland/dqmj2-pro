import bisect
import hashlib
import random
import struct

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from ov001_award_fixture_20261029 import functions
from ov001_action_retry_fixture_20261030 import TABLES

BASE, STACK, STOP = 0x02000000, 0x03010000, 0x07000000


def execute(main, overlay, assets, address, vector):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base, size in ((BASE, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(base, size)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    for name, location, pointer in TABLES:
        machine.mem_write(location, assets[name][8:])
        machine.mem_write(pointer, struct.pack('<I', location))
    machine.mem_write(0x02310000, assets['AbilityTbl.bin'])
    machine.mem_write(0x02238D58, struct.pack('<I', 0x02310000))
    machine.mem_write(0x020F69E4, bytes(4))
    for location, payload in vector['memory']:
        machine.mem_write(location, payload)
    rng = random.Random(vector['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    initial_sp = STACK + 0xFFF0
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[:len(vector['arguments'])] = vector['arguments']
    for index, word in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, word)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, initial_sp)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    expected_ram = bytes(machine.mem_read(BASE, 0x400000))
    starts, ranges = functions()
    cache, seen, calls, protocol, pending = {}, set(), [], [], []
    trace, writes = hashlib.sha256(), hashlib.sha256()
    counts = {'instructions': 0, 'writes': 0}

    def step(engine, pc, size, unused):
        counts['instructions'] += 1
        trace.update(struct.pack('<I', pc))
        if pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['entrySp'] or engine.reg_read(UC_ARM_REG_R0) != item['expected']:
                raise ValueError('Native target protocol helper did not actually return the independent result')
            protocol.append({**item, 'actualReturn': True})
        if pc not in cache:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Policy helper escaped native inventory', hex(pc)))
            cache[pc] = ranges[index]
        entry = cache[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Policy helper entered wrong native mode')
        seen.add(entry)
        if pc == entry[0]:
            calls.append(hex(pc))
        if pc == 0x0203D294:
            raise ValueError('Restricted policy-helper corpus unexpectedly invoked RNG')
        if vector['kind'] != 'target':
            return
        expected_results = {0x021DBEC8: vector['tier'], 0x022182A0: vector['selector'],
                            0x0222BE44: vector['callback'], vector['callback']: vector['returnWord']}
        if pc in expected_results:
            arguments = [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(3)]
            if pc == 0x021DBEC8 and arguments[0] != vector['arguments'][0]:
                raise ValueError('Actor pointer was not passed to the native tier helper')
            if pc == 0x022182A0 and arguments != [vector['side'], vector['tier'], vector['action']]:
                raise ValueError('Native classifier did not receive side/tier/action')
            if pc == 0x0222BE44 and arguments[0] != vector['selector']:
                raise ValueError('Classifier result was not forwarded to native callback lookup')
            if pc == vector['callback']:
                packet = list(struct.unpack('<3I', bytes(engine.mem_read(arguments[0], 12))))
                if arguments[0] != initial_sp - 32 or packet != vector['arguments']:
                    raise ValueError('Actual native callback packet differs from all three independent words')
            pending.append({'callee': hex(pc), 'returnPc': engine.reg_read(UC_ARM_REG_LR),
                            'entrySp': engine.reg_read(UC_ARM_REG_SP), 'expected': expected_results[pc]})

    def written(engine, access, destination, size, word, unused):
        if not STACK <= destination < destination + size <= STACK + 0x10000:
            raise ValueError(('Read-only policy helper wrote outside private stack', hex(destination)))
        counts['writes'] += 1
        writes.update(struct.pack('<IIQ', destination, size, word & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(address, STOP, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != initial_sp or pending:
        raise ValueError('Policy helper or native protocol call did not actually return')
    if machine.reg_read(UC_ARM_REG_R0) != vector['returnWord']:
        raise ValueError(('Independent policy-helper result differs', vector['kind'], vector['seed']))
    if vector['kind'] == 'target' and len(protocol) != 4:
        raise ValueError('Missing actual tier/classifier/lookup/callback return')
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError('Policy helper damaged preserved registers')
    ram = bytes(machine.mem_read(BASE, 0x400000))
    if ram != expected_ram:
        raise ValueError('Policy helper changed independent full RAM')
    recipe = {key: value for key, value in vector.items() if key not in ('memory', 'patches')}
    return {**recipe, 'actualReturn': True, **counts, 'protocolReturns': protocol, 'nativeCallEntries': calls,
            'nativeEntries': [[hex(a), b - a, m, mode] for a, b, m, mode in sorted(seen)],
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'wholeRamSha256': hashlib.sha256(ram).hexdigest(),
            'wholeStackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'traceSha256': trace.hexdigest(), 'writesSha256': writes.hexdigest()}
