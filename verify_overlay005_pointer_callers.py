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
BASE = 0x021D7240
VALUES = [0, 1, 127, 128, 255, 65535, 0x80000000, 0xFFFFFFFF]
CALLERS = {
    0x021DFABC: (0x021DFAB0, 0x021ED1B0),
    0x021E0938: (0x021E0A68, 0x021ED348),
    0x021E0A90: (0x021E0A68, 0x021ED348),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(address, patches, index):
    engine = machine(patches)
    rng = random.Random(20261028005 + address + index)
    helper, data = CALLERS[address]
    before = rng.randbytes(64)
    value = VALUES[index % 8]
    second = VALUES[index // 8 % 8]
    first = [0, 1, 0xFFFFFFFF, 0x03006000][index // 64 % 4]
    engine.mem_write(data, before)
    engine.mem_write(data, struct.pack("<I", value))
    initial = bytes(engine.mem_read(data, 64))
    tag = 0xAABB0000 + index
    registers = (
        [first, second, rng.getrandbits(32), rng.getrandbits(32)]
        + [rng.getrandbits(32) for unused in range(9)]
        + [0x0301FFF0, 0x04000000]
    )
    engine.mem_write(0x0301FF00, rng.randbytes(256))
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for reg, number in zip(REGS, registers):
        engine.reg_write(reg, number)
    calls = []
    writes = []
    engine.hook_add(
        UC_HOOK_MEM_WRITE,
        lambda uc, access, at, width, number, user: writes.append([at, width, number & ((1 << (width * 8)) - 1)]),
    )

    def step(uc, at, width, user):
        if at == helper:
            calls.append({"address": hex(at), "kind": "actual-native-or-recompiled-address-getter"})
        if at != 0x021E0964:
            return
        arguments = [uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)]
        if arguments != [first, (second + value) & 0xFFFF]:
            raise ValueError("Pointer caller unsigned word addition/halfword forwarding differs")
        calls.append({"address": hex(at), "kind": "isolated-synthetic-external-contract", "arguments": arguments})
        uc.mem_write(data, struct.pack("<I", value ^ 0xFFFFFFFF))
        uc.mem_write(0x03008000, struct.pack("<I", tag))
        uc.reg_write(UC_ARM_REG_R0, tag)
        for i, reg in enumerate([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]):
            uc.reg_write(reg, (tag ^ 0x9E3779B9 * (i + 1)) & 0xFFFFFFFF)
        uc.reg_write(UC_ARM_REG_CPSR, (index % 16) << 28 | 0x10)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    engine.hook_add(UC_HOOK_CODE, step)
    engine.emu_start(address, 0x04000000, count=4096)
    if engine.reg_read(UC_ARM_REG_PC) != 0x04000000:
        raise ValueError("Pointer caller did not return in bound")
    expected = bytearray(initial)
    wanted = [{"address": hex(helper), "kind": "actual-native-or-recompiled-address-getter"}]
    if address == 0x021E0938:
        expected[:4] = struct.pack("<I", value ^ 0xFFFFFFFF)
        wanted.append(
            {
                "address": "0x21e0964",
                "kind": "isolated-synthetic-external-contract",
                "arguments": [first, (second + value) & 0xFFFF],
            }
        )
        if engine.reg_read(UC_ARM_REG_R0) != tag or bytes(engine.mem_read(0x03008000, 4)) != struct.pack("<I", tag):
            raise ValueError("Synthetic destination callee return/effect not propagated")
    elif engine.reg_read(UC_ARM_REG_R0) != value:
        raise ValueError("Connected pointer getter did not return full original word")
    if (
        calls != wanted
        or bytes(engine.mem_read(data, 64)) != bytes(expected)
        or any(not 0x0301FF00 <= at < 0x03020000 for at, width, number in writes)
    ):
        raise ValueError("Pointer caller complete object/call/preservation effects differ")
    return {
        "registers": [engine.reg_read(r) for r in REGS],
        "cpsr": engine.reg_read(UC_ARM_REG_CPSR),
        "calls": calls,
        "writes": writes,
        "objectSha256": sha(bytes(expected)),
        "stackSha256": sha(bytes(engine.mem_read(0x0301FF00, 256))),
    }


def main():
    if (
        sha((ROOT / "inputs/game.nds").read_bytes())
        != "674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6"
    ):
        raise ValueError("Wrong ROM namespace")
    report = json.loads((ROOT / "evidence/matches/ov005-reuse01.json").read_text())
    addresses = set(CALLERS) | {x[0] for x in CALLERS.values()}
    patches = {}
    dependencies = []
    for address in sorted(addresses):
        entry = next(e for e in report["matches"] if int(e["address"], 0) == address)
        if sha((ROOT / entry["source"]).read_bytes()) != entry["sourceSha256"]:
            raise ValueError("Frozen pointer-caller source changed")
        rows, result = reuse.compile_entry(
            ROOT / entry["source"], {"name": entry["name"], "module": "ov005", "mode": "arm"}, entry
        )
        if result is None or result[0]["targetSha256"] != entry["targetSha256"]:
            raise ValueError("Pointer caller or address-getter source no longer matches")
        patches[address] = result[1]
        dependencies.append({k: entry[k] for k in ["source", "sourceSha256", "address", "bytes", "compilerSha256"]})
    functions = []
    for address in CALLERS:
        count = 256 if address == 0x021E0938 else 32
        vectors = []
        for index in range(count):
            native = run(address, {}, index)
            compiled = run(address, patches, index)
            if native != compiled:
                raise ValueError("Connected native/recompiled pointer caller differs")
            vectors.append({"index": index, "stateSha256": sha(json.dumps(native, sort_keys=True).encode())})
        functions.append(
            {"address": hex(address), "passed": True, "vectors": count, "executions": count * 2, "results": vectors}
        )
    result = {
        "schemaVersion": 1,
        "kind": "module005-connected-pointer-caller-oracles",
        "romSha256": report["romSha256"],
        "module": "ov005",
        "moduleInputSha256": report["moduleInputSha256"],
        "source": Path(__file__).name,
        "sourceSha256": sha(Path(__file__).read_bytes()),
        "sourceDependencies": dependencies,
        "functions": functions,
        "instructionLimit": 4096,
        "acceptedSourceFunctionsAdded": 0,
        "acceptedSourceBytesAdded": 0,
        "dependencyModel": "Both caller and12-byte address getter execute native instructions in the original run and freshly recompiled C in the paired run. Only021E0964 uses an explicit synthetic callee contract; its full platform behavior and source are not claimed.",
        "limitations": [
            "Fresh isolated module state and bounded synthetic objects/arguments are exercised; this does not claim a full game overlay-load trace or external destination-callee semantics."
        ],
    }
    raw = json.dumps(result, indent=2).encode()
    folder = ROOT / "evidence/validation"
    folder.mkdir(parents=True, exist_ok=True)
    immutable = folder / ("ov005-pointer-callers-" + sha(raw)[:12] + ".json")
    if immutable.exists() and immutable.read_bytes() != raw:
        raise ValueError("Immutable pointer-caller evidence collision")
    immutable.write_bytes(raw)
    current = folder / "ov005-pointer-callers.json"
    temporary = current.with_suffix(".json.tmp")
    temporary.write_bytes(raw)
    os.replace(temporary, current)
    print(
        json.dumps(
            {
                "report": str(immutable.relative_to(ROOT)),
                "functions": len(functions),
                "vectors": sum(f["vectors"] for f in functions),
                "passed": True,
            }
        )
    )


if __name__ == "__main__":
    main()
