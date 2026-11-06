import functools
import hashlib
import random
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR
from match_runtime import REGISTERS


ENTRY, SIZE = 0x02022D80, 900
DATA, STACK, SP, STOP = 0x02380000, 0x03030000, 0x0303F000, 0x0F000000
HELPERS = {0x02022B60: 388, 0x02022CE4: 156, 0x02022A04: 76}
SEEDS = {-64, -53, -32, -16, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8}
EXPONENTS = sorted(set(range(-64, 65)) | {-1024, -129, -128, -127, -100, -65, 65, 100, 127, 128, 129, 1024})


def product(a, b):
    x, ex = a
    y, ey = b
    number = x * y
    length = len(str(number))
    exponent = ex + ey + length - len(str(x)) - len(str(y)) + 1
    if length > 32:
        divisor = 10 ** (length - 32)
        quotient, remainder = divmod(number, divisor)
        number = quotient + (2 * remainder > divisor or 2 * remainder == divisor and quotient & 1)
        if number >= 10 ** 32:
            number = 10 ** 31
            exponent += 1
    return number, (exponent + 32768) % 65536 - 32768


@functools.cache
def model(exponent):
    if exponent in SEEDS:
        number = 2 ** exponent if exponent >= 0 else 5 ** -exponent
        text = str(number)
        result_exponent = len(text) - 1 + min(exponent, 0)
        if len(text) > 32:
            number = int(text[:32]) + 1
        return number, result_exponent
    half = abs(exponent) // 2 * (-1 if exponent < 0 else 1)
    value = model(half)
    value = product(value, value)
    if exponent & 1:
        value = product(value, (2, 0) if exponent > 0 else (5, -1))
    return value


def execute(original, code, index):
    exponent = EXPONENTS[index]
    rng = random.Random(0x20261031022D80 + index)
    page = rng.randbytes(4096)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, original)
    uc.mem_write(ENTRY, code)
    uc.mem_write(DATA, page)
    uc.mem_map(STACK, 65536)
    uc.mem_write(STACK, bytes([0xA5]) * 65536)
    uc.mem_map(STOP, 4096)
    uc.mem_write(STOP, bytes.fromhex('1eff2fe1'))
    control = 0x10 | ((index // 16 & 3) << 6)
    uc.reg_write(UC_ARM_REG_CPSR, index % 16 << 28 | control)
    registers = [rng.getrandbits(32) for unused in REGISTERS]
    registers[:2] = [DATA + 0x100, exponent & 0xFFFFFFFF]
    registers[-2:] = [SP, STOP | (index & 1)]
    for register, value in zip(REGISTERS, registers):
        uc.reg_write(register, value)
    pcs, writes, pending, returns = set(), [], [], []
    stopped, instructions, physical_returns = False, 0, 0

    def instruction(engine, address, width, user):
        nonlocal stopped, instructions, physical_returns
        instructions += 1
        if pending and address == pending[-1][1]:
            physical_returns += 1
            while pending and address == pending[-1][1]:
                returns.append(pending.pop()[0])
        if address == STOP:
            assert not pending
            stopped = True
            engine.emu_stop()
            return
        if address == ENTRY or address in HELPERS:
            pending.append((address, engine.reg_read(UC_ARM_REG_LR) & ~1))
        assert ENTRY <= address < ENTRY + len(code) or any(a <= address < a + size for a, size in HELPERS.items()), hex(address)
        pcs.add(address)

    def memory(engine, access, address, width, value, user):
        assert DATA + 0x100 <= address and address + width <= DATA + 0x126 or SP - 0x4000 <= address < SP
        if DATA <= address < DATA + 4096:
            writes.append([address, width, value])

    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_WRITE, memory)
    uc.emu_start(ENTRY, STOP + 4, count=2000000)
    assert stopped and uc.reg_read(UC_ARM_REG_SP) == SP
    assert uc.reg_read(UC_ARM_REG_CPSR) & 255 == control | ((index & 1) << 5)
    for i in range(4, 12):
        assert uc.reg_read(REGISTERS[i]) == registers[i]
    assert bytes(uc.mem_read(STACK, SP - STACK - 0x4000)) == bytes([0xA5]) * (SP - STACK - 0x4000)
    assert bytes(uc.mem_read(SP, STACK + 65536 - SP)) == bytes([0xA5]) * (STACK + 65536 - SP)
    image = bytes(uc.mem_read(DATA, 4096))
    record = image[0x100:0x126]
    number, expected_exponent = model(exponent)
    expected_digits = [int(value) for value in str(number)]
    digits = list(record[5:5 + record[4]])
    actual_exponent = int.from_bytes(record[2:4], 'little', signed=True)
    passed = record[0] == 0 and record[1] == page[0x101] and record[37] == page[0x125]
    passed = passed and image[:0x100] == page[:0x100] and image[0x126:] == page[0x126:]
    passed = passed and digits == expected_digits and actual_exponent == expected_exponent
    return dict(modelPassed=passed, exponent=exponent, digits=digits, expectedDigits=expected_digits,
        decimalExponent=actual_exponent, expectedExponent=expected_exponent, writes=writes,
        pageSha256=hashlib.sha256(image).hexdigest(), pcs=sorted(pcs), instructions=instructions,
        logicalNativeReturns=returns, physicalNativeReturnInstructions=physical_returns,
        registers=[uc.reg_read(register) for register in REGISTERS], cpsr=uc.reg_read(UC_ARM_REG_CPSR))
