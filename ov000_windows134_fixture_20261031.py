import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, PROVIDER, STOP, SP = 0x0220418C, 0x02061C1C, 0x08000000, 0x0301FF00
TUPLES = [[6, 2, 8, 8, 2, 0, 0], [7, 3, 10, 16, 2, 0, 0], [8, 2, 13, 16, 2, 0, 0],
    [9, 3, 15, 15, 2, 0, 0], [10, 3, 19, 21, 2, 0, 0], [11, 4, 17, 2, 2, 0, 0], [12, 3, 21, 10, 2, 0, 0]]


def recipes():
    return [dict(seed=0x134000 + index, variant=index, poisonArgumentSpace=bool(index & 1)) for index in range(32)]


def execute(main, overlay, recipe, candidate=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, length in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, length)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if candidate is not None:
        if len(candidate) != 284:
            raise ValueError('Windows134 candidate complete span differs')
        machine.mem_write(ENTRY, candidate)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(0x02350000, rng.randbytes(64))
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, trace, writes, observed = [], [], [], set()
    final_return = 0

    def step(engine, pc, width, unused):
        nonlocal final_return
        if pc == STOP:
            engine.emu_stop()
            return
        trace.append(pc)
        if len(trace) > 1000 or engine.reg_read(UC_ARM_REG_CPSR) & 255 != 0x10:
            raise ValueError('Windows134 actual mode/instruction bound differs')
        if ENTRY <= pc < ENTRY + 284:
            observed.update(range(pc, pc + width))
            return
        index = len(calls)
        if pc != PROVIDER or index >= 7:
            raise ValueError('Windows134 provider order differs')
        stack = engine.reg_read(UC_ARM_REG_SP)
        arguments = [engine.reg_read(register) for register in REGS[:4]] + list(struct.unpack('<III', bytes(engine.mem_read(stack, 12))))
        if arguments != TUPLES[index]:
            raise ValueError(('Windows134 independent seven-word argument tuple differs', index, arguments, TUPLES[index]))
        final_return = [0, 1, 0x80000000, 0xFFFFFFFF][(recipe['variant'] + index) % 4]
        calls.append(dict(address=hex(pc), arguments=arguments, suppliedReturn=final_return, sp=stack))
        content = struct.pack('<I', final_return)
        engine.mem_write(0x02350000 + index * 4, content)
        expected_ram[0x350000 + index * 4:0x350000 + index * 4 + 4] = content
        if recipe['poisonArgumentSpace']:
            engine.mem_write(stack, bytes([0xA0 + index]) * 12)
        engine.reg_write(REGS[0], final_return)
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + register + index) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, length, value, unused):
        if not 0x03000000 <= address <= SP - length:
            raise ValueError('Windows134 caller write outside private stack')
        writes.append((address, length, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=1001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP:
        raise ValueError('Windows134 actual top return/SP differs')
    if actual[0] != final_return or actual[4:12] != registers[4:12] or len(calls) != 7:
        raise ValueError('Windows134 independent last-return/preserved-register model differs')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram:
        raise ValueError('Windows134 complete independent RAM model differs')
    return dict(actualReturn=True, returnWord=actual[0], restoredSP=True, preservedRegisters=actual[4:12], instructions=len(trace) - 7,
        providedCalls=calls, nativeDependencyActualReturns=[], ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
        observedCallerInstructionBytes=sorted(observed), pcTrace=trace, writes=writes)
