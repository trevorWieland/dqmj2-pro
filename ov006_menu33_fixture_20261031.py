import hashlib
import random
import re
import struct
from functools import cache

from ov001_ability28_fixture_20261031 import REGS
from ov006_menu33_models_20261031 import CTX, INFO, STATS, ROOT_DATA, KEYS, RAW_STATE, WORD_TABLE, model
from project import ROOT
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021E3064, 0x08000000, 0x0301FF00
NATIVE = {0x0202A634, 0x020417F8, 0x02041800, 0x02067748, 0x020679F0, 0x021DF150, 0x021E2F58, 0x021E3B7C}


@cache
def functions():
    result = {}
    for module, file in [('main', 'config/arm9/symbols.txt'), ('ov006', 'config/arm9/overlays/ov006/symbols.txt')]:
        for mode, size, address in re.findall(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', (ROOT / file).read_text()):
            address = int(address, 0)
            if address in NATIVE:
                result[address] = dict(address=address, mode=mode, bytes=int(size, 0), module=module)
    if set(result) != NATIVE or any(item['mode'] != 'arm' for item in result.values()):
        raise ValueError('Menu33 native entry qualification differs')
    return result


def execute(main, overlay, recipe, source_bytes=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for start, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(start, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        machine.mem_write(ENTRY, source_bytes)
    if struct.unpack_from('<I', main, 0x2A63C)[0] != KEYS or struct.unpack_from('<I', main, 0x679FC)[0] != ROOT_DATA:
        raise ValueError('Menu33 native getter roots differ')
    if struct.unpack_from('<II', main, 0x4180C) != (0x020417F8, RAW_STATE - 2):
        raise ValueError('Menu33 raw-state wrapper target/root differs')
    if struct.unpack_from('<I', overlay, 0x021DF158 - 0x021D7240)[0] != 0x0202A634:
        raise ValueError('Menu33 native key thunk target differs')
    if struct.unpack_from('<I', overlay, 0x021E2F64 - 0x021D7240)[0] != CTX:
        raise ValueError('Menu33 native state-setter root differs')
    rng = random.Random(recipe['seed'])
    for address, length in [(CTX, 0x40), (INFO, 0x40), (STATS, 0x40), (0x03000000, 0x20000)]:
        machine.mem_write(address, rng.randbytes(length))
    machine.mem_write(CTX, struct.pack('<h', recipe['label']))
    machine.mem_write(CTX + 8, struct.pack('<iI', recipe['counter'], recipe['state']))
    machine.mem_write(CTX + 16, struct.pack('<4I', *WORD_TABLE))
    machine.mem_write(INFO + 2, bytes([recipe['flags'], recipe['selector'] & 255]))
    machine.mem_write(STATS + 4, struct.pack('<I', recipe['numeric']))
    machine.mem_write(STATS + 0x2C, struct.pack('<II', 1000, 1 + recipe['numeric'] if recipe['state'] != 11 else 1))
    name_pointer = struct.unpack_from('<I', main, 0x67750)[0]
    machine.mem_write(name_pointer + 4, struct.pack('<I', recipe['index']))
    machine.mem_write(ROOT_DATA + 0x2C, struct.pack('<I', STATS))
    machine.mem_write(KEYS + 2, struct.pack('<H', recipe['keys']))
    machine.mem_write(RAW_STATE, bytes([recipe['rawState']]))
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected, effects, return_word = model(recipe, main, overlay)
    for address, data in effects:
        expected_ram[address - 0x02000000:address - 0x02000000 + len(data)] = data
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    inventory, visits, writes, calls, returned, pending = functions(), [], [], [], [], []

    def step(engine, pc, size, unused):
        while pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['sp'] or engine.reg_read(REGS[0]) != item['service']['returnWord']:
                raise ValueError(('Menu33 actual native return differs', item, hex(pc)))
            returned.append(dict(module=inventory[item['address']]['module'], address=hex(item['address']),
                actualReturn=True, physicalR0=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        if len(visits) >= 2000:
            raise ValueError('Menu33 instruction bound exceeded')
        visits.append(pc)
        if engine.reg_read(UC_ARM_REG_CPSR) & 32:
            raise ValueError('Menu33 caller/dependency mode differs')
        if ENTRY <= pc < ENTRY + (2728 if source_bytes is None else len(source_bytes)):
            return
        if pc not in NATIVE and pending and pending[-1]['address'] <= pc < pending[-1]['address'] + inventory[pending[-1]['address']]['bytes']:
            return
        index = len(calls)
        if index >= len(expected) or pc != expected[index]['address']:
            raise ValueError(('Unexpected menu33 callee/order', hex(pc), index, recipe))
        service, stack = expected[index], engine.reg_read(UC_ARM_REG_SP)
        actual = [engine.reg_read(REGS[i]) if i < 4 else struct.unpack('<I', engine.mem_read(stack + (i - 4) * 4, 4))[0]
            for i in range(len(service['arguments']))]
        if actual != service['arguments']:
            raise ValueError(('Menu33 argument words differ', hex(pc), actual, service))
        calls.append(dict(address=hex(pc), arguments=actual, native=service['native'], expectedReturn=service['returnWord']))
        if service['native']:
            if pc not in inventory:
                raise ValueError('Menu33 unqualified native entry')
            pending.append(dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR), sp=stack, service=service))
            return
        engine.reg_write(REGS[0], service['returnWord'])
        for register in (1, 2, 3, 12):
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
        raise ValueError('Menu33 failed actual return/stack/pending gate')
    if actual[0] != return_word or actual[4:12] != registers[4:12] or len(calls) != len(expected):
        raise ValueError('Menu33 return/preserved registers/protocol count differs')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram):
        raise ValueError('Menu33 complete RAM model differs')
    allowed = [(address, len(data)) for address, data in effects]
    if any(not (0x03000000 <= address <= SP - size or any(start <= address <= start + length - size for start, length in allowed))
        for address, size, value in writes):
        raise ValueError('Menu33 unexpected native memory effect')
    return dict(actualReturn=True, returnWord=actual[0], instructions=len(visits) - sum(not row['native'] for row in calls),
        nativeDependencyActualReturns=returned, providedCalls=[row for row in calls if not row['native']],
        calls=calls, registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR), pcTrace=visits, writes=writes,
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
