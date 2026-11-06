import hashlib
import itertools
import re
import struct
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
from main_format_wrappers_native_20261030 import REGS

DATA, STACK, STOP = 0x02500000, 0x027C0000, 0x02FF0000
ENTRY = 0x0201B338
PATTERN = re.compile(r'^%(?P<flags>[-+ #0]*)(?P<width>\*|[1-9][0-9]*|)(?P<precision>\.(?:\*|[0-9]*))?(?P<length>hh|ll|[hlLjtz])?(?P<char>[\s\S]?)')
LENGTHS = {'': 0, 'hh': 1, 'h': 2, 'l': 3, 'll': 4, 'L': 9, 'j': 6, 'z': 7, 't': 8}


def cases():
    for byte in range(256):
        yield bytes([37, byte, 90]), (-7, 3)
        yield bytes([37, 46, byte, 90]), (-7, 3)
        yield bytes([37, 76, byte, 90]), (-7, 3)
    for length, conversion in itertools.product(LENGTHS, 'diuoxXfFaAgGeEpcsn'):
        yield ('%' + length + conversion + 'Z').encode(), ()
    for flags, width, precision, conversion in itertools.product(['', '-', '0', '-0', '0-', '+ ', ' +', '#0'],
                                                               ['', '0', '1', '509', '510', '*'],
                                                               ['', '.', '.0', '.3', '.*'], 'dxfgscp'):
        yield ('%' + flags + width + precision + conversion + 'Z').encode(), (-7, 3)
    for width, precision in itertools.product([-509, -1, 0, 1, 509, 510], [-7, -1, 0, 1, 509, 510]):
        for conversion in 'dfgs':
            yield ('%*.*' + conversion + 'Z').encode(), (width, precision)
    for text in ['%', '%h', '%ll', '%999d', '%#%', '%q', '%012.3d', '%0*.*s']:
        yield text.encode(), (-3, -1)


def model(text, arguments):
    value = text.decode('latin1')
    if value.startswith('%%'):
        return [1, 0, 0, 0, 0, 37, 0, 0], 2, 0
    match = PATTERN.match(value)
    assert match
    flags, width_text, precision_text, length, character = match.group('flags', 'width', 'precision', 'length', 'char')
    justification = 0 if '-' in flags else 2 if '0' in flags else 1
    sign = 1 if '+' in flags else 2 if ' ' in flags else 0
    alternate = int('#' in flags)
    consumed = 0
    width = int(width_text or 0) if width_text != '*' else arguments[consumed]
    if width_text == '*':
        consumed += 1
        if width < 0:
            justification, width = 0, -width
    if width > 509:
        return [justification, sign, 0, alternate, 0, 255, width, 0], match.end('width') + 1, consumed
    specified = int(precision_text is not None)
    precision = 0
    if precision_text:
        if precision_text == '.*':
            precision = arguments[consumed]
            consumed += 1
            specified = int(precision >= 0)
        else:
            precision = int(precision_text[1:] or 0)
    argument = LENGTHS[length or '']
    conversion = ord(character) if character else 0
    if character and character in 'diuoxX':
        if argument == 9:
            conversion = 255
        elif not specified:
            precision = 1
        elif justification == 2:
            justification = 1
    elif character and character in 'fF':
        if argument in {2, 4, 6, 7, 8}:
            conversion = 255
        elif not specified:
            precision = 6
    elif character and character in 'aA':
        if not specified:
            precision = 13
        if argument in {1, 2, 4, 6, 7, 8}:
            conversion = 255
    elif character and character in 'gGeE':
        if character in 'gG' and precision == 0:
            precision = 1
        if argument in {1, 2, 4, 6, 7, 8}:
            conversion = 255
        elif not specified:
            precision = 6
    elif character == 'p':
        conversion, alternate, argument, precision = 120, 1, 3, 8
    elif character == 'c':
        if argument == 3:
            argument = 5
        elif specified or argument != 0:
            conversion = 255
    elif character == 's':
        if argument == 3:
            argument = 5
        elif argument != 0:
            conversion = 255
    elif character == 'n':
        if argument == 9:
            conversion = 255
    else:
        conversion = 255
    return [justification, sign, specified, alternate, argument, conversion, width, precision], match.end() + int(not character), consumed


