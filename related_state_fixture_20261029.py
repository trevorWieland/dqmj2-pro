import json
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from reward_state_fixture_20261029 import BASE, CONTEXT, STACK, STOP, digest


def vectors(kind):
    states = [*range(14), 128, 255] if kind == 'selector' else [0, 5, 10, 20, 30, 40, 50, 100, 101, 255]
    for state in states:
        for variant in range(32):
            seed = 2026102938100 + state * 32 + variant
            rng = random.Random(seed)
            context = bytearray(rng.randbytes(0x38))
            context[2 if kind == 'selector' else 0x13] = state
            context[0x12] = [0, 1, 29, 30, 254, 255, 2, 31][variant % 8]
            struct.pack_into('<i', context, 0x2C, [0, 1, 300, 65535][variant % 4])
            yield {'seed': seed, 'context': bytes(context), 'reason': [0, 4, 5, 6, 7, 8, 255, 0xFFFFFFFF][variant % 8],
                   'alternate': variant >> 3 & 1, 'ready': variant >> 4 & 1,
                   'complete': variant & 1}


def provider(vector, address, args):
    if address == 0x021DBA58:
        return 0x00100000 + args[0] * 0x100 + args[1] * 0x10
    if address == 0x021DBAC8:
        return 0x00200000 + args[0] * 0x100
    return {0x020443EC: vector['reason'], 0x020444EC: vector['alternate'],
            0x021D774C: vector['ready'], 0x02041800: vector['complete']}.get(address, 0)


def model(kind, vector):
    c = bytearray(vector['context'])
    calls = []

    def call(address, *args):
        args = [value & 0xFFFFFFFF for value in args]
        calls.append({'address': address, 'args': args})
        return provider(vector, address, args)

    if kind == 'selector':
        call(0x021F112C, 2)
        a, b = call(0x021DBA58, 0, 2), call(0x021DBA58, 1, 2)
        d, e = call(0x021DBA58, 0, 1), call(0x021DBA58, 1, 1)
        f, g = call(0x021DBAC8, 0), call(0x021DBAC8, 1)
        if c[2] not in (6, 7):
            call(0x0205F210, 1, 1)
        call(0x021F92B8)
        state = c[2]
        if state in (0, 1, 2):
            call(0x021E36C4, 42, 11 if state == 2 else 7, f, a, d)
            if state != 2:
                call(0x021E35B4, 20 + state)
            call(0x021F9350, state)
            if state == 0:
                reason = call(0x020443EC)
                alternate = call(0x020444EC)
                c[0x16] = 13 if alternate else {5: 13, 6: 14, 7: 16}.get(reason, 1)
            else:
                c[0x16] = state + 1
        elif state in (3, 4, 6, 7):
            c[0x16] = {3: 4, 4: 4, 6: 5, 7: 6}[state]
        elif state in (5, 8, 9):
            call(0x021E36C4, 42, 7, f, a, d)
            call(0x021E36C4, 48, 9, f, a, d)
            call(0x021E35B4, 21 if state == 9 else 20)
            call(0x021F9350, 3)
            c[0x16] = {5: 9, 8: 7, 9: 8}[state]
        elif state in (10, 11, 12):
            call(0x021E36C4, 42, 11, g, b, e)
            call(0x021E35B4, 20 if state == 11 else 21)
            call(0x021F9350, 3)
            c[0x16] = state
        call(0x021F1294, 16, 2)
        return bytes(c), calls, 1
    if c[0x13] == 0:
        call(0x021F1354, 1, 0, 2, 0)
        call(0x021D75D4, 42)
        call(0x021D94CC, 1, 1)
        call(0x021F949C, 222, 1)
        c[0x13] = 5
    elif c[0x13] == 5:
        call(0x02041898, 0)
        c[0x13] = 10
    if c[0x13] == 10 and call(0x021D774C, -1) == 0:
        call(0x021F14A4)
        if struct.unpack_from('<i', c, 0x2C)[0] == 0:
            call(0x02041510, 1, 2, 30)
            call(0x022139E8, 2)
            c[0x13] = 20
        else:
            c[0x13], c[0x12] = 30, 0
    if c[0x13] == 20 and call(0x02041800) != 1:
        c[0x13] = 100
    if c[0x13] == 30:
        if c[0x12] == 0:
            call(0x021F1324)
        c[0x12] = (c[0x12] + 1) & 255
        if c[0x12] >= 2:
            call(0x021F1294, 16, 2)
            c[0x13] = 40
    if c[0x13] == 40:
        amount = struct.unpack_from('<i', c, 0x2C)[0]
        call(0x02048094, amount, 0)
        call(0x021F1354, 1, 0, 22, 0)
        call(0x021E3508, -amount)
        c[0x13], c[0x12] = 50, 0
    if c[0x13] == 50:
        c[0x12] = (c[0x12] + 1) & 255
        if c[0x12] >= 30:
            call(0x021F14A4)
            call(0x02041510, 1, 2, 30)
            call(0x022139E8, 2)
            c[0x13] = 20
    if c[0x13] == 100:
        c[0x16], c[0x13] = 17, 0
    call(0x0204437C)
    call(0x0204439C)
    return bytes(c), calls, 0


