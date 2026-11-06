import hashlib
import random
import struct

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP, ACTOR, RECORD = 0x0220FA6C, 0x08000000, 0x0301FF00, 0x02350000, 0x02360000
RULES = [(0x2A, 10, 2, 0x40), (0x48, 10, 2, 0x2000), (0x7B, 10, 5, 0x8000),
         (0x7C, 10, 5, 0x10000), (0x7D, 10, 5, 0x20000), (0xBC, 10, 5, 0x02000000),
         (0x7E, 10, 5, 0x40000), (0x7F, 100, 25, 0x100000), (0xEC, 100, 25, 0x200000),
         (0xED, 100, 25, 0x400000), (0xBE, 100, 25, 0x04000000), (0xBD, 100, 25, 0x08000000)]
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
        UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
        UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def recipes():
    rows = []
    for index in range(12):
        for level, gate in [(0, 1), (0xFFFFFFFF, 1), (0x80000000, 1), (1, 0), (1, 1), (0x7FFFFFFF, 0xFFFFFFFF)]:
            levels, gates = [0] * 12, [0] * 12
            levels[index], gates[index] = level, gate
            rows.append(dict(seed=0x128000 + len(rows), levels=levels, gates=gates,
                flags=(0, 0xFFFFFFFF, 0x55555555, 0xAAAAAAAA)[len(rows) % 4]))
    rows.append(dict(seed=0x128FFF, levels=[1] * 12, gates=[1] * 12, flags=0))
    rows.append(dict(seed=0x129000, levels=[1] * 12, gates=[0xFFFFFFFF] * 12, flags=0xFFFFFFFF))
    rng = random.Random(0x128128)
    for index in range(64):
        rows.append(dict(seed=0x129100 + index, flags=rng.getrandbits(32),
            levels=[rng.choice([0, 1, 2, 0x7FFFFFFF, 0xFFFFFFFF, 0x80000000]) for unused in range(12)],
            gates=[rng.choice([0, 1, 0x80000000, 0xFFFFFFFF]) for unused in range(12)]))
    return rows


def execute(main, overlay, recipe, source_bytes=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for start, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(start, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        machine.mem_write(ENTRY, source_bytes)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(ACTOR, rng.randbytes(0x440))
    machine.mem_write(ACTOR + 0x1E8, struct.pack('<I', RECORD))
    machine.mem_write(ACTOR + 0x33C, struct.pack('<I', recipe['flags']))
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    services, expected_writes, flags, result = [], [], recipe['flags'], 0
    for index, (identifier, first, second, mask) in enumerate(RULES):
        level, gate = recipe['levels'][index], recipe['gates'][index]
        services.append(dict(address=0x0207B674, arguments=[identifier, RECORD + 0x46], result=level))
        if 0 < level < 0x80000000:
            services.append(dict(address=0x02210AD0, arguments=[ACTOR, first, second], result=gate))
            if gate != 0:
                flags |= mask
                result = 1
                expected_writes.append((ACTOR + 0x33C, 4, flags))
    struct.pack_into('<I', expected_ram, ACTOR - 0x02000000 + 0x33C, flags)
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[0] = ACTOR
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    visits, writes, providers = [], [], []

    def step(engine, pc, size, unused):
        if pc == STOP:
            engine.emu_stop()
            return
        if len(visits) >= 1000:
            raise ValueError('Ability28 instruction bound exceeded')
        visits.append(pc)
        if ENTRY <= pc < ENTRY + (788 if source_bytes is None else len(source_bytes)):
            if engine.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('Ability28 caller mode differs')
            return
        index = len(providers)
        if index >= len(services) or services[index]['address'] != pc:
            raise ValueError(('Unexpected ability28 provider', hex(pc), index))
        service = services[index]
        arguments = [engine.reg_read(REGS[i]) for i in range(len(service['arguments']))]
        if arguments != service['arguments']:
            raise ValueError(('Ability28 argument words differ', arguments, service))
        providers.append(dict(address=hex(pc), arguments=arguments, providedReturn=service['result']))
        engine.reg_write(REGS[0], service['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 0x12345 + register) & 0xFFFFFFFF)
        flags_word = engine.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF | ((recipe['seed'] + index) & 15) << 28
        target = engine.reg_read(UC_ARM_REG_LR)
        engine.reg_write(UC_ARM_REG_CPSR, flags_word & ~32 | (32 if target & 1 else 0))
        engine.reg_write(UC_ARM_REG_PC, target & ~1)

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, lambda engine, access, address, size, value, unused: writes.append((address, size, value)))
    machine.emu_start(ENTRY, STOP + 4, count=1001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP:
        raise ValueError('Ability28 failed actual return/stack gate')
    if actual[0] != result or actual[4:12] != registers[4:12] or len(providers) != len(services):
        raise ValueError('Ability28 return/preserved registers/protocol count differ')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram) or [w for w in writes if 0x02000000 <= w[0] < 0x02400000] != expected_writes:
        raise ValueError('Ability28 complete flag-memory/order model differs')
    return dict(actualReturn=True, returnWord=actual[0], instructions=len(visits) - len(providers),
        providedCalls=providers, nativeDependencyActualReturns=[], registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        ramSha256=hashlib.sha256(ram).hexdigest(), pcTrace=visits, writes=writes,
        stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
