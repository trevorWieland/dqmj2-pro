import hashlib
import json
import random
import struct
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR
from match_runtime import REGISTERS

ENTRY, SIZE = 0x0203B660, 416
DATA, TAIL, GLOBAL = 0x02380000, 0x02380200, 0x020F4000
VIEW, TABLE, ALLOCATOR = 0x020F5B00, 0x020F5B4C, 0x020F4C38
STACK, SP, STOP = 0x03030000, 0x03030800, 0x0F000000
DIVIDE, RESERVE, APPEND, EMPTY, DISABLE, RESTORE = 0x02026350, 0x02038970, 0x0202BA20, 0x0202B9F4, 0x02007FF4, 0x02008008
CLEANUP, SETUP, TIMER, START, CALLBACK = 0x0203B854, 0x0200932C, 0x02009264, 0x0203B9C0, 0x0203B9B0
HELPERS = {DIVIDE: (484, 484), RESERVE: (68, 72), APPEND: (84, 84), EMPTY: (44, 44), DISABLE: (20, 20), RESTORE: (24, 24)}


def recipes():
    return [dict(index=i, count=[-1, 0, 1, 2, 3][i % 5], mode=[0, 1, -1, 2][i // 5 % 4],
                 pool=[0, 1, 3, 7, 0x7F, 0xFF, 0xFE, 0x80][i // 20 % 8],
                 units=[0, 1, 2, 9, 0x80000000, 0xFFFFFFFF][i // 3 % 6], empty=i // 7 % 2 == 0)
            for i in range(640)]


def initial(item):
    rng = random.Random(0x3B660000 + item['index'])
    data, global_data = bytearray(rng.randbytes(4096)), bytearray(rng.randbytes(8192))
    args = [DATA, item['mode'] & 0xFFFFFFFF, rng.getrandbits(32), rng.getrandbits(32),
            [0, 1, 7, 0xFFFFFFFF][item['index'] // 160 % 4], item['units'], rng.getrandbits(32), rng.getrandbits(32)]
    writes = []
    def put(address, width, value, record=False):
        target, base = (data, DATA) if DATA <= address < DATA + 4096 else (global_data, GLOBAL)
        value &= (1 << (width * 8)) - 1
        target[address - base:address - base + width] = value.to_bytes(width, 'little')
        if record:
            writes.append([address, width, value])
    flags = rng.getrandbits(32)
    flags = flags & ~1 | (item['index'] // 2 & 1)
    put(DATA + 0x24, 4, flags)
    put(DATA + 0x48, 4, item['count'])
    channels = [(item['index'] + i * 3) & 15 for i in range(max(item['count'], 0))]
    for i, channel in enumerate(channels):
        put(DATA + 0x4C + i, 1, channel)
    pool = rng.getrandbits(32) & ~255 | item['pool']
    put(ALLOCATOR + 4, 4, pool)
    put(VIEW, 4, 0 if item['empty'] else TAIL)
    put(VIEW + 4, 4, 0 if item['empty'] else TAIL)
    count = [0, 1, 65535][item['index'] % 3]
    put(VIEW + 8, 2, count)
    put(VIEW + 10, 2, 80)
    put(TAIL + 80, 4, 0)
    put(TAIL + 84, 4, 0)
    before_data, before_global = bytes(data), bytes(global_data)
    def divide(first, second):
        return first // second if second else first
    denominator = item['count'] * ((item['units'] << 5) & 0xFFFFFFFF) & 0xFFFFFFFF
    size = divide(args[3], denominator) * item['units'] * 32 & 0xFFFFFFFF
    adjusted = size >> 1 if item['mode'] == 1 else size
    timer = divide(args[4] * adjusted & 0xFFFFFFFF, item['units'])
    sid = next((bit for bit in range(8) if not pool & 1 << bit), -1)
    services = []
    if flags & 1:
        services.append(dict(target=CLEANUP, arguments=[DATA, 0xFFFFFFFF]))
    put(DATA + 0x28, 4, size, True)
    if sid >= 0:
        put(ALLOCATOR + 4, 4, pool | 1 << sid, True)
    put(DATA + 0x40, 4, sid, True)
    helpers = {address: 0 for address in HELPERS}
    helpers[DIVIDE], helpers[RESERVE] = 2, 1
    if sid >= 0:
        for index, channel in enumerate(channels):
            address = size * index + args[2] & 0xFFFFFFFF
            put(TABLE + channel * 8, 4, address, True)
            put(TABLE + channel * 8 + 4, 4, 0, True)
            services.append(dict(target=SETUP, arguments=[channel, args[1], address, 1, 0, size >> 2, 127, 0, args[4] << 5 & 0xFFFFFFFF, 64]))
        services.append(dict(target=TIMER, arguments=[sid, timer, timer, CALLBACK, DATA]))
        helpers[APPEND] = helpers[DISABLE] = helpers[RESTORE] = 1
        if item['empty']:
            helpers[EMPTY] = 1
            put(DATA + 84, 4, 0, True)
            put(DATA + 80, 4, 0, True)
            put(VIEW, 4, DATA, True)
        else:
            put(DATA + 80, 4, TAIL, True)
            put(DATA + 84, 4, 0, True)
            put(TAIL + 84, 4, DATA, True)
        put(VIEW + 4, 4, DATA, True)
        put(VIEW + 8, 2, count + 1, True)
        for offset, value in [(0x20, args[1]), (0x2C, args[5]), (0x30, args[6]), (0x34, args[7]),
                              (0x38, 0), (0x3C, 0), (0x24, flags | 1), (0x2C, 1)]:
            put(DATA + offset, 4, value, True)
        services.append(dict(target=START, arguments=[DATA, 0], transientWord2C=1))
        put(DATA + 0x2C, 4, args[5], True)
    return dict(args=args, beforeData=before_data, beforeGlobal=before_global,
                expectedData=bytes(data), expectedGlobal=bytes(global_data), expectedWrites=writes,
                expectedServices=services, expectedHelpers=helpers, result=int(sid >= 0))


def execute(main, code, item):
    model = initial(item)
    rng = random.Random(0xB6600000 + item['index'])
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, main)
    uc.mem_write(ENTRY, code)
    uc.mem_write(DATA, model['beforeData'])
    uc.mem_write(GLOBAL, model['beforeGlobal'])
    uc.mem_map(STACK, 4096)
    stack = bytearray(rng.randbytes(4096))
    struct.pack_into('<IIII', stack, SP - STACK, *model['args'][4:])
    uc.mem_write(STACK, bytes(stack))
    uc.mem_map(STOP, 4096)
    control = 0x1F | ((item['index'] >> 2) & 1) * 128 | ((item['index'] >> 3) & 1) * 64
    uc.reg_write(UC_ARM_REG_CPSR, (item['index'] & 15) << 28 | control)
    for reg in REGISTERS:
        uc.reg_write(reg, rng.getrandbits(32))
    for reg, value in zip(REGISTERS[:4], model['args']):
        uc.reg_write(reg, value)
    uc.reg_write(UC_ARM_REG_SP, SP)
    uc.reg_write(UC_ARM_REG_LR, STOP | (item['index'] & 1))
    saved = [uc.reg_read(reg) for reg in REGISTERS[4:12]]
    returned, frames, pcs, reads, writes, services = [], [], [], [], [], []
    helpers = {address: 0 for address in HELPERS}

    def step(machine, pc, width, unused):
        while frames and frames[-1][:2] == [pc, machine.reg_read(UC_ARM_REG_SP)]:
            helpers[frames.pop()[2]] += 1
        if pc == STOP:
            returned.append(pc)
            machine.emu_stop()
            return
        if pc in [CLEANUP, SETUP, TIMER, START]:
            count = {CLEANUP: 2, SETUP: 10, TIMER: 5, START: 2}[pc]
            arguments = [machine.reg_read(reg) for reg in REGISTERS[:min(count, 4)]]
            if count > 4:
                arguments += list(struct.unpack('<' + 'I' * (count - 4), bytes(machine.mem_read(machine.reg_read(UC_ARM_REG_SP), (count - 4) * 4))))
            event = dict(target=pc, arguments=arguments)
            if pc == START:
                event['transientWord2C'] = struct.unpack('<I', bytes(machine.mem_read(DATA + 0x2C, 4)))[0]
                assert machine.reg_read(UC_ARM_REG_CPSR) & 128
            services.append(event)
            for index in [0, 1, 2, 3, 12]:
                machine.reg_write(REGISTERS[index], rng.getrandbits(32))
            machine.reg_write(UC_ARM_REG_CPSR, ((item['index'] * 3 & 15) << 28) | (machine.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF))
            machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))
            return
        if pc in HELPERS:
            frames.append([machine.reg_read(UC_ARM_REG_LR), machine.reg_read(UC_ARM_REG_SP), pc])
        assert width == 4 and (ENTRY <= pc < ENTRY + 404 or any(a <= pc < a + n[0] for a, n in HELPERS.items()))
        pcs.append(pc)

    def read(machine, access, address, size, value, unused):
        ranges = [(DATA, DATA + 4096), (GLOBAL, GLOBAL + 8192), (SP - 128, SP + 16),
                  (ENTRY, ENTRY + SIZE), *[(a, a + n[1]) for a, n in HELPERS.items()]]
        assert any(a <= address and address + size <= b for a, b in ranges)
        reads.append([address, size])

    def write(machine, access, address, size, value, unused):
        assert any(a <= address and address + size <= b for a, b in [(DATA, DATA + 4096), (GLOBAL, GLOBAL + 8192), (SP - 128, SP)])
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])

    uc.hook_add(UC_HOOK_CODE, step)
    uc.hook_add(UC_HOOK_MEM_READ, read)
    uc.hook_add(UC_HOOK_MEM_WRITE, write)
    uc.emu_start(ENTRY, STOP + 4, count=4000)
    assert returned == [STOP] and not frames
    assert uc.reg_read(UC_ARM_REG_PC) == STOP
    assert uc.reg_read(UC_ARM_REG_SP) == SP
    assert bool(uc.reg_read(UC_ARM_REG_CPSR) & 32) == bool(item['index'] & 1)
    assert uc.reg_read(UC_ARM_REG_CPSR) & 0xDF == control
    assert [uc.reg_read(reg) for reg in REGISTERS[4:12]] == saved
    final_stack = bytes(uc.mem_read(STACK, 4096))
    assert final_stack[:0x780] == stack[:0x780] and final_stack[0x800:] == stack[0x800:]
    final_data, final_global = bytes(uc.mem_read(DATA, 4096)), bytes(uc.mem_read(GLOBAL, 8192))
    nonstack = [row for row in writes if not SP - 128 <= row[0] < SP]
    result = uc.reg_read(REGISTERS[0])
    passed = result == model['result'] and final_data == model['expectedData'] and final_global == model['expectedGlobal']
    passed = passed and nonstack == model['expectedWrites'] and services == model['expectedServices'] and helpers == model['expectedHelpers']
    return dict(actualReturns=1, actualNativeHelperReturns=sum(helpers.values()), helperCounts=helpers,
                suppliedCalls=len(services), services=services, result=result, modelPassed=passed,
                dataSha256=hashlib.sha256(final_data).hexdigest(), globalSha256=hashlib.sha256(final_global).hexdigest(),
                stackSha256=hashlib.sha256(final_stack).hexdigest(), pcs=pcs, reads=reads, writes=writes,
                registers=[uc.reg_read(reg) for reg in REGISTERS] + [uc.reg_read(UC_ARM_REG_CPSR)])


def compact(result):
    result = dict(result)
    traces = {key: result.pop(key) for key in ['pcs', 'reads', 'writes']}
    result['traceSha256'] = hashlib.sha256(json.dumps(traces, sort_keys=True).encode()).hexdigest()
    return result
