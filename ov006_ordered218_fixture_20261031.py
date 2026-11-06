import hashlib
import random

from ov001_ability28_fixture_20261031 import REGS
from ov006_ordered218_models_20261031 import CONTEXT, TABLE, construct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021FABE4, 0x08000000, 0x0301FF00
NATIVE = {}


def execute(main, overlay, recipe, candidate=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if candidate is not None:
        if len(candidate) != 120:
            raise ValueError('Ordered218 candidate must preserve120 native bytes')
        machine.mem_write(ENTRY, candidate)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    table = __import__('struct').unpack_from('<29H', overlay, TABLE - 0x021D7240)
    initial, expected, services = construct(recipe, table)
    for address, content in initial:
        machine.mem_write(address, content)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    for address, content in expected:
        expected_ram[address - 0x02000000:address - 0x02000000 + len(content)] = content
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x30)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, trace, writes, observed = [], [], [], set()

    def step(engine, pc, width, unused):
        if pc == STOP:
            engine.emu_stop()
            return
        trace.append(pc)
        if len(trace) > 1000:
            raise ValueError('Ordered218 instruction bound exceeded')
        mode = engine.reg_read(UC_ARM_REG_CPSR) & 255
        if ENTRY <= pc < ENTRY + 110:
            if mode != 0x30:
                raise ValueError('Ordered218 original Thumb mode differs')
            observed.update(range(pc, pc + width))
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError(('Ordered218 independent provider order differs', hex(pc), index))
        service = services[index]
        if mode != (0x10 if pc == 0x02002480 else 0x30):
            raise ValueError('Ordered218 qualified ARM/Thumb provider mode differs')
        arguments = [engine.reg_read(REGS[i]) for i in range(len(service['arguments']))]
        if arguments != service['arguments']:
            raise ValueError(('Ordered218 independent saved-word argument differs', arguments, service['arguments']))
        if any(bytes(engine.mem_read(address,len(content))) != content for address,content in service['expectedState']):
            raise ValueError('Ordered218 independent immediate-store/context ordering differs')
        calls.append(dict(address=hex(pc), mode='thumb' if mode == 0x30 else 'arm', arguments=arguments, result=service['result'],
            effects=[dict(address=hex(address), bytesHex=content.hex()) for address, content in service['effects']]))
        for address, content in service['effects']:
            engine.mem_write(address, content)
        engine.reg_write(REGS[0], service['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 13 + register) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or any(base <= address and address+size<=base+len(content)for base,content in initial)):
            raise ValueError('Ordered218 native write outside context/private stack')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY | 1, STOP + 4, count=1001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP:
        raise ValueError('Ordered218 actual top return/SP differs')
    if actual[0] != recipe['result'] or actual[4:12] != registers[4:12] or len(calls) != 16:
        raise ValueError('Ordered218 independent full-word return/completion differs')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram:
        raise ValueError('Ordered218 complete context/RAM model differs')
    return dict(actualReturn=True, returnWord=actual[0], restoredSP=True, preservedRegisters=actual[4:12],
        nativeDependencyActualReturns=[], providedCalls=calls, instructions=len(trace) - len(calls), observedCallerInstructionBytes=sorted(observed),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(), pcTrace=trace, writes=writes)
