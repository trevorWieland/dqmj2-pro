import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ACTOR, INFO, TABLE, GLOBAL = 0x023A8000, 0x023A9000, 0x02360000, 0x020F69EC
STOP, SP = 0x08000000, 0x0301FF00
BODIES = {0x021DB9E0: 20, 0x021DBAAC: 28, 0x02044CDC: 56, 0x02044D14: 28}


def run(main, overlay):
    if struct.unpack_from('<I', main, 0x44D0C)[0] != GLOBAL or struct.unpack_from('<I', main, 0x44D2C)[0] != GLOBAL:
        raise ValueError('Message198 native table roots differ')
    cases = [(0x021DB9E0, index, nibble, nibble // 3) for index in [0, 1, 63, 127, 255] for nibble in range(16)]
    cases += [(0x021DBAAC, index, family, 0 if family == 63 else family)
        for index in [0, 1, 63, 127, 255] for family in [0, 1, 2, 62, 63, 64, 128, 255]]
    results = []
    for case, (entry, index, value, expected) in enumerate(cases):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.ctl_set_cpu_model(UC_CPU_ARM_946)
        for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
            machine.mem_map(address, size)
        machine.mem_write(0x02000000, main)
        machine.mem_write(0x021D7240, overlay)
        rng = random.Random(0x198AB000 + case)
        machine.mem_write(0x03000000, rng.randbytes(0x20000))
        table = bytearray(rng.randbytes(25600))
        if entry == 0x021DB9E0:
            halfword = (rng.getrandbits(16) & 0xF0FF) | (value << 8)
            struct.pack_into('<H', table, index * 100 + 4, halfword)
        else:
            table[index * 100 + 12] = value
        machine.mem_write(TABLE, bytes(table))
        machine.mem_write(GLOBAL + 4, struct.pack('<I', TABLE))
        machine.mem_write(ACTOR + 0x1E8, struct.pack('<I', INFO))
        machine.mem_write(INFO + 0x2A, struct.pack('<h', index))
        expected_ram = bytes(machine.mem_read(0x02000000, 0x400000))
        registers = [rng.getrandbits(32) for unused in range(13)]
        registers[0] = ACTOR
        for register, word in zip(REGS, registers):
            machine.reg_write(register, word)
        machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
        machine.reg_write(UC_ARM_REG_SP, SP)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        frames, returned, trace = [], [], []

        def step(engine, pc, width, unused):
            while frames and pc == frames[-1]['returnAddress']:
                frame = frames.pop()
                if engine.reg_read(UC_ARM_REG_SP) != frame['sp'] or [engine.reg_read(r) for r in REGS[4:12]] != frame['preserved']:
                    raise ValueError('Message198 actual table-chain frame differs')
                returned.append(dict(address=hex(frame['address']), result=engine.reg_read(REGS[0])))
            if pc == STOP:
                engine.emu_stop()
                return
            trace.append(pc)
            if len(trace) > 1000 or engine.reg_read(UC_ARM_REG_CPSR) & 255 != 0x10:
                raise ValueError('Message198 actual table-chain mode/bound differs')
            if pc in BODIES:
                frames.append(dict(address=pc, returnAddress=engine.reg_read(UC_ARM_REG_LR) & ~1,
                    sp=engine.reg_read(UC_ARM_REG_SP), preserved=[engine.reg_read(r) for r in REGS[4:12]]))
            if not any(a <= pc < a + n for a, n in BODIES.items()):
                raise ValueError('Message198 table-chain PC outside original bounded bodies')

        def written(engine, access, address, size, value, unused):
            if not 0x03000000 <= address <= SP - size:
                raise ValueError('Message198 actual table chain wrote outside private stack')

        machine.hook_add(UC_HOOK_CODE, step)
        machine.hook_add(UC_HOOK_MEM_WRITE, written)
        machine.emu_start(entry, STOP + 4, count=1001)
        raw_family = value if entry == 0x021DBAAC else expected
        callee = 0x02044CDC if entry == 0x021DB9E0 else 0x02044D14
        if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or frames:
            raise ValueError('Message198 actual table-chain return completion differs')
        if machine.reg_read(REGS[0]) != expected or [machine.reg_read(r) for r in REGS[4:12]] != registers[4:12]:
            raise ValueError('Message198 actual independent table return differs')
        if returned != [dict(address=hex(callee), result=raw_family), dict(address=hex(entry), result=expected)]:
            raise ValueError('Message198 actual table nested/tail returns differ')
        if bytes(machine.mem_read(0x02000000, 0x400000)) != expected_ram:
            raise ValueError('Message198 actual table-chain complete RAM differs')
        results.append(dict(entry=hex(entry), index=index, value=value, returnWord=expected,
            nativeActualReturns=returned, instructions=len(trace), pcTraceSha256=hashlib.sha256(struct.pack('<' + 'I' * len(trace), *trace)).hexdigest(),
            preservedRegisters=registers[4:12], ramSha256=hashlib.sha256(expected_ram).hexdigest()))
    return dict(cases=results, actualTopReturns=len(results), actualOriginalSdkReturns=len(results), providers=0,
        supportedIndices=[0, 1, 63, 127, 255], supportedTableRecords=256, tableStride=100,
        descriptorPointerOffset=0x1E8, signedIndexOffset=0x2A, tableRoot=hex(GLOBAL), tablePointerOffset=4,
        firstLookupFormula='((u16(record+4) >>8)&15)//3', secondLookupFormula='u8(record+12), then63 becomes0 in overlay wrapper',
        hiddenIncomingR1R2R3R12='Original leaf bodies define all these registers before use; no downstream calls',
        limitations=['Accessible synthetic table and valid nonnegative indices only; null/broken table and negative indices are unsupported',
            'Raw table fields have no semantic ID/category meaning; no real game initialization or table lifetime is established',
            'Separate wide lookup-word caller fixtures remain provider-qualified and are outside these original leaf return ranges'], sourceCredit=0)
