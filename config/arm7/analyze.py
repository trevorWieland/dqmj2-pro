import hashlib
import json
import os
import re
import struct
import subprocess
import sys
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "deps/native"))
import capstone
from capstone.arm import ARM_CC_AL, ARM_OP_IMM

OUT = ROOT / "evidence/arm7"
WORK = ROOT / "build/link-work/arm7"
INPUT_HASH = "9f40087972ccb8b89d4cc4baf8288123e26a479bb43fa68b18a30a59650633a1"
LINKER_HASH = "bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def config():
    metadata = (ROOT / "extract/arm7/arm7.yaml").read_text()
    value = lambda key: int(re.search(rf"^{key}: (\d+)$", metadata, re.M).group(1))
    return {
        "schemaVersion": 1, "processor": "ARM7TDMI", "architecture": "ARMv4T",
        "module": "arm7", "baseAddress": value("base_address"),
        "entryAddress": value("entry_function"), "entryMode": "arm",
        "input": "extract/arm7/arm7.bin", "analysis": "heuristic-capstone-control-flow",
        "dsdSupport": "unsupported-by-pinned-0.12.1-init",
        "dsdEvidence": "tools/ds-decomp-source/cli/src/cmd/init.rs",
        "unknowns": ["function boundaries", "indirect control flow", "code/data boundaries",
                     "literal pool mapping", "all relocations", "compiler identity"]
    }


def analyze(data, spec):
    base, end = spec["baseAddress"], spec["baseAddress"] + len(data)
    engines = {"arm": capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM),
               "thumb": capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_THUMB)}
    for engine in engines.values():
        engine.detail = True
    seeds = {(spec["entryAddress"], "arm"): {"header-entry"}}
    for offset in range(0, len(data) - 4, 4):
        word = struct.unpack_from("<I", data, offset)[0]
        if word & 0xFFFF0000 == 0xE92D0000 and word & 0x4000:
            seeds.setdefault((base + offset, "arm"), set()).add("unverified-stack-prologue")
    for offset in range(0, len(data) - 2, 2):
        half = struct.unpack_from("<H", data, offset)[0]
        if half & 0xFF00 == 0xB500:
            seeds.setdefault((base + offset, "thumb"), set()).add("unverified-stack-prologue")
    queue = deque(seeds)
    visited, instructions, edges, failures = set(), [], [], []
    coverage = bytearray(len(data))
    while queue:
        address, mode = queue.popleft()
        if (address, mode) in visited or not base <= address < end:
            continue
        visited.add((address, mode))
        decoded = list(engines[mode].disasm(data[address - base:address - base + 4], address, count=1))
        if not decoded:
            failures.append({"address": hex(address), "mode": mode, "reason": "undecodable"})
            continue
        ins = decoded[0]
        instructions.append({"address": address, "mode": mode, "size": ins.size,
                             "bytes": bytes(ins.bytes).hex(), "mnemonic": ins.mnemonic,
                             "operands": ins.op_str})
        for index in range(address - base, min(address - base + ins.size, len(data))):
            coverage[index] |= 1 if mode == "arm" else 2
        branch = ins.group(capstone.CS_GRP_JUMP) or ins.group(capstone.CS_GRP_CALL)
        call = ins.group(capstone.CS_GRP_CALL)
        conditional = ins.cc not in (ARM_CC_AL, 0)
        next_address = address + ins.size
        terminal = ins.group(capstone.CS_GRP_RET) or ins.mnemonic in ("bx", "pop", "ldm", "ldmib", "ldmda", "ldmdb") and "pc" in ins.op_str
        if branch:
            immediates = [op.imm for op in ins.operands if op.type == ARM_OP_IMM]
            target_mode = ("thumb" if mode == "arm" else "arm") if ins.mnemonic.startswith("blx") else mode
            target = immediates[0] & ~1 if immediates else None
            edges.append({"from": hex(address), "mode": mode, "to": hex(target) if target is not None else None,
                          "targetMode": target_mode, "call": call,
                          "resolved": target is not None and base <= target < end})
            if target is not None and base <= target < end:
                queue.append((target, target_mode))
                if call:
                    seeds.setdefault((target, target_mode), set()).add("direct-call-target")
            if not call and not conditional:
                continue
        if not terminal or conditional:
            if "pc" not in ins.op_str.split(",")[0] or conditional:
                queue.append((next_address, mode))
    instructions.sort(key=lambda item: (item["address"], item["mode"]))
    functions = [{"module": "arm7", "processor": "ARM7TDMI", "address": hex(address),
                  "mode": mode, "size": None, "status": "candidate", "evidence": sorted(reasons),
                  "boundaryVerified": False}
                 for (address, mode), reasons in sorted(seeds.items())]
    return {"functions": functions, "instructions": instructions, "edges": edges, "decodeFailures": failures,
            "coveredBytes": sum(bool(value) for value in coverage),
            "ambiguousArmThumbBytes": sum(value == 3 for value in coverage)}


