import hashlib
import math
import random
import re
import struct
import functools
import match_runtime
from project import ROOT
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR
from match_runtime import REGISTERS


SIZES = {0x0202263C: 40, 0x02022684: 188, 0x02022740: 588, 0x02023E48: 20, 0x02023E5C: 112}
DATA, STACK, SP, STOP = 0x02380000, 0x03030000, 0x0303F000, 0x0F000000
EDGES = [0, 1 << 63, 1, 0x8000000000000001, 0x000FFFFFFFFFFFFF, 0x0010000000000000,
    0x3FF0000000000000, 0xBFF0000000000000, 0x3FF8000000000000, 0x3FF0000000000001,
    0x7FEFFFFFFFFFFFFF, 0xFFEFFFFFFFFFFFFF, 0x7FF0000000000000, 0xFFF0000000000000,
    0x7FF8000000000000, 0xFFF0000000000001]


@functools.cache
def entrypoints():
    symbols = (ROOT / 'config/arm9/symbols.txt').read_text()
    return {int(value, 16) for value in re.findall(r'^\S+ kind:function\(arm,size=0x[0-9a-f]+\) addr:0x([0-9a-f]{8})$', symbols, re.M)}


def floating(bits):
    return struct.unpack('<d', bits.to_bytes(8, 'little'))[0]


def encoding(value):
    return int.from_bytes(struct.pack('<d', value), 'little')


def recipe(entry, index):
    rng = random.Random(entry * 1000 + index)
    bits = EDGES[index] if index < len(EDGES) else rng.getrandbits(64)
    if index >= len(EDGES) and index % 4 == 0:
        bits &= 0x800FFFFFFFFFFFFF
    second = rng.getrandbits(64)
    exponent = [-50001, -2048, -1075, -1074, -1023, -54, -1, 0, 1, 53, 1023, 1024, 2048, 50001][index % 14]
    absolute = bits & ((1 << 63) - 1)
    special = absolute >> 52 == 2047
    output_exponent = None
    if entry == 0x0202263C:
        result = absolute | (second & (1 << 63))
    elif entry == 0x02023E48:
        result = bits >> 32 & 0x80000000
    elif entry == 0x02023E5C:
        result = 1 if special and absolute & ((1 << 52) - 1) else 2 if special else 3 if absolute == 0 else 5 if absolute >> 52 == 0 else 4
    elif entry == 0x02022684:
        if special or absolute == 0:
            result, output_exponent = bits, 0
        else:
            value, output_exponent = math.frexp(floating(bits))
            result = encoding(value)
    else:
        if special or absolute == 0:
            result = bits
        else:
            try:
                result = encoding(math.ldexp(floating(bits), exponent))
            except OverflowError:
                result = 0x7FF0000000000000 | (bits & (1 << 63))
    return bits, second, exponent, result, output_exponent


def execute(original, entry, code, index):
    bits, second, exponent, expected, output_exponent = recipe(entry, index)
    rng = random.Random(entry * 100000 + index)
    page = rng.randbytes(4096)
    wanted = bytearray(page)
    if output_exponent is not None:
        wanted[0x100:0x104] = output_exponent.to_bytes(4, 'little', signed=True)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, original)
    uc.mem_write(entry, code)
    uc.mem_write(DATA, page)
    uc.mem_map(STACK, 65536)
    uc.mem_write(STACK, bytes([0xA5]) * 65536)
    uc.mem_map(STOP, 4096)
    uc.mem_write(STOP, bytes.fromhex('1eff2fe1'))
    control = 0x10 | ((index // 16 & 3) << 6)
    uc.reg_write(UC_ARM_REG_CPSR, index % 16 << 28 | control)
    registers = [rng.getrandbits(32) for unused in REGISTERS]
    registers[:2] = [bits & 0xFFFFFFFF, bits >> 32]
    if entry == 0x0202263C:
        registers[2:4] = [second & 0xFFFFFFFF, second >> 32]
    elif entry == 0x02022684:
        registers[2] = DATA + 0x100
    elif entry == 0x02022740:
        registers[2] = exponent & 0xFFFFFFFF
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
        assert 0x02000000 <= address < 0x02000000 + len(original), hex(address)
        if address in entrypoints() and (address == entry or not entry <= address < entry + len(code)):
            pending.append((address, engine.reg_read(UC_ARM_REG_LR) & ~1))
        pcs.add(address)

    def memory(engine, access, address, width, value, user):
        assert SP - 0x4000 <= address and address + width <= SP or output_exponent is not None and DATA + 0x100 <= address and address + width <= DATA + 0x104
        if DATA <= address < DATA + 4096:
            writes.append([address, width, value])

    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_WRITE, memory)
    uc.emu_start(entry, STOP + 4, count=100000)
    assert stopped and uc.reg_read(UC_ARM_REG_SP) == SP
    assert uc.reg_read(UC_ARM_REG_CPSR) & 255 == control | ((index & 1) << 5)
    for i in range(4, 12):
        assert uc.reg_read(REGISTERS[i]) == registers[i]
    assert bytes(uc.mem_read(STACK, SP - STACK - 0x4000)) == bytes([0xA5]) * (SP - STACK - 0x4000)
    assert bytes(uc.mem_read(SP, STACK + 65536 - SP)) == bytes([0xA5]) * (STACK + 65536 - SP)
    image = bytes(uc.mem_read(DATA, 4096))
    result = uc.reg_read(REGISTERS[0])
    if entry not in [0x02023E48, 0x02023E5C]:
        result |= uc.reg_read(REGISTERS[1]) << 32
    return dict(modelPassed=result == expected and image == bytes(wanted), result=hex(result),
        expected=hex(expected), input=hex(bits), second=hex(second), scale=exponent,
        expectedExponent=output_exponent, pageSha256=hashlib.sha256(image).hexdigest(), writes=writes,
        pcs=sorted(pcs), instructions=instructions, logicalNativeReturns=returns,
        physicalNativeReturnInstructions=physical_returns,
        registers=[uc.reg_read(register) for register in REGISTERS], cpsr=uc.reg_read(UC_ARM_REG_CPSR))
