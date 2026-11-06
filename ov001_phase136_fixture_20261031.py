import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from ov001_phase136_models_20261031 import CONTEXT, construct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021F8B60, 0x08000000, 0x0301FF00


def execute(main, overlay, recipe, candidate=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, length in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, length)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if candidate is not None:
        if len(candidate) != 240:
            raise ValueError('Phase136 complete candidate span differs')
        machine.mem_write(ENTRY, candidate)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    initial, expected_context, services = construct(recipe, rng.randbytes(136))
    for address, content in initial:
        machine.mem_write(address, content)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_ram[CONTEXT - 0x02000000:CONTEXT - 0x02000000 + 136] = expected_context
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, trace, writes, observed = [], [], [], set()

    def step(engine, pc, width, unused):
        if pc == STOP:
            engine.emu_stop()
            return
        trace.append(pc)
        if len(trace) > 2000 or engine.reg_read(UC_ARM_REG_CPSR) & 255 != 0x10:
            raise ValueError('Phase136 bounded ARM mode differs')
        if ENTRY <= pc < ENTRY + 236:
            observed.update(range(pc, pc + width))
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError(('Phase136 independent provider order differs', hex(pc), index))
        service = services[index]
        arguments = [engine.reg_read(REGS[i]) for i in range(min(4, len(service['arguments'])))]
        expected_arguments = list(service['arguments'])
        output = None
        if service['stackOutput'] is not None:
            stack = engine.reg_read(UC_ARM_REG_SP)
            output = struct.unpack('<I', bytes(engine.mem_read(stack, 4)))[0]
            arguments.append(output)
            expected_arguments[-1] = stack + 4
        if arguments != expected_arguments:
            raise ValueError(('Phase136 independent late-field/stack arguments differ', arguments, expected_arguments))
        calls.append(dict(address=hex(pc), arguments=arguments, suppliedReturn=service['result'], stackOutput=service['stackOutput'],
            effects=[dict(offset=offset, bytesHex=content.hex()) for offset, content in service['effects']]))
        for offset, content in service['effects']:
            engine.mem_write(CONTEXT + offset, content)
        if output is not None:
            engine.mem_write(output, struct.pack('<I', service['stackOutput']))
        engine.reg_write(REGS[0], service['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + register + index) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, length, value, unused):
        if not (0x03000000 <= address <= SP - length or CONTEXT <= address <= CONTEXT + 136 - length):
            raise ValueError('Phase136 caller write outside classified context/private stack')
        writes.append((address, length, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=2001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP:
        raise ValueError('Phase136 actual top return/SP differs')
    if actual[0] != 0 or actual[4:12] != registers[4:12] or len(calls) != len(services):
        raise ValueError('Phase136 independent caller ABI/protocol differs')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram:
        raise ValueError('Phase136 independent complete context/RAM model differs')
    return dict(actualReturn=True, returnWord=actual[0], restoredSP=True, preservedRegisters=actual[4:12], nativeDependencyActualReturns=[],
        providedCalls=calls, instructions=len(trace) - len(calls), observedCallerInstructionBytes=sorted(observed),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(), pcTrace=trace, writes=writes)
