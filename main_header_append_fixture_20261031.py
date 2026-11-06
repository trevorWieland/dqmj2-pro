import hashlib
import random
import struct
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR
from match_runtime import REGISTERS

ENTRY, SIZE, ALLOC = 0x02037B94, 104, 0x0202B784
GET, APPEND, EMPTY = 0x0202BBA0, 0x0202BA20, 0x0202B9F4
CTX, OBJECT = 0x02370000, 0x02380000
LIST, DECOY, NODE, DECOY_NODE = CTX + 0x100, CTX + 0x140, CTX + 0x200, CTX + 0x240
STACK, SP, STOP = 0x03030000, 0x03030800, 0x0F000000
CODE = [(ENTRY, SIZE), (GET, 20), (APPEND, 84), (EMPTY, 44)]


def recipe(index):
    rng = random.Random(0x37B94000 + index)
    edges = [0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF]
    return dict(index=index, failed=index % 7 == 0, empty=bool(index & 1),
                count=[0, 1, 0x7FFF, 0xFFFF][(index // 2) % 4], handle=edges[index % 5],
                bytes=[0, 1, 31, 32, 33, 63, 64, 65, 255, 256, 511, 512][(index // 8) % 12],
                values=[edges[(index + part) % 5] if index < 128 else rng.getrandbits(32) for part in range(3)])


def execute(main, code, item):
    rng = random.Random(0x37B94100 + item['index'])
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, main)
    uc.mem_write(ENTRY, code)
    context, before = bytearray(rng.randbytes(4096)), bytearray(rng.randbytes(4096))
    struct.pack_into('<I', context, 0, item['handle'])
    struct.pack_into('<I', context, 8, LIST)
    struct.pack_into('<I', context, 20, DECOY)
    for address, node in [(LIST, NODE), (DECOY, DECOY_NODE)]:
        struct.pack_into('<IIHH', context, address - CTX, 0 if item['empty'] else node,
                         0 if item['empty'] else node, item['count'], 0)
        struct.pack_into('<II', context, node - CTX, 0, 0)
    uc.mem_write(CTX, bytes(context))
    uc.mem_write(OBJECT, bytes(before))
    uc.mem_map(STACK, 4096)
    stack = bytearray(rng.randbytes(4096))
    struct.pack_into('<I', stack, 2048, item['values'][2])
    uc.mem_write(STACK, bytes(stack))
    uc.mem_map(STOP, 4096)
    uc.reg_write(UC_ARM_REG_CPSR, ((item['index'] & 15) << 28) | 0x1F)
    for reg in REGISTERS:
        uc.reg_write(reg, rng.getrandbits(32))
    for reg, value in zip(REGISTERS, [CTX, item['bytes'], *item['values'][:2]]):
        uc.reg_write(reg, value)
    uc.reg_write(UC_ARM_REG_SP, SP)
    uc.reg_write(UC_ARM_REG_LR, STOP | (item['index'] & 1))
    saved = [uc.reg_read(reg) for reg in REGISTERS[4:12]]
    state = dict(actualReturns=0, actualHelperReturns=0, suppliedAllocatorCompletions=0)
    frames, pcs, reads, writes, supplied = [], [], [], [], []

    def step(machine, pc, width, unused):
        while frames and frames[-1] == [pc, machine.reg_read(UC_ARM_REG_SP)]:
            frames.pop()
            state['actualHelperReturns'] += 1
        if pc == STOP:
            state['actualReturns'] += 1
            machine.emu_stop()
            return
        if pc == ALLOC:
            args = [machine.reg_read(reg) for reg in REGISTERS[:3]]
            assert args == [item['handle'], ((item['bytes'] + 31) & ~31) + 32, 32]
            assert not supplied
            supplied.append(dict(address=pc, args=args, result=0 if item['failed'] else OBJECT))
            for index in [1, 2, 3, 12]:
                machine.reg_write(REGISTERS[index], rng.getrandbits(32))
            machine.reg_write(REGISTERS[0], 0 if item['failed'] else OBJECT)
            machine.reg_write(UC_ARM_REG_CPSR, ((item['index'] * 3 & 15) << 28) | 0x1F)
            machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))
            state['suppliedAllocatorCompletions'] += 1
            return
        if pc in [GET, APPEND, EMPTY]:
            frames.append([machine.reg_read(UC_ARM_REG_LR), machine.reg_read(UC_ARM_REG_SP)])
        assert width == 4 and any(start <= pc < start + size for start, size in CODE)
        pcs.append(pc)

    def read(machine, access, address, size, value, unused):
        assert any(start <= address and address + size <= end for start, end in [
            (CTX, CTX + 4096), (OBJECT, OBJECT + 4096), (SP - 32, SP + 4)])
        reads.append([address, size])

    def write(machine, access, address, size, value, unused):
        assert any(start <= address and address + size <= end for start, end in [
            (CTX, CTX + 4096), (OBJECT, OBJECT + 4096), (SP - 32, SP)])
        writes.append([address, size, value])

    uc.hook_add(UC_HOOK_CODE, step)
    uc.hook_add(UC_HOOK_MEM_READ, read)
    uc.hook_add(UC_HOOK_MEM_WRITE, write)
    uc.emu_start(ENTRY, STOP + 4, count=250)
    assert state['actualReturns'] == 1 and not frames and state['suppliedAllocatorCompletions'] == 1
    assert state['actualHelperReturns'] == (0 if item['failed'] else 3 if item['empty'] else 2)
    assert uc.reg_read(UC_ARM_REG_SP) == SP
    assert [uc.reg_read(reg) for reg in REGISTERS[4:12]] == saved
    final_stack = bytes(uc.mem_read(STACK, 4096))
    assert final_stack[:0x7E0] == stack[:0x7E0] and final_stack[0x800:] == stack[0x800:]
    expected_context, expected_object = bytearray(context), bytearray(before)
    if not item['failed']:
        for offset, value in zip([8, 12, 16, 20], [item['bytes'], *item['values']]):
            struct.pack_into('<I', expected_object, offset, value)
        struct.pack_into('<II', expected_object, 0, 0 if item['empty'] else NODE, 0)
        if item['empty']:
            struct.pack_into('<I', expected_context, LIST - CTX, OBJECT)
        else:
            struct.pack_into('<I', expected_context, NODE - CTX + 4, OBJECT)
        struct.pack_into('<I', expected_context, LIST - CTX + 4, OBJECT)
        struct.pack_into('<H', expected_context, LIST - CTX + 8, (item['count'] + 1) & 0xFFFF)
    actual_context = bytes(uc.mem_read(CTX, 4096))
    actual_object = bytes(uc.mem_read(OBJECT, 4096))
    returned = uc.reg_read(REGISTERS[0])
    model = returned == (0 if item['failed'] else OBJECT + 32)
    model = model and actual_context == expected_context and actual_object == expected_object
    return dict(state=state, result=returned, modelPassed=model, supplied=supplied,
                contextSha256=hashlib.sha256(actual_context).hexdigest(), objectSha256=hashlib.sha256(actual_object).hexdigest(),
                pcs=pcs, reads=reads, writes=writes,
                registers=[uc.reg_read(reg) for reg in REGISTERS] + [uc.reg_read(UC_ARM_REG_CPSR)],
                stackSha256=hashlib.sha256(final_stack).hexdigest())
