import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from ov001_state46_models_20261031 import CONTEXT, ACTOR_A, ACTOR_B, HEIGHT_OLD, HEIGHT_NEW, GLOBAL_FLAG, model
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021EACB0, 0x08000000, 0x0301FF00


def execute(main, overlay, recipe, source_bytes=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, length in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, length)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        machine.mem_write(ENTRY, source_bytes)
    rng = random.Random(recipe['seed'])
    for address, length in [(CONTEXT, 0xA0), (ACTOR_A, 0x440), (ACTOR_B, 0x440), (0x03000000, 0x20000)]:
        machine.mem_write(address, rng.randbytes(length))
    for address, payload in [(CONTEXT + 16, bytes([recipe['phase']])), (CONTEXT + 0x54, struct.pack('<I', ACTOR_B)),
        (CONTEXT + 0x60, struct.pack('<I', ACTOR_A)), (ACTOR_A + 0x1E4, bytes([recipe['blockedA']])),
        (ACTOR_B + 0x1E4, bytes([recipe['blockedB']])), (ACTOR_A + 0x31E, bytes([recipe['side'], recipe['slot']])),
        (ACTOR_A + 0x60, struct.pack('<I', HEIGHT_OLD)), (HEIGHT_OLD, struct.pack('<i', recipe['height'])),
        (HEIGHT_NEW, b'\xa5' * 4), (CONTEXT + 0x36, struct.pack('<H', recipe['field36'])),
        (CONTEXT + 0x29, bytes([recipe['field29']])), (GLOBAL_FLAG, bytes([recipe['flagBefore']]))]:
        machine.mem_write(address, payload)
    services, effects = model(recipe)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    for address, payload in effects:
        expected_ram[address - 0x02000000:address - 0x02000000 + len(payload)] = payload
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    visits, writes, calls = [], [], []

    def step(engine, pc, size, unused):
        if pc == STOP:
            engine.emu_stop()
            return
        if len(visits) >= 1000:
            raise ValueError('State46 instruction bound exceeded')
        visits.append(pc)
        if engine.reg_read(UC_ARM_REG_CPSR) & 32:
            raise ValueError('State46 caller/provider mode differs')
        if ENTRY <= pc < ENTRY + (340 if source_bytes is None else len(source_bytes)):
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError(('Unexpected state46 service/order', hex(pc), index))
        service = services[index]
        actual = [engine.reg_read(REGS[i]) for i in range(len(service['arguments']))]
        if actual != service['arguments']:
            raise ValueError(('State46 argument words differ', hex(pc), actual, service))
        for address, payload in service['probes']:
            if bytes(engine.mem_read(address, len(payload))) != payload:
                raise ValueError('State46 intermediate source store/order differs')
        for address, payload in service['writes']:
            engine.mem_write(address, payload)
        calls.append(dict(address=hex(pc), arguments=actual, suppliedReturn=service['returnWord']))
        engine.reg_write(REGS[0], service['returnWord'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 17 + register) & 0xFFFFFFFF)
        flags = engine.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF | ((recipe['seed'] + index) & 15) << 28
        engine.reg_write(UC_ARM_REG_CPSR, flags)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, lambda engine, access, address, size, value, unused: writes.append((address, size, value)))
    machine.emu_start(ENTRY, STOP + 4, count=1001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or len(calls) != len(services):
        raise ValueError('State46 actual return/stack/protocol completion differs')
    if actual[0] != 0 or actual[4:12] != registers[4:12]:
        raise ValueError('State46 return/preserved registers differ')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram):
        raise ValueError('State46 complete RAM model differs')
    for address, size, value in writes:
        if not (0x03000000 <= address <= SP - size or address in (CONTEXT + 10, CONTEXT + 16, CONTEXT + 19) and size == 1):
            raise ValueError('State46 unexpected native write')
    return dict(actualReturn=True, returnWord=0, instructions=len(visits) - len(calls), providedCalls=calls,
        nativeDependencyActualReturns=[], registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR), pcTrace=visits, writes=writes,
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
