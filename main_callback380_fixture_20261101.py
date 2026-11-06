import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, SIZE = 0x0202FB98, 380
DATA, STACK, STOP = 0x02400000, 0x03030000, 0x0F000000
CALLBACK, CONSUMER = 0x02500000, 0x02500100
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
    UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def execute(image, body, index, bound=2048):
    rng = random.Random(0x2FB980000 + index)
    page = bytearray(rng.randbytes(4096))
    obj, command, manager = DATA + 0x100, DATA + 0x500, DATA + 0x700
    selector = index % 256
    flags = rng.getrandbits(32) & ~0x200
    if index % 7 == 0:
        flags |= 0x200
    def put(target, address, value, size=4):
        target[address - DATA:address - DATA + size] = value.to_bytes(size, 'little')
    def get(target, address, size=4):
        return int.from_bytes(target[address - DATA:address - DATA + size], 'little')
    for offset, value in [(0, command), (4, manager), (8, flags),
        (0x14, CALLBACK if index % 5 else 0), (0xB8, obj + 0x184)]:
        put(page, obj + offset, value)
    put(page, obj + 0x8E, (index // 5) % 5, 1)
    put(page, command + 1, selector, 1)
    put(page, command + 2, (index // 3) % 256, 1)
    put(page, manager + 0x18, 0 if index % 4 == 0 else rng.getrandbits(32) | 1)
    put(page, manager + 0x1C, CONSUMER)
    bit_address = manager + 0x4C + (selector >> 5) * 4
    bits = get(page, bit_address)
    bits = bits | (1 << (selector & 31)) if index % 3 else bits & ~(1 << (selector & 31))
    put(page, bit_address, bits)
    mutation = (index // 11) % 5
    consumer_result = 0 if index % 6 < 3 else (0x80000000 | index)
    consumer_value = [0, 1, 0x80000000, 0xFFFFFFFF][index % 4]
    def effects(target, writes, address, words, ordinal):
        def write(location, value, size=4):
            put(target, location, value, size)
            writes.append([location, size, value])
        if address == CALLBACK:
            old = get(target, obj + 8)
            value = old | 0x40 if mutation == 1 else old & ~0x40
            write(obj + 8, value)
            phase = ((index // 5) + ordinal) % 5 if mutation == 2 else get(target, obj + 0x8E, 1)
            write(obj + 0x8E, phase, 1)
            if mutation == 3:
                write(obj + 0x14, 0)
            return 0xA0000000 | ordinal
        assert address == CONSUMER
        if words[0] == obj + 0x184:
            write(words[0], consumer_value)
        return consumer_result
    expected, expected_calls, expected_writes = bytearray(page), [], []
    def model_write(address, value, size=4):
        put(expected, address, value, size)
        expected_writes.append([address, size, value])
    def model_call(address, words):
        expected_calls.append(dict(address=address, words=words))
        return effects(expected, expected_writes, address, words, len(expected_calls))
    if not flags & 0x200:
        model_write(obj + 0xAC, selector, 1)
        model_write(obj + 8, get(expected, obj + 8) | 4)
        model_write(obj + 0xB8, obj + 0x184)
        phase = get(expected, obj + 0x8E, 1) if get(expected, obj + 0x14) else 0
        def stage(number, phase):
            changed = 0
            if phase == number:
                model_write(obj + 8, get(expected, obj + 8) & ~0x40)
                model_call(CALLBACK, [obj])
                phase = get(expected, obj + 0x8E, 1) if get(expected, obj + 0x14) else 0
                changed = get(expected, obj + 8) & 0x40
            return phase, changed
        phase, changed = stage(1, phase)
        if not changed:
            handle = get(expected, manager + 0x18)
            if not handle or not bits & (1 << (selector & 31)) or not model_call(CONSUMER, [obj + 0x184, handle, selector]):
                model_write(obj + 0x184, get(expected, command + 2, 1) & 1)
        phase, changed = stage(2, phase)
        if not changed:
            old = get(expected, obj + 8)
            model_write(obj + 8, old | 1 if get(expected, obj + 0x184) else old & ~1)
        if phase == 3:
            model_write(obj + 8, get(expected, obj + 8) & ~0x40)
            model_call(CALLBACK, [obj])
    result = get(expected, obj) + 3
    model_write(obj, result)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x100000)
    machine.mem_write(0x02000000, image)
    machine.mem_write(ENTRY, body)
    initial_main = bytes(machine.mem_read(0x02000000, 0x100000))
    machine.mem_map(DATA, 4096)
    machine.mem_write(DATA, bytes(page))
    machine.mem_map(CALLBACK, 4096)
    machine.mem_map(STACK, 4096)
    stack = rng.randbytes(4096)
    machine.mem_write(STACK, stack)
    machine.mem_map(STOP, 4096)
    cpsr = 0x1F | ((index % 16) << 28)
    machine.reg_write(UC_ARM_REG_CPSR, cpsr)
    initial = [rng.getrandbits(32) for register in REGISTERS]
    for register, value in zip(REGISTERS, initial):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_R0, obj)
    machine.reg_write(UC_ARM_REG_SP, STACK + 2048)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, writes, own = [], [], set()
    def code(uc, address, size, unused):
        if ENTRY <= address < ENTRY + len(body):
            own.add(address)
            return
        assert address in [CALLBACK, CONSUMER], hex(address)
        words = [uc.reg_read(register) for register in REGISTERS[:1 if address == CALLBACK else 3]]
        calls.append(dict(address=address, words=words))
        working = bytearray(uc.mem_read(DATA, 4096))
        previous = len(writes)
        value = effects(working, writes, address, words, len(calls))
        for location, width, word in writes[previous:]:
            uc.mem_write(location, word.to_bytes(width, 'little'))
        for register in [UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(UC_ARM_REG_R0, value)
        uc.reg_write(UC_ARM_REG_CPSR, 0x1F | (((index + len(calls)) % 16) << 28))
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
    def write(uc, access, address, size, value, unused):
        if STACK <= address and address + size <= STACK + 4096:
            assert STACK + 1984 <= address and address + size <= STACK + 2048
        else:
            assert DATA <= address and address + size <= DATA + 4096
            writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP, 'Bounded prefix is not actual return'
    assert machine.reg_read(UC_ARM_REG_SP) == STACK + 2048
    assert all(machine.reg_read(register) == value for register, value in zip(REGISTERS[4:12], initial[4:12]))
    after_stack = bytes(machine.mem_read(STACK, 4096))
    assert after_stack[:1984] == stack[:1984] and after_stack[2048:] == stack[2048:]
    assert bytes(machine.mem_read(0x02000000, 0x100000)) == initial_main
    after = bytes(machine.mem_read(DATA, 4096))
    passed = after == expected and writes == expected_writes and calls == expected_calls and machine.reg_read(UC_ARM_REG_R0) == result
    return dict(modelPassed=passed, actualReturn=True, index=index, selector=selector,
        result=machine.reg_read(UC_ARM_REG_R0), registers=[machine.reg_read(register) for register in REGISTERS],
        cpsr=machine.reg_read(UC_ARM_REG_CPSR), lr=machine.reg_read(UC_ARM_REG_LR), calls=calls, writes=writes,
        pageSha256=hashlib.sha256(after).hexdigest(), stackSha256=hashlib.sha256(after_stack).hexdigest(), ownedObserved=sorted(own))
