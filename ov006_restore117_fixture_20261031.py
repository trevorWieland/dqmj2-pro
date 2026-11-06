import hashlib
import random
import re
import struct
from functools import cache

from ov001_ability28_fixture_20261031 import REGS
from project import ROOT
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, CONTEXT, STOP, SP = 0x02204684, 0x0221C1B4, 0x08000000, 0x0301FF00
WRAPPERS = {0x02003CF8: 0x020E3306, 0x02003D0C: 0x020E3308, 0x02003DCC: 0x020E3316, 0x02003DE0: 0x020E3318}
SETTERS = [0x02002E5C, 0x020030EC, 0x0200323C, 0x0200333C, 0x020033E8, 0x020035C0,
    0x020036A8, 0x020038A8, 0x02003950, 0x020039C0, 0x02003A40, 0x02003888]
OFFSETS = list(range(0, 44, 4)) + [48]


def recipes():
    return [dict(seed=0x217000 + index, variant=index) for index in range(16)]


@cache
def modes():
    result = {}
    for name in ['config/arm9/symbols.txt', 'config/arm9/overlays/ov006/symbols.txt']:
        for mode, address in re.findall(r'kind:function\((arm|thumb),size=0x[0-9a-f]+\) addr:(0x[0-9a-f]+)', (ROOT / name).read_text()):
            result[int(address, 0)] = mode
    return result


def execute(main, overlay, recipe, injected=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (0x04000000, 0x2000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if injected is not None:
        if len(injected) != 188:
            raise ValueError('Restore117 injection must preserve188-byte span')
        machine.mem_write(ENTRY, injected)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(CONTEXT, rng.randbytes(52))
    machine.mem_write(0x04000000, rng.randbytes(0x2000))
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_mmio = bytearray(machine.mem_read(0x04000000, 0x2000))
    services = [dict(address=0x02003C18, arguments=[pointer], writes=[], result=(recipe['variant'] << 24) | i)
        for i, pointer in enumerate(WRAPPERS.values())]
    words = [(recipe['seed'] * 0x9E3779B9 + i * 0x13579BDF) & 0xFFFFFFFF for i in range(13)]
    services.append(dict(address=0x02204740, arguments=[], result=0, writes=[(CONTEXT, struct.pack('<13I', *words))]))
    for i, (address, offset) in enumerate(zip(SETTERS, OFFSETS)):
        writes = []
        if i + 1 < len(OFFSETS):
            following = OFFSETS[i + 1] // 4
            words[following] = (recipe['seed'] ^ (0xFA000000 + i * 0x12345)) & 0xFFFFFFFF
            writes.append((CONTEXT + OFFSETS[i + 1], struct.pack('<I', words[following])))
        if i == len(SETTERS) - 1:
            writes += [(0x04000000 + offset, bytes([0xA0 + recipe['variant']]) * size)
                for offset, size in [(0x50, 2), (0x1050, 2), (0x10, 16), (0x1010, 16)]]
        services.append(dict(address=address, arguments=[words[offset // 4]], result=0xDEAD0000 | i, writes=writes))
    for service in services:
        for address, content in service['writes']:
            if address >= 0x04000000:
                expected_mmio[address - 0x04000000:address - 0x04000000 + len(content)] = content
            else:
                expected_ram[address - 0x02000000:address - 0x02000000 + len(content)] = content
    for offset, size in [(0x50, 2), (0x1050, 2), (0x10, 16), (0x1010, 16)]:
        expected_mmio[offset:offset + size] = bytes(size)
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x30)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    frames, returned, calls, visits, writes = [], [], [], [], []

    def step(engine, pc, size, unused):
        if frames and pc == frames[-1]['returnAddress']:
            frame = frames.pop()
            if engine.reg_read(UC_ARM_REG_SP) != frame['sp'] or [engine.reg_read(r) for r in REGS[4:12]] != frame['preserved']:
                raise ValueError('Restore117 actual wrapper frame differs')
            returned.append(dict(address=hex(frame['address']), result=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        visits.append((pc, size))
        if len(visits) > 5000 or engine.reg_read(UC_ARM_REG_CPSR) & 31 != 0x10:
            raise ValueError('Restore117 bounded user mode differs')
        thumb = bool(engine.reg_read(UC_ARM_REG_CPSR) & 32)
        if ENTRY <= pc < ENTRY + 188:
            if not thumb:
                raise ValueError(('Restore117 caller Thumb mode differs', hex(pc), hex(engine.reg_read(UC_ARM_REG_CPSR)), calls[-1:] ))
            return
        if any(address <= pc < address + 20 for address in WRAPPERS):
            if thumb:
                raise ValueError('Restore117 native wrapper ARM mode differs')
            if pc in WRAPPERS:
                frames.append(dict(address=pc, returnAddress=engine.reg_read(UC_ARM_REG_LR) & ~1, sp=engine.reg_read(UC_ARM_REG_SP),
                    preserved=[engine.reg_read(r) for r in REGS[4:12]]))
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address'] or thumb != (modes()[pc] == 'thumb'):
            raise ValueError(('Restore117 mode-checked provider order differs', hex(pc), index, thumb))
        service = services[index]
        arguments = [engine.reg_read(REGS[i]) for i in range(len(service['arguments']))]
        if arguments != service['arguments']:
            raise ValueError(('Restore117 independent late snapshot argument differs', index, arguments, service['arguments']))
        calls.append(dict(address=hex(pc), arguments=arguments, mode=modes()[pc], suppliedReturn=service['result'],
            writes=[dict(address=hex(address), bytesHex=content.hex()) for address, content in service['writes']]))
        for address, content in service['writes']:
            engine.mem_write(address, content)
        engine.reg_write(REGS[0], service['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 17 + register) & 0xFFFFFFFF)
        target = engine.reg_read(UC_ARM_REG_LR)
        engine.reg_write(UC_ARM_REG_CPSR, engine.reg_read(UC_ARM_REG_CPSR) & ~32 | (32 if target & 1 else 0))
        engine.reg_write(UC_ARM_REG_PC, target)

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or 0x04000000 <= address <= 0x04002000 - size):
            raise ValueError('Restore117 unexpected native write')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY | 1, STOP + 4, count=5001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or frames or len(calls) != len(services):
        raise ValueError('Restore117 actual return/SP/call completion differs')
    if actual[0] != 0 or actual[4:12] != registers[4:12] or len(returned) != 4:
        raise ValueError('Restore117 physical return/native wrapper count differs')
    ram, mmio = bytes(machine.mem_read(0x02000000, 0x400000)), bytes(machine.mem_read(0x04000000, 0x2000))
    if ram != expected_ram or mmio != expected_mmio:
        raise ValueError('Restore117 full snapshot/MMIO model differs')
    return dict(actualReturn=True, registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        instructions=len(visits) - len(calls), pcTrace=visits, writes=writes, providedCalls=calls,
        nativeDependencyActualReturns=returned, ramSha256=hashlib.sha256(ram).hexdigest(), mmioSha256=hashlib.sha256(mmio).hexdigest(),
        stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
        observedNativeCallerInstructionBytes=len({pc + i for pc, size in visits if ENTRY <= pc < ENTRY + 188 for i in range(size)}))
