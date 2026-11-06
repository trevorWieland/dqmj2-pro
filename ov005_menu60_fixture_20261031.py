import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from ov005_menu60_models_20261031 import CONTEXT, SELECTION, INPUT, ROWS_A, ROWS_B, ROW_BYTES, model
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021E3560, 0x08000000, 0x0301FF00
NATIVE = {0x021E0A68: 12, 0x021E0A84: 12, 0x021E0A90: 16, 0x0202A634: 12}


def execute(main, overlay, recipe, source_bytes=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for start, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(start, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        machine.mem_write(ENTRY, source_bytes)
    if struct.unpack_from('<I', overlay, 0x021E0A70 - 0x021D7240)[0] != SELECTION or struct.unpack_from('<I', main, 0x2A63C)[0] != INPUT:
        raise ValueError('Menu60 actual selector/input literals differ')
    rng = random.Random(recipe['seed'])
    for address, size in [(0x03000000, 0x20000), (ROWS_A, ROW_BYTES), (ROWS_B, ROW_BYTES), (CONTEXT, 0x50), (INPUT, 8)]:
        machine.mem_write(address, rng.randbytes(size))
    machine.mem_write(SELECTION, struct.pack('<I', recipe['before']))
    machine.mem_write(CONTEXT + 0x40, struct.pack('<I', ROWS_A))
    machine.mem_write(CONTEXT + 0x48, struct.pack('<I', recipe['flag48'] ^ 1))
    machine.mem_write(INPUT + 2, struct.pack('<H', recipe['flags']))
    context, services, effects, return_word, expected_returns = model(recipe, bytes(machine.mem_read(CONTEXT, 0x50)))
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    for address, payload in effects:
        expected_ram[address - 0x02000000:address - 0x02000000 + len(payload)] = payload
    expected_ram[CONTEXT - 0x02000000:CONTEXT - 0x02000000 + len(context)] = context
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    visits, writes, calls, pending, returned = [], [], [], [], []

    def step(engine, pc, size, unused):
        while pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['sp'] or [engine.reg_read(REGS[i]) for i in range(4, 12)] != item['preserved']:
                raise ValueError('Menu60 actual native stack/preserved registers differ')
            returned.append(dict(address=hex(item['address']), physicalR0=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        if len(visits) >= 2000 or engine.reg_read(UC_ARM_REG_CPSR) & 32:
            raise ValueError('Menu60 instruction/mode bound differs')
        visits.append(pc)
        if ENTRY <= pc < ENTRY + 300:
            return
        if pc in NATIVE:
            pending.append(dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR), sp=engine.reg_read(UC_ARM_REG_SP),
                preserved=[engine.reg_read(REGS[i]) for i in range(4, 12)]))
            return
        if any(start < pc < start + size for start, size in NATIVE.items()):
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError(('Menu60 provider/order differs', hex(pc), index))
        service = services[index]
        args = [engine.reg_read(REGS[i]) if i < 4 else struct.unpack('<I', bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_SP) + (i - 4) * 4, 4)))[0] for i in range(len(service['arguments']))]
        if args != service['arguments']:
            raise ValueError(('Menu60 raw argument words differ', hex(pc), args, service))
        for address, payload in service['probes']:
            if bytes(engine.mem_read(address, len(payload))) != payload:
                raise ValueError('Menu60 intermediate narrow store must precede call')
        for address, payload in service['writes']:
            engine.mem_write(address, payload)
        calls.append(dict(address=hex(pc), arguments=args, suppliedReturn=service['result']))
        engine.reg_write(REGS[0], service['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 17 + register) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_CPSR, engine.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF | ((recipe['seed'] + index) & 15) << 28)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or address == CONTEXT + 4 and size == 1 or address == CONTEXT + 0x48 and size == 4):
            raise ValueError('Menu60 unexpected native write')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=2001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or pending or len(calls) != len(services) or len(returned) != expected_returns:
        raise ValueError(('Menu60 actual return/native completion differs', len(returned), expected_returns))
    if actual[0] != return_word or actual[4:12] != registers[4:12]:
        raise ValueError('Menu60 return/preserved registers differ')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram):
        raise ValueError('Menu60 independent complete RAM/reload model differs')
    return dict(actualReturn=True, returnWord=actual[0], instructions=len(visits) - len(calls), registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        providedCalls=calls, nativeDependencyActualReturns=returned, pcTrace=visits, writes=writes,
        observedNativeCallerInstructionBytes=len({pc + i for pc in visits if ENTRY <= pc < ENTRY + 300 for i in range(4)}),
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
