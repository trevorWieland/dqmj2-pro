import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {'02038d88': 8, '02038dec': 12, '02038e50': 16, '02038eb4': 20, '02038f18': 36, '02038f7c': 24, '02038fe0': 32}
SP, STOP, SLOT, MANAGER, BLOB = 0x027f0000, 0x027e0000, 0x020f4c44, 0x02400000, 0x02401000


def fixtures(name):
    return [dict(index=index, count=count, table=table, empty=empty)
            for index in [-2147483648, -1, 0, 1, 3, 4, 16, 17, 2147483647]
            for count in [0, 1, 4, 17] for table in [False, True] for empty in [False, True]]


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    field = SPECS[name]
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    manager = bytearray((i * 17 + ordinal) & 255 for i in range(160))
    struct.pack_into('<I', manager, 140, BLOB)
    blob = bytearray((i * 23 + ordinal) & 255 for i in range(8192))
    for n, offset in enumerate(sorted(set(SPECS.values()))):
        table = 0x100 + n * 0x80
        count = fixture['count'] if offset == field else 19
        struct.pack_into('<I', blob, offset, 0 if offset == field and not fixture['table'] else table)
        struct.pack_into('<I', blob, table, count)
        for item in range(24):
            value = 0 if offset == field and fixture['empty'] else 0x1000 + n * 0x100 + item * 4
            struct.pack_into('<I', blob, table + 4 + item * 4, value)
    vm.mem_write(SLOT, struct.pack('<I', MANAGER))
    vm.mem_write(MANAGER, bytes(manager))
    vm.mem_write(BLOB, bytes(blob))
    vm.mem_write(SP - 256, bytes((i * 31 + ordinal) & 255 for i in range(512)))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    initial[0] = fixture['index'] & 0xffffffff
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal % 16 << 28 | 0x10)
    for register, word in zip(C.REGISTERS, initial):
        vm.reg_write(register, word)
    writes, pcs, failures = [], [], []
    returned = False

    def memory(uc, access, location, size, value, user):
        writes.append(dict(address=location, size=size, value=value))

    def code(uc, location, size, user):
        nonlocal returned
        pcs.append(location)
        if location == STOP:
            returned = True
            uc.emu_stop()
        elif not address <= location < address + len(body):
            raise ValueError(('Native callee/body execution forbidden for leaf lookup', hex(location)))

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=100)
    if not returned:
        raise ValueError('Actual leaf lookup did not return')
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    result = 0
    if fixture['table'] and 0 <= fixture['index'] < fixture['count'] and not fixture['empty']:
        n = sorted(set(SPECS.values())).index(field)
        result = BLOB + 0x1000 + n * 0x100 + fixture['index'] * 4
    if registers[0] != result or writes:
        failures.append('Independent optional-table/record/signed-index/unsigned-count/relative-base result and read-only behavior')
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Actual lookup callee-saved registers/SP differ')
    for location, region in [(MANAGER, manager), (BLOB, blob), (SLOT, struct.pack('<I', MANAGER))]:
        if bytes(vm.mem_read(location, len(region))) != region:
            failures.append('Independent complete unchanged manager/blob/global state')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=[], writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
