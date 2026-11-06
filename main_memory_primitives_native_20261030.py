import hashlib
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
from main_format_wrappers_native_20261030 import REGS

DATA, STACK, STOP = 0x02500000, 0x027C0000, 0x02FF0000
ENTRIES = {'search': (0x0201B21C, 44), 'compare': (0x0201B248, 64), 'fill': (0x0201B288, 176)}


def cases():
    for value in range(256):
        for count in [0, 1, 31, 64]:
            yield 'search', value, count, value % 4, value % 3
        for relation in range(3):
            yield 'compare', value, 64, value % 4, relation
    for count in [0, 1, 2, 3, 4, 7, 8, 15, 16, 31, 32, 33, 34, 35, 36, 63, 64, 65, 127, 128, 129, 255, 256, 257]:
        for alignment in range(4):
            for value in [0, 1, 127, 128, 255, 0x12345678, 0xFFFFFFFF]:
                yield 'fill', value, count, alignment, 0


def execute(main, case, tag):
    mode, value, count, alignment, relation = case
    entry, length = ENTRIES[mode]
    memory = bytearray((i * 73 + tag * 11) & 255 for i in range(0x1000))
    offset, other = 0x100 + alignment, 0x600 + alignment
    stores = []
    if mode == 'search':
        memory[offset:offset + count] = bytes([(value + 1) & 255]) * count
        if count and relation != 2:
            memory[offset + (0 if relation == 0 else count - 1)] = value
        position = bytes(memory[offset:offset + count]).find(bytes([value]))
        expected_return = DATA + offset + position if position >= 0 else 0
        args = [DATA + offset, value | ((tag & 0xFFFFFF) << 8), count]
    elif mode == 'compare':
        memory[offset:offset + count] = bytes([value]) * count
        memory[other:other + count] = memory[offset:offset + count]
        if relation:
            position = 0 if relation == 1 else count - 1
            memory[other + position] = (value + relation) & 255
        a, b = bytes(memory[offset:offset + count]), bytes(memory[other:other + count])
        expected_return = (int(a > b) - int(a < b)) & 0xFFFFFFFF
        args = [DATA + offset, DATA + other, count]
    else:
        args = [DATA + offset, value, count]
        expected_return = None
        cursor, remaining, byte = offset, count, value & 255
        if remaining >= 32:
            padding = (-cursor) & 3
            for unused in range(padding):
                stores.append([DATA + cursor, 1, byte])
                cursor += 1
            remaining -= padding
            for unused in range(remaining // 4):
                stores.append([DATA + cursor, 4, byte * 0x01010101])
                cursor += 4
            remaining %= 4
        for unused in range(remaining):
            stores.append([DATA + cursor, 1, byte])
            cursor += 1
    expected = bytearray(memory)
    for address, size, word in stores:
        expected[address - DATA:address - DATA + size] = word.to_bytes(size, 'little')
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (DATA, 0x1000), (STACK, 0x1000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(DATA, bytes(memory))
    machine.mem_write(STACK, bytes([0x5A]) * 0x1000)
    machine.reg_write(UC_ARM_REG_CPSR, ((tag & 15) << 28) | (0xC0 if tag & 16 else 0) | 0x1F)
    for index, reg in enumerate(REGS):
        machine.reg_write(reg, (0x13579BDF * (index + 1) + tag) & 0xFFFFFFFF)
    for reg, word in zip(REGS[:3], args):
        machine.reg_write(reg, word)
    sp = STACK + 0x800
    machine.reg_write(UC_ARM_REG_SP, sp)
    machine.reg_write(UC_ARM_REG_LR, STOP | (tag & 1))
    preserved = [machine.reg_read(reg) for reg in REGS[4:12]]
    actual_stores, events, pcs = [], [], set()
    steps = [0]

    def code(uc, address, size, user):
        steps[0] += 1
        if address == STOP:
            events.append('actual-return')
            uc.emu_stop()
        else:
            assert entry <= address < entry + length
            pcs.add(address)

    def store(uc, access, address, size, word, user):
        assert DATA <= address and address + size <= DATA + 0x1000
        actual_stores.append([address, size, word & ((1 << (size * 8)) - 1)])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, store)
    machine.emu_start(entry, STOP + 4, count=100000, timeout=1000000)
    assert events == ['actual-return']
    assert machine.reg_read(UC_ARM_REG_PC) == STOP and machine.reg_read(UC_ARM_REG_SP) == sp
    assert [machine.reg_read(reg) for reg in REGS[4:12]] == preserved
    if expected_return is not None:
        assert machine.reg_read(REGS[0]) == expected_return
    assert actual_stores == stores
    assert bytes(machine.mem_read(DATA, 0x1000)) == expected
    assert bytes(machine.mem_read(STACK, 0x1000)) == bytes([0x5A]) * 0x1000
    assert bytes(machine.mem_read(0x02000000, len(main))) == main
    return {'actualReturn': True, 'registers': [machine.reg_read(reg) for reg in REGS],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'lr': machine.reg_read(UC_ARM_REG_LR),
            'stores': stores, 'dataSha256': hashlib.sha256(expected).hexdigest(),
            'instructions': steps[0], 'pcs': sorted(pcs)}
