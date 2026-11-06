import hashlib
import json
import os
import random
import struct
from pathlib import Path
import reuse_overlay_c as reuse
from overlay_oracle005_registry import machine, REGS
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R12,
    UC_ARM_REG_SP,
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_CPSR,
)

ROOT = Path(__file__).resolve().parent
ADDRESS = 0x021DBD24
STATE = 0x021E9818
RECORDS = 0x021EA298
VRAM = 0x06000000
PATHS = [0x021E72B0, 0x021E72C4, 0x021E72D8]
SDK = {
    0x02002C98: "init",
    0x02008C58: "clear",
    0x0201D444: "string",
    0x0203CC2C: "load",
    0x020481B8: "import-first",
    0x0202A8E0: "size",
    0x02048308: "sync",
    0x0202A498: "free",
    0x02004E58: "import-second",
    0x02004B58: "import-third",
    0x021DA824: "reset",
    0x021DDD60: "palette",
    0x021DA838: "widget",
    0x02048A9C: "mode",
    0x02048A94: "enable",
    0x02048A60: "position",
    0x02048644: "clip",
    0x021DBB80: "finish",
    0x021DECBC: "publish",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(code, vector):
    engine = machine({ADDRESS: code}) if code is not None else machine()
    engine.mem_map(VRAM, 0x80000)
    rng = random.Random(202610280712 + vector)
    engine.mem_write(VRAM, rng.randbytes(0x80000))
    state = bytearray(rng.randbytes(112))
    records = bytearray(rng.randbytes(3 * 144))
    gpu = bytearray(rng.randbytes(64))
    engine.mem_write(STATE, bytes(state))
    engine.mem_write(RECORDS, bytes(records))
    engine.mem_write(0x04000000, bytes(gpu))
    engine.mem_write(0x0301FF00, rng.randbytes(256))
    registers = [rng.getrandbits(32) for unused in range(13)] + [0x0301FFF0, 0x04000000]
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for register, value in zip(REGS, registers):
        engine.reg_write(register, value)
    counters = {"string": 0, "load": 0, "position": 0}
    descriptor = None
    descriptorBytes = None
    sizes = [[0, 1], [0x400, 0x800], [65535, 0x80000000], [0xFFFFFFFF, 2]][vector % 4]
    heights = [0, 128, 0x80000000, 0xFFFFFFFF]
    calls = []
    writes = []
    engine.hook_add(
        UC_HOOK_MEM_WRITE,
        lambda uc, access, at, width, value, user: writes.append([at, width, value & ((1 << (width * 8)) - 1)]),
    )

    def step(uc, pc, width, user):
        nonlocal descriptor, descriptorBytes
        if pc not in SDK:
            return
        kind = SDK[pc]
        args = [uc.reg_read(r) for r in [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3]]
        calls.append({"kind": kind, "args": args})
        result = 0
        if kind == "init":
            if args[:3] != [1, 0, 0]:
                raise ValueError("Scene display initialization arguments differ")
            word = struct.unpack_from("<I", gpu, 0)[0] ^ 0x12345678
            uc.mem_write(0x04000000, struct.pack("<I", word))
            struct.pack_into("<I", gpu, 0, word)
        elif kind == "clear":
            if args[0] != 0 or [args[1], args[2]] not in [[VRAM, 0x80000], *[[RECORDS + i * 144, 4] for i in range(3)]]:
                raise ValueError("Scene exact VRAM/record clear range differs")
            uc.mem_write(args[1], bytes(args[2]))
        elif kind == "string":
            index = counters["string"]
            if index >= 3 or args[1] != PATHS[index]:
                raise ValueError("Scene resource path order differs")
            if descriptor is None:
                descriptor = args[0]
            if args[0] != descriptor:
                raise ValueError("Scene temporary descriptor storage identity differs")
            descriptorBytes = struct.pack("<8I", index, vector, PATHS[index], 0xAA, 0xBB, 0xCC, 0xDD, 0xEE)
            uc.mem_write(descriptor, descriptorBytes)
            counters["string"] += 1
        elif kind == "load":
            index = counters["load"]
            if args[:2] != [descriptor, 2] or bytes(uc.mem_read(descriptor, 32)) != descriptorBytes:
                raise ValueError("Scene full stack descriptor/heap contract differs")
            counters["load"] += 1
            result = 0x03008000 + index * 256
            descriptorBytes = bytes([index + 0x31]) * 32
            uc.mem_write(descriptor, descriptorBytes)
        elif kind == "size":
            index = counters["load"] - 1
            if args[0] != descriptor or bytes(uc.mem_read(descriptor, 32)) != descriptorBytes or index not in [0, 1]:
                raise ValueError("Scene resource-size descriptor reuses stale/other storage")
            result = sizes[index]
        elif kind in ["import-first", "import-second"]:
            index = 0 if kind == "import-first" else 1
            if args[:3] != [0x03008000 + index * 256, 0, sizes[index]]:
                raise ValueError("Scene saved resource handle/size call result differs")
        elif kind == "import-third":
            if args[0] != 0x03008200 or args[1] not in [0, 1024] or args[2] != 1024:
                raise ValueError("Scene two resource-half transfers differ")
        elif kind == "free":
            if args[:2] != [2, 0x03008000 + (counters["load"] - 1) * 256]:
                raise ValueError("Scene exact loaded resource handle ownership differs")
        elif kind == "reset":
            if (
                struct.unpack_from("<i", bytes(uc.mem_read(STATE, 112)), 88)[0] != 1
                or struct.unpack_from("<i", bytes(uc.mem_read(STATE, 112)), 76)[0] != 0
            ):
                raise ValueError("Scene full-width area/count stores not visible before reset")
            uc.mem_write(STATE + 84, struct.pack("<I", heights[vector % 4]))
        elif kind == "palette":
            if args[:2] != [0x021E72F0, 4]:
                raise ValueError("Scene palette resource identity differs")
        elif kind in ["widget", "mode", "enable", "position", "clip"]:
            row = (args[0] - RECORDS) // 144
            if row not in range(3) or args[0] != RECORDS + row * 144:
                raise ValueError("Scene three record stride/identity differs")
            if kind == "widget":
                if bytes(uc.mem_read(args[0], 4)) != bytes(4):
                    raise ValueError("Scene record not cleared before widget callback")
                uc.mem_write(args[0] + 16, struct.pack("<I", 0x12340000 + vector + row))
            elif kind == "mode":
                if args[1] != 2:
                    raise ValueError("Scene widget mode differs")
                uc.mem_write(args[0] + 20, struct.pack("<I", 2))
            elif kind == "enable":
                if args[1] != 1:
                    raise ValueError("Scene widget enable flag differs")
                uc.mem_write(args[0] + 24, struct.pack("<I", 1))
            elif kind == "position":
                if args[1:3] != [128, row * 64]:
                    raise ValueError("Scene row coordinate accumulation differs")
                uc.mem_write(args[0] + 28, struct.pack("<2I", 128, row * 64))
                uc.mem_write(STATE + 84, struct.pack("<I", heights[(vector + row + 1) % 4]))
            else:
                height = heights[(vector + row + 1) % 4]
                if args[1:3] != [height, 112]:
                    raise ValueError("Scene callback-mutated clip height not reloaded")
                uc.mem_write(args[0] + 36, struct.pack("<2I", height, 112))
                uc.mem_write(args[0] + 124, struct.pack("<I", [0, 2, 0x80000000, 0xFFFFFFFF][(vector + row) % 4]))
        elif kind == "finish":
            if bytes(uc.mem_read(STATE + 7, 1)) != bytes(1):
                raise ValueError("Scene final state byte not cleared before finalizer")
        elif kind == "publish":
            result = 0x55000000 + vector
        uc.reg_write(UC_ARM_REG_R0, result)
        for i, register in enumerate([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]):
            uc.reg_write(register, (0x9E3779B9 * (i + 1) + vector) & 0xFFFFFFFF)
        uc.reg_write(UC_ARM_REG_CPSR, (vector % 16) << 28 | 0x10)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    engine.hook_add(UC_HOOK_CODE, step)
    engine.emu_start(ADDRESS, 0x04000000, count=4096)
    if engine.reg_read(UC_ARM_REG_PC) != 0x04000000:
        raise ValueError("Scene initialization did not return in bound")
    expectedNames = [
        "init",
        "clear",
        "string",
        "load",
        "size",
        "import-first",
        "sync",
        "free",
        "string",
        "load",
        "size",
        "import-second",
        "free",
        "string",
        "load",
        "import-third",
        "import-third",
        "free",
        "reset",
        "palette",
    ]
    expectedNames += ["clear", "widget", "mode", "enable", "position", "clip"] * 3 + ["finish", "publish"]
    state[8] = 2
    state[7] = 0
    struct.pack_into("<i", state, 88, 1)
    struct.pack_into("<i", state, 76, 0)
    struct.pack_into("<I", state, 84, heights[(vector + 3) % 4])
    struct.pack_into("<I", state, 96, 192)
    for row in range(3):
        at = row * 144
        records[at : at + 4] = bytes(4)
        struct.pack_into("<I", records, at + 16, 0x12340000 + vector + row)
        struct.pack_into("<I", records, at + 20, 2)
        struct.pack_into("<I", records, at + 24, 1)
        struct.pack_into("<2I", records, at + 28, 128, row * 64)
        struct.pack_into("<2I", records, at + 36, heights[(vector + row + 1) % 4], 112)
        struct.pack_into("<I", records, at + 124, [0, 2, 0x80000000, 0xFFFFFFFF][(vector + row) % 4] & ~2)
    for row, constant in enumerate([4, 0x104, 0x1810, 0x418]):
        before = struct.unpack_from("<H", gpu, 8 + row * 2)[0]
        after = ((before & 0x43) | constant) & ~3 | (3 - row)
        struct.pack_into("<H", gpu, 8 + row * 2, after)
    word = struct.unpack_from("<I", gpu, 0)[0]
    struct.pack_into("<I", gpu, 0, word & ~0x1F00 | 0x1F00)
    struct.pack_into("<4I", gpu, 16, 0, 0x00C00000, 0x00040004, 0x00C00000)
    if [c["kind"] for c in calls] != expectedNames or engine.reg_read(UC_ARM_REG_R0) != 0x55000000 + vector:
        raise ValueError("Scene independent resource/widget call order or captured return differs")
    if bytes(engine.mem_read(STATE, 112)) != bytes(state) or bytes(engine.mem_read(RECORDS, len(records))) != bytes(
        records
    ):
        raise ValueError("Scene complete state/three records/padding effects differ")
    if bytes(engine.mem_read(0x04000000, 64)) != bytes(gpu) or bytes(engine.mem_read(VRAM, 0x80000)) != bytes(0x80000):
        raise ValueError("Scene masked GPU register or complete VRAM clear effects differ")
    return {
        "registers": [engine.reg_read(r) for r in REGS],
        "cpsr": engine.reg_read(UC_ARM_REG_CPSR),
        "calls": calls,
        "writes": writes,
        "stateSha256": sha(bytes(state) + bytes(records) + bytes(gpu)),
        "stackSha256": sha(bytes(engine.mem_read(0x0301FF00, 256))),
    }


def main():
    report = json.loads((ROOT / "evidence/matches/ov005-ov005-calls01.json").read_text())
    if sha((ROOT / "inputs/game.nds").read_bytes()) != report["romSha256"]:
        raise ValueError("Scene ROM namespace changed")
    entry = next(e for e in report["matches"] if int(e["address"], 0) == ADDRESS)
    rows, found = reuse.compile_entry(
        ROOT / entry["source"], {"name": entry["name"], "module": "ov005", "mode": "arm"}, entry
    )
    if (
        found is None
        or found[0]["sourceSha256"] != entry["sourceSha256"]
        or found[0]["targetSha256"] != entry["targetSha256"]
    ):
        raise ValueError("Frozen scene source changed")
    vectors = []
    for vector in range(48):
        native = run(None, vector)
        compiled = run(found[1], vector)
        if native != compiled:
            raise ValueError("Native/compiled scene initialization differs")
        vectors.append({"index": vector, "stateSha256": sha(json.dumps(native, sort_keys=True).encode())})
    result = {
        "schemaVersion": 1,
        "kind": "module005-scene-initialization-oracle",
        "romSha256": report["romSha256"],
        "module": "ov005",
        "address": hex(ADDRESS),
        "source": Path(__file__).name,
        "sourceSha256": sha(Path(__file__).read_bytes()),
        "passed": True,
        "vectors": 48,
        "executions": 96,
        "instructionLimit": 4096,
        "sourceDependency": {k: entry[k] for k in ["source", "sourceSha256", "address", "bytes", "compilerSha256"]},
        "independentChecks": [
            "Complete32-byte temporary descriptor lifetime and three resource ownership paths",
            "Saved handles survive call-clobbered registers and size getter callbacks",
            "Masked initial GPU bits, priority fields and four final coordinate words",
            "Exact524288-byte VRAM clear span",
            "Three144-byte records, mode/enable/coordinates, fresh clip heights and whole flag-word masks",
            "State area/count stores observed before reset and complete padding preservation",
        ],
        "dependencyModel": "Only the712-byte scene caller executes original native code or its recompiled C. Explicit SDK/module callback contracts isolate file/GPU/widget services; their actual implementations and full platform semantics receive no source credit.",
        "acceptedSourceFunctionsAdded": 0,
        "acceptedSourceBytesAdded": 0,
        "results": vectors,
    }
    raw = json.dumps(result, indent=2).encode()
    folder = ROOT / "evidence/validation"
    immutable = folder / ("ov005-scene-" + sha(raw)[:12] + ".json")
    if immutable.exists() and immutable.read_bytes() != raw:
        raise ValueError("Immutable scene proof collision")
    immutable.write_bytes(raw)
    current = folder / "ov005-scene.json"
    temporary = current.with_suffix(".json.tmp")
    temporary.write_bytes(raw)
    os.replace(temporary, current)
    print(json.dumps({"report": str(immutable.relative_to(ROOT)), "passed": True, "vectors": 48}))


if __name__ == "__main__":
    main()
