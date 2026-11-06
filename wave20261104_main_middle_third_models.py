import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {name: {} for name in ['0204b380', '0204b4f4', '0204b5b0', '0204b74c', '0204b82c']}
SP, STOP, STATE, POINT, GROUP, CHILDREN, TABLE = 0x027f0000, 0x027e0000, 0x02400000, 0x02401000, 0x02402000, 0x02410000, 0x02420000


def fixtures(name):
    return [dict(ordinal=n, enabled=[0, 1, 0xffffffff, 0x80000000, 1, 0, 2, 1][n], present=n % 4 != 3,
                 predicate=[0, 0, 1, 1, 1, 0, 1, 1][n], step=[0, 1, 8, 0xffffffff, 0x80000000, 32, 0x7fffffff, 63][n],
                 x=[-32768, -1, 0, 1, 32767, 16, -100, 12345][n], y=[32767, 1, -1, 0, -32768, -16, 100, -12345][n],
                 stackByteWord=[0, 1, 255, 256, 511, 0x80000000, 0xffffffff, 0xa5a5ff80][n],
                 row=n // 3, column=n % 3, nullEntry=n % 3 == 0) for n in range(8)]


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    state = bytearray((i * 17 + ordinal) & 255 for i in range(128))
    point = bytearray((i * 29 + ordinal) & 255 for i in range(16))
    children = bytearray((i * 13 + ordinal) & 255 for i in range(0x600))
    table = bytearray(struct.pack('<16I', *[0x02500000 + 0x100 * i + ordinal for i in range(16)]))
    struct.pack_into('<hh', state, 20, fixture['x'], fixture['y'])
    struct.pack_into('<hh', point, 0, fixture['y'], fixture['x'])
    struct.pack_into('<I', state, 28, GROUP if fixture['present'] else 0)
    struct.pack_into('<I', state, 44, 0x12345678 ^ ordinal)
    selected = fixture['row'] * 3 + fixture['column']
    if fixture['nullEntry']:
        struct.pack_into('<I', table, 4 * selected, 0)
    initial_flags = [0xa5a50000 ^ (ordinal * 17 + index * 7) for index in range(3)]
    for index, flags in enumerate(initial_flags):
        struct.pack_into('<I', children, index * 0x200 + 0x7c, flags)
    regions = [(STATE, state), (POINT, point), (CHILDREN, children), (TABLE, table)]
    for location, data in regions:
        vm.mem_write(location, bytes(data))
    expected = {location: bytearray(data) for location, data in regions}
    vm.mem_write(SP - 256, bytes((i * 23 + ordinal) & 255 for i in range(512)))
    argument3, argument4 = 0x12345678 ^ ordinal, 0x89abcdef ^ ordinal
    vm.mem_write(SP, struct.pack('<II', argument4, fixture['stackByteWord']))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    initial[:4] = [STATE, fixture['enabled'], 0xdeadbeef, argument3]
    if name == '0204b4f4':
        initial[:4] = [STATE, POINT, fixture['step'], argument3]
    elif name in ['0204b5b0', '0204b74c']:
        initial[:2] = [STATE, fixture['step']]
    elif name == '0204b82c':
        initial[:3] = [fixture['row'], fixture['column'], TABLE]
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal << 28 | 0x10)
    for register, value in zip(C.REGISTERS, initial):
        vm.reg_write(register, value)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function'}
    calls, writes, pcs, failures = [], [], [], []
    returned = False

    def expected_word(location, offset):
        return struct.unpack_from('<I', expected[location], offset)[0]

    def predict(location, data):
        for base, region in expected.items():
            if base <= location and location + len(data) <= base + len(region):
                region[location - base:location - base + len(data)] = data
                return
        raise ValueError('Independent region prediction escaped')

    def put(location, data):
        vm.mem_write(location, data)
        predict(location, data)
        writes.append(dict(provider=True, address=location, hex=data.hex()))

    def memory(uc, access, location, size, value, user):
        writes.append(dict(provider=False, address=location, size=size, value=value))

    def code(uc, location, size, user):
        nonlocal returned
        pcs.append(location)
        if location == STOP:
            returned = True
            uc.emu_stop()
        elif location in imports:
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('Qualified ARM provider entered as Thumb')
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            stack = bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP), 8))
            call = dict(symbol=imports[location], address=location, words=args, stack=stack.hex())
            calls.append(call)
            result = 0xdead0000 + ordinal
            if name == '0204b380':
                if location == 0x0205f98c:
                    index = len(calls) - 1
                    if index > 2:
                        raise ValueError('Unbounded unexpected child provider sequence')
                    if args[:2] != [expected_word(STATE, 28), index]:
                        failures.append('Independent repeated group reload and child-index protocol')
                    result = CHILDREN + index * 0x200
                    flags = initial_flags[index] ^ 0x80000000
                    put(result + 0x7c, struct.pack('<I', flags))
                    if index < 2 or not fixture['enabled']:
                        predict(result + 0x7c, struct.pack('<I', flags | 2 if fixture['enabled'] else flags & 0xfffffffd))
                    if index == 0 and ordinal % 2:
                        put(STATE + 28, struct.pack('<I', GROUP + 0x40))
                elif location == 0x0204b4b8:
                    if args[0] != STATE or not fixture['enabled']:
                        failures.append('Independent conditional final-child predicate argument')
                    flags = initial_flags[2] ^ 0xc0000004
                    put(CHILDREN + 0x400 + 0x7c, struct.pack('<I', flags))
                    result = fixture['predicate']
                    if result:
                        predict(CHILDREN + 0x400 + 0x7c, struct.pack('<I', flags | 2))
                else:
                    raise ValueError('Unexpected flag-state provider')
            elif name == '0204b4f4':
                if location == 0x0204b1c4:
                    if args != [STATE, 0, POINT, argument3] or list(struct.unpack('<II', stack)) != [argument4, fixture['stackByteWord'] & 255]:
                        failures.append('Independent six-argument ABI, zero flag and byte stack forwarding')
                    put(STATE + 44, struct.pack('<I', 0xcafe0000 + ordinal))
                    put(POINT, struct.pack('<hh', 123, -456))
                elif location == 0x0204b53c:
                    if args[:2] != [STATE, POINT] or struct.unpack('<I', bytes(uc.mem_read(STATE + 44, 4)))[0] != fixture['step'] or bytes(uc.mem_read(POINT, 4)) != expected[POINT][:4]:
                        failures.append('Independent post-constructor state overwrite and original point forwarding')
                    predict(STATE + 44, struct.pack('<I', fixture['step']))
                    put(STATE, struct.pack('<I', 0xabcdef00 + ordinal))
                    put(STATE + 44, struct.pack('<I', fixture['step'] ^ 0x55555555))
                else:
                    raise ValueError('Unexpected six-argument wrapper provider')
            elif name in ['0204b5b0', '0204b74c']:
                target = 0x0204b53c if name == '0204b5b0' else 0x0204b6dc
                if location != target or args[0] != STATE or not SP - 128 <= args[1] < SP:
                    raise ValueError('Unexpected stack-point provider boundary')
                payload = bytes(uc.mem_read(args[1], 4))
                call['pointPayload'] = payload.hex()
                if payload != struct.pack('<hh', fixture['x'], fixture['y']) or struct.unpack('<I', bytes(uc.mem_read(STATE + 44, 4)))[0] != fixture['step']:
                    failures.append('Independent signed-halfword stack snapshot and pre-call step store')
                predict(STATE + 44, struct.pack('<I', fixture['step']))
                put(STATE + 20, struct.pack('<hh', 99, -100))
                put(STATE + 44, struct.pack('<I', fixture['step'] ^ 0x33333333))
                uc.mem_write(args[1], struct.pack('<hh', 77, -88))
                writes.append(dict(provider=True, address=args[1], hex=struct.pack('<hh', 77, -88).hex()))
            else:
                pointer = struct.unpack_from('<I', table, 4 * selected)[0]
                if location != 0x0202a498 or args[:2] != [2, pointer]:
                    failures.append('Independent allocator tag and original selected pointer forwarding')
                put(TABLE + selected * 4, struct.pack('<I', 0xdeadbeef))
                put(TABLE + (selected + 1) * 4, struct.pack('<I', 0xcafebabe))
                predict(TABLE + selected * 4, bytes(4))
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, register in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xcafe0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, result)
            uc.reg_write(R.UC_ARM_REG_CPSR, ((ordinal + 7) % 16) << 28 | 0x10)
            uc.reg_write(R.UC_ARM_REG_PC, lr)
        elif not address <= location < address + len(body):
            raise ValueError(('Unmodeled native callee/body execution forbidden', hex(location)))

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=1500)
    if not returned:
        raise ValueError('Actual caller failed to return')
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Callee-saved registers/SP differ')
    targets = [call['address'] for call in calls]
    if name == '0204b380':
        wanted = ([0x0205f98c] * 3 + ([0x0204b4b8] if fixture['enabled'] else [])) if fixture['present'] else []
    elif name == '0204b4f4':
        wanted = [0x0204b1c4, 0x0204b53c]
    elif name in ['0204b5b0', '0204b74c']:
        wanted = [0x0204b53c if name == '0204b5b0' else 0x0204b6dc]
    else:
        wanted = [] if fixture['nullEntry'] else [0x0202a498]
    if targets != wanted:
        failures.append('Independent complete ordered provider sequence')
    for location, region in expected.items():
        if bytes(vm.mem_read(location, len(region))) != region:
            failures.append('Independent complete modeled region: ' + hex(location))
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
