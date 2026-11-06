import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from ov000_buffer178_models_20261031 import BUFFER, CONTEXT, OBJECTS, construct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x022092E0, 0x08000000, 0x0301FF00
NATIVE = {0x02008BE0: 24, 0x020470FC: 64}


def execute(main, overlay, recipe, candidate=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if candidate is not None:
        if len(candidate) != 268:
            raise ValueError('Buffer178 candidate must preserve268 native bytes')
        machine.mem_write(ENTRY, candidate)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    initial, effects, services, native, expected_result = construct(recipe, rng)
    for address, content in initial:
        machine.mem_write(address, content)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    for address, content in effects:
        expected_ram[address - 0x02000000:address - 0x02000000 + len(content)] = content
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    frames, entries, returned, calls, trace, writes, observed = [], [], [], [], [], [], set()

    def step(engine, pc, width, unused):
        if frames and pc == frames[-1]['returnAddress']:
            frame = frames.pop()
            if engine.reg_read(UC_ARM_REG_SP) != frame['sp'] or [engine.reg_read(r) for r in REGS[4:12]] != frame['preserved']:
                raise ValueError('Buffer178 native frame preservation differs')
            returned.append(dict(address=hex(frame['address']), result=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        trace.append(pc)
        if len(trace) > 5000 or engine.reg_read(UC_ARM_REG_CPSR) & 255 != 0x10:
            raise ValueError('Buffer178 bounded ARM mode differs')
        if pc in NATIVE:
            index = len(entries)
            if index >= len(native) or hex(pc) != native[index]['address']:
                raise ValueError('Buffer178 independent native entry order differs')
            expected = native[index]
            arguments = [engine.reg_read(REGS[i]) for i in range(len(expected['arguments']))]
            if arguments != expected['arguments']:
                raise ValueError('Buffer178 independent native buffer/length differs')
            entries.append(dict(address=hex(pc), arguments=arguments))
            frames.append(dict(address=pc, returnAddress=engine.reg_read(UC_ARM_REG_LR) & ~1,
                sp=engine.reg_read(UC_ARM_REG_SP), preserved=[engine.reg_read(r) for r in REGS[4:12]]))
        if ENTRY <= pc < ENTRY + 252:
            observed.update(range(pc, pc + width))
            return
        if any(address <= pc < address + size for address, size in NATIVE.items()):
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError(('Buffer178 independent provider order differs', hex(pc), index))
        service = services[index]
        arguments = [engine.reg_read(REGS[i]) for i in range(min(4, len(service['arguments'])))]
        if len(service['arguments']) > 4:
            stack = engine.reg_read(UC_ARM_REG_SP)
            arguments.extend(struct.unpack('<II', bytes(engine.mem_read(stack, 8))))
        if arguments != service['arguments']:
            raise ValueError(('Buffer178 independent late-field/stack arguments differ', arguments, service['arguments']))
        if bytes(engine.mem_read(BUFFER, 128)) != service['bufferBefore']:
            raise ValueError('Buffer178 independent complete128-byte buffer differs')
        if pc == 0x02087674 and struct.unpack('<H', bytes(engine.mem_read(OBJECTS[1 if recipe['selector'] == 0 else 0] + 0x6C, 2)))[0] != recipe['length']:
            raise ValueError('Buffer178 original bounded-u16 length was not stored')
        calls.append(dict(address=hex(pc), arguments=arguments, result=service['result'],
            effects=[dict(address=hex(a), bytesHex=b.hex()) for a, b in service['effects']]))
        for address, content in service['effects']:
            engine.mem_write(address, content)
        engine.reg_write(REGS[0], service['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 13 + register) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or any(base <= address <= base + 128 - size for base in OBJECTS)):
            raise ValueError('Buffer178 native write outside object/private stack')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=5001)
    actual = [machine.reg_read(register) for register in REGS]
    expected_returns = [dict(address=n['address'], result=n['result']) for n in native]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or frames:
        raise ValueError('Buffer178 actual top/native completion differs')
    if actual[0] != expected_result or actual[4:12] != registers[4:12] or returned != expected_returns or len(calls) != len(services):
        raise ValueError('Buffer178 independent caller/native completion differs')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram:
        raise ValueError('Buffer178 independent complete object/context/RAM effects differ')
    return dict(actualReturn=True, returnWord=actual[0], restoredSP=True, preservedRegisters=actual[4:12], nativeEntries=entries,
        nativeDependencyActualReturns=returned, providedCalls=calls, instructions=len(trace) - len(calls), observedCallerInstructionBytes=sorted(observed),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(), pcTrace=trace, writes=writes)
