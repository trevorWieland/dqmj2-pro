import struct
from project import sha256
import match_runtime as C
import unicorn
from unicorn import arm_const as R

CONTEXT, INSTRUCTION, SP, STOP = 0x02400000, 0x02410000, 0x027F0000, 0x027E0000
GAME_CALLS = {
    '0205006c': [0x0205BD6C, 0x021E7940, 0x020404F0], '02050134': [0x02210B98],
    '02050244': [0x02040424], '02050290': [0x0205E73C], '020502dc': [0x021E7B9C],
    '02050330': [0x021E0BC4], '020503d0': [0x021E7940], '02050480': [0x0205C1E8],
    '020504cc': [0x021E7BB0], '02050534': [0x0205F35C], '02050590': [0x0205F4BC],
    '02050600': [0x0205F404], '02050660': [0x0205F6A0]}
STATUS_ONE = {'0205006c'}


def bits(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def floating(word):
    return struct.unpack('<f', struct.pack('<I', word))[0]


def signed(word):
    return word - 0x100000000 if word & 0x80000000 else word


def fixed(value):
    product = floating(bits(4096.0 * value))
    return int(floating(bits(0.5 + product if value > 0 else product - 0.5)))


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
    unsigned_supply = [0, 1, 127, 128, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, 0x01000001][ordinal]
    values = [[-129, -128, -1, 0, 47, 48, 127, 256][ordinal],
              [-128, -0.5, -1 / 8192, -0.0, 0.0, 1 / 8192, 128, 256][ordinal],
              [-129, -128, -1, 0, 127, 128, 255, 256][ordinal], 1.5, -1.5, 0, 1, 2]
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
        raise ValueError('Provider address cannot collapse distinct qualified imports')
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
                raise ValueError('Qualified ARM provider entered in Thumb mode')
            symbol = imports[location]
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            stack = bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP), 56))
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
                if location == 0x02040424:
                    result = unsigned_supply
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
        raise ValueError(('Caller did not actually return before instruction/time limits', name, ordinal))
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Callee-saved registers or SP changed')
    failures = []
    game = [call for call in calls if not call['symbol'].startswith('_')]
    integer = [int(value) for value in values]
    expected_calls = list(GAME_CALLS[name])
    if name == '02050134' and not 0 <= integer[0] < 48 or name == '020504cc' and integer[0] < 0:
        expected_calls = []
    if [call['address'] for call in game] != expected_calls:
        failures.append('Independent qualified provider call sequence and range guard')
    argument_words = {
        '02050290': integer[:1], '020502dc': integer[:1], '02050330': integer[:1],
        '020503d0': [max(integer[0], 0)], '020504cc': integer[:2],
        '02050534': [-1, integer[0]], '02050590': integer[:3], '02050600': integer[:2],
        '02050660': [integer[0], min(max(integer[1], 0), 127), integer[2]],
        '02050134': [integer[0], fixed(values[1])]}
    if game and name in argument_words:
        expected = [word & 0xFFFFFFFF for word in argument_words[name]]
        if game[0]['words'][:len(expected)] != expected:
            failures.append('Independent integer forwarding, clamp or fixed-point argument model')
    if name == '0205006c':
        narrow = ((integer[0] + 128) % 256) - 128
        short = ((integer[1] + 32768) % 65536) - 32768
        expected = [0, 0, 0, 0, 0, 0, short, 1, 0, 0, 0, narrow, 45, 1, 0, 0, 0, 0]
        actual = game[0]['words'] + list(struct.unpack('<14I', bytes.fromhex(game[0]['stack'])))
        if actual != [word & 0xFFFFFFFF for word in expected] or game[1]['words'][0] != 0 or game[2]['words'][0] != 27:
            failures.append('Independent eighteen physical argument words and follow-up constants')
    expected = bytearray(context)
    final_bank = (bank + 1) % 4 if changed else bank
    final_advance = advance ^ 0x100 if changed else advance
    expected[3] = final_bank
    struct.pack_into('<I', expected, 0x470 + final_bank * 0x10C, (positions[final_bank] + final_advance) & 0xFFFFFFFF)
    expected[0x477 + final_bank * 0x10C] = int(name in STATUS_ONE)
    output = None
    if name == '02050134':
        output = floating(bits(float(supplied if expected_calls else fixed(values[1])))) / 4096.0
    elif name == '02050244':
        output = float(unsigned_supply)
    elif name in ('020502dc', '02050480', '02050534'):
        output = float(supplied)
    if output is not None:
        struct.pack_into('<I', expected, 16, bits(output))
    if bytes(vm.mem_read(CONTEXT, len(context))) != expected:
        failures.append('Independent complete context, bank stride, arithmetic output, advancing and status model')
    expected_instruction = bytearray(instruction)
    struct.pack_into('<I', expected_instruction, 4, final_advance)
    if bytes(vm.mem_read(INSTRUCTION, len(instruction))) != expected_instruction:
        failures.append('Independent instruction forwarding and supplied mutation model')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
        ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True,
        nativeCalleeBodiesExecuted=0, instructionLimit=5000, wallClockLimitMicroseconds=2000000)
