import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261104_main_tail_proof import bits, floating, signed, fixed, CONTEXT, INSTRUCTION, SP, STOP, REGS

SPECS = {
    '020548c4': dict(calls=[0x0203D0B4], args='one-int', output='u32'),
    '02054918': dict(calls=[0x0203D0C0], args='int-byte', output='u32'),
    '020549d4': dict(calls=[0x0203D0D8], args='two-int', output='s32'),
    '02054a9c': dict(calls=[0x02063DA8], output='s32'),
    '02054ae8': dict(calls=[0x02063DB8], args='one-int'),
    '02054b34': dict(calls=[0x021E0744], args='one-int', output='s32'),
    '02054b88': dict(calls=[0x020725E8, 0x020C1FDC], args='byte-array'),
    '02054c1c': dict(calls=[0x020725E8, 0x020C1FDC], args='selector-array'),
    '02054d50': dict(calls=[0x020725E8, 0x021D8754], args='word-halfword'),
    '02054dbc': dict(calls=[0x021D9760], args='signed-byte', earlyAdvance=True),
    '02054e14': dict(calls=[0x021D8624], args='signed-byte', earlyAdvance=True)}

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
    first = [-1, 0, 1, -32768, 32767, 65535, 16777216, -129][ordinal]
    values = [first, [0, 1, 255, 256, 65535, 16777216, 4294967040, 128][ordinal],
              [255, 256, 65535, 16777216, 4294967040, 128, 0, 1][ordinal],
              [65535, 16777216, 4294967040, 128, 0, 1, 255, 256][ordinal],
              [4294967040, 128, 0, 1, 255, 256, 65535, 16777216][ordinal], 100, 200, 300]
    if spec.get('args') == 'selector-array':
        values[1] = [0, 1, 2, 3, -1, 4, 0, 3][ordinal]
    elif spec.get('args') == 'two-int':
        values[1] = [-32768, -129, -128, -1, 0, 1, 127, 32767][ordinal]
    elif spec.get('args') == 'word-halfword':
        values[1] = [0, 1, 255, 256, 65535, 65536, 4294967040, 131071][ordinal]
    elif spec.get('args') == 'signed-byte':
        values[0] = [-257, -129, -128, -1, 0, 127, 128, 255][ordinal]
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
    calls, writes, pcs, early_errors = [], [], [], []
    returned, changed = False, False
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
            if location == 0x020C1FDC:
                calls[-1]['bufferHex'] = bytes(uc.mem_read(args[1], 4)).hex()
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
                if spec.get('earlyAdvance') and struct.unpack('<I', bytes(uc.mem_read(CONTEXT + 0x470 + bank * 0x10c, 4)))[0] != (positions[bank] + advance) & 0xFFFFFFFF:
                    early_errors.append('Record must advance before native provider entry')
                if ordinal % 2 and not changed:
                    put(CONTEXT + 3, bytes([(bank + 1) % 4]))
                    put(INSTRUCTION + 4, struct.pack('<I', advance ^ 0x100))
                    changed = True
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
    failures.extend(early_errors)
    if [call['address'] for call in game] != spec['calls']:
        failures.append('Independent complete provider sequence')
    kind = spec.get('args')
    expected_words = {'one-int': integer[:1], 'int-byte': [integer[0], integer[1] & 255], 'two-int': integer[:2],
                      'byte-array': integer[:1], 'selector-array': integer[:1], 'word-halfword': integer[:1],
                      'signed-byte': [((integer[0] & 255) - 256 if integer[0] & 128 else integer[0] & 255) & 0xFFFFFFFF]}
    args = expected_words.get(kind, [])
    if game[0]['words'][:len(args)] != args:
        failures.append('Independent signed integer, signed byte and unsigned byte forwarding')
    if kind in ('byte-array', 'selector-array'):
        expected_bytes = bytes(v & 255 for v in integer[1:5]) if kind == 'byte-array' else bytes(100 if index == signed(integer[1]) else 0 for index in range(4))
        if game[1]['words'][0] != supplied & 0xFFFFFFFF or game[1]['bufferHex'] != expected_bytes.hex():
            failures.append('Independent opaque returned word and complete four-byte provider buffer')
        if not SP - 256 <= game[1]['words'][1] <= SP - 4:
            failures.append('Caller-owned four-byte buffer address')
    if kind == 'word-halfword' and game[1]['words'][:2] != [supplied & 0xFFFFFFFF, integer[1] & 65535]:
        failures.append('Independent opaque word and unsigned-halfword forwarding to overlay7')
    expected = bytearray(context)
    final_bank = (bank + 1) % 4 if changed else bank
    final_advance = advance ^ 0x100 if changed else advance
    expected[3] = final_bank
    do_advance = name not in CONDITIONAL or ordinal % 2 != 0
    if do_advance:
        selected_bank, selected_advance = (bank, advance) if spec.get('earlyAdvance') else (final_bank, final_advance)
        struct.pack_into('<I', expected, 0x470 + selected_bank * 0x10C, (positions[selected_bank] + selected_advance) & 0xFFFFFFFF)
    expected[0x477 + final_bank * 0x10C] = int(name in STATUS_ONE)
    outputs = {0: float(supplied & 0xFFFFFFFF if spec['output'] == 'u32' else supplied)} if spec.get('output') else {}
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

