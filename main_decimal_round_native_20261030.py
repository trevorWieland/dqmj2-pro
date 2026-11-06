import hashlib
import random
import struct
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
from main_format_wrappers_native_20261030 import REGS

ENTRY, DATA, STACK, STOP = 0x0201C2EC, 0x02500000, 0x027C0000, 0x02FF0000


def model(raw, keep, pointer):
    result, stores = bytearray(raw), []

    def store(offset, size, value):
        value &= (1 << (size * 8)) - 1
        result[offset:offset + size] = value.to_bytes(size, 'little')
        stores.append([pointer + offset, size, value])

    def zero():
        store(2, 2, 0)
        store(4, 1, 1)
        store(5, 1, 48)

    length = raw[4]
    if keep < 0:
        zero()
        return bytes(result), stores
    if keep >= length:
        return bytes(result), stores
    dropped = raw[5 + keep] - 48
    preceding = raw[4 + keep]
    carry = int(dropped > 5 or dropped == 5 and (any(x != 48 for x in raw[6 + keep:5 + length]) or preceding & 1))
    retained = keep
    while retained:
        position = retained - 1
        digit = raw[5 + position] - 48 + carry
        carry = int(digit > 9)
        if carry or digit == 0:
            retained -= 1
        else:
            store(5 + position, 1, digit + 48)
            break
    if carry:
        store(2, 2, int.from_bytes(raw[2:4], 'little') + 1)
        store(4, 1, 1)
        store(5, 1, 49)
    elif retained == 0:
        zero()
    else:
        store(4, 1, retained)
    return bytes(result), stores


def vectors():
    patterns = ['0', '4', '5', '6', '9', '10', '15', '25', '50', '55', '99', '1000', '1500', '2500', '5000', '5001', '5555', '9999', '12345678', '9' * 32, '5' + '0' * 31, '4' + '9' * 31, '0' * 32]
    for text in patterns:
        for keep in sorted({-2147483648, -1, 0, 1, len(text) // 2, len(text) - 1, len(text), len(text) + 1, 2147483647}):
            for exponent in [0, 32767, -32768]:
                for thumb in [False, True]:
                    yield text, keep, exponent, thumb
    randomizer = random.Random(0x1C2EC)
    for index in range(128):
        text = ''.join(str(randomizer.randrange(10)) for unused in range(randomizer.randrange(1, 33)))
        keep = randomizer.randrange(-1, len(text) + 3)
        exponent = randomizer.randrange(-32768, 32768)
        for thumb in [False, True]:
            yield text, keep, exponent, thumb


def execute(main, case, tag):
    text, keep, exponent, thumb = case
    assert 1 <= len(text) <= 32 and all('0' <= char <= '9' for char in text)
    memory = bytearray([0xA5]) * 0x1000
    offset = 0x100 + (tag % 4) * 2
    pointer = DATA + offset
    raw = bytearray([0xD3]) * 64
    raw[0] = [0, 1, 128, 255][tag % 4]
    raw[2:4] = struct.pack('<h', exponent)
    raw[4] = len(text)
    raw[5:5 + len(text)] = text.encode('ascii')
    memory[offset:offset + 64] = raw
    predicted_record, predicted_stores = model(raw, keep, pointer)
    predicted = bytearray(memory)
    predicted[offset:offset + 64] = predicted_record
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (DATA, 0x1000), (STACK, 0x8000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(DATA, bytes(memory))
    machine.mem_write(STACK, bytes([0x5A]) * 0x8000)
    machine.reg_write(UC_ARM_REG_CPSR, ((tag & 15) << 28) | (0xC0 if tag & 16 else 0) | 0x1F)
    for index, reg in enumerate(REGS):
        machine.reg_write(reg, (0x13579BDF * (index + 1) + tag) & 0xFFFFFFFF)
    machine.reg_write(REGS[0], pointer)
    machine.reg_write(REGS[1], keep & 0xFFFFFFFF)
    sp = STACK + 0x6000
    machine.reg_write(UC_ARM_REG_SP, sp)
    machine.reg_write(UC_ARM_REG_LR, STOP | int(thumb))
    saved = [machine.reg_read(reg) for reg in REGS[4:12]]
    stores, events, steps = [], [], [0]

    def code(uc, address, size, user):
        steps[0] += 1
        if address == STOP:
            events.append('actual-return')
            uc.emu_stop()
        else:
            assert ENTRY <= address < ENTRY + 292

    def store(uc, access, address, size, value, user):
        if DATA <= address < DATA + 0x1000:
            stores.append([address, size, value & ((1 << (size * 8)) - 1)])
        else:
            assert STACK <= address and address + size <= STACK + 0x8000

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, store)
    machine.emu_start(ENTRY, STOP + 4, count=10000, timeout=100000)
    assert events == ['actual-return'] and machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_SP) == sp
    assert [machine.reg_read(reg) for reg in REGS[4:12]] == saved
    assert bool(machine.reg_read(UC_ARM_REG_CPSR) & 32) == thumb
    assert stores == predicted_stores, (case, stores, predicted_stores)
    after = bytes(machine.mem_read(DATA, 0x1000))
    assert after == predicted, case
    assert bytes(machine.mem_read(0x02000000, len(main))) == main
    return {'actualReturn': True, 'dataSha256': hashlib.sha256(after).hexdigest(), 'stores': stores,
            'registers': [machine.reg_read(reg) for reg in REGS], 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'lr': machine.reg_read(UC_ARM_REG_LR), 'instructions': steps[0],
            'stackSha256': hashlib.sha256(bytes(machine.mem_read(STACK, 0x8000))).hexdigest()}