def execute(main, case, tag):
    text, arguments = case
    fields, cursor, consumed = model(text, arguments)
    memory = bytearray([0xA5]) * 0x1000
    memory[0x100:0x100 + len(text) + 1] = text + b'\0'
    memory[0x40:0x44] = struct.pack('<I', DATA + 0x800)
    for index, word in enumerate(arguments):
        memory[0x800 + index * 4:0x804 + index * 4] = struct.pack('<I', word & 0xFFFFFFFF)
    expected = bytearray(memory)
    expected[0x40:0x44] = struct.pack('<I', DATA + 0x800 + consumed * 4)
    expected[0x400:0x410] = bytes(fields[:6]) + bytes([0x5A, 0x5A]) + struct.pack('<ii', *fields[6:])
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (DATA, 0x1000), (STACK, 0x8000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(DATA, bytes(memory))
    machine.mem_write(STACK, bytes([0x5A]) * 0x8000)
    machine.reg_write(UC_ARM_REG_CPSR, ((tag & 15) << 28) | (0xC0 if tag & 16 else 0) | 0x1F)
    for index, reg in enumerate(REGS):
        machine.reg_write(reg, (0x13579BDF * (index + 1) + tag) & 0xFFFFFFFF)
    for reg, word in zip(REGS[:3], [DATA + 0x100, DATA + 0x40, DATA + 0x400]):
        machine.reg_write(reg, word)
    sp = STACK + 0x6000
    machine.reg_write(UC_ARM_REG_SP, sp)
    machine.reg_write(UC_ARM_REG_LR, STOP | (tag & 1))
    preserved = [machine.reg_read(reg) for reg in REGS[4:12]]
    stores, events, pcs = [], [], set()
    steps = [0]

    def code(uc, address, size, user):
        steps[0] += 1
        if address == STOP:
            events.append('actual-return')
            uc.emu_stop()
        else:
            assert ENTRY <= address < ENTRY + 1416
            pcs.add(address)

    def store(uc, access, address, size, word, user):
        if DATA <= address < DATA + 0x1000:
            assert DATA + 0x40 <= address and address + size <= DATA + 0x44 or DATA + 0x400 <= address and address + size <= DATA + 0x410
            stores.append([address, size, word & ((1 << (size * 8)) - 1)])
        else:
            assert STACK <= address and address + size <= STACK + 0x8000

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, store)
    machine.emu_start(ENTRY, STOP + 4, count=100000, timeout=1000000)
    assert events == ['actual-return']
    assert machine.reg_read(UC_ARM_REG_PC) == STOP and machine.reg_read(UC_ARM_REG_SP) == sp
    assert [machine.reg_read(reg) for reg in REGS[4:12]] == preserved
    assert machine.reg_read(REGS[0]) == DATA + 0x100 + cursor, (case, cursor, hex(machine.reg_read(REGS[0])))
    assert bytes(machine.mem_read(DATA, 0x1000)) == expected, (case, fields, bytes(machine.mem_read(DATA + 0x400, 16)).hex())
    assert bytes(machine.mem_read(0x02000000, len(main))) == main
    return {'actualReturn': True, 'fields': fields, 'cursor': cursor, 'consumedWords': consumed,
            'stores': stores, 'registers': [machine.reg_read(reg) for reg in REGS],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'lr': machine.reg_read(UC_ARM_REG_LR),
            'stackSha256': hashlib.sha256(bytes(machine.mem_read(STACK, 0x8000))).hexdigest(),
            'instructions': steps[0], 'pcs': sorted(pcs)}
