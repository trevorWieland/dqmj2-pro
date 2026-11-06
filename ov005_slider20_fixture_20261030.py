import hashlib
import random
import re
import struct
from functools import lru_cache

from ov005_slider20_models_20261030 import STATE, model
from project import ROOT
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021DB400, 0x08000000, 0x0301FF00
NATIVE = {0x02048A44, 0x02048A60, 0x0203515C, 0x02034D68}
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
        UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
        UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


@lru_cache(maxsize=1)
def functions():
    return {int(address, 0): dict(address=int(address, 0), mode=mode, bytes=int(size, 0)) for mode, size, address in
        re.findall(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)',
                   (ROOT / 'config/arm9/symbols.txt').read_text())}


def execute(main, overlay, recipe, source_bytes=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for start, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (0x04000000, 0x10000), (STOP, 0x1000)]:
        machine.mem_map(start, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        machine.mem_write(ENTRY, source_bytes)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(STATE, rng.randbytes(0x80))
    machine.mem_write(0x021E9A28, rng.randbytes(0xA20))
    machine.mem_write(STATE + 0x2C, struct.pack('<I', recipe['scroll']))
    machine.mem_write(STATE + 0x40, struct.pack('<I', recipe['mode']))
    machine.mem_write(STATE + 0x68, struct.pack('<I', recipe['flag']))
    machine.mem_write(0x021E9EA8 + 0x14, struct.pack('<I', recipe['objectType']))
    machine.mem_write(0x04000000, rng.randbytes(0x10000))
    expected = model(recipe, bytes(machine.mem_read(0x02000000, 0x400000)), bytes(machine.mem_read(0x04000000, 0x10000)))
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    inventory, visits, writes, pending, returned = functions(), [], [], [], []

    def step(engine, pc, size, unused):
        while pending and pc == pending[-1]['returnPc']:
            previous = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != previous['sp']:
                raise ValueError('Slider20 actual native dependency stack differs')
            returned.append(dict(module='main', address=hex(previous['address']), actualReturn=True,
                                 physicalR0=engine.reg_read(UC_ARM_REG_R0)))
        if pc == STOP:
            engine.emu_stop()
            return
        if len(visits) >= 1000:
            raise ValueError('Slider20 instruction bound exceeded')
        visits.append(pc)
        if pc in NATIVE:
            item = inventory[pc]
            if item['mode'] != 'arm' or engine.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('Slider20 original dependency mode differs')
            pending.append(dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR), sp=engine.reg_read(UC_ARM_REG_SP)))
            return
        caller_length = 464 if source_bytes is None else len(source_bytes)
        if ENTRY <= pc < ENTRY + caller_length or pending and pending[-1]['address'] <= pc < pending[-1]['address'] + inventory[pending[-1]['address']]['bytes']:
            if engine.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('Slider20 caller/native mode differs')
            return
        raise ValueError(('Unsupported slider20 active-object dependency', hex(pc), recipe['objectType']))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, lambda engine, access, address, size, value, unused: writes.append((address, size, value)))
    machine.emu_start(ENTRY, STOP + 4, count=1001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or pending:
        raise ValueError('Slider20 failed actual return/stack/pending gate')
    if actual[0] != expected['returnWord'] or actual[4:12] != registers[4:12]:
        raise ValueError('Slider20 return/preserved registers differ')
    ram, io = bytes(machine.mem_read(0x02000000, 0x400000)), bytes(machine.mem_read(0x04000000, 0x10000))
    ram_writes = [item for item in writes if 0x02000000 <= item[0] < 0x02400000]
    io_writes = [item for item in writes if 0x04000000 <= item[0] < 0x04010000]
    if ram != expected['ram'] or ram_writes != expected['nativeRamWrites']:
        raise ValueError(('Slider20 complete RAM/write-order model differs', recipe))
    if io != expected['io'] or io_writes != expected['nativeIoWrites']:
        raise ValueError(('Slider20 complete MMIO/write-order model differs', recipe))
    for address, size, value in writes:
        if not (0x03000000 <= address <= SP - size or 0x02000000 <= address < 0x02400000 or 0x04000000 <= address < 0x04010000):
            raise ValueError(('Slider20 unsupported native write', hex(address), size))
    return dict(actualReturn=True, returnWord=actual[0], instructions=len(visits), nativeDependencyActualReturns=returned,
        providedCalls=[], pcTrace=visits, writes=writes, registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        ramSha256=hashlib.sha256(ram).hexdigest(), ioSha256=hashlib.sha256(io).hexdigest(),
        stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
