import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261104_main_nextcmd_fixture import bits, floating, signed
from wave20261104_main_nextcmd_cmp_abi import HELPERS, fixed_body_reference

CONTEXT, INSTRUCTION, SP, STOP = 0x02400000, 0x02410000, 0x027F0000, 0x027E0000
FAMILIES = {
    '020528fc': (0x02062AA0, 0x02062A50, 0x0207C2B8, 0x0207C18C),
    '02052a2c': (0x02062AD0, 0x02062A88, 0x0207C2B8, 0x0207C18C),
    '02052b5c': (0x02062AA0, 0x02062A50, 0x0207C3D8, 0x0207C1B8),
    '02052c8c': (0x02062AD0, 0x02062A88, 0x0207C3D8, 0x0207C1B8)}
GAME_CALLS = FAMILIES
STATUS_ONE = set()
RATIOS = [(0, 1), (1, 10), (13421772, 67108864), (13421773, 67108864),
    (13421774, 67108864), (1, 2), (1, 1), (2, 1)]


def run(row, body, ordinal, main):
    name = format(int(row['address'], 0), '08x')
    count_function, getter, denominator_function, numerator_function = FAMILIES[name]
    count = [-1, 0, 1, 2, 3, 3, 2, 3][ordinal]
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(int(row['address'], 0), body)
    bank = ordinal % 4
    advance = [0, 4, 0xFFFFFFFF, 16, 100, 1, 0x80000000, 8][ordinal]
    context = bytearray((n * 17 + ordinal) & 255 for n in range(0x470 + 4 * 0x10C))
    context[3] = bank
    positions = [0xFFFFFFFD, 0, 0x12345678, 0x80000000]
    for index, position in enumerate(positions):
        struct.pack_into('<I', context, 0x470 + index * 0x10C, position)
        context[0x477 + index * 0x10C] = 0xA5
    instruction = bytearray((n * 31 + ordinal) & 255 for n in range(128))
    struct.pack_into('<II', instruction, 0, 0x12345678, advance)
    records = []
    for index in range(3):
        address = 0x02420000 + index * 0x100
        data = bytearray((n * 23 + ordinal + index) & 255 for n in range(0x90))
        struct.pack_into('<h', data, 0x18, [-32768, -1, 32767][index])
        data[0x1A] = [0, 128, 255][index]
        vm.mem_write(address, bytes(data))
        records.append((address, bytes(data)))
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
        raise ValueError('Qualified comparison imports collapsed')
    calls, writes, pcs, helper_returns = [], [], [], []
    returned, changed, active = False, False, None
    current_index = None

    def put(address, data):
        vm.mem_write(address, data)
        writes.append(dict(provider=True, address=address, hex=data.hex()))

    def memory(uc, access, address, size, value, user):
        writes.append(dict(provider=False, address=address, size=size, value=value))

    def code(uc, address, size, user):
        nonlocal returned, changed, active, current_index
        if active is not None:
            if address == active['lr']:
                registers = [uc.reg_read(register) for register in C.REGISTERS]
                flags = uc.reg_read(R.UC_ARM_REG_CPSR)
                reference, expected_flags = fixed_body_reference(active['helper'], *active['initial'][:2], active['initial'], active['cpsr'])
                if registers != reference or flags != expected_flags or len(writes) != active['writeStart']:
                    raise ValueError('Actual original comparison helper full GPR/CPSR/ordered-write ABI differs inside caller')
                helper_returns.append(dict(helper=active['helper'], initialRegisters=active['initial'],
                    initialCpsr=active['cpsr'], registers=registers, cpsr=flags, orderedMemoryWrites=[], actualReturn=True))
                active = None
            elif not HELPERS[active['helper']][0] <= address < sum(HELPERS[active['helper']]):
                raise ValueError('Actual comparison helper escaped its configured full body')
        pcs.append(address)
        if address == STOP:
            returned = True
            uc.emu_stop()
        elif address in imports:
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('Qualified ARM import entered in Thumb mode')
            symbol = imports[address]
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            call = dict(symbol=symbol, address=address, words=args)
            if symbol in HELPERS:
                calls.append(call)
                active = dict(helper=symbol, initial=[uc.reg_read(register) for register in C.REGISTERS],
                    cpsr=uc.reg_read(R.UC_ARM_REG_CPSR), lr=uc.reg_read(R.UC_ARM_REG_LR), writeStart=len(writes))
                return
            if address in (denominator_function, numerator_function):
                call['temporary'] = bytes(uc.mem_read(args[1], 64)).hex()
            calls.append(call)
            result = 0x12345678
            flags = ((ordinal + len(calls)) & 15) << 28 | 0x10
            if symbol == '_fflt':
                result = bits(float(signed(args[0])))
            elif symbol == '_fdiv':
                result = bits(floating(args[0]) / floating(args[1]))
            elif not symbol.startswith('_'):
                if address == count_function:
                    result = count & 0xFFFFFFFF
                elif address == getter:
                    current_index = args[0]
                    if not 0 <= current_index < count <= 3:
                        raise ValueError('Supplied dense-record getter precondition escaped')
                    result = records[current_index][0]
                elif address == 0x0207B460:
                    put(args[3], bytes((ordinal * 17 + current_index * 13 + n) & 255 for n in range(64)))
                elif address in (denominator_function, numerator_function):
                    numerator, denominator = RATIOS[(ordinal + current_index) % len(RATIOS)]
                    result = denominator if address == denominator_function else numerator
                if ordinal % 2 and not changed:
                    put(CONTEXT + 3, bytes([(bank + 1) % 4]))
                    put(INSTRUCTION + 4, struct.pack('<I', advance ^ 0x100))
                    changed = True
            else:
                raise ValueError('Unexpected unsupported supplied compiler helper')
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, register in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xCAFE0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, result)
            uc.reg_write(R.UC_ARM_REG_CPSR, flags)
            uc.reg_write(R.UC_ARM_REG_PC, lr)

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(int(row['address'], 0), STOP + 4, timeout=2000000, count=5000)
    if not returned or active is not None:
        raise ValueError(('Actual comparison caller/helper return missing within bounds', name, ordinal))
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Caller callee-saved register or SP changed')
    failures = []
    game = [call for call in calls if not call['symbol'].startswith('_')]
    expected_calls = [count_function] + [address for unused in range(max(count, 0))
        for address in (getter, 0x0207B460, denominator_function, numerator_function)]
    if [call['address'] for call in game] != expected_calls:
        failures.append('Independent count/record/buffer/denominator/numerator provider order')
    expected = bytearray(context)
    for index in range(3):
        struct.pack_into('<I', expected, 0x10 + index * 4, bits(-1.0))
    for index in range(max(count, 0)):
        get, prepare, den, num = game[1 + index * 4:5 + index * 4]
        record_address, record = records[index]
        if get['words'][0] != index or prepare['words'][:3] != [struct.unpack_from('<h', record, 0x18)[0] & 0xFFFFFFFF, record[0x1A], record_address + 0x7A]:
            failures.append('Independent signed-halfword/byte fields and partial-record interior pointer')
        expected_temporary = bytes((ordinal * 17 + index * 13 + n) & 255 for n in range(64)).hex()
        for call in (den, num):
            if call['words'][:2] != [record_address + 0x20, prepare['words'][3]] or call['temporary'] != expected_temporary:
                failures.append('Independent complete supplied64-byte buffer and paired record queries')
        numerator, denominator = RATIOS[(ordinal + index) % len(RATIOS)]
        ratio = floating(bits(floating(bits(float(numerator))) / floating(bits(float(denominator)))))
        result = 1.0 if ratio <= floating(0x3E4CCCCD) else 3.0 if ratio < 1.0 else 2.0 if ratio == 1.0 else 0.0
        struct.pack_into('<I', expected, 0x10 + index * 4, bits(result))
    expected_helper_names = []
    for index in range(max(count, 0)):
        numerator, denominator = RATIOS[(ordinal + index) % len(RATIOS)]
        ratio = floating(bits(floating(bits(float(numerator))) / floating(bits(float(denominator)))))
        expected_helper_names.append('_fleq')
        if ratio > floating(0x3E4CCCCD):
            expected_helper_names.append('_fls')
            if ratio >= 1.0:
                expected_helper_names.append('_feq')
    if [item['helper'] for item in helper_returns] != expected_helper_names:
        failures.append('Independent executed ordered comparison-helper paths at measured0.2,one and zero thresholds')
    if any(bytes(vm.mem_read(address, len(data))) != data for address, data in records):
        failures.append('Independent complete read-only source records preserved')
    final_bank = (bank + 1) % 4 if changed else bank
    final_advance = advance ^ 0x100 if changed else advance
    expected[3] = final_bank
    struct.pack_into('<I', expected, 0x470 + final_bank * 0x10C, (positions[final_bank] + final_advance) & 0xFFFFFFFF)
    expected[0x477 + final_bank * 0x10C] = 0
    if bytes(vm.mem_read(CONTEXT, len(context))) != expected:
        failures.append('Independent complete context, negative/zero count, four result codes, advancing and status')
    expected_instruction = bytearray(instruction)
    struct.pack_into('<I', expected_instruction, 4, final_advance)
    if bytes(vm.mem_read(INSTRUCTION, len(instruction))) != expected_instruction:
        failures.append('Independent supplied instruction mutation')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
        ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True,
        actualOriginalComparisonHelperReturns=helper_returns, nativeComparisonHelperBodiesExecuted=len(helper_returns),
        opaqueNativeGameOrConversionBodiesExecuted=0, comparisonHelperOrCalleeSourceCredit=0,
        instructionLimit=5000, wallClockLimitMicroseconds=2000000)
