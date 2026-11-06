import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261104_main_nextcmd_fixture import bits, floating, signed, fixed

CONTEXT, INSTRUCTION, SP, STOP = 0x02400000, 0x02410000, 0x027F0000, 0x027E0000
GAME_CALLS = {
    '020520c0': [0x0220A040], '02052190': [0x021E5C88], '020522c4': [0x021E5C88],
    '02052340': [0x021E5C88], '020523c4': [0x021E5C88], '02052420': [0x02028158, 0x021E5C88],
    '020524dc': [0x021E5C88], '02052564': [0x021E5EC0], '02052600': [0x021E5FFC],
    '02052840': [0x0203D294], '020528b4': [0x0206344C, 0x0206349C],
    '02052dbc': [0x020629E0, 0x02062AA0, 0x02062AD0, 0x02062AA0, 0x02062AD0],
    '02052e38': [], '02052ed8': [], '02052f78': [], '02053000': []}
STATUS_ONE = set()
CAPACITY = {'02052e38', '02052ed8'}
COUNTING = {'02052f78', '02053000'}


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
    unsigned_inputs = [0, 1, 255, 256, 257, 65535, 16777216, 128]
    signed_inputs = [-129, -128, -1, 0, 127, 128, 255, 256]
    samples = [-1.25, -0.5, -1 / 8192, -0.0, 0.0, 1 / 8192, 0.5, 1.25]
    values = [unsigned_inputs[ordinal]] + [samples[(ordinal + index) % 8] for index in range(7)]
    if name == '020520c0':
        values[0] = [-129, -128, -1, 0, 47, 48, 127, 256][ordinal]
        values[1] = unsigned_inputs[ordinal]
    if name == '02052190':
        values[4] = signed_inputs[ordinal]
    if name in ('020522c4', '02052340', '020524dc'):
        values[1] = signed_inputs[ordinal]
    if name in ('020522c4', '02052420'):
        values[2] = unsigned_inputs[ordinal]
    if name == '02052340':
        values[2] = signed_inputs[ordinal]
    if name == '020524dc':
        values[2], values[3] = signed_inputs[(ordinal + 1) % 8], unsigned_inputs[ordinal]
    if name == '02052600':
        values[0], values[3] = samples[ordinal], unsigned_inputs[ordinal]
    if name == '02052840':
        values[0] = signed_inputs[ordinal]
    if name in COUNTING:
        values[0] = [-32768, -1, 0, 127, 32767, 32768, 65535, 65536][ordinal]
    values = [floating(bits(value)) for value in values]
    integer = [int(value) for value in values]
    ids = [((integer[0] + int(index == 2) + 32768) % 65536) - 32768 for index in range(3)]
    records = []
    for pool in range(2):
        for index in range(3):
            address = 0x02420000 + pool * 0x1000 + index * 0x100
            data = bytearray((n * 23 + ordinal + pool) & 255 for n in range(32))
            struct.pack_into('<h', data, 0x18, ids[index])
            vm.mem_write(address, bytes(data))
            records.append((address, bytes(data)))
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
        raise ValueError('Qualified provider imports collapsed')
    calls, writes, pcs, occurrences = [], [], [], {}
    returned, changed = False, False
    world = [0, 1, 99, 100, 101, 102, 50, 103][ordinal]
    sizes = [(ordinal * 3 + index) % 4 for index in range(3)]

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
            call = dict(symbol=symbol, address=location, words=args)
            if location == 0x021E5C88:
                length = {0: 3, 1: 1, 2: 1, 3: 0, 5: 1, 6: 2}[args[1]]
                call['payload'] = list(struct.unpack('<' + 'I' * length, bytes(uc.mem_read(args[2], 4 * length)))) if length else []
            calls.append(call)
            occurrences[location] = occurrences.get(location, 0) + 1
            occurrence = occurrences[location]
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
                if location in (0x02062A50, 0x02062A88):
                    index = args[0]
                    if index >= 3:
                        raise ValueError('Getter escaped bounded three-record provider contract')
                    result = 0x02420000 + (location == 0x02062A88) * 0x1000 + index * 0x100 if ordinal & (1 << index) else 0
                elif location == 0x02044CDC:
                    prior = calls[-2]
                    result = sizes[prior['words'][0]]
                elif location == 0x020629E0:
                    result = world + (ordinal % 3 - 1 if occurrence > 1 else 0)
                elif location == 0x02062AA0:
                    result = (ordinal + occurrence) % 4
                elif location == 0x02062AD0:
                    result = (ordinal * 2 + occurrence) % 4
                if ordinal % 2 and not changed:
                    put(CONTEXT + 3, bytes([(bank + 1) % 4]))
                    put(INSTRUCTION + 4, struct.pack('<I', advance ^ 0x100))
                    changed = True
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, register in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xCAFE0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, result & 0xFFFFFFFF)
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
    expected_calls = list(GAME_CALLS[name])
    output = None
    if name == '020520c0' and not 0 <= integer[0] < 48 or name == '02052840' and integer[0] == 0:
        expected_calls = []
    if name in CAPACITY | COUNTING:
        getter = 0x02062A88 if name in ('02052ed8', '02053000') else 0x02062A50
        expected_calls = []
        value = 3 if name in CAPACITY else 0
        for index in range(3):
            expected_calls.append(getter)
            if ordinal & (1 << index):
                if name in CAPACITY:
                    expected_calls.append(0x02044CDC)
                    value -= sizes[index] + 1
                else:
                    value += ids[index] == integer[0]
        if name in CAPACITY:
            expected_calls.append(0x020629E0)
            if 100 - world < value:
                expected_calls.append(0x020629E0)
                value = 100 - world - (ordinal % 3 - 1)
            value = max(value, 0)
        output = float(value)
        getters = [call for call in game if call['address'] == getter]
        if [call['words'][0] for call in getters] != [0, 1, 2]:
            failures.append('Independent ordered record indices including nullable entries')
        for call in game:
            if call['address'] == 0x02044CDC:
                prior = game[game.index(call) - 1]
                if call['words'][0] != ids[prior['words'][0]] & 0xFFFFFFFF:
                    failures.append('Independent signed-halfword field forwarding')
    if [call['address'] for call in game] != expected_calls:
        failures.append('Independent provider order, range guards, nullable branches and count re-queries')
    args = {'020520c0': [integer[0], integer[1] & 255], '02052564': [integer[0] & 255, fixed(values[1])],
        '02052600': [fixed(value) for value in values[:3]] + [integer[3] & 255], '02052840': [abs(integer[0])]}
    if game and name in args and game[0]['words'][:len(args[name])] != [word & 0xFFFFFFFF for word in args[name]]:
        failures.append('Independent range, fixed scalar and magnitude forwarding')
    tags = {'02052190': (0, [fixed(value) for value in values[1:4]], integer[4]),
        '020522c4': (1, [integer[1]], integer[2]), '02052340': (2, [integer[1] * 30], integer[2]),
        '020523c4': (3, [], 0), '02052420': (5, [supplied], integer[2]),
        '020524dc': (6, integer[1:3], integer[3])}
    if name in tags:
        tag, payload, last = tags[name]
        call = game[-1]
        if call['words'][:2] != [integer[0] & 255, tag] or call['words'][3] != last & 255 or call['payload'] != [word & 0xFFFFFFFF for word in payload]:
            failures.append('Independent tagged payload length, initialized words, byte identity and flag')
        if tag == 3 and call['words'][2] != 0:
            failures.append('Independent null payload for tag three')
        if tag == 5 and game[0]['words'][0] != fixed(values[1]) & 0xFFFFFFFF:
            failures.append('Independent fixed input to supplied word conversion boundary')
    if name == '02052840':
        output = float((supplied if integer[0] > 0 else -supplied) if integer[0] else 0)
    elif name == '02052dbc':
        prior = world - (ordinal + 1) % 4 - (ordinal * 2 + 1) % 4
        output = float(100 - (ordinal + 2) % 4 - (ordinal * 2 + 2) % 4 - prior)
    if any(bytes(vm.mem_read(address, len(data))) != data for address, data in records):
        failures.append('Independent complete read-only pointed-record preservation')
    expected = bytearray(context)
    final_bank = (bank + 1) % 4 if changed else bank
    final_advance = advance ^ 0x100 if changed else advance
    expected[3] = final_bank
    struct.pack_into('<I', expected, 0x470 + final_bank * 0x10C, (positions[final_bank] + final_advance) & 0xFFFFFFFF)
    expected[0x477 + final_bank * 0x10C] = 0
    if output is not None:
        struct.pack_into('<I', expected, 16, bits(output))
    if bytes(vm.mem_read(CONTEXT, len(context))) != expected:
        failures.append('Independent complete context, result, advancing and status')
    expected_instruction = bytearray(instruction)
    struct.pack_into('<I', expected_instruction, 4, final_advance)
    if bytes(vm.mem_read(INSTRUCTION, len(instruction))) != expected_instruction:
        failures.append('Independent supplied instruction mutation')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
        ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True,
        nativeCalleeBodiesExecuted=0, instructionLimit=5000, wallClockLimitMicroseconds=2000000)
