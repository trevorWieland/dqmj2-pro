import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261104_main_tail_proof import bits, floating, signed, fixed, CONTEXT, INSTRUCTION, SP, STOP, REGS

SPECS = {
    '020584d4': dict(calls=[0x0220913C]),
    '0205860c': dict(calls=[0x0220925C]),
    '020588f0': dict(calls=[0x02063520]),
    '02058cd0': dict(calls=[0x021F4280, 0x021F4298]),
    '020591fc': dict(record='field18'),
    '02059278': dict(record='entry'),
    '0205930c': dict(record='field1e'),
    '02059388': dict(calls=[0x0205EB0C])}

CONDITIONAL, STATUS_ONE = set(), set()


def run(row, body, ordinal, main, overlay):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(0x021D7240, overlay)
    vm.mem_write(address, body)
    spec = SPECS[name]
    bank = ordinal % 4
    advance = [0, 4, 0xFFFFFFFF, 16, 100, 1, 0x80000000, 8][ordinal]
    supplied = [0, 1, -1, 127, 128, 255, -32768, 65535][ordinal]
    first = [0, 1, 2, 255, 256, 257, 258, 65535][ordinal]
    values = [first, [-1.25, -0.5, -1 / 8192, 0, 1 / 8192, 0.5, 1.25, 100][ordinal],
              [-129, -128, -1, 0, 127, 128, 255, 256][ordinal], [1.5, -1.5, 0.5, -0.5, 100, -100, 0, 1][ordinal],
              [-1.5, -0.5, -1 / 8192, 0, 1 / 8192, 0.5, 1.5, 100][ordinal],
              [0, 1, 127, 128, 255, 256, 257, 65535][ordinal], 2, 3]
    if spec.get('record'):
        values[0] = [0, 1, 0, -1, 2, 0, 255, 0][ordinal]
        values[2] = [0, 1, 2, 3, 4, 0, 4, 2][ordinal]
    elif name == '020584d4':
        values[1] = [0, 1, 127, 128, 255, 256, 257, 65535][ordinal]
    elif name == '0205860c':
        values[:2] = [[-65537, -32769, -32768, -1, 0, 32767, 32768, 65535][ordinal],
                      [-65536, -32768, -1, 0, 1, 32768, 65535, 65536][ordinal]]
    elif name == '02058cd0':
        values[0] = [-1.25, -0.5, -1 / 8192, -0.0, 0, 1 / 8192, 0.5, 1.25][ordinal]
    values = [floating(bits(v)) for v in values]
    context = bytearray((n * 17 + ordinal) & 255 for n in range(0x470 + 4 * 0x10C))
    context[3] = bank
    struct.pack_into('<8I', context, 16, *[bits(v) for v in values])
    positions = [0xFFFFFFFD, 0, 0x12345678, 0x80000000]
    for index, position in enumerate(positions):
        struct.pack_into('<I', context, 0x470 + index * 0x10C, position)
        context[0x477 + index * 0x10C] = 0xA5
    instruction = bytearray((n * 31 + ordinal) & 255 for n in range(128))
    struct.pack_into('<II', instruction, 0, 0x12345678, advance)
    vm.mem_write(CONTEXT, bytes(context))
    vm.mem_write(INSTRUCTION, bytes(instruction))
    initial = [0x11220000 + n * 0x100 + ordinal for n in range(15)]
    initial[:4] = [CONTEXT, INSTRUCTION, 0xDEADBEEF, 0xA5A55A5A]
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal << 28 | 0x10)
    for register, value in zip(REGS, initial):
        vm.reg_write(register, value)
    calls, writes, pcs = [], [], []
    returned, changed = False, False
    record_address = 0x02430000
    record_present = ordinal % 3 != 0
    record = bytearray((index * 13 + ordinal) & 255 for index in range(256))
    record_short = [-32768, -129, -1, 0, 1, 127, 128, 32767][ordinal]
    struct.pack_into('<h', record, 0x18, record_short)
    record[0x1e] = [0, 1, 127, 128, 255, 0, 255, 32][ordinal]
    for index in range(5):
        record[0x7a + 2 * index] = (index * 47 + ordinal * 31) & 255
    vm.mem_write(record_address, bytes(record))
    primary = [0, 1, 0, -1, 0, 0, 5, 0][ordinal]
    secondary = [0, 0, 1, 0, -1, 0, 0, 7][ordinal]
    scaled_second = ((supplied & 0xFFFFFFFF) ^ 0x1357)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items()}

    def put(location, data):
        vm.mem_write(location, data)
        writes.append(dict(provider=True, address=location, hex=data.hex()))

    def memory(uc, access, location, size, value, user):
        writes.append(dict(provider=False, address=location, size=size, value=value))

    def code(uc, location, size, user):
        nonlocal returned, changed
        pcs.append(location)
        if location == STOP:
            returned = True
            uc.emu_stop()
        elif location in imports:
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('Qualified ARM provider entered as Thumb')
            symbol = imports[location]
            args = [uc.reg_read(r) for r in REGS[:4]]
            calls.append(dict(symbol=symbol, address=location, words=args, stack=bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP), 16)).hex()))
            result = supplied & 0xFFFFFFFF
            flags = ((ordinal + len(calls)) & 15) << 28 | 0x10
            if symbol in ('_ffix', '_ffixu'):
                result = int(floating(args[0])) & 0xFFFFFFFF
            elif symbol == '_fflt':
                result = bits(float(signed(args[0])))
            elif symbol == '_ffltu':
                result = bits(float(args[0]))
            elif symbol in ('_fadd', '_fsub', '_fmul', '_fdiv'):
                left, right = floating(args[0]), floating(args[1])
                result = bits(left + right if symbol == '_fadd' else left - right if symbol == '_fsub' else left * right if symbol == '_fmul' else left / right)
            elif symbol == '_fgr':
                comparison = floating(args[0]) > floating(args[1])
                flags = (0x20000000 if comparison else 0x40000000) | 0x10
            else:
                if ordinal % 2 and not changed:
                    put(CONTEXT + 3, bytes([(bank + 1) % 4]))
                    put(INSTRUCTION + 4, struct.pack('<I', advance ^ 0x100))
                    changed = True
                if location in (0x02062A50, 0x02062A88):
                    result = record_address if record_present else 0
                elif location == 0x02063520:
                    result = primary & 0xFFFFFFFF
                elif location == 0x020635D4:
                    result = secondary & 0xFFFFFFFF
                elif location == 0x021F4298:
                    result = scaled_second
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, register in enumerate(REGS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xCAFE0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, result)
            uc.reg_write(R.UC_ARM_REG_CPSR, flags)
            uc.reg_write(R.UC_ARM_REG_PC, lr)

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=5000)
    if not returned:
        raise ValueError(('Caller did not actually return', name, ordinal))
    registers = [vm.reg_read(register) for register in REGS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Callee-saved/SP differs')
    failures = []
    game = [call for call in calls if not call['symbol'].startswith('_')]
    integer = [int(v) & 0xFFFFFFFF for v in values]
    expected_calls = [0x02062A50 if integer[0] == 0 else 0x02062A88] if spec.get('record') else list(spec['calls'])
    if name == '020588f0' and not primary:
        expected_calls.append(0x020635D4)
    if [call['address'] for call in game] != expected_calls:
        failures.append('Independent nullable provider selection and short-circuit sequence')
    def narrow16(value):
        low = value & 65535
        return (low - 65536 if low & 32768 else low) & 0xFFFFFFFF
    expected_words = {
        '020584d4': [integer[0] & 255, integer[1] & 255, integer[2], integer[3]],
        '0205860c': [narrow16(integer[0]), narrow16(integer[1])],
        '020588f0': integer[:2],
        '02058cd0': [fixed(values[0])],
        '02059388': [integer[0], fixed(values[1]), fixed(values[2]), fixed(values[3])]}
    if spec.get('record'):
        expected_words[name] = [integer[1]]
    if game[0]['words'][:len(expected_words[name])] != expected_words[name]:
        failures.append('Independent integer, signed-short, byte or fixed conversion arguments')
    if name == '02058cd0' and game[1]['words'][0] != fixed(values[1]):
        failures.append('Independent second fixed argument')
    if name == '020588f0' and len(game) == 2 and game[1]['words'][:2] != integer[:2]:
        failures.append('Independent secondary query forwarding')
    if name == '020584d4' and list(struct.unpack('<II', bytes.fromhex(game[0]['stack'])[:8])) != integer[4:6]:
        failures.append('Independent fifth and sixth scalar stack arguments')
    if name == '02059388' and struct.unpack('<I', bytes.fromhex(game[0]['stack'])[:4])[0] != fixed(values[4]):
        failures.append('Independent fifth fixed stack argument')
    if bytes(vm.mem_read(record_address, len(record))) != record:
        failures.append('Independent pointed record remains read-only')
    expected = bytearray(context)
    final_bank = (bank + 1) % 4 if changed else bank
    final_advance = advance ^ 0x100 if changed else advance
    expected[3] = final_bank
    do_advance = name not in CONDITIONAL or ordinal % 2 != 0
    if do_advance:
        struct.pack_into('<I', expected, 0x470 + final_bank * 0x10C, (positions[final_bank] + final_advance) & 0xFFFFFFFF)
    expected[0x477 + final_bank * 0x10C] = int(name in STATUS_ONE)
    outputs = {}
    if name == '020588f0':
        outputs = {0: float(bool(primary or secondary))}
    elif name == '02058cd0':
        outputs = {0: floating(bits(float(supplied))) / 4096.0, 1: floating(bits(float(signed(scaled_second)))) / 4096.0}
    elif spec.get('record'):
        value = record_short if spec['record'] == 'field18' else record[0x1e] if spec['record'] == 'field1e' else record[0x7a + 2 * integer[2]]
        outputs = {0: float(value if record_present else 0)}
    for index, value in outputs.items():
        struct.pack_into('<I', expected, 16 + index * 4, bits(value))
    if bytes(vm.mem_read(CONTEXT, len(context))) != expected:
        failures.append('Independent complete context, selected record stride, conditional position and status model')
    expected_instruction = bytearray(instruction)
    struct.pack_into('<I', expected_instruction, 4, final_advance)
    if bytes(vm.mem_read(INSTRUCTION, len(instruction))) != expected_instruction:
        failures.append('Independent instruction forwarding and supplied mutation model')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes,
                pcs=pcs, ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)

