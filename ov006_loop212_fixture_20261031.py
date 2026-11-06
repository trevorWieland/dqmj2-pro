import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from ov006_loop212_models_20261031 import CONTEXT, GLOBAL, construct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021F4F44, 0x08000000, 0x0301FF00
NATIVE = {0x021F4FC0: 80, 0x0209747C: 12, 0x02097470: 12, 0x021F52CC: 12}


def execute(main, overlay, recipe, candidate=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x02500000, 0x1000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if candidate is not None:
        if len(candidate) != 124:
            raise ValueError('Loop212 candidate must preserve124 native bytes')
        machine.mem_write(ENTRY, candidate)
    if struct.unpack_from('<I', overlay, 0x021F500C - 0x021D7240)[0] != CONTEXT:
        raise ValueError('Loop212 native gate context differs')
    if any(struct.unpack_from('<I', main, a - 0x02000000 + 8)[0] != GLOBAL for a in [0x02097470, 0x0209747C]):
        raise ValueError('Loop212 native pointer getter/setter literal differs')
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    initial, old, expected, expected_global, native, services, expected_result = construct(recipe, rng)
    machine.mem_write(CONTEXT, initial)
    machine.mem_write(GLOBAL, struct.pack('<I', old))
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_ram[CONTEXT - 0x02000000:CONTEXT - 0x02000000 + 32] = expected
    expected_ram[GLOBAL - 0x02000000:GLOBAL - 0x02000000 + 4] = struct.pack('<I', expected_global)
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[:3] = [recipe['first'], recipe['mode'], recipe['flags']]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x30)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    frames, entries, returned, calls, trace, writes, observed = [], [], [], [], [], [], set()

    def before(engine, event):
        if bytes(engine.mem_read(CONTEXT, 32)) != event['contextBefore'] or struct.unpack('<I', bytes(engine.mem_read(GLOBAL, 4)))[0] != event['globalBefore']:
            raise ValueError(('Loop212 independent ordered state differs', hex(event['address'])))

    def step(engine, pc, width, unused):
        while frames and pc == frames[-1]['returnAddress']:
            frame = frames.pop()
            if engine.reg_read(UC_ARM_REG_SP) != frame['sp'] or [engine.reg_read(r) for r in REGS[4:12]] != frame['preserved']:
                raise ValueError('Loop212 native frame preservation differs')
            returned.append(dict(address=hex(frame['address']), result=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        trace.append(pc)
        if len(trace) > 5000:
            raise ValueError('Loop212 native instruction bound exceeded')
        mode = engine.reg_read(UC_ARM_REG_CPSR) & 255
        if pc in NATIVE:
            index = len(entries)
            if index >= len(native) or pc != native[index]['address']:
                raise ValueError('Loop212 independent native entry order differs')
            event = native[index]
            before(engine, event)
            arguments = [engine.reg_read(REGS[i]) for i in range(len(event['arguments']))]
            if arguments != event['arguments'] or mode != 0x30:
                raise ValueError('Loop212 independent native arguments/Thumb mode differ')
            entries.append(dict(address=hex(pc), arguments=arguments))
            frames.append(dict(address=pc, returnAddress=engine.reg_read(UC_ARM_REG_LR) & ~1,
                sp=engine.reg_read(UC_ARM_REG_SP), preserved=[engine.reg_read(r) for r in REGS[4:12]]))
        if ENTRY <= pc < ENTRY + 110:
            if mode != 0x30:
                raise ValueError('Loop212 caller Thumb mode differs')
            observed.update(range(pc, pc + width))
            return
        if any(a <= pc < a + n for a, n in NATIVE.items()):
            if mode != 0x30:
                raise ValueError('Loop212 actual helper Thumb mode differs')
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError(('Loop212 independent service/callback order differs', hex(pc), index))
        event = services[index]
        before(engine, event)
        arguments = [engine.reg_read(REGS[i]) for i in range(len(event['arguments']))]
        if arguments != event['arguments'] or mode != (0x30 if event['mode'] == 'thumb' else 0x10):
            raise ValueError('Loop212 independent provider arguments/target mode differ')
        calls.append(dict(address=hex(pc), mode=event['mode'], arguments=arguments, result=event['result'],
            effects=[dict(address=hex(a), bytesHex=b.hex()) for a, b in event['effects']]))
        for address, content in event['effects']:
            engine.mem_write(address, content)
        engine.reg_write(REGS[0], event['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 13 + register) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or CONTEXT <= address <= CONTEXT + 32 - size or GLOBAL <= address <= GLOBAL + 4 - size):
            raise ValueError('Loop212 native write outside classified state/private stack')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY | 1, STOP + 4, count=5001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or frames:
        raise ValueError('Loop212 actual top/native completion differs')
    expected_returns = [dict(address=hex(n['address']), result=n['result']) for n in native]
    if actual[0] != expected_result or actual[4:12] != registers[4:12] or returned != expected_returns or len(calls) != len(services):
        raise ValueError(('Loop212 independent return/native/service completion differs', actual[0], expected_result))
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram:
        raise ValueError('Loop212 complete context/pointer/RAM model differs')
    return dict(actualReturn=True, returnWord=actual[0], restoredSP=True, preservedRegisters=actual[4:12], nativeEntries=entries,
        nativeDependencyActualReturns=returned, providedCalls=calls, instructions=len(trace) - len(calls), observedCallerInstructionBytes=sorted(observed),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(), pcTrace=trace, writes=writes)
