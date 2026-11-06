import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261104_main_tail_proof import bits, floating, signed, fixed, CONTEXT, INSTRUCTION, SP, STOP, REGS

SPECS = {
    '020577cc': dict(member=0, setter=False),
    '0205785c': dict(member=0, setter=True),
    '02057914': dict(member=1, setter=False),
    '020579a4': dict(member=1, setter=True),
    '02057e4c': dict(calls=[0x02057D1C, 0x0222212C, 0x020406FC]),
    '0205857c': dict(calls=[0x022092C8])}

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
    values = [[-65537, -32769, -32768, -1, 0, 32767, 32768, 65535][ordinal],
              [-65536, -32768, -1, 0, 1, 32768, 65535, 65536][ordinal],
              [-1.25, -0.5, -1 / 8192, 0, 1 / 8192, 0.5, 1.25, 100][ordinal], 1, 2, 3, 4, 5]
    if name == '02057e4c':
        values[2] = [-65537, -32769, -1, 0, 1, 32767, 32768, 65535][ordinal]
    elif name == '0205857c':
        values[0] = [-1, 255, 511, -257, 0, 1, 128, 127][ordinal]
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
    region_base = 0x02430000
    region = bytearray((index * 13 + ordinal) & 255 for index in range(0x5000))
    struct.pack_into('<I', region, 0x60, region_base + 0x1000)
    struct.pack_into('<I', region, 0x6c, region_base + 0x2000)
    struct.pack_into('<I', region, 0x1008, region_base + 0x3000)
    struct.pack_into('<I', region, 0x2008, region_base + 0x4000)
    lengths = [[0, 1, 2, 17, 255, 4095, 32768, 65535][ordinal], [65535, 32768, 4095, 255, 17, 2, 1, 0][ordinal]]
    struct.pack_into('<H', region, 0x3004, lengths[0])
    struct.pack_into('<H', region, 0x4004, lengths[1])
    vm.mem_write(region_base, bytes(region))
    encoded = [0x10, 0x10, 0x32, 0x30, 0x21, 0x43, 0x12, 0x34][ordinal]
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
                if location == 0x0221220C:
                    result = region_base
                elif location == 0x0203D0B4:
                    result = encoded
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
    expected_calls = [0x0221220C] if 'member' in spec else list(spec['calls'])
    mode = integer[0] & 255
    mode = mode - 256 if mode & 128 else mode
    if name == '0205857c' and mode == -1:
        expected_calls.insert(0, 0x0203D0B4)
    if [call['address'] for call in game] != expected_calls:
        failures.append('Independent pointer lookup, sentinel dispatch and constructor/provider sequence')
    def narrow16(value):
        low = value & 65535
        return (low - 65536 if low & 32768 else low) & 0xFFFFFFFF
    if 'member' in spec and game[0]['words'][:2] != [narrow16(integer[0]), narrow16(integer[1])]:
        failures.append('Independent signed-short object lookup arguments')
    if name == '02057e4c':
        if game[0]['words'] != [narrow16(integer[0]), integer[1], narrow16(integer[2]), CONTEXT + 0x1c]:
            failures.append('Independent constructor arguments and inline float-array address')
        if game[1]['words'][0] != supplied & 0xFFFFFFFF or game[2]['words'][0] != 1:
            failures.append('Independent returned-word forwarding and constant final argument')
    if name == '0205857c':
        if mode == -1:
            if game[0]['words'][0] != 63:
                failures.append('Independent sentinel request constant')
            mode = 0 if bank == encoded & 15 else int(bank == (encoded >> 4) & 15)
        if game[-1]['words'][0] != mode & 0xFFFFFFFF:
            failures.append('Independent signed-byte and pre-callback bank/nibble selection')
    expected_region = bytearray(region)
    if spec.get('setter'):
        struct.pack_into('<I', expected_region, 0x1000 * (spec['member'] + 1), fixed(values[2]))
    if bytes(vm.mem_read(region_base, len(region))) != expected_region:
        failures.append('Independent complete object, both playbacks and descriptors; selected member writes only')
    expected = bytearray(context)
    final_bank = (bank + 1) % 4 if changed else bank
    final_advance = advance ^ 0x100 if changed else advance
    expected[3] = final_bank
    do_advance = name not in CONDITIONAL or ordinal % 2 != 0
    if do_advance:
        struct.pack_into('<I', expected, 0x470 + final_bank * 0x10C, (positions[final_bank] + final_advance) & 0xFFFFFFFF)
    expected[0x477 + final_bank * 0x10C] = int(name in STATUS_ONE)
    outputs = {}
    if 'member' in spec and not spec['setter']:
        value = (lengths[spec['member']] << 12) - 1
        outputs[0] = floating(bits(float(value))) / 4096.0
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

