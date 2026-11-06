import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {'02028a4c': {}, '02028af4': {}}
SP, STOP, OUTPUT, RESOURCE, OWNER0, OWNER1, TEXTURE, MODEL = 0x027f0000, 0x027e0000, 0x02400000, 0x02401000, 0x02402000, 0x02403000, 0x02404000, 0x02405000


def fixtures(name):
    if name == '02028a4c':
        return [dict(signature=signature, owner=owner, mode=mode, parsed=parsed, texture=texture, model=model)
                for signature, owner, mode, parsed, texture, model in [(0, 1, 0, 1, 1, 1), (0x30444d42, 1, 1, 1, 1, 1), (0x30585442, 0, 1, 1, 1, 1)] +
                [(0x30585442, 1, mode, parsed, texture, model) for mode in [0, 1, 0x80000000]
                 for parsed, texture, model in [(0, 1, 1), (1, 0, 1), (0x80000000, 1, 0), (1, 1, 1)]]]
    return [dict(flags=n, owner=n % 3 != 0, auxiliary=n % 4 != 0, count=n % 2, mutate=bool(n & 4)) for n in range(256)] + [
        dict(flags=3, owner=owner, auxiliary=auxiliary, count=count, mutate=mutate)
        for owner in [0, 1] for auxiliary in [0, 1] for count in [0, 255] for mutate in [False, True]]


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    context = bytearray((i * 17 + ordinal) & 255 for i in range(96))
    header = bytearray((i * 23 + ordinal) & 255 for i in range(32))
    struct.pack_into('<I', context, 0, OWNER0 if fixture['owner'] else 0)
    struct.pack_into('<I', context, 8, RESOURCE if fixture.get('auxiliary') else 0)
    context[0x38] = fixture.get('flags', 0xa4)
    context[0xf] = fixture.get('count', 0x95)
    struct.pack_into('<I', header, 0, fixture.get('signature', 0x30585442))
    expected = {OUTPUT: bytearray(context), RESOURCE: bytearray(header)}
    for location, region in expected.items():
        vm.mem_write(location, bytes(region))
    vm.mem_write(SP - 256, bytes((i * 31 + ordinal) & 255 for i in range(512)))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    initial[:3] = [OUTPUT, RESOURCE, fixture.get('mode', 0)]
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal % 16 << 28 | 0x10)
    for register, word in zip(C.REGISTERS, initial):
        vm.reg_write(register, word)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function'}
    calls, writes, pcs, failures = [], [], [], []
    actions = []
    returned = False
    result = 0

    def action(location, args, returned_word, mutations):
        actions.append(dict(address=location, args=args, returned=returned_word, mutations=mutations))
        for at, data in mutations:
            for base, region in expected.items():
                if base <= at and at + len(data) <= base + len(region):
                    region[at - base:at - base + len(data)] = data
                    break

    def word(value):
        return struct.pack('<I', value)

    if name == '02028a4c':
        if fixture['signature'] == 0x30585442 and fixture['owner']:
            args = [RESOURCE] if fixture['mode'] else [OUTPUT, RESOURCE]
            action(0x02031fa4 if fixture['mode'] else 0x0202882c, args, fixture['parsed'], [(OUTPUT, word(OWNER1)), (OUTPUT + 8, word(0xfeed0000 + ordinal))])
            if fixture['parsed']:
                action(0x0202beec, [RESOURCE], TEXTURE if fixture['texture'] else 0, [(OUTPUT, word(OWNER1 + 4)), (RESOURCE, word(0xfeed1000 + ordinal))])
                action(0x0202bedc, [OWNER1 + 4], MODEL if fixture['model'] else 0, [(OUTPUT, word(0)), (OUTPUT + 8, word(0xfeed2000 + ordinal))])
                action(0x0202f3dc, [MODEL if fixture['model'] else 0, TEXTURE if fixture['texture'] else 0], 0xdead0000 + ordinal, [(OUTPUT + 8, word(0xfeed3000 + ordinal))])
                struct.pack_into('<I', expected[OUTPUT], 8, RESOURCE)
                result = 1
    else:
        if context[0x38] & 1:
            result |= 1
            if fixture['owner']:
                changes = [(OUTPUT + 0x38, bytes([context[0x38] ^ 2])), (OUTPUT + 8, word(OWNER1)), (OUTPUT + 0xf, b'\xff')] if fixture['mutate'] else []
                action(0x020321dc, [OWNER0], 0xdead1000 + ordinal, changes)
        if expected[OUTPUT][0x38] & 2:
            result |= 2
            auxiliary = struct.unpack_from('<I', expected[OUTPUT], 8)[0]
            if auxiliary:
                changes = [(OUTPUT + 0xf, b'\x00' if fixture['count'] else b'\xff')] if fixture['mutate'] else []
                action(0x020321dc, [auxiliary], 0xdead2000 + ordinal, changes)
            if expected[OUTPUT][0xf]:
                action(0x0203c00c, [OUTPUT + 0x10], 0xdead3000 + ordinal, [(OUTPUT + 0x38, b'\xf7')])
        expected[OUTPUT][0x38] = 0

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
                raise ValueError('Measured resource provider entered as Thumb')
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            call = dict(address=location, symbol=imports[location], words=args)
            n = len(calls)
            calls.append(call)
            if n >= len(actions):
                failures.append('Extra provider beyond independently predicted sequence')
                current = dict(address=0, args=[], returned=0, mutations=[])
            else:
                current = actions[n]
            if location != current['address'] or args[:len(current['args'])] != current['args']:
                failures.append('Independent complete provider order/argument pointer ABI')
            if name == '02028a4c' and n == 3 and bytes(uc.mem_read(OUTPUT + 8, 4)) != word(0xfeed2000 + ordinal):
                failures.append('Auxiliary pointer must commit after model bind provider')
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
    vm.emu_start(address, STOP + 4, count=1500)
    if not returned:
        raise ValueError('Actual resource caller did not return')
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Actual resource caller callee-saved registers/SP differ')
    if registers[0] != result or len(calls) != len(actions):
        failures.append('Independent complete provider sequence and resource result')
    for location, region in expected.items():
        if bytes(vm.mem_read(location, len(region))) != region:
            failures.append('Independent complete resource/context state: ' + hex(location))
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
