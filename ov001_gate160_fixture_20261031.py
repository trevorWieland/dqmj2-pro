import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from ov001_gate160_models_20261031 import POOLS, construct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021F73B8, 0x08000000, 0x0301FF00
NATIVE = {0x020444A8: 68, 0x020444EC: 28, 0x0204453C: 24, 0x02044520: 28,
    0x020443EC: 16, 0x020655D8: 16, 0x021DB438: 124, 0x021DB8D0: 72}


def execute(main, overlay, recipe, candidate=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if candidate is not None:
        if len(candidate) != 224:
            raise ValueError('Gate160 candidate must preserve the complete224-byte span')
        machine.mem_write(ENTRY, candidate)
    if struct.unpack_from('<4I', overlay, 0x021DB4A4 - 0x021D7240) != POOLS:
        raise ValueError('Gate160 native actor-pool literals differ')
    for offset, expected in [(0x443F8, 0x020F69C4), (0x44538, 0x020DD9BC), (0x655E4, 0x021C0EF4)]:
        if struct.unpack_from('<I', main, offset)[0] != expected:
            raise ValueError('Gate160 native mode-byte/word literals differ')
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    initial, expected_result, expected_entries, expected_returns = construct(recipe, rng)
    for address, content in initial:
        machine.mem_write(address, content)
    expected_ram = bytes(machine.mem_read(0x02000000, 0x400000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[0] = recipe['argument']
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    frames, entries, returned, trace, writes, observed = [], [], [], [], [], set()

    def step(engine, pc, width, unused):
        while frames and pc == frames[-1]['returnAddress']:
            frame = frames.pop()
            if engine.reg_read(UC_ARM_REG_SP) != frame['sp'] or [engine.reg_read(r) for r in REGS[4:12]] != frame['preserved']:
                raise ValueError('Gate160 native callee did not restore its frame')
            returned.append(dict(address=hex(frame['address']), result=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        trace.append(pc)
        if len(trace) > 2000 or engine.reg_read(UC_ARM_REG_CPSR) & 255 != 0x10:
            raise ValueError('Gate160 bounded ARM mode differs')
        if pc in NATIVE:
            index = len(entries)
            if index >= len(expected_entries) or hex(pc) != expected_entries[index]['address']:
                raise ValueError('Gate160 independent native call order differs')
            expected = expected_entries[index]
            arguments = [engine.reg_read(REGS[i]) for i in range(len(expected['arguments']))]
            if arguments != expected['arguments']:
                raise ValueError('Gate160 independent native arguments differ')
            entries.append(dict(address=hex(pc), arguments=arguments))
            frames.append(dict(address=pc, returnAddress=engine.reg_read(UC_ARM_REG_LR) & ~1,
                sp=engine.reg_read(UC_ARM_REG_SP), preserved=[engine.reg_read(r) for r in REGS[4:12]]))
        if ENTRY <= pc < ENTRY + 220:
            observed.update(range(pc, pc + width))
            return
        if not any(address <= pc < address + count for address, count in NATIVE.items()):
            raise ValueError(('Gate160 instruction outside caller/classified native bodies', hex(pc)))

    def written(engine, access, address, size, value, unused):
        if not 0x03000000 <= address <= SP - size:
            raise ValueError('Gate160 write outside private stack')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=2001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or frames:
        raise ValueError('Gate160 actual top/native return completion differs')
    if actual[0] != expected_result or actual[4:12] != registers[4:12] or entries != expected_entries or returned != expected_returns:
        raise ValueError(('Gate160 independent return/call model differs', actual[0], expected_result, returned, expected_returns))
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram:
        raise ValueError('Gate160 independent complete unchanged-RAM model differs')
    return dict(actualReturn=True, returnWord=actual[0], restoredSP=True, preservedRegisters=actual[4:12], nativeEntries=entries,
        nativeDependencyActualReturns=returned, providedCalls=[], instructions=len(trace), observedCallerInstructionBytes=sorted(observed),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(), pcTrace=trace, writes=writes)
