import json
import struct
from pathlib import Path
import utility_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "evidence/utility/entry-seeds.json"


def derive():
    layout, files = utility_runtime.derive()
    modules = {module["id"]: module for module in layout["modules"]}
    main = modules["utility-child-arm9-main"]
    itcm = modules["utility-child-arm9-itcm"]
    dtcm = modules["utility-child-arm9-dtcm"]
    binary = files[ROOT / main["binary"]]
    seeds = {}
    def add(module, target, evidence):
        key = (module, target & ~1)
        if key not in seeds:
            seeds[key] = {"module": module, "program": utility_runtime.PROGRAM, "processor": modules[module]["processor"],
                          "address": hex(target & ~1), "mode": "thumb" if target & 1 else "arm", "evidence": []}
        seeds[key]["evidence"].append(evidence)
    for index, target in enumerate(struct.unpack("<24I", files[ROOT / dtcm["binary"]])):
        if not target:
            continue
        if not target & 1 or not int(main["base"], 0) <= target & ~1 < int(main["runtimeEnd"], 0):
            raise ValueError("Utility IRQ table target changed mode or module")
        add(main["id"], target, {"kind": "IRQ-dispatch-table-pointer", "module": dtcm["id"], "offset": index * 4,
                                 "inputSha256": dtcm["sha256"], "instructionEvidence": "Native ARM IRQ dispatcher loads this table and transfers through BX r0"})
    irq = files[ROOT / itcm["binary"]]
    if struct.unpack_from("<I", irq, 0x48)[0] != 0xE59FE004 or struct.unpack_from("<I", irq, 0x54)[0] != 0x01FF8058:
        raise ValueError("Utility IRQ continuation literal changed")
    add(itcm["id"], 0x01FF8058, {"kind": "IRQ-link-register-continuation", "instructionAddress": "0x01ff8048",
                                 "literalAddress": "0x01ff8054", "inputSha256": itcm["sha256"]})
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    for call, target in [(0x0200AA28, 0x01FF81F0), (0x0200AA84, 0x01FF81F0), (0x0200AAE8, 0x01FF81B4), (0x0200AE64, 0x01FF8238)]:
        offset = call - int(main["base"], 0)
        instruction = next(decoder.disasm(binary[offset:offset + 4], call))
        if instruction.mnemonic != "bl" or instruction.op_str != f"#0x{target:x}":
            raise ValueError("Utility measured same-mode Thumb call changed")
        add(itcm["id"], target | 1, {"kind": "same-mode-Thumb-BL", "module": main["id"], "address": hex(call),
                                   "bytes": instruction.bytes.hex(), "inputSha256": main["sha256"]})
    import utility_bridges
    for bridge in utility_bridges.derive()["bridges"]:
        add(bridge["targetModule"], int(bridge["targetAddress"], 0),
            {"kind": "measured-Thumb-to-ARM-linkage-target", "linkageId": bridge["id"],
             "module": bridge["module"], "address": bridge["address"], "bridgeSha256": bridge["sha256"],
             "inputSha256": bridge["inputModuleSha256"]})
    return {"schemaVersion": 1, "program": utility_runtime.PROGRAM, "romSha256": utility_runtime.audit_regions.ROM_HASH,
            "entrySeeds": list(seeds.values()), "sourceReconstructionComplete": False,
            "limitations": ["Pointer and direct-call mode evidence establishes analysis entry modes, not complete function boundaries or source matches"]}


def main():
    report = derive()
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print({"qualifiedEntries": len(report["entrySeeds"])})


if __name__ == "__main__":
    main()
