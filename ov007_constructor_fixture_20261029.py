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
STATE, STACK, STOP, NAME = 0x021DA9DC, 0x03010000, 0x07000000, 0x03000000
OPEN, LEASE = 0x02048404, 0x0204854C
CONSTRUCTORS = (0x021D8AF8, 0x021D9040)
NAMES = (0x021DA8E8, 0x021DA8FC)
SIZES = (200, 248)


def string_at(data, address):
    offset = address - 0x021D7240
    return data[offset:data.index(0, offset)]


def execute(main, overlay, entry, code, case, vector):
    randomizer = random.Random(20261029071000 + vector)
    bank, index, free_slot = case["bank"], case["index"], case.get("freeSlot")
    bank_base = CACHE + bank * STRIDE
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in ((BASE, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(address, size)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    if code is not None:
        machine.mem_write(entry, code)
    caches = bytearray(STRIDE * 2)
    wanted = string_at(overlay, NAMES[bank])
    machine.mem_write(NAME, wanted + b"\0")
    for current_bank in range(2):
        offset = current_bank * STRIDE
        for slot in range(8):
            name = wanted if current_bank == bank and slot == index else b"fixture-unused-" + bytes([65 + slot])
            start = offset + slot * 100
            caches[start + 24:start + 24 + len(name) + 1] = name + b"\0"
            struct.pack_into("<I", caches, start + 92, randomizer.getrandbits(32) | 1)
        for slot in range(128):
            start = offset + 0x320 + slot * 8
            flags = randomizer.getrandbits(32) | 1
            if current_bank == bank and slot == free_slot:
                flags &= ~1
            struct.pack_into("<II", caches, start, flags, randomizer.getrandbits(32))
    machine.mem_write(CACHE, bytes(caches))
    manager = bytearray(randomizer.randbytes(44))
    machine.mem_write(STATE, bytes(manager))
    machine.mem_write(STACK, randomizer.randbytes(0x10000))
    registers = [randomizer.getrandbits(32) for unused in range(13)]
    arguments = [] if entry in CONSTRUCTORS else [bank, NAME, 4, 5] if entry == OPEN else [bank, index & 0xFFFFFFFF]
    for position, argument in enumerate(arguments):
        registers[position] = argument
    machine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
    for position, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + position, value)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    expected_caches = bytearray(caches)
    if entry in CONSTRUCTORS:
        expected_return = 0
        manager[bank] = index if index is not None else 255
        if index is not None:
            struct.pack_into("<I", manager, 0x24 if bank == 0 else 0x14, 0)
            start = bank * STRIDE + index * 100
            expected_caches[start:start + 100] = bytes(100)
    elif entry == OPEN:
        expected_return = index if index is not None else 255
    else:
        expected_return = 0 if free_slot is None else bank_base + 0x320 + free_slot * 8
        if free_slot is not None:
            start = bank * STRIDE + 0x320 + free_slot * 8
            flags = struct.unpack_from("<I", expected_caches, start)[0]
            struct.pack_into("<II", expected_caches, start, flags | 1,
                             (bank_base + (index & 0xFFFFFFFF) * 100) & 0xFFFFFFFF)
    expected_ram = bytearray(machine.mem_read(BASE, 0x400000))
    expected_ram[CACHE - BASE:CACHE - BASE + len(caches)] = expected_caches
    expected_ram[STATE - BASE:STATE - BASE + len(manager)] = manager
    trace, writes, calls = [], [], []

    def step(engine, pc, size, user):
        if not (BASE <= pc < BASE + len(main) or entry in CONSTRUCTORS and entry <= pc < entry + SIZES[bank]):
            raise ValueError("Execution escaped measured executable images: " + hex(pc))
        trace.append(pc)
        if pc in (OPEN, LEASE, 0x020484DC, 0x02048E14, 0x0201D800,
                  0x0201D69C, 0x02008D78, 0x02008C14):
            calls.append({"address": hex(pc), "arguments": [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(4)]})

    def written(engine, access, address, size, value, user):
        allowed = [(STACK, 0x10000)]
        if entry in CONSTRUCTORS:
            allowed.append((STATE, 44))
            if index is not None:
                allowed.append((bank_base + index * 100, 100))
        elif entry == LEASE and free_slot is not None:
            allowed.append((expected_return, 8))
        if not any(start <= address and address + size <= start + length for start, length in allowed):
            raise ValueError("Unexpected native write: " + hex(address))
        writes.append((address, size, value & ((1 << (size * 8)) - 1)))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(entry, STOP, count=30000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError("Native fixture did not return with restored SP")
    if machine.reg_read(UC_ARM_REG_R0) != expected_return:
        raise ValueError("Full-width return differs from independent model")
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError("Preserved register changed")
    ram = bytes(machine.mem_read(BASE, 0x400000))
    if ram != expected_ram:
        first = next(i for i, (actual, expected) in enumerate(zip(ram, expected_ram)) if actual != expected)
        raise ValueError("RAM differs from independent model: " + hex(BASE + first))
    return {"case": case, "entry": hex(entry), "actualReturn": True,
            "r0FullWidth": expected_return, "instructions": len(trace), "nativeCalls": calls,
            "registers": [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            "cpsr": machine.reg_read(UC_ARM_REG_CPSR), "ramSha256": compiler.sha(ram),
            "scratchStackSha256": compiler.sha(bytes(machine.mem_read(0x03000000, 0x20000))),
            "pcTraceSha256": compiler.sha(json.dumps(trace).encode()),
            "writeTraceSha256": compiler.sha(json.dumps(writes).encode())}
