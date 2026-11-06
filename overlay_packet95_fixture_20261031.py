import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from overlay_packet95_models_20261031 import ACTOR, RECORD, FLAG, model
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

STOP, SP = 0x08000000, 0x0301FF00
SPANS = {'gate': (0x021E9B84, 312), 'dialog': (0x021E979C, 220)}


def execute(kind, main, overlay, recipe, injected=None):
    entry, length = SPANS[kind]
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    if injected is not None:
        if len(injected) != length:
            raise ValueError('Packet95 injection must preserve native span')
        machine.mem_write(entry, injected)
    rng = random.Random(recipe['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(ACTOR, rng.randbytes(0x400))
    machine.mem_write(RECORD, rng.randbytes(32))
    initial, services, final, arguments, result = model(kind, recipe)
    for address, content in initial:
        machine.mem_write(address, content)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    for address, content in [write for service in services for write in service['writes']] + final:
        expected_ram[address - 0x02000000:address - 0x02000000 + len(content)] = content
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    for i, value in enumerate(arguments):
        machine.reg_write(REGS[i], value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, visits, writes = [], [], []

    def step(engine, pc, size, unused):
        if pc == STOP:
            engine.emu_stop()
            return
        visits.append(pc)
        if len(visits) > 2000 or engine.reg_read(UC_ARM_REG_CPSR) & 255 != 0x10:
            raise ValueError('Packet95 bounded ARM user mode differs')
        if entry <= pc < entry + length:
            return
        index = len(calls)
        if index >= len(services) or pc != services[index]['address']:
            raise ValueError(('Packet95 provider order differs', kind, hex(pc), index))
        service = services[index]
        actual = [engine.reg_read(REGS[i]) if i < 4 else struct.unpack('<I', bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_SP) + 4 * (i - 4), 4)))[0]
            for i in range(len(service['arguments']))]
        if actual != service['arguments']:
            raise ValueError(('Packet95 independent provider argument model differs', kind, index, actual, service['arguments']))
        calls.append(dict(address=hex(pc), arguments=actual, suppliedReturn=service['result'],
            writes=[dict(address=hex(address), bytesHex=content.hex()) for address, content in service['writes']]))
        for address, content in service['writes']:
            engine.mem_write(address, content)
        engine.reg_write(REGS[0], service['result'])
        for register in (1, 2, 3, 12):
            engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 17 + register) & 0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, address, size, value, unused):
        stack = 0x03000000 <= address <= SP - size
        flag = kind == 'gate' and address == FLAG and size == 1 and value == 1 and calls and calls[-1]['address'] == '0x220efd0' and result != 0
        if not stack and not flag:
            raise ValueError('Packet95 unexpected native RAM write')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(entry, STOP + 4, count=2001)
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or len(calls) != len(services):
        raise ValueError('Packet95 actual return/SP/provider completion differs')
    if actual[0] != result or actual[4:12] != registers[4:12]:
        raise ValueError('Packet95 physical return/preserved-register model differs')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != expected_ram:
        raise ValueError('Packet95 full RAM/provider write model differs')
    return dict(actualReturn=True, registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        instructions=len(visits) - len(calls), pcTrace=visits, writes=writes, providedCalls=calls,
        nativeDependencyActualReturns=[], ramSha256=hashlib.sha256(ram).hexdigest(),
        stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest(),
        observedNativeCallerInstructionBytes=len({pc + i for pc in visits if entry <= pc < entry + length for i in range(4)}))
