import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, SIZE, DATA, STACK, STOP = 0x020316B4, 220, 0x02380000, 0x027F0000, 0x027FF000
CALLBACK, SERVICE = 0x020FF000, 0x0202E380
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def word(page, offset):
    return struct.unpack_from('<I', page, offset)[0]


def put(page, offset, value):
    struct.pack_into('<I', page, offset, value & 0xFFFFFFFF)


def scenario(index):
    rng = random.Random(ENTRY * 10000 + index)
    page = bytearray(rng.randbytes(4096))
    put(page, 0, DATA + 0x200)
    put(page, 8, [0, 0x40, 0x100, 0x140, 0xFFFFFFFF, 0x80000000, 0x12345678, 0x89ABCDEF][index % 8])
    put(page, 0x34, CALLBACK if index // 8 % 2 else 0)
    page[0x96] = [0, 1, 2, 3, 255][index // 16 % 5]
    put(page, 0xC0, 0)
    put(page, 0xC4, 0)
    for offset in [0x200, 0x300]:
        put(page, offset + 1, rng.randrange(256))
        put(page, offset + 5, rng.randrange(0x80000000))
    policy = dict(flags=index // 80 % 4, phase=index // 320 % 5,
        remove=bool(index // 1600 % 2), redirect=bool(index // 3200 % 2))
    return page, policy


def callback_effect(page, policy):
    flags = word(page, 8)
    if policy['flags'] == 1:
        flags |= 0x40
    elif policy['flags'] == 2:
        flags |= 0x100
    elif policy['flags'] == 3:
        flags &= ~0x140
    put(page, 8, flags)
    page[0x96] = [0, 1, 2, 3, 255][policy['phase']]
    if policy['remove']:
        put(page, 0x34, 0)
    if policy['redirect']:
        put(page, 0, DATA + 0x300)
    put(page, 0xC0, word(page, 0xC0) + 1)


def model(initial, policy):
    page = bytearray(initial)
    events = []
    phase = page[0x96] if word(page, 0x34) else 0
    first_phase = phase == 1
    if first_phase:
        put(page, 8, word(page, 8) & ~0x40)
        events.append(['callback', DATA])
        callback_effect(page, policy)
        phase = page[0x96] if word(page, 0x34) else 0
    suppressed = bool(word(page, 8) & 0x100 or first_phase and word(page, 8) & 0x40)
    if not suppressed:
        stream = word(page, 0)
        offset = stream - DATA
        events.append(['service', stream + word(page, offset + 1), word(page, offset + 5), page[offset + 8]])
        put(page, 0xC4, word(page, 0xC4) + 1)
    if phase == 3:
        put(page, 8, word(page, 8) & ~0x40)
        events.append(['callback', DATA])
        callback_effect(page, policy)
    result = word(page, 0) + 9
    put(page, 0, result)
    return page, events, result


def execute(image, body, index, instruction_bound=512, require_model=True):
    page, policy = scenario(index)
    expected, expected_events, expected_result = model(page, policy)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_write(0x02000000, image)
    machine.mem_write(ENTRY, body)
    machine.mem_write(DATA, bytes(page))
    initial = [0xA5170000 + n * 0x100 + index for n in range(13)]
    machine.reg_write(UC_ARM_REG_CPSR, (index % 16 << 28) | 0x10)
    for register, value in zip(REGS, initial):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_R0, DATA)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    events, observed, writes = [], set(), []

    def watch(uc, address, length, unused):
        if ENTRY <= address < ENTRY + SIZE:
            observed.update(range(address, address + length))
            return
        if address not in [CALLBACK, SERVICE]:
            raise ValueError(('Unexpected native stream instruction', hex(address)))
        state = bytearray(uc.mem_read(DATA, 4096))
        if address == CALLBACK:
            assert uc.reg_read(UC_ARM_REG_R0) == DATA
            events.append(['callback', DATA])
            callback_effect(state, policy)
        else:
            events.append(['service', *[uc.reg_read(register) for register in REGS[:3]]])
            put(state, 0xC4, word(state, 0xC4) + 1)
        uc.mem_write(DATA, bytes(state))
        for position in [0, 1, 2, 3, 12]:
            uc.reg_write(REGS[position], (0xD0020000 + position * 64 + len(events)) & 0xFFFFFFFF)
        uc.reg_write(UC_ARM_REG_CPSR, ((len(events) % 16) << 28) | 0x10)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    def memory_write(uc, access, address, size, value, unused):
        assert DATA <= address and address + size <= DATA + 4096 or STACK - 4096 <= address and address + size <= STACK
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, watch)
    machine.hook_add(UC_HOOK_MEM_WRITE, memory_write)
    machine.emu_start(ENTRY, STOP, timeout=1000000, count=instruction_bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_SP) == STACK
    assert machine.reg_read(UC_ARM_REG_CPSR) & 0x3F == 0x10
    assert [machine.reg_read(register) for register in REGS[4:12]] == initial[4:12]
    after = bytes(machine.mem_read(DATA, 4096))
    result = machine.reg_read(UC_ARM_REG_R0)
    model_passed = after == expected and events == expected_events and result == expected_result
    if require_model:
        assert model_passed, (index, events, expected_events, result, expected_result)
    record = dict(index=index, result=result, modelPassed=model_passed, events=events,
        stateSha256=hashlib.sha256(after).hexdigest(), writes=writes,
        actualTopReturns=1, suppliedCalls=len(events), observed=sorted(observed),
        registers=[machine.reg_read(register) for register in REGS], lr=machine.reg_read(UC_ARM_REG_LR), cpsr=machine.reg_read(UC_ARM_REG_CPSR))
    del machine
    return record
