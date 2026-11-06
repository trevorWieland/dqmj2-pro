import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261104_main_tail_proof import bits, floating, signed, fixed, CONTEXT, INSTRUCTION, SP, STOP, REGS

SPECS = {
    '0205392c': dict(variant=0, helper=0x020535B4, pointer=True),
    '020539a4': dict(variant=1, helper=0x020535B4, pointer=True),
    '02053a1c': dict(variant=0, helper=0x02053748, pointer=True),
    '02053a94': dict(variant=1, helper=0x02053748, pointer=True),
    '02053b0c': dict(calls=[0x0205C338], args='times30'),
    '02053b64': dict(calls=[0x0205C338], args='u32'),
    '02053bb0': dict(calls=[0x02063E80], slots='clear'),
    '02053c08': dict(calls=[0x02063E80], slots='read'),
    '02053c68': dict(calls=[0x0205BFD4], output=True),
    '02053d98': dict(calls=[0x0204077C, 0x0204073C], args='second-zero'),
    '02053de4': dict(calls=[0x0204073C], args='one'),
    '02053ec0': dict(calls=[0x0205BD60] * 3, reset=True),
    '02053f20': dict(calls=[0x020653D0], output=True),
    '02053f6c': dict(calls=[0x02063D30], output=True),
    '02053fb8': dict(calls=[0x02063CF4], output=True)}

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
    wanted = [0, 1, -1, 32767, -32768, 65535, 128, -129][ordinal]
    if 'variant' not in spec:
        wanted = [0, 1, 255, 256, 65535, 16777216, 4294967040, 128][ordinal]
    values = [wanted, -1.25, 127, 255, 100, 200, 300, 400]
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
    region = bytearray((index * 13 + ordinal) & 255 for index in range(100 * 0x84))
    for index in range(100):
        offset = index * 0x84
        field14 = [0, 1, 0x80000000, 0xFFFFFFFF][(index + ordinal) % 4]
        field18 = ((wanted + index % 3 + 32768) & 65535) - 32768
        struct.pack_into('<Ih', region, offset + 0x14, field14, field18)
        region[offset + 0x1a] = (42 + index * 19 + ordinal * 31) & 255
        region[offset + 0x1b] = (128 + index * 29 + ordinal * 47) & 255
        region[offset + 0x1e] = (255 - index * 31 - ordinal * 17) & 255
    vm.mem_write(region_base, bytes(region))
    gate = [0, 1, 0, 0x80000000, 0, 0xFFFFFFFF, 0, 255][ordinal]
    record_offset = spec.get('variant', 0) * 0x84
    slots_base, reset_base = 0x02434000, 0x02435000
    slots = bytearray((index * 7 + ordinal) & 255 for index in range(0x424))
    for index in range(256):
        struct.pack_into('<I', slots, 0x24 + index * 4, (0x80000000 ^ (index * 0x01010101 + ordinal)) & 0xFFFFFFFF)
    reset = bytearray((index * 19 + ordinal) & 255 for index in range(64))
    vm.mem_write(slots_base, bytes(slots))
    vm.mem_write(reset_base, bytes(reset))
    reset_counter = 0
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items()}

    def put(location, data):
        vm.mem_write(location, data)
        writes.append(dict(provider=True, address=location, hex=data.hex()))

    def memory(uc, access, location, size, value, user):
        writes.append(dict(provider=False, address=location, size=size, value=value))

    def code(uc, location, size, user):
        nonlocal returned, changed, reset_counter
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
                if location == 0x02062B00:
                    result = region_base
                elif location in (0x02062A68, 0x02062A78):
                    result = gate
                elif location in (0x02062A50, 0x02062A88):
                    result = region_base + record_offset
                elif location == 0x02063E80:
                    result = slots_base
                elif location == 0x0205BD60:
                    result = reset_base + reset_counter * 16
                    reset_counter += 1
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
    if 'variant' in spec:
        expected_calls = [0x02062A68 if spec['variant'] == 0 else 0x02062A78]
        if gate:
            expected_calls.append(0x02062A50 if spec['variant'] == 0 else 0x02062A88)
            if spec.get('helper'):
                expected_calls.append(spec['helper'])
    else:
        expected_calls = spec['calls']
    if [call['address'] for call in game] != expected_calls:
        failures.append('Independent gate/lookup/conversion and complete provider sequence')
    if 'variant' in spec:
        if game[0]['words'][0] != integer[0] or gate and game[1]['words'][0] != integer[0]:
            failures.append('Independent gate and lookup integer index')
        if gate and spec.get('helper'):
            field18 = struct.unpack_from('<h', region, record_offset + 0x18)[0] & 0xFFFFFFFF
            args = [region_base + record_offset] if spec.get('pointer') else [field18, region[record_offset + 0x1a]] if spec['helper'] == 0x02044DC4 else [field18]
            if game[-1]['words'][:len(args)] != args:
                failures.append('Independent signed record ID and unsigned byte forwarding')
    elif spec.get('args'):
        args = spec['args']
        if args in ('times30', 'u32') and game[0]['words'][0] != (integer[0] * (30 if args == 'times30' else 1)) & 0xFFFFFFFF:
            failures.append('Independent unsigned conversion and wrapped multiply')
        if args == 'one' and game[0]['words'][0] != 1 or args == 'second-zero' and game[1]['words'][0] != 0:
            failures.append('Independent fixed dispatch argument')
    if bytes(vm.mem_read(region_base, len(region))) != region:
        failures.append('Independent pointed record region remains read-only')
    expected_slots, expected_reset = bytearray(slots), bytearray(reset)
    if spec.get('slots') == 'clear':
        struct.pack_into('<I', expected_slots, 0x24 + (integer[0] & 255) * 4, 0)
    if spec.get('reset'):
        for index in range(3):
            struct.pack_into('<H', expected_reset, index * 16 + index * 2, 65535)
    if bytes(vm.mem_read(slots_base, len(slots))) != expected_slots or bytes(vm.mem_read(reset_base, len(reset))) != expected_reset:
        failures.append('Independent complete indexed word region and per-provider signed-halfword writes')
    expected = bytearray(context)
    final_bank = (bank + 1) % 4 if changed else bank
    final_advance = advance ^ 0x100 if changed else advance
    expected[3] = final_bank
    do_advance = name not in CONDITIONAL or ordinal % 2 != 0
    if do_advance:
        struct.pack_into('<I', expected, 0x470 + final_bank * 0x10C, (positions[final_bank] + final_advance) & 0xFFFFFFFF)
    expected[0x477 + final_bank * 0x10C] = int(name in STATUS_ONE)
    outputs = {}
    if 'variant' in spec:
        outputs[0] = float(supplied if gate else -1)
    elif spec.get('output'):
        outputs[0] = float(supplied & 0xFFFFFFFF)
    elif spec.get('slots') == 'read':
        outputs[0] = float(struct.unpack_from('<I', slots, 0x24 + (integer[0] & 255) * 4)[0])
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

