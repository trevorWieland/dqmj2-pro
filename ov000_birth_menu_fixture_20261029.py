import bisect
import json
import random
import struct

import match_runtime
from link_runtime_unit import measured_module
from project import ROOT, sha256
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0,
    UC_ARM_REG_SP, UC_CPU_ARM_946,
)

ENTRY = 0x02227F94
STOP, STACK = 0x027FF800, 0x027FF000
OUTPUT = 0x02600000
RNG = 0x020F6044
STOCK = 0x021BD674
FILES = [
    ("CombinationNotRankTbl.bin", 0x02500000, 8, False),
    ("Combination4GTbl.bin", 0x02510000, 12, False),
    ("CombinationKindTbl.bin", 0x02520000, 16, False),
    ("CombinationKindTypeTbl.bin", 0x02530000, 20, False),
    ("EnmyKindTbl.bin", 0x02540000, 0x020F69F0, True),
    ("ItemTbl.bin", 0x02550000, 0x021C2AB4, True),
]


def read32(machine, address):
    return struct.unpack("<I", machine.mem_read(address, 4))[0]


def parent(species, variant, item, identity):
    data = bytearray(0x84)
    struct.pack_into("<Ih", data, 0x14, identity, species)
    data[0x1A] = variant
    data[0x1B] = identity - 1
    data[0x30] = 10
    data[0x31] = item
    return bytes(data)


class Resources:
    def __init__(self):
        self.main_meta, self.main, unused = measured_module("main")
        self.overlay_meta, self.overlay, unused = measured_module("ov000")
        self.resources = []
        self.hashes = {}
        for name, address, pointer, skip in FILES:
            path = ROOT / "extract/files" / name
            raw = path.read_bytes()
            self.hashes[str(path.relative_to(ROOT))] = sha256(path)
            self.resources.append((address, pointer, skip, raw[8:] if skip else raw))
        self.context = struct.unpack_from("<I", self.overlay, 0x02229FAC - 0x021D7240)[0]

    def execute(self, code, case, serial):
        left, right, tier, selected = case
        randomizer = random.Random(202610290900 + serial)
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.ctl_set_cpu_model(UC_CPU_ARM_946)
        machine.mem_map(0x02000000, 0x00800000)
        machine.mem_write(0x02000000, self.main)
        machine.mem_write(0x021D7240, self.overlay)
        machine.mem_write(ENTRY, code)
        for address, pointer, absolute, data in self.resources:
            machine.mem_write(address, data)
            machine.mem_write(pointer if absolute else self.context + pointer,
                              struct.pack("<I", address))
        machine.mem_write(STOCK, parent(*left, 1) + parent(*right, 2))
        machine.mem_write(RNG, struct.pack("<I", 0x13579BDF))
        machine.mem_write(STACK - 0x7000, randomizer.randbytes(0x7000))
        machine.mem_write(OUTPUT, bytes([0xA5]) * 16)
        registers = [randomizer.getrandbits(32) for unused in range(13)]
        registers[:4] = [1, 2, tier, selected]
        for index, value in enumerate(registers):
            machine.reg_write(UC_ARM_REG_R0 + index, value)
        machine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
        machine.reg_write(UC_ARM_REG_SP, STACK)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.mem_write(STACK, struct.pack("<III", OUTPUT, OUTPUT + 4, OUTPUT + 8))
        delegates, writes, pending = [], [], None
        executed = set()
        instructions = 0

        def step(engine, pc, size, user):
            nonlocal pending, instructions
            instructions += 1
            if not (0x02000000 <= pc < 0x02000000 + len(self.main)
                    or 0x021D7240 <= pc < 0x021D7240 + len(self.overlay)):
                raise ValueError("Native menu escaped measured initialized executable images")
            if pc == 0x0203D294:
                raise ValueError("This native menu fixture unexpectedly consumed RNG")
            executed.add(pc)
            if pc == 0x022280FC:
                if pending is not None:
                    raise ValueError("Native delegate calls unexpectedly nested")
                sp = engine.reg_read(UC_ARM_REG_SP)
                pending = {
                    "arguments": [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(4)],
                    "pointers": [read32(engine, sp + i * 4) for i in range(3)],
                    "return": engine.reg_read(UC_ARM_REG_LR),
                }
            elif pending is not None and pc == pending["return"]:
                pointers = pending["pointers"]
                delegates.append({
                    "arguments": pending["arguments"],
                    "species": engine.reg_read(UC_ARM_REG_R0),
                    "rule": engine.mem_read(pointers[0], 1)[0],
                    "bonus": engine.mem_read(pointers[1], 1)[0],
                    "variant": read32(engine, pointers[2]),
                })
                pending = None

        def written(engine, access, address, size, value, user):
            if not (STACK - 0x7000 <= address and address + size <= STACK + 12
                    or OUTPUT <= address and address + size <= OUTPUT + 16):
                raise ValueError("Native menu wrote outside private stack/output fields")
            writes.append((address, size))

        machine.hook_add(UC_HOOK_CODE, step)
        machine.hook_add(UC_HOOK_MEM_WRITE, written)
        machine.emu_start(ENTRY, STOP, count=250000)
        if machine.reg_read(UC_ARM_REG_PC) != STOP or pending is not None:
            raise ValueError("Native menu did not actually return with completed delegates")
        if machine.reg_read(UC_ARM_REG_SP) != STACK:
            raise ValueError("Native menu did not restore caller stack")
        if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
            raise ValueError("Native menu changed a preserved register")
        if read32(machine, RNG) != 0x13579BDF:
            raise ValueError("Native menu changed RNG state")
        if len(delegates) != 3:
            raise ValueError("Native menu did not evaluate three candidate delegates")
        expected = model(delegates, selected)
        actual = [machine.reg_read(UC_ARM_REG_R0), machine.mem_read(OUTPUT, 1)[0],
                  machine.mem_read(OUTPUT + 4, 1)[0], read32(machine, OUTPUT + 8)]
        if actual != expected:
            raise ValueError({"actual": actual, "expected": expected, "delegates": delegates})
        return {"case": case, "result": actual, "delegates": delegates,
                "instructions": instructions, "executedPcCount": len(executed),
                "executedPcSha256": match_runtime.sha(json.dumps(sorted(executed)).encode()),
                "actualReturn": True, "rngStateUnchanged": True,
                "preservedRegisters": True, "writes": len(writes)}


def model(delegates, selected):
    species = [0xFFFFFFFF] * 3
    variants = [0xFFFFFFFF] * 3
    bonuses = [0xA5] * 3
    count, rule = 0, 11
    for slot, candidate in enumerate(delegates):
        if candidate["arguments"][3] != slot:
            raise ValueError("Native candidate delegate order changed")
        bonuses[slot] = candidate["bonus"]
        variants[count] = candidate["variant"]
        duplicate = -1
        value = candidate["species"]
        if value != 0xFFFFFFFF:
            for earlier in range(slot):
                if species[earlier] == value and variants[earlier] == variants[slot]:
                    duplicate = earlier
            if duplicate == -1:
                species[count] = value
                count += 1
            elif bonuses[count] > bonuses[duplicate]:
                bonuses[duplicate] = bonuses[count]
        if count - 1 == selected and value != 0xFFFFFFFF:
            rule = candidate["rule"]
    value = species[selected] & 0xFFFF
    if value & 0x8000:
        value -= 0x10000
    return [value & 0xFFFFFFFF, rule, bonuses[selected], variants[selected]]
