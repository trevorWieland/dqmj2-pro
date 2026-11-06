import hashlib
import random
import re
import match_runtime
from project import ROOT
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR
from match_runtime import REGISTERS
from main_decimal_pow2_fixture_20261031 import model as power, product


ENTRY, SIZE = 0x02023568, 384
DATA, STACK, SP, STOP = 0x02380000, 0x03030000, 0x0303F000, 0x0F000000
EDGES = [0, 1 << 63, 1, 0x8000000000000001, 0x000FFFFFFFFFFFFF, 0x0010000000000000,
    0x3FF0000000000000, 0xBFF0000000000000, 0x3FF8000000000000, 0x3FF0000000000001,
    0x7FEFFFFFFFFFFFFF, 0xFFEFFFFFFFFFFFFF, 0x7FF0000000000000, 0xFFF0000000000000,
    0x7FF8000000000000, 0xFFF0000000000001]


def argument(index):
    return EDGES[index] if index < len(EDGES) else random.Random(20261031023568 + index).getrandbits(64)


def expected(bits):
    sign = bits >> 63
    exponent = bits >> 52 & 2047
    mantissa = bits & ((1 << 52) - 1)
    if exponent == 2047:
        return sign, 0, [ord('N') if mantissa else ord('I')]
    if exponent == 0 and mantissa == 0:
        return sign, 0, [0]
    if exponent:
        mantissa |= 1 << 52
    binary_exponent = exponent - 1023 - 52 if exponent else -1074
    trailing = (mantissa & -mantissa).bit_length() - 1
    mantissa >>= trailing
    binary_exponent += trailing
    number, decimal_exponent = product((mantissa, len(str(mantissa)) - 1), power(binary_exponent))
    return sign, decimal_exponent, [int(value) for value in str(number)]


def execute(original, code, index):
    bits = argument(index)
    rng = random.Random(2026103102356800 + index)
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
    registers[0], registers[1], registers[2] = DATA + 0x100, bits & 0xFFFFFFFF, bits >> 32
    registers[-2:] = [SP, STOP | (index & 1)]
    for register, value in zip(REGISTERS, registers):
        uc.reg_write(register, value)
    symbols = (ROOT / 'config/arm9/symbols.txt').read_text()
    entries = {int(value, 16) for value in re.findall(r'^\S+ kind:function\(arm,size=0x[0-9a-f]+\) addr:0x([0-9a-f]{8})$', symbols, re.M)}
    entries.add(0x020260E8)
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
        assert 0x02000000 <= address < 0x02000000 + len(original), hex(address)
        if address in entries and (address == ENTRY or not ENTRY <= address < ENTRY + len(code)):
            pending.append((address, engine.reg_read(UC_ARM_REG_LR) & ~1))
        pcs.add(address)

    def memory(engine, access, address, width, value, user):
        assert DATA + 0x100 <= address and address + width <= DATA + 0x126 or SP - 0x4000 <= address and address + width <= SP
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
    sign, exponent, digits = expected(bits)
    observed = list(record[5:5 + record[4]])
    passed = record[0] == sign and int.from_bytes(record[2:4], 'little', signed=True) == exponent and observed == digits
    passed = passed and record[1] == page[0x101] and record[37] == page[0x125]
    passed = passed and image[:0x100] == page[:0x100] and image[0x126:] == page[0x126:]
    return dict(modelPassed=passed, inputBits=hex(bits), digits=observed, expectedDigits=digits,
        decimalExponent=int.from_bytes(record[2:4], 'little', signed=True), expectedExponent=exponent,
        sign=record[0], expectedSign=sign, writes=writes, pageSha256=hashlib.sha256(image).hexdigest(),
        pcs=sorted(pcs), instructions=instructions, logicalNativeReturns=returns,
        physicalNativeReturnInstructions=physical_returns,
        registers=[uc.reg_read(register) for register in REGISTERS], cpsr=uc.reg_read(UC_ARM_REG_CPSR))
