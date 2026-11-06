import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from ov001_message198_models_20261031 import ACTOR, construct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021D7E80, 0x08000000, 0x0301FF00
NATIVE = {0x021DB9E0: 20, 0x021DBAAC: 28, 0x02042C2C: 8, 0x02041F74: 28}


def execute(main, overlay, recipe, candidate=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if candidate is not None:
        if len(candidate) != 212:
            raise ValueError('Message198 candidate must preserve212 native bytes')
        machine.mem_write(ENTRY, candidate)
    if struct.unpack_from('<I', overlay, 0x021DB9F0 - 0x021D7240)[0] != 0x02044CDC:
        raise ValueError('Message198 native tail lookup differs')
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    initial, actor, services, native = construct(recipe, rng)
    for address, content in initial:
        machine.mem_write(address, content)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_ram[ACTOR - 0x02000000:ACTOR - 0x02000000 + len(actor)] = actor
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[0] = ACTOR
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    frames, entries, returned, calls, trace, writes, observed = [], [], [], [], [], [], set()

    def step(engine, pc, width, unused):
        while frames and pc == frames[-1]['returnAddress']:
            frame = frames.pop()
            if engine.reg_read(UC_ARM_REG_SP) != frame['sp'] or [engine.reg_read(r) for r in REGS[4:12]] != frame['preserved']:
                raise ValueError('Message198 native frame preservation differs')
            returned.append(dict(address=hex(frame['address']), result=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        trace.append(pc)
        if len(trace) > 2000 or engine.reg_read(UC_ARM_REG_CPSR) & 255 != 0x10:
            raise ValueError('Message198 bounded ARM mode differs')
        if pc in NATIVE:
            index = len(entries)
            if index >= len(native) or hex(pc) != native[index]['address']:
                raise ValueError('Message198 independent native order differs')
            expected = native[index]
            arguments = [engine.reg_read(REGS[i]) for i in range(len(expected['arguments']))]
            if arguments != expected['arguments']:
                raise ValueError('Message198 independent actor/getter arguments differ')
            entries.append(dict(address=hex(pc), arguments=arguments))
            frames.append(dict(address=pc, returnAddress=engine.reg_read(UC_ARM_REG_LR) & ~1,
                sp=engine.reg_read(UC_ARM_REG_SP), preserved=[engine.reg_read(r) for r in REGS[4:12]]))
        if ENTRY <= pc < ENTRY + 212:
            observed.update(range(pc, pc + width))
            return
        if any(address <= pc < address + size for address, size in NATIVE.items()):
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError('Message198 independent lookup/UI provider order differs')
        service = services[index]
        arguments = [engine.reg_read(REGS[i]) for i in range(len(service['arguments']))]
        if arguments != service['arguments']:
            raise ValueError(('Message198 independent lookup/late-byte arguments differ', hex(pc), arguments, service['arguments']))
        if service['expectedVector'] is not None and bytes(engine.mem_read(ACTOR + 0x70, 12)) != service['expectedVector']:
            raise ValueError('Message198 late vector contents differ')
        calls.append(dict(address=hex(pc), arguments=arguments, result=service['result'],
            effects=[dict(address=hex(a), bytesHex=b.hex()) for a, b in service['effects']]))
        for address, content in service['effects']:
            engine.mem_write(address, content)
        engine.reg_write(REGS[0], service['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 13 + register) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, size, value, unused):
        if not 0x03000000 <= address <= SP - size:
            raise ValueError('Message198 native write outside private stack')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=2001)
    actual = [machine.reg_read(register) for register in REGS]
    expected_returns = [dict(address=r['address'], result=r['result']) for r in native]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or frames:
        raise ValueError('Message198 actual top/native return completion differs')
    if actual[0] != recipe['result'] or actual[4:12] != registers[4:12] or returned != expected_returns or len(calls) != len(services):
        raise ValueError('Message198 independent full-word return/completion differs')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram:
        raise ValueError('Message198 complete actor/descriptor/RAM model differs')
    return dict(actualReturn=True, returnWord=actual[0], restoredSP=True, preservedRegisters=actual[4:12], nativeEntries=entries,
        nativeDependencyActualReturns=returned, providedCalls=calls, instructions=len(trace) - len(calls), observedCallerInstructionBytes=sorted(observed),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(), pcTrace=trace, writes=writes)
