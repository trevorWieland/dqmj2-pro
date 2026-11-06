import argparse
import hashlib
import json
import os
import random
import struct
from pathlib import Path
import match_runtime as compiler
from overlay_oracle005_registry import machine, REGS
from refine_scalar_globals import immutable
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_SP,
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_CPSR,
)

ROOT = Path(__file__).resolve().parent
BASE = 0x021D7240
ADDRESS = 0x021D9DE0
TARGET = ROOT / "evidence/matches/ov005-packet-manual.json"
CASES = sorted(
    {
        (chunks, index, width, (chunks - 1) * width + last, null)
        for chunks in range(1, 5)
        for index in range(chunks)
        for width in [1, 2, 7, 63, 508]
        for last in {1, max(width - 1, 1), width}
        for null in [False, True]
    }
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(code, vector):
    chunks, index, width, total, null = CASES[vector]
    rng = random.Random(202610280144 + vector)
    engine = machine({ADDRESS: code}) if code is not None else machine()
    obj, holder, root, context, packet, destinationPointer, output = [
        0x03002000,
        0x03003000,
        0x03004000,
        0x03006000,
        0x03008000,
        0x03009000,
        0x0300A000,
    ]
    memory = {
        obj: rng.randbytes(64),
        holder: rng.randbytes(32),
        root: rng.randbytes(64),
        context: rng.randbytes(0x590),
        packet: rng.randbytes(512),
        destinationPointer: rng.randbytes(4),
    }
    for at, data in memory.items():
        engine.mem_write(at, data)
    engine.mem_write(obj + 32, struct.pack("<I", holder))
    engine.mem_write(holder + 12, struct.pack("<I", root))
    engine.mem_write(root + 36, struct.pack("<I", context))
    engine.mem_write(context + 0x420, struct.pack("<2i", total, chunks))
    engine.mem_write(context + 0x586, struct.pack("<H", width))
    engine.mem_write(packet + 2, struct.pack("<H", index))
    destination = 0 if null else output + 4
    engine.mem_write(destinationPointer, struct.pack("<I", destination))
    memory = {at: bytes(engine.mem_read(at, len(data))) for at, data in memory.items()}
    before = rng.randbytes(4 * 508 + 8)
    engine.mem_write(output, before)
    engine.mem_write(0x0301FF00, rng.randbytes(256))
    registers = (
        [obj, packet, destinationPointer] + [rng.getrandbits(32) for unused in range(10)] + [0x0301FFF0, 0x04000000]
    )
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for register, value in zip(REGS, registers):
        engine.reg_write(register, value)
    calls = []
    writes = []

    def step(uc, pc, instructionWidth, user):
        if pc in [0x02026144, 0x02008E0C]:
            calls.append(
                {"address": hex(pc), "args": [uc.reg_read(r) for r in [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2]]}
            )

    engine.hook_add(UC_HOOK_CODE, step)
    engine.hook_add(
        UC_HOOK_MEM_WRITE,
        lambda uc, access, at, size, value, user: writes.append([at, size, value & ((1 << (size * 8)) - 1)]),
    )
    engine.emu_start(ADDRESS, 0x04000000, count=4096)
    if engine.reg_read(UC_ARM_REG_PC) != 0x04000000:
        raise ValueError("Packet caller or actual division/copy helper did not return")
    expected = bytearray(before)
    wanted = []
    if null:
        if engine.reg_read(UC_ARM_REG_R0) != root:
            raise ValueError("Null packet destination early return differs")
    else:
        remainder = total % width
        count = remainder if index == chunks - 1 and remainder else width
        if index == chunks - 1:
            wanted.append({"address": "0x2026144", "args": [total, width]})
        wanted.append({"address": "0x2008e0c", "args": [packet + 4, destination + index * 508, count]})
        start = 4 + index * 508
        expected[start : start + count] = memory[packet][4 : 4 + count]
    if len(calls) != len(wanted):
        raise ValueError("Packet native helper call count differs")
    for call, contract in zip(calls, wanted):
        if call["address"] != contract["address"] or call["args"][: len(contract["args"])] != contract["args"]:
            raise ValueError("Packet signed remainder or exact copy arguments differ")
    if bytes(engine.mem_read(output, len(expected))) != bytes(expected):
        raise ValueError("Packet final-block/full-block destination or boundary padding differs")
    if any(bytes(engine.mem_read(at, len(data))) != data for at, data in memory.items()):
        raise ValueError("Packet input graph/header/payload/output-pointer storage changed")
    if any(
        not (0x0301FF00 <= at and at + size <= 0x03020000 or output <= at and at + size <= output + len(expected))
        for at, size, value in writes
    ):
        raise ValueError("Packet native execution wrote outside stack and bounded output")
    return {
        "registers": [engine.reg_read(r) for r in REGS],
        "cpsr": engine.reg_read(UC_ARM_REG_CPSR),
        "calls": calls,
        "writes": writes,
        "outputSha256": sha(bytes(expected)),
        "stackSha256": sha(bytes(engine.mem_read(0x0301FF00, 256))),
    }


def oracle(code):
    results = []
    for vector in range(len(CASES)):
        native = run(None, vector)
        compiled = run(code, vector)
        if native != compiled:
            raise ValueError("Actual native/recompiled packet caller state differs")
        results.append({"index": vector, "stateSha256": sha(json.dumps(native, sort_keys=True).encode())})
    mainImage = (ROOT / "extract/arm9/arm9.bin").read_bytes()
    return {
        "passed": True,
        "vectors": len(CASES),
        "executions": len(CASES) * 2,
        "instructionLimit": 4096,
        "sourceModel": Path(__file__).name,
        "sourceModelSha256": sha(Path(__file__).read_bytes()),
        "results": results,
        "executedNativeHelpers": [
            {
                "module": "main",
                "address": hex(address),
                "bytes": size,
                "sha256": sha(mainImage[address - 0x02000000 : address - 0x02000000 + size]),
            }
            for address, size in [(0x02026144, 524), (0x02008E0C, 304)]
        ],
        "independentChecks": [
            "Zero through three packet indices in logically consistent one-through-four chunk records",
            "Five positive block widths and full/partial final blocks",
            "Actual signed division remainder determines final copy length",
            "Exact packet source offset,508-byte destination stride and null output behavior",
            "Complete destination with both boundary sentinels and untouched input object graph",
            "All registers/flags, ordered writes and stack state compared",
        ],
        "limitations": [
            "Positive block widths1,2,7,63,508 and nonnegative consistent payload lengths are exercised. Zero divisors, negative payload lengths, invalid pointers and larger packet counts are unproved.",
            "The C offset temporary width is a compiler-matching hypothesis; original source-language typedefs are not claimed. Non-null return-register behavior is compared through the actual native copy helper, without assigning a higher-level status meaning.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", type=Path)
    args = parser.parse_args()
    romHash = sha((ROOT / "inputs/game.nds").read_bytes())
    if romHash != "674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6":
        raise ValueError("Packet ROM namespace changed")
    if args.publish:
        if TARGET.exists():
            raise ValueError("Packet source already frozen")
        text = (ROOT / args.publish).read_text()
        if len(text.splitlines()) > 500:
            raise ValueError("Packet source exceeds500 lines")
        source = ROOT / f"src/overlays/ov005_packet_{sha(text.encode())[:12]}.c"
        immutable(source, text.encode())
        old = None
    else:
        old = json.loads(TARGET.read_text())
        source = ROOT / old["matches"][0]["source"]
    records, found = compiler.compare(source, "ov005", 2, "off", True)
    if "native_ov005_021d9de0" not in found:
        raise ValueError("Frozen packet C no longer matches every native byte")
    entry, code = found["native_ov005_021d9de0"]
    helpers = [r for r in entry["relocations"] if r["symbol"].startswith("_")]
    if [(r["symbol"], int(r["target"], 0)) for r in helpers] != [("_s32_div_f", 0x02026144)]:
        raise ValueError("Packet compiler helper no longer identifies proven native signed division")
    currentOracle = oracle(code)
    if old is not None:
        previous = old["matches"][0]
        for field in [
            "source",
            "sourceSha256",
            "address",
            "bytes",
            "compiledBytes",
            "targetSha256",
            "outputSha256",
            "relocations",
            "compilerSha256",
            "compilerFlags",
        ]:
            if entry[field] != previous[field]:
                raise ValueError("Frozen packet source/compiler/target/span/relocations changed")
        for field in ["object", "objectSha256", "sectionIndex", "sectionOffset"]:
            previous[field] = entry[field]
        report = old
    else:
        entry["oracle"] = currentOracle
        entry["sourceHypothesis"] = {
            "kind": "signed-remainder-and-wide-offset-local",
            "signedRuntimeHelper": "main:0x02026144",
            "offsetValueBound": "Unsigned16-bit index times508 fits32 bits; u64 local is narrowed to u32 at byte-pointer addition",
            "originalTypedefsProven": False,
            "ordinaryCOnly": True,
        }
        report = {
            "schemaVersion": 1,
            "romSha256": romHash,
            "module": "ov005",
            "moduleInputSha256": sha((ROOT / "extract/arm9_overlays/ov005.bin").read_bytes()),
            "matches": [entry],
            "nativeSymbols": {r["symbol"]: r["target"] for r in entry["relocations"]},
            "wholeModuleLinked": False,
            "sourceReconstructionComplete": False,
        }
    raw = json.dumps(report, indent=2).encode()
    temporary = TARGET.with_suffix(".json.tmp")
    temporary.write_bytes(raw)
    os.replace(temporary, TARGET)
    print(
        json.dumps(
            {
                "report": str(TARGET.relative_to(ROOT)),
                "source": entry["source"],
                "functions": 1,
                "bytes": entry["bytes"],
                "vectors": currentOracle["vectors"],
                "passed": True,
                "frozenProofPreserved": old is not None,
            }
        )
    )


if __name__ == "__main__":
    main()
