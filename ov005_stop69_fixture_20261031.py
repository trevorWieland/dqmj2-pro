import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from ov005_stop69_models_20261031 import BUFFER, OTHER, LENGTH, GLOBAL, plan
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021D9060, 0x08000000, 0x0301FF00
NATIVE = {0x02007FF4: 20, 0x02008008: 24, 0x021D90F0: 16, 0x021D9124: 52, 0x021D8788: 44}


def execute(main, overlay, recipe, source_bytes=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x02410000, 0x2000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        if len(source_bytes) != 144:
            raise ValueError('Stop69 supplied source span would overlap adjacent native code')
        machine.mem_write(ENTRY, source_bytes)
    rng, expected = random.Random(recipe['seed']), plan(recipe)
    for address, size in [(BUFFER, LENGTH), (OTHER, LENGTH), (0x03000000, 0x20000)]:
        machine.mem_write(address, rng.randbytes(size))
    machine.mem_write(GLOBAL, struct.pack('<II', BUFFER, recipe['state']))
    machine.mem_write(BUFFER + 4, struct.pack('<I', recipe['callback']))
    for address in (BUFFER, OTHER):
        machine.mem_write(address + 0x5204, struct.pack('<HH', recipe['shift'], recipe['flags'] ^ (0xFFFF if expected['callback'] else 0)))
        machine.mem_write(address + 0x5210, struct.pack('<I', recipe['innerState']))
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    if expected['active']:
        struct.pack_into('<I', expected_ram, GLOBAL + 4 - 0x02000000, expected['state'])
    if expected['callback']:
        struct.pack_into('<I', expected_ram, GLOBAL - 0x02000000, expected['target'])
        struct.pack_into('<H', expected_ram, expected['target'] + 0x5206 - 0x02000000, recipe['flags'])
    if expected['cleanup']:
        struct.pack_into('<I', expected_ram, expected['target'] + 0x5214 - 0x02000000, 0)
    registers = [rng.getrandbits(32) for unused in range(13)]
    initial_cpsr = rng.getrandbits(4) << 28 | 0x1F | recipe['irq'] | recipe['fiq']
    machine.reg_write(UC_ARM_REG_CPSR, initial_cpsr)
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    visits, writes, pending, returned, supplied = [], [], [], [], []

    def step(engine, pc, size, unused):
        while pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['sp'] or [engine.reg_read(REGS[i]) for i in range(4, 12)] != item['preserved']:
                raise ValueError('Stop69 native stack/preserved registers differ')
            if item['address'] == 0x021D9124 and engine.reg_read(REGS[0]) != expected['query']:
                raise ValueError('Stop69 original halfword/shift query differs')
            returned.append(dict(address=hex(item['address']), physicalR0=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        if len(visits) >= 2000:
            raise ValueError('Stop69 instruction bound exceeded')
        visits.append(pc)
        if pc in (recipe['callback'] & ~1, 0x021D7874) and pc:
            cpsr = engine.reg_read(UC_ARM_REG_CPSR)
            if cpsr & 0xDF != 0x9F | recipe['fiq']:
                raise ValueError('Stop69 provider virtual CPU I/F/mode differs')
            if pc == recipe['callback'] & ~1:
                if not expected['callback'] or supplied or bool(cpsr & 32) != bool(recipe['callback'] & 1):
                    raise ValueError('Stop69 callback mode/order differs')
                if [engine.reg_read(REGS[i]) for i in (0, 1)] != [1, 0] or bytes(engine.mem_read(GLOBAL + 4, 4)) != struct.pack('<I', 1):
                    raise ValueError('Stop69 state1 must precede callback1/0')
                engine.mem_write(GLOBAL, struct.pack('<II', expected['target'], recipe['callbackState']))
                engine.mem_write(expected['target'] + 0x5206, struct.pack('<H', recipe['flags']))
                arguments = [1, 0]
            else:
                arguments = [engine.reg_read(REGS[i]) for i in range(3)]
                if not expected['message'] or arguments != [expected['target'] + 0x120, recipe['innerState'], 0]:
                    raise ValueError('Stop69 message-provider arguments differ')
                if bytes(engine.mem_read(expected['target'] + 0x5214, 4)) != bytes(4):
                    raise ValueError('Stop69 zero field must precede message provider')
            supplied.append(dict(address=hex(pc), mode='thumb' if cpsr & 32 else 'arm', arguments=arguments, suppliedReturn=0xDEAD1234))
            for register in (0, 1, 2, 3, 12):
                engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + len(supplied) * 17 + register) & 0xFFFFFFFF)
            lr = engine.reg_read(UC_ARM_REG_LR)
            engine.reg_write(UC_ARM_REG_CPSR, cpsr & 0x0FFFFFDF | ((recipe['seed'] + len(supplied)) & 15) << 28 | (32 if lr & 1 else 0))
            engine.reg_write(UC_ARM_REG_PC, lr)
            return
        if engine.reg_read(UC_ARM_REG_CPSR) & 32:
            raise ValueError('Stop69 wrong original ARM mode')
        if pc in NATIVE:
            pending.append(dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR), sp=engine.reg_read(UC_ARM_REG_SP),
                preserved=[engine.reg_read(REGS[i]) for i in range(4, 12)]))
            return
        if ENTRY <= pc < ENTRY + 144 or any(start < pc < start + size for start, size in NATIVE.items()):
            return
        raise ValueError(('Stop69 escaped native/provider scope', hex(pc)))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or address == GLOBAL + 4 and size == 4 or address == expected['target'] + 0x5214 and size == 4):
            raise ValueError('Stop69 unexpected native write')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=2001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or pending or len(returned) != expected['nativeReturns'] or len(supplied) != int(expected['callback']) + int(expected['message']):
        raise ValueError('Stop69 actual return/native completion differs')
    if actual[0] != 0x80 or actual[4:12] != registers[4:12] or machine.reg_read(UC_ARM_REG_CPSR) & 255 != initial_cpsr & 255:
        raise ValueError('Stop69 physical return/restored I/F/preserved registers differ')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram):
        raise ValueError('Stop69 independent complete RAM/late-read model differs')
    return dict(actualReturn=True, returnWord=actual[0], instructions=len(visits) - len(supplied), registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        providedCalls=supplied, nativeDependencyActualReturns=returned, pcTrace=visits, writes=writes,
        observedNativeCallerInstructionBytes=len({pc + i for pc in visits if ENTRY <= pc < ENTRY + 144 for i in range(4)}),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
