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
STATE = 0x021E9818
ARRAY = 0x021E992C
BYTE = 0x021E708C
COUNTS = {0x021DBC7C: 90, 0x021DC4CC: 192, 0x021DCC10: 64, 0x021DBAA4: 48}
TARGETS = {
    0x02084924: "allocate",
    0x02049FFC: "prepare-object",
    0x02084F4C: "release",
    0x021DA874: "reset",
    0x021DB134: "cleanup",
    0x020485B4: "release-field",
    0x020484DC: "restore-byte",
    0x02045654: "finish",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(address, patches, vector):
    rng = random.Random(202610280168 + address + vector)
    engine = machine(patches)
    state = bytearray(rng.randbytes(112))
    flag = [0, 1, 2, 3, 4, 127, 128, 255][vector % 8]
    count = [-1, 0, 1, 2, 9, 15][vector // 8 % 6]
    mode = [0, 1, 2, 127, 128, 255][vector % 6]
    area = [0, 5, 4096, -32][vector % 4]
    dims = [(-2, 3), (0, 0), (1, 1), (5, 7), (10, 255)][vector % 5]
    mutation = vector // 48 % 4
    if address == 0x021DBC7C:
        count = vector % 15
        mutation = vector // 15 % 3
    state[8] = flag
    state[102] = mode
    struct.pack_into("<i", state, 76, count)
    struct.pack_into("<i", state, 88, area)
    engine.mem_write(STATE, bytes(state))
    handles = [0x03009000 + i * 64 for i in range(16)]
    pointers = list(handles)
    engine.mem_write(ARRAY, struct.pack("<16I", *pointers))
    nodes = {p: rng.randbytes(44) for p in handles + [0x0300F000, 0x0300F080]}
    for pointer, data in nodes.items():
        engine.mem_write(pointer, data)
    beforeByte = [0, 127, 128, 255][vector % 4]
    afterByte = [255, 128, 127, 0][vector % 4]
    engine.mem_write(BYTE, bytes([beforeByte]))
    args = [[0, 1, 0x80000000, 0xFFFFFFFF][vector % 4], 0xAABB0000 + vector, dims[0] & 0xFFFFFFFF, dims[1] & 0xFFFFFFFF]
    registers = args + [rng.getrandbits(32) for unused in range(9)] + [0x0301FFF0, 0x04000000]
    engine.mem_write(0x0301FF00, rng.randbytes(256))
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for register, value in zip(REGS, registers):
        engine.reg_write(register, value)
    calls = []
    writes = []
    released = []
    postAllocateCount = count if mutation == 0 else (count + 3) % 15
    postPrepareCount = count if mutation == 0 else (count + 7) % 15
    postArea = area if mutation == 0 else [0, 5, 4096, -32][(vector + 1) % 4]
    releaseCount = count
    engine.hook_add(
        UC_HOOK_MEM_WRITE,
        lambda uc, access, at, width, value, user: writes.append([at, width, value & ((1 << (width * 8)) - 1)]),
    )

    def step(uc, pc, width, user):
        if pc not in TARGETS:
            return
        kind = TARGETS[pc]
        actual = [uc.reg_read(r) for r in [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3]]
        calls.append({"kind": kind, "args": actual})
        value = 0
        if kind == "allocate":
            stack = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 24))
            if actual != [7, args[0], args[1], args[2]] or stack != struct.pack(
                "<6I", args[3], 3, 3, area & 0xFFFFFFFF, 1, 1
            ):
                raise ValueError("Allocator complete six-word stack contract differs")
            uc.mem_write(STATE + 76, struct.pack("<i", postAllocateCount))
            value = 0x0300F000
        elif kind == "prepare-object":
            if actual[0] != 0x0300F000:
                raise ValueError("Object preparation did not receive allocator return in r0")
            uc.mem_write(STATE + 76, struct.pack("<i", postPrepareCount))
            uc.mem_write(STATE + 88, struct.pack("<i", postArea))
            if mutation == 2:
                uc.mem_write(ARRAY + postPrepareCount * 4, struct.pack("<I", 0x0300F080))
        elif kind == "release":
            released.append(actual[0])
            if len(released) == 1 and mutation:
                uc.mem_write(STATE + 76, struct.pack("<i", [0, 1, 3, 15][mutation]))
        elif kind in ["reset", "cleanup"]:
            uc.mem_write(STATE + 76, struct.pack("<i", 0))
            uc.mem_write(STATE + 24, struct.pack("<I", 0xAABB0000 + vector))
            if kind == "reset":
                uc.mem_write(STATE + 8, b"\xa5")
            else:
                uc.mem_write(STATE + 102, b"\x7f")
        elif kind == "release-field":
            if actual[0] != 0xAABB0000 + vector:
                raise ValueError("Cleanup did not reload SDK-reset field")
            uc.mem_write(BYTE, bytes([afterByte]))
        elif kind == "restore-byte":
            if actual[:2] != [0, afterByte]:
                raise ValueError("Cleanup did not reload latest global byte")
            value = 0x44000000 + vector
            uc.mem_write(STATE + 28, struct.pack("<I", value))
        elif kind == "finish":
            if actual[0] != 1:
                raise ValueError("Cleanup terminal enable flag differs")
            value = 0x55000000 + vector
            uc.mem_write(STATE + 32, struct.pack("<I", value))
        uc.reg_write(UC_ARM_REG_R0, value)
        for i, register in enumerate([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]):
            uc.reg_write(register, (0x9E3779B9 * (i + 1) + vector) & 0xFFFFFFFF)
        uc.reg_write(UC_ARM_REG_CPSR, (vector % 16) << 28 | 0x10)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    engine.hook_add(UC_HOOK_CODE, step)
    engine.emu_start(address, 0x04000000, count=4096)
    if engine.reg_read(UC_ARM_REG_PC) != 0x04000000:
        raise ValueError("Resource operation did not return in bound")
    expectedNames = []
    expectedByte = beforeByte
    if address == 0x021DBC7C:
        expectedNames = ["allocate", "prepare-object"]
        pointers[count] = 0x0300F000
        if mutation == 2:
            pointers[postPrepareCount] = 0x0300F080
        selected = pointers[postPrepareCount]
        record = bytearray(nodes[selected])
        originalFlags = struct.unpack_from("<I", record, 24)[0]
        struct.pack_into("<I", record, 24, originalFlags | 2)
        nodes[selected] = bytes(record)
        struct.pack_into("<i", state, 76, postPrepareCount + 1)
        struct.pack_into("<i", state, 88, postArea + dims[0] * dims[1])
        result = postPrepareCount
    elif address == 0x021DBAA4:
        total = 15 if mode == 0 else 14 if mode == 1 else 0
        expectedNames = ["release"] * total + ["cleanup"]
        if released != handles[:total]:
            raise ValueError("Signed mode/fixed cleanup span differs")
        struct.pack_into("<i", state, 76, 0)
        struct.pack_into("<I", state, 24, 0xAABB0000 + vector)
        state[102] = 255
        result = STATE
    else:
        required = 2 if address == 0x021DC4CC else 3
        if flag != required:
            result = flag if address == 0x021DC4CC else STATE
        else:
            total = 9
            if address == 0x021DC4CC:
                total = 0
                current = count
                while total < current:
                    total += 1
                    if total == 1 and mutation:
                        current = [0, 1, 3, 15][mutation]
            expectedNames = ["release"] * total + ["reset", "release-field", "restore-byte"]
            if released != handles[:total]:
                raise ValueError("Dynamic count reload or fixed nine-entry cleanup span differs")
            struct.pack_into("<i", state, 76, 0)
            struct.pack_into("<I", state, 24, 0xAABB0000 + vector)
            struct.pack_into("<I", state, 28, 0x44000000 + vector)
            state[8] = 165
            expectedByte = afterByte
            result = 0x44000000 + vector
            if address == 0x021DC4CC:
                expectedNames.append("finish")
                struct.pack_into("<I", state, 32, 0x55000000 + vector)
                result = 0x55000000 + vector
    if [c["kind"] for c in calls] != expectedNames or engine.reg_read(UC_ARM_REG_R0) != result:
        raise ValueError("Resource independent callback order/captured return differs")
    if (
        bytes(engine.mem_read(STATE, len(state))) != bytes(state)
        or bytes(engine.mem_read(ARRAY, 64)) != struct.pack("<16I", *pointers)
        or bytes(engine.mem_read(BYTE, 1)) != bytes([expectedByte])
    ):
        raise ValueError("Resource complete state/array/global-byte effects differ")
    if any(bytes(engine.mem_read(p, 44)) != data for p, data in nodes.items()):
        raise ValueError("Resource object flag/prefix preservation differs")
    return {
        "registers": [engine.reg_read(r) for r in REGS],
        "cpsr": engine.reg_read(UC_ARM_REG_CPSR),
        "calls": calls,
        "writes": writes,
        "stateSha256": sha(bytes(state) + struct.pack("<16I", *pointers) + b"".join(nodes.values())),
        "stackSha256": sha(bytes(engine.mem_read(0x0301FF00, 256))),
    }


