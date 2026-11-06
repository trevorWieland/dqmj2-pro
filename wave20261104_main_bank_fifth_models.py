import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261104_main_tail_proof import bits, floating, signed, fixed, CONTEXT, INSTRUCTION, SP, STOP, REGS

SPECS = {
    '02055088': dict(calls=[0x021E6A70, 0x021E6BAC], extraSelector=True, snapshot=0, vectorOutput=True),
    '02055360': dict(calls=[0x021E6A40, 0x021E70B0], extraSelector=True, snapshot=0, vectorOutput=True),
    '020554e0': dict(calls=[0x021E6A70, 0x021E7108], extraSelector=True, snapshot=0, vectorOutput=True),
    '02055660': dict(calls=[0x021E6A40, 0x021E6C70], extraSelector=True, snapshot=0, vectorOutput=True, duration=True),
    '02055c90': dict(calls=[0x021F3E5C, 0x021F3E88], snapshot=1, vectorOutput=True, callerBuffer=True),
    '02055ff4': dict(calls=[0x021F3F1C], snapshot=1, scalarOutput=True),
    '0205624c': dict(calls=[0x021F4234], snapshot=1, scalarOutput=True)}

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
    first = [-1.25, -0.5, -1 / 8192, -0.0, 0, 1 / 8192, 0.5, 1.25][ordinal]
    vector = [first, [-129, -128, -1, 0, 127, 128, 255, 256][ordinal],
              [1.5, -1.5, 0.5, -0.5, 100, -100, 0, 1][ordinal]]
    values = vector + [[0, 1, -1, 127, 128, -129, 32767, -32768][ordinal], 100, 200, 300, 400]
    if spec['snapshot'] == 1:
        values = [[-1, 0, 1, -32768, 32767, 65535, 16777216, -129][ordinal]] + vector + [100, 200, 300, 400]
    values = [floating(bits(v)) for v in values]
    selector = [0, 1, 2, 0xFFFFFFFF, 7, 0, 0x80000000, 255][ordinal]
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
    if spec.get('extraSelector'):
        initial[2] = selector
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal << 28 | 0x10)
    for register, value in zip(REGS, initial):
        vm.reg_write(register, value)
    calls, writes, pcs = [], [], []
    returned, changed = False, False
    vector_base = 0x02436000
    coordinates = [(ordinal + 1) * 4096, -(ordinal + 1) * 2048, [0, 1, -1, 123, 4095, -4096, 0x7FFFFFFF, -0x80000000][ordinal]]
    vector_region = struct.pack('<iii', *coordinates)
    vm.mem_write(vector_base, vector_region)
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
                if location in (0x021E6A40, 0x021E6A70, 0x021F3E5C):
                    if ordinal % 2:
                        put(CONTEXT + 16, struct.pack('<3I', bits(9.25), bits(-7.5), bits(8.75)))
                    if location == 0x021F3E5C:
                        put(args[1], vector_region)
                    else:
                        result = vector_base
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
    if [call['address'] for call in game] != spec['calls']:
        failures.append('Independent complete vector getter/setter sequence')
    offset = spec['snapshot']
    originals = values[offset:offset + 3]
    wanted = [selector if spec.get('extraSelector') else integer[0]] + [fixed(value) for value in originals]
    if game[-1]['words'] != wanted:
        failures.append('Independent preserved pre-getter float snapshots and physical fixed arguments')
    if spec.get('extraSelector') and game[0]['words'][:2] != [selector, 0]:
        failures.append('Independent incomingR2 selector and constant vector-getter argument')
    if spec.get('callerBuffer'):
        if game[0]['words'][0] != integer[0] or not SP - 256 <= game[0]['words'][1] <= SP - 12 or game[0]['words'][1] % 4:
            failures.append('Independent object and aligned caller-owned vector output buffer')
    if spec.get('duration') and struct.unpack('<I', bytes.fromhex(game[-1]['stack'])[:4])[0] != integer[3]:
        failures.append('Independent fifth signed duration stack argument')
    if bytes(vm.mem_read(vector_base, 12)) != vector_region:
        failures.append('Independent read-only provider vector remains unchanged')
    expected = bytearray(context)
    final_bank = (bank + 1) % 4 if changed else bank
    final_advance = advance ^ 0x100 if changed else advance
    expected[3] = final_bank
    do_advance = name not in CONDITIONAL or ordinal % 2 != 0
    if do_advance:
        struct.pack_into('<I', expected, 0x470 + final_bank * 0x10C, (positions[final_bank] + final_advance) & 0xFFFFFFFF)
    expected[0x477 + final_bank * 0x10C] = int(name in STATUS_ONE)
    outputs = {index: floating(bits(float(value))) / 4096.0 for index, value in enumerate(coordinates)} if spec.get('vectorOutput') else {0: float(supplied)}
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

