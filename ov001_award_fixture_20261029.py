import bisect
import hashlib
import json
import random
import re
import struct
from functools import cache

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from ov001_award_cases_20261029 import ACTIVE, RESERVE, ROSTER, setup, expected, read32
from project import ROOT

BASE, STACK, STOP = 0x02000000, 0x03010000, 0x07000000
UI = {0x022071A8, 0x022071D0, 0x02207074}
RESOURCE = 0x0202A818


@cache
def functions():
    result = []
    for module, file in [('main', 'config/arm9/symbols.txt'), ('ov001', 'config/arm9/overlays/ov001/symbols.txt')]:
        for mode, length, address in re.findall(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', (ROOT / file).read_text()):
            result.append((int(address, 0), int(address, 0) + int(length, 0), module, mode))
    result.sort()
    return [row[0] for row in result], result


def check_rows(machine, address, rows, outcomes):
    for outcome in outcomes:
        row = rows[outcome['row']]
        storage = address == 0x021E4C34
        location = ROSTER + row['index'] * 0x84 if storage else row['actorAddress']
        before = row['record'] if storage else row['actor']
        after = bytes(machine.mem_read(location, len(before)))
        if not outcome['eligible']:
            if after != before:
                raise ValueError('Ineligible reward recipient changed')
            continue
        fields = [(0x34 if storage else 0x200, outcome['experience'], 'I'),
                  (0x30 if storage else 0x1FC, outcome['level'], 'B'),
                  (0x38 if storage else 0x204, outcome['nextExperience'], 'I'),
                  (0x3C if storage else 0x208, outcome['skillPoints'], 'H')]
        for offset, value, kind in fields:
            actual = struct.unpack_from('<' + kind, after, offset)[0]
            if kind == 'I':
                value &= 0xFFFFFFFF
            if actual != value:
                raise ValueError(('Independent experience/level/skill model differs', hex(address), row['index'], hex(offset), actual, value))
        allowed = [(0x20, 0x10), (0x30, 1), (0x34, 10)] if storage else [(0x1EC, 4), (0x1F4, 9), (0x200, 10), (0x20C, 0x20)]
        normalized = bytearray(after)
        for start, size in allowed:
            normalized[start:start + size] = before[start:start + size]
        if bytes(normalized) != before:
            raise ValueError('Reward changed a recipient field outside its declared effects')


def execute(main, overlay, address, code, bindings, blobs, vector):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for start, size in ((BASE, 0x800000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(start, size)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(address, code)
    rows = setup(machine, blobs, vector)
    rng = random.Random(vector['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    for index, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    expected_result, outcomes = expected(address, rows, blobs, vector)
    initial = bytes(machine.mem_read(BASE, 0x800000))
    starts, ranges = functions()
    seen, calls, resources, pc_cache = set(), [], [], {}
    instruction_hash, write_hash = hashlib.sha256(), hashlib.sha256()
    counts = {'instructions': 0, 'writes': 0}

    def returned(engine, value):
        engine.reg_write(UC_ARM_REG_R0, value)
        lr = engine.reg_read(UC_ARM_REG_LR)
        engine.reg_write(UC_ARM_REG_CPSR, engine.reg_read(UC_ARM_REG_CPSR) & ~32 | (32 if lr & 1 else 0))
        engine.reg_write(UC_ARM_REG_PC, lr & ~1)

    def step(engine, pc, size, unused):
        counts['instructions'] += 1
        instruction_hash.update(struct.pack('<I', pc))
        if pc not in pc_cache:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Native award escaped qualified function inventory', hex(pc)))
            pc_cache[pc] = ranges[index]
        entry = pc_cache[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Native award entered a function in the wrong mode')
        seen.add(entry)
        if pc in UI:
            calls.append({'address': hex(pc), 'arguments': [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(4)]})
            returned(engine, 0)
        elif pc == RESOURCE:
            name, destination, length, offset = [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(4)]
            if bytes(engine.mem_read(name, 15)) != b'LevelUpTbl.bin\0' or destination != 0x021B9E9C or length != 4 or offset % 4 or offset + length > len(blobs['LevelUpTbl.bin']):
                raise ValueError('Native threshold resource read violated its measured file contract')
            if vector['ioSuccess']:
                engine.mem_write(destination, blobs['LevelUpTbl.bin'][offset:offset + length])
            resources.append({'offset': offset, 'length': length, 'success': vector['ioSuccess']})
            for index in range(1, 4):
                engine.reg_write(UC_ARM_REG_R0 + index, 0x12345678 + index * 0x11111111)
            returned(engine, int(vector['ioSuccess']))

    def written(engine, access, destination, size, value, unused):
        allowed = [(STACK, 0x10000), (ROSTER, 100 * 0x84), (ACTIVE, 3 * 0x440),
                   (RESERVE, 3 * 0x440), (0x021C0E20, 0xE0), (0x021B9E9C, 4)]
        if not any(start <= destination and destination + size <= start + length for start, length in allowed):
            raise ValueError(('Native award wrote outside declared state', hex(destination), size))
        counts['writes'] += 1
        write_hash.update(struct.pack('<IIQ', destination, size, value & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(address, STOP, count=1000000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError('Native award did not actually return within its instruction bound')
    if machine.reg_read(UC_ARM_REG_R0) != expected_result:
        raise ValueError('Native award return differs from independent recipient model')
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError('Native award damaged preserved registers')
    check_rows(machine, address, rows, outcomes)
    ram = bytes(machine.mem_read(BASE, 0x800000))
    normalized = bytearray(ram)
    for start, length in [(ROSTER, 100 * 0x84), (ACTIVE, 3 * 0x440), (RESERVE, 3 * 0x440), (0x021C0E20, 0xE0), (0x021B9E9C, 4)]:
        normalized[start - BASE:start - BASE + length] = initial[start - BASE:start - BASE + length]
    if bytes(normalized) != initial:
        raise ValueError('Native award changed RAM outside declared output regions')
    return {'actualReturn': True, 'seed': vector['seed'], 'vector': vector, **counts,
            'return': expected_result, 'independentRecipients': outcomes, 'uiProviders': calls,
            'fileIoBindings': resources, 'nativeFunctionEntries': [[hex(start), end - start, module, mode] for start, end, module, mode in sorted(seen) if start not in UI | {RESOURCE}],
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'wholeRamSha256': hashlib.sha256(ram).hexdigest(),
            'wholeStackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'pcTraceSha256': instruction_hash.hexdigest(), 'writeTraceSha256': write_hash.hexdigest()}
