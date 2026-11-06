import itertools
import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {name: {} for name in ['02060b84', '020640f0', '02064304', '020656f0']}
SP, STOP, INPUT = 0x027f0000, 0x027e0000, 0x02400000
PARTY, POINTS, FLAG, RECORDS = 0x021bd524, 0x021b9e94, 0x021c2870, 0x021c2871


def fixtures(name):
    if name == '02060b84':
        return [dict(kind=k, alternate=a, selected=k if same else s) for k, a, same, s in itertools.product([0, 1, 2, 3, 9, 0x80000000, 0xffffffff], [0, 1, 0x80000000], [False, True], [0, 7])]
    if name == '020640f0':
        sets = [[0, 0, 1, 2, 3, 4], [1, 1, 2, 3, 4, 5], [1, 2, 3, 1, 4, 5], [0, 0, 0, 0, 0, 0],
                [8, 1, 2, 3, 4, 8], [8, 8, 0, 0, 0, 0], [1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5],
                [2, 3, 4, 5, 6, 7], [7, 6, 5, 4, 3, 2], [1, 2, 1, 3, 4, 5], [0, 8, 0, 8, 0, 8]]
        return [dict(categories=c, include=i, mutate=m) for c, i, m in itertools.product(sets, [0, 1, 2, 0xffffffff], [False, True])]
    if name == '02064304':
        return [dict(source=source, seed=seed) for source, seed in itertools.product(['separate', 'same', 'before2', 'before4', 'after2', 'after4'], range(8))]
    return [dict(seed=n) for n in range(16)]


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    expected, calls_expected, result = {}, [], None
    words = [0x11223344, 0x89abcdef, 0x76543210, 0xdeadbeef]

    def region(base, size):
        raw = bytearray((i * 37 + ordinal * 17 + 0x43) & 255 for i in range(size))
        vm.mem_write(base, bytes(raw))
        expected[base] = raw
        return raw

    if name == '02060b84':
        kind, alternate, selected = [fixture[k] for k in ['kind', 'alternate', 'selected']]
        words[:3] = [kind, alternate, selected]
        if kind == 0:
            result = 4 if alternate == 0 else 7
        elif kind == 1:
            result = 0 if alternate == 0 else 2
        elif kind == 2:
            result = 1 if alternate == 0 else 3
        elif kind == selected:
            result = 6 if alternate == 0 else 9
        else:
            result = 5 if alternate == 0 else 8
    elif name == '02064304':
        base = POINTS - 16
        raw = region(base, 80)
        for i in range(0, len(raw), 2):
            struct.pack_into('<H', raw, i, (i * 0x719 + fixture['seed'] * 0x101 + 0x2a39) & 65535)
        vm.mem_write(base, bytes(raw))
        source = INPUT if fixture['source'] == 'separate' else POINTS + 20 + {'same': 0, 'before2': -2, 'before4': -4, 'after2': 2, 'after4': 4}[fixture['source']]
        if source == INPUT:
            separate = region(INPUT, 12)
            source_region, source_offset = separate, 0
        else:
            source_region, source_offset = raw, source - base
        words[0] = source
        for i in range(3):
            pair = bytes(source_region[source_offset + i * 4:source_offset + i * 4 + 4])
            raw[POINTS + 20 - base + i * 4:POINTS + 24 - base + i * 4] = pair
    elif name == '020656f0':
        raw = region(FLAG - 8, 8 + 1 + 324 + 8)
        raw[8] = 0
        for i in range(36):
            raw[9 + i * 9] = i
            raw[11 + i * 9] = 0
    else:
        raw = region(PARTY - 8, 0x44)
        ids = [ordinal * 100 + n + 1 for n in range(6)]
        for n, value in enumerate(ids):
            struct.pack_into('<I', raw, 8 + 28 + n * 4, value)
        vm.mem_write(PARTY - 8, bytes(raw))
        words[0] = fixture['include']
        length = 6 if fixture['include'] else 3
        counts = [0] * 9
        calls_expected.append(dict(address=0x02008d78, args=None, returnWord=0, fill=True))
        for n in range(length):
            category = fixture['categories'][n]
            calls_expected.append(dict(address=0x020640b4, args=[ids[n]], returnWord=category, fill=False))
            counts[category] += 1
            if fixture['mutate']:
                ids = [(value + 0x101 + n) & 0xffffffff for value in ids]
                for j, value in enumerate(ids):
                    struct.pack_into('<I', raw, 8 + 28 + j * 4, value)
                calls_expected[-1]['mutation'] = bytes(raw)
        result = int(any(value > 1 for value in counts[1:]))

    vm.mem_write(SP - 256, bytes((i * 31 + ordinal * 7) & 255 for i in range(512)))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    initial[:4] = words
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal % 16 << 28 | 0x10)
    for reg, value in zip(C.REGISTERS, initial):
        vm.reg_write(reg, value)
    imports = {int(v['address'], 0): (k, v) for k, v in row['nativeSymbolEntries'].items() if v['kind'] == 'function'}
    calls, writes, pcs, failures = [], [], [], []
    returned = False

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
            args = [uc.reg_read(reg) for reg in C.REGISTERS[:4]]
            n = len(calls)
            action = calls_expected[n] if n < len(calls_expected) else dict(address=0, args=[], returnWord=0)
            calls.append(dict(address=location, symbol=symbol, words=args, program=binding.get('program') or '', processor=binding['processor'], module=binding['module'], mode=binding['mode']))
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32 or location != action['address']:
                failures.append('Independent exact main ARM provider order/mode')
            if action.get('fill'):
                if args[0] != SP - 32 or args[1:3] != [0, 9]:
                    failures.append('Independent exact9-byte stack buffer initialization arguments')
                if args[2] > 64:
                    raise ValueError('Unbounded invalid fill argument')
                raw = bytes([args[1] & 255]) * args[2]
                uc.mem_write(args[0], raw)
                writes.append(dict(provider=True, address=args[0], hex=raw.hex()))
            elif args[:len(action.get('args', []))] != action.get('args', []):
                failures.append('Independent freshly loaded primary/secondary ID order')
            if 'mutation' in action:
                uc.mem_write(PARTY - 8, action['mutation'])
                writes.append(dict(provider=True, address=PARTY - 8, hex=action['mutation'].hex()))
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, reg in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(reg, 0xcafe0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, action['returnWord'])
            uc.reg_write(R.UC_ARM_REG_CPSR, (ordinal + len(calls)) % 16 << 28 | 0x10)
            uc.reg_write(R.UC_ARM_REG_PC, lr)
        elif not address <= location < address + len(body):
            raise ValueError(('No native game/SDK body execution is authorized', hex(location)))

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=4000)
    if not returned:
        raise ValueError('Collection/classification caller did not return')
    registers = [vm.reg_read(reg) for reg in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Actual ARM callee-saved registers/SP differ')
    if result is not None and registers[0] != result or len(calls) != len(calls_expected):
        failures.append('Independent unsigned classification/ignored-category0/duplicate result')
    for base, raw in expected.items():
        if bytes(vm.mem_read(base, len(raw))) != raw:
            failures.append('Independent full state/padding/provider mutation/paired-copy/reset layout')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
