import hashlib
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2
from unicorn.arm_const import UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6
from unicorn.arm_const import UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10
from unicorn.arm_const import UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR

DATA, STACK, STOP = 0x02400000, 0x027C0000, 0x02FF0000
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
        UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
        UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def execute(body, address, kind, first_payload, second_payload, first_alignment, second_alignment, tag, same_pointer=False):
    first, second = DATA + 0x100 + first_alignment, DATA + 0x2100 + second_alignment
    memory = bytearray([0xA5]) * 0x4000
    a = first_payload.split(bytes(1), 1)[0] + bytes(1)
    b = second_payload.split(bytes(1), 1)[0] + bytes(1)
    memory[first - DATA:first - DATA + len(a)] = a
    memory[second - DATA:second - DATA + len(b)] = b
    if same_pointer:
        second, b = first, a
    expected = bytearray(memory)
    if kind == 'copy':
        expected[first - DATA:first - DATA + len(b)] = b
        result = first
    else:
        index = 0
        while a[index] == b[index] and a[index] != 0:
            index += 1
        result = (a[index] - b[index]) & 0xFFFFFFFF
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base, size in [(address & ~0xFFF, 0x1000), (DATA, 0x4000), (STACK, 0x2000), (STOP, 0x1000)]:
        machine.mem_map(base, size)
    machine.mem_write(address, body)
    machine.mem_write(DATA, bytes(memory))
    machine.mem_write(STACK, bytes([0x5A]) * 0x2000)
    machine.reg_write(UC_ARM_REG_CPSR, ((tag & 15) << 28) | 0x1F)
    for index, reg in enumerate(REGS):
        machine.reg_write(reg, (0x13579BDF * (index + 1) + tag) & 0xFFFFFFFF)
    for reg, word in [(UC_ARM_REG_R0, first), (UC_ARM_REG_R1, second),
                      (UC_ARM_REG_SP, STACK + 0x1000), (UC_ARM_REG_LR, STOP)]:
        machine.reg_write(reg, word)
    saved = [machine.reg_read(reg) for reg in REGS[4:12]]
    events, reads, writes = [], [], []
    literal = address + len(body) - 8
    assert int.from_bytes(body[-8:-4], 'little') == 0xFEFEFEFF
    assert int.from_bytes(body[-4:], 'little') == 0x80808080

    def code(uc, pc, size, user):
        if pc == STOP:
            events.append('actual-return')
            uc.emu_stop()
        else:
            assert address <= pc < literal

    def read(uc, access, pointer, size, value, user):
        if DATA <= pointer < DATA + 0x4000:
            ranges = [(second, len(b) + 3)] if kind == 'copy' else [(first, len(a) + 3), (second, len(b) + 3)]
            assert any(start <= pointer and pointer + size <= start + length for start, length in ranges)
        elif address <= pointer < address + len(body):
            assert literal <= pointer and pointer + size <= address + len(body)
        else:
            assert STACK + 0x1000 - 64 <= pointer and pointer + size <= STACK + 0x1000
        reads.append([pointer, size, int.from_bytes(uc.mem_read(pointer, size), 'little')])

    def write(uc, access, pointer, size, value, user):
        if DATA <= pointer < DATA + 0x4000:
            assert kind == 'copy' and first <= pointer and pointer + size <= first + len(b)
        else:
            assert STACK + 0x1000 - 64 <= pointer and pointer + size <= STACK + 0x1000
        writes.append([pointer, size, value & ((1 << (size * 8)) - 1)])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_READ, read)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(address, STOP + 4, count=20000, timeout=100000)
    assert events == ['actual-return'] and machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_R0) == result
    assert bytes(machine.mem_read(DATA, 0x4000)) == bytes(expected)
    assert machine.reg_read(UC_ARM_REG_SP) == STACK + 0x1000
    assert [machine.reg_read(reg) for reg in REGS[4:12]] == saved
    return {'registers': [machine.reg_read(reg) for reg in REGS], 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'sp': machine.reg_read(UC_ARM_REG_SP), 'lr': machine.reg_read(UC_ARM_REG_LR),
            'dataSha256': hashlib.sha256(expected).hexdigest(),
            'stackSha256': hashlib.sha256(bytes(machine.mem_read(STACK, 0x2000))).hexdigest(),
            'reads': reads, 'writes': writes}


def oracle(original, rebuilt, address, kind):
    cases = []
    for byte in range(256):
        for alignment in range(4):
            payload = bytes([byte]) * 5
            if kind == 'copy':
                cases.append((b'', payload, alignment, (alignment + byte % 4) % 4, False))
            else:
                cases.append((payload, payload, alignment, alignment, False))
                cases.append((payload, bytes([byte ^ 128]) * 5, alignment, (alignment + 1) % 4, False))
    for length in [0, 1, 2, 3, 4, 5, 7, 8, 15, 16, 31, 64]:
        for left in range(4):
            for right in range(4):
                for pattern in range(3):
                    a = bytes(((index * [0, 73, 251][pattern] + pattern * 127) % 255 + 1) for index in range(length))
                    b = a
                    if kind != 'copy' and a and pattern:
                        position = 0 if pattern == 1 else len(a) - 1
                        altered = bytearray(a)
                        altered[position] = (altered[position] % 255) + 1
                        b = bytes(altered)
                    cases.append((a, b, left, right, False))
        for alignment in range(4):
            cases.append((bytes([128]) * length, b'', alignment, alignment, True))
    digest = hashlib.sha256()
    for index, (a, b, first_alignment, second_alignment, same) in enumerate(cases):
        native = execute(original, address, kind, a, b, first_alignment, second_alignment, index, same)
        source = execute(rebuilt, address, kind, a, b, first_alignment, second_alignment, index, same)
        assert native == source
        digest.update(repr(native).encode())
    return {'cases': len(cases), 'actualOriginalAndSourceReturns': len(cases) * 2,
            'stateDigest': digest.hexdigest(), 'hostProviders': 0, 'fullByteValues': 256,
            'pointerAlignments': 4, 'initialNzcvCombinations': 16, 'literalBytes': 8,
            'instructionBytes': len(original) - 8, 'actualDataAndStackEffectsCompared': True,
            'samePointerCases': 48,
            'limitations': ['Synthetic padded RAM strings; word reads may inspect up to three bytes past the terminator',
                'Partially overlapping copy ranges, unbounded strings and invalid pointers are unsupported',
                'No natural gameplay or original SDK version claim follows from the reference-supported routine identity']}
