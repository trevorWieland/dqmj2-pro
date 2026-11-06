import hashlib
import json
import random
import struct

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from ov001_reward_worker_model_20261029 import INPUT, ENTITY, model

BASE, CONTEXT, STACK, STOP = 0x02000000, 0x02238CD4, 0x03010000, 0x07000000


def digest(value):
    return hashlib.sha256(value).hexdigest()


def execute(main, overlay, address, code, bindings, vector):
    rng = random.Random(vector['seed'])
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base, size in ((BASE, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(base, size)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(address, code)
    machine.mem_write(CONTEXT, vector['context'])
    machine.mem_write(INPUT, struct.pack('<HH', 0, vector['keys']))
    entity = bytearray(0x40)
    struct.pack_into('<I', entity, 0x1C, vector['entityWord'])
    entity[0x23] = 7
    machine.mem_write(ENTITY, bytes(entity))
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[0] = vector['argument']
    for position, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + position, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    expected_context, expected_entity, expected_calls = model(address, vector)
    expected_ram = bytearray(machine.mem_read(BASE, 0x400000))
    expected_ram[CONTEXT - BASE:CONTEXT - BASE + 0x38] = expected_context
    expected_ram[ENTITY - BASE:ENTITY - BASE + 0x40] = expected_entity
    providers = {int(binding['address'], 0): binding for binding in bindings.values() if binding['kind'] == 'function'}
    calls, trace, writes = [], [], []

    def step(engine, pc, size, unused):
        trace.append(pc)
        if pc in providers:
            if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (providers[pc]['mode'] == 'thumb'):
                raise ValueError('Provider entered with incorrect qualified native mode')
            calls.append({'address': pc, 'arguments': [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(4)]})
            engine.reg_write(UC_ARM_REG_R0, vector['returns'].get(pc, 0))
            lr = engine.reg_read(UC_ARM_REG_LR)
            engine.reg_write(UC_ARM_REG_CPSR, engine.reg_read(UC_ARM_REG_CPSR) & ~32 | (32 if lr & 1 else 0))
            engine.reg_write(UC_ARM_REG_PC, lr & ~1)
        elif not address <= pc < address + len(code):
            raise ValueError('Reward caller escaped its explicit caller/provider domains')

    def written(engine, access, destination, size, value, unused):
        allowed = [(STACK, 0x10000), (CONTEXT, 0x38), (ENTITY, 0x40)]
        if not any(base <= destination and destination + size <= base + length for base, length in allowed):
            raise ValueError('Reward caller wrote outside bounded declared state')
        writes.append((destination, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(address, STOP, count=10000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError('Reward caller did not actually return with restored SP')
    if machine.reg_read(UC_ARM_REG_R0) != 0:
        raise ValueError('Reward caller return differs from independent zero result')
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError('Reward caller changed preserved registers')
    ram = bytes(machine.mem_read(BASE, 0x400000))
    if ram != expected_ram or [item['address'] for item in calls] != [item['address'] for item in expected_calls]:
        raise ValueError(('Independent transition/call-order model differs', hex(address), vector['seed'], calls, expected_calls))
    for actual, expected in zip(calls, expected_calls):
        if actual['arguments'][:len(expected['arguments'])] != expected['arguments']:
            raise ValueError(('Independent call-argument model differs', hex(address), vector['seed'], actual, expected))
    return {'actualReturn': True, 'instructions': len(trace), 'providerCalls': calls,
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'seed': vector['seed'],
            'initialContext': vector['context'].hex(), 'finalContext': expected_context.hex(),
            'wholeRamSha256': digest(ram), 'wholeStackSha256': digest(bytes(machine.mem_read(0x03000000, 0x20000))),
            'pcTraceSha256': digest(json.dumps(trace).encode()), 'writeTraceSha256': digest(json.dumps(writes).encode())}
