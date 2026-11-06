import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, SIZE = 0x020095E8, 272
DATA, STACK, STOP = 0x02400000, 0x03030000, 0x0F000000
GLOBAL, TABLE, PAGE = 0x020E3780, 0x020E37A4, 0x020E3000
CURRENT = 0x02009DBC
HELPERS = {0x02007FF4:20, 0x02008008:24, 0x02008064:12}
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
    UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def execute(image, body, index, bound=4096):
    rng = random.Random(0x95E80000 + index)
    data, page = bytearray(rng.randbytes(4096)), bytearray(rng.randbytes(4096))
    def get(address, target_data=data, target_page=page):
        target, offset = (target_data, address - DATA) if DATA <= address < DATA + 4096 else (target_page, address - PAGE)
        return struct.unpack_from('<I', target, offset)[0]
    def put(address, value, target_data=data, target_page=page):
        target, offset = (target_data, address - DATA) if DATA <= address < DATA + 4096 else (target_page, address - PAGE)
        struct.pack_into('<I', target, offset, value & 0xFFFFFFFF)
    slot = index % 9
    head = DATA + 0xA00 if index % 3 else 0
    tail = DATA + 0xA00 if head else 0
    put(DATA + 0xA00, 0)
    gate = 0x12340000 | index
    for offset, value in [(0, head), (4, gate), (0x10, tail), (0x14, slot), (0x1C, index % 100 + 1)]:
        put(GLOBAL + offset, value)
    for number in range(9):
        node = DATA + 0x100 + number * 0x40
        put(TABLE + number * 4, node)
        length = (index + number) % 4
        for step in range(length + 1):
            put(node + step * 8, node + (step + 1) * 8 if step < length else 0)
    argument = [0, 1, 2, 0xFFFFFFFF][index % 4]
    same = index % 5 != 0
    iterations = (index // 5) % 3 + 1
    def current_result(call):
        return gate if same and (not argument & 1 or call <= iterations) else gate ^ 0x40000000
    expected_data, expected_page = bytearray(data), bytearray(page)
    expected_writes = []
    def model_put(address, value):
        put(address, value, expected_data, expected_page)
        expected_writes.append([address, 4, value & 0xFFFFFFFF])
    top_current_calls = iterations + 1 if argument & 1 and same else 1
    expected_native = [0x02007FF4]
    for ordinal in range(top_current_calls - 1):
        expected_native.extend([0x02008008, 0x02008064, 0x02007FF4])
    result = 0
    if not argument & 1 and same:
        expected_native.append(0x02008008)
    else:
        result = get(TABLE + slot * 4)
        model_put(GLOBAL + 0x14, slot + 1)
        if slot == 8:
            model_put(GLOBAL + 0x14, 0)
        last = result
        while get(last) != 0:
            last = get(last)
        model_put(tail if tail else GLOBAL, result)
        model_put(GLOBAL + 0x10, last)
        model_put(GLOBAL + 0x1C, get(GLOBAL + 0x1C) - 1)
        model_put(GLOBAL + 4, gate + 1)
        expected_native.append(0x02008008)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x100000)
    machine.mem_write(0x02000000, image)
    machine.mem_write(ENTRY, body)
    machine.mem_write(PAGE, bytes(page))
    initial_main = bytes(machine.mem_read(0x02000000, 0x100000))
    machine.mem_map(DATA, 4096)
    machine.mem_write(DATA, bytes(data))
    machine.mem_map(STACK, 4096)
    stack = rng.randbytes(4096)
    machine.mem_write(STACK, stack)
    machine.mem_map(STOP, 4096)
    initial_irq = (index % 2) * 0x80
    machine.reg_write(UC_ARM_REG_CPSR, 0x1F | initial_irq | ((index % 16) << 28))
    initial = [rng.getrandbits(32) for register in REGISTERS]
    for register, value in zip(REGISTERS, initial):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_R0, argument)
    machine.reg_write(UC_ARM_REG_SP, STACK + 2048)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, native, returned, pending, writes, own, helper_own = [], [], [], [], [], set(), set()
    def code(uc, address, size, unused):
        if pending and address == pending[-1][0]:
            returned.append(pending.pop()[1])
        if ENTRY <= address < ENTRY + len(body):
            own.add(address)
            return
        if address == CURRENT:
            value = current_result(len(calls) + 1)
            calls.append(dict(address=address, words=[], result=value))
            for register in [UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]:
                uc.reg_write(register, rng.getrandbits(32))
            cpsr = uc.reg_read(UC_ARM_REG_CPSR)
            uc.reg_write(UC_ARM_REG_CPSR, (cpsr & 0x0FFFFFFF) | (((index + len(calls)) % 16) << 28))
            uc.reg_write(UC_ARM_REG_R0, value)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
            return
        assert any(base <= address < base + length for base, length in HELPERS.items()), hex(address)
        helper_own.add(address)
        if address in HELPERS and (not pending or pending[-1] != (uc.reg_read(UC_ARM_REG_LR), address)):
            native.append(dict(address=address, arg0=uc.reg_read(UC_ARM_REG_R0)))
            pending.append((uc.reg_read(UC_ARM_REG_LR), address))
    def write(uc, access, address, size, value, unused):
        if STACK <= address and address + size <= STACK + 4096:
            assert STACK + 1984 <= address and address + size <= STACK + 2048
        else:
            assert DATA <= address < DATA + 4096 or PAGE <= address < PAGE + 4096
            writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP, 'Instruction-bound prefix is not return'
    assert not pending and len(returned) == len(native)
    assert machine.reg_read(UC_ARM_REG_SP) == STACK + 2048
    assert machine.reg_read(UC_ARM_REG_CPSR) & 0x80 == initial_irq
    assert all(machine.reg_read(register) == value for register, value in zip(REGISTERS[4:12], initial[4:12]))
    after_stack = bytes(machine.mem_read(STACK, 4096))
    assert after_stack[:1984] == stack[:1984] and after_stack[2048:] == stack[2048:]
    after_main = bytes(machine.mem_read(0x02000000, 0x100000))
    lo, hi = PAGE - 0x02000000, PAGE - 0x02000000 + 4096
    assert after_main[:lo] == initial_main[:lo] and after_main[hi:] == initial_main[hi:]
    after_data = bytes(machine.mem_read(DATA, 4096))
    after_page = bytes(machine.mem_read(PAGE, 4096))
    passed = after_data == expected_data and after_page == expected_page and writes == expected_writes
    passed = passed and machine.reg_read(UC_ARM_REG_R0) == result and len(calls) == top_current_calls
    passed = passed and [item['address'] for item in native] == expected_native
    passed = passed and all(item['arg0'] == (100 if item['address'] == 0x02008064 else initial_irq) for item in native if item['address'] != 0x02007FF4)
    return dict(modelPassed=passed, actualReturn=True, index=index, argument=argument, slot=slot,
        result=machine.reg_read(UC_ARM_REG_R0), registers=[machine.reg_read(register) for register in REGISTERS],
        cpsr=machine.reg_read(UC_ARM_REG_CPSR), lr=machine.reg_read(UC_ARM_REG_LR), calls=calls, native=native,
        actualNativeReturns=len(returned), writes=writes, ownedObserved=sorted(own), helperObserved=sorted(helper_own),
        dataSha256=hashlib.sha256(after_data).hexdigest(), pageSha256=hashlib.sha256(after_page).hexdigest(),
        stackSha256=hashlib.sha256(after_stack).hexdigest())
