import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261104_main_nextcmd_fixture import bits, floating, signed, fixed

CONTEXT, INSTRUCTION, SP, STOP = 0x02400000, 0x02410000, 0x027F0000, 0x027E0000
GAME_CALLS = {
    '0205182c': [0x02212720], '02051970': [0x0205BE34, 0x0204040C],
    '020519cc': [0x020406EC], '02051a14': [0x020406EC], '02051a5c': [0x0205BF5C],
    '02051aa8': [0x02063144], '02051afc': [0x020630E4], '02051b68': [0x02062B0C],
    '02051c38': [0x020405CC], '02051c88': [0x02081FC8], '02051cec': [0x020820AC],
    '02051d3c': [0x02081FC8], '02051dac': [0x020823F4], '02051dfc': [0x02082458],
    '02051e4c': [0x022129F8], '02051ea8': [0x02212C94], '02052074': [0x02212E1C]}
STATUS_ONE = {'02051c88', '02051cec', '02051d3c', '02051dac', '02051dfc'}


def run(row, body, ordinal, main):
    name = format(int(row['address'], 0), '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(int(row['address'], 0), body)
    bank = ordinal % 4
    advance = [0, 4, 0xFFFFFFFF, 16, 100, 1, 0x80000000, 8][ordinal]
    supplied = [0, 1, -1, 127, -128, 12345, -12345, 0x3FFFFFFF][ordinal]
    samples = [-1.25, -0.5, -1 / 8192, -0.0, 0.0, 1 / 8192, 0.5, 1.25]
    values = [[-129, -128, -1, 0, 17, 18, 127, 256][ordinal]]
    values.extend(samples[(ordinal + index) % 8] for index in range(7))
    if name in ('02051970', '02051a5c', '02051c38', '02051ea8'):
        values[0] = [0, 1, 255, 256, 257, 65535, 16777216, 128][ordinal]
    if name == '02051afc':
        values[1] = [-129, -128, -1, 0, 127, 128, 255, 256][ordinal]
    if name == '02051ea8':
        values[5] = [0, 1, 255, 256, 257, 65535, 16777216, 128][ordinal]
        values[6] = [-32769, -32768, -1, 0, 32767, 32768, 65535, 65536][ordinal]
    values = [floating(bits(value)) for value in values]
    context = bytearray((n * 17 + ordinal) & 255 for n in range(0x470 + 4 * 0x10C))
    context[3] = bank
    struct.pack_into('<8I', context, 16, *[bits(value) for value in values])
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
    for register, value in zip(C.REGISTERS, initial):
        vm.reg_write(register, value)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items()}
    if len(imports) != len(row['nativeSymbolEntries']):
        raise ValueError('Qualified provider imports collapsed by address')
    calls, writes, pcs = [], [], []
    returned, changed = False, False

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
                raise ValueError('ARM provider entered in Thumb mode')
            symbol = imports[location]
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            stack = bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP), 16))
            calls.append(dict(symbol=symbol, address=location, words=args, stack=stack.hex()))
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
                flags = (0x20000000 if floating(args[0]) > floating(args[1]) else 0x40000000) | 0x10
            else:
                if name in STATUS_ONE:
                    result = ordinal & 1
                if ordinal % 2 and not changed:
                    put(CONTEXT + 3, bytes([(bank + 1) % 4]))
                    put(INSTRUCTION + 4, struct.pack('<I', advance ^ 0x100))
                    changed = True
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, register in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xCAFE0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, result)
            uc.reg_write(R.UC_ARM_REG_CPSR, flags)
            uc.reg_write(R.UC_ARM_REG_PC, lr)

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(int(row['address'], 0), STOP + 4, timeout=2000000, count=5000)
    if not returned:
        raise ValueError(('Caller did not actually return within both bounds', name, ordinal))
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Callee-saved register or SP changed')
    failures = []
    game = [call for call in calls if not call['symbol'].startswith('_')]
    integer = [int(value) for value in values]
    expected_calls = list(GAME_CALLS[name])
    if name == '02051e4c' and integer[0] >= 18:
        expected_calls = []
    if [call['address'] for call in game] != expected_calls:
        failures.append('Independent qualified provider sequence and signed upper-bound guard')
    narrow = ((integer[1] + 128) % 256) - 128
    byte_first = ((integer[0] + 128) % 256) - 128
    expected_args = {'02051970': [integer[0] & 255], '020519cc': [0], '02051a14': [1],
        '02051a5c': [integer[0]], '02051aa8': integer[:1], '02051afc': [integer[0], narrow],
        '02051c38': [integer[0] & 255], '02051c88': [byte_first, 1], '02051d3c': [byte_first, 0],
        '02051e4c': integer[:1], '02052074': integer[:1]}
    if game and name in expected_args and game[0]['words'][:len(expected_args[name])] != [word & 0xFFFFFFFF for word in expected_args[name]]:
        failures.append('Independent signed byte, unsigned byte and scalar forwarding')
    if name == '02051970' and game[1]['words'][0] != integer[0] & 255:
        failures.append('Independent byte forwarded to both ordered providers')
    if name == '0205182c':
        expected = integer[:2] + [fixed(value) for value in values[2:5]]
        actual = game[0]['words'] + [struct.unpack_from('<I', bytes.fromhex(game[0]['stack']))[0]]
        if actual != [word & 0xFFFFFFFF for word in expected]:
            failures.append('Independent twelve-byte by-value struct split across R2/R3 and stack')
    elif name == '02051ea8':
        short = ((integer[6] + 32768) % 65536) - 32768
        expected = [integer[0] & 255] + [fixed(value) for value in values[1:5]] + [integer[5] & 255, 0, short]
        actual = game[0]['words'] + list(struct.unpack('<4I', bytes.fromhex(game[0]['stack'])))
        if actual != [word & 0xFFFFFFFF for word in expected]:
            failures.append('Independent eight physical words, four fixed values and byte/short boundaries')
    expected = bytearray(context)
    final_bank = (bank + 1) % 4 if changed else bank
    final_advance = advance ^ 0x100 if changed else advance
    expected[3] = final_bank
    if name not in STATUS_ONE or ordinal & 1:
        struct.pack_into('<I', expected, 0x470 + final_bank * 0x10C, (positions[final_bank] + final_advance) & 0xFFFFFFFF)
    expected[0x477 + final_bank * 0x10C] = int(name in STATUS_ONE)
    if name in ('02051aa8', '02051afc', '02051b68', '02051ea8') or name == '02051e4c' and expected_calls:
        struct.pack_into('<I', expected, 16, bits(float(supplied)))
    if bytes(vm.mem_read(CONTEXT, len(context))) != expected:
        failures.append('Independent complete context, conditional advancing, signed output and status')
    expected_instruction = bytearray(instruction)
    struct.pack_into('<I', expected_instruction, 4, final_advance)
    if bytes(vm.mem_read(INSTRUCTION, len(instruction))) != expected_instruction:
        failures.append('Independent supplied instruction mutation')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
        ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True,
        nativeCalleeBodiesExecuted=0, instructionLimit=5000, wallClockLimitMicroseconds=2000000)
