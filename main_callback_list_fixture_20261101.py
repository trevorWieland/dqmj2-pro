import hashlib
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, SIZE = 0x0202DDA0, 100
DATA, GLOBAL, IO, STACK, STOP = 0x02380000, 0x020ED000, 0x04000000, 0x027F0000, 0x027FF000
CALLBACKS = {0x02029D5C: (0xD24, 0x354), 0x02029E68: (0xD1A, 0x35C)}
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def execute(image, body, index, bound=512, require_model=True):
    rng = random.Random(ENTRY * 100000 + index)
    pages = [bytearray(rng.randbytes(4096)) for unused in range(3)]
    user = [0, 1, 0xFFFF, 0x10000, 0x80000000, 0xFFFFFFFF, rng.getrandbits(32)][index % 7]
    selector = [0, 1, 2, 3, 126, 127, 254, 255, 256, 0xFFFFFFFF][index // 7 % 10]
    length = [0, 1, 2, 3, 4][index // 70 % 5]
    nodes = [DATA + 0x100 + slot * 0x300 for slot in range(length)]
    expected_calls, expected_writes = [], []
    for slot, node in enumerate(nodes):
        offset = node - DATA
        count = [0, 1, 2, 127, 255][(index // 350 + slot) % 5]
        flags = [0, 0xFF, 0x100, 0x1AB, 0xFFFF][(index // 5 + slot) % 5]
        callback = [0, 0x02029D5C, 0x02029E68][(index // 3 + slot) % 3]
        struct.pack_into('<I', pages[0], offset + 0xC, callback)
        struct.pack_into('<I', pages[0], offset + 0x10, nodes[slot + 1] if slot + 1 < length else 0)
        pages[0][offset + 0x19] = count
        if selector < count:
            struct.pack_into('<H', pages[0], offset + 0x1A + selector * 2, flags)
            if flags & 0x100 and callback:
                expected_calls.append([callback, [user, node, flags & 0xFF]])
    for offset, unused in CALLBACKS.values():
        struct.pack_into('<H', pages[1], offset, [0, 1, 0xFFFF, rng.getrandbits(16)][index % 4])
    expected = [bytearray(page) for page in pages]
    for callback, arguments in expected_calls:
        offset, hardware = CALLBACKS[callback]
        struct.pack_into('<H', expected[1], offset, user & 0xFFFF)
        struct.pack_into('<H', expected[2], hardware, user & 0xFFFF)
        stores = [[GLOBAL + offset, 2, user & 0xFFFF], [IO + hardware, 2, user & 0xFFFF]]
        expected_writes.extend(stores if callback == 0x02029D5C else stores[::-1])
    initial = [rng.getrandbits(32) for unused in REGS]
    initial[:3] = [user, nodes[0] if nodes else 0, selector]
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_map(IO, 4096)
    machine.mem_write(0x02000000, image)
    machine.mem_write(ENTRY, body)
    for address, page in zip([DATA, GLOBAL, IO], pages):
        machine.mem_write(address, bytes(page))
    guards = rng.randbytes(8192)
    machine.mem_write(STACK - 4096, guards)
    cpsr = ((index % 16) << 28) | 0x10 | ((index // 2 % 4) << 6)
    machine.reg_write(UC_ARM_REG_CPSR, cpsr)
    for register, value in zip(REGS, initial):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, writes, observed, callback_observed, returned_callbacks = [], [], set(), set(), []

    def code(uc, address, size, unused):
        if ENTRY <= address < ENTRY + len(body):
            observed.update(range(address, address + size))
            return
        for callback in CALLBACKS:
            if callback <= address < callback + 32:
                callback_observed.update(range(address, address + size))
                if address == callback:
                    calls.append([callback, [uc.reg_read(register) for register in REGS[:3]]])
                if address == callback + 28:
                    returned_callbacks.append(callback)
                return
        raise AssertionError(('Unexpected native instruction', hex(address)))

    def write(uc, access, address, size, value, unused):
        if STACK - 4096 <= address and address + size <= STACK + 4096:
            return
        assert any(start <= address and address + size <= start + 4096 for start in [DATA, GLOBAL, IO])
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP, timeout=1000000, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_SP) == STACK
    assert [machine.reg_read(register) for register in REGS[4:12]] == initial[4:12]
    assert machine.reg_read(UC_ARM_REG_CPSR) & 0xFF == cpsr & 0xFF
    assert bytes(machine.mem_read(STACK - 4096, 256)) == guards[:256]
    assert bytes(machine.mem_read(STACK + 4096 - 256, 256)) == guards[-256:]
    actual = [bytes(machine.mem_read(address, 4096)) for address in [DATA, GLOBAL, IO]]
    result = machine.reg_read(UC_ARM_REG_R0)
    passed = actual == expected and calls == expected_calls and writes == expected_writes and result == int(bool(expected_calls))
    assert len(returned_callbacks) == len(calls)
    if require_model:
        assert passed, (index, calls, expected_calls, writes, expected_writes, result)
    record = dict(index=index, modelPassed=passed, result=result, calls=calls, writes=writes,
                  pagesSha256=hashlib.sha256(b''.join(actual)).hexdigest(), actualTopReturns=1,
                  suppliedCalls=0, actualNativeDependencyReturns=len(returned_callbacks),
                  observed=sorted(observed), helperObserved=sorted(callback_observed),
                  registers=[machine.reg_read(register) for register in REGS], cpsr=machine.reg_read(UC_ARM_REG_CPSR))
    del machine
    return record
