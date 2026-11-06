import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {'020602ec': {}, '020603ec': {}, '0206092c': {}, '02060954': {}, '0206099c': {}, '02060a20': {}}
SP, STOP, OUTPUT, OWNER, UI0, UI1, META, EFFECT, PARAMETERS = 0x027f0000, 0x027e0000, 0x02400000, 0x02401000, 0x02402000, 0x02403000, 0x02404000, 0x02405000, 0x02406000


def fixtures(name):
    if name == '020602ec':
        return [dict(flags=(n << 4) | (n * 7 & 15) | ((k * 0x55) << 8), x=[-32768, -1, 0, 32767][k],
                     y=[32767, 0, -1, -32768][k], mode=[0, 1, -1, -2147483648][k], value=0x80000000 + n,
                     returned=[0, 1, 0xfffffff9, 0xffffffff][k]) for n in range(16) for k in range(4)]
    if name == '020603ec':
        return [dict(value=item, kind=kind, style=style, modifier=[-32768, -1, 0, 32767][n], flags=0)
                for n, item in enumerate([-32768, -1, 0, 32767]) for kind in [0, 0x80000000] for style in [0, 255]]
    if name == '0206092c':
        return [dict(value=value, flags=0) for value in list(range(256)) + [0x80000000, 0xffffffff, 0x12345678, 0x100]]
    if name == '02060954':
        return [dict(value=0x80000000 + n, flags=(n << 4) | upper) for n in range(16) for upper in [0, 0xff0f]]
    if name == '0206099c':
        return [dict(value=kind, mapped=mapped, flags=0) for kind in [-2147483648, -1, 0, 7, 8, 9, 2147483647] for mapped in [0, 255, 256, 0xffffffff]]
    return [dict(value=item, symbol=symbol, mapped=mapped, flags=0) for item in [0, 0xffffffff]
            for symbol in [0, 1, 0x80, 0xff] for mapped in [0, 255, 256, 0xffffffff]]


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    expected = {OUTPUT: bytearray((i * 13 + ordinal) & 255 for i in range(512)),
                OWNER: bytearray((i * 17 + ordinal) & 255 for i in range(32)),
                UI0: bytearray((i * 19 + ordinal) & 255 for i in range(128)),
                UI1: bytearray((i * 23 + ordinal) & 255 for i in range(128)),
                META: bytearray((i * 29 + ordinal) & 255 for i in range(16)),
                EFFECT: bytearray((i * 31 + ordinal) & 255 for i in range(64))}
    struct.pack_into('<I', expected[OWNER], 4, UI0)
    struct.pack_into('<H', expected[META], 4, fixture['flags'])
    for n, location in enumerate([UI0, UI1]):
        struct.pack_into('<I', expected[location], 0x68, PARAMETERS + n * 0x100)
    for location, region in expected.items():
        vm.mem_write(location, bytes(region))
    vm.mem_write(SP - 256, bytes((i * 37 + ordinal) & 255 for i in range(512)))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    if name == '020602ec':
        initial[:4] = [OWNER, fixture['value'], 0x89ab0000 + ordinal, fixture['x'] & 0xffffffff]
        vm.mem_write(SP, struct.pack('<2I', fixture['y'] & 0xffffffff, fixture['mode'] & 0xffffffff))
    elif name == '020603ec':
        initial[:4] = [OUTPUT, fixture['value'] & 0xffffffff, fixture['kind'], fixture['style']]
        vm.mem_write(SP, struct.pack('<I', fixture['modifier'] & 0xffffffff))
    else:
        initial[:2] = [fixture['value'] & 0xffffffff, OUTPUT]
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal % 16 << 28 | 0x10)
    for register, word in zip(C.REGISTERS, initial):
        vm.reg_write(register, word)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function'}
    calls, writes, pcs, failures, actions = [], [], [], [], []
    returned = False
    result = 2

    def word(value):
        return struct.pack('<I', value & 0xffffffff)

    def action(location, args, returned_word=0x80000000, mutations=(), reads=()):
        actions.append(dict(address=location, args=[v & 0xffffffff for v in args], returned=returned_word, mutations=list(mutations), reads=list(reads)))
        for at, data in mutations:
            for base, region in expected.items():
                if base <= at and at + len(data) <= base + len(region):
                    region[at - base:at - base + len(data)] = data
                    break

    if name == '020602ec':
        buffer = SP - 88
        initial_flags = fixture['flags']
        late_flags = initial_flags ^ 0xf0
        action(0x020449d4, [fixture['value']], META, [(OWNER + 4, word(UI1)), (META + 4, struct.pack('<H', initial_flags))])
        action(0x02008be0, [0, buffer, 64], mutations=[(buffer, bytes(64)), (OWNER + 4, word(UI0)), (META + 4, struct.pack('<H', late_flags))])
        glyph = struct.unpack_from('<H', main, 0xdbc18 + 2 * (392 + ((late_flags >> 4) & 15)))[0]
        symbol_buffer = struct.pack('<H', glyph) + bytes(62)
        action(0x02087a48, [UI1, 0, fixture['x'], fixture['y'], 1, buffer], returned_word=0xffffffff,
               reads=[(buffer, symbol_buffer)])
        action(0x020852b0, [UI1 + 0x3c, initial[2]], mutations=[(UI1 + 0x5e, b'\x9a'), (UI1 + 0x68, word(PARAMETERS + 0x200))])
        text = struct.pack('<32H', *([0x41 + ordinal + i for i in range(31)] + [0]))
        action(0x02046af4, [0x021c9698, PARAMETERS + 0x200, 0x9a, 0, buffer, 255], mutations=[(buffer, text)])
        shifted = (fixture['x'] + 8 + 32768) % 65536 - 32768
        action(0x02087a48, [UI1, 0, shifted, fixture['y'], fixture['mode'], buffer], fixture['returned'], reads=[(buffer, text)])
        result = (fixture['returned'] + 8) & 0xffff
    elif name == '020603ec':
        parameters = SP - 48
        descriptor = bytes((i * 41 + ordinal) & 255 for i in range(32))
        action(0x02044ff4, [parameters, fixture['value'], fixture['kind']], mutations=[(parameters, descriptor)])
        text = struct.pack('<8H', 0xe200, 0x3456, 0xffff, ordinal, 0, 0, 0, 0)
        action(0x02046af4, [0x021c9698, parameters, fixture['style'], fixture['modifier'], OUTPUT, 255],
               returned_word=0xffffffff, mutations=[(OUTPUT, text)], reads=[(parameters, descriptor)])
        result = 1
    else:
        command = SP - (8 if name == '0206092c' else 16)
        encoded = fixture['value'] & 255
        if name == '02060954':
            action(0x020449d4, [fixture['value']], META, [(META + 4, struct.pack('<H', fixture['flags']))])
            encoded = 13 + ((fixture['flags'] >> 4) & 15)
        elif name == '0206099c':
            if fixture['value'] >= 8:
                action(0x02060510, [fixture['value']], fixture['mapped'])
                encoded = fixture['mapped'] & 255
            else:
                result = 0
        elif name == '02060a20':
            action(0x02065d88, [fixture['value']], EFFECT, [(EFFECT + 0x24, bytes([fixture['symbol']]))])
            action(0x02066a6c, [fixture['symbol']], fixture['mapped'])
            encoded = fixture['mapped'] & 255
        if result:
            payload = bytes([0xe2, encoded])
            action(0x02047ff0, [command, 2, OUTPUT], mutations=[(OUTPUT, payload + word(0xface0000 + ordinal))], reads=[(command, payload)])

    def memory(uc, access, location, size, value, user):
        writes.append(dict(provider=False, address=location, size=size, value=value))

    def code(uc, location, size, user):
        nonlocal returned
        pcs.append(location)
        if location == STOP:
            returned = True
            uc.emu_stop()
            return
        if location in imports:
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('Measured text provider entered as Thumb')
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            stack = uc.reg_read(R.UC_ARM_REG_SP)
            stack_words = list(struct.unpack('<2I', bytes(uc.mem_read(stack, 8))))
            n = len(calls)
            calls.append(dict(address=location, symbol=imports[location], words=args, stackWords=stack_words, stack=stack))
            current = actions[n] if n < len(actions) else dict(address=0, args=[], returned=0, mutations=[], reads=[])
            if location != current['address'] or (args + stack_words)[:len(current['args'])] != current['args']:
                failures.append('Independent text/glyph provider sequence, signed coordinates, captured UI, buffer and stack argument ABI')
            for at, data in current['reads']:
                if bytes(uc.mem_read(at, len(data))) != data:
                    failures.append('Independent complete two-byte glyph/64-byte wide buffer/32-byte parameter descriptor')
            for at, data in current['mutations']:
                uc.mem_write(at, data)
                writes.append(dict(provider=True, address=at, hex=data.hex()))
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, register in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xcafe0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, current['returned'])
            uc.reg_write(R.UC_ARM_REG_CPSR, (ordinal + len(calls)) % 16 << 28 | 0x10)
            uc.reg_write(R.UC_ARM_REG_PC, lr)
        elif not address <= location < address + len(body):
            raise ValueError(('Unmodeled native provider/body execution forbidden', hex(location)))

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=2000)
    if not returned:
        raise ValueError('Actual text/glyph caller did not return')
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Actual text/glyph caller callee-saved registers/SP differ')
    if registers[0] != result or len(calls) != len(actions):
        failures.append('Independent complete provider sequence and narrowed/literal text result')
    for location, region in expected.items():
        if bytes(vm.mem_read(location, len(region))) != region:
            failures.append('Independent complete owner/both UI/metadata/effect/output states')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
