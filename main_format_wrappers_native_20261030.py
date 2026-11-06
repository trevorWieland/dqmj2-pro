import hashlib
import struct
from project import ROOT, configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2
from unicorn.arm_const import UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6
from unicorn.arm_const import UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10
from unicorn.arm_const import UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR

DATA, STACK, STOP = 0x02500000, 0x027C0000, 0x02FF0000
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
        UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
        UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def execute(main, entry, format_bytes, arguments, expected_text, capacity, alignment, null_destination, tag):
    memory = bytearray([0xA5]) * 0x4000
    output = 0 if null_destination else DATA + 0x100 + alignment
    format_address, argument_address = DATA + 0x500, DATA + 0x700
    memory[0x500:0x500 + len(format_bytes) + 1] = format_bytes + bytes(1)
    words = []
    for index, item in enumerate(arguments):
        if isinstance(item, bytes):
            pointer = DATA + 0x1000 + index * 0x100
            memory[pointer - DATA:pointer - DATA + len(item) + 1] = item + bytes(1)
            words.append(pointer)
        else:
            words.append(item & 0xFFFFFFFF)
    argument_bytes = b''.join(word.to_bytes(4, 'little') for word in words)
    memory[0x700:0x700 + len(argument_bytes)] = argument_bytes
    expected = bytearray(memory)
    if output and capacity:
        copied = min(len(expected_text), capacity - 1)
        expected[output - DATA:output - DATA + copied + 1] = expected_text[:copied] + bytes(1)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (DATA, 0x4000), (STACK, 0x8000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(DATA, bytes(memory))
    machine.mem_write(STACK, bytes([0x5A]) * 0x8000)
    machine.reg_write(UC_ARM_REG_CPSR, ((tag & 15) << 28) | 0x1F)
    for index, reg in enumerate(REGS):
        machine.reg_write(reg, (0x13579BDF * (index + 1) + tag) & 0xFFFFFFFF)
    sp = STACK + 0x6000
    if entry == 0x0201D3DC:
        registers = [output, capacity, format_address, argument_address]
    else:
        padded = words + [0, 0]
        registers = [output, format_address, padded[0], padded[1]]
        machine.mem_write(sp, b''.join(word.to_bytes(4, 'little') for word in words[2:]))
    for reg, value in zip(REGS[:4], registers):
        machine.reg_write(reg, value)
    machine.reg_write(UC_ARM_REG_SP, sp)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    saved = [machine.reg_read(reg) for reg in REGS[4:12]]
    events, writes, entries = [], [], {}

    def code(uc, address, size, user):
        if address == STOP:
            events.append('actual-return')
            uc.emu_stop()
        else:
            assert 0x02000000 <= address < 0x02400000
            if address in [0x0201D3DC, 0x0201D444, 0x0201CB74, 0x0201D398, 0x0201B19C]:
                entries[hex(address)] = entries.get(hex(address), 0) + 1

    def store(uc, access, address, size, value, user):
        if DATA <= address < DATA + 0x4000:
            assert output and capacity and output <= address and address + size <= output + min(capacity, len(expected_text) + 1)
        else:
            assert STACK <= address and address + size <= STACK + 0x8000
        writes.append([address, size, value & ((1 << (8 * size)) - 1)])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, store)
    machine.emu_start(entry, STOP + 4, count=200000, timeout=1000000)
    assert events == ['actual-return'] and machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_R0) == len(expected_text)
    assert machine.reg_read(UC_ARM_REG_SP) == sp
    assert [machine.reg_read(reg) for reg in REGS[4:12]] == saved
    assert bytes(machine.mem_read(DATA, 0x4000)) == bytes(expected)
    assert bytes(machine.mem_read(0x02000000, len(main))) == main
    return {'registers': [machine.reg_read(reg) for reg in REGS], 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'sp': machine.reg_read(UC_ARM_REG_SP), 'lr': machine.reg_read(UC_ARM_REG_LR),
            'dataSha256': hashlib.sha256(expected).hexdigest(),
            'stackSha256': hashlib.sha256(bytes(machine.mem_read(STACK, 0x8000))).hexdigest(),
            'writes': writes, 'entryObservationsNotReturnCredits': entries}


def oracle(original, rebuilt):
    formats = [(b'', [], b''), (b'abc', [], b'abc'), (b'%s', [b'one'], b'one'),
               (b'%s/%s', [b'one', b'two'], b'one/two'),
               (b'[%s:%s:%s:%s:%s]', [b'a', b'b', b'c', b'd', b'e'], b'[a:b:c:d:e]'),
               (b'%s', [bytes([128, 255, 65])], bytes([128, 255, 65])),
               (b'%d/%u/%x', [-1, 0xFFFFFFFF, 0x80000000], b'-1/4294967295/80000000'),
               (b'%c-%c', [65, 255], bytes([65, 45, 255]))]
    records, digest = [], hashlib.sha256()
    for entry in [0x0201D3DC, 0x0201D444]:
        capacities = [0, 1, 2, 3, 4, 8, 16, 64] if entry == 0x0201D3DC else [0xFFFFFFFF]
        for format_bytes, arguments, text in formats:
            for capacity in capacities:
                for alignment in range(4):
                    for null in ([False, True] if capacity == 0 else [False]):
                        tag = len(records)
                        native = execute(original, entry, format_bytes, arguments, text, capacity, alignment, null, tag)
                        source = execute(rebuilt, entry, format_bytes, arguments, text, capacity, alignment, null, tag)
                        assert native == source
                        digest.update(repr(native).encode())
                        records.append({'entry': hex(entry), 'formatHex': format_bytes.hex(), 'capacity': capacity,
                                        'alignment': alignment, 'nullDestination': null})
    return {'cases': len(records), 'actualOriginalAndSourceReturns': len(records) * 2,
            'stateDigest': digest.hexdigest(), 'hostProviders': 0,
            'literalStringsIntegerAndByteArgumentsOnly': True, 'records': records,
            'helperEntryObservationsAreNotReturnOrSourceCredits': True,
            'limitations': ['Original formatter/writer/memory helpers remain execution context with zero source credit',
                'ARM32 variadic register-home arithmetic is target-specific and is not a portable host va_list',
                'Floating, long-long, percent-n, malformed formats, positive-capacity null buffers and invalid pointers are unsupported']}
