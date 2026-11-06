import hashlib
import random
import struct
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR
from match_runtime import REGISTERS

ENTRY, SIZE = 0x0202E380, 180
DIRECT, FLUSH, SEND, CALLBACK = 0x0202E434, 0x0202E300, 0x02008C40, 0x0202E374
TRANSFER_A, TRANSFER_B = 0x020088F8, 0x02008AFC
CHANNEL, STATE, BUFFER, PORT = 0x020DCB44, 0x020EDF84, 0x02380000, 0x04000400
STACK, SP, STOP = 0x03030000, 0x03030800, 0x0F000000
CODE = [(ENTRY, 164), (DIRECT, 220), (FLUSH, 84), (SEND, 24)]


def recipes():
    rows = []
    for length in [4, 5, 7, 8, 15, 31, 32, 63, 64, 127, 128, 251, 252, 255, 256, 257, 260, 511, 512]:
        for channel in [0xFFFFFFFF, 0, 1, 3, 0x80000000]:
            for mode in [0, 1, 0x80000000, 0xFFFFFFFF]:
                rows.append(dict(index=len(rows), bytes=length, channel=channel, mode=mode))
    return rows


def execute(main, code, item):
    rng = random.Random(0x2E380000 + item['index'])
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, main)
    uc.mem_write(ENTRY, code)
    channel = struct.pack('<I', item['channel'])
    state_before = struct.pack('<IIII', 0, 0, item['mode'], rng.getrandbits(32))
    buffer = rng.randbytes(512)
    port_before = rng.randbytes(4)
    uc.mem_write(CHANNEL, channel)
    uc.mem_write(STATE, state_before)
    uc.mem_write(BUFFER, buffer)
    uc.mem_map(PORT & ~4095, 4096)
    uc.mem_write(PORT, port_before)
    uc.mem_map(STACK, 4096)
    stack = rng.randbytes(4096)
    uc.mem_write(STACK, stack)
    uc.mem_map(STOP, 4096)
    uc.reg_write(UC_ARM_REG_CPSR, ((item['index'] & 15) << 28) | 0x1F)
    for reg in REGISTERS:
        uc.reg_write(reg, rng.getrandbits(32))
    uc.reg_write(REGISTERS[0], BUFFER)
    uc.reg_write(REGISTERS[1], item['bytes'])
    uc.reg_write(UC_ARM_REG_SP, SP)
    uc.reg_write(UC_ARM_REG_LR, STOP | (item['index'] & 1))
    saved = [uc.reg_read(reg) for reg in REGISTERS[4:12]]
    cpu = item['bytes'] < 256 or item['channel'] == 0xFFFFFFFF
    provided_result = rng.getrandbits(32)
    counters = dict(actualReturns=0, actualHelperReturns=0, suppliedTransfers=0)
    frames, pcs, reads, writes, port_words, transfers = [], [], [], [], [], []

    def step(machine, pc, width, unused):
        while frames and frames[-1] == [pc, machine.reg_read(UC_ARM_REG_SP)]:
            frames.pop()
            counters['actualHelperReturns'] += 1
        if pc == STOP:
            counters['actualReturns'] += 1
            machine.emu_stop()
            return
        if pc in [TRANSFER_A, TRANSFER_B]:
            assert not cpu and not transfers and not frames
            args = [machine.reg_read(reg) for reg in REGISTERS[:4]]
            fifth = struct.unpack('<I', bytes(machine.mem_read(machine.reg_read(UC_ARM_REG_SP), 4)))[0]
            assert pc == (TRANSFER_B if item['mode'] else TRANSFER_A)
            assert args == [item['channel'], BUFFER, item['bytes'], CALLBACK] and fifth == STATE + 4
            transfers.append(dict(target=pc, arguments=args + [fifth], result=provided_result))
            for index in [1, 2, 3, 12]:
                machine.reg_write(REGISTERS[index], rng.getrandbits(32))
            machine.reg_write(REGISTERS[0], provided_result)
            machine.reg_write(UC_ARM_REG_CPSR, ((item['index'] * 3 & 15) << 28) | 0x1F)
            machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))
            counters['suppliedTransfers'] += 1
            return
        if pc in [DIRECT, FLUSH, SEND]:
            frames.append([machine.reg_read(UC_ARM_REG_LR), machine.reg_read(UC_ARM_REG_SP)])
        assert width == 4 and any(start <= pc < start + size for start, size in CODE)
        pcs.append(pc)

    def read(machine, access, address, size, value, unused):
        assert any(start <= address and address + size <= end for start, end in [
            (ENTRY, ENTRY + SIZE), (DIRECT, DIRECT + 228), (FLUSH, FLUSH + 92),
            (SEND, SEND + 24), (CHANNEL, CHANNEL + 4), (STATE, STATE + 16),
            (BUFFER, BUFFER + 512), (SP - 32, SP)])
        reads.append([address, size])

    def write(machine, access, address, size, value, unused):
        assert any(start <= address and address + size <= end for start, end in [
            (SP - 32, SP), (STATE + 4, STATE + 8), (PORT, PORT + 4)])
        if address == PORT:
            assert size == 4
            port_words.append(value & 0xFFFFFFFF)
        writes.append([address, size, value])

    uc.hook_add(UC_HOOK_CODE, step)
    uc.hook_add(UC_HOOK_MEM_READ, read)
    uc.hook_add(UC_HOOK_MEM_WRITE, write)
    uc.emu_start(ENTRY, STOP + 4, count=1500)
    assert counters['actualReturns'] == 1 and not frames
    assert uc.reg_read(UC_ARM_REG_PC) == STOP
    assert bool(uc.reg_read(UC_ARM_REG_CPSR) & 0x20) == bool(item['index'] & 1)
    assert counters['actualHelperReturns'] == (2 if cpu else 1)
    assert counters['suppliedTransfers'] == int(not cpu)
    assert uc.reg_read(UC_ARM_REG_SP) == SP
    assert [uc.reg_read(reg) for reg in REGISTERS[4:12]] == saved
    final_stack = bytes(uc.mem_read(STACK, 4096))
    assert final_stack[:0x7E0] == stack[:0x7E0] and final_stack[0x800:] == stack[0x800:]
    assert bytes(uc.mem_read(CHANNEL, 4)) == channel and bytes(uc.mem_read(BUFFER, 512)) == buffer
    expected_state = bytearray(state_before)
    if cpu:
        count = item['bytes'] // 4
        expected_words = list(struct.unpack('<' + 'I' * count, buffer[:count * 4]))
        expected_result = BUFFER + count * 4
        expected_port = struct.pack('<I', expected_words[-1])
    else:
        expected_words = []
        expected_result = provided_result
        expected_port = port_before
        struct.pack_into('<I', expected_state, 4, 1)
    final_state = bytes(uc.mem_read(STATE, 16))
    result = uc.reg_read(REGISTERS[0])
    model = result == expected_result and port_words == expected_words
    model = model and final_state == expected_state and bytes(uc.mem_read(PORT, 4)) == expected_port
    return dict(counters=counters, result=result, modelPassed=model, cpu=cpu,
                portWords=port_words, finalState=final_state.hex(), transfers=transfers,
                pcs=pcs, reads=reads, writes=writes,
                registers=[uc.reg_read(reg) for reg in REGISTERS] + [uc.reg_read(UC_ARM_REG_CPSR)],
                stackSha256=hashlib.sha256(final_stack).hexdigest())
