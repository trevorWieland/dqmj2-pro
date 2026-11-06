import bisect
import hashlib
import random
import re
import struct
from functools import cache

from ov001_ability28_fixture_20261031 import REGS
from project import ROOT
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, CONTEXT, FORMAT, STOP, SP = 0x021F6008, 0x02236EE4, 0x0222F2F0, 0x08000000, 0x0301FF00


def recipes():
    return [dict(seed=0x216000 + i, state=state, variant=v)
        for i, (state, v) in enumerate((state, v) for state in (0, 1, 2, 3, 0x7FFFFFFF, 0xFFFFFFFF) for v in range(4))]


@cache
def inventory():
    rows = sorted((int(address, 0), int(address, 0) + int(size, 0), mode)
        for mode, size, address in re.findall(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)',
            (ROOT / 'config/arm9/symbols.txt').read_text()))
    return [row[0] for row in rows], rows


def execute(main, overlay, recipe, injected=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x01FF0000, 0x10000), (0x02000000, 0x400000), (0x03000000, 0x20000), (0x04000000, 0x1000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if injected is not None:
        if len(injected) != 344:
            raise ValueError('Setup116 injection must preserve344-byte native span')
        machine.mem_write(ENTRY, injected)
    filename = overlay[FORMAT - 0x021D7240:].split(b'\0', 1)[0]
    if filename != b'tournament_bg_cut.csc' or len(filename) >= 32 or b'%' in filename:
        raise ValueError('Setup116 bounded original literal format differs')
    expected_buffer = filename + bytes(32 - len(filename))
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(CONTEXT, rng.randbytes(0x24))
    machine.mem_write(CONTEXT + 32, struct.pack('<I', recipe['state']))
    machine.mem_write(0x04000000, rng.randbytes(0x1000))
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_mmio = bytearray(machine.mem_read(0x04000000, 0x1000))
    v = recipe['variant']
    selected = [recipe['state'], 0, 2, 0xFFFFFFFF][v]
    returned = [0, 1, 0x80000000, 0xFFFFFFFF][v]
    expected_ram[CONTEXT - 0x02000000 + 32:CONTEXT - 0x02000000 + 36] = struct.pack('<I', selected ^ 0xFFFFFFFF)
    struct.pack_into('<I', expected_ram, CONTEXT - 0x02000000 + 28, returned)
    expected_ram[CONTEXT - 0x02000000 + 2] = 2
    for offset in (8, 12, 14):
        value = struct.unpack_from('<H', expected_mmio, offset)[0] ^ (0xA55A + offset)
        struct.pack_into('<H', expected_mmio, offset, value)
    for offset, value in [(8, 2), (12, 1), (14, 3)]:
        old = struct.unpack_from('<H', expected_mmio, offset)[0]
        struct.pack_into('<H', expected_mmio, offset, (old & ~3) | value)
    old = struct.unpack_from('<H', expected_mmio, 12)[0]
    struct.pack_into('<H', expected_mmio, 12, (old & 0x43) | 0x218)
    services = [(0x02061C1C, [6, 7, 1, 18, 2, 0, 0])]
    if selected in (0, 1, 2):
        services.append((0x01FFB50C, [6, 16, 13, (3, 38, 39)[selected], 1]))
    services.append((0x0203CC2C, None))
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    starts, ranges = inventory()
    calls, frames, returned_native, visits, writes, buffers = [], [], [], [], [], []

    def step(engine, pc, size, unused):
        while frames and pc == frames[-1]['returnAddress']:
            frame = frames.pop()
            if engine.reg_read(UC_ARM_REG_SP) != frame['sp'] or [engine.reg_read(r) for r in REGS[4:12]] != frame['preserved']:
                raise ValueError(('Setup116 native formatter frame differs', hex(frame['address'])))
            returned_native.append(dict(address=hex(frame['address']), result=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        visits.append(pc)
        if len(visits) > 50000 or engine.reg_read(UC_ARM_REG_CPSR) & 31 != 0x10:
            raise ValueError('Setup116 bounded user mode differs')
        provider = next((item for item in services if item[0] == pc), None)
        if provider:
            index = len(calls)
            if index >= len(services) or provider != services[index]:
                raise ValueError('Setup116 provider order differs')
            expected = provider[1]
            if expected is None:
                if not buffers:
                    raise ValueError('Setup116 constructor before actual formatter')
                expected = [buffers[-1], 2]
                if bytes(engine.mem_read(expected[0], 32)) != expected_buffer:
                    raise ValueError('Setup116 actual32-byte formatted buffer differs')
            actual = [engine.reg_read(REGS[i]) if i < 4 else struct.unpack('<I', bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_SP) + 4 * (i - 4), 4)))[0]
                for i in range(len(expected))]
            if actual != expected:
                raise ValueError(('Setup116 independent provider arguments differ', actual, expected))
            calls.append(dict(address=hex(pc), arguments=actual))
            if pc == 0x02061C1C:
                engine.mem_write(CONTEXT + 32, struct.pack('<I', selected))
            if pc == 0x0203CC2C:
                engine.mem_write(CONTEXT + 32, struct.pack('<I', selected ^ 0xFFFFFFFF))
                engine.mem_write(CONTEXT + 2, b'\xEE')
                engine.mem_write(CONTEXT + 28, struct.pack('<I', returned ^ 0xDEADBEEF))
                for offset in (8, 12, 14):
                    value = struct.unpack('<H', bytes(engine.mem_read(0x04000000 + offset, 2)))[0] ^ (0xA55A + offset)
                    engine.mem_write(0x04000000 + offset, struct.pack('<H', value))
            engine.reg_write(REGS[0], returned if pc == 0x0203CC2C else 0)
            for register in (1, 2, 3, 12):
                engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 17 + register) & 0xFFFFFFFF)
            engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))
            return
        if ENTRY <= pc < ENTRY + 344:
            if engine.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('Setup116 caller changed instruction mode')
            return
        owner_index = bisect.bisect_right(starts, pc) - 1
        owner = ranges[owner_index] if owner_index >= 0 else None
        if not owner or not owner[0] <= pc < owner[1] or bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (owner[2] == 'thumb'):
            raise ValueError(('Setup116 unsupported native formatter PC/mode', hex(pc)))
        if pc == 0x0201D444:
            destination = engine.reg_read(REGS[0])
            if engine.reg_read(REGS[1]) != FORMAT or bytes(engine.mem_read(destination, 32)) != bytes(32):
                raise ValueError('Setup116 buffer must be fully zero before native formatter')
            buffers.append(destination)
        if not frames and pc != 0x0201D444:
            raise ValueError('Setup116 native body outside formatter chain')
        if pc == owner[0]:
            frames.append(dict(address=pc, returnAddress=engine.reg_read(UC_ARM_REG_LR) & ~1, sp=engine.reg_read(UC_ARM_REG_SP),
                preserved=[engine.reg_read(r) for r in REGS[4:12]]))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or CONTEXT <= address <= CONTEXT + 0x24 - size or 0x04000000 <= address <= 0x04001000 - size):
            raise ValueError('Setup116 unexpected native write')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=50001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or frames or len(calls) != len(services):
        raise ValueError('Setup116 actual return/SP/call completion differs')
    if actual[0] != 2 or actual[4:12] != registers[4:12] or len(buffers) != 1 or not returned_native:
        raise ValueError('Setup116 physical return/native formatter completion differs')
    ram, mmio = bytes(machine.mem_read(0x02000000, 0x400000)), bytes(machine.mem_read(0x04000000, 0x1000))
    if ram != expected_ram or mmio != expected_mmio:
        raise ValueError('Setup116 full RAM/MMIO model differs')
    return dict(actualReturn=True, registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        instructions=len(visits) - len(calls), pcTrace=visits, writes=writes, providedCalls=calls,
        nativeDependencyActualReturns=returned_native, ramSha256=hashlib.sha256(ram).hexdigest(), mmioSha256=hashlib.sha256(mmio).hexdigest(),
        stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
        observedNativeCallerInstructionBytes=len({pc + i for pc in visits if ENTRY <= pc < ENTRY + 344 for i in range(4)}))
