import bisect
import hashlib
import random
import re
import struct
from functools import cache

from ov001_ability28_fixture_20261031 import REGS
from ov005_initializer47_models_20261031 import BUFFER, LENGTH, GLOBALS, TEMPLATE, model
from project import ROOT
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021D8EDC, 0x08000000, 0x0301FF00
NATIVE = {0x02007FE0, 0x02007FF4, 0x02008008, 0x02008C14, 0x02008C28, 0x021D731C, 0x021D86F0, 0x021D87B4, 0x021D90F0}


@cache
def inventory():
    result = []
    for module, file in [('main', 'config/arm9/symbols.txt'), ('ov005', 'config/arm9/overlays/ov005/symbols.txt')]:
        for mode, size, address in re.findall(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', (ROOT / file).read_text()):
            start = int(address, 0)
            result.append((start, start + int(size, 0), module, mode))
    result.sort()
    return [item[0] for item in result], result


def execute(main, overlay, recipe, source_bytes=None, misalign=False):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x02410000, 0x2000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        machine.mem_write(ENTRY, source_bytes)
    rng = random.Random(recipe['seed'])
    for address, size in [(BUFFER, LENGTH + 32), (GLOBALS, 16), (0x03000000, 0x20000)]:
        machine.mem_write(address, rng.randbytes(size))
    machine.mem_write(GLOBALS + 12, struct.pack('<I', recipe['state']))
    expected_buffer, expected_globals, services = model(recipe, bytes(machine.mem_read(BUFFER, LENGTH)),
        bytes(machine.mem_read(GLOBALS, 16)), bytes(machine.mem_read(TEMPLATE, 64)))
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_ram[BUFFER - 0x02000000:BUFFER - 0x02000000 + LENGTH] = expected_buffer
    expected_ram[GLOBALS - 0x02000000:GLOBALS - 0x02000000 + 16] = expected_globals
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[:3] = [BUFFER + int(misalign), recipe['callback'], recipe['owner']]
    initial_cpsr = rng.getrandbits(4) << 28 | 0x1F | recipe['irq'] | recipe['fiq']
    machine.reg_write(UC_ARM_REG_CPSR, initial_cpsr)
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    starts, ranges = inventory()
    pending, returned, provided, seen, observed = [], [], [], set(), set()
    counts, trace, writes = dict(instructions=0, writes=0), hashlib.sha256(), hashlib.sha256()

    def step(engine, pc, size, unused):
        while pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['sp'] or [engine.reg_read(REGS[i]) for i in range(4, 12)] != item['preserved']:
                raise ValueError('Initializer47 native dependency return/stack/preserved registers differ')
            returned.append(dict(address=hex(item['address']), physicalR0=engine.reg_read(REGS[0]), cpsr=engine.reg_read(UC_ARM_REG_CPSR)))
        if pc == STOP:
            engine.emu_stop()
            return
        if pc == 0x02008430:
            raise ValueError('Initializer47 unsupported unaligned-buffer assertion reached')
        if counts['instructions'] >= 100000:
            raise ValueError('Initializer47 instruction bound exceeded')
        counts['instructions'] += 1
        trace.update(struct.pack('<I', pc))
        if ENTRY <= pc < ENTRY + 276:
            observed.update(range(pc, pc + 4))
        if pc in (0x02007A9C, 0x020125BC, recipe['callback'] & ~1) and pc:
            index = len(provided)
            if index >= len(services) or services[index]['address'] != pc:
                raise ValueError(('Initializer47 provider order differs', hex(pc), index))
            service = services[index]
            cpsr = engine.reg_read(UC_ARM_REG_CPSR)
            if cpsr & 0xDF != 0x1F | service['irq'] | recipe['fiq']:
                raise ValueError(('Initializer47 provider virtual IRQ/control differs', hex(pc), hex(cpsr)))
            mode = 'thumb' if cpsr & 32 else 'arm'
            if mode != service.get('mode', 'arm'):
                raise ValueError('Initializer47 callback mode differs')
            arguments = [engine.reg_read(REGS[i]) for i in range(len(service.get('arguments', [])))]
            if arguments != service.get('arguments', []):
                raise ValueError('Initializer47 callback argument words differ')
            if pc == recipe['callback'] & ~1:
                if bytes(engine.mem_read(GLOBALS + 12, 4)) != struct.pack('<I', 2):
                    raise ValueError('Initializer47 state2 must be stored before callback')
                if bytes(engine.mem_read(BUFFER, LENGTH - 8)) != bytes(expected_buffer[:-8]):
                    raise ValueError('Initializer47 buffer must be constructed before callback')
                engine.mem_write(GLOBALS + 12, struct.pack('<I', recipe['callbackState']))
                engine.mem_write(BUFFER + LENGTH - 8, struct.pack('<II', *recipe['callbackMarker']))
            provided.append(dict(address=hex(pc), mode=mode, arguments=arguments, suppliedReturnWords=service['returnWords'], cpsr=cpsr))
            for register in (0, 1, 2, 3, 12):
                engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 17 + register) & 0xFFFFFFFF)
            for i, value in enumerate(service['returnWords']):
                engine.reg_write(REGS[i], value)
            lr = engine.reg_read(UC_ARM_REG_LR)
            engine.reg_write(UC_ARM_REG_CPSR, cpsr & 0x0FFFFFDF | ((recipe['seed'] + index) & 15) << 28 | (32 if lr & 1 else 0))
            engine.reg_write(UC_ARM_REG_PC, lr & ~1)
            return
        index = bisect.bisect_right(starts, pc) - 1
        if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
            raise ValueError(('Initializer47 escaped native inventory', hex(pc)))
        entry = ranges[index]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Initializer47 wrong native instruction mode')
        seen.add(entry)
        if pc in NATIVE:
            pending.append(dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR), sp=engine.reg_read(UC_ARM_REG_SP),
                preserved=[engine.reg_read(REGS[i]) for i in range(4, 12)]))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or BUFFER <= address <= BUFFER + LENGTH - size or GLOBALS <= address <= GLOBALS + 16 - size):
            raise ValueError(('Initializer47 unexpected native write', hex(address), size))
        counts['writes'] += 1
        writes.update(struct.pack('<IIQ', address, size, value & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    try:
        machine.emu_start(ENTRY, STOP + 4, count=100001)
    except Exception as error:
        if isinstance(error, ValueError):
            raise
        raise ValueError(dict(nativeFaultPc=hex(machine.reg_read(UC_ARM_REG_PC)), instructions=counts['instructions'])) from error
    actual = [machine.reg_read(register) for register in REGS]
    expected_native = 3 if recipe['state'] else 14
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or pending or len(returned) != expected_native or len(provided) != len(services):
        raise ValueError(('Initializer47 actual return/native stack/call completion differs', len(returned), expected_native, pending))
    if actual[4:12] != registers[4:12] or actual[0] != 0x80 or machine.reg_read(UC_ARM_REG_CPSR) & 0xFF != initial_cpsr & 0xFF:
        raise ValueError('Initializer47 final preserved registers/raw IRQ return/control differs')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram):
        offset = next(i for i, pair in enumerate(zip(ram, expected_ram)) if pair[0] != pair[1])
        raise ValueError(('Initializer47 complete independent RAM model differs', hex(offset + 0x02000000), ram[offset:offset + 8].hex(), expected_ram[offset:offset + 8].hex()))
    return dict(actualReturn=True, returnWord=actual[0], **counts, registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        providedCalls=provided, nativeDependencyActualReturns=returned,
        nativeEntries=[[hex(start), end - start, module, mode] for start, end, module, mode in sorted(seen)],
        observedNativeCallerInstructionBytes=len(observed), pcTraceSha256=trace.hexdigest(), writeTraceSha256=writes.hexdigest(),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
