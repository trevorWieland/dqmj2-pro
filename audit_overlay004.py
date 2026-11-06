import hashlib
import json
import os
import random
import struct
import sys
from pathlib import Path

import dsprot128

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "deps/native"))
from ndspy import codeCompression
from unicorn import (
    Uc,
    UC_ARCH_ARM,
    UC_MODE_ARM,
    UC_HOOK_CODE,
    UC_HOOK_MEM_READ,
    UC_HOOK_MEM_WRITE,
)
from unicorn.arm_const import (
    UC_ARM_REG_CPSR,
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_SP,
)

ROM_HASH = "674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6"
BASE = 0x021D7240
STOP = 0x04000000
STACK = 0x03010000


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inputs():
    rom = (ROOT / "inputs/game.nds").read_bytes()
    if sha(rom) != ROM_HASH:
        raise ValueError("Original ROM namespace differs")
    start, size = struct.unpack_from("<2I", rom, 0x50)
    entries = [
        struct.unpack_from("<8I", rom, at) for at in range(start, start + size, 32)
    ]
    entry = next(item for item in entries if item[0] == 4)
    ident, base, initialized, bss_size, ctor_start, ctor_end, file_id, flags = entry
    if base != BASE or initialized != 7328 or bss_size != 32:
        raise ValueError("Overlay004 layout differs")
    fat = struct.unpack_from("<I", rom, 0x48)[0]
    first, last = struct.unpack_from("<2I", rom, fat + file_id * 8)
    stored = rom[first:last]
    decoded = codeCompression.decompress(stored)
    analysis = (ROOT / "extract/arm9_overlays/ov004.bin").read_bytes()
    metadata = (ROOT / "extract/arm9_overlays/overlays.yaml").read_text()
    variable, functions, relocations = dsprot128.metadata(metadata)
    pointers = list(
        struct.unpack(
            "<" + "I" * ((ctor_end - ctor_start) // 4),
            decoded[ctor_start - base : ctor_end - base],
        )
    )
    if len(decoded) != initialized or len(analysis) != initialized:
        raise ValueError("Overlay004 initialized size differs")
    if dsprot128.image_transform(decoded, functions, base, False) != analysis:
        raise ValueError("Independent full-image DSProtect decryption differs")
    if dsprot128.image_transform(analysis, functions, base, True) != decoded:
        raise ValueError("Independent full-image DSProtect encryption differs")
    return {
        "entry": entry,
        "stored": stored,
        "decoded": decoded,
        "analysis": analysis,
        "functions": functions,
        "relocations": relocations,
        "bssVariable": variable,
        "constructors": pointers,
        "fatRange": [first, last],
        "metadataSha256": sha(metadata.encode()),
    }


class Machine:
    def __init__(self, image, bss_size, seed):
        self.engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.engine.mem_map(0x02000000, 0x400000)
        self.engine.mem_map(0x03000000, 0x20000)
        self.engine.mem_map(STOP, 0x1000)
        self.engine.mem_write(BASE, image)
        self.engine.mem_write(BASE + len(image), bytes(bss_size))
        self.random = random.Random(seed)
        self.engine.mem_write(STACK, self.random.randbytes(0x10000))
        self.image_size = len(image)
        self.bss_size = bss_size
        self.steps = 0
        self.reads = set()
        self.writes = []
        self.executed = set()
        self.observe_target = None
        self.entry_snapshot = None
        self.engine.hook_add(UC_HOOK_CODE, self.step)
        self.engine.hook_add(UC_HOOK_MEM_READ, self.read)
        self.engine.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def permitted(self, address, size):
        return any(
            start <= address and address + size <= end
            for start, end in [
                (BASE, BASE + self.image_size + self.bss_size),
                (STACK, STACK + 0x10000),
            ]
        )

    def step(self, engine, address, size, user):
        if not BASE <= address < BASE + self.image_size:
            raise ValueError("Native execution escaped Overlay004")
        self.steps += 1
        self.executed.add(address)
        if address == self.observe_target:
            self.entry_snapshot = bytes(engine.mem_read(address, 12))

    def read(self, engine, access, address, size, value, user):
        if not self.permitted(address, size):
            raise ValueError(
                "Native read escaped own image/BSS or bounded stack: " + hex(address)
            )
        self.reads.add((address, size))

    def write(self, engine, access, address, size, value, user):
        if not self.permitted(address, size):
            raise ValueError(
                "Native write escaped own image/BSS or bounded stack: " + hex(address)
            )
        self.writes.append((address, size))

    def call(self, address, target=None, arguments=()):
        self.engine.reg_write(UC_ARM_REG_CPSR, 0x1F)
        for register in range(UC_ARM_REG_R0, UC_ARM_REG_R0 + 13):
            self.engine.reg_write(register, self.random.getrandbits(32))
        for index, value in enumerate(arguments):
            self.engine.reg_write(UC_ARM_REG_R0 + index, value & 0xFFFFFFFF)
        self.engine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
        self.engine.reg_write(UC_ARM_REG_LR, STOP)
        self.observe_target = target
        self.entry_snapshot = None
        first_steps = self.steps
        first_writes = len(self.writes)
        self.engine.emu_start(address, STOP, count=100000)
        if self.engine.reg_read(UC_ARM_REG_PC) != STOP:
            raise ValueError("Native routine did not return within instruction bound")
        return {
            "entry": hex(address),
            "instructions": self.steps - first_steps,
            "writes": len(self.writes) - first_writes,
            "result": self.engine.reg_read(UC_ARM_REG_R0),
        }

    def image(self):
        return bytes(self.engine.mem_read(BASE, self.image_size))


def runtime(data, seed):
    decoded, analysis = data["decoded"], data["analysis"]
    machine = Machine(decoded, data["entry"][3], seed)
    constructor_results = [
        machine.call(pointer) for pointer in data["constructors"] if pointer
    ]
    initialized = machine.image()
    ranges = []
    for function in data["functions"]:
        start = function["address"] - BASE
        size = function["codeBytes"] + (function["poolBytes"] or 0)
        observed = initialized[start : start + size]
        plain = analysis[start : start + size]
        cold = decoded[start : start + size]
        if function["kind"] == "unkeyed" and observed != plain:
            raise ValueError("Unkeyed function did not decode to extracted analysis")
        if function["kind"] == "keyed" and observed != cold:
            raise ValueError(
                "Keyed function changed during primary constructor sequence"
            )
        ranges.append(
            {
                "address": hex(function["address"]),
                "kind": function["kind"],
                "codeBytes": function["codeBytes"],
                "poolBytes": function["poolBytes"],
                "runtimeEqualsAnalysis": observed == plain,
                "runtimeEqualsCold": observed == cold,
                "runtimeSha256": sha(observed),
            }
        )
    keyed_results = []
    for wrapper, target, expected in [
        (0x021D8920, 0x021D8908, 0xAA65),
        (0x021D895C, 0x021D8914, 0xA99F),
    ]:
        offset = target - BASE
        for iteration in range(2):
            before = machine.image()[offset : offset + 12]
            result = machine.call(wrapper, target)
            after = machine.image()[offset : offset + 12]
            if (
                result["result"] != expected
                or machine.entry_snapshot != analysis[offset : offset + 12]
                or after[:8] == analysis[offset : offset + 8]
                or after[8:] != analysis[offset + 8 : offset + 12]
                or after == before
            ):
                raise ValueError(
                    "Native keyed on-demand decode/reencrypt result differs"
                )
            keyed_results.append(
                {
                    **result,
                    "target": hex(target),
                    "iteration": iteration,
                    "targetEntryFullSpanEqualsAnalysis": True,
                    "beforeEqualsAnalysis": before == analysis[offset : offset + 12],
                    "afterEqualsAnalysis": False,
                    "afterEqualsOriginalCiphertext": after
                    == decoded[offset : offset + 12],
                    "postReturnFullSpanSha256": sha(after),
                    "reencryptedAfterReturn": True,
                    "reencryptedCiphertextDiffersFromPrevious": after != before,
                    "literalPoolUnchanged": after[8:]
                    == analysis[offset + 8 : offset + 12],
                }
            )
    return {
        "seed": seed,
        "constructors": constructor_results,
        "constructorInstructions": sum(
            item["instructions"] for item in constructor_results
        ),
        "constructorInitializedSha256": sha(initialized),
        "constructorChangedBytesFromCold": sum(
            a != b for a, b in zip(initialized, decoded)
        ),
        "constructorChangedBytesFromAnalysis": sum(
            a != b for a, b in zip(initialized, analysis)
        ),
        "ranges": ranges,
        "keyedOnDemand": keyed_results,
        "totalInstructions": machine.steps,
        "uniqueExecutedInstructionAddresses": len(machine.executed),
        "uniqueReadSpans": len(machine.reads),
        "writes": len(machine.writes),
        "finalInitializedSha256": sha(machine.image()),
        "substitutedNativeCallees": 0,
        "memoryAccessesRestrictedToOwnImageBssAndStack": True,
    }


def save(report):
    raw = json.dumps(report, indent=2).encode()
    folder = ROOT / "evidence/validation"
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / ("overlay004-runtime-views-" + sha(raw)[:12] + ".json")
    if target.exists() and target.read_bytes() != raw:
        raise ValueError("Immutable report collision")
    target.write_bytes(raw)
    temporary = folder / "overlay004-runtime-views.json.tmp"
    temporary.write_bytes(raw)
    os.replace(temporary, folder / "overlay004-runtime-views.json")
    return target


def main():
    data = inputs()
    runs = [runtime(data, seed) for seed in [0, 1, 0x004128, 0xFFFFFFFF]]
    if len({item["constructorInitializedSha256"] for item in runs}) != 1:
        raise ValueError(
            "Constructor image depends on randomized caller registers/stack"
        )
    counts = {
        kind: sum(f["kind"] == kind for f in data["functions"])
        for kind in ["keyed", "unkeyed", "none"]
    }
    if counts != {"keyed": 17, "unkeyed": 27, "none": 5}:
        raise ValueError("Protection inventory differs")
    report = {
        "schemaVersion": 1,
        "date": "2026-10-27",
        "kind": "overlay004-dsprotect128-native-runtime-view-audit",
        "romSha256": ROM_HASH,
        "module": "ov004",
        "loadAddress": hex(BASE),
        "source": Path(__file__).name,
        "sourceSha256": sha(Path(__file__).read_bytes()),
        "transformSourceSha256": sha((ROOT / "dsprot128.py").read_bytes()),
        "metadataSha256": data["metadataSha256"],
        "stored": {
            "bytes": len(data["stored"]),
            "sha256": sha(data["stored"]),
            "fatRange": data["fatRange"],
        },
        "decodedCiphertext": {
            "bytes": len(data["decoded"]),
            "sha256": sha(data["decoded"]),
        },
        "analysisPlaintext": {
            "bytes": len(data["analysis"]),
            "sha256": sha(data["analysis"]),
        },
        "fullImageIndependentDecryptionExact": True,
        "fullImageIndependentEncryptionExact": True,
        "dsprotectVersion": "1.28",
        "cipherAlgorithm": "V4 reverse-KSA modified RC4 for keyed functions, rolling XOR for unkeyed functions, branch/addend transform; instruction prefixes only",
        "upstream": {
            "repository": "https://github.com/AetiasHax/ds-rom",
            "crate": "https://static.crates.io/crates/ds-rom/ds-rom-0.8.0.crate",
            "crateSha256": "1198474d0a87563e36273f87278d1fddf595e88f8c4c5fe4c51ca28e264409e1",
            "version": "0.8.0",
            "pinnedBy": "tools/ds-decomp-source/Cargo.lock",
        },
        "protectionFunctionCounts": counts,
        "encodedRelocations": len(data["relocations"]),
        "encodedRelocationsSha256": sha(
            json.dumps(data["relocations"], sort_keys=True).encode()
        ),
        "bssVariable": hex(data["bssVariable"]),
        "constructorEntries": [hex(p) for p in data["constructors"]],
        "runs": runs,
        "constructorImageIndependentOfRandomCallerState": True,
        "postReturnCiphertextVariesAcrossCallerStates": len(
            {item["finalInitializedSha256"] for item in runs}
        )
        > 1,
        "ordinarySourceLinkingRequirements": [
            "Compile ordinary C against the extracted analysis plaintext and prove complete function spans including genuine pools and declared relocations.",
            "Preserve metadata-declared encoded relocation addends in the analysis representation; do not normalize them as ordinary runtime pointers.",
            "Encrypt metadata instruction prefixes after analysis-view source linking and before backward-LZ packing; verify full stored ROM separately.",
            "Keep compiler-generated ordinary logic distinct from native protection stubs, encoded metadata tables, or unrecovered instructions; the latter receive no ordinary-source credit.",
            "Start native loader tests from decompressed ciphertext; running primary decryptors over extracted plaintext double-decrypts the image.",
        ],
        "limitations": [
            "Bounded Unicorn System-mode execution models constructors and two keyed wrappers, not full hardware/OS overlay loading or CP15 cache behavior.",
            "The other fifteen keyed functions are independently decrypted by the matching full-image transform but were not invoked in this runtime audit.",
            "Both keyed routines tested here re-encrypt their instruction prefixes after return with changing ciphertext; their literal pools remain unchanged. Other keyed routines were not invoked.",
        ],
        "acceptedSourceFunctions": 0,
        "acceptedSourceBytes": 0,
        "protectedDataCreditedAsSource": False,
        "passed": True,
    }
    target = save(report)
    print(
        json.dumps(
            {
                "report": str(target.relative_to(ROOT)),
                "counts": counts,
                "runs": len(runs),
                "instructions": sum(r["totalInstructions"] for r in runs),
                "passed": True,
            }
        )
    )


if __name__ == "__main__":
    main()
