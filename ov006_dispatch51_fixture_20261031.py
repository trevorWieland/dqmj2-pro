import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from ov006_dispatch51_models_20261031 import STATE, OUTPUT, TABLE, REG_A, REG_B, NEXT, protocol, expected
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021F5870, 0x08000000, 0x0301FF00
NATIVE = {0x021F5328: 12, 0x021F5334: 16, 0x021F5344: 24, 0x021F52CC: 12, 0x02203908: 76}


def execute(main, overlay, recipe, source_bytes=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for start, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (0x04000000, 0x2000), (STOP, 0x1000)]:
        machine.mem_map(start, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        machine.mem_write(ENTRY, source_bytes)
    rng = random.Random(recipe['seed'])
    for address, size in [(STATE, 0x30), (0x03000000, 0x20000), (0x04000000, 0x2000)]:
        machine.mem_write(address, rng.randbytes(size))
    machine.mem_write(STATE, bytes([recipe['selector'] ^ 1]))
    machine.mem_write(STATE + 8, struct.pack('<I', recipe['flags'] ^ 0xFFFFFFFF))
    if any(struct.unpack_from('<I', overlay, a - 0x021D7240)[0] != STATE for a in (0x021F5330, 0x021F5340, 0x021F5358, 0x021F52D4)):
        raise ValueError('Dispatch51 independently measured native state literals differ')
    table = struct.unpack('<7I', bytes(machine.mem_read(TABLE, 28)))
    if table != (0x0220DA54, 0x0220DA04, 0x0220DA34, 0x0220DA24, 0x0220DA14, 0x0220DA44, 0x0220D9F4):
        raise ValueError('Dispatch51 measured7-word table differs')
    calls = protocol(recipe, table)
    expected_ram, expected_io = expected(recipe, bytes(machine.mem_read(0x02000000, 0x400000)), bytes(machine.mem_read(0x04000000, 0x2000)))
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x30)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    visits, writes, provided, returned, pending, io_writes = [], [], [], [], [], []

    def step(engine, pc, size, unused):
        while pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['sp'] or [engine.reg_read(REGS[i]) for i in range(4, 12)] != item['preserved']:
                raise ValueError('Dispatch51 native return/stack/preserved registers differ')
            returned.append(dict(address=hex(item['address']), actualReturn=True, physicalR0=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        if len(visits) >= 2000:
            raise ValueError('Dispatch51 instruction bound exceeded')
        visits.append((pc, size))
        if not engine.reg_read(UC_ARM_REG_CPSR) & 32:
            raise ValueError('Dispatch51 wrong caller/callee Thumb mode')
        if ENTRY <= pc < ENTRY + 360:
            return
        if pc in NATIVE:
            if pc == 0x02203908 and [engine.reg_read(REGS[i]) for i in (0, 1)] != [1 - sum(item['address'] == '0x2203908' for item in returned), 2]:
                raise ValueError('Dispatch51 actual MMIO helper arguments/order differ')
            if pc == 0x021F5344 and engine.reg_read(REGS[0]) != 2 or pc == 0x021F52CC and engine.reg_read(REGS[0]) != NEXT:
                raise ValueError('Dispatch51 native getter/setter arguments differ')
            pending.append(dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR) & ~1, sp=engine.reg_read(UC_ARM_REG_SP),
                preserved=[engine.reg_read(REGS[i]) for i in range(4, 12)]))
            return
        if any(address < pc < address + size for address, size in NATIVE.items()):
            return
        index = len(provided)
        if index >= len(calls) or calls[index]['address'] != pc:
            raise ValueError(('Dispatch51 unexpected provider/order', hex(pc), index))
        service = calls[index]
        args = [engine.reg_read(REGS[i]) for i in range(len(service['arguments']))]
        if args != service['arguments']:
            raise ValueError(('Dispatch51 argument words differ', hex(pc), args, service))
        if pc == 0x021F26E4:
            engine.mem_write(STATE, bytes([recipe['selector']]))
            engine.mem_write(STATE + 8, struct.pack('<I', recipe['flags']))
        if pc == 0x021F2798 and bytes(engine.mem_read(OUTPUT, 4)) != struct.pack('<I', recipe['objectWord']):
            raise ValueError('Dispatch51 full-word output must be stored before descriptor queries')
        provided.append(dict(address=hex(pc), mode='thumb', arguments=args, suppliedReturn=service['result']))
        engine.reg_write(REGS[0], service['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 17 + register) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_CPSR, engine.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF | ((recipe['seed'] + index) & 15) << 28)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or address == OUTPUT and size == 4 or address == STATE + 12 and size == 4 or address in (REG_A, REG_B) and size == 2 or address in (0x04000000, 0x04001000) and size == 4):
            raise ValueError(('Dispatch51 unexpected native write', hex(address), size))
        writes.append((address, size, value))
        if 0x04000000 <= address < 0x04002000:
            io_writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY | 1, STOP + 4, count=2001)
    actual = [machine.reg_read(register) for register in REGS]
    count = 6 if recipe['selector'] != 1 or recipe['flags'] & 0x20 else 7
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or pending or len(returned) != count or len(provided) != len(calls):
        raise ValueError(('Dispatch51 actual return/stack/protocol completion differs', len(returned), count))
    if actual[4:12] != registers[4:12] or actual[0] != NEXT:
        raise ValueError('Dispatch51 preserved registers/raw next-pointer return differs')
    if bytes(machine.mem_read(0x02000000, 0x400000)) != bytes(expected_ram) or bytes(machine.mem_read(0x04000000, 0x2000)) != bytes(expected_io):
        raise ValueError('Dispatch51 complete RAM/MMIO model differs')
    if [row[:2] for row in io_writes] != [(REG_A, 2), (REG_B, 2), (REG_B, 2), (0x04001000, 4), (0x04000000, 4)]:
        raise ValueError('Dispatch51 ordered repeated MMIO stores differ')
    observed = {pc + offset for pc, size in visits if ENTRY <= pc < ENTRY + 360 for offset in range(size)}
    return dict(actualReturn=True, returnWord=actual[0], instructions=len(visits) - len(provided),
        registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR), providedCalls=provided, nativeDependencyActualReturns=returned,
        observedNativeCallerInstructionBytes=len(observed), observedNativeCallerInstructionRanges=sorted({(pc, size) for pc, size in visits if ENTRY <= pc < ENTRY + 360}), pcTraceSha256=hashlib.sha256(repr(visits).encode()).hexdigest(),
        writeTraceSha256=hashlib.sha256(repr(writes).encode()).hexdigest(), ioWrites=io_writes,
        ramSha256=hashlib.sha256(expected_ram).hexdigest(), ioSha256=hashlib.sha256(expected_io).hexdigest(),
        stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
