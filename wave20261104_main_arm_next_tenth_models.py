import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {'02039fa4': {}, '0203a000': {}, '0203a050': {}, '0203a01c': {}, '02039fc4': {}}
SP, STOP, HANDLE, PLAYER0, PLAYER1 = 0x027f0000, 0x027e0000, 0x02400000, 0x02401000, 0x02402000


def fixtures(name):
    if name == '02039fc4':
        return [dict(provided=provided, first_result=result, value=value, extra=value ^ 0x87654321, flags=7, reassign=False)
                for provided in [False, True] for result in [0, 1, 0x80000000, 0xffffffff]
                for value in [0, 1, 0x80000001, 0xffffffff]]
    flags = range(16) if name in ['02039fa4', '0203a01c'] else [3]
    values = [0] if name == '02039fa4' else [0, 1, 0x80000001, 0xffffffff]
    return [dict(provided=provided, flags=flag, value=value, extra=value ^ 0x87654321, reassign=reassign)
            for flag in flags for value in values for provided in [False, True] for reassign in [False, True]]


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    handle = bytearray((i * 13 + ordinal) & 255 for i in range(32))
    struct.pack_into('<I', handle, 0, PLAYER0 if fixture['provided'] else 0)
    players = {location: bytearray((i * 17 + ordinal + n) & 255 for i in range(0x180)) for n, location in enumerate([PLAYER0, PLAYER1])}
    for n, player in enumerate(players.values()):
        struct.pack_into('<I', player, 0x110, (0xa5a50000 + n * 0x100) | fixture['flags'])
    expected = {HANDLE: bytearray(handle), **{k: bytearray(v) for k, v in players.items()}}
    for location, region in expected.items():
        vm.mem_write(location, bytes(region))
    vm.mem_write(SP - 256, bytes((i * 31 + ordinal) & 255 for i in range(512)))
    value, extra = fixture['value'], fixture['extra']
    fourth = (0xf00d0000 + ordinal) & 0xffffffff
    fifth = (0x89ab0000 + ordinal) & 0xffffffff
    vm.mem_write(SP, struct.pack('<I', fifth))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    initial[:4] = [HANDLE, value, extra, fourth]
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal % 16 << 28 | 0x10)
    for register, word in zip(C.REGISTERS, initial):
        vm.reg_write(register, word)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function'}
    calls, writes, pcs, failures, actions = [], [], [], [], []
    returned = False
    handle_reads = 0
    result = None
    selected = PLAYER1 if fixture['reassign'] else PLAYER0
    if name != '02039fc4' and fixture['provided'] and fixture['reassign']:
        struct.pack_into('<I', expected[HANDLE], 0, PLAYER1)

    def action(location, args, returned_word, mutations):
        actions.append(dict(address=location, args=args, returned=returned_word, mutations=mutations))
        for at, data in mutations:
            for base, region in expected.items():
                if base <= at and at + len(data) <= base + len(region):
                    region[at - base:at - base + len(data)] = data
                    break

    if name == '02039fc4':
        action(0x02039f2c, [HANDLE, value, extra, fourth, fifth], fixture['first_result'], [(HANDLE, struct.pack('<I', PLAYER1))])
        result = int(bool(fixture['first_result']))
        if result:
            action(0x02039fa4, [HANDLE], 0x80000000, [(PLAYER1 + 0x110, struct.pack('<I', 0x12340000 + ordinal))])
    elif fixture['provided']:
        if name == '02039fa4':
            flag = struct.unpack_from('<I', expected[selected], 0x110)[0]
            struct.pack_into('<I', expected[selected], 0x110, flag | 4)
        elif name in ['0203a000', '0203a050']:
            args = [selected, value] + ([extra] if name == '0203a050' else [])
            action(0x0203a4fc if name == '0203a000' else 0x0203b8dc, args, 0x80000000 + ordinal,
                   [(HANDLE, struct.pack('<I', PLAYER0)), (selected + 0x160, struct.pack('<I', 0xdead0000 + ordinal))])
        elif not fixture['flags'] & 8:
            action(0x020379c4, [selected + 0xe8, (value << 8) & 0xffffffff, extra], 0xffffffff,
                   [(selected + 0xe8, struct.pack('<4I', 0x100 + ordinal, 0x200 + ordinal, 0x300 + ordinal, 0x400 + ordinal))])

    def memory_write(uc, access, location, size, word, user):
        writes.append(dict(provider=False, address=location, size=size, value=word))

    def memory_read(uc, access, location, size, word, user):
        nonlocal handle_reads
        if location == HANDLE and size == 4:
            handle_reads += 1
            if name != '02039fc4' and fixture['provided'] and fixture['reassign'] and handle_reads == 2:
                uc.mem_write(HANDLE, struct.pack('<I', PLAYER1))
                writes.append(dict(environment=True, address=HANDLE, hex=struct.pack('<I', PLAYER1).hex()))

    def code(uc, location, size, user):
        nonlocal returned
        pcs.append(location)
        if location == STOP:
            returned = True
            uc.emu_stop()
            return
        if location in imports:
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('Measured handle provider entered as Thumb')
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            stack = uc.reg_read(R.UC_ARM_REG_SP)
            stackword = struct.unpack('<I', bytes(uc.mem_read(stack, 4)))[0]
            n = len(calls)
            calls.append(dict(address=location, symbol=imports[location], words=args, stackWord=stackword, stack=stack))
            current = actions[n] if n < len(actions) else dict(address=0, args=[], returned=0, mutations=[])
            if location != current['address'] or (args + [stackword])[:len(current['args'])] != current['args']:
                failures.append('Independent handle reload/extra live argument/frame shift/fifth stack word ABI')
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
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory_write)
    vm.hook_add(unicorn.UC_HOOK_MEM_READ, memory_read)
    vm.emu_start(address, STOP + 4, count=300)
    if not returned:
        raise ValueError('Actual handle caller did not return')
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Actual handle caller callee-saved registers/SP differ')
    wanted_reads = 0 if name == '02039fc4' else 2 if fixture['provided'] else 1
    if handle_reads != wanted_reads or len(calls) != len(actions) or result is not None and registers[0] != result:
        failures.append('Independent two-load guard/access contract/provider sequence/literal result')
    for location, region in expected.items():
        if bytes(vm.mem_read(location, len(region))) != region:
            failures.append('Independent complete handle and both possible player states/flags/timer')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                handleReads=handle_reads, ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
