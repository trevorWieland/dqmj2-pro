import bisect
import hashlib
import random
import re
import struct
from functools import cache

from ov001_ability28_fixture_20261031 import REGS
from ov001_reroll59_models_20261031 import CONTEXT, RNG_STATE, model
from project import ROOT
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x0220C888, 0x08000000, 0x0301FF00
NATIVE = {0x0220B770, 0x0220B74C, 0x0220B794, 0x021DB438, 0x0203D294, 0x02026350}


@cache
def inventory():
    rows = []
    for module, file in [('main', 'config/arm9/symbols.txt'), ('ov001', 'config/arm9/overlays/ov001/symbols.txt')]:
        for mode, size, address in re.findall(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', (ROOT / file).read_text()):
            start = int(address, 0)
            rows.append((start, start + int(size, 0), module, mode))
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
    if any(struct.unpack_from('<I', overlay, address - 0x021D7240)[0] != CONTEXT for address in (0x0220B758, 0x0220B77C, 0x0220B7A0)):
        raise ValueError('Reroll59 actual getter context literals differ')
    pools = struct.unpack_from('<4I', overlay, 0x021DB4A4 - 0x021D7240)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    context = bytearray(rng.randbytes(0x30))
    for offset, key in [(14, 'phase'), (13, 'counter'), (0x1A, 'side'), (0x1B, 'nativeId'), (0x1C, 'slot')]:
        context[offset] = recipe[key]
    machine.mem_write(CONTEXT, bytes(context))
    machine.mem_write(RNG_STATE, struct.pack('<I', recipe['rngWord'] ^ 0xFFFFFFFF if recipe['phase'] == 0 else recipe['rngWord']))
    output, services, rng_after = model(recipe, context, pools)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_ram[CONTEXT - 0x02000000:CONTEXT - 0x02000000 + len(output)] = output
    struct.pack_into('<I', expected_ram, RNG_STATE - 0x02000000, rng_after)
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    starts, ranges = inventory()
    visits, writes, pending, returned, calls, seen = [], [], [], [], [], set()

    def step(engine, pc, size, unused):
        while pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['sp'] or [engine.reg_read(REGS[i]) for i in range(4, 12)] != item['preserved']:
                raise ValueError('Reroll59 actual native stack/preserved registers differ')
            returned.append(dict(address=hex(item['address']), physicalR0=engine.reg_read(REGS[0]), physicalR1=engine.reg_read(REGS[1])))
        if pc == STOP:
            engine.emu_stop()
            return
        if len(visits) >= 5000:
            raise ValueError('Reroll59 instruction bound exceeded')
        visits.append((pc, size))
        if pc in (0x02066A7C, 0x0220C6E0, 0x0220C7EC):
            index = len(calls)
            if index >= len(services) or services[index]['address'] != pc:
                raise ValueError('Reroll59 supplied caller protocol/order differs')
            service = services[index]
            args = [engine.reg_read(REGS[i]) for i in range(len(service['arguments']))]
            if args != service['arguments']:
                raise ValueError(('Reroll59 raw argument words differ', hex(pc), args, service))
            for address, payload in service['writes']:
                engine.mem_write(address, payload)
            calls.append(dict(address=hex(pc), arguments=args, suppliedReturn=service['result']))
            engine.reg_write(REGS[0], service['result'])
            for register in (1, 2, 3, 12):
                engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 17 + register) & 0xFFFFFFFF)
            lr = engine.reg_read(UC_ARM_REG_LR)
            engine.reg_write(UC_ARM_REG_CPSR, engine.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFDF | ((recipe['seed'] + index) & 15) << 28 | (32 if lr & 1 else 0))
            engine.reg_write(UC_ARM_REG_PC, lr)
            return
        index = bisect.bisect_right(starts, pc) - 1
        if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
            raise ValueError(('Reroll59 escaped qualified native inventory', hex(pc)))
        entry = ranges[index]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Reroll59 wrong native mode')
        seen.add(entry)
        if pc in NATIVE:
            if pc == 0x0203D294 and engine.reg_read(REGS[0]) != 100:
                raise ValueError('Reroll59 actual RNG bound differs')
            pending.append(dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR) & ~1, sp=engine.reg_read(UC_ARM_REG_SP),
                preserved=[engine.reg_read(REGS[i]) for i in range(4, 12)]))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or CONTEXT <= address < CONTEXT + 0x30 and size == 1 or address == RNG_STATE and size == 4):
            raise ValueError('Reroll59 unexpected native write')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=5001)
    actual = [machine.reg_read(register) for register in REGS]
    expected_returns = 3 + int(recipe['slot'] != 4) + int(recipe['phase'] == 0) * 2
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or pending or len(returned) != expected_returns or len(calls) != len(services):
        raise ValueError(('Reroll59 actual return/native completion differs', len(returned), expected_returns))
    if actual[0] or actual[4:12] != registers[4:12]:
        raise ValueError('Reroll59 return/preserved registers differ')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram):
        raise ValueError('Reroll59 independent complete RAM/RNG model differs')
    return dict(actualReturn=True, returnWord=0, instructions=len(visits) - len(calls), registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        providedCalls=calls, nativeDependencyActualReturns=returned, rngActualReturns=sum(row['address'] == '0x203d294' for row in returned),
        observedNativeCallerInstructionRanges=[(pc, size) for pc, size in visits if ENTRY <= pc < ENTRY + 356],
        nativeEntries=[[hex(start), end - start, module, mode] for start, end, module, mode in sorted(seen)],
        pcTraceSha256=hashlib.sha256(repr(visits).encode()).hexdigest(), writeTraceSha256=hashlib.sha256(repr(writes).encode()).hexdigest(),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
