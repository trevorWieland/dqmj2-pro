import hashlib
import math
import struct
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
from main_format_wrappers_native_20261030 import REGS

ENTRY, DATA, STACK, STOP = 0x0201C410, 0x02500000, 0x027C0000, 0x02FF0000
HELPERS = {0x020236E8, 0x0201C2EC, 0x0202516C}


def expected(bits, conversion, precision, sign, alternate, end):
    if precision > 509:
        return 0, []
    stores = [[end - 1, 1, 0]]
    if conversion in 'eE' and precision >= 505:
        assert bits == 0x3FF8000000000000
        for byte in ('+00'[::-1] + conversion).encode():
            stores.append([end - 1 - len(stores), 1, byte])
        return 0, stores
    value = struct.unpack('<d', struct.pack('<Q', bits))[0]
    special = bits & 0x7FF0000000000000 == 0x7FF0000000000000
    if special:
        text = 'nan' if bits & 0xFFFFFFFFFFFFF else 'inf'
        if conversion.isupper():
            text = text.upper()
        if bits >> 63:
            text = '-' + text
        pointer = end - len(text) - 1
        return pointer, [[pointer + index, 1, byte] for index, byte in enumerate(text.encode() + bytes(1))]
    marker = '+' if sign == 1 else ' ' if sign == 2 else ''
    text = format(value, marker + ('#' if alternate else '') + '.' + str(precision) + conversion)
    assert len(text) + 1 <= 512
    for byte in text[::-1].encode():
        stores.append([end - 1 - len(stores), 1, byte])
    return end - len(text) - 1, stores


def vectors():
    values = [0.0, -0.0, 1.5, -2.25, 0.125, 32.125, 127.9375, 1024.0, -65536.125, 0.0009765625]
    for value in values:
        bits = struct.unpack('<Q', struct.pack('<d', value))[0]
        for conversion in 'fFeEgG':
            for precision in [6, 12, 20]:
                for thumb in [False, True]:
                    yield bits, conversion, precision, 0, 0, thumb
    for bits in [0x7FF0000000000000, 0xFFF0000000000000, 0x7FF8000000000001, 0xFFF8000000000001]:
        for conversion in 'fFeEgG':
            for sign in range(3):
                yield bits, conversion, 6, sign, 0, bool(sign & 1)
    for value in [0.0, 1.5, -2.25, 32.125]:
        bits = struct.unpack('<Q', struct.pack('<d', value))[0]
        for conversion in 'fFeEgG':
            for sign in range(3):
                for alternate in [0, 1]:
                    yield bits, conversion, 6, sign, alternate, bool(alternate)
    for conversion in 'fFeEgG':
        yield 0x3FF8000000000000, conversion, 510, 0, 0, False
    for conversion in 'eE':
        for precision in [505, 506, 507, 508, 509]:
            yield 0x3FF8000000000000, conversion, precision, 0, 0, bool(precision & 1)
    for precision in [0, 1, 2, 3, 4, 500, 508, 509]:
        yield 0x0000000000000000, 'f', precision, 0, 0, False
        yield 0x3FF8000000000000, 'f', max(1, precision), 0, 0, True


def execute(main, case, tag):
    bits, conversion, precision, sign, alternate, thumb = case
    end = DATA + 0x1000 + tag % 4
    result, expected_stores = expected(bits, conversion, precision, sign, alternate, end)
    initial = bytearray([0xA5]) * 0x4000
    predicted = bytearray(initial)
    for address, size, value in expected_stores:
        predicted[address - DATA:address - DATA + size] = value.to_bytes(size, 'little')
    descriptor = struct.pack('<6B2xii', tag % 256, sign, tag * 7 % 256, alternate, tag * 13 % 256,
                             ord(conversion), -2147483648 + tag, precision)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (DATA, 0x4000), (STACK, 0x8000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(DATA, bytes(initial))
    machine.mem_write(STACK, bytes([0x5A]) * 0x8000)
    sp = STACK + 0x6000
    machine.mem_write(sp, descriptor[4:])
    machine.reg_write(UC_ARM_REG_CPSR, ((tag & 15) << 28) | (0xC0 if tag & 16 else 0) | 0x1F)
    for index, reg in enumerate(REGS):
        machine.reg_write(reg, (0x13579BDF * (index + 1) + tag) & 0xFFFFFFFF)
    for reg, value in zip(REGS[:4], [bits & 0xFFFFFFFF, bits >> 32, end, int.from_bytes(descriptor[:4], 'little')]):
        machine.reg_write(reg, value)
    machine.reg_write(UC_ARM_REG_SP, sp)
    machine.reg_write(UC_ARM_REG_LR, STOP | int(thumb))
    preserved = [machine.reg_read(reg) for reg in REGS[4:12]]
    stores, pending, returns, events, steps = [], [], [], [], [0]

    def code(uc, address, size, user):
        assert not ENTRY + 1848 <= address < ENTRY + 1892
        steps[0] += 1
        if pending and address == pending[-1][1]:
            target, return_pc, frame = pending.pop()
            assert uc.reg_read(UC_ARM_REG_SP) == frame
            returns.append(target)
        if address in HELPERS:
            if address == 0x020236E8:
                form, low, high, destination = [uc.reg_read(reg) for reg in REGS[:4]]
                assert bytes(uc.mem_read(form, 1)) == bytes(1)
                assert int.from_bytes(uc.mem_read(form + 2, 2), 'little') == 32
                assert low | high << 32 == bits
                assert STACK <= destination < STACK + 0x8000
            pending.append((address, uc.reg_read(UC_ARM_REG_LR), uc.reg_read(UC_ARM_REG_SP)))
        if address == STOP:
            events.append('actual-return')
            uc.emu_stop()
        else:
            assert 0x02000000 <= address < 0x02400000

    def store(uc, access, address, size, value, user):
        if DATA <= address < DATA + 0x4000:
            assert end - 512 <= address and address + size <= end
            stores.append([address, size, value & ((1 << (size * 8)) - 1)])
        else:
            assert STACK <= address and address + size <= STACK + 0x8000

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, store)
    machine.emu_start(ENTRY, STOP + 4, count=1000000, timeout=1000000)
    assert events == ['actual-return'] and not pending
    assert machine.reg_read(UC_ARM_REG_PC) == STOP and machine.reg_read(UC_ARM_REG_SP) == sp
    assert machine.reg_read(REGS[0]) == result, (case, machine.reg_read(REGS[0]), result)
    assert [machine.reg_read(reg) for reg in REGS[4:12]] == preserved
    assert bool(machine.reg_read(UC_ARM_REG_CPSR) & 32) == thumb
    assert stores == expected_stores, (case, stores[:8], expected_stores[:8])
    actual = bytes(machine.mem_read(DATA, 0x4000))
    assert actual == predicted, case
    assert bytes(machine.mem_read(0x02000000, len(main))) == main
    assert returns.count(0x020236E8) == int(precision <= 509)
    return {'actualReturn': True, 'return': result, 'registers': [machine.reg_read(reg) for reg in REGS],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'lr': machine.reg_read(UC_ARM_REG_LR),
            'dataSha256': hashlib.sha256(actual).hexdigest(), 'stores': stores,
            'stackSha256': hashlib.sha256(bytes(machine.mem_read(STACK, 0x8000))).hexdigest(),
            'nativeHelperReturns': returns, 'instructions': steps[0]}
