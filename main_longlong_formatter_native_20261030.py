import hashlib
import struct
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
from main_format_wrappers_native_20261030 import REGS

ENTRY, DIVIDE, MODULUS, DATA, STACK, STOP = 0x0201BB14, 0x020260DC, 0x020260E8, 0x02500000, 0x027C0000, 0x02FF0000


def model(word, conversion, justification, sign, alternate, precision, width, end):
    signed = word if word < 0x8000000000000000 else word - 0x10000000000000000
    stores = [[end - 1, 1, 0]]
    if not word and precision == 0 and not (alternate and conversion == 'o'):
        return end - 1, stores
    negative = conversion in 'di' and signed < 0
    magnitude = abs(signed) if conversion in 'di' else word
    kind = 'd' if conversion in 'diu' else conversion
    digits = format(magnitude, kind)
    pointer = end - 1
    for byte in digits[::-1].encode('ascii'):
        pointer -= 1
        stores.append([pointer, 1, byte])
    if conversion == 'o' and alternate and digits[0] != '0':
        pointer -= 1
        stores.append([pointer, 1, 48])
        digits = '0' + digits
    if conversion not in 'di':
        sign = 0
    target = precision
    if justification == 2:
        target = width - int(negative or sign != 0) - (2 if conversion in 'xX' and alternate else 0)
    if len(digits) + 1 + target > 509:
        return 0, stores
    padding = max(0, target - len(digits))
    for index in range(padding):
        pointer -= 1
        stores.append([pointer, 1, 48])
    if conversion in 'xX' and alternate:
        for byte in [ord(conversion), 48]:
            pointer -= 1
            stores.append([pointer, 1, byte])
    prefix = '-' if negative else '+' if sign == 1 else ' ' if sign == 2 else ''
    if prefix:
        pointer -= 1
        stores.append([pointer, 1, ord(prefix)])
    return pointer, stores


def execute(main, case, tag):
    word, conversion, justification, sign, alternate, precision, width, alignment = case
    end = DATA + 0x1200 + alignment
    expected_return, expected_stores = model(word, conversion, justification, sign, alternate, precision, width, end)
    expected = bytearray([0xA5]) * 0x4000
    for address, size, value in expected_stores:
        assert end - 512 <= address < end
        expected[address - DATA] = value
    descriptor = struct.pack('<6B2xii', justification, sign, tag % 256, alternate, (tag * 17) % 256,
                             ord(conversion), width, precision)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (DATA, 0x4000), (STACK, 0x8000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(DATA, bytes([0xA5]) * 0x4000)
    machine.mem_write(STACK, bytes([0x5A]) * 0x8000)
    sp = STACK + 0x6000
    machine.mem_write(sp, descriptor[4:])
    machine.reg_write(UC_ARM_REG_CPSR, ((tag & 15) << 28) | 0x1F)
    for index, reg in enumerate(REGS):
        machine.reg_write(reg, (0x13579BDF * (index + 1) + tag) & 0xFFFFFFFF)
    for reg, value in zip(REGS[:4], [word & 0xFFFFFFFF, word >> 32, end, int.from_bytes(descriptor[:4], 'little')]):
        machine.reg_write(reg, value)
    machine.reg_write(UC_ARM_REG_SP, sp)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    saved = [machine.reg_read(reg) for reg in REGS[4:12]]
    events, stores, pending, returns, steps = [], [], [], [], [0]

    def code(uc, address, size, user):
        assert not ENTRY + 760 <= address < ENTRY + 764
        steps[0] += 1
        if pending and address == pending[-1][0]:
            return_pc, saved_sp, numerator, divisor, helper = pending.pop()
            quotient, remainder = divmod(numerator, divisor)
            assert uc.reg_read(UC_ARM_REG_SP) == saved_sp
            expected_arithmetic = quotient if helper == DIVIDE else remainder
            assert uc.reg_read(REGS[0]) | uc.reg_read(REGS[1]) << 32 == expected_arithmetic
            returns.append([numerator, divisor, quotient, remainder])
        if address in (DIVIDE, MODULUS):
            numerator = uc.reg_read(REGS[0]) | uc.reg_read(REGS[1]) << 32
            divisor = uc.reg_read(REGS[2]) | uc.reg_read(REGS[3]) << 32
            assert divisor == (8 if conversion == 'o' else 16 if conversion in 'xX' else 10)
            pending.append((uc.reg_read(UC_ARM_REG_LR), uc.reg_read(UC_ARM_REG_SP), numerator, divisor, address))
        elif address == STOP:
            events.append('actual-return')
            uc.emu_stop()
        else:
            assert 0x02000000 <= address < 0x02400000

    def write(uc, access, address, size, value, user):
        if DATA <= address < DATA + 0x4000:
            assert end - 512 <= address and address + size <= end
            stores.append([address, size, value & ((1 << (8 * size)) - 1)])
        else:
            assert STACK <= address and address + size <= STACK + 0x8000

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP + 4, count=200000, timeout=1000000)
    assert events == ['actual-return'] and not pending
    assert machine.reg_read(UC_ARM_REG_PC) == STOP and machine.reg_read(UC_ARM_REG_SP) == sp
    assert machine.reg_read(REGS[0]) == expected_return, case
    assert [machine.reg_read(reg) for reg in REGS[4:12]] == saved
    assert stores == expected_stores, case
    assert bytes(machine.mem_read(DATA, 0x4000)) == expected
    assert bytes(machine.mem_read(0x02000000, len(main))) == main
    return {'actualReturn': True, 'return': expected_return, 'registers': [machine.reg_read(reg) for reg in REGS],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'lr': machine.reg_read(UC_ARM_REG_LR),
            'stackSha256': hashlib.sha256(bytes(machine.mem_read(STACK, 0x8000))).hexdigest(),
            'dataSha256': hashlib.sha256(bytes(expected)).hexdigest(),
            'orderedStoresSha256': hashlib.sha256(repr(stores).encode()).hexdigest(), 'orderedStoreCount': len(stores),
            'actualArithmeticHelperReturns': len(returns), 'divisionReturnsSha256': hashlib.sha256(repr(returns).encode()).hexdigest(),
            'instructions': steps[0]}


def vectors():
    words = [0, 1, 9, 10, 15, 16, 17, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, 0x100000000,
             0x7FFFFFFFFFFFFFFF, 0x8000000000000000, 0xFFFFFFFFFFFFFFFF, 0x8765432112345678, 0x8000000000000001]
    precisions = [-1, 0, 1, 4, 8, 499, 500, 506, 507, 508, 509, 510]
    widths = [0, 1, 8, 499, 509, 510]
    index = 0
    for word in words:
        for conversion in 'diuoxX':
            for justification in range(3):
                for sign in range(3):
                    for alternate in range(2):
                        yield word, conversion, justification, sign, alternate, precisions[index % len(precisions)], widths[(index // 3) % len(widths)], index % 4
                        index += 1
    for precision in range(-1, 513):
        for conversion in 'diuoxX':
            yield 17, conversion, 1, 1, 1, precision, 8, index % 4
            index += 1
