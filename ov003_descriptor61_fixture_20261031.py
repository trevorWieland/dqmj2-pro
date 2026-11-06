import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021DEAF8, 0x08000000, 0x0301FF00
ARGUMENT, RECORD, CHILD = 0x02350000, 0x02351000, 0x02352000
BUFFER, TABLE, HOLDER = 0x021029D8, 0x02102A18, 0x02102980
NATIVE = {0x02049F24: 12, 0x02049F30: 28, 0x02008C58: 76, 0x02049AD0: 20, 0x02049F14: 16}


def recipes():
    return [dict(seed=0x161000 + index, inputWord=value, number=(0, 0x80000000, 0xFFFFFFFF)[index % 3],
        byte=(0, 1, 255)[index % 3], length=(0, 1, 31, 63, 64)[index % 5])
        for index, value in enumerate((0, 1, 7, 119, 120, 127, 128, 255, 256, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF))]


def execute(main, overlay, recipe, source_bytes=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        machine.mem_write(ENTRY, source_bytes)
    for offset, value in [(0x49F2C, BUFFER), (0x49F44, 0x02008C58), (0x49F48, BUFFER), (0x49AE0, TABLE), (0x49F20, HOLDER - 12)]:
        if struct.unpack_from('<I', main, offset)[0] != value:
            raise ValueError('Descriptor61 actual native mapping literal differs')
    rng = random.Random(recipe['seed'])
    for address, size in [(0x03000000, 0x20000), (BUFFER, 64), (RECORD, 16), (CHILD, 0x80)]:
        machine.mem_write(address, rng.randbytes(size))
    index = (recipe['inputWord'] + 8) & 255
    index -= 256 if index & 128 else 0
    row = TABLE + 12 * index
    if BUFFER <= row < BUFFER + 64:
        raise ValueError('Descriptor61 unsupported cleared descriptor alias')
    machine.mem_write(ARGUMENT, struct.pack('<I', recipe['inputWord']))
    machine.mem_write(row, struct.pack('<I', RECORD))
    machine.mem_write(RECORD + 4, struct.pack('<I', CHILD))
    machine.mem_write(CHILD + 0x68, struct.pack('<I', recipe['number']))
    machine.mem_write(CHILD + 0x5E, bytes([recipe['byte']]))
    payload = bytes((recipe['seed'] + i * 17) & 255 for i in range(recipe['length']))
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_ram[BUFFER - 0x02000000:BUFFER - 0x02000000 + 64] = payload + bytes(64 - len(payload))
    struct.pack_into('<I', expected_ram, HOLDER - 0x02000000, BUFFER)
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[0] = ARGUMENT
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    visits, writes, pending, returned, provided = [], [], [], [], []

    def step(engine, pc, size, unused):
        while pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['sp'] or [engine.reg_read(REGS[i]) for i in range(4, 12)] != item['preserved']:
                raise ValueError('Descriptor61 native stack/preserved registers differ')
            returned.append(dict(address=hex(item['address']), physicalR0=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        if len(visits) >= 2000 or engine.reg_read(UC_ARM_REG_CPSR) & 32:
            raise ValueError('Descriptor61 instruction/mode bound exceeded')
        visits.append(pc)
        if ENTRY <= pc < ENTRY + 104:
            return
        if pc in NATIVE:
            if pc == 0x02049AD0 and engine.reg_read(REGS[0]) != index & 0xFFFFFFFF:
                raise ValueError('Descriptor61 wrapped signed-byte index differs')
            if pc == 0x02049F14 and engine.reg_read(REGS[0]) != BUFFER:
                raise ValueError('Descriptor61 restored output pointer differs')
            pending.append(dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR), sp=engine.reg_read(UC_ARM_REG_SP),
                preserved=[engine.reg_read(REGS[i]) for i in range(4, 12)]))
            return
        if any(start < pc < start + size for start, size in NATIVE.items()):
            return
        if pc != 0x02046AF4 or provided:
            raise ValueError(('Descriptor61 escaped native/provider scope', hex(pc)))
        arguments = [engine.reg_read(REGS[i]) for i in range(4)] + list(struct.unpack('<II', bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_SP), 8))))
        if arguments != [0x021C9698, recipe['number'], recipe['byte'], 0, BUFFER, 255]:
            raise ValueError(('Descriptor61 formatter argument words differ', arguments))
        if bytes(engine.mem_read(BUFFER, 64)) != bytes(64):
            raise ValueError('Descriptor61 native clear must precede formatter')
        engine.mem_write(BUFFER, payload)
        engine.mem_write(HOLDER, b'\xff' * 4)
        provided.append(dict(address=hex(pc), arguments=arguments, suppliedBytes=len(payload), suppliedReturn=0xFFFFFFFF))
        for register in (0, 1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + register) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_CPSR, engine.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF | (recipe['seed'] & 15) << 28)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or BUFFER <= address <= BUFFER + 64 - size or address == HOLDER and size == 4):
            raise ValueError('Descriptor61 unexpected native write')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=2001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or pending or len(returned) != 5 or len(provided) != 1:
        raise ValueError('Descriptor61 actual return/native completion differs')
    if actual[0] != BUFFER or actual[4:12] != registers[4:12]:
        raise ValueError('Descriptor61 raw return/preserved registers differ')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram):
        raise ValueError('Descriptor61 complete independent RAM model differs')
    return dict(actualReturn=True, returnWord=actual[0], instructions=len(visits) - len(provided), registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        providedCalls=provided, nativeDependencyActualReturns=returned, pcTrace=visits, writes=writes,
        observedNativeCallerInstructionBytes=len({pc + i for pc in visits if ENTRY <= pc < ENTRY + 104 for i in range(4)}),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
