import json
import struct
from pathlib import Path
import utility_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_JUMP, CS_GRP_CALL
from capstone.arm import ARM_OP_MEM, ARM_REG_PC

ROOT = Path(__file__).resolve().parent


def main():
    layout, files = utility_runtime.derive()
    module = next(module for module in layout["modules"] if module["id"] == "utility-child-arm9-itcm")
    binary = bytes(files[ROOT / module["binary"]])
    base = int(module["base"], 0)
    spans, evidence = [], []
    for name in ("utility-hardware01", "utility-dma01", "utility-hardware02"):
        path = ROOT / f"evidence/matches/{name}.json"
        report = json.loads(path.read_text())
        for entry in report["matches"]:
            if entry["program"] != utility_runtime.PROGRAM or entry["module"] != module["id"] or not entry["exactAfterDeclaredRelocation"]:
                raise ValueError("Utility ITCM padding proof has an unqualified source span")
            if utility_runtime.sha((ROOT / entry["source"]).read_bytes()) != entry["sourceSha256"] or utility_runtime.sha((ROOT / entry["object"]).read_bytes()) != entry["objectSha256"]:
                raise ValueError("Utility ITCM padding proof has stale source/object evidence")
            first, size = int(entry["address"], 0), entry["bytes"]
            target = binary[first - base:first - base + size]
            if utility_runtime.sha(target) != entry["targetSha256"]:
                raise ValueError("Utility ITCM target span hash changed")
            spans.append((first, first + size))
            evidence.append({"report": path.relative_to(ROOT).as_posix(), "name": entry["name"], "address": hex(first), "bytes": size})
    cursor = base
    for first, last in sorted(spans):
        if first != cursor:
            raise ValueError("Utility ITCM recovered spans overlap or leave a pre-tail hole")
        cursor = last
    first, last = cursor, base + len(binary)
    tail = binary[first - base:]
    if len(tail) != 24 or any(tail) or ((first + 31) & ~31) != last:
        raise ValueError("Utility ITCM zero tail is not the measured 32-byte extent alignment")
    thumb = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    terminal = next(thumb.disasm(binary[0x260:0x262], 0x01FF8260))
    if terminal.mnemonic != "bx" or terminal.op_str != "r3" or binary[0x262:0x264] != b"\xc0\x46" or struct.unpack_from("<I", binary, 0x264)[0] != 0x040000B0:
        raise ValueError("Utility ITCM final return/NOP/literal boundary changed")
    references, inspected = [], 0
    inventory_path = ROOT / "evidence/utility/runtime-functions.json"
    census = json.loads(inventory_path.read_text())
    if census["program"] != utility_runtime.PROGRAM or census["romSha256"] != layout["romSha256"]:
        raise ValueError("Utility padding reference census has a different program/build namespace")
    inventory = {"functions": [{**function, "ranges": function["bodyRanges"]} for function in census["functions"] if function["processor"] == "arm9"]}
    modules = {item["id"]: item for item in layout["modules"]}
    for function in inventory["functions"]:
        source_module = modules[function["module"]]
        payload = bytes(files[ROOT / source_module["binary"]])
        source_base = int(source_module["base"], 0)
        decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if function["mode"] == "thumb" else CS_MODE_ARM)
        decoder.detail = True
        for begin, end in function["ranges"]:
            begin, end = int(begin, 0), int(end, 0)
            for instruction in decoder.disasm(payload[begin - source_base:end - source_base], begin):
                inspected += 1
                if (instruction.group(CS_GRP_JUMP) or instruction.group(CS_GRP_CALL)) and instruction.operands and instruction.operands[0].type == 2:
                    target = instruction.operands[0].imm & ~1
                    if first <= target < last:
                        references.append({"kind": "direct-control-flow", "module": function["module"], "address": hex(instruction.address), "target": hex(target)})
                for operand in instruction.operands:
                    if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC:
                        target = ((instruction.address + 4) & ~3 if function["mode"] == "thumb" else instruction.address + 8) + operand.mem.disp
                        if first <= target < last:
                            references.append({"kind": "PC-relative-data", "module": function["module"], "address": hex(instruction.address), "target": hex(target)})
    pointer_windows = 0
    for source_module in layout["modules"]:
        if source_module["processor"] != "arm9":
            continue
        payload = bytes(files[ROOT / source_module["binary"]])
        for offset in range(len(payload) - 3):
            target = struct.unpack_from("<I", payload, offset)[0]
            pointer_windows += 1
            if first <= target & ~1 < last:
                references.append({"kind": "stored-address-window", "module": source_module["id"], "offset": offset, "value": hex(target)})
    candidate_entries = [function for function in inventory["functions"] if function["module"] == module["id"] and first <= int(function["address"], 0) < last]
    main_module = modules["utility-child-arm9-main"]
    main_binary = bytes(files[ROOT / main_module["binary"]])
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cache_steps = []
    for offset in (0xA9C, 0xAAC):
        instruction = next(decoder.disasm(main_binary[offset:offset + 4], 0x02000000 + offset))
        cache_steps.append({"address": hex(instruction.address), "instruction": instruction.mnemonic + " " + instruction.op_str, "bytes": instruction.bytes.hex()})
    supported = not references and not candidate_entries
    report = {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM,
              "processor": "arm9", "module": module["id"], "inputModuleSha256": module["sha256"],
              "sourceSpanEvidence": evidence, "recoveredContiguousBytes": first - base,
              "tail": {"address": hex(first), "bytes": len(tail), "sha256": utility_runtime.sha(tail), "allZero": True},
              "moduleDescriptorBytes": len(binary), "observedExtentAlignment": 32, "loaderCacheLoop": cache_steps,
              "terminalReturn": {"address": "0x01ff8260", "instruction": terminal.mnemonic + " " + terminal.op_str,
                                 "followingNopBytes": 2, "followingLiteralAddress": "0x01ff8264", "followingLiteralValue": "0x040000b0"},
              "referenceScan": {"candidateInstructionsInspected": inspected, "allByteAlignedStoredAddressWindowsInspected": pointer_windows,
                                "inventory": inventory_path.relative_to(ROOT).as_posix(), "inventorySha256": utility_runtime.sha(inventory_path.read_bytes()),
                                "referencesToTail": references, "candidateEntriesInTail": candidate_entries},
              "supportsDeterministicLinkerZeroAlignment": supported, "historicalOriginalAlignmentDirectiveProven": False,
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "limitations": ["A 32-byte zero alignment rule exactly regenerates the tail and agrees with the measured loader extent/cache step",
                              "No stored pointer, direct branch/call, candidate entry or PC-relative read targets the tail in the scoped decoded embedded ARM9 build",
                              "Computed targets and arbitrary runtime writes are not excluded by a static reference scan; absence of every possible dynamic reference is not proven",
                              "The tail must receive no source credit until an actual source-only link generates its declared extent and fill exactly"]}
    (ROOT / "evidence/utility/itcm-tail.json").write_text(json.dumps(report, indent=2) + "\n")
    print({"initializedSourceSpans": first - base, "zeroTailBytes": len(tail), "references": len(references), "supportsZeroAlignment": supported})


if __name__ == "__main__":
    main()
