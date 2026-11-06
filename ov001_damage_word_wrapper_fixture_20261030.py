import hashlib
import json
import random
import struct

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946

BASE, ADDRESS, SP, STOP = 0x02000000, 0x021F0818, 0x0301FFF0, 0x07000000


def vectors():
    result = []
    for index in range(160):
        rng = random.Random(610000 + index)
        words = [rng.getrandbits(32) for unused in range(8)]
        if index < 32:
            words = [1 << index] * 8
        elif index < 40:
            words = [0xFFFFFFFF if slot == index - 32 else 0 for slot in range(8)]
        result.append({'seed': 610000 + index, 'words': words, 'result': rng.getrandbits(32)})
    return result


def execute(main, overlay, code, bindings, vector):
    rng = random.Random(vector['seed'])
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base, size in ((BASE, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(base, size)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ADDRESS, code)
    stack = bytearray(rng.randbytes(0x20000))
    words = vector['words']
    struct.pack_into('<4I', stack, SP - 0x03000000, *words[4:])
    machine.mem_write(0x03000000, bytes(stack))
    packet = words[:4] + [0, words[4], 0, 0, words[5], words[6], words[7]]
    struct.pack_into('<8I', stack, SP - 32 - 0x03000000, *packet[4:], STOP)
    registers = words[:4] + [rng.getrandbits(32) for unused in range(9)]
    for position, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + position, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    initial_ram = bytes(machine.mem_read(BASE, 0x400000))
    providers = {int(item['address'], 0): item for item in bindings.values() if item['kind'] == 'function'}
    calls, trace, writes = [], [], []

    def step(engine, pc, size, unused):
        trace.append(pc)
        if pc == 0x021F0578:
            if pc not in providers or providers[pc]['mode'] != 'arm' or engine.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('Core provider qualification differs')
            call_sp = engine.reg_read(UC_ARM_REG_SP)
            arguments = [engine.reg_read(UC_ARM_REG_R0 + index) for index in range(4)]
            arguments += list(struct.unpack('<7I', bytes(engine.mem_read(call_sp, 28))))
            if arguments != packet:
                raise ValueError(('Eleven-word forwarding model differs', arguments, packet))
            calls.append(arguments)
            engine.reg_write(UC_ARM_REG_R0, vector['result'])
            engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))
        elif not ADDRESS <= pc < ADDRESS + 64:
            raise ValueError('Wrapper escaped its bounded native/provider domain')

    def written(engine, access, destination, size, value, unused):
        if not SP - 32 <= destination or destination + size > SP:
            raise ValueError('Wrapper wrote outside its 32-byte stack frame')
        writes.append((destination, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ADDRESS, STOP, count=1000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or len(calls) != 1:
        raise ValueError('Wrapper did not actually return once')
    if machine.reg_read(UC_ARM_REG_R0) != vector['result']:
        raise ValueError('Wrapper did not forward the physical core result')
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError('Wrapper changed preserved registers')
    ram = bytes(machine.mem_read(BASE, 0x400000))
    observed_stack = bytes(machine.mem_read(0x03000000, 0x20000))
    if ram != initial_ram or observed_stack != bytes(stack):
        raise ValueError('Independent complete memory model differs')
    return {'seed': vector['seed'], 'actualReturn': True, 'instructions': len(trace),
            'forwardedWords': calls[0], 'physicalR0': vector['result'],
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'wholeRamSha256': hashlib.sha256(ram).hexdigest(),
            'wholeStackSha256': hashlib.sha256(observed_stack).hexdigest(),
            'traceSha256': hashlib.sha256(json.dumps(trace).encode()).hexdigest(),
            'writesSha256': hashlib.sha256(json.dumps(writes).encode()).hexdigest()}
