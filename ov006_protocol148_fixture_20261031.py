import hashlib
import random

from ov001_ability28_fixture_20261031 import REGS
from ov006_protocol148_models_20261031 import OBJECTS, PACKET, ROOT_STATE, construct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x0220192C, 0x08000000, 0x0301FF00
NATIVE = {0x022012C0: 16, 0x02201270: 62, 0x022018BC: 106}


def execute(main, overlay, recipe, candidate=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, length in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, length)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if candidate is not None:
        if len(candidate) != 144:
            raise ValueError('Protocol148 complete candidate span differs')
        machine.mem_write(ENTRY, candidate)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    initial, expected, plan, expected_return = construct(recipe, rng.randbytes(16), rng.randbytes(256))
    for address, content in initial:
        machine.mem_write(address, content)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    for address, content in expected:
        offset = address - 0x02000000
        expected_ram[offset:offset + len(content)] = content
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(REGS[0], PACKET)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x30)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, returned, frames, trace, writes, observed = [], [], [], [], [], set()

    def step(engine, pc, width, unused):
        while frames and pc == frames[-1]['returnAddress']:
            frame = frames.pop()
            if engine.reg_read(UC_ARM_REG_SP) != frame['sp'] or [engine.reg_read(r) for r in REGS[4:12]] != frame['preserved']:
                raise ValueError('Protocol148 actual native helper frame differs')
            returned.append(dict(address=hex(frame['address']), result=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        trace.append(pc)
        if len(trace) > 5000:
            raise ValueError('Protocol148 instruction bound differs')
        if ENTRY <= pc < ENTRY + 144:
            if engine.reg_read(UC_ARM_REG_CPSR) & 255 != 0x30:
                raise ValueError('Protocol148 Thumb caller mode differs')
            observed.update(range(pc, pc + width))
            return
        if pc not in NATIVE and any(address <= pc < address + count for address, count in NATIVE.items()):
            if engine.reg_read(UC_ARM_REG_CPSR) & 255 != 0x30:
                raise ValueError('Protocol148 Thumb native body mode differs')
            return
        index = len(calls)
        if index >= len(plan) or pc != plan[index]['address']:
            raise ValueError(('Protocol148 independent call order differs', hex(pc), index, recipe))
        item = plan[index]
        arguments = [engine.reg_read(REGS[i]) for i in range(len(item['arguments']))]
        if arguments != item['arguments']:
            raise ValueError(('Protocol148 independent arguments differ', arguments, item['arguments']))
        expected_mode = 0x10 if pc in (0x02012290, 0x02390000) else 0x30
        if engine.reg_read(UC_ARM_REG_CPSR) & 255 != expected_mode:
            raise ValueError('Protocol148 native/provider interworking mode differs')
        calls.append(dict(kind=item['kind'], address=hex(pc), arguments=arguments,
            providedReturn=item.get('result'), effects=[dict(address=hex(a), bytesHex=b.hex()) for a, b in item.get('effects', [])]))
        if pc in NATIVE:
            frames.append(dict(address=pc, returnAddress=engine.reg_read(UC_ARM_REG_LR) & ~1,
                sp=engine.reg_read(UC_ARM_REG_SP), preserved=[engine.reg_read(r) for r in REGS[4:12]]))
            return
        for address, content in item.get('effects', []):
            engine.mem_write(address, content)
        engine.reg_write(REGS[0], item['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + register + index) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, length, value, unused):
        allowed = [(0x03000000, SP), (ROOT_STATE, ROOT_STATE + 8), (PACKET, PACKET + 16)]
        allowed += [(address, address + 128) for address in OBJECTS]
        if not any(start <= address <= end - length for start, end in allowed):
            raise ValueError('Protocol148 native write outside classified state/private stack')
        writes.append((address, length, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY | 1, STOP + 4, count=5001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or frames:
        raise ValueError('Protocol148 actual top return/SP/native completion differs')
    if actual[0] != expected_return or actual[4:12] != registers[4:12] or len(calls) != len(plan):
        raise ValueError(('Protocol148 independent caller ABI/protocol differs', hex(actual[0]), hex(expected_return)))
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram:
        offset = next(i for i, (a, b) in enumerate(zip(ram, expected_ram)) if a != b)
        raise ValueError(('Protocol148 complete independent state/RAM model differs', hex(0x02000000 + offset), ram[offset], expected_ram[offset]))
    return dict(actualReturn=True, returnWord=actual[0], restoredSP=True, preservedRegisters=actual[4:12], nativeDependencyActualReturns=returned,
        providedCalls=[item for item in calls if item['kind'] == 'provided'], allCalls=calls, instructions=len(trace) - sum(item['kind'] == 'provided' for item in calls),
        observedCallerInstructionBytes=sorted(observed), ramSha256=hashlib.sha256(ram).hexdigest(),
        stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(), pcTrace=trace, writes=writes)
