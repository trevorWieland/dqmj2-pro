import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from ov001_state58_models_20261031 import CONTEXT, RAW_STATE, model
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021F98E4, 0x08000000, 0x0301FF00
NATIVE = {0x02041800: 20, 0x020417F8: 8}


def execute(main, overlay, recipe, source_bytes=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        machine.mem_write(ENTRY, source_bytes)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    context = bytearray(rng.randbytes(32))
    for offset, key in [(0x19, 'phase19'), (0xB, 'phaseB'), (9, 'phase9'), (2, 'phase2'), (0x13, 'counter13'), (8, 'counter8')]:
        context[offset] = recipe[key]
    machine.mem_write(CONTEXT, bytes(context))
    output, services, native, effects = model(recipe, context)
    before_state = recipe['rawState'] ^ 255 if effects else recipe['rawState']
    machine.mem_write(RAW_STATE, bytes([before_state]))
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_ram[CONTEXT - 0x02000000:CONTEXT - 0x02000000 + 32] = output
    for address, payload in effects:
        expected_ram[address - 0x02000000:address - 0x02000000 + len(payload)] = payload
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
            if engine.reg_read(UC_ARM_REG_SP) != item['sp'] or engine.reg_read(REGS[0]) != recipe['rawState']:
                raise ValueError('State58 actual native raw-byte return/stack differs')
            returned.append(dict(address=hex(item['address']), physicalR0=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        if len(visits) >= 2000 or engine.reg_read(UC_ARM_REG_CPSR) & 32:
            raise ValueError('State58 instruction/mode bound exceeded')
        visits.append(pc)
        if ENTRY <= pc < ENTRY + 484:
            return
        if pc in NATIVE:
            pending.append(dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR), sp=engine.reg_read(UC_ARM_REG_SP)))
            return
        if any(address < pc < address + size for address, size in NATIVE.items()):
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError(('State58 provider/order differs', hex(pc), index))
        service = services[index]
        args = [engine.reg_read(REGS[i]) for i in range(len(service['arguments']))]
        if args != service['arguments']:
            raise ValueError(('State58 raw arguments/unsigned pack differ', hex(pc), args, service))
        for address, payload in service['writes']:
            engine.mem_write(address, payload)
        calls.append(dict(address=hex(pc), arguments=args, suppliedReturn=service['result']))
        engine.reg_write(REGS[0], service['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 17 + register) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_CPSR, engine.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF | ((recipe['seed'] + index) & 15) << 28)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or CONTEXT <= address < CONTEXT + 32 and size == 1):
            raise ValueError('State58 unexpected native write')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=2001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or pending or len(calls) != len(services) or len(returned) != int(native) * 2:
        raise ValueError('State58 actual return/stack/native completion differs')
    if actual[0] != 0 or actual[4:12] != registers[4:12]:
        raise ValueError('State58 raw return/preserved registers differ')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram):
        raise ValueError('State58 complete independent RAM model differs')
    return dict(actualReturn=True, returnWord=actual[0], instructions=len(visits) - len(calls), registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        providedCalls=calls, nativeDependencyActualReturns=returned, observedNativeCallerInstructionBytes=len({pc + i for pc in visits if ENTRY <= pc < ENTRY + 484 for i in range(4)}),
        pcTrace=visits, writes=writes, ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
