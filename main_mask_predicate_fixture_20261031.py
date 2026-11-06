import hashlib
import random
import struct
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR
from match_runtime import REGISTERS

ENTRY, SIZE, HELPER = 0x020D3F4C, 112, 0x020D3540
FIELDS, POINTER, TABLE = 0x020E32F4, 0x021D71EC, 0x023C0000
STACK, SP, STOP = 0x03030000, 0x03030800, 0x0F000000


def recipe(index):
    rng = random.Random(0xD3F4C000 + index)
    edges = [0, 1, 2, 3, 0x8000, 0xFFFF, 0xFFFF0000, 0xFFFFFFFF]
    fields = [edges[(index + i) % len(edges)] for i in range(3)]
    if index >= 128:
        fields = [rng.getrandbits(32) for unused in range(3)]
    return dict(index=index, indices=[index % 32, (index // 8) % 32],
                fields=fields, table=rng.randbytes(256).hex(), null=index % 17 == 0)


def expected(item):
    if item['null']:
        first = second = 0
    else:
        table = bytes.fromhex(item['table'])
        first, second = [struct.unpack_from('<H', table, 10 + 4 * index)[0] for index in item['indices']]
    return sum(bit for offset, bit in [(1, 1), (2, 2), (0, 4)]
               if item['fields'][offset] & first and item['fields'][offset] & second)


def execute(main, code, item):
    rng = random.Random(0xD3F4C100 + item['index'])
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, main)
    uc.mem_write(ENTRY, code)
    fields = struct.pack('<III', *item['fields'])
    pointer = struct.pack('<I', 0 if item['null'] else TABLE)
    table = bytes.fromhex(item['table'])
    uc.mem_write(FIELDS, fields)
    uc.mem_write(POINTER, pointer)
    uc.mem_write(TABLE, table)
    uc.mem_map(STACK, 4096)
    stack = rng.randbytes(4096)
    uc.mem_write(STACK, stack)
    uc.mem_map(STOP, 4096)
    uc.reg_write(UC_ARM_REG_CPSR, ((item['index'] & 15) << 28) | 0x1F)
    for reg in REGISTERS:
        uc.reg_write(reg, rng.getrandbits(32))
    for reg, value in zip(REGISTERS, item['indices']):
        uc.reg_write(reg, value)
    uc.reg_write(UC_ARM_REG_SP, SP)
    uc.reg_write(UC_ARM_REG_LR, STOP | (item['index'] & 1))
    saved = [uc.reg_read(reg) for reg in REGISTERS[4:12]]
    state = dict(actualReturns=0, actualHelperReturns=0, activeHelperReturn=None)
    pcs, reads, writes = [], [], []

    def step(machine, pc, width, unused):
        if state['activeHelperReturn'] == pc:
            state['actualHelperReturns'] += 1
            state['activeHelperReturn'] = None
        if pc == STOP:
            state['actualReturns'] += 1
            machine.emu_stop()
            return
        if pc == HELPER:
            assert state['activeHelperReturn'] is None
            target = machine.reg_read(UC_ARM_REG_LR)
            assert target in [ENTRY + 16, ENTRY + 28]
            state['activeHelperReturn'] = target
        assert width == 4 and (ENTRY <= pc < ENTRY + SIZE - 4 or HELPER <= pc < HELPER + 32)
        pcs.append(pc)

    def read(machine, access, address, size, value, unused):
        assert any(start <= address and address + size <= end for start, end in [
            (ENTRY, ENTRY + SIZE), (HELPER, HELPER + 36), (FIELDS, FIELDS + 12),
            (POINTER, POINTER + 4), (TABLE, TABLE + 256), (SP - 16, SP)])
        reads.append([address, size])

    def write(machine, access, address, size, value, unused):
        assert SP - 16 <= address and address + size <= SP
        writes.append([address, size, value])

    uc.hook_add(UC_HOOK_CODE, step)
    uc.hook_add(UC_HOOK_MEM_READ, read)
    uc.hook_add(UC_HOOK_MEM_WRITE, write)
    uc.emu_start(ENTRY, STOP + 4, count=200)
    assert state['actualReturns'] == 1 and state['actualHelperReturns'] == 2
    assert state['activeHelperReturn'] is None and uc.reg_read(UC_ARM_REG_SP) == SP
    assert [uc.reg_read(reg) for reg in REGISTERS[4:12]] == saved
    final_stack = bytes(uc.mem_read(STACK, 4096))
    assert final_stack[:0x7F0] == stack[:0x7F0] and final_stack[0x800:] == stack[0x800:]
    assert bytes(uc.mem_read(FIELDS, 12)) == fields and bytes(uc.mem_read(POINTER, 4)) == pointer
    assert bytes(uc.mem_read(TABLE, 256)) == table
    result = uc.reg_read(REGISTERS[0])
    return dict(state=state, result=result, modelPassed=result == expected(item), pcs=pcs,
                reads=reads, stackWrites=writes, registers=[uc.reg_read(reg) for reg in REGISTERS] +
                [uc.reg_read(UC_ARM_REG_CPSR)], stackSha256=hashlib.sha256(final_stack).hexdigest())
