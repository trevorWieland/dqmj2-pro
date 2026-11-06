import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261104_main_nextcmd_fixture import bits, floating, signed

CONTEXT, INSTRUCTION, SP, STOP = 0x02400000, 0x02410000, 0x027F0000, 0x027E0000
GAME_CALLS = {'020506e4': [], '02051bb4': [0x02062B0C, 0x02062B1C]}
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
    values = [[-1, 0, 127, 128, 255, -129, 32767, -32768][ordinal],
        [-129, -128, -1, 0, 127, 128, 255, 256][ordinal], 0, 1, 2, 3, 4, 5]
    getter = [0, 999998, 0, 999999, 1000000, 1000010, -1, 0x7FFFFFFF][ordinal]
    if name == '02051bb4':
        values[0] = [0, 1, -1, 127, -128, 12345, -12345, 16777216][ordinal]
    values = [floating(bits(value)) for value in values]
    integer = [int(value) for value in values]
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
            calls.append(dict(symbol=symbol, address=location, words=args))
            result = 0x12345678
            flags = ((ordinal + len(calls)) & 15) << 28 | 0x10
            if symbol == '_ffix':
                result = int(floating(args[0])) & 0xFFFFFFFF
            elif symbol == '_fflt':
                result = bits(float(signed(args[0])))
            else:
                if location == 0x0205F2D8:
                    result = (args[0] + ordinal) & 1
                elif location == 0x0205F45C:
                    result = (args[0] + (ordinal >> 1)) & 1
                elif location == 0x02062B0C:
                    result = getter & 0xFFFFFFFF
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
    expected_calls = list(GAME_CALLS[name])
    output = None
    if name == '020506e4':
        expected_calls = []
        value = min(max(integer[0], 0), 127)
        for index in range(16):
            expected_calls.append(0x0205F2D8)
            if (index + ordinal) & 1:
                expected_calls.append(0x0205E814)
        for index in range(4):
            expected_calls.append(0x0205F45C)
            if (index + (ordinal >> 1)) & 1:
                expected_calls.append(0x0205F7E0)
        for address, count in [(0x0205F2D8, 16), (0x0205F45C, 4)]:
            if [call['words'][0] for call in game if call['address'] == address] != list(range(count)):
                failures.append('Independent complete ordered sixteen/four query indices')
        last_index = None
        for call in game:
            if call['address'] in (0x0205F2D8, 0x0205F45C):
                last_index = call['words'][0]
            if call['address'] in (0x0205E814, 0x0205F7E0) and call['words'][0] != last_index:
                failures.append('Independent selected query index forwarded unchanged')
            if call['address'] in (0x0205E814, 0x0205F7E0) and call['words'][1:3] != [value, integer[1] & 0xFFFFFFFF]:
                failures.append('Independent signed clamp and retained third word across every query')
    else:
        wrapped = signed((getter + integer[0]) & 0xFFFFFFFF)
        value = min(max(wrapped, 0), 999999)
        output = float(value)
        if game[-1]['words'][0] != value:
            failures.append('Independent modular word sum, signed lower bound and exact upper bound forwarded to setter')
    if [call['address'] for call in game] != expected_calls:
        failures.append('Independent conditional query/forwarding sequence or ordered getter/setter')
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
