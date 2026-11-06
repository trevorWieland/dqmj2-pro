import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {name: {} for name in ['020281b8', '0202859c', '020285c8', '02028dac', '02028dcc']}
SP, STOP, NODE0, NODE1, OUTPUT, INPUT, FLAGS, CURRENT = 0x027f0000, 0x027e0000, 0x02400000, 0x02401000, 0x02402000, 0x02403000, 0x02410000, 0x020edd0c


def fixtures(name):
    if name in ['02028dac', '02028dcc']:
        return [dict(value=value) for value in range(256)]
    if name in ['0202859c', '020285c8']:
        return [dict(provided=not bool(n % 2), outputKind=n // 2) for n in range(8)]
    return [dict(vector=list(vector), providerReturn=returned) for vector, returned in
            [((0, 0, 0), 0), ((4096, 0, 0), 1), ((12288, 16384, 0), 4096),
             ((-4096, 8192, -12288), 8192), ((-2147483648, 2147483647, 0), 0x7fffffff),
             ((-2147483648, -2147483648, -2147483648), 0x80000000),
             ((0x12345678, -0x12345678, 2147483647), 0xffffffff), ((-1, 1, 65535), 0x12345678)]]


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    node0 = bytearray((i * 17 + ordinal) & 255 for i in range(64))
    node1 = bytearray((i * 29 + ordinal) & 255 for i in range(64))
    output = bytearray((i * 13 + ordinal) & 255 for i in range(64))
    value = bytearray((i * 23 + ordinal) & 255 for i in range(32))
    flags = bytearray((i * 31 + ordinal) & 255 for i in range(32))
    current = bytearray((i * 7 + ordinal) & 255 for i in range(16))
    for index, data in enumerate([node0, node1]):
        struct.pack_into('<iii', data, 28, 0x12340000 + ordinal + index, -4096 - ordinal - index, -2147483648 + ordinal + index)
        struct.pack_into('<iii', data, 40, -1 - ordinal - index, 8192 + ordinal + index, 2147483647 - ordinal - index)
    struct.pack_into('<I', current, 8, NODE1)
    field = 8 if name == '02028dac' else 12
    if name in ['02028dac', '02028dcc']:
        flags[field] = fixture['value']
    if name == '020281b8':
        struct.pack_into('<iii', value, 0, *fixture['vector'])
    regions = {NODE0: node0, NODE1: node1, OUTPUT: output, INPUT: value, FLAGS: flags, CURRENT: current}
    expected = {location: bytearray(data) for location, data in regions.items()}
    for location, data in regions.items():
        vm.mem_write(location, bytes(data))
    vm.mem_write(SP - 256, bytes((i * 19 + ordinal) & 255 for i in range(512)))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    if name in ['0202859c', '020285c8']:
        chosen = NODE0 if fixture['provided'] else NODE1
        offset = 28 if name == '0202859c' else 40
        other = 40 if offset == 28 else 28
        destination = [0, OUTPUT, chosen + offset, chosen + other][fixture['outputKind']]
        initial[:2] = [NODE0 if fixture['provided'] else 0, destination]
        if destination:
            words = bytes(regions[chosen][offset:offset + 12])
            if destination == OUTPUT:
                expected[OUTPUT][:12] = words
            else:
                at = destination - chosen
                expected[chosen][at:at + 12] = words
    else:
        initial[0] = INPUT if name == '020281b8' else FLAGS
        if name != '020281b8' and fixture['value']:
            expected[FLAGS][field] = 0
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, (ordinal % 16) << 28 | 0x10)
    for register, word in zip(C.REGISTERS, initial):
        vm.reg_write(register, word)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function'}
    calls, writes, pcs, failures = [], [], [], []
    returned = False

    def memory(uc, access, location, size, word, user):
        writes.append(dict(address=location, size=size, value=word))

    def code(uc, location, size, user):
        nonlocal returned
        pcs.append(location)
        if location == STOP:
            returned = True
            uc.emu_stop()
        elif location in imports:
            if name != '020281b8' or location != 0x0200236c or uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('Unexpected native scalar-provider body/mode')
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            calls.append(dict(symbol=imports[location], address=location, words=args))
            total = sum(component * component for component in fixture['vector']) & ((1 << 64) - 1)
            if args[0] != total >> 12 & 0xffffffff:
                failures.append('Independent signed32 square products, modulo64 accumulation and low32 shifted scalar argument')
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, register in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xcafe0000 + index)
            uc.reg_write(R.UC_ARM_REG_R0, fixture['providerReturn'])
            uc.reg_write(R.UC_ARM_REG_CPSR, ((ordinal + 7) % 16) << 28 | 0x10)
            uc.reg_write(R.UC_ARM_REG_PC, lr)
        elif not address <= location < address + len(body):
            raise ValueError(('Unmodeled native body execution forbidden', hex(location)))

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=500)
    if not returned:
        raise ValueError('Actual caller failed to return')
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Callee-saved registers/SP differ')
    if name == '020281b8':
        result = fixture['providerReturn']
        if len(calls) != 1:
            failures.append('Independent single opaque scalar-provider call')
    elif name in ['0202859c', '020285c8']:
        result = chosen + offset
        if calls:
            failures.append('Vector getter must execute no provider')
    else:
        result = int(bool(fixture['value']))
        stores = [write for write in writes if FLAGS <= write['address'] < FLAGS + len(flags)]
        wanted = [] if not fixture['value'] else [dict(address=FLAGS + field, size=1, value=0)]
        if stores != wanted or calls:
            failures.append('Independent byte test, exactly one conditional zero store and no provider')
    if registers[0] != result:
        failures.append('Independent scalar, field pointer or normalized acknowledge return')
    for location, data in expected.items():
        if bytes(vm.mem_read(location, len(data))) != data:
            failures.append('Independent complete vector/node/output/flag/current region: ' + hex(location))
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
