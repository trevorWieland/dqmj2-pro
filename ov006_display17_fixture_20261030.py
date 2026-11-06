import hashlib
import random
import re
import struct
from functools import lru_cache

from ov006_display17_models_20261030 import ROOT_DATA, ROWS, STATE, model
from project import ROOT
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021DB050, 0x08000000, 0x0301FF00
NATIVE = {0x02067748, 0x0206442C, 0x020643FC, 0x020679F0, 0x02067A30}
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
    for start, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(start, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        if len(source_bytes) != 812:
            raise ValueError('Display17 caller span differs')
        machine.mem_write(ENTRY, source_bytes)
    if struct.unpack_from('<I', main, 0x679FC)[0] != ROOT_DATA or struct.unpack_from('<I', main, 0x67A3C)[0] != ROOT_DATA:
        raise ValueError('Display17 two-load getter roots differ')
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(STATE, rng.randbytes(0x40))
    machine.mem_write(ROWS, rng.randbytes(4 * 0x14))
    machine.mem_write(ROOT_DATA + 0x2C, struct.pack('<II', STATE, ROWS))
    for key, value in recipe['fields'].items():
        machine.mem_write(STATE + int(key), struct.pack('<I', value))
    for index, value in enumerate(recipe['rows']):
        machine.mem_write(ROWS + index * 0x14 + 0x10, struct.pack('<I', value))
    identifier_pointer = struct.unpack_from('<I', main, 0x64434)[0]
    machine.mem_write(identifier_pointer, struct.pack('<H', recipe['identifier']))
    expected_ram = bytes(machine.mem_read(0x02000000, 0x400000))
    expected = model(recipe, main)
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    inventory, visits, writes, providers, pending, returned = functions(), [], [], [], [], []
    text_pointer = None

    def step(engine, pc, size, unused):
        nonlocal text_pointer
        if pending and pc == pending[-1]['returnPc']:
            previous = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != previous['sp']:
                raise ValueError('Display17 actual native dependency stack differs')
            returned.append(dict(module='main', address=hex(previous['address']), actualReturn=True,
                                 physicalR0=engine.reg_read(UC_ARM_REG_R0)))
        if pc == STOP:
            engine.emu_stop()
            return
        if len(visits) >= 2000:
            raise ValueError('Display17 instruction bound exceeded')
        visits.append(pc)
        if pc in NATIVE:
            item = inventory[pc]
            if item['mode'] != 'arm' or engine.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('Display17 native dependency mode differs')
            pending.append(dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR), sp=engine.reg_read(UC_ARM_REG_SP)))
            return
        if ENTRY <= pc < ENTRY + 812 or pending and pending[-1]['address'] <= pc < pending[-1]['address'] + inventory[pending[-1]['address']]['bytes']:
            if engine.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('Display17 caller/native mode differs')
            return
        index = len(providers)
        if index >= len(expected) or expected[index]['address'] != pc:
            raise ValueError(('Unexpected display17 provider', hex(pc), index, recipe))
        service, stack = expected[index], engine.reg_read(UC_ARM_REG_SP)
        values = [engine.reg_read(REGS[i]) if i < 4 else struct.unpack('<I', bytes(engine.mem_read(stack + 4 * (i - 4), 4)))[0]
                  for i in range(len(service['arguments']))]
        semantic = []
        for actual, target in zip(values, service['arguments']):
            if isinstance(target, int):
                if actual != target:
                    raise ValueError(('Display17 argument differs', hex(pc), values, service))
                semantic.append(actual)
            elif 'outWords' in target:
                if actual & 1 or actual < stack + 8 or actual + 64 > SP - 16:
                    raise ValueError(('Display17 output buffer escapes locals', hex(actual), hex(stack)))
                text_pointer = actual
                engine.mem_write(actual, struct.pack('<' + 'H' * len(service['words']), *service['words']))
                semantic.append(dict(outputWords=service['words']))
            elif 'textWords' in target:
                words = list(struct.unpack('<' + 'H' * len(target['textWords']), bytes(engine.mem_read(actual, 2 * len(target['textWords'])))))
                if actual != text_pointer or words != target['textWords']:
                    raise ValueError('Display17 formatted output/consumption differs')
                semantic.append(dict(textWords=words))
        result = text_pointer if service['kind'] in ('format', 'number') else service['returnWord']
        providers.append(dict(address=hex(pc), kind=service['kind'], semanticArguments=semantic,
            rawArgumentWords=values, providedReturn=result))
        engine.reg_write(REGS[0], result)
        for register in [1, 2, 3, 12]:
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 0x12345 + register) & 0xFFFFFFFF)
        flags = engine.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF | ((recipe['seed'] + index) & 15) << 28
        target = engine.reg_read(UC_ARM_REG_LR)
        engine.reg_write(UC_ARM_REG_CPSR, flags & ~32 | (32 if target & 1 else 0))
        engine.reg_write(UC_ARM_REG_PC, target & ~1)

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, lambda engine, access, address, size, value, unused: writes.append((address, size, value)))
    machine.emu_start(ENTRY, STOP + 4, count=2001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or pending:
        raise ValueError('Display17 failed actual return/stack/pending gate')
    if actual[0] != recipe['returnWord'] or actual[4:12] != registers[4:12]:
        raise ValueError('Display17 return/preserved registers differ')
    if len(providers) != len(expected) or bytes(machine.mem_read(0x02000000, 0x400000)) != expected_ram:
        raise ValueError('Display17 full protocol/RAM differs')
    for address, size, value in writes:
        if not 0x03000000 <= address <= SP - size:
            raise ValueError(('Display17 unexpected native write', hex(address), size))
    return dict(actualReturn=True, returnWord=actual[0], instructions=len(visits) - len(providers),
        nativeDependencyActualReturns=returned, providedCalls=providers, pcTrace=visits, writes=writes,
        registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        ramSha256=hashlib.sha256(expected_ram).hexdigest(),
        stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
