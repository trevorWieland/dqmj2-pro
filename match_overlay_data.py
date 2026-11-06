import hashlib
import argparse
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "deps/native"))
from elftools.elf.elffile import ELFFile
from match_overlay_modules import compile_compare, immutable, sha, symbol_data, ROM_HASH
from overlay_report_refresh import refresh_data_report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="src/overlays/ov002_data_b1c8dc8f7a55.c")
    args = parser.parse_args()
    source = (ROOT / args.source).resolve()
    if not source.is_relative_to(ROOT):
        raise ValueError("Data source must be inside the repository")
    frozen = ROOT / f"src/overlays/ov002_data_{sha(source.read_bytes())[:12]}.c"
    immutable(frozen, source.read_bytes())
    report, compiled = compile_compare("ov002", frozen)
    if report["returncode"]:
        raise ValueError(report["stderr"])
    lookup, boundaries = symbol_data("ov002")
    lookup.update(native_ov002_bss=0x021DA620)
    native = (ROOT / "extract/arm9_overlays/ov002.bin").read_bytes()
    objects = []
    with (ROOT / report["object"]).open("rb") as stream:
        elf = ELFFile(stream)
        symbols = elf.get_section_by_name(".symtab")
        for name, address, size, kind in [("native_ov002_rodata", 0x021DA46C, 196, ".rodata"), ("native_ov002_data", 0x021DA540, 224, ".data"), ("native_ov002_bss", 0x021DA620, 3552, ".bss")]:
            symbol = symbols.get_symbol_by_name(name)[0]
            section = elf.get_section(symbol["st_shndx"]) if isinstance(symbol["st_shndx"], int) else None
            if symbol["st_size"] != size:
                raise ValueError("Data object size differs: " + name)
            if kind == ".bss":
                if section is not None and section["sh_type"] != "SHT_NOBITS":
                    raise ValueError("Zero storage unexpectedly occupies initialized data")
                objects.append({"name": name, "kind": "bss", "section": ".bss", "address": hex(address), "size": size, "exactZeroStorage": True, "elfAllocation": str(symbol["st_shndx"]), "source": report["source"], "sourceSha256": report["sourceSha256"], "object": report["object"], "objectSha256": report["objectSha256"]})
                continue
            start = symbol["st_value"]
            raw = section.data()[start:start + size]
            code = bytearray(raw)
            relocations = []
            for relocation_section in elf.iter_sections():
                if relocation_section["sh_type"] not in {"SHT_REL", "SHT_RELA"} or relocation_section["sh_info"] != symbol["st_shndx"]:
                    continue
                table = elf.get_section(relocation_section["sh_link"])
                for relocation in relocation_section.iter_relocations():
                    at = relocation["r_offset"] - start
                    if not 0 <= at < size:
                        continue
                    target_name = table.get_symbol(relocation["r_info_sym"]).name
                    if relocation["r_info_type"] != 2 or target_name not in lookup:
                        raise ValueError("Unsupported data relocation")
                    addend = relocation["r_addend"] if relocation_section["sh_type"] == "SHT_RELA" else struct.unpack_from("<I", code, at)[0]
                    target = lookup[target_name]
                    struct.pack_into("<I", code, at, target + addend)
                    relocations.append({"offset": at, "type": 2, "symbol": target_name, "target": hex(target), "addend": addend})
            expected = native[address - 0x021D7240:address - 0x021D7240 + size]
            if bytes(code) != expected:
                differences = [index for index, (a, b) in enumerate(zip(code, expected)) if a != b]
                raise ValueError("Typed data differs: " + name + " " + str(differences[:32]))
            objects.append({"name": name, "kind": "initialized-data", "section": kind, "address": hex(address), "size": size, "exactAfterDeclaredRelocation": True, "rawSha256": sha(raw), "outputSha256": sha(code), "targetSha256": sha(expected), "relocations": relocations, "source": report["source"], "sourceSha256": report["sourceSha256"], "object": report["object"], "objectSha256": report["objectSha256"]})
    aliases = {name: hex(address) for name, address in lookup.items() if name.startswith("data_ov002_")}
    result = {"schemaVersion": 1, "date": "2026-10-27", "romSha256": ROM_HASH, "module": "ov002", "source": report["source"], "sourceSha256": report["sourceSha256"], "object": report["object"], "objectSha256": report["objectSha256"], "compilerSha256": report["compilerSha256"], "flags": report["flags"], "dataMatches": objects, "nativeSymbols": {item["symbol"]: item["target"] for obj in objects for item in obj.get("relocations", [])}, "dataAliases": aliases, "alignmentPadding": {"address": "0x021da530", "size": 16, "allZero": not any(native[0x32F0:0x3300])}, "wholeModuleLinked": False, "limitations": ["Data field names denote offsets and structural observations; game-level meanings remain unassigned.", "BSS labels are views into shared zero storage and must not become independent overlapping allocations."]}
    path = ROOT / f"evidence/data/overlays-ov002-{report['sourceSha256'][:12]}.json"
    refresh_data_report(path, result)
    print(json.dumps({"report": str(path.relative_to(ROOT)), "initializedBytes": 420, "bssBytes": 3552, "objects": len(objects)}, indent=2))


if __name__ == "__main__":
    main()
