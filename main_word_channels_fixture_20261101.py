import hashlib
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

DATA, IO, STACK, STOP = 0x02380000, 0x04000000, 0x027F0000, 0x027FF000
COMMANDS = {0x02009128: 4, 0x020092A4: 26, 0x020092C4: 27, 0x0200930C: 21,
            0x02009378: 30, 0x02009398: 31, 0x020093B8: 32}
HARDWARE = {0x0200434C: (23, 0x02005994), 0x02004368: (25, 0x02005994),
            0x02004384: (26, 0x02008D0C)}
OFFSETS = {0x020346FC: 20, 0x02034748: 12}
ENTRIES = {**{entry: 32 for entry in COMMANDS}, **{entry: 28 for entry in HARDWARE},
           **{entry: 16 for entry in OFFSETS}}
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def execute(image, entry, body, index, bound=128, require_model=True):
    rng = random.Random(entry * 100000 + index)
    data, io = bytearray(rng.randbytes(4096)), bytearray(rng.randbytes(4096))
    expected_data, expected_io = bytearray(data), bytearray(io)
    registers = [rng.getrandbits(32) for unused in REGS]
    edge = [0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, rng.getrandbits(32)]
    registers[0], registers[1] = edge[index % 6], edge[index // 6 % 6]
    returned = [0, 1, 0x80000000, 0xFFFFFFFF, rng.getrandbits(32)][index % 5]
    payload = (entry ^ index ^ 0xA55A9669) & 0xFFFFFFFF
    expected_calls, expected_writes = [], []
    helper = None
    if entry in COMMANDS:
        helper = 0x02009470
        expected_calls = [[helper, [COMMANDS[entry], registers[0], registers[1], 0], 0]]
    elif entry in HARDWARE:
        command, helper = HARDWARE[entry]
        expected_calls = [[helper, [registers[0], IO + 0x400], None]]
        struct.pack_into('<I', expected_io, 0x400, command)
        expected_writes.append([IO + 0x400, 4, command])
    else:
        registers[0] = DATA + 0x100
        offset = 0x100 + OFFSETS[entry]
        old = edge[index % 6]
        struct.pack_into('<I', data, offset, old)
        expected_data[:] = data
        value = (old + registers[0]) & 0xFFFFFFFF
        struct.pack_into('<I', expected_data, offset, value)
        expected_writes.append([DATA + offset, 4, value])
        returned = registers[0]
    if helper is not None:
        struct.pack_into('<I', expected_data, 0x300, payload)
        expected_writes.append([DATA + 0x300, 4, payload])
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_map(IO, 4096)
    machine.mem_write(0x02000000, image)
    machine.mem_write(entry, body)
    machine.mem_write(DATA, bytes(data))
    machine.mem_write(IO, bytes(io))
    machine.mem_write(STACK - 4096, rng.randbytes(8192))
    machine.reg_write(UC_ARM_REG_CPSR, ((index % 16) << 28) | 0x10)
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, writes, observed = [], [], set()

    def code(uc, address, size, unused):
        if helper is not None and address == helper:
            words = [uc.reg_read(register) for register in REGS[:4]]
            fifth = struct.unpack('<I', bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 4)))[0]
            calls.append([address, words if entry in COMMANDS else words[:2], fifth if entry in COMMANDS else None])
            uc.mem_write(DATA + 0x300, struct.pack('<I', payload))
            writes.append([DATA + 0x300, 4, payload])
            for register in REGS[:4]:
                uc.reg_write(register, 0xCCCC0000 + register)
            uc.reg_write(UC_ARM_REG_R0, returned)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
            return
        assert entry <= address < entry + len(body), hex(address)
        observed.update(range(address, address + size))

    def write(uc, access, address, size, value, unused):
        if STACK - 4096 <= address and address + size <= STACK + 4096:
            return
        assert any(start <= address and address + size <= start + 4096 for start in [DATA, IO])
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(entry, STOP, timeout=1000000, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_SP) == STACK
    assert [machine.reg_read(register) for register in REGS[4:12]] == registers[4:12]
    assert machine.reg_read(UC_ARM_REG_CPSR) & 0x3F == 0x10
    actual_data, actual_io = bytes(machine.mem_read(DATA, 4096)), bytes(machine.mem_read(IO, 4096))
    result = machine.reg_read(UC_ARM_REG_R0)
    passed = (actual_data == expected_data and actual_io == expected_io and result == returned
              and calls == expected_calls and writes == expected_writes)
    if require_model:
        assert passed, (hex(entry), index, calls, expected_calls, writes, expected_writes, result, returned)
    record = dict(index=index, modelPassed=passed, result=result, calls=calls, writes=writes,
                  pagesSha256=hashlib.sha256(actual_data + actual_io).hexdigest(),
                  actualTopReturns=int(entry not in HARDWARE), actualInvocationCompletions=1,
                  suppliedTailReturnCompletions=int(entry in HARDWARE),
                  suppliedCalls=len(calls), actualNativeDependencyReturns=0, observed=sorted(observed),
                  registers=[machine.reg_read(register) for register in REGS], cpsr=machine.reg_read(UC_ARM_REG_CPSR))
    del machine
    return record
