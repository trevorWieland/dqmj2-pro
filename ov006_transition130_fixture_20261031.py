import hashlib
import random

from ov001_ability28_fixture_20261031 import REGS
from ov006_transition130_models_20261031 import construct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY = dict(transition=(0x021F7C64, 148, 134), predicate=(0x021F23C4, 32, 26))
NATIVE = {0x02203188: 20, 0x021F23C4: 26, 0x021F52CC: 6, 0x021F52D8: 8}
STOP, SP = 0x08000000, 0x0301FF00


def execute(kind, main, overlay, recipe, candidate=None):
    entry, size, instruction_bytes = ENTRY[kind]
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, length in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, length)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if candidate is not None:
        if len(candidate) != size:
            raise ValueError('Transition130 complete candidate span differs')
        machine.mem_write(entry, candidate)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    for address, length in [(0x02350000, 0x100), (0x02360000, 0x100), (0x0221C06C, 32)]:
        machine.mem_write(address, rng.randbytes(length))
    initial, effects, services, expected_return, expected_native = construct(kind, recipe)
    for address, content in initial:
        machine.mem_write(address, content)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    for address, content in effects:
        offset = address - 0x02000000
        expected_ram[offset:offset + len(content)] = content
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x30)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, frames, returned, trace, writes, observed = [], [], [], [], [], set()

    def step(engine, pc, width, unused):
        if frames and pc == frames[-1]['returnAddress']:
            frame = frames.pop()
            if engine.reg_read(UC_ARM_REG_SP) != frame['sp'] or [engine.reg_read(r) for r in REGS[4:12]] != frame['preserved']:
                raise ValueError('Transition130 actual Thumb helper SP/preserved registers differ')
            returned.append(dict(address=hex(frame['address']), result=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        trace.append(pc)
        if len(trace) > 2000 or engine.reg_read(UC_ARM_REG_CPSR) & 255 != 0x30:
            raise ValueError('Transition130 Thumb mode/instruction bound differs')
        if pc in NATIVE and pc != entry:
            frames.append(dict(address=pc, returnAddress=engine.reg_read(UC_ARM_REG_LR) & ~1,
                sp=engine.reg_read(UC_ARM_REG_SP), preserved=[engine.reg_read(r) for r in REGS[4:12]]))
        if entry <= pc < entry + instruction_bytes:
            observed.update(range(pc, pc + width))
            return
        if any(address != entry and address <= pc < address + count for address, count in NATIVE.items()):
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError(('Transition130 provider order differs', kind, hex(pc), index))
        service = services[index]
        arguments = [engine.reg_read(REGS[i]) for i in range(len(service['arguments']))]
        if arguments != service['arguments']:
            raise ValueError(('Transition130 independent fresh-field arguments differ', arguments, service['arguments']))
        calls.append(dict(address=hex(pc), arguments=arguments, suppliedReturn=service['result'],
            effects=[dict(address=hex(address), bytesHex=value.hex()) for address, value in service['effects']]))
        for address, content in service['effects']:
            engine.mem_write(address, content)
        engine.reg_write(REGS[0], service['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + register + index) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, length, value, unused):
        if not (0x03000000 <= address <= SP - length or 0x0221C078 <= address <= 0x0221C084 - length):
            raise ValueError('Transition130 native write outside measured setters/private stack')
        writes.append((address, length, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(entry | 1, STOP + 4, count=2001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or frames:
        raise ValueError('Transition130 actual top return/SP/frame completion differs')
    if actual[0] != expected_return or actual[4:12] != registers[4:12] or len(calls) != len(services) or len(returned) != expected_native:
        raise ValueError('Transition130 independent actual return/completion differs')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram:
        raise ValueError('Transition130 independent complete RAM model differs')
    return dict(actualReturn=True, returnWord=actual[0], restoredSP=True, preservedRegisters=actual[4:12], nativeReturns=returned,
        providedCalls=calls, ramSha256=hashlib.sha256(ram).hexdigest(), instructions=len(trace) - len(calls),
        observedCallerInstructionBytes=sorted(observed), pcTrace=trace, writes=writes)
