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
ADDRESS, STATE, HANDLE = 0x021DDD60, 0x021E9818, 0x021E708C
STACK, NAME, STOP = 0x03010000, 0x03000000, 0x07100000
PALETTE, COUNTER, TAGS = 0x020FB2E8, 0x020F0F04, 0x020F0F08


def execute(main, overlay, code, record_index, lease_index, counter, kind, vector):
    randomizer = random.Random(20261029071300 + vector)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    mappings = ((BASE, 0x400000), (0x03000000, 0x20000), (0x04000000, 0x2000),
                (0x05000000, 0x1000), (0x06400000, 0x40000), (0x07000000, 0x1000), (STOP, 0x1000))
    for base, length in mappings:
        machine.mem_map(base, length)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ADDRESS, code)
    wanted = b"fixture-cache-context.bin"
    machine.mem_write(NAME, wanted + b"\0")
    caches = bytearray(randomizer.randbytes(STRIDE * 2))
    for bank in range(2):
        for slot in range(8):
            start = bank * STRIDE + slot * 100
            caches[start:start + 100] = bytes(100)
            name = wanted if bank == 0 and slot == record_index else b"fixture-unused-" + bytes([65 + slot])
            caches[start + 24:start + 24 + len(name) + 1] = name + b"\0"
            struct.pack_into("<I", caches, start + 92, randomizer.getrandbits(32) | 1)
        for slot in range(128):
            flags = randomizer.getrandbits(32) | 1
            if bank == 0 and slot == lease_index:
                flags &= ~1
            struct.pack_into("<II", caches, bank * STRIDE + 0x320 + slot * 8,
                             flags, randomizer.getrandbits(32))
    machine.mem_write(CACHE, bytes(caches))
    machine.mem_write(STATE, randomizer.randbytes(88))
    machine.mem_write(HANDLE, bytes([randomizer.getrandbits(8)]))
    machine.mem_write(COUNTER, struct.pack("<H", counter))
    palette_cache = randomizer.randbytes(0x800)
    palette_vram = bytearray(randomizer.randbytes(0x1000))
    machine.mem_write(PALETTE, palette_cache)
    machine.mem_write(0x05000000, bytes(palette_vram))
    machine.mem_write(0x06400000, randomizer.randbytes(0x40000))
    oam = bytearray(randomizer.randbytes(0x1000))
    machine.mem_write(0x07000000, bytes(oam))
    display = randomizer.getrandbits(32)
    machine.mem_write(0x04000000, struct.pack("<I", display))
    machine.mem_write(0x020DCB44, b"\xff" * 4)
    machine.mem_write(STACK, randomizer.randbytes(0x10000))
    registers = [randomizer.getrandbits(32) for unused in range(13)]
    registers[0], registers[1] = NAME, kind
    machine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
    for position, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + position, value)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    expected = bytearray(machine.mem_read(BASE, 0x400000))

    def store(address, data):
        expected[address - BASE:address - BASE + len(data)] = data

    fills = [(0x020F1008, 0x400, 0x00C0), (0x020F1548, 0x400, 0x00C0),
             (0x020F1A88, 0x400, 0x00C0), (0x020F0F08, 0x100, 0xFFFF),
             (0x020F1448, 0x100, 0xFFFF), (0x020F1988, 0x100, 0xFFFF),
             (0x020F1408, 0x40, 0xFFFF), (0x020F1948, 0x40, 0xFFFF), (0x020F1E88, 0x40, 0xFFFF)]
    for address, length, pattern in fills:
        store(address, struct.pack("<H", pattern) * (length // 2))
    store(CACHE + 0x3544, bytes(512))
    store(COUNTER, struct.pack("<H", (counter + 1) & 0xFFFF))
    store(TAGS, struct.pack("<H", counter) * 128)
    store(TAGS + 0x500, struct.pack("<H", counter) * 32)
    context = CACHE + 0x520
    store(context, struct.pack("<I6H", 0, 0, 127, 0, 0, 31, 0))
    store(context + 0x10, struct.pack("<H", counter))
    store(context + 0x14, struct.pack("<I", 1))
    lease = CACHE + 0x320 + lease_index * 8
    record = CACHE + record_index * 100
    flags = struct.unpack_from("<I", expected, lease - BASE)[0]
    store(lease, struct.pack("<II", flags | 1, record))
    store(STATE + 24, struct.pack("<I", lease))
    store(STATE + 84, struct.pack("<I", record))
    store(HANDLE, bytes([record_index]))
    for destination, source in ((0, 0x600), (0x200, 0x400), (0x400, 0), (0x600, 0x200)):
        palette_vram[destination:destination + 512] = palette_cache[source:source + 512]
    oam[:0x400] = bytes(0x400)
    expected_io = struct.pack("<I", display & 0xFFCFFFEF | 0x10) + bytes(0x1FFC)
    trace, writes, calls = [], [], []

    def step(engine, pc, instruction_size, user):
        if not (BASE <= pc < BASE + len(main) or ADDRESS <= pc < ADDRESS + 140):
            raise ValueError("Execution escaped measured executable images: " + hex(pc))
        trace.append(pc)
        if pc in (0x020489F0, 0x0204837C, 0x02036BB8, 0x02036C78,
                  0x02048404, 0x0204854C, 0x02048308, 0x02008BE0, 0x02008C58):
            calls.append({"address": hex(pc), "arguments": [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(4)]})

    def written(engine, access, destination, length, value, user):
        allowed = [(STACK, 0x10000), (STATE, 88), (HANDLE, 1), (lease, 8),
                   (CACHE + 0x3544, 512), (context, 24), (COUNTER, 2),
                   (0x04000000, 4), (0x05000000, 0x800), (0x06400000, 0x40000), (0x07000000, 0x400)]
        allowed += [(address, count) for address, count, pattern in fills]
        if not any(base <= destination and destination + length <= base + count for base, count in allowed):
            raise ValueError("Unexpected native write: " + hex(destination))
        writes.append((destination, length, value & ((1 << (length * 8)) - 1)))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ADDRESS, STOP, count=600000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError("Native fixture did not return with restored SP")
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError("Preserved register changed")
    ram = bytes(machine.mem_read(BASE, 0x400000))
    if ram != expected:
        first = next(i for i, (actual, wanted) in enumerate(zip(ram, expected)) if actual != wanted)
        raise ValueError("Independent RAM initialization model differs: " + hex(BASE + first))
    for base, data in ((0x04000000, expected_io), (0x05000000, bytes(palette_vram)),
                       (0x06400000, bytes(0x40000)), (0x07000000, bytes(oam))):
        if bytes(machine.mem_read(base, len(data))) != data:
            raise ValueError("Independent VRAM/OAM/MMIO model differs: " + hex(base))
    return {"case": {"recordIndex": record_index, "leaseIndex": lease_index,
                     "counter": counter, "kind": kind}, "actualReturn": True,
            "instructions": len(trace), "nativeCalls": calls,
            "registers": [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            "cpsr": machine.reg_read(UC_ARM_REG_CPSR), "ramSha256": compiler.sha(ram),
            "scratchStackSha256": compiler.sha(bytes(machine.mem_read(0x03000000, 0x20000))),
            "pcTraceSha256": compiler.sha(json.dumps(trace).encode()),
            "writeTraceSha256": compiler.sha(json.dumps(writes).encode()),
            "memoryModelPassed": True}
