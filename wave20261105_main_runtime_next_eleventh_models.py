import itertools
import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {name: {} for name in ['02065c48', '02065d00', '02065d14', '02066f84']}
SP, STOP, GROUP = 0x027f0000, 0x027e0000, 0x02400040
TABLES = {'02065c48': 0x020daea8, '02065d00': 0x020de091, '02065d14': 0x020de092}


def fixtures(name):
    if name == '02065c48':
        return [dict(x=x, y=y, replacement=None) for x, y in itertools.product(range(5), range(4))] + [dict(x=4, y=3, replacement=n) for n in [0, 1, 0x7fff, 0x8000, 0xffff]]
    if name in ['02065d00', '02065d14']:
        return [dict(kind=n, replacement=None) for n in range(93)] + [dict(kind=n, replacement=value) for n, value in itertools.product([0, 7, 92], [0, 1, 127, 128, 255])]
    weights = [[0, 0, 0, 0, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 1], [1, 1, 1, 1, 1], [3, 0, 4, 1, 2], [255, 255, 255, 255, 255]]
    return [dict(low=low, high=high, weights=w, required=r, outcome=mode, mutate=mutate)
            for (low, high), w, r, mode, mutate in itertools.product([(0, 0), (1, 4), (3, 2), (8, 2), (255, 255), (255, 0)], weights, [-2, 0, 1, 4, 255], [0, 1, 2, 3], [False, True])]


def scenario(fixture):
    data = bytearray([fixture['low'], fixture['high'], *fixture['weights']])
    actions = []

    def random(bound):
        n = len(actions)
        mode = fixture['outcome']
        result = [0, bound // 2, bound - 1, -1 if n == 0 else bound + 3][mode]
        action = dict(bound=bound, returned=result & 0xffffffff)
        if fixture['mutate']:
            data[0] = (data[0] + n + 3) & 255
            data[1] = (data[1] + n + 7) & 255
            data[2:] = bytes((v + n * 5 + 1) & 255 for v in reversed(data[2:]))
            action['mutation'] = bytes(data)
        actions.append(action)
        return result

    available = fixture['high'] - fixture['low'] + 1
    if available > 0:
        available = random(available)
    threshold = available + data[0]
    result = -1
    weighted_call = False
    if fixture['required'] <= threshold:
        total = sum(data[2:])
        if total:
            weighted_call = True
            roll = random(total)
            cumulative = [sum(data[2:3 + i]) for i in range(5)]
            result = next((i for i, end in enumerate(cumulative) if roll < end), -1)
    return dict(actions=actions, result=result & 0xffffffff, finalData=bytes(data), threshold=threshold, rangeValue=available, weightedCall=weighted_call)


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    weighted = name == '02066f84'
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    if weighted:
        pages = [(address & ~0xfff, ((address & 0xfff) + len(body) + 0xfff) & ~0xfff), (0x0203d000, 0x1000), (0x02400000, 0x1000), (SP - 0x1000, 0x2000), (STOP, 0x1000)]
        for base, size in pages:
            vm.mem_map(base, size)
    else:
        vm.mem_map(0x02000000, 0x800000)
        vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    words = [0x11223344, 0x89abcdef, 0x76543210, 0xdeadbeef]
    if weighted:
        plan = scenario(fixture)
        initial_group = bytes([fixture['low'], fixture['high'], *fixture['weights']])
        raw = bytearray((i * 37 + ordinal * 17 + 0x43) & 255 for i in range(128))
        raw[64:71] = initial_group
        vm.mem_write(0x02400000, bytes(raw))
        expected = bytearray(raw)
        expected[64:71] = plan['finalData']
        words[:2] = [GROUP, fixture['required'] & 0xffffffff]
        result = plan['result']
    else:
        width = 2 if name == '02065c48' else 1
        index = fixture['x'] + fixture['y'] * 5 if width == 2 else fixture['kind'] * 4
        table_at = TABLES[name] + index * width
        if fixture['replacement'] is not None:
            vm.mem_write(table_at, int(fixture['replacement']).to_bytes(width, 'little'))
        result = int.from_bytes(bytes(vm.mem_read(table_at, width)), 'little', signed=width == 1) & 0xffffffff
        words[:2] = [fixture['x'], fixture['y']] if width == 2 else [fixture['kind'], words[1]]
        plan = dict(actions=[])
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
            n = len(calls)
            action = plan['actions'][n] if n < len(plan['actions']) else dict(bound=0, returned=0)
            args = [uc.reg_read(reg) for reg in C.REGISTERS[:4]]
            calls.append(dict(symbol=symbol, address=location, words=args, program=binding.get('program') or '', processor=binding['processor'], module=binding['module'], mode=binding['mode']))
            if location != 0x0203d294 or args[0] != action['bound'] or uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                failures.append('Independent interval/weight sum/range-gated ARM RNG boundary')
            if 'mutation' in action:
                uc.mem_write(GROUP, action['mutation'])
                writes.append(dict(provider=True, address=GROUP, hex=action['mutation'].hex()))
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, reg in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(reg, 0xcafe0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, action['returned'])
            uc.reg_write(R.UC_ARM_REG_CPSR, (ordinal + len(calls)) % 16 << 28 | 0x10)
            uc.reg_write(R.UC_ARM_REG_PC, lr)
        elif not address <= location < address + len(body):
            raise ValueError(('No actual RNG/game/SDK body execution authorized', hex(location)))

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=2000)
    if not returned:
        raise ValueError('Actual table/weighted selector did not return')
    registers = [vm.reg_read(reg) for reg in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Actual ARM callee-saved registers/SP differ')
    if registers[0] != result or len(calls) != len(plan['actions']):
        failures.append('Independent signed lookup/unsigned halfword/cumulative weighted result and RNG count')
    if weighted:
        if bytes(vm.mem_read(0x02400000, len(expected))) != expected:
            failures.append('Independent fresh low/weight reads and provider-mutation/guard persistence')
        memory_sha = C.sha(b''.join(bytes(vm.mem_read(base, size)) for base, size in pages))
    else:
        memory_sha = C.sha(bytes(vm.mem_read(0x02000000, 0x800000)))
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                mappedRamSha256=memory_sha, modelFailures=failures, actualTopReturn=True)
