import hashlib
import json
import os
import re
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "deps/native"))
from elftools.elf.elffile import ELFFile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    work = ROOT / "work/lowlevel-recovery/dtcm"
    work.mkdir(parents=True, exist_ok=True)
    source = ROOT / "src/itcm/dtcm_callbacks.c"
    compiler = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
    if sha(compiler.read_bytes()) != "7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880":
        raise ValueError("Compiler identity differs")
    flags = ["-O2", "-enum", "int", "-char", "signed", "-str", "noreuse", "-proc", "arm946e", "-gccext,on", "-fp", "soft", "-inline", "off", "-Cpp_exceptions", "off", "-RTTI", "off", "-interworking", "-w", "off", "-sym", "on", "-gccinc", "-nolink", "-msgstyle", "gcc"]
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat"))
    obj = work / "callbacks.o"
    command = [str(compiler), *flags, "-c", str(source), "-o", str(obj)]
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=60)
    if result.returncode:
        raise RuntimeError(result.stdout.decode(errors="replace") + result.stderr.decode(errors="replace"))
    object_hash = sha(obj.read_bytes())
    stable = work / (object_hash + ".o")
    if not stable.exists():
        stable.write_bytes(obj.read_bytes())
    native = (ROOT / "extract/arm9/dtcm.bin").read_bytes()
    if sha(native) != "8b37cdd1c1c304deb8c6355aa56411d80adc4a55d29ccf4b7a52e5afd64d75f4":
        raise ValueError("DTCM module differs from measured build")
    relocations = []
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        symbols = {symbol.name: symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols()}
        table = symbols["native_dtcm_027e0000"]
        section = elf.get_section(table["st_shndx"])
        code = bytearray(section.data())
        for relocation_section in elf.iter_sections():
            if relocation_section["sh_type"] != "SHT_RELA" or relocation_section["sh_info"] != table["st_shndx"]:
                continue
            symbol_table = elf.get_section(relocation_section["sh_link"])
            for relocation in relocation_section.iter_relocations():
                target_name = symbol_table.get_symbol(relocation["r_info_sym"]).name
                target = int(re.search(r"([0-9a-f]{8})$", target_name).group(1), 16)
                if relocation["r_info_type"] != 2:
                    raise ValueError("Unsupported DTCM relocation")
                offset, addend = relocation["r_offset"], relocation["r_addend"]
                struct.pack_into("<I", code, offset, target + addend)
                relocations.append({"offset": offset, "type": 2, "symbol": target_name, "target": hex(target), "addend": addend})
        bss = symbols["native_dtcm_027e0060"]
        bss_section = elf.get_section(bss["st_shndx"])
        data_record = {"name": table.name, "symbol": table.name, "module": "dtcm", "kind": "data", "processor": "arm9", "address": "0x027e0000", "bytes": len(native), "size": len(native), "section": section.name, "sectionIndex": table["st_shndx"], "sectionOffset": table["st_value"], "compiledBytes": len(code), "exactAfterDeclaredRelocation": code == native, "targetSha256": sha(native), "outputSha256": sha(code), "relocations": relocations, "nativeAlias": "data_027e0000", "nativeInteriorSymbols": {"data_027e0021": "0x027e0021"}}
        bss_record = {"name": bss.name, "symbol": bss.name, "kind": "bss", "module": "dtcm", "processor": "arm9", "address": "0x027e0060", "bytes": bss["st_size"], "size": bss["st_size"], "section": bss_section.name, "sectionIndex": bss["st_shndx"], "sectionOffset": bss["st_value"], "zeroFill": bss_section["sh_type"] == "SHT_NOBITS" and bss["st_size"] == 32, "exactAfterDeclaredRelocation": bss_section["sh_type"] == "SHT_NOBITS" and bss["st_size"] == 32, "nativeAlias": "data_027e0060", "relocations": []}
    if not data_record["exactAfterDeclaredRelocation"] or not bss_record["zeroFill"]:
        raise ValueError("DTCM typed-data reconstruction differs")
    report = {"schemaVersion": 1, "romSha256": sha((ROOT / "inputs/game.nds").read_bytes()), "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha(source.read_bytes()), "object": stable.relative_to(ROOT).as_posix(), "objectSha256": object_hash, "compilerSha256": sha(compiler.read_bytes()), "compilerFlags": flags, "command": command, "dataMatches": [data_record, bss_record], "matches": [], "nativeSymbols": {item["symbol"]: item["target"] for item in relocations}, "functionMatched": 0, "dataMatchedBytes": len(code), "bssMatchedBytes": 32, "wholeModuleLinked": False, "limitations": ["Pointer targets are measured native addresses; callback gameplay identities are not inferred", "Behavioral execution is not applicable to static initialized pointers and zero-fill data", "Whole-module link validation is performed separately"]}
    for entry in report["dataMatches"]:
        entry.update({key: report[key] for key in ("source", "sourceSha256", "object", "objectSha256", "compilerSha256", "compilerFlags", "nativeSymbols")})
    target = ROOT / "evidence/data/dtcm.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + "\n")
    print({"dataMatchedBytes": len(code), "bssMatchedBytes": 32, "relocations": len(relocations), "functionMatched": 0})


if __name__ == "__main__":
    main()