def main():
    report = json.loads((ROOT / "evidence/matches/ov005-ov005-scalars02.json").read_text())
    if sha((ROOT / "inputs/game.nds").read_bytes()) != report["romSha256"]:
        raise ValueError("Resource ROM namespace changed")
    patches = {}
    dependencies = []
    for address in COUNTS:
        entry = next(e for e in report["matches"] if int(e["address"], 0) == address)
        records, result = reuse.compile_entry(
            ROOT / entry["source"], {"name": entry["name"], "module": "ov005", "mode": "arm"}, entry
        )
        if (
            result is None
            or result[0]["sourceSha256"] != entry["sourceSha256"]
            or result[0]["targetSha256"] != entry["targetSha256"]
        ):
            raise ValueError("Frozen resource source no longer matches")
        patches[address] = result[1]
        dependencies.append({k: entry[k] for k in ["address", "bytes", "source", "sourceSha256", "compilerSha256"]})
    functions = []
    for address, count in COUNTS.items():
        states = []
        for vector in range(count):
            native = run(address, {}, vector)
            compiled = run(address, patches, vector)
            if native != compiled:
                raise ValueError("Native/compiled resource operation differs")
            states.append({"index": vector, "stateSha256": sha(json.dumps(native, sort_keys=True).encode())})
        functions.append(
            {"address": hex(address), "passed": True, "vectors": count, "executions": count * 2, "results": states}
        )
    result = {
        "schemaVersion": 1,
        "kind": "module005-resource-operations-oracle",
        "romSha256": report["romSha256"],
        "module": "ov005",
        "source": Path(__file__).name,
        "sourceSha256": sha(Path(__file__).read_bytes()),
        "passed": True,
        "sourceDependencies": dependencies,
        "functions": functions,
        "instructionLimit": 4096,
        "acceptedSourceFunctionsAdded": 0,
        "acceptedSourceBytesAdded": 0,
        "independentChecks": [
            "All sixteen full-width resource-pointer array words and object prefixes",
            "Saved allocation slot versus SDK-mutated later slot and area",
            "All six allocator stack arguments and inherited allocator-result r0 at object preparation",
            "Dynamic count reload versus fixed nine/fourteen/fifteen-entry cleanup",
            "Signed mode bytes and callback-mutated state/global-byte reloads",
            "Whole object flag word OR and all padding preservation",
        ],
        "dependencyModel": "Only the four reported callers execute actual native code or freshly recompiled C. Listed SDK/module callbacks use explicit synthetic contracts; their original platform behavior receives no source credit.",
        "limitations": [
            "Finite counts are bounded to sixteen valid resource slots. Invalid handles, allocation failures, cycles, full platform lifetime, and count wrap beyond byte capacity remain unproved. Callee signatures are constrained by observed register/stack ABI effects rather than claimed original C declarations."
        ],
    }
    raw = json.dumps(result, indent=2).encode()
    folder = ROOT / "evidence/validation"
    immutable = folder / ("ov005-resources-" + sha(raw)[:12] + ".json")
    if immutable.exists() and immutable.read_bytes() != raw:
        raise ValueError("Immutable resource evidence collision")
    immutable.write_bytes(raw)
    current = folder / "ov005-resources.json"
    temporary = current.with_suffix(".json.tmp")
    temporary.write_bytes(raw)
    os.replace(temporary, current)
    print(
        json.dumps(
            {
                "report": str(immutable.relative_to(ROOT)),
                "passed": True,
                "functions": len(functions),
                "vectors": sum(COUNTS.values()),
            }
        )
    )


if __name__ == "__main__":
    main()
