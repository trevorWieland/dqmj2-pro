import hashlib
import json
import random
import struct
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR
from match_runtime import REGISTERS

PAGE, STACK, SP, STOP, HEAP = 0x02380000, 0x03030000, 0x03030800, 0x0F000000, 0x0F000100
DESCRIPTOR, SECTION, ARGUMENT, OBJECT, AUX = PAGE + 0x300, PAGE + 0x340, PAGE + 0x2F0, PAGE + 0xA00, PAGE + 0xC00
TABLE_COUNT, FACTORY_POINTER = 0x020DD5F4, 0x020EDD10
QUERY, ALLOCATE, ALLOCATION_SIZE = 0x0202BF2C, 0x02028DEC, 0x0202E858
INITIALIZE, ENQUEUE, MASK, INSERT, REFRESH = 0x0202E8B8, 0x0202EACC, 0x0202EA64, 0x0202E9AC, 0x020290C8
HELPERS = {QUERY: 92, ALLOCATE: 52, ALLOCATION_SIZE: 96, INITIALIZE: 148, ENQUEUE: 128, MASK: 104, INSERT: 184}
VARIANTS = [(0x02029758, 136, 2, 0x68), (0x020298C8, 136, 8, 0x6C), (0x020291F4, 144, 1, 0x60)]


def recipes():
    result = []
    for active in [0, 1, 2, 128, 255]:
        for descriptor in [False, True]:
            for query in [0, 1, 2, 3, 255, 0xFFFFFFFF]:
                for flow in ['provided', 'allocated', 'allocation-fails']:
                    for count in [0, 1, 127, 255]:
                        result.append(dict(index=len(result), active=active, descriptor=descriptor,
                                           query=query, flow=flow, count=count))
    return result


def initial(variant, item):
    entry, size, bit, destination = variant
    rng = random.Random(0x291F4000 + item['index'])
    data = bytearray(rng.randbytes(4096))
    def put(address, value):
        struct.pack_into('<I', data, address - PAGE, value)
    data[8] = item['active']
    put(PAGE + 16, AUX)
    for offset in [0x14, 0x1C, 0x24]:
        put(PAGE + offset, 0)
    put(ARGUMENT, DESCRIPTOR if item['descriptor'] else 0)
    struct.pack_into('<H', data, DESCRIPTOR + 12 - PAGE, 16)
    put(DESCRIPTOR + 16, SECTION - DESCRIPTOR)
    data[SECTION + 9 - PAGE] = 3
    struct.pack_into('<H', data, SECTION + 14 - PAGE, 32)
    struct.pack_into('<H', data, SECTION + 40 - PAGE, 8)
    for index, kind in enumerate([0x4D, 0x4A, 0x56]):
        put(SECTION + 44 + index * 8, 0x100 + index * 64)
        data[SECTION + 0x100 + index * 64 - PAGE] = kind
    data[AUX + 24 - PAGE] = item['count']
    data[AUX + 23 - PAGE] = 255 - item['count']
    before = bytes(data)
    header = SECTION + 0x100 + item['query'] * 64 if item['descriptor'] and item['query'] < 3 else 0
    provided = item['flow'] == 'provided'
    object_address = OBJECT if provided or header and item['flow'] == 'allocated' else 0
    expected_helpers = {address: 0 for address in HELPERS}
    heap_calls = refresh_calls = 0
    if item['active']:
        expected_helpers[QUERY] = 1
        if not provided:
            expected_helpers[ALLOCATE] = 1
            if header:
                expected_helpers[ALLOCATION_SIZE] = 1
                heap_calls = 1
            data[10] |= bit
        if object_address:
            expected_helpers[INITIALIZE] = expected_helpers[ENQUEUE] = 1
            for offset, value in [(0, 0), (4, 4096), (8, header), (12, 0), (16, 0), (20, 0)]:
                put(OBJECT + offset, value)
            data[OBJECT + 24 - PAGE] = 127
            data[OBJECT + 25 - PAGE] = 0
            if header:
                expected_helpers[MASK] = expected_helpers[INSERT] = 1
                put(PAGE + {0: 0x14, 1: 0x1C, 2: 0x24}[item['query']], OBJECT)
            put(PAGE + destination, OBJECT)
            refresh_calls = int(entry == 0x020291F4)
    expected_result = int(bool(item['active'] and object_address))
    allocation_count = item['count'] if item['query'] == 0 else 255 - item['count']
    return dict(before=before, expected=bytes(data), header=header,
                argument2=OBJECT if provided else 0, result=expected_result,
                allocationBytes=(allocation_count * 2 + 28) & ~3,
                heapResult=OBJECT if item['flow'] == 'allocated' else 0,
                expectedHelpers=expected_helpers, expectedHeap=heap_calls, expectedRefresh=refresh_calls)


