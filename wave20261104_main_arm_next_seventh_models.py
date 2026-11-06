import itertools
import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {'02039ab0': {}, '02039b20': {}}
SP, STOP, OUTPUT, INFO, ARCHIVE, RECORD = 0x027f0000, 0x027e0000, 0x02400000, 0x02401000, 0x02402000, 0x02403000


def fixtures(name):
    if name == '02039ab0':
        return [dict(fields=list(values), lookup=lookup, index=-9 if n % 2 else 0x7fffffff, ordinal=n)
                for n, values in enumerate(itertools.product([-2147483648, -1, 0, 2147483647], repeat=3)) for lookup in [False, True]]
    return [dict(index=index, subindex=subindex, failed=failed, ordinal=n)
            for n, (index, subindex, failed) in enumerate(itertools.product([-1, 0, 0x7fffffff], [-1, 0, 0x7fffffff], [0, 1, 2, 3]))]


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    output = bytearray((i * 17 + ordinal) & 255 for i in range(64))
    info = bytearray((i * 23 + ordinal) & 255 for i in range(32))
    record = bytearray((i * 31 + ordinal) & 255 for i in range(32))
    expected = {OUTPUT: output, INFO: info, RECORD: record}
    for location, region in expected.items():
        vm.mem_write(location, bytes(region))
    vm.mem_write(SP - 256, bytes((i * 29 + ordinal) & 255 for i in range(512)))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    initial[0] = OUTPUT
    if name == '02039ab0':
        initial[1:4] = [v & 0xffffffff for v in fixture['fields']]
        vm.mem_write(SP, struct.pack('<I', fixture['index'] & 0xffffffff))
    else:
        initial[1:3] = [fixture['index'] & 0xffffffff, fixture['subindex'] & 0xffffffff]
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal % 16 << 28 | 0x10)
    for register, word in zip(C.REGISTERS, initial):
        vm.reg_write(register, word)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function'}
    calls, writes, pcs, failures = [], [], [], []
    actions = []
    returned = False
    result = [0, 1, 0x80000000, 0xffffffff][ordinal % 4]
    field4 = [0, 0xffff, 0x8000, 0x7fff][fixture['ordinal'] % 4]
    field8 = 0xff if ordinal % 2 else 0x80
    field9 = 0x80 if ordinal % 2 else 0xff
    record_mutations = [(RECORD + 4, struct.pack('<H', field4)), (RECORD + 8, bytes([field8, field9]))]

    def action(location, args, returned_word, mutations):
        actions.append(dict(address=location, args=[v & 0xffffffff for v in args], returned=returned_word, mutations=mutations))
        for at, data in mutations:
            for base, region in expected.items():
                if base <= at and at + len(data) <= base + len(region):
                    region[at - base:at - base + len(data)] = data
                    break

    if name == '02039ab0':
        action(0x02038d88, [fixture['index']], RECORD if fixture['lookup'] else 0, record_mutations)
        if fixture['lookup']:
            resolved = [default if value < 0 else value for value, default in zip(fixture['fields'], [field9, field4, field8])]
            action(0x02039ba0, [OUTPUT, *resolved, RECORD, fixture['index']], result, [(OUTPUT + 12, struct.pack('<I', 0xdead0000 + ordinal))])
        else:
            result = 0
    else:
        resource_id = 0x80001000 + ordinal
        action(0x02038dec, [fixture['index']], 0 if fixture['failed'] == 1 else INFO, [(INFO, struct.pack('<I', resource_id))])
        if fixture['failed'] != 1:
            action(0x0203917c, [resource_id], 0 if fixture['failed'] == 2 else ARCHIVE, [(INFO, struct.pack('<I', 0xdead0000 + ordinal))])
            if fixture['failed'] != 2:
                action(0x020389f4, [ARCHIVE, fixture['subindex']], 0 if fixture['failed'] == 3 else RECORD, record_mutations)
                if fixture['failed'] != 3:
                    action(0x02039c9c, [OUTPUT, field9, field4, field8, RECORD, ARCHIVE, fixture['index'], fixture['subindex']], result,
                           [(OUTPUT + 12, struct.pack('<I', 0xdead1000 + ordinal)), (RECORD + 8, b'\x17\x39')])
        if fixture['failed']:
            result = 0

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
                raise ValueError('Measured record provider entered as Thumb')
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            stack = uc.reg_read(R.UC_ARM_REG_SP)
            words = list(struct.unpack('<4I', bytes(uc.mem_read(stack, 16))))
            call = dict(address=location, symbol=imports[location], words=args, stackWords=words, stack=stack)
            n = len(calls)
            calls.append(call)
            current = actions[n] if n < len(actions) else dict(address=0, args=[], returned=0, mutations=[])
            observed = args + words
            if location != current['address'] or observed[:len(current['args'])] != current['args']:
                failures.append('Independent complete provider order/default fields/zero extension/stack argument ABI')
            if location in [0x02039ba0, 0x02039c9c] and row['realLink']['exactCallerBytes'] and stack != SP - (32 if name == '02039ab0' else 40):
                failures.append('Independent original six/eight-argument stack frame')
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
    vm.emu_start(address, STOP + 4, count=1000)
    if not returned:
        raise ValueError('Actual record caller did not return')
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Actual record caller callee-saved registers/SP differ')
    if registers[0] != result or len(calls) != len(actions):
        failures.append('Independent complete record provider sequence and forwarded result')
    for location, region in expected.items():
        if bytes(vm.mem_read(location, len(region))) != region:
            failures.append('Independent complete output/info/record state')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
