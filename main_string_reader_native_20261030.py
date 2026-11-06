import hashlib
import struct
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2
from unicorn.arm_const import UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6
from unicorn.arm_const import UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10
from unicorn.arm_const import UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR

ENTRY, SIZE, DATA, STACK, STOP = 0x0201D618, 132, 0x02400000, 0x027C0000, 0x02FF0000
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
        UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
        UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def state(context, cursor, eof):
    memory = bytearray([0xA5]) * 0x2000
    if DATA <= context <= DATA + len(memory) - 8:
        struct.pack_into('<II', memory, context - DATA, cursor, eof)
    return memory


def model(initial, context, value, mode):
    data, reads, writes = bytearray(initial), [], []

    def read(address, size):
        offset = address - DATA
        assert 0 <= offset and offset + size <= len(data)
        result = int.from_bytes(data[offset:offset + size], 'little')
        reads.append([address, size, result])
        return result

    def write(address, size, value):
        offset = address - DATA
        assert 0 <= offset and offset + size <= len(data)
        value &= (1 << (size * 8)) - 1
        data[offset:offset + size] = value.to_bytes(size, 'little')
        writes.append([address, size, value])

    if mode == 0:
        cursor = read(context, 4)
        byte = read(cursor, 1)
        if byte == 0:
            write(context + 4, 4, 1)
            result = 0xFFFFFFFF
        else:
            write(context, 4, (cursor + 1) & 0xFFFFFFFF)
            result = byte
    elif mode == 1:
        eof = read(context + 4, 4)
        if eof:
            write(context + 4, 4, 0)
        else:
            write(context, 4, (read(context, 4) - 1) & 0xFFFFFFFF)
        result = value & 0xFFFFFFFF
    elif mode == 2:
        result = read(context + 4, 4)
    else:
        result = 0
    return bytes(data), result, reads, writes


def execute(body, initial, context, value, mode, tag):
    expected, result, expected_reads, expected_writes = model(initial, context, value, mode)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, length in [(ENTRY & ~0xFFF, 0x1000), (DATA, 0x2000), (STACK, 0x2000), (STOP, 0x1000)]:
        machine.mem_map(address, length)
    machine.mem_write(ENTRY, body)
    machine.mem_write(DATA, bytes(initial))
    machine.mem_write(STACK, bytes([0x5A]) * 0x2000)
    machine.reg_write(UC_ARM_REG_CPSR, ((tag & 15) << 28) | 0x1F)
    for index, reg in enumerate(REGS):
        machine.reg_write(reg, (0x13579BDF * (index + 1) + tag) & 0xFFFFFFFF)
    for reg, word in [(UC_ARM_REG_R0, context), (UC_ARM_REG_R1, value), (UC_ARM_REG_R2, mode),
                      (UC_ARM_REG_SP, STACK + 0x1000), (UC_ARM_REG_LR, STOP)]:
        machine.reg_write(reg, word & 0xFFFFFFFF)
    callee_saved = [machine.reg_read(reg) for reg in REGS[4:]]
    events, reads, writes = [], [], []

    def code(uc, address, size, user):
        if address == STOP:
            events.append('actual-return')
            uc.emu_stop()
        else:
            assert ENTRY <= address < ENTRY + SIZE

    def read(uc, access, address, size, value, user):
        assert DATA <= address and address + size <= DATA + 0x2000
        reads.append([address, size, int.from_bytes(uc.mem_read(address, size), 'little')])

    def write(uc, access, address, size, value, user):
        assert DATA <= address and address + size <= DATA + 0x2000
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_READ, read)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP + 4, count=1000, timeout=100000)
    assert events == ['actual-return'] and machine.reg_read(UC_ARM_REG_PC) == STOP
    assert reads == expected_reads and writes == expected_writes
    assert machine.reg_read(UC_ARM_REG_R0) == result
    assert bytes(machine.mem_read(DATA, 0x2000)) == expected
    assert bytes(machine.mem_read(STACK, 0x2000)) == bytes([0x5A]) * 0x2000
    assert machine.reg_read(UC_ARM_REG_SP) == STACK + 0x1000
    assert [machine.reg_read(reg) for reg in REGS[4:]] == callee_saved
    final = {'registers': [machine.reg_read(reg) for reg in REGS], 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
             'sp': machine.reg_read(UC_ARM_REG_SP), 'lr': machine.reg_read(UC_ARM_REG_LR),
             'memorySha256': hashlib.sha256(expected).hexdigest(), 'reads': reads, 'writes': writes}
    return final, expected


def oracle(original, rebuilt):
    assert len(original) == SIZE and len(rebuilt) == SIZE
    context = DATA + 0x100
    eof_values = [0, 1, 2, 0xFFFFFFFF, 0x80000000, 0x12345678]
    cases = []
    for byte in range(256):
        for alignment in range(4):
            for eof in [0, 0xFFFFFFFF]:
                cursor = DATA + 0x400 + alignment
                memory = state(context, cursor, eof)
                memory[cursor - DATA] = byte
                cases.append((memory, context, 0x87654321, 0))
    for eof in eof_values:
        for value in [0, 1, 255, 256, 0xFFFFFFFF, 0x80000000, 0x12345678]:
            for alignment in range(4):
                cases.append((state(context, DATA + 0x400 + alignment, eof), context, value, 1))
        for flags in range(16):
            cases.append((state(context, DATA + 0x400, eof), context, flags * 0x11111111, 2))
    for mode in [3, 255, 0xFFFFFFFF, 0x80000000]:
        for opaque in [0, 0xFFFFFFFF, context]:
            for flags in range(16):
                cases.append((state(opaque, DATA + 0x400, flags), opaque, 0xDEADBEEF, mode))
    for offset in range(8):
        for eof in eof_values:
            for mode in range(3):
                cases.append((state(context, context + offset, eof), context, 0x76543210, mode))
    digest = hashlib.sha256()
    for index, (memory, pointer, value, mode) in enumerate(cases):
        native, after = execute(original, memory, pointer, value, mode, index)
        source, source_after = execute(rebuilt, memory, pointer, value, mode, index)
        assert native == source and after == source_after
        digest.update(repr(native).encode())
    persistent_calls = 0
    for payload in [b'ab\0', b'\x80\xff\0', b'\0']:
        memory = state(context, DATA + 0x400, 0)
        memory[0x400:0x400 + len(payload)] = payload
        current_native, current_source = bytes(memory), bytes(memory)
        for mode in [0, 1, 0, 2, 0, 0, 1, 2]:
            native, current_native = execute(original, current_native, context, 0xAABBCCDD, mode, persistent_calls)
            source, current_source = execute(rebuilt, current_source, context, 0xAABBCCDD, mode, persistent_calls)
            assert native == source and current_native == current_source
            persistent_calls += 1
            digest.update(repr(native).encode())
    total = len(cases) + persistent_calls
    return {'independentCases': len(cases), 'persistentCallsPerImage': persistent_calls,
            'actualOriginalAndSourceReturns': total * 2, 'stateDigest': digest.hexdigest(),
            'hostProviders': 0, 'fullByteValues': 256, 'initialNzcvCombinations': 16,
            'fullRegistersMemoryAndOrderedAccessesCompared': True, 'opaqueDefaultContextPointers': True,
            'limitations': ['Valid action 0..2 requires aligned mapped context and supported cursor memory',
                'Unterminated or malformed external stream contexts are not claimed as native validation errors',
                'Callback identity and ordinary gameplay use require separate caller evidence']}
