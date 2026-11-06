import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from ov000_parser169_models_20261031 import POOL, construct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021E3C0C, 0x08000000, 0x0301FF00
NATIVE = {0x021E3444: 52, 0x021E3478: 64, 0x0201D914: 52, 0x02025A28: 72,
    0x02024E0C: 540, 0x02025CA4: 632, 0x020259B4: 52, 0x021D8A08: 16}


def execute(main, overlay, recipe, candidate=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if candidate is not None:
        if len(candidate) != 272:
            raise ValueError('Parser169 candidate must preserve the complete272-byte span')
        machine.mem_write(ENTRY, candidate)
    setter_global = struct.unpack_from('<I', overlay, 0x021D8A14 - 0x021D7240)[0]
    if overlay[0x0222EC40 - 0x021D7240:0x0222EC50 - 0x021D7240] != b'hasigo_\0mapfix_\0':
        raise ValueError('Parser169 original prefix literals differ')
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    initial, pool, effects, expected_entries, expected_returns, services, expected_result = construct(recipe, rng, setter_global)
    for address, content in initial:
        machine.mem_write(address, content)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    for address, content in [(POOL, pool), *effects]:
        expected_ram[address - 0x02000000:address - 0x02000000 + len(content)] = content
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[0] = 0x02390000
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
                raise ValueError('Parser169 native callee frame differs')
            returned.append(dict(address=hex(frame['address']), result=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        trace.append(pc)
        if len(trace) > 5000 or engine.reg_read(UC_ARM_REG_CPSR) & 255 != 0x10:
            raise ValueError('Parser169 bounded ARM mode differs')
        if pc in NATIVE:
            index = len(entries)
            if index >= len(expected_entries) or hex(pc) != expected_entries[index]['address']:
                raise ValueError(('Parser169 independent native entry order differs', hex(pc), index))
            expected = expected_entries[index]
            arguments = [engine.reg_read(REGS[i]) for i in range(len(expected['arguments']))]
            if arguments != expected['arguments']:
                raise ValueError(('Parser169 independent numeric/native arguments differ', hex(pc), arguments, expected['arguments']))
            entries.append(dict(address=hex(pc), arguments=arguments))
            frames.append(dict(address=pc, returnAddress=engine.reg_read(UC_ARM_REG_LR) & ~1,
                sp=engine.reg_read(UC_ARM_REG_SP), preserved=[engine.reg_read(r) for r in REGS[4:12]]))
        if ENTRY <= pc < ENTRY + 260:
            observed.update(range(pc, pc + width))
            return
        if any(address <= pc < address + count for address, count in NATIVE.items()):
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError(('Parser169 independent provider order differs', hex(pc), index))
        service = services[index]
        arguments = [engine.reg_read(REGS[i]) for i in range(len(service['arguments']))]
        if arguments != service['arguments']:
            raise ValueError('Parser169 independent provider arguments differ')
        calls.append(dict(address=hex(pc), arguments=arguments, result=service['result'],
            effects=[dict(address=hex(a), bytesHex=b.hex()) for a, b in service['effects']]))
        for address, content in service['effects']:
            engine.mem_write(address, content)
        engine.reg_write(REGS[0], service['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 13 + register) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or POOL <= address <= POOL + 64 * 52 - size
                or setter_global + 4 <= address <= setter_global + 8 - size):
            raise ValueError('Parser169 write outside pool/setter/private stack')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=5001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or frames:
        raise ValueError('Parser169 actual top/native return completion differs')
    if actual[0] != expected_result or actual[4:12] != registers[4:12] or entries != expected_entries or returned != expected_returns or len(calls) != len(services):
        raise ValueError(('Parser169 independent return/native/provider model differs', actual[0], expected_result, returned, expected_returns))
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram:
        raise ValueError('Parser169 independent complete pool/global/RAM model differs')
    return dict(actualReturn=True, returnWord=actual[0], restoredSP=True, preservedRegisters=actual[4:12], nativeEntries=entries,
        nativeDependencyActualReturns=returned, providedCalls=calls, instructions=len(trace) - len(calls), observedCallerInstructionBytes=sorted(observed),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(), pcTrace=trace, writes=writes)
