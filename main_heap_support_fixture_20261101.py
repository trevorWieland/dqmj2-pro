import hashlib
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from main_list_unlink_fixture_20261101 import REGS

DATA, STACK, STOP = 0x02380000, 0x027F0000, 0x027FF000
ENTRIES = {0x0202ADFC: 44, 0x0202B9F4: 44, 0x0202BA20: 84}


def execute(image, entry, replacements, index, bound=256, require_model=True):
    rng = random.Random(entry * 100000 + index)
    page = bytearray(rng.randbytes(4096))
    registers = [rng.getrandbits(32) for unused in REGS]
    object_address = DATA + 0x500
    expected_result = None
    if entry == 0x0202ADFC:
        region = DATA + 0x100
        end = [object_address + 16, object_address + 20, object_address + 512,
               0, 0xFFFFFFFF, rng.getrandbits(32)][index % 6]
        signature = [0, 1, 0x4652, 0x5544, 0xFFFF, 0x10000, 0xFFFFFFFF, rng.getrandbits(32)][index // 6 % 8]
        struct.pack_into('<2I', page, 0x100, object_address, end)
        registers[:2] = [region, signature]
        expected = bytearray(page)
        struct.pack_into('<HH3I', expected, 0x500, signature & 0xFFFF, 0,
                         (end - object_address - 16) & 0xFFFFFFFF, 0, 0)
        expected_result = object_address
    else:
        list_address = DATA + 0x100
        offset = [0, 4, 12, 24][index % 4]
        length = 0 if entry == 0x0202B9F4 else index // 4 % 3
        head = DATA + (0x200 if length == 2 else 0x300) if length else 0
        tail = DATA + 0x300 if length else 0
        count = [length, 0xFFFF, 0xFFFE, 0x8000][index // 12 % 4]
        struct.pack_into('<2I2H', page, 0x100, head, tail, count, offset)
        if length:
            struct.pack_into('<2I', page, 0x300 + offset, DATA + 0x200 if length == 2 else 0, 0)
            if length == 2:
                struct.pack_into('<2I', page, 0x200 + offset, 0, tail)
        registers[:2] = [list_address, object_address]
        expected = bytearray(page)
        struct.pack_into('<2I', expected, 0x500 + offset, tail, 0)
        if tail:
            struct.pack_into('<I', expected, tail - DATA + offset + 4, object_address)
        else:
            struct.pack_into('<I', expected, 0x100, object_address)
        struct.pack_into('<I', expected, 0x104, object_address)
        struct.pack_into('<H', expected, 0x108, (count + 1) & 0xFFFF)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_write(0x02000000, image)
    for address, body in replacements.items():
        machine.mem_write(address, body)
    machine.mem_write(DATA, bytes(page))
    guards = rng.randbytes(8192)
    machine.mem_write(STACK - 4096, guards)
    cpsr = ((index % 16) << 28) | 0x10 | ((index // 2 % 4) << 6)
    machine.reg_write(UC_ARM_REG_CPSR, cpsr)
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    writes, calls, returned, own, lower, pending = [], [], [], set(), set(), []

    def code(uc, address, size, unused):
        if pending and address == pending[-1][1]:
            returned.append(pending.pop()[0])
        if entry <= address < entry + len(replacements.get(entry, bytes(ENTRIES[entry]))):
            own.update(range(address, address + size))
            return
        helper = 0x0202B9F4
        if helper <= address < helper + len(replacements.get(helper, bytes(44))):
            lower.update(range(address, address + size))
            if address == helper:
                calls.append([address, [uc.reg_read(register) for register in REGS[:2]]])
                pending.append((address, uc.reg_read(UC_ARM_REG_LR)))
            return
        raise AssertionError(('Unexpected native instruction', hex(address)))

    def write(uc, access, address, size, value, unused):
        if STACK - 4096 <= address and address + size <= STACK + 4096:
            return
        assert DATA <= address and address + size <= DATA + 4096
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(entry, STOP, timeout=1000000, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP and not pending
    assert machine.reg_read(UC_ARM_REG_SP) == STACK
    assert [machine.reg_read(register) for register in REGS[4:12]] == registers[4:12]
    assert machine.reg_read(UC_ARM_REG_CPSR) & 0xFF == cpsr & 0xFF
    assert bytes(machine.mem_read(STACK - 4096, 256)) == guards[:256]
    assert bytes(machine.mem_read(STACK + 4096 - 256, 256)) == guards[-256:]
    actual = bytes(machine.mem_read(DATA, 4096))
    result = machine.reg_read(UC_ARM_REG_R0)
    passed = actual == expected and (expected_result is None or result == expected_result)
    if require_model:
        assert passed, (hex(entry), index, result, expected_result)
    record = dict(index=index, modelPassed=passed, result=result, calls=calls, writes=writes,
        pageSha256=hashlib.sha256(actual).hexdigest(), actualTopReturns=1,
        actualNativeDependencyReturns=len(returned), returnedHelpers=returned, suppliedCalls=0,
        observed=sorted(own), helperObserved=sorted(lower),
        registers=[machine.reg_read(register) for register in REGS], cpsr=machine.reg_read(UC_ARM_REG_CPSR))
    del machine
    return record
