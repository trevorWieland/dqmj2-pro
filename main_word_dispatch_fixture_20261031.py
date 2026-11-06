import hashlib
import random
import struct
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR
from match_runtime import REGISTERS

ENTRY, SIZE = 0x02005BD8, 140
SHARED, TABLE = 0x027E0000, 0x020E335C
STACK, STOP = 0x03030000, 0x0F000000


def recipe(index, mask):
    rng = random.Random(0xBD800000 + index)
    return dict(index=index, mask=mask, shared=rng.randbytes(88).hex(), table=rng.randbytes(96).hex())


def recipes():
    masks = [0, 0xFFFFFFFF, 0x80000000, 0xFFC00000, 0x003FFFFF]
    masks.extend(1 << bit for bit in range(32))
    masks.extend((1 << bit) | (1 << other) for bit in range(22) for other in range(bit + 1, 22))
    rng = random.Random(0x5BD8)
    masks.extend(rng.getrandbits(32) for unused in range(256))
    return [recipe(index, mask) for index, mask in enumerate(masks)]


def expected(item):
    bit = next((bit for bit in range(22) if item['mask'] & (1 << bit)), None)
    if bit is None:
        return 0
    if 8 <= bit <= 11:
        return struct.unpack_from('<I', bytes.fromhex(item['table']), (bit - 8) * 12)[0]
    if 3 <= bit <= 6:
        return struct.unpack_from('<I', bytes.fromhex(item['table']), (bit + 1) * 12)[0]
    return struct.unpack_from('<I', bytes.fromhex(item['shared']), bit * 4)[0]


def execute(main, code, item):
    rng = random.Random(0x5BD80000 + item['index'])
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, main)
    uc.mem_write(ENTRY, code)
    uc.mem_map(SHARED, 4096)
    shared, table = bytes.fromhex(item['shared']), bytes.fromhex(item['table'])
    uc.mem_write(SHARED, shared)
    uc.mem_write(TABLE, table)
    uc.mem_map(STACK, 4096)
    stack = rng.randbytes(4096)
    uc.mem_write(STACK, stack)
    uc.mem_map(STOP, 4096)
    uc.reg_write(UC_ARM_REG_CPSR, ((item['index'] & 15) << 28) | 0x1F)
    for reg in REGISTERS:
        uc.reg_write(reg, rng.getrandbits(32))
    uc.reg_write(REGISTERS[0], item['mask'])
    uc.reg_write(UC_ARM_REG_SP, STACK + 2048)
    uc.reg_write(UC_ARM_REG_LR, STOP | (item['index'] & 1))
    saved = [uc.reg_read(reg) for reg in REGISTERS[4:12]]
    state = dict(actualReturns=0, instructions=0)
    reads, pcs = [], []

    def step(machine, pc, width, unused):
        if pc == STOP:
            state['actualReturns'] += 1
            machine.emu_stop()
            return
        if not ENTRY <= pc < ENTRY + SIZE - 8 or width != 4:
            raise ValueError('Unexpected native body, literal execution, or instruction mode')
        pcs.append(pc)
        state['instructions'] += 1

    def read(machine, access, address, size, value, unused):
        if not any(start <= address and address + size <= end for start, end in [
                (ENTRY, ENTRY + SIZE), (SHARED, SHARED + 88), (TABLE, TABLE + 96)]):
            raise ValueError('Unexpected native dependency read')
        reads.append([address, size])

    def write(machine, access, address, size, value, unused):
        raise ValueError('Read-only native routine attempted a memory write')

    uc.hook_add(UC_HOOK_CODE, step)
    uc.hook_add(UC_HOOK_MEM_READ, read)
    uc.hook_add(UC_HOOK_MEM_WRITE, write)
    uc.emu_start(ENTRY, STOP + 4, count=600)
    if state['actualReturns'] != 1:
        raise ValueError('Bounded routine did not actually return')
    assert uc.reg_read(UC_ARM_REG_SP) == STACK + 2048
    assert [uc.reg_read(reg) for reg in REGISTERS[4:12]] == saved
    assert bytes(uc.mem_read(STACK, 4096)) == stack
    assert bytes(uc.mem_read(SHARED, 88)) == shared
    assert bytes(uc.mem_read(TABLE, 96)) == table
    return dict(state=state, returnValue=uc.reg_read(REGISTERS[0]), reads=reads, pcs=pcs,
                registers=[uc.reg_read(reg) for reg in REGISTERS] + [uc.reg_read(UC_ARM_REG_CPSR)],
                stackSha256=hashlib.sha256(stack).hexdigest(),
                modelPassed=uc.reg_read(REGISTERS[0]) == expected(item))
