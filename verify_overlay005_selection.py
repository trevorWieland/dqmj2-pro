import hashlib
import json
import os
import random
import struct
from pathlib import Path
import reuse_overlay_c as reuse
from overlay_oracle005_registry import machine, REGS
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_INVALID
from unicorn.arm_const import (
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_CPSR,
)

ROOT = Path(__file__).resolve().parent
ADDRESS = 0x021E2640
STATE = 0x021ED438
CURSOR = 0x021ED348
STAGING = 0x021EDAF4
FLAG = 0x021E7764
SIZE = 616
CALLS = {
    0x021E0964: "gate",
    0x021E0D88: "refresh",
    0x0202A634: "input",
    0x020BF014: "record",
    0x020BF148: "commit",
    0x021E155C: "phase",
    0x021E1048: "sound",
    0x020653C0: "enable",
    0x020BF218: "destination",
    0x02048034: "reset-record",
    0x021E0708: "panel",
    0x021E0724: "show",
    0x021E0040: "finish",
    0x021E6D64: "prepare",
    0x020BF084: "cancel-record",
    0x021E026C: "restore",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def parameters(index):
    v = max(index - 8, 0)
    capacity = [0, 6, 7, 128, 255][v % 5]
    v //= 5
    last = v % 4
    v //= 4
    first = v % 4
    v //= 4
    choice = v % 4
    return {
        "gate": int(index < 8),
        "choice": choice,
        "first": first,
        "last": last,
        "capacity": capacity,
        "slot": [0, 127, 128, 255][index % 4],
        "alias": index // 160 % 2,
        "prefix": [0, 1, 65535, 0xFFFFFFFF][index % 4],
    }


def run(patches, index):
    p = parameters(index)
    engine = machine(patches)
    rng = random.Random(202610280452 + index)
    state = bytearray(rng.randbytes(104))
    state[4] = p["slot"]
    engine.mem_write(STATE, bytes(state))
    engine.mem_write(CURSOR, struct.pack("<I", p["prefix"]))
    flag = rng.randbytes(4)
    engine.mem_write(FLAG, flag)
    regions = {
        STAGING - 4: rng.randbytes(SIZE + 8),
        0x03006000: rng.randbytes(SIZE + 8),
        0x03007000: rng.randbytes(SIZE + 8),
        0x0300B000: rng.randbytes(SIZE + 8),
        0x0300C000: rng.randbytes(SIZE + 8),
    }
    for address, data in regions.items():
        engine.mem_write(address, data)
    data = bytearray(regions[0x03006000])
    data[0xAF] = p["capacity"]
    regions[0x03006000] = bytes(data)
    engine.mem_write(0x03006000, bytes(data))
    engine.mem_write(0x03005000, struct.pack("<2H", 0, p["first"]))
    engine.mem_write(0x03005100, struct.pack("<2H", 0, p["last"]))
    engine.mem_write(0x0301FF00, rng.randbytes(256))
    registers = [rng.getrandbits(32) for unused in range(13)] + [0x0301FFF0, 0x04000000]
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for reg, value in zip(REGS, registers):
        engine.reg_write(reg, value)
    calls = []
    writes = []
    counts = {"record": 0, "input": 0, "destination": 0, "finish": 0}
    engine.hook_add(
        UC_HOOK_MEM_WRITE,
        lambda uc, access, at, width, value, user: writes.append([at, width, value & ((1 << (width * 8)) - 1)]),
    )

    def step(uc, address, width, user):
        if address not in CALLS:
            return
        kind = CALLS[address]
        args = [uc.reg_read(r) for r in [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3]]
        calls.append({"kind": kind, "args": args, "stack": bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 8)).hex()})
        value = 0
        if kind == "gate":
            if args[:2] != [1, (p["prefix"] + 6) & 65535]:
                raise ValueError("Connected entry gate/cursor addition differs")
            value = p["gate"]
        elif kind == "refresh":
            uc.mem_write(CURSOR, struct.pack("<I", p["choice"]))
        elif kind == "input":
            counts[kind] += 1
            value = 0x03005000 if counts[kind] == 1 else 0x03005100
        elif kind == "record":
            expected = (p["slot"] + counts[kind]) & 255
            if args[0] != expected:
                raise ValueError("Record selector did not reload SDK-mutated slot byte")
            counts[kind] += 1
            value = 0x03006000 if counts[kind] == 1 else 0x03007000
            uc.mem_write(STATE + 4, bytes([(p["slot"] + counts[kind]) & 255]))
        elif kind == "commit":
            if args[0] != (p["slot"] + 1) & 255:
                raise ValueError("Commit slot argument not reloaded")
            uc.mem_write(STATE + 4, bytes([((p["slot"] + 1) & 255) ^ 128]))
        elif kind == "phase":
            uc.mem_write(STATE + 100, struct.pack("<I", args[0]))
        elif kind == "destination":
            counts[kind] += 1
            value = (0x03007000 if p["alias"] else 0x0300B000) if counts[kind] == 1 else 0x0300C000
        elif kind == "reset-record":
            if args[:2] != [0x0300C0B0, 0]:
                raise ValueError("Second destination getter pointer not used")
            uc.mem_write(0x0300C0B0, struct.pack("<I", 0xAA550000 + index))
        elif kind == "finish":
            counts[kind] += 1
            value = 0x77000000 + index + counts[kind]
            uc.mem_write(STATE + 28, struct.pack("<I", value))
        elif kind == "cancel-record":
            value = 0x03009000
        uc.reg_write(UC_ARM_REG_R0, value)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    engine.hook_add(UC_HOOK_CODE, step)

    def invalid(uc, access, address, width, value, user):
        raise ValueError(
            f"Invalid selection access index{index} pc{uc.reg_read(UC_ARM_REG_PC):08x} target{address:08x} args"
            + str([hex(uc.reg_read(r)) for r in [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3]])
        )

    engine.hook_add(UC_HOOK_MEM_INVALID, invalid)
    engine.emu_start(ADDRESS, 0x04000000, count=8192)
    if engine.reg_read(UC_ARM_REG_PC) != 0x04000000:
        raise ValueError("Selection handler failed bounded native return")
    expected = []
    checks = {}
    finalFlag = flag
    slot = p["slot"]
    finish = 0
    if p["gate"]:
        result = 1
    else:
        expected += ["refresh", "input"]
        result = p["last"]
        if p["first"] & 1:
            choice = p["choice"]
            if choice == 0:
                expected += ["record", "commit", "phase"]
                regions[STAGING - 4] = regions[STAGING - 4][:4] + regions[0x03006000][:SIZE] + regions[STAGING - 4][-4:]
                slot = ((slot + 1) & 255) ^ 128
                finalFlag = struct.pack("<I", 87)
                struct.pack_into("<I", state, 100, 18)
                struct.pack_into("<I", state, 24, 0)
                checks["phase"] = [[18]]
            elif choice == 1:
                expected += ["record"]
                slot = (slot + 1) & 255
                if p["capacity"] >= 7:
                    expected += ["sound"]
                    checks["sound"] = [[84]]
                else:
                    expected += [
                        "enable",
                        "sound",
                        "record",
                        "destination",
                        "destination",
                        "reset-record",
                        "panel",
                        "phase",
                    ]
                    checks.update(enable=[[1]], sound=[[82]], panel=[[19, 2, 14]], phase=[[53]])
                    slot = (slot + 1) & 255
                    destination = 0x03007000 if p["alias"] else 0x0300B000
                    regions[destination] = regions[0x03007000][:SIZE] + regions[destination][SIZE:]
                    data = bytearray(regions[0x0300C000])
                    struct.pack_into("<I", data, 0xB0, 0xAA550000 + index)
                    regions[0x0300C000] = bytes(data)
                    struct.pack_into("<I", state, 100, 13)
            elif choice == 2:
                expected += ["prepare", "panel", "show", "phase", "finish", "sound"]
                checks.update(panel=[[19, 2, 26]], show=[[1]], phase=[[14]], sound=[[82]])
                struct.pack_into("<I", state, 100, 14)
                finish += 1
                struct.pack_into("<I", state, 28, 0x77000000 + index + finish)
        expected += ["input"]
        if p["last"] & 2:
            expected += ["sound", "phase", "cancel-record", "restore", "finish"]
            checks.setdefault("sound", []).append([83])
            checks.setdefault("phase", []).append([12])
            checks["restore"] = [[0x03009000, slot, 0, 1]]
            struct.pack_into("<I", state, 100, 12)
            struct.pack_into("<I", state, 24, 1)
            finish += 1
            result = 0x77000000 + index + finish
            struct.pack_into("<I", state, 28, result)
    state[4] = slot
    names = [c["kind"] for c in calls]
    if names != ["gate"] + expected:
        raise ValueError("Selection independent gate/case/input callback order differs")
    for name, values in checks.items():
        actual = [c["args"][: len(v)] for c, v in zip([c for c in calls if c["kind"] == name], values)]
        if actual != values:
            raise ValueError("Selection independent callback argument sequence differs: " + name)
    for call in calls:
        if call["kind"] == "restore" and bytes.fromhex(call["stack"]) != bytes(8):
            raise ValueError("Selection restore stack flags differ")
    if (
        engine.reg_read(UC_ARM_REG_R0) != result
        or bytes(engine.mem_read(STATE, 104)) != bytes(state)
        or bytes(engine.mem_read(FLAG, 4)) != finalFlag
    ):
        raise ValueError("Selection full state/word-width flag/return effects differ")
    for address, data in regions.items():
        if bytes(engine.mem_read(address, len(data))) != data:
            raise ValueError("Selection complete616-byte copy/reset/padding effects differ")
    return {
        "registers": [engine.reg_read(r) for r in REGS],
        "cpsr": engine.reg_read(UC_ARM_REG_CPSR),
        "calls": calls,
        "writes": writes,
        "stateSha256": sha(
            bytes(state) + finalFlag + b"".join(bytes(engine.mem_read(a, len(d))) for a, d in regions.items())
        ),
        "stackSha256": sha(bytes(engine.mem_read(0x0301FF00, 256))),
    }


