import hashlib
import random
import struct
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
from main_format_wrappers_native_20261030 import REGS

DATA, STACK, STOP = 0x02500000, 0x027C0000, 0x02FF0000
ENTRIES = {0x0201B09C: 136}
HELPERS = {0x0201D69C, 0x0201B018}


def cases():
    for byte in range(256):
        for limit in [0, 1, 2, 4, 8]:
            yield 'bytewide', byte, limit, False
    for byte in [0, 65, 255]:
        yield 'bytewide', byte, 8, True



def execute(main, case, tag):
    mode, value, limit, null_output = case
    entry = 0x0201B09C
    memory = bytearray([0xA5]) * 0x4000
    output, input_pointer = DATA + 0x200 + (tag % 2) * 2, DATA + 0x800
    stores = []
    units = [value, 0x80, 0xFF, 0]
    memory[0x800:0x804] = bytes(units)
    args = [0 if null_output else output, input_pointer, limit]
    expected_return = 0
    if not null_output:
        for unit in units:
            if expected_return >= limit:
                break
            stores.append([output + expected_return * 2, 2, unit])
            if unit == 0:
                break
            expected_return += 1
    expected = bytearray(memory)
    for address, size, word in stores:
        expected[address - DATA:address - DATA + size] = word.to_bytes(size, 'little')
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (DATA, 0x4000), (STACK, 0x8000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(DATA, bytes(memory))
    machine.mem_write(STACK, bytes([0x5A]) * 0x8000)
    machine.reg_write(UC_ARM_REG_CPSR, ((tag & 15) << 28) | (0xC0 if tag & 16 else 0) | 0x1F)
    for index, reg in enumerate(REGS):
        machine.reg_write(reg, (0x13579BDF * (index + 1) + tag) & 0xFFFFFFFF)
    for reg, word in zip(REGS[:3], args):
        machine.reg_write(reg, word)
    sp = STACK + 0x6000
    machine.reg_write(UC_ARM_REG_SP, sp)
    machine.reg_write(UC_ARM_REG_LR, STOP | (tag & 1))
    preserved = [machine.reg_read(reg) for reg in REGS[4:12]]
    actual_stores, pending, returns, events = [], [], [], []
    steps = [0]

    def code(uc, address, size, user):
        steps[0] += 1
        if entry in [0x0201B018, 0x0201B080]:
            assert not entry + 24 <= address < entry + 28
        if pending and address == pending[-1][1]:
            target, pc, frame = pending.pop()
            assert uc.reg_read(UC_ARM_REG_SP) == frame
            returns.append(target)
        if address in HELPERS and address != entry:
            pending.append((address, uc.reg_read(UC_ARM_REG_LR), uc.reg_read(UC_ARM_REG_SP)))
        if address == STOP:
            events.append('actual-return')
            uc.emu_stop()
        else:
            assert 0x02000000 <= address < 0x02400000

    def store(uc, access, address, size, word, user):
        if DATA <= address < DATA + 0x4000:
            actual_stores.append([address, size, word & ((1 << (size * 8)) - 1)])
        else:
            assert STACK <= address and address + size <= STACK + 0x8000

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, store)
    machine.emu_start(entry, STOP + 4, count=100000, timeout=1000000)
    assert events == ['actual-return'] and not pending
    assert machine.reg_read(UC_ARM_REG_PC) == STOP and machine.reg_read(UC_ARM_REG_SP) == sp
    assert [machine.reg_read(reg) for reg in REGS[4:12]] == preserved
    assert machine.reg_read(REGS[0]) == expected_return, (case, machine.reg_read(REGS[0]), expected_return)
    assert actual_stores == stores, (case, actual_stores, stores)
    assert bytes(machine.mem_read(DATA, 0x4000)) == expected
    assert bytes(machine.mem_read(0x02000000, len(main))) == main
    return {'actualReturn': True, 'return': expected_return, 'stores': stores, 'helperReturns': returns,
            'registers': [machine.reg_read(reg) for reg in REGS], 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'lr': machine.reg_read(UC_ARM_REG_LR), 'dataSha256': hashlib.sha256(bytes(expected)).hexdigest(),
            'stackSha256': hashlib.sha256(bytes(machine.mem_read(STACK, 0x8000))).hexdigest(), 'instructions': steps[0]}
