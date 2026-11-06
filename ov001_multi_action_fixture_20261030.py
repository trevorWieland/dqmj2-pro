import hashlib
import json
import random
import struct

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from ov001_multi_action_model_20261030 import CONTEXT, ACTOR, OPPONENTS, MOTION, MOTION_INFO, DESCRIPTOR, FLAGS, model

BASE, ADDRESS, STACK, STOP = 0x02000000, 0x021EC6C0, 0x03010000, 0x07000000


def execute(main, overlay, code, bindings, vector):
    rng = random.Random(vector['seed'])
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base, size in ((BASE, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(base, size)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ADDRESS, code)
    machine.mem_write(CONTEXT, vector['context'])
    machine.mem_write(ACTOR, vector['actor'])
    for index, data in enumerate(vector['opponents']):
        machine.mem_write(OPPONENTS + index * 1088, data)
    machine.mem_write(FLAGS, vector['flags'])
    motion = bytearray(rng.randbytes(32))
    struct.pack_into('<i', motion, 0, vector['clock'])
    struct.pack_into('<I', motion, 8, MOTION_INFO)
    machine.mem_write(MOTION, bytes(motion))
    info = bytearray(rng.randbytes(16))
    struct.pack_into('<H', info, 4, vector['frames'])
    machine.mem_write(MOTION_INFO, bytes(info))
    descriptor = bytearray(rng.randbytes(40))
    struct.pack_into('<h', descriptor, 12, vector['song'])
    machine.mem_write(DESCRIPTOR, bytes(descriptor))
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    for index, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    context, opponents, flags, expected_calls = model(vector)
    expected_ram = bytearray(machine.mem_read(BASE, 0x400000))
    expected_ram[CONTEXT - BASE:CONTEXT - BASE + len(context)] = context
    expected_ram[FLAGS - BASE:FLAGS - BASE + len(flags)] = flags
    for index, data in enumerate(opponents):
        offset = OPPONENTS + index * 1088 - BASE
        expected_ram[offset:offset + len(data)] = data
    providers = {int(item['address'], 0): item for item in bindings.values() if item['kind'] == 'function'}
    calls, trace, writes = [], [], []

    def step(engine, pc, size, unused):
        trace.append(pc)
        if pc in providers:
            if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (providers[pc]['mode'] == 'thumb'):
                raise ValueError('Qualified action provider entered with wrong native mode')
            arguments = [engine.reg_read(UC_ARM_REG_R0 + index) for index in range(4)]
            if pc == 0x0220F600:
                arguments.append(struct.unpack('<I', bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_SP), 4)))[0])
            calls.append({'address': pc, 'arguments': arguments})
            if pc == 0x0207AFEC:
                result = DESCRIPTOR
            elif pc == 0x021D9534:
                result = vector['eventHit'] if arguments[2] == 1 else vector['eventEnd']
            elif pc == 0x021DB438:
                if arguments[0] not in (0, 1) or arguments[1] not in (0, 1, 2):
                    raise ValueError('Actor provider domain exceeded')
                result = OPPONENTS + arguments[1] * 1088
            elif pc in (0x021DB8D0, 0x021DBD24):
                index = (arguments[0] - OPPONENTS) // 1088
                if arguments[0] != OPPONENTS + index * 1088 or index not in (0, 1, 2):
                    raise ValueError('Actor-query pointer domain exceeded')
                result = vector['valid' if pc == 0x021DB8D0 else 'spent'][index]
            else:
                result = int(vector['returns'].get(pc, 0))
            engine.reg_write(UC_ARM_REG_R0, result & 0xFFFFFFFF)
            lr = engine.reg_read(UC_ARM_REG_LR)
            engine.reg_write(UC_ARM_REG_CPSR, engine.reg_read(UC_ARM_REG_CPSR) & ~32 | (32 if lr & 1 else 0))
            engine.reg_write(UC_ARM_REG_PC, lr & ~1)
        elif not ADDRESS <= pc < ADDRESS + 1364:
            raise ValueError('Action scheduler escaped its native/provider domains')

    def written(engine, access, destination, size, value, unused):
        allowed = [(STACK, 0x10000), (CONTEXT, 0x98), (FLAGS, 3), (OPPONENTS, 3 * 1088)]
        if not any(base <= destination and destination + size <= base + length for base, length in allowed):
            raise ValueError('Action scheduler wrote outside bounded state/frame')
        writes.append((destination, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ADDRESS, STOP, count=10000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError('Action scheduler did not actually return with restored SP')
    if machine.reg_read(UC_ARM_REG_R0) != 0:
        raise ValueError('Action scheduler physical zero result differs')
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError('Action scheduler changed preserved registers')
    ram = bytes(machine.mem_read(BASE, 0x400000))
    if ram != expected_ram or [item['address'] for item in calls] != [item['address'] for item in expected_calls]:
        raise ValueError(('Independent complete memory/call-order model differs', vector['seed'], calls, expected_calls))
    for actual, expected in zip(calls, expected_calls):
        if actual['arguments'][:len(expected['arguments'])] != expected['arguments']:
            raise ValueError(('Independent consumed-argument model differs', vector['seed'], actual, expected))
    return {'seed': vector['seed'], 'actualReturn': True, 'instructions': len(trace),
            'providerCalls': calls, 'initialState': vector['context'][3], 'finalState': context[3],
            'finalContext': context.hex(),
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'wholeRamSha256': hashlib.sha256(ram).hexdigest(),
            'wholeStackSha256': hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
            'traceSha256': hashlib.sha256(json.dumps(trace).encode()).hexdigest(),
            'writesSha256': hashlib.sha256(json.dumps(writes).encode()).hexdigest()}
