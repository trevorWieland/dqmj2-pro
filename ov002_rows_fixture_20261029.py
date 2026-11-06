import json
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from reward_state_fixture_20261029 import BASE, STACK, STOP, digest

ENTRY, OBJECT, FIRST, LAST = 0x021D7F98, 0x023E0000, 0x021D7998, 0x021D7A50


def signed(value, bits):
    return (value & ((1 << (bits - 1)) - 1)) - (value & (1 << (bits - 1)))


def expected(arguments, field):
    obj, saved, count, x, y, height, extra = arguments
    result = [(FIRST, [4, signed(field, 8), 12, (x - 1) & 255, (y - 1) & 255,
                       (height + 2) & 255, (count * 2 + 2) & 255, 1, 0])]
    for index in range(count):
        result.append((FIRST, [signed(index + 5, 8), signed(field, 8), 1, x,
                               (y + index * 2) & 255, height, 2, 0, 1]))
    result.append((LAST, [obj, saved, count, 5, 0, 1, 0, extra]))
    return [(address, [value & 0xFFFFFFFF for value in words]) for address, words in result]


def execute(main, overlay, code, arguments, field, vector, require_return=True):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE, 0x400000)
    machine.mem_map(0x03000000, 0x20000)
    machine.mem_map(STOP, 0x1000)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ENTRY, code)
    machine.mem_write(OBJECT, bytes(16) + bytes([field]) + bytes(47))
    rng = random.Random(202610294100 + vector)
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for index in range(13):
        machine.reg_write(UC_ARM_REG_R0 + index, rng.getrandbits(32))
    for index, value in enumerate(arguments[:4]):
        machine.reg_write(UC_ARM_REG_R0 + index, value & 0xFFFFFFFF)
    sp = STACK + 0xFFF0
    machine.mem_write(sp, struct.pack('<3I', *[value & 0xFFFFFFFF for value in arguments[4:]]))
    machine.reg_write(UC_ARM_REG_SP, sp)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    initial = bytes(machine.mem_read(BASE, 0x400000))
    calls, trace, writes = [], [], []

    def step(engine, pc, size, unused):
        trace.append(pc)
        if pc in (FIRST, LAST):
            count = 9 if pc == FIRST else 8
            words = [engine.reg_read(UC_ARM_REG_R0 + index) for index in range(4)]
            words += list(struct.unpack('<' + 'I' * (count - 4), bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_SP), (count - 4) * 4))))
            calls.append((pc, words))
            engine.reg_write(UC_ARM_REG_R0, 0x01234567 if pc == FIRST else 0x89ABCDEF)
            engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))
        elif not ENTRY <= pc < ENTRY + len(code):
            raise ValueError('Overlay2 row caller escaped measured function/provider bounds')

    def written(engine, access, destination, size, value, unused):
        if not STACK <= destination or destination + size > STACK + 0x10000:
            raise ValueError('Overlay2 row caller wrote outside its stack')
        writes.append((destination, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP, timeout=2000000, count=20000)
    returned = machine.reg_read(UC_ARM_REG_PC) == STOP
    if not require_return:
        if returned:
            raise ValueError('Wrapping count unexpectedly returned')
        return {'actualReturn': False, 'instructionCap': 20000, 'observedInstructions': len(trace),
                'callsBeforeBoundary': len(calls), 'postBoundaryStateUsedForProof': False}
    if not returned:
        raise ValueError('Overlay2 row caller did not actually return')
    if calls != expected(arguments, field):
        raise ValueError(('Overlay2 row caller argument model differs', vector, calls, expected(arguments, field)))
    if bytes(machine.mem_read(BASE, 0x400000)) != initial:
        raise ValueError('Overlay2 row caller modified persistent RAM')
    return {'actualReturn': True, 'instructions': len(trace), 'calls': calls,
            'registers': [machine.reg_read(UC_ARM_REG_R0 + index) for index in range(13)],
            'sp': machine.reg_read(UC_ARM_REG_SP), 'lr': machine.reg_read(UC_ARM_REG_LR),
            'pc': machine.reg_read(UC_ARM_REG_PC), 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'wholeRamSha256': digest(initial), 'stackSha256': digest(bytes(machine.mem_read(0x03000000, 0x20000))),
            'traceSha256': digest(json.dumps(trace).encode()), 'writesSha256': digest(json.dumps(writes).encode())}


def vectors():
    for count in (0, 1, 2, 6, 127, 128, 250, 255):
        for variant in range(8):
            byte = (0, 1, 127, 128, 254, 255, 3, 19)[variant]
            yield [OBJECT, (0, -1, 0x7FFFFFFF, -2147483648)[variant % 4], count,
                   byte, 255 - byte, (0, -1, 0x7FFFFFFF, -2147483648)[variant % 4],
                   (0, -1, 0x80000000, 12345)[variant % 4]], byte
