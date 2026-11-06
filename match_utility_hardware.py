import json
import os
import re
import struct
import subprocess
from pathlib import Path
import utility_runtime
import match_itcm_hardware
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/lowlevel-recovery/utility-hardware"
ASSEMBLER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwasmarm.exe"
ASSEMBLER_HASH = "e928cbcce71d687fadf25cf426280f23252e2aaae897fc2ce4e5570d8554dc8c"
JUSTIFICATIONS = {
    0x01FF8000: "Native IRQ dispatch reads and acknowledges interrupt MMIO, then tail-dispatches through a callback table with a special LR continuation rather than a conventional C call/return ABI",
    0x01FF8058: "Native IRQ scheduler continuation changes CPSR/SPSR modes, transfers user-bank registers with privileged LDM/STM and restores a different execution context; ordinary C cannot express these hardware operations"
}
SPECS = {0x01FF8000: (88, {0x01FF8050, 0x01FF8054}),
         0x01FF8058: (348, {0x01FF81A4, 0x01FF81A8, 0x01FF81AC, 0x01FF81B0})}


def main():
    layout, files = utility_runtime.derive()
    module = next(module for module in layout["modules"] if module["id"] == "utility-child-arm9-itcm")
    binary = files[ROOT / module["binary"]]
    if utility_runtime.sha(ASSEMBLER.read_bytes()) != ASSEMBLER_HASH:
        raise ValueError("Utility privileged assembler identity changed")
    WORK.mkdir(parents=True, exist_ok=True)
    matches, attempts = [], []
    bindings = {}
    for address, (size, pools) in SPECS.items():
        name = f"native_utility_child_arm9_itcm_hw_{address:08x}"
        source = ROOT / f"src/utility/hardware/{name}.s"
        text = source.read_text()
        measured_pools = {int(location, 16) for location in re.findall(r"local_([0-9a-f]{8}):\s*\.word", text)}
        if measured_pools != pools or any(directive in text for directive in (".byte", ".hword", ".incbin")):
            raise ValueError("Utility privileged source must use mnemonics and only the measured literal pools")
        flags = ["-proc", "arm5TE", "-c"]
        obj = WORK / (name + ".o")
        command = [str(ASSEMBLER), *flags, str(source), "-o", str(obj)]
        process = subprocess.run(command, cwd=ROOT, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat")),
                                 capture_output=True, text=True, timeout=30)
        attempts.append({"command": command, "exitCode": process.returncode, "stdout": process.stdout, "stderr": process.stderr})
        if process.returncode:
            raise ValueError("Utility privileged assembly failed")
        digest = utility_runtime.sha(obj.read_bytes())
        stable = WORK / "objects" / (digest + ".o")
        stable.parent.mkdir(exist_ok=True)
        if not stable.exists():
            stable.write_bytes(obj.read_bytes())
        with obj.open("rb") as stream:
            elf = ELFFile(stream)
            symbol = next(symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols() if symbol.name == name)
            section = elf.get_section(symbol["st_shndx"])
            output = bytearray(section.data())
            relocations = []
            for reloc in elf.iter_sections():
                if reloc["sh_type"] not in ("SHT_REL", "SHT_RELA") or reloc["sh_info"] != symbol["st_shndx"]:
                    continue
                table = elf.get_section(reloc["sh_link"])
                for item in reloc.iter_relocations():
                    external = table.get_symbol(item["r_info_sym"]).name
                    target = int(external.rsplit("_", 1)[-1], 16)
                    at = item["r_offset"]
                    if item["r_info_type"] != 2 or address + at not in pools:
                        raise ValueError("Unexpected relocation in utility privileged assembly")
                    addend = item["r_addend"] if reloc["sh_type"] == "SHT_RELA" else struct.unpack_from("<I", output, at)[0]
                    struct.pack_into("<I", output, at, (target + addend) & 0xFFFFFFFF)
                    relocations.append({"offset": at, "type": 2, "symbol": external, "target": hex(target), "addend": addend})
                    bindings[external] = hex(target)
        native = bytes(binary[address - 0x01FF8000:address - 0x01FF8000 + size])
        if len(output) != size or symbol["st_size"] != size or output != native:
            raise ValueError("Utility privileged reconstruction differs from its complete native span")
        oracle = match_itcm_hardware.irq_oracle(native, bytes(output)) if address == 0x01FF8000 else {
            "supported": False, "reason": "Privileged banked-context and full scheduler state are not executed in the isolated unit model"}
        matches.append({"name": name, "program": utility_runtime.PROGRAM, "module": module["id"], "processor": "arm9", "mode": "arm",
                        "address": hex(address), "bytes": size, "size": size, "compiledBytes": size, "matchingBytes": size,
                        "nativeAlias": f"func_utility_child_arm9_itcm_{address:08x}", "exactAfterDeclaredRelocation": True,
                        "source": source.relative_to(ROOT).as_posix(), "sourceSha256": utility_runtime.sha(source.read_bytes()),
                        "object": stable.relative_to(ROOT).as_posix(), "objectSha256": digest,
                        "compiler": ASSEMBLER.relative_to(ROOT).as_posix(), "compilerSha256": ASSEMBLER_HASH,
                        "assemblerSha256": ASSEMBLER_HASH, "compilerFlags": flags, "relocations": relocations,
                        "sectionIndex": symbol["st_shndx"], "sectionOffset": symbol["st_value"],
                        "inputModuleSha256": module["sha256"], "targetSha256": utility_runtime.sha(native), "outputSha256": utility_runtime.sha(output),
                        "assemblyJustification": JUSTIFICATIONS[address], "oracle": oracle, "linked": False,
                        "boundaryEvidence": "Measured IRQ entry/continuation and following literal pools; next verified native Thumb-call entry begins at 0x01ff81b4"})
    report = {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM,
              "runtimeMappingCanonical": True, "matches": matches, "nativeSymbols": bindings, "attempts": attempts,
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "limitations": ["Assembly is restricted to measured privileged IRQ/controller/context machinery, without normal game-logic fallback",
                              "The second routine's physical scheduler/banked-context behavior remains untested",
                              "All data/call addresses belong to the embedded ARM9 program, never the host game's equal numeric addresses"]}
    (ROOT / "evidence/matches/utility-hardware01.json").write_text(json.dumps(report, indent=2) + "\n")
    print({"functions": len(matches), "nativeSpanBytes": sum(entry["bytes"] for entry in matches)})


if __name__ == "__main__":
    main()
