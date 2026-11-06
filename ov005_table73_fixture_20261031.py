import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021E6C18, 0x08000000, 0x0301FF00
PROGRESS, OUTPUT, COUNTER, TABLE = 0x021C0DC8, 0x021B9E94, 0x021ED458, 0x021E6F2C
NATIVE = {0x02063B18: 16, 0x02064304: 60}


def recipes():
    profiles = [(0, 0), (10, 28), (11, 28), (12, 28), (13, 28), (255, 28), (13, 29), (255, 255)]
    counters = (0, 0x6977F, 0x69780, 0x69781, 0x13C67F, 0x13C680, 0x13C681, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF)
    return [dict(seed=0x173000 + profile * 10 + index, progress0=values[0], progress20=values[1], counter=counter)
        for profile, values in enumerate(profiles) for index, counter in enumerate(counters)]


def execute(main, overlay, recipe, source_bytes=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        if len(source_bytes) != 176:
            raise ValueError('Table73 reject adjacent source overlap')
        machine.mem_write(ENTRY, source_bytes)
    if struct.unpack_from('<I', main, 0x63B24)[0] != PROGRESS or struct.unpack_from('<I', main, 0x6433C)[0] != OUTPUT:
        raise ValueError('Table73 measured native global literals differ')
    table = bytes(machine.mem_read(TABLE, 144))
    base = 3 * (int(recipe['progress0'] >= 11) + int(recipe['progress0'] >= 13))
    if recipe['progress20'] >= 29:
        base = 9
    index = base + int(recipe['counter'] >= 0x69780) + int(recipe['counter'] >= 0x13C680)
    row = table[index * 12:index * 12 + 12]
    rng = random.Random(recipe['seed'])
    for address, size in [(0x03000000, 0x20000), (OUTPUT, 0x24), (PROGRESS, 0x20)]:
        machine.mem_write(address, rng.randbytes(size))
    machine.mem_write(PROGRESS, bytes([recipe['progress0']]))
    machine.mem_write(PROGRESS + 20, bytes([recipe['progress20']]))
    machine.mem_write(COUNTER, struct.pack('<I', recipe['counter']))
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_ram[OUTPUT + 0x14 - 0x02000000:OUTPUT + 0x20 - 0x02000000] = row
    return_word = struct.unpack_from('<H', row, 10)[0]
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    visits, writes, pending, returned, progress_reads = [], [], [], [], []

    def step(engine, pc, size, unused):
        while pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['sp'] or [engine.reg_read(REGS[i]) for i in range(4, 12)] != item['preserved']:
                raise ValueError('Table73 actual native stack/preserved registers differ')
            returned.append(dict(address=hex(item['address']), physicalR0=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        if len(visits) >= 2000 or engine.reg_read(UC_ARM_REG_CPSR) & 32:
            raise ValueError('Table73 instruction/mode bound exceeded')
        visits.append(pc)
        if pc in NATIVE:
            if pc == 0x02063B18:
                progress_reads.append(engine.reg_read(REGS[0]))
            else:
                pointer, local = engine.reg_read(REGS[0]), SP - 152
                if pointer != local + index * 12 or bytes(engine.mem_read(local, 144)) != table:
                    raise ValueError('Table73 independent local-table/selected-row model differs')
                if local + 144 != SP - 8:
                    raise ValueError('Table73 local table escapes native144-byte frame')
            pending.append(dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR), sp=engine.reg_read(UC_ARM_REG_SP),
                preserved=[engine.reg_read(REGS[i]) for i in range(4, 12)]))
            return
        if ENTRY <= pc < ENTRY + 176 or any(start < pc < start + size for start, size in NATIVE.items()):
            return
        raise ValueError(('Table73 escaped original native scope', hex(pc)))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or OUTPUT + 0x14 <= address <= OUTPUT + 0x20 - size and size == 2):
            raise ValueError('Table73 unexpected native write')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=2001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or pending or len(returned) != 4 or progress_reads != [0, 0, 20]:
        raise ValueError('Table73 actual return/native order/completion differs')
    if actual[0] != return_word or actual[4:12] != registers[4:12]:
        raise ValueError('Table73 raw halfword return/preserved registers differ')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram):
        raise ValueError('Table73 independent full RAM/row-copy model differs')
    return dict(actualReturn=True, returnWord=actual[0], instructions=len(visits), registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        providedCalls=[], nativeDependencyActualReturns=returned, pcTrace=visits, writes=writes, selectedRow=index,
        observedNativeCallerInstructionBytes=len({pc + i for pc in visits if ENTRY <= pc < ENTRY + 176 for i in range(4)}),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
