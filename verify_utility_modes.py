import json
from pathlib import Path
import utility_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent


def main():
    layout, files = utility_runtime.derive()
    module = next(module for module in layout["modules"] if module["id"] == "utility-child-arm9-main")
    binary = bytes(files[ROOT / module["binary"]])
    source_report = ROOT / "evidence/matches/utility-manual02.json"
    entry = json.loads(source_report.read_text())["matches"][0]
    first, last = 0x0200AB14, 0x0200AB2C
    native = binary[first - 0x02000000:last - 0x02000000]
    if entry["program"] != utility_runtime.PROGRAM or entry["module"] != module["id"] or entry["processor"] != "arm9" or entry["mode"] != "arm" or int(entry["address"], 0) != first or entry["bytes"] != last - first or entry["targetSha256"] != utility_runtime.sha(native):
        raise ValueError("Utility mode reconciliation source span changed")
    if any(utility_runtime.sha((ROOT / entry[key]).read_bytes()) != entry[key + "Sha256"] for key in ("source", "object")):
        raise ValueError("Utility ARM source/object provenance changed")
    with (ROOT / entry["object"]).open("rb") as stream:
        elf = ELFFile(stream)
        symbols = list(elf.get_section_by_name(".symtab").iter_symbols())
        symbol = next(symbol for symbol in symbols if symbol.name == entry["name"])
        mappings = [{"name": marker.name, "offset": marker["st_value"]} for marker in symbols if marker["st_shndx"] == symbol["st_shndx"] and marker.name in ("$a", "$t", "$d")]
        if mappings != [{"name": "$a", "offset": 0}] or elf.get_section(symbol["st_shndx"]).data() != native:
            raise ValueError("Compiled utility leaf does not establish the complete native ARM region")
    arm = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    thumb = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    thumb.detail = True
    instructions = list(arm.disasm(native, first))
    fake = next(thumb.disasm(binary[0xAB16:0xAB18], 0x0200AB16))
    if fake.mnemonic != "b" or fake.operands[0].imm != 0x0200B25A or any(instruction.address == fake.address for instruction in instructions):
        raise ValueError("Rejected mode-conflict edge no longer describes the measured bytes")
    census_path = ROOT / "evidence/utility/runtime-functions.json"
    census = json.loads(census_path.read_text())
    enclosing = [function for function in census["functions"] if function["processor"] == "arm9" and function["module"] == module["id"] and
                 any(int(begin, 0) <= fake.address < int(end, 0) for begin, end in function["bodyRanges"])]
    if len(enclosing) != 1 or enclosing[0]["mode"] != "arm" or int(enclosing[0]["address"], 0) != first:
        raise ValueError("Qualified analysis census conflicts with the exact ARM source span")
    join = next(thumb.disasm(binary[0xB25A:0xB25E], 0x0200B25A))
    if join.mnemonic != "blx" or join.operands[0].imm != 0x0200A660:
        raise ValueError("Accepted destination interior join changed")
    report = {"schemaVersion": 1, "romSha256": layout["romSha256"], "program": utility_runtime.PROGRAM,
              "processor": "arm9", "module": module["id"], "inputModuleSha256": module["sha256"],
              "qualifiedArmSpan": {"address": hex(first), "bytes": len(native), "sha256": utility_runtime.sha(native),
                                   "sourceReport": source_report.relative_to(ROOT).as_posix(), "source": entry["source"], "sourceSha256": entry["sourceSha256"],
                                   "object": entry["object"], "objectSha256": entry["objectSha256"], "mappingSymbols": mappings,
                                   "instructions": [{"address": hex(instruction.address), "bytes": instruction.size, "instruction": instruction.mnemonic + " " + instruction.op_str} for instruction in instructions]},
              "rejectedEdge": {"address": hex(fake.address), "wrongMode": "thumb", "decodedInstruction": fake.mnemonic + " " + fake.op_str,
                               "target": "0x0200b25a", "reason": "Source address is the second halfword of the exact ARM MOV at0200ab14, not an ARM9 instruction boundary"},
              "destination": {"address": "0x0200b22c", "report": "evidence/matches/utility-translated15.json", "interiorJoin": "0x0200b25a", "instruction": join.mnemonic + " " + join.op_str,
                              "classification": "Internal Thumb CFG join within the accepted complete C function"},
              "analysisEvidence": {"path": census_path.relative_to(ROOT).as_posix(), "sha256": utility_runtime.sha(census_path.read_bytes()), "enclosingFunctions": enclosing},
              "conclusion": "Conflicting Thumb decoding of an original ARM gap created a false cross-function edge; real compiled ARM mapping must resolve it without blanket mode overrides",
              "reproduce": ["python", "verify_utility_modes.py"], "wholeModuleLinked": False, "sourceReconstructionComplete": False}
    (ROOT / "evidence/utility/mode-reconciliation-ab14.json").write_text(json.dumps(report, indent=2) + "\n")
    print({"exactArmBytes": len(native), "rejectedInteriorEdges": 1, "nativeSourceChanged": False})


if __name__ == "__main__":
    main()
