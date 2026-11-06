import bisect
import hashlib
import random
import re
import struct
from functools import cache

from ov001_ability28_fixture_20261031 import REGS
from ov005_bucket64_models_20261031 import RNG_STATE, PROGRESS, OUTPUT, TABLES, model
from project import ROOT
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021E6B30, 0x08000000, 0x0301FF00
NATIVE = {0x0203D294, 0x02026350, 0x02063B18, 0x020642EC}


@cache
def inventory():
    rows = [(int(address, 0), int(address, 0) + int(size, 0), mode) for mode, size, address in
        re.findall(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', (ROOT / 'config/arm9/symbols.txt').read_text())]
    rows.sort()
    return [row[0] for row in rows], rows


def execute(main, overlay, recipe, source_bytes=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        machine.mem_write(ENTRY, source_bytes)
    if struct.unpack_from('<I', main, 0x63B24)[0] != PROGRESS or struct.unpack_from('<I', main, 0x642F4)[0] != OUTPUT:
        raise ValueError('Bucket64 actual native global literals differ')
    if [tuple(overlay[address - 0x021D7240:address - 0x021D7240 + 4]) for address in (0x021E7768, 0x021E776C, 0x021E7770, 0x021E7774)] != TABLES:
        raise ValueError('Bucket64 measured original cumulative tables differ')
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(PROGRESS, rng.randbytes(0x20))
    machine.mem_write(PROGRESS, bytes([recipe['progress0']]))
    machine.mem_write(PROGRESS + 20, bytes([recipe['progress20']]))
    machine.mem_write(RNG_STATE, struct.pack('<I', recipe['rngWord']))
    machine.mem_write(OUTPUT, rng.randbytes(8))
    expected = model(recipe)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    struct.pack_into('<I', expected_ram, RNG_STATE - 0x02000000, expected['rngAfter'])
    expected_ram[OUTPUT - 0x02000000] = expected['output']
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    starts, ranges = inventory()
    visits, writes, pending, returned, provided, progress_reads = [], [], [], [], [], []

    def step(engine, pc, size, unused):
        while pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['sp'] or [engine.reg_read(REGS[i]) for i in range(4, 12)] != item['preserved']:
                raise ValueError('Bucket64 actual native stack/preserved registers differ')
            if item['address'] == 0x0203D294:
                index = sum(row['address'] == '0x203d294' for row in returned)
                if engine.reg_read(REGS[0]) != expected['draws'][index]:
                    raise ValueError('Bucket64 actual bounded RNG result differs')
            returned.append(dict(address=hex(item['address']), physicalR0=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        if len(visits) >= 5000:
            raise ValueError('Bucket64 instruction bound exceeded')
        visits.append((pc, size))
        if ENTRY <= pc < ENTRY + 232:
            if engine.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('Bucket64 wrong caller ARM mode')
            return
        if pc == 0x021E63E8:
            if provided or engine.reg_read(REGS[0]) != expected['bucket'] + 1:
                raise ValueError('Bucket64 raw category call argument differs')
            if struct.unpack('<I', bytes(engine.mem_read(RNG_STATE, 4)))[0] != expected['rngAfter']:
                raise ValueError('Bucket64 both native draws must precede category provider')
            provided.append(dict(address=hex(pc), argument=engine.reg_read(REGS[0]), suppliedReturn=0xDEAD1234))
            engine.mem_write(OUTPUT, b'\xff')
            for register in (0, 1, 2, 3, 12):
                engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + register) & 0xFFFFFFFF)
            engine.reg_write(UC_ARM_REG_CPSR, engine.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF | (recipe['seed'] & 15) << 28)
            engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))
            return
        index = bisect.bisect_right(starts, pc) - 1
        if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
            raise ValueError(('Bucket64 escaped qualified native body', hex(pc)))
        entry = ranges[index]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[2] == 'thumb'):
            raise ValueError('Bucket64 wrong native callee mode')
        if pc in NATIVE:
            if pc == 0x0203D294 and engine.reg_read(REGS[0]) != 10:
                raise ValueError('Bucket64 native RNG bound differs')
            if pc == 0x02063B18:
                progress_reads.append(engine.reg_read(REGS[0]))
            pending.append(dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR) & ~1, sp=engine.reg_read(UC_ARM_REG_SP),
                preserved=[engine.reg_read(REGS[i]) for i in range(4, 12)]))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or address == RNG_STATE and size == 4 or address == OUTPUT and size == 1):
            raise ValueError('Bucket64 unexpected native write')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=5001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or pending or len(returned) != 8 or len(provided) != 1 or progress_reads != [0, 0, 20]:
        raise ValueError('Bucket64 actual return/native call order/completion differs')
    if actual[0] != OUTPUT or actual[4:12] != registers[4:12]:
        raise ValueError('Bucket64 raw pointer return/preserved registers differ')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram):
        raise ValueError('Bucket64 independent full RAM/state/byte model differs')
    return dict(actualReturn=True, returnWord=actual[0], instructions=len(visits) - len(provided), registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        providedCalls=provided, nativeDependencyActualReturns=returned, rngActualReturns=2,
        observedNativeCallerInstructionRanges=[(pc, size) for pc, size in visits if ENTRY <= pc < ENTRY + 232],
        pcTraceSha256=hashlib.sha256(repr(visits).encode()).hexdigest(), writeTraceSha256=hashlib.sha256(repr(writes).encode()).hexdigest(),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
