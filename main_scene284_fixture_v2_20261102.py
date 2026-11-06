import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, BASE, GLOBAL, STACK, STOP = 0x0203DB28, 0x02000000, 0x020F6054, 0x03030000, 0x0F000000
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
    UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
    UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]
CALLS = [0x02211098, 0x021E33D8, 0x021E7AEC, 0x021DF4EC, 0x021DF3F4, 0x0202AC08,
    0x0203D310, 0x0203D324, 0x0203D338, 0x021DF200, 0x020407FC, 0x021E725C,
    0x02212B20, 0x021D900C, 0x021D92B4, 0x021D9580, 0x021E4014, 0x021D9088,
    0x021DA454, 0x021DD4BC, 0x021D966C, 0x021DEA48, 0x0205BFD4, 0x021D99AC,
    0x021E4D04, 0x020C55DC, 0x02066E98, 0x02066C64, 0x021E7BD4, 0x02209C04,
    0x022127A8, 0x020C56F8, 0x021D8C80, 0x021E0944, 0x021E4E9C]
ARGUMENTS = {0x0202AC08: 1, 0x021DF200: 1, 0x021D900C: 1, 0x021D92B4: 1,
    0x021D9580: 1, 0x021E4014: 1, 0x021DA454: 1, 0x021DD4BC: 1, 0x021D966C: 1,
    0x021DEA48: 1, 0x021D99AC: 1, 0x021E4D04: 1, 0x02066C64: 1,
    0x021D8C80: 1, 0x021E0944: 1, 0x021E4E9C: 1}


def scenario(index):
    rng = random.Random(0xDB280000 + index)
    first, second, threshold, final = index % 2, index // 2 % 2, index // 4 % 2, index // 8 % 2
    byte = [0, 1, 127, 128, 255][index // 16 % 5]
    signed = [0, 1, 127, 128, 255][index // 80 % 5]
    page = bytearray(rng.randbytes(4096))
    page[GLOBAL % 4096 + 12] = byte
    page[GLOBAL % 4096 + 4] = signed
    expected = bytearray(page)
    expected[GLOBAL % 4096 + 10] = 0x31 if final else 2
    calls = [(a, []) for a in CALLS[:5]]
    calls += [(0x0202AC08, [0x020F60A8])]
    calls += [(a, []) for a in CALLS[6:9]]
    calls += [(0x021DF200, [byte]), (0x020407FC, [])]
    if not first:
        calls += [(0x021E725C, []), (0x02212B20, [])]
        calls += [(a, [255]) if a != 0x021D9088 else (a, []) for a in CALLS[13:22]]
        calls += [(0x0205BFD4, []), (0x021D99AC, [2 if threshold else 0])]
    calls += [(0x021E4D04, [255]), (0x020407FC, [])]
    if not second:
        calls += [(0x020C55DC, []), (0x02066E98, []), (0x02066C64, [255])]
        calls += [(a, []) for a in CALLS[28:32]]
    calls += [(0x021D8C80, [1]), (0x021E0944, [signed if signed < 128 else signed + 0xFFFFFF00]),
        (0x021E4E9C, [128])]
    return rng, bytes(page), bytes(expected), calls, [first, second], threshold, final


def execute(image, body, index, bound=2000):
    rng, page, expected, expected_calls, queries, threshold, final = scenario(index)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE, 0x100000)
    machine.mem_write(BASE, image)
    machine.mem_write(ENTRY, body)
    machine.mem_write(GLOBAL & ~4095, page)
    machine.mem_map(0x021D0000, 0x60000)
    machine.mem_map(STACK, 4096)
    stack = rng.randbytes(4096)
    machine.mem_write(STACK, stack)
    machine.mem_map(STOP, 4096)
    machine.mem_write(STOP, b'\x70\x00\x20\xe1')
    registers = [rng.getrandbits(32) for _ in REGS]
    for reg, value in zip(REGS, registers): machine.reg_write(reg, value)
    machine.reg_write(UC_ARM_REG_CPSR, (rng.getrandbits(4) << 28) | 0x10)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0x800)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    state = dict(returned=False, calls=[], writes=[], pcs=[], queries=0)

    def code(uc, address, size, data):
        if address == STOP:
            state['returned'] = True
            uc.emu_stop()
            return
        if ENTRY <= address < ENTRY + len(body) - 8:
            state['pcs'].append(address)
            return
        assert address in CALLS, hex(address)
        args = [uc.reg_read(r) for r in REGS[:ARGUMENTS.get(address, 0)]]
        state['calls'].append((address, args))
        result = rng.getrandbits(32)
        if address == 0x020407FC:
            result = queries[state['queries']]
            state['queries'] += 1
        elif address == 0x0205BFD4: result = threshold
        elif address == 0x021E4E9C: result = final
        for reg in [UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]:
            uc.reg_write(reg, rng.getrandbits(32))
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_CPSR, (rng.getrandbits(4) << 28) | 0x10)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    def write(uc, access, address, size, value, data):
        assert STACK <= address < STACK + 4096 or address == GLOBAL + 10
        state['writes'].append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP + 4, count=bound)
    assert state['returned'], 'Bounded prefix is not a return'
    actual_page = bytes(machine.mem_read(GLOBAL & ~4095, 4096))
    values = [machine.reg_read(r) for r in REGS]
    passed = actual_page == expected and state['calls'] == expected_calls and values[0] == 1
    passed &= values[4:12] == registers[4:12] and machine.reg_read(UC_ARM_REG_SP) == STACK + 0x800
    return dict(actualReturn=True, modelPassed=bool(passed), registers=values,
        flags=machine.reg_read(UC_ARM_REG_CPSR), calls=state['calls'], writes=state['writes'],
        dataSha256=hashlib.sha256(actual_page).hexdigest(),
        stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK, 4096))).hexdigest(),
        observedInstructionAddresses=sorted(set(state['pcs'])), suppliedBoundaryCalls=len(state['calls']),
        actualNativeHelperReturns=0)
