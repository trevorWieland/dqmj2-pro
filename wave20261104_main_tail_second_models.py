import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R
import wave20261104_main_tail_proof as B

SPECS = {
    '02057434': dict(calls=[0x02029C88], args='three-u8'),
    '020574dc': dict(calls=[0x02214A54], output='s32'),
    '02057528': dict(calls=[0x02214ACC], output='s32'),
    '020575ec': dict(calls=[0x0205BF9C], output='u32'),
    '02057638': dict(calls=[0x0205BF7C], args='u8'),
    '02057ba4': dict(calls=[0x02218C24], args='u16'),
    '02057bf8': dict(calls=[0x02218CB4], args='u16'),
    '02057c4c': dict(calls=[0x02218D20], args='u16-s32'),
    '02058000': dict(calls=[0x0205E844], args='s32', conditional=True, status=1),
    '02058058': dict(calls=[0x02040534], args='shift'),
    '020580ac': dict(calls=[0x02040518], args='shift'),
    '02058100': dict(calls=[0x0205D8A4], args='u8', output='u32'),
    '02058158': dict(calls=[0x020D3FD0], output='u8'),
    '020581a8': dict(calls=[0x020D3FBC], args='u8'),
    '020581f8': dict(calls=[0x020D3DC0] * 3, loop=3, mode=1, output='s32-loop'),
    '02058264': dict(calls=[0x020D3DC0] * 6, loop=6, mode=2, output='s32-loop'),
    '020582d0': dict(calls=[0x020D3E80] * 3, loop=3, mode=1, output='u32-loop'),
    '0205833c': dict(calls=[0x020D3E80] * 6, loop=6, mode=2, output='u32-loop'),
    '020583a8': dict(calls=[0x020D3738, 0x020D38F0], args='word-chain', output='s32'),
    '020583f8': dict(calls=[0x020D37F0], output='s32'),
    '02058444': dict(calls=[0x0205C278], output='u32'),
    '02058674': dict(calls=[0x022092B0], args='u8'),
    '020586c4': dict(calls=[0x02209244, 0x022092E0], args='payload-chain'),
    '02058710': dict(calls=[0x0205DC70, 0x02209244, 0x022092E0], args='descriptor-chain'),
    '02058774': dict(calls=[0x022093EC], args='u8-s32'),
    '020587d4': dict(calls=[0x022094E8], args='u8')}


