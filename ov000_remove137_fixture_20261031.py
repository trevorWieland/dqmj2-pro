import hashlib
import random

from ov001_ability28_fixture_20261031 import REGS
from ov000_remove137_models_20261031 import COPIES, CONTEXT, GROUP, POOL, construct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x02225BF0, 0x08000000, 0x0301FF00
NATIVE = {0x02062AA0: 48, 0x02062AD0: 48, 0x02062A50: 16, 0x02062A88: 16, 0x02062A10: 60,
    0x020628B0: 80, 0x02062980: 92, 0x020627A0: 72, 0x02062828: 32, 0x0201D470: 356, 0x020627EC: 60, 0x02008D78: 148}


def execute(main, overlay, recipe, candidate=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, length in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, length)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if candidate is not None:
        if len(candidate) != 300:
            raise ValueError('Remove137 complete candidate span differs')
        machine.mem_write(ENTRY, candidate)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    initial, expected, services, expected_return, cleared = construct(recipe,
        rng.randbytes(13200), rng.randbytes(396), rng.randbytes(64), rng.randbytes(64))
    for address, content in initial:
        machine.mem_write(address, content)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    for address, content in expected:
        start = address - 0x02000000
        expected_ram[start:start + len(content)] = content
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(REGS[0], recipe['index'])
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, frames, returned, trace, writes, observed = [], [], [], [], [], set()

    def step(engine, pc, width, unused):
        while frames and pc == frames[-1]['returnAddress']:
            frame = frames.pop()
            if engine.reg_read(UC_ARM_REG_SP) != frame['sp'] or [engine.reg_read(r) for r in REGS[4:12]] != frame['preserved']:
                raise ValueError('Remove137 actual native helper SP/preserved registers differ')
            returned.append(dict(address=hex(frame['address']), result=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        trace.append(pc)
        if len(trace) > 1000000 or engine.reg_read(UC_ARM_REG_CPSR) & 255 != 0x10:
            raise ValueError(('Remove137 bounded ARM mode differs',hex(pc),len(trace),hex(engine.reg_read(UC_ARM_REG_CPSR))))
        if pc in NATIVE:
            frames.append(dict(address=pc, returnAddress=engine.reg_read(UC_ARM_REG_LR), sp=engine.reg_read(UC_ARM_REG_SP),
                preserved=[engine.reg_read(r) for r in REGS[4:12]]))
        if ENTRY <= pc < ENTRY + 300:
            observed.update(range(pc, pc + width))
            return
        if any(address <= pc < address + size for address, size in NATIVE.items()):
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError(('Remove137 independent provider order differs', hex(pc), index))
        service = services[index]
        arguments = [engine.reg_read(REGS[i]) for i in range(len(service['arguments']))]
        if arguments != service['arguments']:
            raise ValueError('Remove137 independent provider arguments differ')
        if bytes(engine.mem_read(cleared, 132)) != bytes(132):
            raise ValueError('Remove137 complete132-byte record is not cleared before UI service')
        calls.append(dict(address=hex(pc), arguments=arguments, effects=[dict(address=hex(a), bytesHex=b.hex()) for a, b in service['effects']]))
        for address, content in service['effects']:
            engine.mem_write(address, content)
        for register in (0, 1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + register + index) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, length, value, unused):
        allowed = [(0x03000000, SP), (POOL, POOL + 13200), (GROUP, GROUP + 64), (COPIES, COPIES + 396), (CONTEXT, CONTEXT + 64)]
        if not any(start <= address <= end - length for start, end in allowed):
            raise ValueError(('Remove137 native write outside classified state', hex(address)))
        writes.append((address, length, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=1000001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or frames:
        raise ValueError('Remove137 actual return/SP/frame completion differs')
    if actual[0] != expected_return or actual[4:12] != registers[4:12] or len(calls) != len(services):
        raise ValueError('Remove137 independent caller ABI/protocol model differs')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram:
        position = next(i for i, (a, b) in enumerate(zip(ram, expected_ram)) if a != b)
        raise ValueError(('Remove137 independent full pool/group/copy/counter RAM model differs', hex(0x02000000 + position), ram[position], expected_ram[position]))
    return dict(actualReturn=True, returnWord=actual[0], restoredSP=True, preservedRegisters=actual[4:12], nativeDependencyActualReturns=returned,
        providedCalls=calls, instructions=len(trace) - len(calls), observedCallerInstructionBytes=sorted(observed),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
        pcTrace=trace, writes=writes)