def object_blob(data, path):
    section_names = b"\0.text\0.symtab\0.strtab\0.shstrtab\0"
    strings = b"\0Arm7Entry\0"
    symbols = bytes(16) + struct.pack("<IIIBBH", 0, 0, 0, 3, 0, 1)
    symbols += struct.pack("<IIIBBH", 1, 0, 0, 0x12, 0, 1)
    content = bytearray(bytes(52))
    sections = [bytes(40)]
    items = [(1, 1, 6, data, 0, 0, 4, 0), (7, 2, 0, symbols, 3, 2, 4, 16),
             (15, 3, 0, strings, 0, 0, 1, 0), (23, 3, 0, section_names, 0, 0, 1, 0)]
    for name, kind, flags, payload, link, info, alignment, entry_size in items:
        content.extend(bytes((-len(content)) % alignment))
        offset = len(content)
        content.extend(payload)
        sections.append(struct.pack("<IIIIIIIIII", name, kind, flags, 0, offset,
                                    len(payload), link, info, alignment, entry_size))
    content.extend(bytes((-len(content)) % 4))
    section_offset = len(content)
    content.extend(b"".join(sections))
    content[:52] = struct.pack("<16sHHIIIIIHHHHHH", b"\x7fELF\x01\x01\x01" + bytes(9),
                               1, 40, 1, 0, 0, section_offset, 0x05000000,
                               52, 0, 0, 40, len(sections), 4)
    path.write_bytes(content)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    spec = config()
    (ROOT / "config/arm7/config.json").write_text(json.dumps(spec, indent=2) + "\n")
    data = (ROOT / spec["input"]).read_bytes()
    if len(data) != 160048 or digest(data) != INPUT_HASH:
        raise ValueError("ARM7 input differs from measured build")
    report = analyze(data, spec)
    for key in ("functions", "instructions", "edges", "decodeFailures"):
        (OUT / f"{key}.json").write_text(json.dumps(report[key], indent=2) + "\n")
    lines = [f'{item["address"]:08x} {item["mode"]:5s} {item["bytes"]:8s} {item["mnemonic"]} {item["operands"]}'
             for item in report["instructions"]]
    (OUT / "disassembly.txt").write_text("\n".join(lines) + "\n")
    blob = WORK / "original-blob.o"
    object_blob(data, blob)
    lcf = WORK / "arm7.lcf"
    lcf.write_text(
        f'MEMORY {{ ARM7 : ORIGIN = {spec["baseAddress"]:#x} > arm7.bin }}\n'
        'SECTIONS { .arm7 : { ALIGNALL(4); original-blob.o(.text) } > ARM7 }\n'
    )
    project = json.loads((ROOT / "project.json").read_text())
    linker = ROOT / project["linker"]
    if digest(linker.read_bytes()) != LINKER_HASH:
        raise ValueError("ARM7 linker differs from pinned executable")
    env = os.environ.copy()
    env["LM_LICENSE_FILE"] = str(ROOT / project["license"])
    command = [str(linker), "-nostdlib", "-nodeadstrip", "-proc", "arm7tdmi", "-main", "Arm7Entry",
               str(lcf), str(blob), "-o", str(WORK / "arm7.elf")]
    result = subprocess.run(command, cwd=WORK, env=env, capture_output=True, text=True, timeout=60)
    output = WORK / "arm7.bin"
    summary = {"schemaVersion": 1, "createdUtc": datetime.now(timezone.utc).isoformat(),
               **spec, "inputBytes": len(data), "inputSha256": digest(data),
               "capstoneImportedVersion": capstone.__version__,
               "capstoneDlls": [{"path": str(p), "sha256": digest(p.read_bytes())}
                                 for p in (ROOT / "deps/native/capstone").rglob("*.dll")],
               "candidateFunctions": len(report["functions"]), "decodedInstructions": len(lines),
               "coveredBytes": report["coveredBytes"], "ambiguousArmThumbBytes": report["ambiguousArmThumbBytes"],
               "unknownBytes": len(data) - report["coveredBytes"],
               "architectureInstructionValidation": "Capstone decoding does not establish ARMv4T instruction validity",
               "unresolvedControlFlowEdges": sum(not item["resolved"] for item in report["edges"]),
               "decodeFailureCount": len(report["decodeFailures"]),
               "objectKind": "unrelocated-original-whole-module-blob", "relocationRecovery": False,
               "sourceReconstruction": False, "scaffoldingObjectSha256": digest(blob.read_bytes()),
               "linkerSha256": digest(linker.read_bytes()),
               "command": {"argv": command, "cwd": str(WORK), "exitCode": result.returncode,
                           "stdout": result.stdout, "stderr": result.stderr},
               "linkedOriginalBlobExact": output.exists() and output.read_bytes() == data,
               "linkedSha256": digest(output.read_bytes()) if output.exists() else None}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({key: summary[key] for key in ("candidateFunctions", "decodedInstructions", "coveredBytes",
                                                    "ambiguousArmThumbBytes", "linkedOriginalBlobExact")}))
    return 0 if summary["linkedOriginalBlobExact"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
