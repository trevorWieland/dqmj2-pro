import hashlib
import random
import struct
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR
from match_runtime import REGISTERS

REMOVE, SEARCH, INSERT, NEXT = 0x0202EB4C, 0x0202B884, 0x0202E9AC, 0x0202BB88
PAGE, STACK, SP, STOP = 0x02380000, 0x03030000, 0x03030800, 0x0F000000


def recipes(kind):
    if kind == 'insert':
        return [dict(index=i, count=i % 8, parts=1 + (i // 8) % 3,
                     priority=i % 256, equal=(i // 8) % 4 == 0) for i in range(768)]
    if kind == 'remove':
        return [dict(index=i, count=i % 8, target=(i // 8) % 10 - 1) for i in range(640)]
    rows = []
    for base in [0, 0x100, 0x10000, 0x7FFFFE00, 0x80000000, 0xFFFFFE00]:
        for offset in [0, 1, 99, 100, 119, 120, 139, 140, 159, 160, 179, 180, 199, 200, 219, 220, 249, 250, 299, 300, 319, 320]:
            for empty in [False, True]:
                rows.append(dict(index=len(rows), base=base, target=base + offset, empty=empty))
    return rows


def initial(kind, item):
    rng = random.Random(0x2B884000 + item['index'])
    data = bytearray(rng.randbytes(4096))
    def put(address, value):
        struct.pack_into('<I', data, address - PAGE, value)
    if kind == 'insert':
        nodes = [PAGE + 0x200 + 48 * i for i in range(11)]
        order = nodes[:item['count']]
        incoming = nodes[8:8 + item['parts']]
        keys = [rng.getrandbits(8) for node in nodes]
        keys[8] = item['priority']
        if item['equal']:
            keys[0] = keys[8]
        for index, node in enumerate(nodes):
            put(node + 16, 0)
            data[node + 24 - PAGE] = keys[index]
        for chain in [order, incoming]:
            for index, node in enumerate(chain):
                put(node + 16, chain[index + 1] if index + 1 < len(chain) else 0)
        put(PAGE, order[0] if order else 0)
        before = bytes(data)
        if not order:
            put(PAGE, incoming[0])
        elif len(order) == 1:
            if keys[0] > keys[8]:
                put(incoming[-1] + 16, order[0])
                put(PAGE, incoming[0])
            else:
                put(order[0] + 16, incoming[0])
        else:
            position = next((i for i in range(1, len(order)) if keys[i] >= keys[8]), len(order))
            put(order[position - 1] + 16, incoming[0])
            if position < len(order):
                put(incoming[-1] + 16, order[position])
        return dict(before=before, expected=bytes(data), argument=incoming[0], result=None,
                    helperReturns=0, recursiveReturns=0)
    if kind == 'remove':
        nodes = [PAGE + 0x200 + 32 * i for i in range(8)]
        order = rng.sample(nodes, item['count'])
        target = 0 if item['target'] < 0 else nodes[item['target'] % 8]
        put(PAGE, order[0] if order else 0)
        for node in nodes:
            put(node + 16, 0)
        for index, node in enumerate(order):
            put(node + 16, order[index + 1] if index + 1 < len(order) else 0)
        before = bytes(data)
        found = target in order
        if found:
            index = order.index(target)
            put(PAGE if index == 0 else order[index - 1] + 16,
                order[index + 1] if index + 1 < len(order) else 0)
            put(target + 16, 0)
        return dict(before=before, expected=bytes(data), argument=target, result=int(found), helperReturns=0, recursiveReturns=0)
    nodes = [PAGE + 0x200 + 80 * i for i in range(7)]
    link_offset = [32, 40, 48][item['index'] % 3]
    chains = {PAGE: [] if item['empty'] else [0, 1, 2], nodes[0] + 12: [3, 4],
              nodes[3] + 12: [5], nodes[1] + 12: [6]}
    ranges = [(100, 200), (200, 300), (300, 320), (120, 180), (100, 200), (140, 160), (220, 250)]
    for index, node in enumerate(nodes):
        put(node + 12, 0)
        struct.pack_into('<H', data, node + 22 - PAGE, link_offset)
        put(node + link_offset + 4, 0)
        low, high = ranges[index]
        put(node + 24, item['base'] + low)
        put(node + 28, item['base'] + high)
    for view, indices in chains.items():
        put(view, nodes[indices[0]] if indices else 0)
        struct.pack_into('<H', data, view + 10 - PAGE, link_offset)
        for index, node_id in enumerate(indices):
            put(nodes[node_id] + link_offset + 4, nodes[indices[index + 1]] if index + 1 < len(indices) else 0)
    counters = dict(helper=0, recursive=0)
    def search(view):
        counters['helper'] += 1
        for index in chains.get(view, []):
            low, high = ranges[index]
            if item['base'] + low <= item['target'] < item['base'] + high:
                counters['recursive'] += 1
                return search(nodes[index] + 12) or nodes[index]
            counters['helper'] += 1
        return 0
    result = search(PAGE)
    return dict(before=bytes(data), expected=bytes(data), argument=item['target'], result=result,
                helperReturns=counters['helper'], recursiveReturns=counters['recursive'])


def execute(main, code, kind, item):
    entry, size = {'remove': (REMOVE, 116), 'search': (SEARCH, 104), 'insert': (INSERT, 184)}[kind]
    model = initial(kind, item)
    rng = random.Random(0x2EB4C000 + item['index'])
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, main)
    uc.mem_write(entry, code)
    uc.mem_write(PAGE, model['before'])
    uc.mem_map(STACK, 4096)
    stack = rng.randbytes(4096)
    uc.mem_write(STACK, stack)
    uc.mem_map(STOP, 4096)
    uc.reg_write(UC_ARM_REG_CPSR, ((item['index'] & 15) << 28) | 0x1F)
    for reg in REGISTERS:
        uc.reg_write(reg, rng.getrandbits(32))
    uc.reg_write(REGISTERS[0], PAGE)
    uc.reg_write(REGISTERS[1], model['argument'])
    uc.reg_write(UC_ARM_REG_SP, SP)
    uc.reg_write(UC_ARM_REG_LR, STOP | (item['index'] & 1))
    saved = [uc.reg_read(reg) for reg in REGISTERS[4:12]]
    counters = dict(actualReturns=0, actualHelperReturns=0, actualRecursiveCallerReturns=0)
    frames, pcs, reads, writes = [], [], [], []

    def step(machine, pc, width, unused):
        while frames and frames[-1][:2] == [pc, machine.reg_read(UC_ARM_REG_SP)]:
            frame = frames.pop()
            counters[frame[2]] += 1
        if pc == STOP:
            counters['actualReturns'] += 1
            machine.emu_stop()
            return
        if pc == entry and machine.reg_read(UC_ARM_REG_SP) != SP:
            frames.append([machine.reg_read(UC_ARM_REG_LR), machine.reg_read(UC_ARM_REG_SP), 'actualRecursiveCallerReturns'])
        if kind == 'search' and pc == NEXT:
            frames.append([machine.reg_read(UC_ARM_REG_LR), machine.reg_read(UC_ARM_REG_SP), 'actualHelperReturns'])
        assert width == 4 and (entry <= pc < entry + size or kind == 'search' and NEXT <= pc < NEXT + 24)
        pcs.append(pc)

    def read(machine, access, address, size, value, unused):
        assert PAGE <= address and address + size <= PAGE + 4096 or SP - 64 <= address and address + size <= SP
        reads.append([address, size])

    def write(machine, access, address, size, value, unused):
        assert kind in ['remove', 'insert'] and PAGE <= address and address + size <= PAGE + 4096 or SP - 64 <= address and address + size <= SP
        writes.append([address, size, value])

    uc.hook_add(UC_HOOK_CODE, step)
    uc.hook_add(UC_HOOK_MEM_READ, read)
    uc.hook_add(UC_HOOK_MEM_WRITE, write)
    uc.emu_start(entry, STOP + 4, count=1500)
    assert counters['actualReturns'] == 1 and not frames
    assert uc.reg_read(UC_ARM_REG_PC) == STOP
    assert bool(uc.reg_read(UC_ARM_REG_CPSR) & 32) == bool(item['index'] & 1)
    assert uc.reg_read(UC_ARM_REG_SP) == SP
    assert [uc.reg_read(reg) for reg in REGISTERS[4:12]] == saved
    final_stack = bytes(uc.mem_read(STACK, 4096))
    assert final_stack[:0x7C0] == stack[:0x7C0] and final_stack[0x800:] == stack[0x800:]
    final = bytes(uc.mem_read(PAGE, 4096))
    result = uc.reg_read(REGISTERS[0])
    passed = (model['result'] is None or result == model['result']) and final == model['expected']
    passed = passed and counters['actualHelperReturns'] == model['helperReturns']
    passed = passed and counters['actualRecursiveCallerReturns'] == model['recursiveReturns']
    return dict(counters=counters, result=result, modelPassed=passed, pcs=pcs, reads=reads, writes=writes,
                dataSha256=hashlib.sha256(final).hexdigest(), stackSha256=hashlib.sha256(final_stack).hexdigest(),
                registers=[uc.reg_read(reg) for reg in REGISTERS] + [uc.reg_read(UC_ARM_REG_CPSR)])
