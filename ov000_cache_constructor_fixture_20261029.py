import json
import random
import struct

import match_overlay_modules as compiler
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0,
    UC_ARM_REG_SP, UC_CPU_ARM_946,
)

BASE, CACHE, STRIDE = 0x02000000, 0x020FBAE8, 0x3744
STACK, STOP = 0x03010000, 0x07000000


def execute(main, overlay, code, metadata, index, vector):
    address, size, state, state_size, bank, name_address, handle_offset, lease_offset = metadata
    bank_base = CACHE + bank * STRIDE
    randomizer = random.Random(20261029071100 + vector)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base, length in ((BASE, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(base, length)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(address, code)
    start = name_address - 0x021D7240
    wanted = overlay[start:overlay.index(0, start)]
    caches = bytearray(STRIDE * 2)
    for current_bank in range(2):
        offset = current_bank * STRIDE
        for slot in range(8):
            name = wanted if current_bank == bank and slot == index else b"fixture-unused-" + bytes([65 + slot])
            start = offset + slot * 100
            caches[start + 24:start + 24 + len(name) + 1] = name + b"\0"
            struct.pack_into("<I", caches, start + 92, randomizer.getrandbits(32) | 1)
        for slot in range(128):
            start = offset + 0x320 + slot * 8
            struct.pack_into("<II", caches, start, randomizer.getrandbits(32) | 1, randomizer.getrandbits(32))
    manager = bytearray(randomizer.randbytes(state_size))
    machine.mem_write(CACHE, bytes(caches))
    machine.mem_write(state, bytes(manager))
    machine.mem_write(STACK, randomizer.randbytes(0x10000))
    registers = [randomizer.getrandbits(32) for unused in range(13)]
    machine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
    for position, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + position, value)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    manager[handle_offset] = index if index is not None else 255
    if index is not None:
        struct.pack_into("<I", manager, lease_offset, 0)
        start = bank * STRIDE + index * 100
        caches[start:start + 100] = bytes(100)
    expected_ram = bytearray(machine.mem_read(BASE, 0x400000))
    expected_ram[CACHE - BASE:CACHE - BASE + len(caches)] = caches
    expected_ram[state - BASE:state - BASE + state_size] = manager
    trace, writes, calls = [], [], []

    def step(engine, pc, instruction_size, user):
        if not (BASE <= pc < BASE + len(main) or address <= pc < address + size):
            raise ValueError("Execution escaped measured executable images: " + hex(pc))
        trace.append(pc)
        if pc in (0x02048404, 0x0204854C, 0x020484DC, 0x02048E14,
                  0x0201D800, 0x0201D69C, 0x02008D78, 0x02008C14):
            calls.append({"address": hex(pc), "arguments": [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(4)]})

    def written(engine, access, destination, length, value, user):
        allowed = [(STACK, 0x10000), (state, state_size)]
        if index is not None:
            allowed.append((bank_base + index * 100, 100))
        if not any(base <= destination and destination + length <= base + count for base, count in allowed):
            raise ValueError("Unexpected native write: " + hex(destination))
        writes.append((destination, length, value & ((1 << (length * 8)) - 1)))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(address, STOP, count=30000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError("Native fixture did not return with restored SP")
    if machine.reg_read(UC_ARM_REG_R0) != 0:
        raise ValueError("Failure path must return full-word0")
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError("Preserved register changed")
    ram = bytes(machine.mem_read(BASE, 0x400000))
    if ram != expected_ram:
        first = next(i for i, (actual, expected) in enumerate(zip(ram, expected_ram)) if actual != expected)
        raise ValueError("RAM differs from independent model: " + hex(BASE + first))
    return {"case": {"index": index, "bank": bank}, "entry": hex(address), "actualReturn": True,
            "r0FullWidth": 0, "instructions": len(trace), "nativeCalls": calls,
            "registers": [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            "cpsr": machine.reg_read(UC_ARM_REG_CPSR), "ramSha256": compiler.sha(ram),
            "scratchStackSha256": compiler.sha(bytes(machine.mem_read(0x03000000, 0x20000))),
            "pcTraceSha256": compiler.sha(json.dumps(trace).encode()),
            "writeTraceSha256": compiler.sha(json.dumps(writes).encode())}
