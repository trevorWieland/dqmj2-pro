import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE, ENTRY, STATE, DATA, STACK, STOP, CALLBACK = 0x02000000, 0x0200DED8, 0x020E53D0, 0x02400000, 0x03030000, 0x0F000000, 0x0240F000
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
    UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
    UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]
PROVIDERS = {0x02007FF4: 0, 0x02008008: 1, 0x0200A440: 3, CALLBACK: 3}


def inputs(index):
    rng = random.Random(0xDED80000 + index)
    page, data = bytearray(rng.randbytes(4096)), bytearray(rng.randbytes(65536))
    vcount = [0, 1, 191, 263, 65535][index % 5]
    frequency = [0, 1, 127, 128, 255, 256, 65535][index // 5 % 7]
    size = [0, 1, 2, 7][index // 35 % 4]
    first = [-1, 0, 1, -2147483648][index // 140 % 4]
    second = [-1, 0, 1][index // 560 % 3]
    callback = CALLBACK if index // 1680 % 2 else 0
    offset = STATE % 4096
    struct.pack_into('<I', page, offset + 4, callback)
    expected_page, expected_data = bytearray(page), bytearray(data)
    struct.pack_into('<HHI H', expected_page, offset + 16, 0, frequency, DATA + 0x1000, size)
    for i in range(size): struct.pack_into('<H', expected_data, 0x1000 + i * 8 + 4, 0)
    success = first >= 0 and second >= 0
    flags = struct.unpack_from('<H', expected_page, offset + 0x38)[0]
    struct.pack_into('<H', expected_page, offset + 0x38, flags & ~2 if success else flags | 2)
    if success:
        command = struct.unpack_from('<H', expected_page, offset + 0x3A)[0]
        struct.pack_into('<H', expected_page, offset + 0x3A, command | 2)
    return rng, bytes(page), bytes(data), bytes(expected_page), bytes(expected_data), [vcount, frequency, DATA + 0x1000, size], first, second, callback


def execute(image, body, index, bound=4000):
    rng, page, data, expected_page, expected_data, args, first, second, callback = inputs(index)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(BASE, 0x100000)
    uc.mem_write(BASE, image)
    uc.mem_write(ENTRY, body)
    uc.mem_write(STATE & ~4095, page)
    uc.mem_map(DATA, 65536)
    uc.mem_write(DATA, data)
    uc.mem_map(STACK, 4096)
    uc.mem_write(STACK, rng.randbytes(4096))
    uc.mem_map(STOP, 4096)
    uc.mem_write(STOP, b'\x70\x00\x20\xe1')
    values = [rng.getrandbits(32) for _ in REGS]
    for reg, value in zip(REGS, values): uc.reg_write(reg, value)
    for reg, value in zip(REGS, args): uc.reg_write(reg, value)
    uc.reg_write(UC_ARM_REG_CPSR, (rng.getrandbits(4) << 28) | 0x10)
    uc.reg_write(UC_ARM_REG_SP, STACK + 0x800)
    uc.reg_write(UC_ARM_REG_LR, STOP)
    token = rng.getrandbits(32)
    state = dict(returned=False, calls=[], writes=[], pcs=[], pxi=0)

    def code(machine, address, size, unused):
        if address == STOP:
            state['returned'] = True
            machine.emu_stop()
            return
        if ENTRY <= address < ENTRY + len(body) - 4:
            state['pcs'].append(address)
            return
        assert address in PROVIDERS, hex(address)
        values = [machine.reg_read(r) for r in REGS[:PROVIDERS[address]]]
        state['calls'].append((address, values))
        result = rng.getrandbits(32)
        if address == 0x02007FF4: result = token
        elif address == 0x0200A440:
            result = [first, second][state['pxi']] & 0xFFFFFFFF
            state['pxi'] += 1
        for reg in [UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]:
            machine.reg_write(reg, rng.getrandbits(32))
        machine.reg_write(UC_ARM_REG_R0, result)
        machine.reg_write(UC_ARM_REG_CPSR, (rng.getrandbits(4) << 28) | 0x10)
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    def write(machine, access, address, size, value, unused):
        assert STACK <= address < STACK + 4096 or STATE <= address < STATE + 64 or DATA <= address < DATA + 65536
        state['writes'].append((address, size, value))

    uc.hook_add(UC_HOOK_CODE, code)
    uc.hook_add(UC_HOOK_MEM_WRITE, write)
    uc.emu_start(ENTRY, STOP + 4, count=bound)
    assert state['returned'], 'Bounded prefix is not a return'
    calls = [(0x02007FF4, []), (0x0200A440, [6, 0x02000100 | (args[1] & 255), 0])]
    if first >= 0: calls.append((0x0200A440, [6, 0x01010000 | args[0], 0]))
    calls.append((0x02008008, [token]))
    if (first < 0 or second < 0) and callback: calls.append((CALLBACK, [1, 4, 0]))
    actual_page, actual_data = bytes(uc.mem_read(STATE & ~4095, 4096)), bytes(uc.mem_read(DATA, 65536))
    result = [uc.reg_read(r) for r in REGS]
    passed = actual_page == expected_page and actual_data == expected_data and state['calls'] == calls
    passed &= result[4:12] == values[4:12] and uc.reg_read(UC_ARM_REG_SP) == STACK + 0x800
    return dict(actualReturn=True, modelPassed=bool(passed), registers=result, flags=uc.reg_read(UC_ARM_REG_CPSR),
        calls=state['calls'], writes=state['writes'], observedInstructionAddresses=sorted(set(state['pcs'])),
        stateSha256=hashlib.sha256(actual_page).hexdigest(), dataSha256=hashlib.sha256(actual_data).hexdigest(),
        stackSha256=hashlib.sha256(bytes(uc.mem_read(STACK, 4096))).hexdigest(),
        suppliedBoundaryCalls=len(calls), actualNativeLowerReturns=0)
