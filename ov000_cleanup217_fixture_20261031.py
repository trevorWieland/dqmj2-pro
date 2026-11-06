import hashlib
import random

from ov001_ability28_fixture_20261031 import REGS
from ov000_cleanup217_models_20261031 import CONTEXT, construct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021EB060, 0x08000000, 0x0301FF00
NATIVE = {0x02084920: 4}


def execute(main, overlay, recipe, candidate=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    if main[0x84920:0x84924] != bytes.fromhex('1eff2fe1'):
        raise ValueError('Cleanup217 measured empty BX LR body differs')
    machine.mem_write(0x021D7240, overlay)
    if candidate is not None:
        if len(candidate) != 232:
            raise ValueError('Cleanup217 candidate must preserve232 native bytes')
        machine.mem_write(ENTRY, candidate)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    initial, expected, services, empty_input = construct(recipe)
    machine.mem_write(CONTEXT, initial)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_ram[CONTEXT - 0x02000000:CONTEXT - 0x02000000 + 40] = expected
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, trace, writes, observed, returned = [], [], [], set(), []
    empty_frame = None

    def step(engine, pc, width, unused):
        nonlocal empty_frame
        if empty_frame and pc == empty_frame['returnAddress']:
            if engine.reg_read(REGS[0]) != empty_input or engine.reg_read(UC_ARM_REG_SP) != empty_frame['sp'] or [engine.reg_read(r) for r in REGS] != empty_frame['registers']:
                raise ValueError('Cleanup217 native empty return differs')
            returned.append(dict(address=hex(0x02084920), result=engine.reg_read(REGS[0])))
            empty_frame = None
        if pc == STOP:
            engine.emu_stop()
            return
        trace.append(pc)
        if len(trace) > 1000:
            raise ValueError('Cleanup217 instruction bound exceeded')
        mode = engine.reg_read(UC_ARM_REG_CPSR) & 255
        if ENTRY <= pc < ENTRY + 228:
            if mode != 0x10:
                raise ValueError('Cleanup217 original ARM mode differs')
            observed.update(range(pc, pc + width))
            return
        if pc == 0x02084920:
            if len(calls) != 10 or returned or mode != 0x10 or engine.reg_read(REGS[0]) != empty_input:
                raise ValueError('Cleanup217 actual empty ARM routine entry differs')
            empty_frame = dict(returnAddress=engine.reg_read(UC_ARM_REG_LR), sp=engine.reg_read(UC_ARM_REG_SP), registers=[engine.reg_read(r) for r in REGS])
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError(('Cleanup217 independent provider order differs', hex(pc), index))
        service = services[index]
        if mode != 0x10:
            raise ValueError('Cleanup217 qualified ARM/Thumb provider mode differs')
        arguments = [engine.reg_read(REGS[i]) for i in range(len(service['arguments']))]
        if arguments != service['arguments']:
            raise ValueError(('Cleanup217 independent saved-word argument differs', arguments, service['arguments']))
        if bytes(engine.mem_read(CONTEXT, 40)) != service['expectedContext']:
            raise ValueError('Cleanup217 independent immediate-store/context ordering differs')
        calls.append(dict(address=hex(pc), mode='arm', arguments=arguments, result=service['result'],
            effects=[dict(offset=offset, bytesHex=content.hex()) for offset, content in service['effects']]))
        for offset, content in service['effects']:
            engine.mem_write(CONTEXT + offset, content)
        engine.reg_write(REGS[0], service['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 13 + register) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or CONTEXT <= address <= CONTEXT + 40 - size):
            raise ValueError('Cleanup217 native write outside context/private stack')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=1001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP:
        raise ValueError('Cleanup217 actual top return/SP differs')
    if actual[0] != CONTEXT or actual[4:12] != registers[4:12] or len(calls) != 18 or len(returned) != 1 or empty_frame is not None:
        raise ValueError('Cleanup217 independent full-word return/completion differs')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram:
        raise ValueError('Cleanup217 complete context/RAM model differs')
    return dict(actualReturn=True, returnWord=actual[0], restoredSP=True, preservedRegisters=actual[4:12],
        nativeDependencyActualReturns=returned, providedCalls=calls, instructions=len(trace) - len(calls), observedCallerInstructionBytes=sorted(observed),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(), pcTrace=trace, writes=writes)
