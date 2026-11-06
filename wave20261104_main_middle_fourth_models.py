import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {name: {} for name in ['02048d14', '02048d54', '02048d94', '02048dd4', '0204983c']}
CHECKERS = {'02048d14': 0x020349b8, '02048d54': 0x0203454c, '02048d94': 0x0203470c, '02048dd4': 0x020346c0}
SP, STOP, TAG, VALUE, ENTRIES, LINKS = 0x027f0000, 0x027e0000, 0x02102970, 0x02410000, 0x02420000, 0x02421000


def fixtures(name):
    if name == '0204983c':
        return [dict(first=first, second=second) for first, second in
                [(-1, -128), (-128, 127), (127, -1), (0, 0), (128, 1), (-129, 0), (0x7fffffff, 0), (1, -1)]]
    return [dict(null=True, result=0, before=42, after=255, key=0),
            dict(null=False, result=1, before=42, after=128, key=0xffffffff),
            dict(null=False, result=0x80000000, before=42, after=255, key=0x80000000)] + [
                dict(null=False, result=0, before=42, after=tag, key=0x12345678 ^ tag) for tag in [0, 1, 127, 128, 255]]


def signed(byte):
    return byte - 256 if byte >= 128 else byte


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    value = bytearray((i * 17 + ordinal) & 255 for i in range(32))
    entries = bytearray((i * 13 + ordinal) & 255 for i in range(36 * 8 + 32))
    links = bytearray((i * 29 + ordinal) & 255 for i in range(36 * 8 + 32))
    planned_handlers = []
    mutate = False
    if name == '0204983c':
        first, second = fixture['first'], fixture['second']
        for index in range(36):
            struct.pack_into('<Ibb', entries, index * 8, LINKS + index * 8 if index % 3 else 0, index - 18, 17 - index)
            struct.pack_into('<I', links, index * 8 + 4, VALUE + index if index % 4 else 0)
        mutate = -128 <= first <= 127 and -128 <= second <= 127
        if mutate:
            struct.pack_into('<Ibb', entries, 5 * 8, LINKS + 5 * 8, first, second)
            struct.pack_into('<I', links, 5 * 8 + 4, VALUE + 5)
            struct.pack_into('<I', entries, 6 * 8, 0)
        simulated = bytearray(entries)
        for index in range(36):
            link, field4, field5 = struct.unpack_from('<Ibb', simulated, index * 8)
            resource = struct.unpack_from('<I', links, link - LINKS + 4)[0] if link else 0
            if link and resource and field4 == first and field5 == second:
                planned_handlers.append(index)
                if index == 5 and mutate:
                    struct.pack_into('<Ibb', simulated, 6 * 8, LINKS + 6 * 8, first, second)
        initial_args = [first & 0xffffffff, second & 0xffffffff]
    else:
        vm.mem_write(TAG, bytes([fixture['before']]))
        initial_args = [fixture['key'], 0 if fixture['null'] else VALUE]
    regions = [(VALUE, value), (ENTRIES, entries), (LINKS, links)]
    expected = {location: bytearray(data) for location, data in regions}
    for location, data in regions:
        vm.mem_write(location, bytes(data))
    expected_tag = fixture.get('before', 0)
    vm.mem_write(SP - 256, bytes((i * 23 + ordinal) & 255 for i in range(512)))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    initial[:2] = initial_args
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal << 28 | 0x10)
    for register, word in zip(C.REGISTERS, initial):
        vm.reg_write(register, word)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function'}
    calls, writes, pcs, failures, handled = [], [], [], [], []
    returned = False
    gets = 0

    def put(location, data):
        vm.mem_write(location, data)
        for base, region in expected.items():
            if base <= location and location + len(data) <= base + len(region):
                region[location - base:location - base + len(data)] = data
                break
        writes.append(dict(provider=True, address=location, hex=data.hex()))

    def memory(uc, access, location, size, word, user):
        writes.append(dict(provider=False, address=location, size=size, value=word))

    def code(uc, location, size, user):
        nonlocal returned, gets, expected_tag
        pcs.append(location)
        if location == STOP:
            returned = True
            uc.emu_stop()
        elif location in imports:
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('Qualified ARM provider entered as Thumb')
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            calls.append(dict(symbol=imports[location], address=location, words=args))
            result = 0xdead0000 + ordinal
            if name == '0204983c':
                if location == 0x02049aa8:
                    if gets >= 36:
                        raise ValueError('Unbounded entry getter protocol')
                    if args[0] != gets:
                        failures.append('Independent ascending36-entry signed-byte index protocol')
                    result = ENTRIES + gets * 8
                    gets += 1
                elif location == 0x02049898:
                    delta = args[0] - ENTRIES
                    if delta % 8 or not 0 <= delta // 8 < 36:
                        raise ValueError('Entry handler pointer escaped measured model domain')
                    index = delta // 8
                    handled.append(index)
                    if index == 5 and mutate:
                        put(ENTRIES + 6 * 8, struct.pack('<Ibb', LINKS + 6 * 8, fixture['first'], fixture['second']))
                else:
                    raise ValueError('Unexpected signed-entry provider')
            else:
                if location == CHECKERS[name]:
                    if args[:2] != [VALUE, fixture['key']]:
                        failures.append('Independent predicate pointer/key forwarding')
                    expected_tag = fixture['after']
                    put(TAG, bytes([expected_tag]))
                    put(VALUE + 4, struct.pack('<I', 0xcafe0000 + ordinal))
                    result = fixture['result']
                elif location == 0x0204532c:
                    if args[:2] != [signed(fixture['after']) & 0xffffffff, VALUE]:
                        failures.append('Independent late signed-byte reload and cleanup pointer')
                    expected_tag = 0xa5
                    put(TAG, b'\xa5')
                    put(VALUE + 8, struct.pack('<I', 0xbeef0000 + ordinal))
                else:
                    raise ValueError('Unexpected guarded-value provider')
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, register in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xcafe0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, result)
            uc.reg_write(R.UC_ARM_REG_CPSR, ((ordinal + 7) % 16) << 28 | 0x10)
            uc.reg_write(R.UC_ARM_REG_PC, lr)
        elif not address <= location < address + len(body):
            raise ValueError(('Unmodeled native body execution forbidden', hex(location)))

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=5000)
    if not returned:
        raise ValueError('Actual caller failed to return')
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Callee-saved registers/SP differ')
    if name == '0204983c':
        if gets != 36 or handled != planned_handlers:
            failures.append('Independent signed-byte pair, null-link/resource and post-handler next-entry mutation model')
    else:
        wanted = [] if fixture['null'] else [CHECKERS[name]] + ([] if fixture['result'] else [0x0204532c])
        if [call['address'] for call in calls] != wanted:
            failures.append('Independent null/success/failure provider sequence')
        if registers[0] != (VALUE if not fixture['null'] and fixture['result'] else 0):
            failures.append('Independent preserved input pointer versus predicate result/null return')
        if bytes(vm.mem_read(TAG, 1)) != bytes([expected_tag]):
            failures.append('Independent prescribed global-byte callback effects')
    for location, region in expected.items():
        if bytes(vm.mem_read(location, len(region))) != region:
            failures.append('Independent complete pointer/entry/link region: ' + hex(location))
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
