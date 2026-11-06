import hashlib
import json
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946


BASE, ENTRY, CONTEXT = 0x02000000, 0x021E4EB0, 0x02238CD4
MARKER, ITEMS, INPUT, ENTITY = 0x0222EC40, 0x02238D10, 0x023E0000, 0x023E1000
STACK, STOP = 0x03010000, 0x07000000


def digest(value):
    return hashlib.sha256(value).hexdigest()


def signed(value):
    return (value & 127) - (value & 128)


def vectors():
    for state in [*range(20), 20, 255]:
        for variant in range(32):
            seed = 2026102937000 + state * 32 + variant
            rng = random.Random(seed)
            context = bytearray(rng.randbytes(0x38))
            context[4], context[10] = state, variant & 1
            context[0x21] = [0, 1, 18, 255][variant % 4]
            context[0x22] = variant & 1
            context[0x23] = [0, 1, 20, 255][variant % 4]
            context[0x26] = [0, 1, 2, 255][variant % 4]
            struct.pack_into('<i', context, 0x30, [-1, 0, 1, 0x7FFFFFFF][variant % 4])
            marker = bytearray([0, 0, variant & 3, (variant >> 1) & 3])
            items = [0, 256, 65535] if variant & 4 else [65535, 0, 256]
            returns = {
                0x0202A634: INPUT, 0x0221F1A4: 0,
                0x021F1A44: ENTITY, 0x0205E7A8: [0, 127, 128, 255][variant % 4],
                0x021E3BE4: variant % 4, 0x021E3F68: variant & 1,
                0x0205F2D8: variant & 1, 0x021F14C0: variant & 1,
                0x021F14E4: variant & 1, 0x02041800: (variant >> 1) & 1,
                0x02213630: variant & 1, 0x021E49D0: (variant >> 1) & 1,
                0x0221175C: (variant >> 2) & 1,
                0x02212848: 0xFFFFFFFF if variant & 1 else 0,
                0x0205EB00: (variant >> 1) & 1, 0x02207058: variant & 1,
            }
            yield {'seed': seed, 'context': bytes(context), 'marker': bytes(marker),
                   'items': items, 'keys': 0xFF7 if variant & 2 else 0,
                   'entityWord': variant & 1, 'returns': returns}


def model(vector):
    c, m = bytearray(vector['context']), bytearray(vector['marker'])
    entity = bytearray(0x40)
    struct.pack_into('<I', entity, 0x1C, vector['entityWord'])
    entity[0x23] = 7
    calls = []

    def call(address):
        calls.append(address)
        return vector['returns'].get(address, 0)

    call(0x0202A634)
    if c[4] == 0:
        for a in [0x021E3B34, 0x021D75D4, 0x021D94CC, 0x021E3564, 0x02202654, 0x021DC8E8]:
            call(a)
        c[5], c[4] = 0, 1
    state = c[4]
    if state == 1 and c[10]:
        c[0x25], c[0x24] = call(0x021E3BE4) & 255, call(0x0205E7A8) & 255
        c[0x23], c[4], c[0x21] = 20, 3, 18
        call(0x02212858)
    elif state == 3 and vector['keys'] & 0xFF7:
        c[4] = 4
    elif state == 4:
        c[4] = 2 if call(0x021E3F68) == 0 else 5
    elif state == 5:
        for a in [0x021F1354, 0x021F1414, 0x021F1438, 0x02047D40, 0x020630E4]:
            call(a)
        if call(0x0205F2D8) == 0:
            call(0x021F94D8)
        c[1], c[4] = 0, 6
    elif state == 6 and call(0x021F14C0):
        c[4] = 7
    elif state == 7 and vector['keys'] & 0xFF7:
        c[4] = 8
    state = c[4]
    if state == 8:
        if c[0x26] >= 2:
            c[4] = 10
        else:
            c[0x26] += 1
            c[4] = 10 if vector['items'][c[0x26]] == 0 else 9
            if c[4] == 9:
                c[1] = 0
        call(0x021F14A4)
    elif state == 9 and call(0x021F14E4) == 0:
        c[4] = 5
    elif state == 10:
        c[4] = 2
    elif state == 2 and signed(c[0x21]) <= 0:
        call(0x021E3508)
        if struct.unpack_from('<i', c, 0x30)[0] > 0:
            c[4] = 11
        else:
            call(0x02041510)
            c[4] = 12
            call(0x022023C4)
    elif state == 12 and call(0x02041800) != 1:
        c[4] = 18
        call(0x021F1A44)
        entity[0x23] = 0
    elif state == 11:
        if call(0x0205F2D8) == 0:
            call(0x021F949C)
        call(0x022116D0)
        call(0x022023C4)
        c[4], m[2] = 13, 1
    elif state == 13:
        if call(0x02213630) == 0:
            if call(0x021E49D0):
                c[4] = 14
            else:
                call(0x022071F8)
                c[4] = 15
            call(0x021E4C34)
            call(0x021E4B34)
        else:
            if signed(c[0x23]) > 0:
                c[0x23] -= 1
            elif vector['keys'] & 0xFF7:
                m[3] = 0
                call(0x02211714)
            if call(0x0221175C):
                if not (m[2] & m[3]):
                    call(0x021F949C)
                m[2] = ((signed(m[2]) + 1) & signed(m[3])) & 255
            else:
                m[2] = 1
    elif state == 14:
        value = call(0x02212848)
        if vector['keys'] & 0xFF7:
            c[0x22] = 1
        if (value == 0xFFFFFFFF or call(0x0205EB00) == 0) and c[0x22]:
            call(0x022071F8)
            c[4] = 15
    elif state == 15 and vector['keys'] & 0xFF7:
        c[4] = 16
    if c[4] == 16 and call(0x02207058):
        for a in [0x022139E8, 0x02041510, 0x0205F210, 0x022068AC]:
            call(a)
        c[4] = 17
    if c[4] == 17 and call(0x02041800) != 1:
        c[4] = 18
        call(0x021F1A44)
        entity[0x23] = 0
    if c[4] == 18:
        call(0x021F1A44)
        if vector['entityWord'] == 0:
            c[4] = 19
    if c[4] == 19:
        call(0x021E3BD0)
        if c[0x26]:
            call(0x021F14A4)
        c[0x16], c[4], c[0x26] = 17, 0, 0
    if signed(c[0x21]) > 0:
        c[0x21] -= 1
    call(0x0204437C)
    call(0x0204439C)
    return bytes(c), bytes(m), bytes(entity), calls


