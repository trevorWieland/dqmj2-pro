import json
import random
import struct
import sys
from pathlib import Path

import match_overlay_modules as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn import __version__ as unicorn_version
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0,
    UC_ARM_REG_SP, UC_CPU_ARM_946,
)

SOURCE = ROOT / "src/overlays/ov007_20261029_secondary_palette_84c0ecdaf642.c"
WORK = ROOT / "work/ov007-finish/20261029/palette"
REPORT = ROOT / "evidence/matches/ov007-20261029-palette01.json"
ADDRESS, STATE = 0x021D7D7C, 0x021DA9B8
STACK, STOP = 0x03010000, 0x07000000
PAL_SOURCE, MAP_SOURCE, TILE_SOURCE = 0x03000000, 0x03001000, 0x03002000
PAL_CACHE, MAP_CACHE, FLAGS = 0x020FB2E8, 0x020F7AEC, 0x020F6AE6


def execute(main, overlay, code, vector, case):
    palette_bytes, map_bytes, tile_bytes, character_base = case
    randomizer = random.Random(202610290700 + vector)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000),
                          (0x04000000, 0x2000), (0x05000000, 0x1000),
                          (0x06200000, 0x40000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ADDRESS, code)
    source = randomizer.randbytes(0x3000)
    machine.mem_write(PAL_SOURCE, source)
    machine.mem_write(STACK, randomizer.randbytes(0x10000))
    caches = randomizer.randbytes(0x800)
    map_cache = randomizer.randbytes(0x800)
    vram = bytearray(randomizer.randbytes(0x40000))
    palette_vram = bytearray(randomizer.randbytes(0x1000))
    flag = randomizer.getrandbits(16)
    machine.mem_write(PAL_CACHE, caches)
    machine.mem_write(MAP_CACHE, map_cache)
    machine.mem_write(0x06200000, bytes(vram))
    machine.mem_write(0x05000000, bytes(palette_vram))
    machine.mem_write(FLAGS, struct.pack("<H", flag))
    machine.mem_write(0x020DCB44, b"\xff" * 4)
    machine.mem_write(0x0400100C, struct.pack("<H", character_base << 2))
    fields = [randomizer.getrandbits(32), map_bytes, 0, PAL_SOURCE,
              MAP_SOURCE, TILE_SOURCE, tile_bytes, palette_bytes]
    machine.mem_write(STATE, struct.pack("<8I", *fields))
    registers = [randomizer.getrandbits(32) for unused in range(13)]
    machine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
    for index, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    instructions, writes, callees = [], [], set()
    initial_mmio = bytes(machine.mem_read(0x04000000, 0x2000))
    tile_start = 0x06200000 + character_base * 0x4000
    tile_count = (tile_bytes + 3) // 4 * 4

    def step(engine, pc, size, user):
        if not (0x02000000 <= pc < 0x02000000 + len(main)
                or ADDRESS <= pc < ADDRESS + 100):
            raise ValueError("Palette caller escaped its native main/caller executable images")
        instructions.append(pc)
        if pc in (0x0204820C, 0x02048308, 0x02045994, 0x02045490,
                  0x020048A0, 0x0200494C, 0x020048F4, 0x020049A4,
                  0x02008BF8, 0x02008C28, 0x02005038, 0x020041E4, 0x02045600):
            callees.add(pc)

    def written(engine, access, address, size, value, user):
        allowed = [(PAL_CACHE, 512), (MAP_CACHE, 0x800), (FLAGS, 2),
                   (0x05000000, 0x800), (tile_start, tile_count), (STACK, 0x10000)]
        if not any(base <= address and address + size <= base + length for base, length in allowed):
            raise ValueError("Palette caller/native helpers wrote outside expected state")
        writes.append((address, size, value & ((1 << (8 * size)) - 1)))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ADDRESS, STOP, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise ValueError("Palette caller did not actually return within its instruction bound")
    expected_caches = bytearray(caches)
    copied = min(palette_bytes, 512) // 2 * 2
    expected_caches[:copied] = source[:copied]
    expected_caches[:2] = b"\0\0"
    expected_palette = palette_vram[:]
    for offset, cache_offset in [(0, 0x600), (0x200, 0x400), (0x400, 0), (0x600, 0x200)]:
        expected_palette[offset:offset + 512] = expected_caches[cache_offset:cache_offset + 512]
    expected_map = bytearray(map_cache)
    map_count = (map_bytes + 1) // 2 * 2
    expected_map[:map_count] = source[0x1000:0x1000 + map_count]
    vram[character_base * 0x4000:character_base * 0x4000 + tile_count] = source[0x2000:0x2000 + tile_count]
    expected = [(PAL_CACHE, bytes(expected_caches)), (MAP_CACHE, bytes(expected_map)),
                (0x05000000, bytes(expected_palette)), (0x06200000, bytes(vram)),
                (FLAGS, struct.pack("<H", flag | 4)), (PAL_SOURCE, source),
                (STATE, struct.pack("<8I", *fields)), (0x04000000, initial_mmio)]
    for address, data in expected:
        if bytes(machine.mem_read(address, len(data))) != data:
            raise ValueError("Native palette/map/tile effects differ from independent copy model at " + hex(address))
    if machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError("Palette caller did not restore SP")
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError("Palette caller changed preserved registers")
    return {"case": case, "actualReturn": True, "targetInstructions": len(instructions),
            "registers": [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            "cpsr": machine.reg_read(UC_ARM_REG_CPSR), "nativeCalleeEntries": sorted(callees),
            "pcTraceSha256": compiler.sha(json.dumps(instructions).encode()),
            "writeTraceSha256": compiler.sha(json.dumps(writes).encode()),
            "ramSha256": compiler.sha(bytes(machine.mem_read(0x02000000, 0x400000))),
            "scratchStackSha256": compiler.sha(bytes(machine.mem_read(0x03000000, 0x20000))),
            "paletteSha256": compiler.sha(bytes(machine.mem_read(0x05000000, 0x1000))),
            "vramSha256": compiler.sha(bytes(machine.mem_read(0x06200000, 0x40000)))}


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python/Unicorn required")
    metadata, overlay, unused = measured_module("ov007")
    main_metadata, main, unused = measured_module("main")
    compiler.WORK = WORK / "compiler"
    report, code = compiler.compile_compare("ov007", SOURCE, "2", "off")
    if report["returncode"] or len(report["functions"]) != 1:
        raise ValueError("Frozen palette source did not compile as one function")
    entry = report["functions"][0]
    if not entry["exactAfterDeclaredRelocation"]:
        raise ValueError("Frozen palette source no longer matches all104 native bytes")
    entry.update(processor="arm9", sourceLanguage="C")
    bindings = qualified_bindings(entry)
    directory = WORK / "link" / entry["objectSha256"]
    proof = validate(entry, bindings, directory)
    linked = (directory / "caller.bin").read_bytes()
    save_link_snapshots.DIRECTORY = WORK / "link-artifacts"
    entry.update(save_link_snapshots.freeze_link(proof))
    native = overlay[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 104]
    randomizer = random.Random(202610290007)
    cases = [(size, 128, 144, base) for size in (0, 1, 2, 3, 31, 32, 511, 512, 513)
             for base in (0, 3, 15)]
    cases += [(randomizer.randrange(600), randomizer.randrange(513), randomizer.randrange(513),
               randomizer.randrange(16)) for unused in range(64)]
    vectors = []
    for index, case in enumerate(cases):
        original = execute(main, overlay, native, index, case)
        rebuilt = execute(main, overlay, linked, index, case)
        if original != rebuilt:
            raise ValueError("Native/linked C register, memory or trace difference")
        vectors.append(original)
    entry.update(nativeSymbolEntries=bindings, isolatedCallerLink=proof, ordinaryCBytes=104,
                 justifiedAssemblyBytes=0, oracle={"vectors": len(vectors), "executions": len(vectors) * 2,
                    "actualReturnRequired": True, "nativeCalleesExecuted": True,
                    "hostCalleeStubs": False, "instructionBound": 100000, "results": vectors,
                    "supportedContext": "Default DMA channel=-1; CPU copies into mapped palette/VRAM storage",
                    "limitations": ["No physical display, timing or DMA behavior proof",
                                    "MMIO display controls and palette/VRAM are explicit memory models",
                                    "Malformed pointers and alternate SDK/DMA contexts unsupported"]})
    result = {"schemaVersion": 1, "createdUtc": now(), "romSha256": configuration()["romSha256"],
              "processor": "arm9", "module": "ov007", "moduleInputSha256": metadata["sha256"],
              "mainInputSha256": main_metadata["sha256"], "source": str(SOURCE.relative_to(ROOT)),
              "sourceSha256": sha256(SOURCE), "matches": [entry], "compileReport": report,
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "generator": Path(__file__).name, "generatorSha256": sha256(Path(__file__)),
              "nativeSymbols": {item["symbol"]: item["target"] for item in entry["relocations"]}}
    compiler.immutable(WORK / ("match-" + compiler.sha(json.dumps(result, sort_keys=True).encode()) + ".json"),
                       json.dumps(result, indent=2).encode())
    write_json(REPORT, result)
    print(json.dumps({"functions": 1, "bytes": 104, "executions": len(vectors) * 2,
                      "report": str(REPORT.relative_to(ROOT))}))


if __name__ == "__main__":
    run()