def execute(main, code, variant, item):
    entry, size, bit, destination = variant
    model = initial(variant, item)
    rng = random.Random(0x29758000 + item['index'])
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, main)
    uc.mem_write(entry, code)
    uc.mem_write(PAGE, model['before'])
    uc.mem_write(TABLE_COUNT, bytes(4))
    uc.mem_write(FACTORY_POINTER, struct.pack('<I', HEAP))
    uc.mem_map(STACK, 4096)
    stack = rng.randbytes(4096)
    uc.mem_write(STACK, stack)
    uc.mem_map(STOP, 4096)
    uc.reg_write(UC_ARM_REG_CPSR, ((item['index'] & 15) << 28) | 0x1F)
    for reg in REGISTERS:
        uc.reg_write(reg, rng.getrandbits(32))
    for reg, value in zip(REGISTERS, [PAGE, ARGUMENT, model['argument2'], item['query']]):
        uc.reg_write(reg, value)
    uc.reg_write(UC_ARM_REG_SP, SP)
    uc.reg_write(UC_ARM_REG_LR, STOP | (item['index'] & 1))
    saved = [uc.reg_read(reg) for reg in REGISTERS[4:12]]
    returned, frames, pcs, reads, writes, providers = [], [], [], [], [], []
    helper_counts = {address: 0 for address in HELPERS}
    provider_counts = dict(heap=0, refresh=0)

    def step(machine, pc, width, unused):
        while frames and frames[-1][:2] == [pc, machine.reg_read(UC_ARM_REG_SP)]:
            helper_counts[frames.pop()[2]] += 1
        if pc == STOP:
            returned.append(pc)
            machine.emu_stop()
            return
        if pc in [HEAP, REFRESH]:
            argument = machine.reg_read(REGISTERS[0])
            if pc == HEAP:
                assert argument == model['allocationBytes'] and model['header'] and item['flow'] != 'provided'
                assert machine.reg_read(REGISTERS[1]) == HEAP
                result = model['heapResult']
                provider_counts['heap'] += 1
            else:
                assert entry == 0x020291F4 and argument == PAGE
                result = rng.getrandbits(32)
                provider_counts['refresh'] += 1
            providers.append(dict(target=pc, consumedArguments=[argument], result=result))
            for index in [1, 2, 3, 12]:
                machine.reg_write(REGISTERS[index], rng.getrandbits(32))
            machine.reg_write(REGISTERS[0], result)
            machine.reg_write(UC_ARM_REG_CPSR, ((item['index'] * 3 & 15) << 28) | 0x1F)
            machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))
            return
        if pc in HELPERS:
            frames.append([machine.reg_read(UC_ARM_REG_LR), machine.reg_read(UC_ARM_REG_SP), pc])
        assert width == 4 and (entry <= pc < entry + size or any(a <= pc < a + n for a, n in HELPERS.items()))
        pcs.append(pc)

    def read(machine, access, address, size, value, unused):
        ranges = [(PAGE, PAGE + 4096), (SP - 64, SP), (TABLE_COUNT, TABLE_COUNT + 4),
                  (FACTORY_POINTER, FACTORY_POINTER + 4), (INITIALIZE, INITIALIZE + 160),
                  (ALLOCATE, ALLOCATE + 56)]
        assert any(a <= address and address + size <= b for a, b in ranges)
        reads.append([address, size])

    def write(machine, access, address, size, value, unused):
        assert PAGE <= address and address + size <= PAGE + 4096 or SP - 64 <= address and address + size <= SP
        writes.append([address, size, value])

    uc.hook_add(UC_HOOK_CODE, step)
    uc.hook_add(UC_HOOK_MEM_READ, read)
    uc.hook_add(UC_HOOK_MEM_WRITE, write)
    uc.emu_start(entry, STOP + 4, count=1500)
    assert returned == [STOP] and not frames
    assert uc.reg_read(UC_ARM_REG_PC) == STOP
    assert bool(uc.reg_read(UC_ARM_REG_CPSR) & 32) == bool(item['index'] & 1)
    assert uc.reg_read(UC_ARM_REG_SP) == SP
    assert [uc.reg_read(reg) for reg in REGISTERS[4:12]] == saved
    final_stack = bytes(uc.mem_read(STACK, 4096))
    assert final_stack[:0x7C0] == stack[:0x7C0] and final_stack[0x800:] == stack[0x800:]
    assert bytes(uc.mem_read(TABLE_COUNT, 4)) == bytes(4)
    assert bytes(uc.mem_read(FACTORY_POINTER, 4)) == struct.pack('<I', HEAP)
    final = bytes(uc.mem_read(PAGE, 4096))
    result = uc.reg_read(REGISTERS[0])
    passed = final == model['expected'] and result == model['result']
    passed = passed and helper_counts == model['expectedHelpers']
    passed = passed and provider_counts == dict(heap=model['expectedHeap'], refresh=model['expectedRefresh'])
    return dict(actualReturns=1, actualNativeHelperReturns=sum(helper_counts.values()), helperCounts=helper_counts,
                providerCounts=provider_counts, providers=providers, result=result, modelPassed=passed,
                dataSha256=hashlib.sha256(final).hexdigest(), stackSha256=hashlib.sha256(final_stack).hexdigest(),
                pcs=pcs, reads=reads, writes=writes,
                registers=[uc.reg_read(reg) for reg in REGISTERS] + [uc.reg_read(UC_ARM_REG_CPSR)])


def compact(result):
    result = dict(result)
    traces = {key: result.pop(key) for key in ['pcs', 'reads', 'writes']}
    result['traceSha256'] = hashlib.sha256(json.dumps(traces, sort_keys=True).encode()).hexdigest()
    return result
