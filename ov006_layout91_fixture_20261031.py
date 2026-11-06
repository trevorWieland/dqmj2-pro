import hashlib
import random

from ov001_ability28_fixture_20261031 import REGS
from ov006_layout91_models_20261031 import model
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP = 0x021EA660, 0x08000000, 0x0301FF00
NATIVE = {0x02067B08: 52, 0x02067AF4: 20, 0x02044CDC: 56, 0x021EA2AC: 28}


def execute(main, overlay, recipe, injected=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if injected is not None:
        if len(injected) != 240:
            raise ValueError('Layout91 injection must preserve exact240-byte span')
        machine.mem_write(ENTRY, injected)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    initial, services, expected_native = model(recipe)
    for address, data in initial:
        machine.mem_write(address, data)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    for service in services:
        for address, data in service['writes']:
            expected_ram[address - 0x02000000:address - 0x02000000 + len(data)] = data
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    frames, returned, calls, visits, writes = [], [], [], [], []

    def step(engine, pc, size, unused):
        if frames and pc == frames[-1]['returnAddress']:
            frame = frames.pop()
            if engine.reg_read(UC_ARM_REG_SP) != frame['sp'] or [engine.reg_read(r) for r in REGS[4:12]] != frame['preserved']:
                raise ValueError('Layout91 actual native dependency frame differs')
            returned.append(dict(address=hex(frame['address']), result=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        visits.append(pc)
        if len(visits) > 20000 or engine.reg_read(UC_ARM_REG_CPSR) & 255 != 0x10:
            raise ValueError('Layout91 instruction/ARM user-mode bound differs')
        if pc in NATIVE:
            frames.append(dict(address=pc, returnAddress=engine.reg_read(UC_ARM_REG_LR), sp=engine.reg_read(UC_ARM_REG_SP),
                preserved=[engine.reg_read(r) for r in REGS[4:12]]))
        if ENTRY <= pc < ENTRY + 240 or any(address <= pc < address + length for address, length in NATIVE.items()):
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError(('Layout91 provider order differs', hex(pc), index))
        service = services[index]
        arguments = [engine.reg_read(REGS[i]) for i in range(len(service['arguments']))]
        if arguments != service['arguments']:
            raise ValueError(('Layout91 independent UI argument model differs', index, arguments, service['arguments']))
        calls.append(dict(address=hex(pc), arguments=arguments,
            writes=[dict(address=hex(address), bytesHex=data.hex()) for address, data in service['writes']]))
        for address, data in service['writes']:
            engine.mem_write(address, data)
        for register in (0, 1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 17 + register) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, size, value, unused):
        if not 0x03000000 <= address <= SP - size:
            raise ValueError('Layout91 caller/native helpers may only write private stack')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=20001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or frames:
        raise ValueError('Layout91 actual top return/SP/incomplete native call differs')
    if actual[0] != 1 or actual[4:12] != registers[4:12] or len(returned) != expected_native or len(calls) != len(services):
        raise ValueError('Layout91 independent return/native completion model differs')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram:
        raise ValueError('Layout91 full original RAM/provider-write model differs')
    return dict(actualReturn=True, registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        instructions=len(visits) - len(calls), pcTrace=visits, writes=writes, nativeDependencyActualReturns=returned,
        providedCalls=calls, ramSha256=hashlib.sha256(ram).hexdigest(),
        stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
        observedNativeCallerInstructionBytes=len({pc + i for pc in visits if ENTRY <= pc < ENTRY + 240 for i in range(4)}))