def execute(kind, main, overlay, code, entry, bindings, arities, vector):
    address = int(entry['address'], 0)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE, 0x400000)
    machine.mem_map(0x03000000, 0x20000)
    machine.mem_map(STOP, 0x1000)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(address, code)
    machine.mem_write(CONTEXT, vector['context'])
    rng = random.Random(vector['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for i in range(13):
        machine.reg_write(UC_ARM_REG_R0 + i, rng.getrandbits(32))
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    providers = {int(row['address'], 0): name for name, row in bindings.items() if row['kind'] == 'function'}
    calls, trace, writes = [], [], []

    def step(engine, pc, size, unused):
        trace.append(pc)
        if pc in providers:
            name = providers[pc]
            count = arities[name]
            args = [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(min(count, 4))]
            if count > 4:
                args += list(struct.unpack('<' + 'I' * (count - 4), bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_SP), (count - 4) * 4))))
            calls.append({'address': pc, 'args': args})
            engine.reg_write(UC_ARM_REG_R0, provider(vector, pc, args))
            lr = engine.reg_read(UC_ARM_REG_LR)
            engine.reg_write(UC_ARM_REG_CPSR, engine.reg_read(UC_ARM_REG_CPSR) & ~32 | (32 if lr & 1 else 0))
            engine.reg_write(UC_ARM_REG_PC, lr & ~1)
        elif not address <= pc < address + len(code):
            raise ValueError('Related state unit escaped caller/provider bounds')

    def written(engine, access, destination, size, value, unused):
        if not (STACK <= destination and destination + size <= STACK + 0x10000 or CONTEXT <= destination and destination + size <= CONTEXT + 0x38):
            raise ValueError('Related state unit wrote outside its fixture state')
        writes.append((destination, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(address, STOP, timeout=2000000, count=10000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise ValueError('Related state unit did not actually return')
    result = machine.reg_read(UC_ARM_REG_R0)
    actual = (bytes(machine.mem_read(CONTEXT, 0x38)), calls, result)
    if actual != model(kind, vector):
        raise ValueError(('Independent related state model differs', kind, vector['seed'], actual, model(kind, vector)))
    return {'actualReturn': True, 'instructions': len(trace), 'initialState': vector['context'][2 if kind == 'selector' else 0x13],
            'returnValue': result, 'calls': calls,
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'sp': machine.reg_read(UC_ARM_REG_SP), 'lr': machine.reg_read(UC_ARM_REG_LR),
            'pc': machine.reg_read(UC_ARM_REG_PC), 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'wholeRamSha256': digest(bytes(machine.mem_read(BASE, 0x400000))),
            'wholeStackSha256': digest(bytes(machine.mem_read(0x03000000, 0x20000))),
            'pcTraceSha256': digest(json.dumps(trace).encode()), 'writeTraceSha256': digest(json.dumps(writes).encode())}
