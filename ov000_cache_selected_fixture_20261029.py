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
STACK, STOP, ACTIVE, PALETTE = 0x03010000, 0x07000000, 0x0210297C, 0x020FB2E8


def execute(main, overlay, code, metadata, record_index, lease_index, vector):
    address, size = metadata["address"], metadata["bytes"]
    bank, state = metadata["bank"], metadata["state"]
    randomizer = random.Random(20261029071200 + vector)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base, length in ((BASE, 0x400000), (0x03000000, 0x20000),
                         (0x04000000, 0x2000), (0x05000000, 0x1000), (STOP, 0x1000)):
        machine.mem_map(base, length)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(address, code)
    offset = metadata["name"] - 0x021D7240
    wanted = overlay[offset:overlay.index(0, offset)]
    caches = bytearray(STRIDE * 2)
    for current_bank in range(2):
        offset = current_bank * STRIDE
        for slot in range(8):
            name = wanted if current_bank == bank and slot == record_index else b"fixture-unused-" + bytes([65 + slot])
            start = offset + slot * 100
            caches[start + 24:start + 24 + len(name) + 1] = name + b"\0"
            struct.pack_into("<I", caches, start + 92, randomizer.getrandbits(32) | 1)
        for slot in range(128):
            start = offset + 0x320 + slot * 8
            flags = randomizer.getrandbits(32) | 1
            if current_bank == bank and slot == lease_index:
                flags &= ~1
            struct.pack_into("<II", caches, start, flags, randomizer.getrandbits(32))
    machine.mem_write(CACHE, bytes(caches))
    manager = bytearray(randomizer.randbytes(metadata["stateBytes"]))
    machine.mem_write(state, bytes(manager))
    machine.mem_write(metadata["handle"], bytes([randomizer.getrandbits(8)]))
    machine.mem_write(ACTIVE, struct.pack("<I", randomizer.getrandbits(32)))
    palette_cache = randomizer.randbytes(0x800)
    palette_vram = bytearray(randomizer.randbytes(0x1000))
    machine.mem_write(PALETTE, palette_cache)
    machine.mem_write(0x05000000, bytes(palette_vram))
    machine.mem_write(0x020DCB44, b"\xff" * 4)
    machine.mem_write(STACK, randomizer.randbytes(0x10000))
    registers = [randomizer.getrandbits(32) for unused in range(13)]
    registers[0], registers[1] = metadata["name"], metadata["kind"]
    machine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
    for position, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + position, value)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    record = CACHE + bank * STRIDE + record_index * 100
    lease = CACHE + bank * STRIDE + 0x320 + lease_index * 8
    offset = bank * STRIDE + 0x320 + lease_index * 8
    flags = struct.unpack_from("<I", caches, offset)[0]
    struct.pack_into("<II", caches, offset, flags | 1, record)
    struct.pack_into("<I", manager, metadata["leaseOffset"], lease)
    struct.pack_into("<I", manager, metadata["recordOffset"], record)
    expected_ram = bytearray(machine.mem_read(BASE, 0x400000))
    expected_ram[CACHE - BASE:CACHE - BASE + len(caches)] = caches
    expected_ram[state - BASE:state - BASE + len(manager)] = manager
    expected_ram[metadata["handle"] - BASE] = record_index
    struct.pack_into("<I", expected_ram, ACTIVE - BASE, record)
    if metadata["flushPalette"]:
        for destination, source in ((0, 0x600), (0x200, 0x400), (0x400, 0), (0x600, 0x200)):
            palette_vram[destination:destination + 512] = palette_cache[source:source + 512]
    trace, writes, calls = [], [], []

    def step(engine, pc, instruction_size, user):
        if not (BASE <= pc < BASE + len(main) or address <= pc < address + size):
            raise ValueError("Execution escaped measured executable images: " + hex(pc))
        trace.append(pc)
        if pc in (0x02048404, 0x0204854C, 0x0204B1A0, 0x02048308, 0x02008BF8, 0x02008C28):
            calls.append({"address": hex(pc), "arguments": [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(4)]})

    def written(engine, access, destination, length, value, user):
        allowed = [(STACK, 0x10000), (state, metadata["stateBytes"]),
                   (metadata["handle"], 1), (lease, 8), (ACTIVE, 4)]
        if metadata["flushPalette"]:
            allowed.append((0x05000000, 0x800))
        if not any(base <= destination and destination + length <= base + count for base, count in allowed):
            raise ValueError("Unexpected native write: " + hex(destination))
        writes.append((destination, length, value & ((1 << (length * 8)) - 1)))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(address, STOP, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError("Native fixture did not return with restored SP")
    if machine.reg_read(UC_ARM_REG_R0) != record:
        raise ValueError("Measured final setter register R0 differs from record pointer")
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError("Preserved register changed")
    ram = bytes(machine.mem_read(BASE, 0x400000))
    if ram != expected_ram or bytes(machine.mem_read(0x05000000, 0x1000)) != palette_vram:
        raise ValueError("Native state differs from independent lease/record/palette model")
    if bytes(machine.mem_read(0x04000000, 0x2000)) != bytes(0x2000):
        raise ValueError("Unexpected modeled MMIO change")
    return {"case": {"recordIndex": record_index, "leaseIndex": lease_index, "bank": bank},
            "entry": hex(address), "actualReturn": True, "instructions": len(trace), "nativeCalls": calls,
            "registers": [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            "cpsr": machine.reg_read(UC_ARM_REG_CPSR), "ramSha256": compiler.sha(ram),
            "scratchStackSha256": compiler.sha(bytes(machine.mem_read(0x03000000, 0x20000))),
            "paletteSha256": compiler.sha(bytes(machine.mem_read(0x05000000, 0x1000))),
            "pcTraceSha256": compiler.sha(json.dumps(trace).encode()),
            "writeTraceSha256": compiler.sha(json.dumps(writes).encode())}
