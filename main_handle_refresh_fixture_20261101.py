import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, SIZE, DATA, STACK, STOP = 0x020296B0, 96, 0x02380000, 0x027F0000, 0x027FF000
HELPERS = {0x02029688: 40, 0x02029618: 92, 0x0202EBC0: 84, 0x0202EB4C: 116}
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def word(page, offset):
    return struct.unpack_from('<I', page, offset)[0]


def put(page, offset, value):
    struct.pack_into('<I', page, offset, value & 0xFFFFFFFF)


def scenario(index):
    rng = random.Random(ENTRY * 10000 + index)
    page = bytearray(rng.randbytes(4096))
    page[0xA] = (index % 256) & ~4
    incoming = [0, DATA + 0x800, 0xFFFFFFFF, 0x80000000][index // 128 % 4]
    current = DATA + 0x600 if index // 512 % 2 else 0
    put(page, 0x60, incoming)
    put(page, 0x64, current)
    lists = []
    matched_list = index // 1024 % 4
    for position, header in enumerate([0x14, 0x1C, 0x24]):
        nodes = [DATA + 0x400 + position * 0x80, DATA + 0x440 + position * 0x80]
        if index // 4096 & 1:
            nodes = []
        if current and position == matched_list:
            nodes.insert(0 if index // 256 & 1 else len(nodes), current)
        lists.append((header, nodes))
        put(page, header, nodes[0] if nodes else 0)
        for slot, node in enumerate(nodes):
            put(page, node - DATA + 0x10, nodes[slot + 1] if slot + 1 < len(nodes) else 0)
    expected = bytearray(page)
    if incoming:
        if current:
            removed = False
            for header, nodes in lists:
                if current in nodes:
                    offset = nodes.index(current)
                    following = nodes[offset + 1] if offset + 1 < len(nodes) else 0
                    put(expected, header if offset == 0 else nodes[offset - 1] - DATA + 0x10, following)
                    put(expected, current - DATA + 0x10, 0)
                    removed = True
                    break
            if removed:
                put(expected, 0xC, word(expected, 0xC) | 0x10)
            put(expected, 0x64, 0)
            put(expected, 0xF8, 0)
        put(expected, 0x64, incoming)
        put(expected, 0xF8, 0x1000)
        if page[0xA] & 1:
            expected[0xA] = 4
    return page, expected, int(bool(incoming))


def execute(image, body, index, bound=2048, require_model=True):
    before, expected, expected_result = scenario(index)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_write(0x02000000, image)
    machine.mem_write(ENTRY, body)
    machine.mem_write(DATA, bytes(before))
    initial = [0xA5120000 + slot * 0x100 + index for slot in range(13)]
    machine.reg_write(UC_ARM_REG_CPSR, ((index % 16) << 28) | 0x10)
    for register, value in zip(REGS, initial):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_R0, DATA)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    frames, returned, observed, writes = [], [], set(), []

    def watch(uc, address, length, unused):
        if frames and address == frames[-1]['lr'] and uc.reg_read(UC_ARM_REG_SP) == frames[-1]['sp']:
            frame = frames.pop()
            assert [uc.reg_read(register) for register in REGS[4:12]] == frame['preserved']
            assert uc.reg_read(UC_ARM_REG_CPSR) & 0x3F == 0x10
            returned.append(frame['entry'])
        if address in HELPERS:
            frames.append(dict(entry=address, lr=uc.reg_read(UC_ARM_REG_LR), sp=uc.reg_read(UC_ARM_REG_SP),
                preserved=[uc.reg_read(register) for register in REGS[4:12]]))
        own = ENTRY <= address < ENTRY + len(body)
        assert own or any(start <= address < start + size for start, size in HELPERS.items()), hex(address)
        if own:
            observed.update(range(address, address + length))

    def memory_write(uc, access, address, size, value, unused):
        assert DATA <= address and address + size <= DATA + 4096 or STACK - 4096 <= address and address + size <= STACK
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, watch)
    machine.hook_add(UC_HOOK_MEM_WRITE, memory_write)
    machine.emu_start(ENTRY, STOP, timeout=1000000, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP and not frames
    assert machine.reg_read(UC_ARM_REG_SP) == STACK
    assert machine.reg_read(UC_ARM_REG_CPSR) & 0x3F == 0x10
    assert [machine.reg_read(register) for register in REGS[4:12]] == initial[4:12]
    after = bytes(machine.mem_read(DATA, 4096))
    result = machine.reg_read(UC_ARM_REG_R0)
    passed = after == expected and result == expected_result
    if require_model:
        assert passed, (index, result, expected_result, [i for i,(a,b) in enumerate(zip(after, expected)) if a != b][:8])
    record = dict(index=index, result=result, modelPassed=passed, stateSha256=hashlib.sha256(after).hexdigest(),
        actualTopReturns=1, actualNativeDependencyReturns=len(returned), returnedHelpers=returned,
        suppliedCalls=0, observed=sorted(observed), writes=writes,
        registers=[machine.reg_read(register) for register in REGS], lr=machine.reg_read(UC_ARM_REG_LR), cpsr=machine.reg_read(UC_ARM_REG_CPSR))
    del machine
    return record
