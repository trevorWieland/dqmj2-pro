import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY = 0x0203D158
OUTPUT = 0x020F6034
STATE = 0x020F6044
PAGE = 0x020F6000
STACK = 0x03030000
STOP = 0x0F000000
HELPERS = {0x0203D294: 72, 0x0203D1F0: 68, 0x02026350: 484}
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
    UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def encoded(value):
    return value >> 16 == (((value & 255) * ~(value >> 8 & 255) + 123) & 65535)


def model(seed, argument):
    writes, calls = [], []
    def draw(limit):
        nonlocal seed
        seed = (seed * 0x41C64E6D + 12345) & 0xFFFFFFFF
        writes.append([STATE, 4, seed])
        result = (seed >> 16) % limit
        calls.append(dict(limit=limit, result=result))
        return result
    if argument:
        first, second = draw(256), draw(256)
        value = first | second << 8 | (((first * ~second + 123) & 65535) << 16)
        writes.append([OUTPUT, 4, value])
        iterations = 1
    else:
        for iterations in range(1, 33):
            first, second = draw(65535) + 1, draw(65535) + 1
            value = (first * second) & 0xFFFFFFFF
            writes.append([OUTPUT, 4, value])
            if not encoded(value):
                break
        else:
            raise ValueError('Independent model exceeds supported finite iteration bound')
    return dict(result=value, seed=seed, writes=writes, calls=calls, iterations=iterations,
        predicateReturns=iterations if argument == 0 else 0)


def cases():
    repeated = []
    for seed in range(2000000):
        first_state = (seed * 0x41C64E6D + 12345) & 0xFFFFFFFF
        second_state = (first_state * 0x41C64E6D + 12345) & 0xFFFFFFFF
        value = (((first_state >> 16) % 65535 + 1) * ((second_state >> 16) % 65535 + 1)) & 0xFFFFFFFF
        if encoded(value) and model(seed, 0)['iterations'] > 1:
            repeated.append(dict(seed=seed, argument=0, forcedRepeatEvidence=True))
            if len(repeated) == 8:
                break
    assert len(repeated) == 8
    rng = random.Random(0x3D158152)
    result = list(repeated)
    for index in range(504):
        seed = [0, 1, 0xFFFFFFFF, 0x80000000, 0x7FFFFFFF, 0x12345678][index] if index < 6 else rng.getrandbits(32)
        result.append(dict(seed=seed, argument=[0, 1, 0x80000000, 0xFFFFFFFF][index % 4], forcedRepeatEvidence=False))
    return result


def execute(image, body, case, index, bound=50000):
    expected = model(case['seed'], case['argument'])
    rng = random.Random(0x3D158000 + index)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x100000)
    machine.mem_write(0x02000000, image)
    machine.mem_write(ENTRY, body)
    initial_page = bytearray(rng.randbytes(4096))
    struct.pack_into('<I', initial_page, STATE - PAGE, case['seed'])
    machine.mem_write(PAGE, bytes(initial_page))
    machine.mem_map(STACK, 4096)
    initial_stack = rng.randbytes(4096)
    machine.mem_write(STACK, initial_stack)
    machine.mem_map(STOP, 4096)
    machine.reg_write(UC_ARM_REG_CPSR, 0x10 | ((index % 16) << 28))
    initial_registers = [rng.getrandbits(32) for register in REGISTERS]
    for register, value in zip(REGISTERS, initial_registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_R0, case['argument'])
    machine.reg_write(UC_ARM_REG_SP, STACK + 2048)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    pending, returned, draws, predicates, writes = [], [], [], [], []
    own, helper_seen = set(), set()
    def code(uc, address, size, unused):
        if pending and address == pending[-1]['returnAddress']:
            record = pending.pop()
            returned.append(record['entry'])
            if record['entry'] == 0x0203D294:
                draws.append(dict(limit=record['argument'], result=uc.reg_read(UC_ARM_REG_R0)))
            elif record['entry'] == 0x0203D1F0:
                predicates.append(uc.reg_read(UC_ARM_REG_R0))
        if ENTRY <= address < ENTRY + len(body):
            own.add(address)
            return
        assert any(base <= address < base + length for base, length in HELPERS.items()), hex(address)
        if address in HELPERS:
            pending.append(dict(entry=address, returnAddress=uc.reg_read(UC_ARM_REG_LR), argument=uc.reg_read(UC_ARM_REG_R0)))
        helper_seen.add(address)
    def write(uc, access, address, size, value, unused):
        if STACK <= address and address + size <= STACK + 4096:
            assert address >= STACK + 1792 and address + size <= STACK + 2048
        else:
            assert PAGE <= address and address + size <= PAGE + 4096
            writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP, 'Bounded prefix does not count as return'
    assert not pending and machine.reg_read(UC_ARM_REG_SP) == STACK + 2048
    assert all(machine.reg_read(register) == value for register, value in zip(REGISTERS[4:12], initial_registers[4:12]))
    stack = bytes(machine.mem_read(STACK, 4096))
    assert stack[:1792] == initial_stack[:1792] and stack[2048:] == initial_stack[2048:]
    page_expected = bytearray(initial_page)
    for address, size, value in expected['writes']:
        page_expected[address - PAGE:address - PAGE + size] = value.to_bytes(size, 'little')
    page = bytes(machine.mem_read(PAGE, 4096))
    result = machine.reg_read(UC_ARM_REG_R0)
    passed = result == expected['result'] and page == page_expected and writes == expected['writes'] and draws == expected['calls']
    passed = passed and len(predicates) == expected['predicateReturns'] and returned.count(0x02026350) == len(expected['calls'])
    if not case['argument']:
        passed = passed and predicates == [1] * (expected['iterations'] - 1) + [0]
    return dict(case=case, result=result, modelPassed=passed, actualReturn=True,
        iterations=expected['iterations'], nativeDraws=draws, nativePredicates=predicates,
        helperReturns={hex(address): returned.count(address) for address in HELPERS},
        actualNativeHelperReturns=len(returned), ownObserved=sorted(own), helperObserved=sorted(helper_seen),
        registers=[machine.reg_read(register) for register in REGISTERS], cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        pageSha256=hashlib.sha256(page).hexdigest(), stackSha256=hashlib.sha256(stack).hexdigest(), writes=writes)
