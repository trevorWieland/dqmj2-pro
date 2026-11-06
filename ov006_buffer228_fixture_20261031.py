import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from ov006_buffer228_models_20261031 import BUFFER, construct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021E78AC, 0x08000000, 0x0301FF00
NATIVE = {0x02008BE0: 24}


def execute(main, overlay, recipe, candidate=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if candidate is not None:
        if len(candidate) != 112:
            raise ValueError('Buffer228 candidate must preserve112 native bytes')
        machine.mem_write(ENTRY, candidate)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(SP, struct.pack('<IIII', *recipe['arguments'][4:]))
    expected_ram = bytes(machine.mem_read(0x02000000, 0x400000))
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[:4] = recipe['arguments'][:4]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    services = construct(recipe)
    frames, returned, calls, trace, writes, observed = [], [], [], [], [], set()

    def step(engine, pc, width, unused):
        if frames and pc == frames[-1]['returnAddress']:
            frame = frames.pop()
            if engine.reg_read(UC_ARM_REG_SP) != frame['sp'] or [engine.reg_read(r) for r in REGS[4:12]] != frame['preserved'] or engine.reg_read(REGS[0]) != 0:
                raise ValueError('Buffer228 native fill return/frame differs')
            returned.append(dict(address=hex(frame['address']), result=0))
        if pc == STOP:
            engine.emu_stop()
            return
        trace.append(pc)
        if len(trace) > 1000 or engine.reg_read(UC_ARM_REG_CPSR) & 255 != 0x10:
            raise ValueError('Buffer228 bounded ARM mode differs')
        if pc in NATIVE:
            if frames or returned or [engine.reg_read(r) for r in REGS[:3]] != [0, BUFFER, 128]:
                raise ValueError('Buffer228 independent native buffer extent differs')
            frames.append(dict(address=pc, returnAddress=engine.reg_read(UC_ARM_REG_LR) & ~1,
                sp=engine.reg_read(UC_ARM_REG_SP), preserved=[engine.reg_read(r) for r in REGS[4:12]]))
        if ENTRY <= pc < ENTRY + 112:
            observed.update(range(pc, pc + width))
            return
        if any(address <= pc < address + size for address, size in NATIVE.items()):
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError('Buffer228 independent provider order differs')
        service = services[index]
        stack = engine.reg_read(UC_ARM_REG_SP)
        arguments = [engine.reg_read(r) for r in REGS[:4]]
        count = len(service['arguments']) - 4
        arguments.extend(struct.unpack('<' + 'I' * count, bytes(engine.mem_read(stack, 4 * count))))
        if arguments != service['arguments']:
            raise ValueError(('Buffer228 independent full-word/low-byte arguments differ', arguments, service['arguments']))
        if bytes(engine.mem_read(BUFFER, 128)) != service['bufferBefore']:
            raise ValueError('Buffer228 independent128-byte contents differ')
        calls.append(dict(address=hex(pc), arguments=arguments, result=service['result'], bufferSha256=hashlib.sha256(service['bufferAfter']).hexdigest()))
        engine.mem_write(BUFFER, service['bufferAfter'])
        if count:engine.mem_write(stack, struct.pack('<III', 0xDEADBEEF, 0x80000000, 0xFFFFFFFF)[:4 * count])
        engine.reg_write(REGS[0], service['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 13 + register) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, size, value, unused):
        if not 0x03000000 <= address <= SP - size:
            raise ValueError('Buffer228 native write outside private stack')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=1001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or frames:
        raise ValueError('Buffer228 actual top/native return completion differs')
    if actual[0] != recipe['result'] or actual[4:12] != registers[4:12] or len(returned) != 1 or len(calls) != 2:
        raise ValueError('Buffer228 independent full return/frame differs')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram or bytes(machine.mem_read(BUFFER, 128)) != services[-1]['bufferAfter'] or bytes(machine.mem_read(SP, 16)) != struct.pack('<IIII', *recipe['arguments'][4:]):
        raise ValueError('Buffer228 complete RAM/buffer/incoming arguments differ')
    return dict(actualReturn=True, returnWord=actual[0], restoredSP=True, preservedRegisters=actual[4:12],
        nativeDependencyActualReturns=returned, providedCalls=calls, instructions=len(trace) - len(calls), observedCallerInstructionBytes=sorted(observed),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(), pcTrace=trace, writes=writes)
