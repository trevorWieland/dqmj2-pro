import hashlib
import random
import struct
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR
from match_runtime import REGISTERS

ENTRY, SIZE, HELPER = 0x0203C5B8, 164, 0x02008C58
FALLBACK, FLAG, RECORD, BUFFER = 0x020F5C00, 0x020F5BF0, 0x02370000, 0x02380000
STACK, SP, STOP = 0x03030000, 0x03030800, 0x0F000000


def recipes():
    rows = []
    counts = [1, 2, 3, 7, 8, 9, 32, 33, 64]
    for default in [False, True]:
        for mode in range(256):
            rows.append(dict(default=default, mode=mode, count=counts[mode % len(counts)]))
    for count in [0, -1, -2147483648, 1, 2, 3, 7, 8, 9, 16, 17, 31, 32, 33, 64]:
        for mode in [0, 1, 255]:
            for default in [False, True]:
                rows.append(dict(default=default, mode=mode, count=count))
    for index, row in enumerate(rows):
        row['index'] = index
    return rows


def execute(main, code, item):
    rng = random.Random(0xC5B80000 + item['index'])
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, main)
    uc.mem_write(ENTRY, code)
    record = struct.pack('<IiB', BUFFER, item['count'], item['mode']) + rng.randbytes(3)
    other = rng.randbytes(12)
    fallback, explicit = (record, other) if item['default'] else (other, record)
    uc.mem_write(FALLBACK, fallback)
    uc.mem_write(RECORD, explicit)
    before = rng.randbytes(512)
    uc.mem_write(BUFFER, before)
    flags = rng.randbytes(16)
    uc.mem_write(FLAG, flags)
    uc.mem_map(STACK, 4096)
    stack = rng.randbytes(4096)
    uc.mem_write(STACK, stack)
    uc.mem_map(STOP, 4096)
    uc.reg_write(UC_ARM_REG_CPSR, ((item['index'] & 15) << 28) | 0x1F)
    for reg in REGISTERS:
        uc.reg_write(reg, rng.getrandbits(32))
    uc.reg_write(REGISTERS[0], 0 if item['default'] else RECORD)
    uc.reg_write(UC_ARM_REG_SP, SP)
    uc.reg_write(UC_ARM_REG_LR, STOP | (item['index'] & 1))
    saved = [uc.reg_read(reg) for reg in REGISTERS[4:12]]
    state = dict(actualReturns=0, actualHelperReturns=0, helperFrame=None)
    pcs, reads, writes = [], [], []

    def step(machine, pc, width, unused):
        frame = state['helperFrame']
        if frame and frame == [pc, machine.reg_read(UC_ARM_REG_SP)]:
            state['actualHelperReturns'] += 1
            state['helperFrame'] = None
        if pc == STOP:
            state['actualReturns'] += 1
            machine.emu_stop()
            return
        if pc == HELPER:
            assert state['helperFrame'] is None
            target = machine.reg_read(UC_ARM_REG_LR)
            assert target in [ENTRY + 56, ENTRY + 104]
            state['helperFrame'] = [target, machine.reg_read(UC_ARM_REG_SP)]
        assert width == 4 and (ENTRY <= pc < ENTRY + SIZE - 8 or HELPER <= pc < HELPER + 76)
        pcs.append(pc)

    def read(machine, access, address, size, value, unused):
        assert any(start <= address and address + size <= end for start, end in [
            (ENTRY, ENTRY + SIZE), (HELPER, HELPER + 76), (FALLBACK, FALLBACK + 12),
            (RECORD, RECORD + 12), (SP - 32, SP)])
        reads.append([address, size])

    def write(machine, access, address, size, value, unused):
        assert any(start <= address and address + size <= end for start, end in [
            (SP - 32, SP), (BUFFER, BUFFER + 512), (FLAG, FLAG + 1)])
        writes.append([address, size, value])

    uc.hook_add(UC_HOOK_CODE, step)
    uc.hook_add(UC_HOOK_MEM_READ, read)
    uc.hook_add(UC_HOOK_MEM_WRITE, write)
    uc.emu_start(ENTRY, STOP + 4, count=500)
    assert state['actualReturns'] == 1 and state['helperFrame'] is None
    assert state['actualHelperReturns'] == int(item['count'] > 0)
    assert uc.reg_read(UC_ARM_REG_SP) == SP
    assert [uc.reg_read(reg) for reg in REGISTERS[4:12]] == saved
    final_stack = bytes(uc.mem_read(STACK, 4096))
    assert final_stack[:0x7E0] == stack[:0x7E0] and final_stack[0x800:] == stack[0x800:]
    assert bytes(uc.mem_read(FALLBACK, 12)) == fallback and bytes(uc.mem_read(RECORD, 12)) == explicit
    expected_buffer = bytearray(before)
    positive = item['count'] > 0
    if positive:
        for word in range(item['count']):
            value = 1 if item['mode'] == 0 else 2
            if word == (item['count'] - 1 if item['mode'] == 0 else 0):
                value = 0
            struct.pack_into('<I', expected_buffer, 4 * word, value)
    actual_buffer = bytes(uc.mem_read(BUFFER, 512))
    actual_flag = bytes(uc.mem_read(FLAG, 16))
    model = actual_buffer == expected_buffer and actual_flag == bytes([not positive]) + flags[1:]
    model = model and uc.reg_read(REGISTERS[0]) == int(positive)
    return dict(state=state, result=uc.reg_read(REGISTERS[0]), modelPassed=model,
                bufferSha256=hashlib.sha256(actual_buffer).hexdigest(), flag=actual_flag.hex(),
                pcs=pcs, reads=reads, writes=writes,
                registers=[uc.reg_read(reg) for reg in REGISTERS] + [uc.reg_read(UC_ARM_REG_CPSR)],
                stackSha256=hashlib.sha256(final_stack).hexdigest())
