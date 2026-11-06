import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261104_main_nextcmd_fixture import bits, floating, fixed

CONTEXT, INSTRUCTION, TARGET, SP, STOP = 0x02400000, 0x02410000, 0x02420000, 0x027F0000, 0x027E0000
GAME_CALLS = {'02051510': [0x0221220C, 0x02028158, 0x02028158, 0x02028158,
    0x02000CE8, 0x020280A0, 0x02028044, 0x02027FE8, 0x02000E1C, 0x02000E1C]}
STATUS_ONE = set()
ROTATIONS = [0x020280A0, 0x02028044, 0x02027FE8]


def converted(word):
    return ((word * 33) ^ 0x12345678) & 0xFFFFFFFF


def provided_matrix(address, word):
    return [(address ^ word ^ (index * 0x01010101)) & 0xFFFFFFFF for index in range(9)]


def provided_combine(left, right):
    return [(a + 3 * b + index + 1) & 0xFFFFFFFF for index, (a, b) in enumerate(zip(left, right))]


def run(row, body, ordinal, main):
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(int(row['address'], 0), body)
    bank = ordinal % 4
    advance = [0, 4, 0xFFFFFFFF, 16, 100, 1, 0x80000000, 8][ordinal]
    samples = [-1.25, -0.5, -1 / 8192, -0.0, 0.0, 1 / 8192, 0.5, 1.25]
    values = [[-32769, -32768, -1, 0, 32767, 32768, 65535, 65536][ordinal],
        [-65536, -32769, -32768, -1, 0, 32767, 32768, 65535][ordinal]]
    values.extend(samples[(ordinal + index) % 8] for index in range(6))
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
    target = bytearray((n * 23 + ordinal) & 255 for n in range(0xB8))
    target[9] = [0, 1, 255, 128, 2, 0, 127, 254][ordinal]
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
        raise ValueError('Qualified matrix imports collapsed')
    calls, writes, pcs = [], [], []
    returned, changed = False, False

    def put(address, data):
        vm.mem_write(address, data)
        writes.append(dict(provider=True, address=address, hex=data.hex()))

    def memory(uc, access, address, size, value, user):
        writes.append(dict(provider=False, address=address, size=size, value=value))

    def code(uc, address, size, user):
        nonlocal returned, changed
        pcs.append(address)
        if address == STOP:
            returned = True
            uc.emu_stop()
        elif address in imports:
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('ARM matrix provider entered in Thumb mode')
            symbol = imports[address]
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            call = dict(symbol=symbol, address=address, words=args)
            if address == 0x02000E1C:
                call['inputs'] = [list(struct.unpack('<9I', bytes(uc.mem_read(pointer, 36)))) for pointer in args[:2]]
            calls.append(call)
            result = 0x12345678
            flags = ((ordinal + len(calls)) & 15) << 28 | 0x10
            if symbol == '_ffix':
                result = int(floating(args[0])) & 0xFFFFFFFF
            elif symbol in ('_fadd', '_fsub', '_fmul'):
                left, right = floating(args[0]), floating(args[1])
                result = bits(left + right if symbol == '_fadd' else left - right if symbol == '_fsub' else left * right)
            elif symbol == '_fgr':
                flags = (0x20000000 if floating(args[0]) > floating(args[1]) else 0x40000000) | 0x10
            elif not symbol.startswith('_'):
                if address == 0x0221220C:
                    result = TARGET
                elif address == 0x02028158:
                    result = converted(args[0])
                elif address == 0x02000CE8:
                    put(args[0], struct.pack('<9I', *range(0x101, 0x10A)))
                elif address in ROTATIONS:
                    put(args[0], struct.pack('<9I', *provided_matrix(address, args[1])))
                elif address == 0x02000E1C:
                    put(args[2], struct.pack('<9I', *provided_combine(*call['inputs'])))
                else:
                    raise ValueError('Unsupported opaque matrix boundary')
                if ordinal % 2 and not changed:
                    put(CONTEXT + 3, bytes([(bank + 1) % 4]))
                    put(INSTRUCTION + 4, struct.pack('<I', advance ^ 0x100))
                    changed = True
            else:
                raise ValueError('Unsupported matrix compiler helper')
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
        raise ValueError('Matrix caller failed actual return within both bounds')
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Matrix caller callee-saved register or SP changed')
    failures = []
    game = [call for call in calls if not call['symbol'].startswith('_')]
    if [call['address'] for call in game] != GAME_CALLS['02051510']:
        failures.append('Independent lookup/conversion/four-buffer/two-combine order')
    narrowed = [(((int(value) + 32768) % 65536) - 32768) & 0xFFFFFFFF for value in values[:2]]
    if game[0]['words'][:2] != narrowed:
        failures.append('Independent signed-halfword lookup words')
    words = [fixed(value) & 0xFFFFFFFF for value in values[2:5]]
    converted_words = [converted(word) for word in words]
    if [call['words'][0] for call in game[1:4]] != words:
        failures.append('Independent ordered signed fixed conversions')
    a, b, c, d = [call['words'][0] for call in game[4:8]]
    if [b - a, c - a, d - a] != [36, 72, 108] or not SP - 0xA0 <= a < d + 36 <= SP:
        failures.append('Independent four complete nonoverlapping36-byte stack regions')
    if [call['words'][1] for call in game[5:8]] != [converted_words[2], converted_words[1], converted_words[0]]:
        failures.append('Independent retained conversion words reloaded in measured order')
    buffers = [provided_matrix(address, value) for address, value in zip(ROTATIONS,
        [converted_words[2], converted_words[1], converted_words[0]])]
    combined = provided_combine(buffers[1], buffers[0])
    final = provided_combine(buffers[2], combined)
    if game[8]['words'][:3] != [c, b, a] or game[8]['inputs'] != [buffers[1], buffers[0]]:
        failures.append('Independent first combine ordered input/output buffers')
    if game[9]['words'][:3] != [d, a, TARGET + 0x94] or game[9]['inputs'] != [buffers[2], combined]:
        failures.append('Independent second combine forwarding and record output offset')
    expected_target = bytearray(target)
    expected_target[9] = 0
    struct.pack_into('<3I', expected_target, 0x88, *converted_words)
    struct.pack_into('<9I', expected_target, 0x94, *final)
    if bytes(vm.mem_read(TARGET, len(target))) != expected_target:
        failures.append('Independent complete record, three retained words, clear flag and supplied36-byte final output')
    flags_written = [item['value'] for item in writes if not item['provider'] and item['address'] == TARGET + 9]
    if flags_written != [1, 1, 1, 0]:
        failures.append('Independent ordered three flag stores and final clear')
    expected = bytearray(context)
    final_bank = (bank + 1) % 4 if changed else bank
    final_advance = advance ^ 0x100 if changed else advance
    expected[3] = final_bank
    struct.pack_into('<I', expected, 0x470 + final_bank * 0x10C, (positions[final_bank] + final_advance) & 0xFFFFFFFF)
    expected[0x477 + final_bank * 0x10C] = 0
    if bytes(vm.mem_read(CONTEXT, len(context))) != expected:
        failures.append('Independent complete context, advancing and status')
    expected_instruction = bytearray(instruction)
    struct.pack_into('<I', expected_instruction, 4, final_advance)
    if bytes(vm.mem_read(INSTRUCTION, len(instruction))) != expected_instruction:
        failures.append('Independent supplied instruction mutation')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
        ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True,
        nativeCalleeBodiesExecuted=0, calleeOrMatrixMathSourceCredit=0,
        instructionLimit=5000, wallClockLimitMicroseconds=2000000)
