import hashlib
import json
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946

BASE, OBJECT, PACKET = 0x02000000, 0x02300000, 0x02310000
STACK, STOP = 0x03000000, 0x04000000
GLOBAL = 0x021E78C4
RETURNS = {0x021D75F8: 0xA1234567, 0x021D8788: 0xB7654321, 0x020127EC: 0x02320000,
           0x021D773C: 0xC1020304, 0x021D7874: 0xD5060708}
ARITIES = {0x021D75F8: 1, 0x021D8788: 2, 0x020127EC: 1, 0x021D773C: 3, 0x021D7874: 3, 0x021D7778: 2}


def digest(value):
    return hashlib.sha256(value).hexdigest()


def model(entry, case):
    state, small, packet = case['state'], case['small'], case['packet']
    calls = []
    if entry == 0x021D761C:
        event, value = case['event'] & 0xFFFFFFFF, case['value'] & 0xFFFFFFFF
        if value == 0 or event in (0x81, 15):
            result = OBJECT
        elif event == 12 and (value == 1 or (value - 11) & 0xFFFFFFFF <= 1):
            state = 5
            calls = [(0x021D8788, [OBJECT, 3])]
            result = RETURNS[0x021D8788]
        else:
            if event == 14:
                state = 5
            calls = [(0x021D75F8, [OBJECT])]
            result = RETURNS[0x021D75F8]
    elif packet:
        calls = [(0x021D7778, [OBJECT, PACKET])]
        if not case['accepted']:
            result = 0
        elif case['packetWord'] != 1:
            result = case['packetWord']
        else:
            small = 0
            calls.append((0x021D7874, [OBJECT, 3, 0]))
            result = RETURNS[0x021D7874]
    else:
        state = 1
        calls = [(0x020127EC, [entry]), (0x021D773C, [OBJECT, 1, RETURNS[0x020127EC]])]
        result = RETURNS[0x021D773C]
    return result, state, small, calls


def execute(main, overlay, entry, code, case, vector):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE, 0x400000)
    machine.mem_map(STACK, 0x20000)
    machine.mem_map(STOP, 0x1000)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(entry, code)
    rng = random.Random(2026103043000 + vector)
    machine.mem_write(OBJECT, rng.randbytes(0x5200))
    machine.mem_write(PACKET, struct.pack('<H', case['packetWord']))
    machine.mem_write(GLOBAL + 4, struct.pack('<I', OBJECT))
    machine.mem_write(OBJECT + 0x50F0, struct.pack('<I', case['state']))
    machine.mem_write(OBJECT + 0x50E4, struct.pack('<H', case['small']))
    machine.mem_write(STACK, rng.randbytes(0x20000))
    initial = bytearray(machine.mem_read(BASE, 0x400000))
    initial[entry - BASE:entry - BASE + len(code)] = bytes(len(code))
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    registers = [rng.getrandbits(32) for unused in range(13)]
    for index, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    args = [OBJECT, case['event'] & 0xFFFFFFFF, case['value'] & 0xFFFFFFFF] if entry == 0x021D761C else [PACKET if case['packet'] else 0]
    for index, value in enumerate(args):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    sp = STACK + 0x1FFF0
    machine.reg_write(UC_ARM_REG_SP, sp)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, trace, writes = [], [], []

    def step(engine, pc, size, unused):
        trace.append(pc)
        if pc in ARITIES:
            calls.append((pc, [engine.reg_read(UC_ARM_REG_R0 + index) for index in range(ARITIES[pc])]))
            engine.reg_write(UC_ARM_REG_R0, case['accepted'] if pc == 0x021D7778 else RETURNS[pc])
            for register in (1, 2, 3, 12):
                engine.reg_write(UC_ARM_REG_R0 + register, (pc * 33 + register * 0x01020304 + vector) & 0xFFFFFFFF)
            engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))
        elif not entry <= pc < entry + len(code):
            raise AssertionError(('Escaped caller/provider bounds', hex(pc)))

    def written(engine, access, address, size, value, unused):
        if not ((STACK <= address and address + size <= STACK + 0x20000) or
                (OBJECT + 0x50F0 <= address and address + size <= OBJECT + 0x50F4) or
                (OBJECT + 0x50E4 <= address and address + size <= OBJECT + 0x50E6)):
            raise AssertionError(('Unexpected memory write', hex(address), size))
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(entry, STOP, timeout=1000000, count=20000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != sp:
        raise AssertionError('Caller did not actually return with a balanced stack')
    result, state, small, expected_calls = model(entry, case)
    if machine.reg_read(UC_ARM_REG_R0) != result or calls != expected_calls:
        raise AssertionError(('Independent return/call model differs', hex(entry), case, calls, expected_calls))
    expected = bytearray(initial)
    struct.pack_into('<I', expected, OBJECT + 0x50F0 - BASE, state)
    struct.pack_into('<H', expected, OBJECT + 0x50E4 - BASE, small)
    actual = bytearray(machine.mem_read(BASE, 0x400000))
    actual[entry - BASE:entry - BASE + len(code)] = bytes(len(code))
    if actual != expected:
        raise AssertionError('Independent complete data-RAM model differs')
    final = [machine.reg_read(UC_ARM_REG_R0 + index) for index in range(13)]
    if final[4:12] != registers[4:12]:
        raise AssertionError('Caller did not preserve required registers')
    return {'actualReturn': True, 'instructions': len(trace), 'result': result, 'calls': calls,
            'registers': final, 'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'sp': sp,
            'dataRamSha256': digest(actual), 'stackSha256': digest(bytes(machine.mem_read(STACK, 0x20000))),
            'orderedWritesSha256': digest(json.dumps(writes).encode()), 'pcTraceSha256': digest(json.dumps(trace).encode())}


def vectors(entry):
    if entry == 0x021D761C:
        for event in (0, 1, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 30, 38, 0x80, 0x81, -1):
            for value in (0, 1, 2, 10, 11, 12, 13, -2147483648, 0x7FFFFFFF):
                yield {'event': event, 'value': value, 'state': (event * 31) & 0xFFFFFFFF,
                       'small': 0xABCD, 'packet': False, 'packetWord': 0, 'accepted': 0}
    else:
        for packet in (False, True):
            for value in (0, 1, 2, 0x7FFF, 0x8000, 0xFFFF):
                for accepted in (0, 1, 0x80000000, 0xFFFFFFFF):
                    yield {'event': 0, 'value': 0, 'state': 0x10203040, 'small': 0xABCD,
                           'packet': packet, 'packetWord': value, 'accepted': accepted}
