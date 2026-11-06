import json
import random
import struct

import match_runtime as compiler
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0,
    UC_ARM_REG_SP, UC_CPU_ARM_946,
)

BASE, CACHE, STRIDE = 0x02000000, 0x020FBAE8, 0x3744
ADDRESS, STACK, STOP = 0x020484DC, 0x03010000, 0x07000000


def execute(main, code, bank, index, length, flags, vector):
    randomizer = random.Random(20261029071400 + vector)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base, size in ((BASE, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(base, size)
    machine.mem_write(BASE, main)
    machine.mem_write(ADDRESS, code)
    caches = bytearray(randomizer.randbytes(STRIDE * 2))
    record = CACHE + bank * STRIDE + index * 100
    offset = bank * STRIDE + index * 100
    caches[offset:offset + 8] = bytes(8)
    name = bytes(randomizer.randrange(65, 91) for unused in range(length)) + b"\0"
    caches[offset + 24:offset + 24 + len(name)] = name
    struct.pack_into("<I", caches, offset + 92, flags)
    machine.mem_write(CACHE, bytes(caches))
    machine.mem_write(STACK, randomizer.randbytes(0x10000))
    registers = [randomizer.getrandbits(32) for unused in range(13)]
    registers[0], registers[1] = bank, index
    machine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
    for position, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + position, value)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    expected = bytearray(machine.mem_read(BASE, 0x400000))
    if flags & 1:
        expected[record - BASE:record - BASE + 100] = bytes(100)
    trace, writes, calls = [], [], []

    def step(engine, pc, size, user):
        if not BASE <= pc < BASE + len(main):
            raise ValueError("SDK close escaped measured main executable image")
        trace.append(pc)
        if pc in (0x0201D69C, 0x02008D78, 0x02048E14, 0x02008C14):
            calls.append({"address": hex(pc), "arguments": [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(4)]})

    def written(engine, access, destination, size, value, user):
        allowed = [(STACK, 0x10000)] + ([(record, 100)] if flags & 1 else [])
        if not any(base <= destination and destination + size <= base + count for base, count in allowed):
            raise ValueError("SDK close wrote outside selected record and stack")
        writes.append((destination, size, value & ((1 << (size * 8)) - 1)))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ADDRESS, STOP, count=20000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError("SDK close did not actually return with restored SP")
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError("SDK close changed preserved registers")
    ram = bytes(machine.mem_read(BASE, 0x400000))
    if ram != expected:
        raise ValueError("SDK close differs from independent active-record clear model")
    if bool(calls) != bool(flags & 1):
        raise ValueError("SDK close helper paths differ from independent validity-bit model")
    return {"case": {"bank": bank, "index": index, "nameLength": length, "flags": flags},
            "actualReturn": True, "instructions": len(trace), "nativeCalls": calls,
            "registers": [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            "cpsr": machine.reg_read(UC_ARM_REG_CPSR), "ramSha256": compiler.sha(ram),
            "scratchStackSha256": compiler.sha(bytes(machine.mem_read(0x03000000, 0x20000))),
            "pcTraceSha256": compiler.sha(json.dumps(trace).encode()),
            "writeTraceSha256": compiler.sha(json.dumps(writes).encode())}
