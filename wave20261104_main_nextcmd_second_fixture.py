import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261104_main_nextcmd_fixture import bits, floating, signed, fixed

CONTEXT, INSTRUCTION, TARGET, SP, STOP = 0x02400000, 0x02410000, 0x02420000, 0x027F0000, 0x027E0000
GAME_CALLS = {
    '020507b0': [0x0205F6A0], '02050828': [0x0205F7E0], '020508ac': [0x021E582C],
    '02050c34': [0x021E58A0], '02050c88': [0x0221221C, 0x0221225C, 0x0221229C],
    '02050d4c': [0x02211188], '02050edc': [0x02212480], '02050f4c': [0x022124B4],
    '02050fbc': [0x022122DC], '02051130': [0x021E77F8, 0x021E784C, 0x02211188, 0x02212480],
    '020511e0': [0x0221220C], '02051310': [0x0221220C], '02051458': [0x0221220C]}
STATUS_ONE = set()


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
    values = [[-129, -128, -1, 0, 47, 48, 127, 256][ordinal],
        [-128, -0.5, -1 / 8192, -0.0, 0.0, 1 / 8192, 128, 256][ordinal]]
    samples = [-1.25, -0.5, -1 / 8192, -0.0, 0.0, 1 / 8192, 0.5, 1.25]
    values.extend(samples[(ordinal + index) % 8] for index in range(14))
    if name in ('020508ac', '02050c34'):
        values[0] = [0, 1, 65535, 65536, 65537, 32768, 16777216, 256][ordinal]
    if name == '020508ac':
        values[13] = [0, 1, 255, 256, 257, 65535, 16777216, 128][ordinal]
    if name in ('020511e0', '02051310', '02051458'):
        values[0] = [-32769, -32768, -1, 0, 32767, 32768, 65535, 65536][ordinal]
        values[1] = [-65536, -32769, -32768, -1, 0, 32767, 32768, 65535][ordinal]
    if name in ('02050edc', '02050f4c', '02051130', '02050828', '02050c88'):
        values[2] = [-129, -128, -1, 0, 127, 128, 255, 256][ordinal]
    values = [floating(bits(value)) for value in values]
    context = bytearray((n * 17 + ordinal) & 255 for n in range(0x470 + 4 * 0x10C))
    context[3] = bank
    struct.pack_into('<16I', context, 16, *[bits(value) for value in values])
    positions = [0xFFFFFFFD, 0, 0x12345678, 0x80000000]
    for index, position in enumerate(positions):
        struct.pack_into('<I', context, 0x470 + index * 0x10C, position)
        context[0x477 + index * 0x10C] = 0xA5
    instruction = bytearray((n * 31 + ordinal) & 255 for n in range(128))
    struct.pack_into('<II', instruction, 0, 0x12345678, advance)
    target = bytearray((n * 23 + ordinal) & 255 for n in range(0xB8))
    struct.pack_into('<III', target, 0x70, 0xFFFFFFFD, 0, 0x80000000)
    vm.mem_write(CONTEXT, bytes(context))
    vm.mem_write(INSTRUCTION, bytes(instruction))
    vm.mem_write(TARGET, bytes(target))
    initial = [0x11220000 + n * 0x100 + ordinal for n in range(15)]
    initial[:4] = [CONTEXT, INSTRUCTION, 0xDEADBEEF, 0xA5A55A5A]
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal << 28 | 0x10)
    for register, value in zip(C.REGISTERS, initial):
        vm.reg_write(register, value)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items()}
    if len(imports) != len(row['nativeSymbolEntries']):
        raise ValueError('Provider address collapsed qualified imports')
    calls, writes, pcs = [], [], []
    returned, changed = False, False
    coordinates = [ordinal * 4096 + 1, -ordinal * 17, 0x7FFFFFFF - ordinal]

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
            stack = bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP), 8))
            call = dict(symbol=symbol, address=location, words=args, stack=stack.hex())
            if location == 0x021E582C:
                pointers = args[1:4] + [struct.unpack_from('<I', stack)[0]]
                call['vectors'] = [list(struct.unpack('<3I', bytes(uc.mem_read(pointer, 12)))) for pointer in pointers]
            elif location == 0x02211188:
                call['vectors'] = [list(struct.unpack('<3I', bytes(uc.mem_read(pointer, 12)))) for pointer in args[1:3]]
            elif location == 0x022122DC:
                call['vectors'] = [list(struct.unpack('<3I', bytes(uc.mem_read(args[2], 12))))]
            calls.append(call)
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
                if location == 0x0221220C:
                    result = TARGET
                elif location == 0x021E77F8:
                    put(args[1], struct.pack('<3I', *[word & 0xFFFFFFFF for word in coordinates]))
                elif location == 0x0221221C:
                    result = ordinal & 1
                elif location == 0x0221225C:
                    result = ordinal >> 1 & 1
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
    if name == '02050c88':
        expected_calls = [0x0221221C] + ([] if ordinal & 1 else [0x022124E8]) + [0x0221225C] + ([] if ordinal >> 1 & 1 else [0x02212518]) + [0x0221229C]
    if [call['address'] for call in game] != expected_calls:
        failures.append('Independent qualified provider sequence and four conditional paths')
    args = {'020507b0': [0, min(max(integer[0], 0), 127), integer[1]],
        '02050828': [integer[0], min(max(integer[1], 0), 127), integer[2]],
        '020508ac': [integer[0] & 65535], '02050c34': [integer[0] & 65535],
        '02050edc': integer[:3], '02050f4c': integer[:3]}
    if name in args and game[0]['words'][:len(args[name])] != [word & 0xFFFFFFFF for word in args[name]]:
        failures.append('Independent scalar, clamp and unsigned-short forwarding model')
    if name == '02050c88' and any(call['words'][:3] != [word & 0xFFFFFFFF for word in integer[:3]] for call in game):
        failures.append('Independent three-word conditional forwarding')
    if name == '020508ac':
        expected_vectors = [[fixed(values[index + component]) & 0xFFFFFFFF for component in range(3)] for index in (1, 4, 7, 10)]
        if game[0]['vectors'] != expected_vectors or struct.unpack_from('<I', bytes.fromhex(game[0]['stack']), 4)[0] != integer[13] & 255:
            failures.append('Independent twelve fixed components, four buffers and byte-width final argument')
    elif name == '02050d4c':
        expected_vectors = [[fixed(value) & 0xFFFFFFFF for value in values[2:5]], [0, fixed(values[5]) & 0xFFFFFFFF, 0]]
        if game[0]['vectors'] != expected_vectors or game[0]['words'][0] != integer[0] & 0xFFFFFFFF or game[0]['words'][3] != integer[1] & 0xFFFFFFFF:
            failures.append('Independent two three-word buffers and surrounding scalar arguments')
    elif name == '02050fbc':
        if game[0]['vectors'] != [[fixed(value) & 0xFFFFFFFF for value in values[2:5]]] or game[0]['words'][:2] != [word & 0xFFFFFFFF for word in integer[:2]] or game[0]['words'][3] != fixed(values[5]) & 0xFFFFFFFF:
            failures.append('Independent fixed buffer and fourth signed fixed argument')
    elif name == '02051130':
        expected_vectors = [[word & 0xFFFFFFFF for word in coordinates], [0, supplied & 0xFFFFFFFF, 0]]
        if game[0]['words'][0] != integer[2] & 0xFFFFFFFF or game[1]['words'][0] != integer[2] & 0xFFFFFFFF or game[2]['vectors'] != expected_vectors or game[2]['words'][0] != integer[0] & 0xFFFFFFFF or game[2]['words'][3] != integer[1] & 0xFFFFFFFF or game[3]['words'][:3] != [integer[0] & 0xFFFFFFFF, integer[1] & 0xFFFFFFFF, 1]:
            failures.append('Independent supplied output buffer, returned word and chained forwarding')
    if name in ('020511e0', '02051310', '02051458'):
        narrowed = [(((word + 32768) % 65536) - 32768) & 0xFFFFFFFF for word in integer[:2]]
        if game[0]['words'][:2] != narrowed:
            failures.append('Independent signed-halfword identities')
    expected_target = bytearray(target)
    if name in ('020511e0', '02051310'):
        for index in range(3):
            old = struct.unpack_from('<I', target, 0x70 + index * 4)[0] if name == '02051310' else 0
            struct.pack_into('<I', expected_target, 0x70 + index * 4, (old + fixed(values[index + 2])) & 0xFFFFFFFF)
    elif name == '02051458':
        expected_target[9] = 1
        struct.pack_into('<I', expected_target, 0x8C, fixed(values[2]) & 0xFFFFFFFF)
    if bytes(vm.mem_read(TARGET, len(target))) != expected_target:
        failures.append('Independent complete pointed record, three-word stores, modular additions and byte flag')
    expected = bytearray(context)
    final_bank = (bank + 1) % 4 if changed else bank
    final_advance = advance ^ 0x100 if changed else advance
    expected[3] = final_bank
    struct.pack_into('<I', expected, 0x470 + final_bank * 0x10C, (positions[final_bank] + final_advance) & 0xFFFFFFFF)
    expected[0x477 + final_bank * 0x10C] = 0
    if bytes(vm.mem_read(CONTEXT, len(context))) != expected:
        failures.append('Independent complete context, selected record, advancing and status')
    expected_instruction = bytearray(instruction)
    struct.pack_into('<I', expected_instruction, 4, final_advance)
    if bytes(vm.mem_read(INSTRUCTION, len(instruction))) != expected_instruction:
        failures.append('Independent supplied instruction mutation')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
        ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True,
        nativeCalleeBodiesExecuted=0, instructionLimit=5000, wallClockLimitMicroseconds=2000000)
