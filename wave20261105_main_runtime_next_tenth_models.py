import itertools
import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {name: {} for name in ['02060adc', '02060c1c', '02060c60', '02060cb4', '02067754']}
SP, STOP, STATE, SLOTS = 0x027f0000, 0x027e0000, 0x021c3708, 0x021c3768


def fixtures(name):
    if name == '02060adc':
        return [dict(value=low | high) for low, high in itertools.product(range(256), [0, 0x12345600, 0xffffff00])]
    if name in ['02060c1c', '02060cb4']:
        return [dict(kind=k, alternate=a, selected=k if equal else 7) for k, a, equal in itertools.product([0, 1, 2, 7, 0x80000000, 0xffffffff], [0, 1, 0x80000000], [False, True])]
    if name == '02060c60':
        return [dict(x=x, y=y, sx=x if equalx else 7, sy=y if equaly else 9) for x, y, equalx, equaly in itertools.product([0, 1, 2, 0xffffffff], [0, 1, 9, 0x80000000], [False, True], [False, True])]
    return [dict(seed=seed, mutate=mutate, nulls=nulls) for seed, mutate, nulls in itertools.product(range(3), [False, True], [False, True])]


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    allocation = name == '02067754'
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    if allocation:
        vm.mem_map(0x02000000, 0x800000)
        vm.mem_write(0x02000000, main)
    else:
        vm.mem_map(address & ~0xfff, 0x1000)
        vm.mem_map(SP - 0x1000, 0x2000)
        vm.mem_map(STOP, 0x1000)
    vm.mem_write(address, body)
    words = [0x11223344, 0x89abcdef, 0x76543210, 0xdeadbeef]
    calls_expected, stores_expected, result, expected = [], [], None, None
    if allocation:
        base = STATE - 16
        expected = bytearray((i * 43 + ordinal * 17 + 0x35) & 255 for i in range(164))
        vm.mem_write(base, bytes(expected))
        sizes = [0x1100] + [0x5c0] * 9 + [0x440]
        destinations = [STATE + 8] + [SLOTS + i * 4 for i in range(9)] + [STATE + 28]
        for i, (size, destination) in enumerate(zip(sizes, destinations)):
            returned = 0 if fixture['nulls'] and i % 3 == 1 else 0x02400000 + fixture['seed'] * 0x10000 + i * 0x1200
            action = dict(args=[7, size, 4], returned=returned)
            if fixture['mutate']:
                expected[:] = bytes((j * 29 + i * 19 + fixture['seed']) & 255 for j in range(len(expected)))
                action['mutation'] = bytes(expected)
            calls_expected.append(action)
            struct.pack_into('<I', expected, destination - base, returned)
            stores_expected.append(dict(address=destination, size=4, value=returned))
    elif name == '02060adc':
        words[0] = fixture['value']
        low = fixture['value'] & 255
        result = (low if low < 128 else low - 256) & 0xffffffff
    elif name in ['02060c1c', '02060cb4']:
        kind, alternate, selected = [fixture[k] for k in ['kind', 'alternate', 'selected']]
        words[:3] = [kind, alternate, selected]
        result = 3 if alternate else 0
        if kind:
            result += 2 if kind == selected else 1
    else:
        x, y, sx, sy = [fixture[k] for k in ['x', 'y', 'sx', 'sy']]
        words = [x, y, sx, sy]
        category = 2 if y == sy else 0 if y == 0 else 1
        result = category * 3 + (0 if not x else 2 if x == sx else 1)
    vm.mem_write(SP - 256, bytes((i * 31 + ordinal * 7) & 255 for i in range(512)))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    initial[:4] = words
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal % 16 << 28 | 0x10)
    for reg, value in zip(C.REGISTERS, initial):
        vm.reg_write(reg, value)
    imports = {int(v['address'], 0): (k, v) for k, v in row['nativeSymbolEntries'].items() if v['kind'] == 'function'}
    calls, writes, pcs, failures, stores = [], [], [], [], []
    returned = False

    def memory(uc, access, location, size, value, user):
        writes.append(dict(provider=False, address=location, size=size, value=value))
        if allocation and STATE - 16 <= location < STATE - 16 + len(expected):
            stores.append(dict(address=location, size=size, value=value))

    def code(uc, location, size, user):
        nonlocal returned
        pcs.append(location)
        if location == STOP:
            returned = True
            uc.emu_stop()
            return
        if location in imports:
            symbol, binding = imports[location]
            n = len(calls)
            action = calls_expected[n] if n < len(calls_expected) else dict(args=[], returned=0)
            args = [uc.reg_read(reg) for reg in C.REGISTERS[:4]]
            calls.append(dict(symbol=symbol, address=location, words=args, program=binding.get('program') or '', processor=binding['processor'], module=binding['module'], mode=binding['mode']))
            if location != 0x0202a37c or args[:3] != action['args'] or uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                failures.append('Independent11 ARM allocation requests: tag7, ordered sizes, alignment4')
            if 'mutation' in action:
                uc.mem_write(STATE - 16, action['mutation'])
                writes.append(dict(provider=True, address=STATE - 16, hex=action['mutation'].hex()))
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, reg in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(reg, 0xcafe0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, action['returned'])
            uc.reg_write(R.UC_ARM_REG_CPSR, (ordinal + len(calls)) % 16 << 28 | 0x10)
            uc.reg_write(R.UC_ARM_REG_PC, lr)
        elif not address <= location < address + len(body):
            raise ValueError(('No native allocation/SDK/game body execution authorized', hex(location)))

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=2000)
    if not returned:
        raise ValueError('Actual integer/allocation caller did not return')
    registers = [vm.reg_read(reg) for reg in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Actual ARM callee-saved registers/SP differ')
    if result is not None and registers[0] != result:
        failures.append('Independent signed-byte projection/unsigned classification result')
    if len(calls) != len(calls_expected):
        failures.append('Independent allocation provider count')
    if allocation:
        if stores != stores_expected or bytes(vm.mem_read(STATE - 16, len(expected))) != expected:
            failures.append('Independent complete ordered pointer stores, padding and provider mutation persistence')
        memory_sha = C.sha(bytes(vm.mem_read(0x02000000, 0x800000)))
    else:
        memory_sha = C.sha(bytes(vm.mem_read(address & ~0xfff, 0x1000)) + bytes(vm.mem_read(SP - 0x1000, 0x2000)) + bytes(vm.mem_read(STOP, 0x1000)))
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                mappedRamSha256=memory_sha, modelFailures=failures, actualTopReturn=True)
