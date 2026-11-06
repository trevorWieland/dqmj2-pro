import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R
import wave20261104_main_tail_proof as B

SPECS = {'020540f4': {}, '0205443c': {}, '020558ac': {}}


def words(data):
    return list(struct.unpack('<' + 'I' * (len(data) // 4), data))


def run(row, body, ordinal, main, overlay):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(0x021D7240, overlay)
    vm.mem_write(address, body)
    bank = ordinal % 4
    advance = [0, 4, 0xFFFFFFFF, 16, 100, 1, 0x80000000, 8][ordinal]
    value = [-1.25, -0.5, -1 / 8192, 0, 1 / 8192, 0.5, 1.25, 100][ordinal]
    if name == '0205443c':
        value = [0, 1, -1, 0, 2, 0, 1, -1][ordinal]
    values = [B.floating(B.bits(value)), 1.5, -129, 255, 100, 200, 300, 400]
    context = bytearray((index * 17 + ordinal) & 255 for index in range(0x470 + 4 * 0x10C))
    context[3] = bank
    struct.pack_into('<8I', context, 16, *[B.bits(v) for v in values])
    positions = [0xFFFFFFFD, 0, 0x12345678, 0x80000000]
    for index, position in enumerate(positions):
        struct.pack_into('<I', context, 0x470 + index * 0x10C, position)
        context[0x477 + index * 0x10C] = 0xA5
    instruction = bytearray((index * 31 + ordinal) & 255 for index in range(128))
    struct.pack_into('<II', instruction, 0, 0x12345678, advance)
    vm.mem_write(B.CONTEXT, bytes(context))
    vm.mem_write(B.INSTRUCTION, bytes(instruction))
    base = 0x02440000
    region = bytearray((index * 13 + ordinal) & 255 for index in range(0x6000))
    coordinates = [[10000 + ordinal, -20000, 30000], [4000, 5000 + ordinal, -6000],
                   [11000 + ordinal, -22000, 33000], [4400, 5500 + ordinal, -6600],
                   [4096 * (ordinal + 1), -2048 * (ordinal + 1), 123 + ordinal]]
    for index, vector in enumerate(coordinates):
        struct.pack_into('<iii', region, (index + 1) * 0x1000, *vector)
    vm.mem_write(base, bytes(region))
    initial = [0x11220000 + index * 0x100 + ordinal for index in range(15)]
    initial[:4] = [B.CONTEXT, B.INSTRUCTION, 0xDEADBEEF, 0xA5A55A5A]
    initial[-2:] = [B.SP, B.STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal << 28 | 0x10)
    for register, word in zip(C.REGISTERS, initial):
        vm.reg_write(register, word)
    returned, changed, stepped = False, False, False
    calls, writes, pcs = [], [], []
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items()}
    length = [0, 1, -1, 4096, -4096, 4097, -0x80000000, 0x7FFFFFFF][ordinal]
    fallback = [8193, 7, 8191, 3, 16385, 5, 32769, 1][ordinal]
    intersect = [0, 1, 1, 1, 0, 1, 1, 0][ordinal]
    result_before = [123 + ordinal, -456 - ordinal, 789 + 2 * ordinal]
    result_after = [result_before[0] + 10, result_before[1] - 20, result_before[2] + 30]
    normalized = [4096, -2048, 1024]

    def put(location, data):
        vm.mem_write(location, data)
        writes.append(dict(provider=True, address=location, hex=data.hex()))

    def memory(uc, access, location, size, word, user):
        writes.append(dict(provider=False, address=location, size=size, value=word))

    def code(uc, location, size, user):
        nonlocal returned, changed, stepped
        pcs.append(location)
        if location == B.STOP:
            returned = True
            uc.emu_stop()
        elif location in imports:
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('Qualified ARM provider entered as Thumb')
            symbol = imports[location]
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            call = dict(symbol=symbol, address=location, words=args, stack=bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP), 16)).hex())
            calls.append(call)
            result = 0x13572468
            flags = ((ordinal + len(calls)) & 15) << 28 | 0x10
            if symbol in ('_ffix', '_ffixu'):
                result = int(B.floating(args[0])) & 0xFFFFFFFF
            elif symbol in ('_fflt', '_ffltu'):
                result = B.bits(float(B.signed(args[0]) if symbol == '_fflt' else args[0]))
            elif symbol in ('_fadd', '_fsub', '_fmul', '_fdiv'):
                left, right = B.floating(args[0]), B.floating(args[1])
                result = B.bits(left + right if symbol == '_fadd' else left - right if symbol == '_fsub' else left * right if symbol == '_fmul' else left / right)
            elif symbol == '_fgr':
                flags = (0x20000000 if B.floating(args[0]) > B.floating(args[1]) else 0x40000000) | 0x10
            else:
                if ordinal % 2 and not changed:
                    put(B.CONTEXT + 3, bytes([(bank + 1) % 4]))
                    put(B.INSTRUCTION + 4, struct.pack('<I', advance ^ 0x100))
                    changed = True
                if location == 0x021E07B8:
                    result = base + 0x5000
                elif location == 0x021E07AC:
                    result = base
                elif location == 0x021DA5E4:
                    put(args[2], struct.pack('<iii', *result_before))
                    result = intersect
                elif location == 0x021DBBB8:
                    put(args[1], struct.pack('<iii', *result_after))
                    put(args[0], struct.pack('<I', 0xABCD0000 + ordinal))
                elif location == 0x021E71E0:
                    result = length & 0xFFFFFFFF
                elif location in (0x0202859C, 0x020285C8):
                    result = base + (0x3000 if stepped else 0x1000) + (0x1000 if location == 0x020285C8 else 0)
                elif location == 0x0200285C:
                    result = fallback
                elif location == 0x020284F4:
                    stepped = True
                elif location == 0x02002618:
                    call['inputVector'] = words(bytes(uc.mem_read(args[0], 12)))
                    put(args[1], struct.pack('<iii', *normalized))
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, register in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xCAFE0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, result)
            uc.reg_write(R.UC_ARM_REG_CPSR, flags)
            uc.reg_write(R.UC_ARM_REG_PC, lr)

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, B.STOP + 4, count=5000)
    if not returned:
        raise ValueError(('No actual caller return', name, ordinal))
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != B.SP:
        raise ValueError('Callee-saved/SP differs')
    failures = []
    game = [call for call in calls if not call['symbol'].startswith('_')]
    expected_region = bytearray(region)
    if name == '020540f4':
        expected_calls = [0x021E07B8, 0x021E8DE8]
        if len(game) != 2 or game[0]['words'][0] != 0 or game[1]['words'] != [int(values[0]) & 0xFFFFFFFF] + [v & 0xFFFFFFFF for v in coordinates[4]]:
            failures.append('Independent vector provider constant and three raw signed-word arguments')
    elif name == '0205443c':
        apply = bool(intersect and int(values[0]))
        expected_calls = [0x021E07B8, 0x021E07AC, 0x021DA5E4] + ([0x021DBBB8] if apply else [])
        intersection = next((call for call in game if call['address'] == 0x021DA5E4), None)
        if not game or game[0]['words'][0] != 0 or intersection is None:
            failures.append('Intersection must run before testing the caller apply flag')
        elif intersection['words'][:2] != [base + 0x5000, base + 0x210] or intersection['words'][3] != 1 or not B.SP - 256 <= intersection['words'][2] <= B.SP - 12:
            failures.append('Independent matrix pointer, caller vector output and constant intersection flag')
        if apply:
            transform = next((call for call in game if call['address'] == 0x021DBBB8), None)
            if transform is None or intersection is None or transform['words'][:2] != [base + 0x210, intersection['words'][2]]:
                failures.append('Independent matrix and same post-intersection output pointer')
            struct.pack_into('<iii', expected_region, 0x70, *result_after)
            struct.pack_into('<I', expected_region, 0x210, 0xABCD0000 + ordinal)
    else:
        expected_calls = [0x021E71E0] + ([0x0202859C, 0x020285C8, 0x0200285C] if length <= 0 else []) + [0x020284F4, 0x0202859C, 0x020285C8, 0x02002618]
        for call in game:
            if call['address'] in (0x0202859C, 0x020285C8) and call['words'][:2] != [0, 0]:
                failures.append('Independent two zero vector-provider arguments')
            elif call['address'] == 0x0200285C and call['words'][:2] != [base + 0x1000, base + 0x2000]:
                failures.append('Independent fallback distance pre-step vectors')
            elif call['address'] == 0x020284F4 and call['words'][:2] != [0, B.fixed(values[0])]:
                failures.append('Independent fixed step argument')
            elif call['address'] == 0x02002618:
                difference = [(left - right) & 0xFFFFFFFF for left, right in zip(coordinates[2], coordinates[3])]
                if call['words'][0] != call['words'][1] or call.get('inputVector') != difference or not B.SP - 256 <= call['words'][0] <= B.SP - 12:
                    failures.append('Independent in-place caller vector and post-step difference')
        used_length = fallback if length <= 0 else length
        result_vector = [(origin + ((used_length * component + 2048) // 4096)) & 0xFFFFFFFF for origin, component in zip(coordinates[3], normalized)]
        struct.pack_into('<III', expected_region, 0x3000, *result_vector)
    if [call['address'] for call in game] != expected_calls:
        failures.append('Independent full conditional provider sequence')
    if bytes(vm.mem_read(base, len(region))) != expected_region:
        failures.append('Independent complete scene/vector region, matrix effects, post-call reload and rounded64-bit products')
    expected = bytearray(context)
    final_bank, final_advance = ((bank + 1) % 4, advance ^ 0x100) if changed else (bank, advance)
    expected[3] = final_bank
    struct.pack_into('<I', expected, 0x470 + final_bank * 0x10C, (positions[final_bank] + final_advance) & 0xFFFFFFFF)
    expected[0x477 + final_bank * 0x10C] = 0
    if bytes(vm.mem_read(B.CONTEXT, len(context))) != expected:
        failures.append('Independent complete context, bank stride, advancement and status')
    expected_instruction = bytearray(instruction)
    struct.pack_into('<I', expected_instruction, 4, final_advance)
    if bytes(vm.mem_read(B.INSTRUCTION, len(instruction))) != expected_instruction:
        failures.append('Independent complete instruction forwarding/mutation model')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
