import itertools
import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {'02067380': {}}
SP, STOP, TRANSITION, MODE = 0x027f0000, 0x027e0000, 0x021c36fc, 0x020de23c


def fixtures(name):
    return [dict(mode=mode, step=step, choice=choice, desired=mode if not mismatch else mode ^ 0x1234,
                 outcome=[0, 1, 2, 0xffffffff][n % 4])
            for n, (mode, step, choice, mismatch) in enumerate(itertools.product(
                [0, 1, 2, 3, 4, 0xffffffff], [0, 5, 10, 20, 0xffff, -1], [0, 1, 2, 3, 0xff], [False, True]))]


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    transition = bytearray([fixture['choice'], 0x89, ordinal & 255, 0xab]) + bytearray(struct.pack('<I', fixture['step'] & 0xffffffff))
    mode = bytearray(struct.pack('<2I', fixture['desired'], fixture['mode']))
    expected = {TRANSITION: transition, MODE: mode}
    for location, region in expected.items():
        vm.mem_write(location, bytes(region))
    vm.mem_write(SP - 256, bytes((i * 31 + ordinal) & 255 for i in range(512)))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal % 16 << 28 | 0x10)
    for register, word in zip(C.REGISTERS, initial):
        vm.reg_write(register, word)
    imports = {int(binding['address'], 0): (symbol, binding) for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function'}
    calls, writes, pcs, failures, actions = [], [], [], [], []
    returned = False
    result = 0

    def word(value):
        return struct.pack('<I', value & 0xffffffff)

    def action(location, args=(), returned_word=0):
        n = len(actions)
        mutations = [(TRANSITION + 4, word(0x76540000 + ordinal + n)), (TRANSITION, bytes([fixture['choice'] ^ 0x80])),
                     (MODE, word(0x9abc0000 + ordinal + n)), (MODE + 4, word(0x80000000 + ordinal + n))]
        actions.append(dict(address=location, args=list(args), returned=returned_word, mutations=mutations))
        for at, data in mutations:
            for base, region in expected.items():
                if base <= at and at + len(data) <= base + len(region):
                    region[at - base:at - base + len(data)] = data
                    break

    def store_step(value):
        struct.pack_into('<I', expected[TRANSITION], 4, value)

    def copy_desired():
        expected[MODE][4:8] = expected[MODE][0:4]

    if fixture['step'] == 0xffff:
        result = 1
    elif fixture['mode'] == 0:
        result = 1
    elif fixture['mode'] == 2:
        if fixture['step'] == 0:
            action(0x02041510, [1, 2, 10])
            action(0x02041560, [10])
            action(0x020414b0, [0x21])
            store_step(10)
        elif fixture['step'] == 10:
            if fixture['choice'] == 3:
                store_step(20)
            elif fixture['choice'] in [1, 2]:
                action(0x02041510, [int(fixture['choice'] == 2), 2, 10])
                action(0x020418e8, [10, 10])
                action(0x020414b0, [0x3f])
                store_step(20)
            elif fixture['mode'] != fixture['desired']:
                action(0x02041510, [1, 2, 10])
                action(0x020418e8, [10, 10])
                action(0x020414b0, [0x3f])
                copy_desired()
                store_step(0xffff)
        elif fixture['step'] == 20:
            action(0x02041800, returned_word=fixture['outcome'])
            result = int(fixture['outcome'] != 1)
    elif fixture['mode'] in [1, 3]:
        if fixture['step'] == 0:
            action(0x02214120)
            action(0x020407cc, returned_word=fixture['outcome'])
            if not fixture['outcome']:
                action(0x02041510, [1, 2, 10])
            else:
                action(0x020407bc, [0])
            store_step(5)
        elif fixture['step'] == 5:
            action(0x02041800, returned_word=fixture['outcome'])
            if fixture['outcome'] != 1:
                store_step(10)
        elif fixture['step'] == 10:
            action(0x022149dc, returned_word=fixture['outcome'])
            if fixture['outcome']:
                copy_desired()
                store_step(0xffff)
                result = 1

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
            symbol, binding = imports[location]
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('Measured ordered-state provider entered as Thumb')
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            n = len(calls)
            calls.append(dict(symbol=symbol, address=location, module=binding['module'], processor=binding['processor'], program=binding.get('program') or '', mode=binding['mode'], words=args))
            current = actions[n] if n < len(actions) else dict(address=0, args=[], returned=0, mutations=[])
            if location != current['address'] or args[:len(current['args'])] != current['args']:
                failures.append('Independent complete original main/ov000 provider order/word arguments')
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
            raise ValueError(('Unmodeled native main/overlay body execution forbidden', hex(location)))

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=2000)
    if not returned:
        raise ValueError('Actual ordered-state caller did not return')
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Actual ordered-state caller callee-saved registers/SP differ')
    if registers[0] != result or len(calls) != len(actions):
        failures.append('Independent captured dispatch/ordered choices/nonzero-vs-one tests/result')
    for location, region in expected.items():
        if bytes(vm.mem_read(location, len(region))) != region:
            failures.append('Independent complete two-state words,choice,padding,late desired copy/provider mutation persistence')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