def run(row, body, ordinal, main, overlay):
    address = int(row['address'], 0)
    name = format(address, '08x')
    spec = SPECS[name]
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(0x021D7240, overlay)
    vm.mem_write(address, body)
    bank = ordinal % 4
    advance = [0, 4, 0xFFFFFFFF, 16, 100, 1, 0x80000000, 8][ordinal]
    supplied = [0, 1, 0xFFFFFFFF, 0x80000000, 0xFFFFFF00, 255, 32767, 65535][ordinal]
    first = [0, 1, 255, 256, 65535, 16777216, 31, 16][ordinal]
    if spec.get('args') == 'shift':
        first = [0, 1, 3, 7, 15, 16, 30, 31][ordinal]
    second = [0, 127, 128, 255, 256, 65535, 16777216, 4294967040][ordinal]
    if spec.get('args') in ('u16-s32', 'u8-s32'):
        second = [-32768, -129, -128, 127, 128, 255, 0, 1][ordinal]
    values = [first, second, [0, 1, 255, 256, 1024, 65535, 32768, 0][ordinal], 100, 200, 300, 400, 500]
    values = [B.floating(B.bits(v)) for v in values]
    context = bytearray((n * 17 + ordinal) & 255 for n in range(0x470 + 4 * 0x10C))
    context[3] = bank
    struct.pack_into('<8I', context, 16, *[B.bits(v) for v in values])
    positions = [0xFFFFFFFD, 0, 0x12345678, 0x80000000]
    for index, position in enumerate(positions):
        struct.pack_into('<I', context, 0x470 + index * 0x10C, position)
        context[0x477 + index * 0x10C] = 0xA5
    instruction = bytearray((n * 31 + ordinal) & 255 for n in range(128))
    struct.pack_into('<II', instruction, 0, 0x12345678, advance)
    vm.mem_write(B.CONTEXT, bytes(context))
    vm.mem_write(B.INSTRUCTION, bytes(instruction))
    initial = [0x11220000 + n * 0x100 + ordinal for n in range(15)]
    initial[:4] = [B.CONTEXT, B.INSTRUCTION, 0xDEADBEEF, 0xA5A55A5A]
    initial[-2:] = [B.SP, B.STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal << 28 | 0x10)
    for register, value in zip(C.REGISTERS, initial):
        vm.reg_write(register, value)
    calls, writes, pcs = [], [], []
    returned, changed = False, False
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items()}
    token = 0x02420000 + ordinal * 16
    decoded = supplied ^ 0x2468

    def put(location, data):
        vm.mem_write(location, data)
        writes.append(dict(provider=True, address=location, hex=data.hex()))

    def memory(uc, access, location, size, value, user):
        writes.append(dict(provider=False, address=location, size=size, value=value))

    def code(uc, location, size, user):
        nonlocal returned, changed
        pcs.append(location)
        if location == B.STOP:
            returned = True
            uc.emu_stop()
        elif location in imports:
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('Qualified ARM provider entered as Thumb')
            symbol = imports[location]
            args = [uc.reg_read(r) for r in C.REGISTERS[:4]]
            calls.append(dict(symbol=symbol, address=location, words=args, stack=bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP), 16)).hex()))
            result = supplied
            if symbol in ('_ffix', '_ffixu'):
                result = int(B.floating(args[0])) & 0xFFFFFFFF
            elif symbol in ('_fflt', '_ffltu'):
                result = B.bits(float(B.signed(args[0]) if symbol == '_fflt' else args[0]))
            elif symbol.startswith('_'):
                raise ValueError('Unexpected compiler helper outside this scalar family')
            else:
                if ordinal % 2 and not changed:
                    put(B.CONTEXT + 3, bytes([(bank + 1) % 4]))
                    put(B.INSTRUCTION + 4, struct.pack('<I', advance ^ 0x100))
                    changed = True
                if spec.get('conditional'):
                    result = ordinal % 2
                elif location in (0x020D3DC0, 0x020D3E80):
                    result = (supplied + args[1] * 17) & 0xFFFFFFFF
                elif location == 0x0205DC70:
                    result = token
                elif location == 0x02209244:
                    result = decoded
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, register in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xCAFE0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, result)
            uc.reg_write(R.UC_ARM_REG_CPSR, ((ordinal + len(calls)) & 15) << 28 | 0x10)
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
    if [call['address'] for call in game] != spec['calls']:
        failures.append('Independent provider sequence/count')
    integer = [int(v) & 0xFFFFFFFF for v in values]
    kind = spec.get('args')
    expected_words = {'three-u8': [v & 255 for v in integer[:3]], 'u8': [integer[0] & 255], 'u16': [integer[0] & 65535],
                      'u16-s32': [integer[0] & 65535, integer[1]], 'u8-s32': [integer[0] & 255, integer[1]],
                      's32': integer[:1], 'shift': [(1 << integer[0]) & 0xFFFFFFFF]}
    if kind in expected_words and game[0]['words'][:len(expected_words[kind])] != expected_words[kind]:
        failures.append('Independent scalar conversion/narrowing/shift arguments')
    if kind == 'word-chain' and game[1]['words'][0] != supplied:
        failures.append('Opaque returned word forwarded')
    if kind == 'payload-chain' and (game[0]['words'][0] != B.INSTRUCTION + 8 or game[1]['words'][0] != decoded):
        failures.append('Payload address and decoded-word forwarding')
    if kind == 'descriptor-chain' and (game[0]['words'][:3] != [2, 0, integer[0] & 65535] or game[1]['words'][0] != token or game[2]['words'][0] != decoded):
        failures.append('Narrow descriptor request and two opaque forwarding boundaries')
    if spec.get('loop') and [call['words'][:2] for call in game] != [[spec['mode'], i] for i in range(spec['loop'])]:
        failures.append('Independent indexed getter mode/count/order')
    expected = bytearray(context)
    final_bank = (bank + 1) % 4 if changed else bank
    final_advance = advance ^ 0x100 if changed else advance
    expected[3] = final_bank
    if not spec.get('conditional') or ordinal % 2:
        struct.pack_into('<I', expected, 0x470 + final_bank * 0x10C, (positions[final_bank] + final_advance) & 0xFFFFFFFF)
    expected[0x477 + final_bank * 0x10C] = spec.get('status', 0)
    output = spec.get('output')
    for index in range(spec.get('loop', 1)) if output else []:
        value = (supplied + index * 17) & 0xFFFFFFFF
        if output.startswith('s32'):
            value = B.signed(value)
        elif output == 'u8':
            value &= 255
        struct.pack_into('<I', expected, 16 + index * 4, B.bits(float(value)))
    if bytes(vm.mem_read(B.CONTEXT, len(context))) != expected:
        failures.append('Independent complete context, repeated conversions, bank stride and advancement/status model')
    expected_instruction = bytearray(instruction)
    struct.pack_into('<I', expected_instruction, 4, final_advance)
    if bytes(vm.mem_read(B.INSTRUCTION, len(instruction))) != expected_instruction:
        failures.append('Independent instruction forwarding/mutation model')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes,
                pcs=pcs, ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