def execute(main, overlay, code, bindings, vector):
    rng = random.Random(vector['seed'])
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE, 0x400000)
    machine.mem_map(0x03000000, 0x20000)
    machine.mem_map(STOP, 0x1000)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ENTRY, code)
    machine.mem_write(CONTEXT, vector['context'])
    machine.mem_write(MARKER, vector['marker'])
    machine.mem_write(ITEMS, struct.pack('<256H', *vector['items'], *([0] * 253)))
    machine.mem_write(INPUT, struct.pack('<HH', 0, vector['keys']))
    entity = bytearray(0x40)
    struct.pack_into('<I', entity, 0x1C, vector['entityWord'])
    entity[0x23] = 7
    machine.mem_write(ENTITY, bytes(entity))
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    for i in range(13):
        machine.reg_write(UC_ARM_REG_R0 + i, rng.getrandbits(32))
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    providers = {int(b['address'], 0): name for name, b in bindings.items() if b['kind'] == 'function'}
    calls, trace, writes = [], [], []

    def step(engine, pc, size, unused):
        trace.append(pc)
        if pc in providers:
            calls.append({'address': pc, 'arguments': [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(4)]})
            engine.reg_write(UC_ARM_REG_R0, vector['returns'].get(pc, 0))
            lr = engine.reg_read(UC_ARM_REG_LR)
            engine.reg_write(UC_ARM_REG_CPSR, engine.reg_read(UC_ARM_REG_CPSR) & ~32 | (32 if lr & 1 else 0))
            engine.reg_write(UC_ARM_REG_PC, lr & ~1)
        elif not ENTRY <= pc < ENTRY + len(code):
            raise ValueError('Reward unit escaped its bounded caller/provider contracts')

    def written(engine, access, address, size, value, unused):
        allowed = [(STACK, 0x10000), (CONTEXT, 0x38), (MARKER, 4), (ENTITY, 0x40)]
        if not any(start <= address and address + size <= start + length for start, length in allowed):
            raise ValueError('Reward caller wrote outside declared fixture state')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP, timeout=2000000, count=10000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise ValueError('Reward caller did not actually return')
    actual = (bytes(machine.mem_read(CONTEXT, 0x38)), bytes(machine.mem_read(MARKER, 4)),
              bytes(machine.mem_read(ENTITY, 0x40)), [item['address'] for item in calls])
    if actual != model(vector):
        raise ValueError(('Independent reward transition model differs', vector['seed'], actual, model(vector)))
    for call in calls:
        if call['address'] in (0x02047D40, 0x020630E4):
            index = vector['context'][0x26]
            item = vector['items'][index] if index < 3 else 0
            if call['arguments'][0] != item or call['address'] == 0x020630E4 and call['arguments'][1] != 1:
                raise ValueError('Native item table width or mutation delta differs')
    return {'actualReturn': True, 'instructions': len(trace), 'initialState': vector['context'][4],
            'finalState': actual[0][4], 'providerCalls': calls,
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'sp': machine.reg_read(UC_ARM_REG_SP), 'lr': machine.reg_read(UC_ARM_REG_LR),
            'pc': machine.reg_read(UC_ARM_REG_PC), 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'wholeRamSha256': digest(bytes(machine.mem_read(BASE, 0x400000))),
            'wholeStackSha256': digest(bytes(machine.mem_read(0x03000000, 0x20000))),
            'pcTraceSha256': digest(json.dumps(trace).encode()),
            'writeTraceSha256': digest(json.dumps(writes).encode())}
