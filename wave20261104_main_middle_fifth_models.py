import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {'02049af0': {}, '02049be4': {}}
SP, STOP, ENTRY, LINK, TABLE0, TABLE1 = 0x027f0000, 0x027e0000, 0x02400000, 0x02401000, 0x021029c8, 0x021029d0


def fixtures(name):
    if name == '02049af0':
        return [dict(previous=[0, 1, 4, 5, 0, 1, 4, 5][n], current=[1, 0, 5, 4, 5, 4, 1, 0][n],
                     enabled=[0, 1, 1, 1, 0, 1, 0, 1][n], include4=n % 2, ordinal=n) for n in range(8)]
    return [dict(font=[0, 1, 7, 2, 128, 255, 0xffffffff, 3][n], present=n in [0, 2, 3, 7], ordinal=n,
                 field4=0x12345678 ^ n, field5=0x87654321 ^ n,
                 stackWords=[0xa5a5ff00 | n, 0xffff0080 | n, 0x123400ff ^ n, 0xdeadbe00 | n,
                             0x89abcdef ^ n, [0x80, 0xff, 0x7f, 0, 1, 0xffffff80, 0xfffffffe, 0xa5a5ff80][n], 0xfedcba98 ^ n])
            for n in range(8)]


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    entry = bytearray((i * 17 + ordinal) & 255 for i in range(32))
    link = bytearray((i * 29 + ordinal) & 255 for i in range(32))
    tables = bytearray([0, 1, 127, 128, 255, 2, 3, 254, 255, 128, 127, 1, 0, 254, 3, 2])
    vm.mem_write(ENTRY, bytes(entry))
    vm.mem_write(LINK, bytes(link))
    vm.mem_write(TABLE0, bytes(tables))
    expected_entry, expected_link, expected_tables = bytearray(entry), bytearray(link), bytearray(tables)
    vm.mem_write(SP - 256, bytes((i * 23 + ordinal) & 255 for i in range(512)))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    block = None
    first_words = [0x12340000 + ordinal, 0x23450000 + ordinal, 0x34560000 + ordinal]
    initial_block = [0x45670000 + ordinal, 1 - fixture.get('enabled', 0), 1 - fixture.get('include4', 0), 0x56780000 + ordinal]
    if name == '02049af0':
        initial[:4] = first_words + [initial_block[0]]
        vm.mem_write(SP, struct.pack('<3I', *initial_block[1:]))
    else:
        initial[:4] = [ENTRY, fixture['font'], fixture['field4'], fixture['field5']]
        vm.mem_write(SP, struct.pack('<7I', *fixture['stackWords']))
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal << 28 | 0x10)
    for register, word in zip(C.REGISTERS, initial):
        vm.reg_write(register, word)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function'}
    calls, writes, pcs, failures = [], [], [], []
    returned = False
    getter_count = 0
    block_pointer = None
    snapshot_enabled = fixture.get('enabled', 0)

    def put(location, data):
        vm.mem_write(location, data)
        writes.append(dict(provider=True, address=location, hex=data.hex()))

    def memory(uc, access, location, size, word, user):
        writes.append(dict(provider=False, address=location, size=size, value=word))

    def code(uc, location, size, user):
        nonlocal returned, getter_count, block_pointer, block
        pcs.append(location)
        if location == STOP:
            returned = True
            uc.emu_stop()
        elif location in imports:
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('Qualified ARM provider entered as Thumb')
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            call = dict(symbol=imports[location], address=location, words=args)
            calls.append(call)
            result = 0xdead0000 + ordinal
            if name == '02049af0':
                if location == 0x02048f7c:
                    if args[0] != 1 or getter_count >= 2:
                        raise ValueError('Unexpected aggregate getter protocol')
                    result = fixture['previous'] if getter_count == 0 else fixture['current']
                    getter_count += 1
                elif location == 0x02049c90:
                    block_pointer = args[1]
                    if args[:3] != [fixture['current'], SP - 4, initial_block[3]]:
                        raise ValueError('Genuine by-value R3/stack aggregate boundary differs')
                    call['inputBlock'] = bytes(uc.mem_read(block_pointer, 16)).hex()
                    if call['inputBlock'] != struct.pack('<4I', *initial_block).hex():
                        failures.append('Independent complete initial16-byte aggregate copy')
                    block = [0x67890000 + ordinal, 1 - fixture['enabled'], 1 - fixture['include4'], 0x789a0000 + ordinal]
                    put(block_pointer, struct.pack('<4I', *block))
                elif location == 0x02049e28:
                    if args[:3] != first_words or block_pointer is None:
                        failures.append('Independent first-three-word preservation after opaque calls')
                    block = [0xabcdef00 + ordinal, fixture['enabled'], fixture['include4'], 0x9abc0000 + ordinal]
                    put(block_pointer, struct.pack('<4I', *block))
                elif location == 0x020414c8:
                    mask = (~(1 << fixture['previous'])) & 63
                    if not fixture['include4']:
                        mask &= ~16
                    if args[0] != mask:
                        failures.append('Independent first-getter mask and late include4 word')
                    block[1], block[2] = 0, 1 - fixture['include4']
                    put(block_pointer, struct.pack('<4I', *block))
                elif location == 0x02041538:
                    if args[:3] != [1, 2, 4]:
                        failures.append('Independent conditional controller constant triple')
                elif location == 0x0204157c:
                    if args[0] != 10:
                        failures.append('Independent final controller constant')
                    block[0] ^= 0x55555555
                    put(block_pointer, struct.pack('<4I', *block))
                else:
                    raise ValueError('Unexpected by-value aggregate provider')
            else:
                if location == 0x0205fe20:
                    signed_font = fixture['font'] & 255
                    if signed_font >= 128:
                        signed_font -= 256
                    if args[0] != signed_font & 0xffffffff:
                        failures.append('Independent low-byte signed font lookup argument')
                    expected_link[0] = 0x80 + ordinal
                    put(LINK, bytes([expected_link[0]]))
                    if fixture['font'] < 8:
                        index = fixture['font']
                        expected_tables[index], expected_tables[index + 8] = 0x80 + ordinal, 255 - ordinal
                        put(TABLE0 + index, bytes([expected_tables[index]]))
                        put(TABLE1 + index, bytes([expected_tables[index + 8]]))
                    result = LINK if fixture['present'] else 0
                    if fixture['present']:
                        expected_entry[6] = expected_link[0]
                elif location == 0x0205fe74:
                    font = fixture['font']
                    if args != [LINK, font, expected_tables[font], expected_tables[font + 8]]:
                        failures.append('Independent preserved font and late unsigned table-byte arguments')
                    stack = list(struct.unpack('<7I', bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP), 28))))
                    call['stackWords'] = stack
                    raw = fixture['stackWords']
                    signed_byte = raw[5] & 255
                    if signed_byte >= 128:
                        signed_byte -= 256
                    wanted = [word & 255 for word in raw[:4]] + [raw[4], signed_byte & 0xffffffff, raw[6]]
                    if stack != wanted:
                        failures.append('Independent eleven-argument unsigned/signed-byte/full-word stack forwarding')
                    if bytes(uc.mem_read(ENTRY + 6, 1)) != bytes([expected_link[0]]):
                        failures.append('Independent pre-provider signed first-byte snapshot into entry+6')
                    expected_entry[6], expected_link[0] = 0xab, 0xcd
                    put(ENTRY + 6, b'\xab')
                    put(LINK, b'\xcd')
                    struct.pack_into('<I', expected_entry, 0, LINK)
                    expected_entry[4], expected_entry[5] = fixture['field4'] & 255, fixture['field5'] & 255
                else:
                    raise ValueError('Unexpected eleven-argument provider')
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
    vm.emu_start(address, STOP + 4, count=2500)
    if not returned:
        raise ValueError('Actual caller failed to return')
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Callee-saved registers/SP differ')
    if name == '02049af0':
        wanted = [0x02048f7c, 0x02048f7c, 0x02049c90, 0x02049e28] + ([0x020414c8, 0x02041538, 0x0204157c] if snapshot_enabled else [])
        if registers[0] != block[0] or bytes(vm.mem_read(block_pointer, 16)) != struct.pack('<4I', *block):
            failures.append('Independent complete escaped aggregate and late output-word return')
    else:
        wanted = [0x0205fe20] + ([0x0205fe74] if fixture['present'] else [])
        if registers[0] != int(fixture['present']):
            failures.append('Independent NULL/present result')
    if [call['address'] for call in calls] != wanted:
        failures.append('Independent complete ordered provider sequence')
    for location, expected in [(ENTRY, expected_entry), (LINK, expected_link), (TABLE0, expected_tables)]:
        if bytes(vm.mem_read(location, len(expected))) != expected:
            failures.append('Independent complete entry/link/table region: ' + hex(location))
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
