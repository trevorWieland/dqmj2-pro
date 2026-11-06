import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from ov001_sweep110_models_20261031 import CONTEXT, construct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

STOP, SP = 0x08000000, 0x0301FF00
ENTRY = 0x0220C554
NATIVE = {0x0220B770: 16, 0x0220B74C: 16, 0x0220B794: 16, 0x021DB438: 124, 0x021DB8D0: 72}


def execute(main, overlay, recipe, injected=None):
    entry, length = ENTRY, 396
    base, context_size = CONTEXT, 0x30
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if injected is not None:
        if len(injected) != length:
            raise ValueError('Sweep110 injection must preserve396-byte native span')
        machine.mem_write(entry, injected)
    if any(struct.unpack_from('<I', overlay, address - 0x021D7240)[0] != 0x0223E088 for address in (0x0220B758, 0x0220B77C, 0x0220B7A0)):
        raise ValueError('Sweep110 getter context literals differ')
    pools = struct.unpack_from('<4I', overlay, 0x021DB4A4 - 0x021D7240)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    initial, expected, services, native_count = construct(recipe, rng.randbytes(context_size), pools)
    for address, content in initial:
        machine.mem_write(address, content)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    for service in services:
        for address, data in service['writes']:
            expected_ram[address - 0x02000000:address - 0x02000000 + len(data)] = data
    expected_ram[base - 0x02000000:base - 0x02000000 + len(expected)] = expected
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
                raise ValueError('Sweep110 actual native dependency frame differs')
            returned.append(dict(address=hex(frame['address']), physicalR0=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        visits.append(pc)
        if len(visits) > 5000 or engine.reg_read(UC_ARM_REG_CPSR) & 255 != 0x10:
            raise ValueError('Sweep110 bounded ARM user mode differs')
        if pc in NATIVE:
            frames.append(dict(address=pc, returnAddress=engine.reg_read(UC_ARM_REG_LR), sp=engine.reg_read(UC_ARM_REG_SP),
                preserved=[engine.reg_read(r) for r in REGS[4:12]]))
        if entry <= pc < entry + length or any(address <= pc < address + count for address, count in NATIVE.items()):
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError(('Sweep110 provider order differs', hex(pc), index))
        service = services[index]
        arguments = [engine.reg_read(REGS[i]) for i in range(len(service['arguments']))]
        if arguments != service['arguments']:
            raise ValueError(('Sweep110 independent provider arguments differ', index, arguments, service['arguments']))
        calls.append(dict(address=hex(pc), arguments=arguments, suppliedReturn=service['result'],
            writes=[dict(address=hex(address), bytesHex=data.hex()) for address, data in service['writes']]))
        for address, data in service['writes']:
            engine.mem_write(address, data)
        engine.reg_write(REGS[0], service['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 17 + register) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, size, value, unused):
        if not (0x03000000 <= address <= SP - size or base <= address <= base + context_size - size):
            raise ValueError('Sweep110 native write outside context/private stack')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(entry, STOP + 4, count=5001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or frames:
        raise ValueError('Sweep110 actual top return/SP/native frame completion differs')
    if actual[0] != 0 or actual[4:12] != registers[4:12] or len(returned) != native_count or len(calls) != len(services):
        raise ValueError('Sweep110 independent return/native/provider completion differs')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram:
        raise ValueError('Sweep110 independent complete RAM model differs')
    return dict(actualReturn=True, registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        instructions=len(visits) - len(calls), pcTrace=visits, writes=writes, providedCalls=calls,
        nativeDependencyActualReturns=returned, ramSha256=hashlib.sha256(ram).hexdigest(),
        stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
        observedNativeCallerInstructionBytes=len({pc + i for pc in visits if entry <= pc < entry + length for i in range(4)}))
