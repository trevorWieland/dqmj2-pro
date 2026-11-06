import hashlib
import json
import random
import struct

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946

BASE, CONTEXT, ACTOR, TARGET = 0x02000000, 0x02239A14, 0x02360000, 0x02361000
STACK, STOP = 0x03010000, 0x07000000


def vectors():
    result = []
    for mode in (0, 1, 2, 3, 4, 255, 0x80000000, 0xFFFFFFFF):
        for category in (0, 1, 2, 3, 0xFFFFFFFF):
            for present, state in ((0, 0), (0, 1), (1, 0), (1, 1), (0xFFFFFFFF, 2)):
                seed = len(result) + 510000
                rng = random.Random(seed)
                result.append({'seed': seed, 'mode': mode, 'category': category,
                               'present': present, 'actorState': state,
                               'x': rng.getrandbits(32), 'y': rng.getrandbits(32),
                               'result': (0, 1, 0x7FFFFFFF, 0xFFFFFFFF)[seed % 4]})
    return result


def model(vector):
    calls = []

    def call(address, *arguments):
        calls.append({'address': address, 'arguments': list(arguments)})

    mode, category = vector['mode'], vector['category']
    if mode == 0:
        actor = ACTOR
        call(0x021DB9E0, actor)
        call(0x021DBAAC, actor)
        camera = (8 if vector['actorState'] == 1 else 9) if vector['present'] else (7 if category == 2 else 6 if category == 1 else 5)
        flag = 0
    elif mode == 1:
        actor = TARGET
        call(0x021DB9E0, actor)
        camera = 12 if category == 2 else 11 if category == 1 else 10
        flag = 1
    elif mode == 2:
        call(0x021D75D4, 13)
        call(0x021D94CC, 1, 1)
        return calls, vector['result']
    else:
        return calls, mode
    call(0x021D75D4, camera)
    call(0x02042C2C, actor)
    call(0x021D77B0, 0xFFFFFFFF, vector['x'])
    call(0x02041F74, actor, 0)
    call(0x021D7814, 0xFFFFFFFF, vector['y'])
    call(0x021D94CC, 1, flag)
    return calls, vector['result']


def execute(main, overlay, code, bindings, vector):
    rng = random.Random(vector['seed'])
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base, size in ((BASE, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(base, size)
    address = 0x021F9EF0
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(address, code)
    context = bytearray(rng.randbytes(0x100))
    struct.pack_into('<I', context, 0x34, ACTOR)
    struct.pack_into('<I', context, 0x40, TARGET)
    machine.mem_write(CONTEXT, bytes(context))
    for actor in (ACTOR, TARGET):
        data = bytearray(rng.randbytes(1088))
        data[0x31E] = vector['actorState']
        machine.mem_write(actor, bytes(data))
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[0] = vector['mode']
    for index, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    before = bytes(machine.mem_read(BASE, 0x400000))
    expected_calls, expected_r0 = model(vector)
    providers = {int(item['address'], 0): item for item in bindings.values() if item['kind'] == 'function'}
    returns = {0x021DB9E0: vector['category'], 0x021DBAAC: vector['present'],
               0x02042C2C: vector['x'], 0x02041F74: vector['y'], 0x021D94CC: vector['result']}
    calls, trace, writes = [], [], []

    def step(engine, pc, size, unused):
        trace.append(pc)
        if pc in providers:
            if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (providers[pc]['mode'] == 'thumb'):
                raise ValueError('Qualified provider mode differs')
            calls.append({'address': pc, 'arguments': [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(4)]})
            engine.reg_write(UC_ARM_REG_R0, returns.get(pc, 0))
            lr = engine.reg_read(UC_ARM_REG_LR)
            engine.reg_write(UC_ARM_REG_CPSR, engine.reg_read(UC_ARM_REG_CPSR) & ~32 | (32 if lr & 1 else 0))
            engine.reg_write(UC_ARM_REG_PC, lr & ~1)
        elif not address <= pc < address + len(code):
            raise ValueError('Scout setup escaped its caller/provider domain')

    def written(engine, access, destination, size, value, unused):
        if not STACK <= destination or destination + size > STACK + 0x10000:
            raise ValueError('Scout setup wrote outside bounded stack')
        writes.append((destination, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(address, STOP, count=10000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError('Scout setup did not return with restored stack')
    if machine.reg_read(UC_ARM_REG_R0) != expected_r0:
        raise ValueError('Physical R0 differs from bounded model')
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError('Preserved registers differ')
    after = bytes(machine.mem_read(BASE, 0x400000))
    if before != after or [item['address'] for item in calls] != [item['address'] for item in expected_calls]:
        raise ValueError(('Independent memory/call-order model differs', vector, calls, expected_calls))
    for actual, expected in zip(calls, expected_calls):
        if actual['arguments'][:len(expected['arguments'])] != expected['arguments']:
            raise ValueError(('Independent argument model differs', vector, actual, expected))
    return {'seed': vector['seed'], 'actualReturn': True, 'instructions': len(trace),
            'providerCalls': calls, 'physicalR0': expected_r0,
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'wholeRamSha256': hashlib.sha256(after).hexdigest(),
            'wholeStackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'traceSha256': hashlib.sha256(json.dumps(trace).encode()).hexdigest(),
            'writesSha256': hashlib.sha256(json.dumps(writes).encode()).hexdigest()}