def main():
    if (
        sha((ROOT / "inputs/game.nds").read_bytes())
        != "674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6"
    ):
        raise ValueError("Wrong ROM namespace")
    reports = [
        json.loads((ROOT / p).read_text())
        for p in ["evidence/matches/ov005-ov005-scalars01.json", "evidence/matches/ov005-reuse01.json"]
    ]
    wanted = {ADDRESS, 0x021E0938, 0x021E0A84, 0x021E0A90, 0x021E0A68}
    patches = {}
    dependencies = []
    for address in sorted(wanted):
        entry = next(e for report in reports for e in report["matches"] if int(e["address"], 0) == address)
        rows, found = reuse.compile_entry(
            ROOT / entry["source"], {"name": entry["name"], "module": "ov005", "mode": "arm"}, entry
        )
        if (
            found is None
            or found[0]["sourceSha256"] != entry["sourceSha256"]
            or found[0]["targetSha256"] != entry["targetSha256"]
        ):
            raise ValueError("Frozen selection-chain source identity changed")
        patches[address] = found[1]
        dependencies.append({k: entry[k] for k in ["address", "bytes", "source", "sourceSha256", "compilerSha256"]})
    vectors = []
    for index in range(328):
        native = run({}, index)
        compiled = run(patches, index)
        if native != compiled:
            raise ValueError("Connected native/recompiled selection handler differs")
        vectors.append({"index": index, "stateSha256": sha(json.dumps(native, sort_keys=True).encode())})
    mainImage = (ROOT / "extract/arm9/arm9.bin").read_bytes()
    result = {
        "schemaVersion": 1,
        "kind": "module005-connected-selection-handler-oracle",
        "romSha256": reports[0]["romSha256"],
        "module": "ov005",
        "address": hex(ADDRESS),
        "source": Path(__file__).name,
        "sourceSha256": sha(Path(__file__).read_bytes()),
        "passed": True,
        "vectors": 328,
        "executions": 656,
        "instructionLimit": 8192,
        "sourceDependencies": dependencies,
        "executedNativeHelpers": [
            {"module": "main", "address": "0x02008e0c", "bytes": 304, "sha256": sha(mainImage[0x8E0C:0x8F3C])}
        ],
        "dependencyModel": "Caller, entry wrapper and address/input getter thunks execute actual native code or freshly recompiled C; native304-byte memory-copy helper executes. Other listed SDK/module targets use explicit isolated synthetic contracts, whose actual platform semantics are not claimed.",
        "independentChecks": [
            "Entry gate and first/second input pointer identities",
            "All four selector values, five capacity boundaries and both button tests",
            "Fresh slot reloads after SDK mutation",
            "Full616-byte source/destination snapshots including boundary padding and exact alias case",
            "Whole-word87 store clears all three upper bytes",
            "Complete state fields, callback order/arguments/stack flags and captured return values",
        ],
        "acceptedSourceFunctionsAdded": 0,
        "acceptedSourceBytesAdded": 0,
        "results": vectors,
    }
    raw = json.dumps(result, indent=2).encode()
    folder = ROOT / "evidence/validation"
    immutable = folder / ("ov005-selection-" + sha(raw)[:12] + ".json")
    if immutable.exists() and immutable.read_bytes() != raw:
        raise ValueError("Immutable selection evidence collision")
    immutable.write_bytes(raw)
    current = folder / "ov005-selection.json"
    temporary = current.with_suffix(".json.tmp")
    temporary.write_bytes(raw)
    os.replace(temporary, current)
    print(json.dumps({"report": str(immutable.relative_to(ROOT)), "passed": True, "vectors": 328}))


if __name__ == "__main__":
    main()
