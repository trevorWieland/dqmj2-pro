import hashlib
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from main_irq_guarded_getters_fixture_v2_20261101 import REGS

ENTRY, SIZE = 0x0200A81C, 192
IRQ = {0x02007FF4: 20, 0x02008008: 24}
SLEEP, CALLBACK = 0x020068D4, 0x026A0000
DATA, STACK, STOP = 0x02380000, 0x027F0000, 0x027FF000


def execute(image, body, index, bound=2048, require_model=True, permanent=False):
    rng = random.Random(ENTRY * 100000 + index)
    page = bytearray(rng.randbytes(4096))
    cursor = DATA + 0x100
    state = DATA + (0x200 if index % 2 == 0 else 0x900)
    result_pointer = DATA + 0x600
    alternate = DATA + 0x700
    values = [0, 1, 0xFFFFFFFF, 0x7FFFFFFF, 0x80000000, rng.getrandbits(32)]
    offset, length, value = [values[(index + slot * 2) % 6] for slot in range(3)]
    status = [0, 1, 2, 5, 6, 0xFFFFFFFF, 0x80000000, rng.getrandbits(32)][index % 8]
    if permanent:
        status = 6
    waits = index // 8 % 4 if status == 6 else 0
    if permanent:
        waits = 100000
    flags, callback_flags = rng.getrandbits(32), rng.getrandbits(32)
    if status == 6 and waits == 0:
        callback_flags &= ~0x200
    else:
        callback_flags |= 0x200
    replacement = values[index // 3 % 6]
    final_status = rng.getrandbits(32)

    def put(memory, address, word):
        struct.pack_into('<I', memory, address - DATA, word & 0xFFFFFFFF)

    def get(memory, address):
        return struct.unpack_from('<I', memory, address - DATA)[0]

    for address, word in [(cursor, state), (cursor + 4, offset), (state + 0x1C, flags),
        (state + 0x24, result_pointer), (state + 0x50, CALLBACK),
        (result_pointer + 0x14, rng.getrandbits(32)), (alternate + 0x14, final_status)]:
        put(page, address, word)
    wanted = bytearray(page)
    expected = []

    def model_store(kind, address, word):
        put(wanted, address, word)
        expected.append([kind, address, 4, word & 0xFFFFFFFF])

    model_store('native-store', state + 0x1C, flags | 0x200)
    expected.append(['callback', [state, value, offset, length]])
    model_store('service-store', state + 0x1C, callback_flags)
    model_store('service-store', state + 0x24, alternate)
    if index % 3 == 0:
        model_store('service-store', cursor + 4, replacement)
    cpsr = (index % 16 << 28) | 0x1F | (index // 2 % 2 << 7) | (index // 7 % 2 << 6)
    if status in (0, 1):
        model_store('native-store', state + 0x1C, callback_flags & ~0x200)
    if status == 6:
        expected.append(['disable'])
        for number in range(1, min(waits, 4) + 1):
            expected.append(['sleep', [state + 0xC]])
            model_store('service-store', cursor + 4, (replacement + number * 0x10001) & 0xFFFFFFFF)
            if number == waits:
                model_store('service-store', state + 0x1C, callback_flags & ~0x200)
                model_store('service-store', alternate + 0x14, final_status ^ (number << 24))
        expected.append(['restore', [cpsr & 0x80]])
    result = get(wanted, alternate + 0x14) if status == 6 else status
    model_store('native-store', cursor + 4, (get(wanted, cursor + 4) + length) & 0xFFFFFFFF)
    initial = [rng.getrandbits(32) for unused in REGS]
    initial[:3] = [cursor, value, length]
    guards = rng.randbytes(8192)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_write(0x02000000, image)
    machine.mem_write(ENTRY, body)
    machine.mem_write(DATA, bytes(page))
    machine.mem_write(STACK - 4096, guards)
    machine.reg_write(UC_ARM_REG_CPSR, cpsr)
    for register, word in zip(REGS, initial):
        machine.reg_write(register, word)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    own, lower, events, stack_writes, pending, returns = set(), set(), [], [], [], []
    sleep_count = 0

    def service_store(uc, address, word):
        uc.mem_write(address, struct.pack('<I', word & 0xFFFFFFFF))
        events.append(['service-store', address, 4, word & 0xFFFFFFFF])

    def service_return(uc, result_word, ordinal):
        resume = uc.reg_read(UC_ARM_REG_LR)
        for slot in [0, 1, 2, 3, 12]:
            uc.reg_write(REGS[slot], (0xF13579BD * (slot + 1) + index * 17 + ordinal) & 0xFFFFFFFF)
        uc.reg_write(UC_ARM_REG_R0, result_word)
        control = uc.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF
        uc.reg_write(UC_ARM_REG_CPSR, control | ((index + ordinal) % 16 << 28))
        uc.reg_write(UC_ARM_REG_PC, resume)

    def code(uc, address, size, unused):
        nonlocal sleep_count
        if pending and address == pending[-1][1]:
            returns.append(pending.pop()[0])
        if address == CALLBACK:
            events.append(['callback', [uc.reg_read(register) for register in REGS[:4]]])
            service_store(uc, state + 0x1C, callback_flags)
            service_store(uc, state + 0x24, alternate)
            if index % 3 == 0:
                service_store(uc, cursor + 4, replacement)
            service_return(uc, status, 0)
            return
        if address == SLEEP:
            sleep_count += 1
            events.append(['sleep', [uc.reg_read(UC_ARM_REG_R0)]])
            service_store(uc, cursor + 4, replacement + sleep_count * 0x10001)
            if sleep_count == waits:
                service_store(uc, state + 0x1C, callback_flags & ~0x200)
                service_store(uc, alternate + 0x14, final_status ^ (sleep_count << 24))
            service_return(uc, 0xFA1ED, sleep_count)
            return
        if address in IRQ:
            pending.append([address, uc.reg_read(UC_ARM_REG_LR)])
            events.append(['disable'] if address == 0x02007FF4 else ['restore', [uc.reg_read(UC_ARM_REG_R0)]])
        if ENTRY <= address < ENTRY + len(body):
            own.update(range(address, address + size))
        else:
            assert any(start <= address < start + width for start, width in IRQ.items()), hex(address)
            lower.update(range(address, address + size))

    def write(uc, access, address, size, word, unused):
        if STACK - 4096 <= address and address + size <= STACK + 4096:
            assert STACK - 128 <= address and address + size <= STACK
            stack_writes.append([address, size, word])
        else:
            assert DATA <= address and address + size <= DATA + 4096
            events.append(['native-store', address, size, word])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP, timeout=1000000, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP and not pending
    assert machine.reg_read(UC_ARM_REG_SP) == STACK
    assert [machine.reg_read(register) for register in REGS[4:12]] == initial[4:12]
    assert bytes(machine.mem_read(STACK - 4096, 256)) == guards[:256]
    assert bytes(machine.mem_read(STACK + 4096 - 256, 256)) == guards[-256:]
    actual = bytes(machine.mem_read(DATA, 4096))
    actual_result = machine.reg_read(UC_ARM_REG_R0)
    passed = (actual == wanted and events == expected and actual_result == result
        and len(returns) == (2 if status == 6 else 0) and sleep_count == waits
        and machine.reg_read(UC_ARM_REG_CPSR) & 0xFF == cpsr & 0xFF)
    if require_model:
        assert passed, (index, actual_result, result, events, expected)
    record = dict(index=index, modelPassed=passed, result=actual_result, events=events,
        stackWrites=stack_writes, pageSha256=hashlib.sha256(actual).hexdigest(),
        completeStackSha256=hashlib.sha256(bytes(machine.mem_read(STACK - 4096, 8192))).hexdigest(),
        registers=[machine.reg_read(register) for register in REGS], cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        actualTopReturns=1, actualNativeDependencyReturns=len(returns), suppliedCalls=1 + sleep_count,
        observed=sorted(own), helperObserved=sorted(lower))
    del machine
    return record
