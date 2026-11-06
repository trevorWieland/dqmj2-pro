import json
import os
import re
import struct
import subprocess
from pathlib import Path
import utility_runtime
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/lowlevel-recovery/utility-data"
COMPILER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
COMPILER_HASH = "7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880"


def compile_source(source, processor):
    flags = ["-O2", "-proc", "arm946e" if processor == "arm9" else "arm7tdmi", "-sym", "on", "-nolink", "-c"]
    output = WORK / (source.stem + ".o")
    command = [str(COMPILER), *flags, str(source), "-o", str(output)]
    result = subprocess.run(command, cwd=ROOT, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat")),
                            capture_output=True, text=True, timeout=30)
    attempt = {"command": command, "exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    if result.returncode:
        raise ValueError("Utility typed storage compilation failed: " + str(attempt))
    digest = utility_runtime.sha(output.read_bytes())
    stable = WORK / "objects" / (digest + ".o")
    stable.parent.mkdir(parents=True, exist_ok=True)
    if not stable.exists():
        stable.write_bytes(output.read_bytes())
    return stable, flags, attempt


def match(source, obj, flags, module, symbol_name, bindings):
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        symbols = elf.get_section_by_name(".symtab")
        symbol = next(symbol for symbol in symbols.iter_symbols() if symbol.name == symbol_name)
        section = elf.get_section(symbol["st_shndx"])
        at, size = symbol["st_value"], symbol["st_size"]
        bss = section["sh_type"] == "SHT_NOBITS"
        address = int(module["bssStart"] if bss else module["base"], 0)
        expected = module["bssBytes"] if bss else module["bytes"]
        if size != expected:
            raise ValueError("Utility typed storage allocation has the wrong size")
        output = bytearray(size) if bss else bytearray(section.data()[at:at + size])
        relocations = []
        for reloc in elf.iter_sections():
            if reloc["sh_type"] != "SHT_RELA" or reloc["sh_info"] != symbol["st_shndx"]:
                continue
            table = elf.get_section(reloc["sh_link"])
            for item in reloc.iter_relocations():
                offset = item["r_offset"] - at
                if not 0 <= offset < size:
                    continue
                name = table.get_symbol(item["r_info_sym"]).name
                if item["r_info_type"] != 2 or name not in bindings:
                    raise ValueError("Utility data has an undeclared relocation")
                target = int(bindings[name], 0)
                struct.pack_into("<I", output, offset, (target + item["r_addend"]) & 0xFFFFFFFF)
                relocations.append({"offset": offset, "type": 2, "symbol": name, "target": hex(target), "addend": item["r_addend"]})
    native = bytes(size) if bss else (ROOT / module["binary"]).read_bytes()
    if output != native:
        raise ValueError("Utility initialized data differs after declared relocations")
    return {"name": symbol_name, "symbol": symbol_name, "nativeAlias": "data_" + module["id"].replace("-", "_") + f"_{address:08x}",
            "program": utility_runtime.PROGRAM, "processor": module["processor"], "module": module["id"], "address": hex(address),
            "kind": "bss" if bss else "data", "bytes": size, "size": size, "compiledBytes": size,
            "initializedBytes": 0 if bss else size, "allocatedZeroFillBytes": size if bss else 0,
            "source": source.relative_to(ROOT).as_posix(), "sourceSha256": utility_runtime.sha(source.read_bytes()),
            "object": obj.relative_to(ROOT).as_posix(), "objectSha256": utility_runtime.sha(obj.read_bytes()),
            "compiler": COMPILER.relative_to(ROOT).as_posix(), "compilerSha256": COMPILER_HASH, "compilerFlags": flags,
            "section": section.name, "sectionType": section["sh_type"], "sectionFlags": section["sh_flags"],
            "sectionIndex": symbol["st_shndx"], "sectionOffset": at, "relocations": relocations,
            "targetSha256": utility_runtime.sha(native), "outputSha256": utility_runtime.sha(output),
            "inputModuleSha256": module["sha256"], "exactAfterDeclaredRelocation": True,
            "allocationProof": "Measured embedded native loader module parameters and copy/zero descriptors" if bss else "Native IRQ dispatcher indexes the 24-entry DTCM function-pointer table",
            "linked": False, "runtimeProof": False}


def main():
    layout, files = utility_runtime.derive()
    if json.loads(utility_runtime.OUTPUT.read_text()) != layout or any(path.read_bytes() != data for path, data in files.items()):
        raise ValueError("Utility storage input layout is stale")
    if utility_runtime.sha(COMPILER.read_bytes()) != COMPILER_HASH:
        raise ValueError("Utility storage compiler identity changed")
    modules = {module["id"]: module for module in layout["modules"]}
    directory = ROOT / "src/utility/storage"
    source = directory / "arm9_irq_table.c"
    names = re.findall(r"extern void (native_utility_child_arm9_handler_[0-9a-f]{8})\(void\);", source.read_text())
    bindings = {name: hex(int(name.rsplit("_", 1)[-1], 16)) for name in names}
    WORK.mkdir(parents=True, exist_ok=True)
    entries, attempts = [], []
    for filename, processor, symbols in [
        ("arm9_irq_table.c", "arm9", [("utility-child-arm9-dtcm", "native_utility_child_arm9_dtcm_027e0000")]),
        ("arm9_storage.c", "arm9", [("utility-child-arm9-main", "native_utility_child_arm9_main_bss_02022620"),
                                    ("utility-child-arm9-dtcm", "native_utility_child_arm9_dtcm_bss_027e0060")]),
        ("arm7_storage.c", "arm7", [("utility-child-arm7-wram", "native_utility_child_arm7_wram_bss_03805944"),
                                    ("utility-child-arm7-main", "native_utility_child_arm7_main_bss_027f84f0")])]:
        source = directory / filename
        obj, flags, attempt = compile_source(source, processor)
        attempts.append(attempt)
        entries.extend(match(source, obj, flags, modules[module], symbol, bindings) for module, symbol in symbols)
    report = {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM,
              "runtimeMappingCanonical": True, "dataMatches": entries, "nativeSymbols": bindings,
              "nativeSymbolBindings": [{"name": name, "program": utility_runtime.PROGRAM, "processor": "arm9",
                                        "module": "utility-child-arm9-main", "address": value, "mode": "thumb"} for name, value in bindings.items()],
              "dataMatchedBytes": sum(entry["initializedBytes"] for entry in entries),
              "bssMatchedBytes": sum(entry["allocatedZeroFillBytes"] for entry in entries), "functionMatched": 0,
              "wholeModuleLinked": False, "sourceReconstructionComplete": False, "attempts": attempts,
              "limitations": ["The IRQ callback ABI and byte-storage types remain structural descriptions, not recovered application-level types",
                              "All handler bindings are qualified to the embedded ARM9 program and retain Thumb pointer bits",
                              "BSS is allocated memory only and contributes no initialized ROM or function-byte credit",
                              "Whole-module linked bytes and embedded-image recomposition are validated independently"]}
    output = ROOT / "evidence/data/utility.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print({"initializedDataBytes": report["dataMatchedBytes"], "allocatedBssBytes": report["bssMatchedBytes"], "entries": len(entries)})


if __name__ == "__main__":
    main()
