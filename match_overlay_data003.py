import argparse
import json
import struct
from match_overlay_modules import ROOT, ROM_HASH, compile_compare, immutable, sha, symbol_data, ELFFile
from overlay_report_refresh import refresh_data_report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="src/overlays/ov003_data_c14f5ceca865.c")
    args = parser.parse_args()
    source = (ROOT / args.source).resolve()
    if not source.is_relative_to(ROOT):
        raise ValueError("Data source must be inside the repository")
    frozen = ROOT / f"src/overlays/ov003_data_{sha(source.read_bytes())[:12]}.c"
    immutable(frozen, source.read_bytes())
    report, compiled = compile_compare("ov003", frozen)
    if report["returncode"]:
        raise ValueError(report["stdout"] + report["stderr"])
    lookup, boundaries = symbol_data("ov003")
    lookup.update(native_ov003_rodata=0x021E0104, native_ov003_data=0x021E0220, native_ov003_bss=0x021E0440)
    native = (ROOT / "extract/arm9_overlays/ov003.bin").read_bytes()
    objects = []
    specs = [("native_ov003_rodata", 0x021E0104, 276, ".rodata"), ("native_ov003_data", 0x021E0220, 544, ".data"), ("native_ov003_bss", 0x021E0440, 2816, ".bss")]
    with (ROOT / report["object"]).open("rb") as stream:
        elf = ELFFile(stream)
        symbols = elf.get_section_by_name(".symtab")
        for name, address, size, kind in specs:
            symbol = symbols.get_symbol_by_name(name)[0]
            section = elf.get_section(symbol["st_shndx"]) if isinstance(symbol["st_shndx"], int) else None
            if symbol["st_size"] != size:
                raise ValueError("Data object size differs: " + name + " " + str(symbol["st_size"]))
            evidence = {"name": name, "section": kind, "address": hex(address), "size": size, "source": report["source"], "sourceSha256": report["sourceSha256"], "object": report["object"], "objectSha256": report["objectSha256"]}
            if kind == ".bss":
                if section is not None and section["sh_type"] != "SHT_NOBITS":
                    raise ValueError("Zero storage unexpectedly occupies initialized data")
                objects.append(dict(evidence, kind="bss", exactZeroStorage=True, elfAllocation=str(symbol["st_shndx"])))
                continue
            start = symbol["st_value"]
            raw = section.data()[start:start + size]
            data = bytearray(raw)
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
                        raise ValueError("Unsupported data relocation: " + target_name)
                    addend = relocation["r_addend"] if relocation_section["sh_type"] == "SHT_RELA" else struct.unpack_from("<I", data, at)[0]
                    target = lookup[target_name]
                    struct.pack_into("<I", data, at, target + addend)
                    relocations.append({"offset": at, "type": 2, "symbol": target_name, "target": hex(target), "addend": addend})
            expected = native[address - 0x021D7240:address - 0x021D7240 + size]
            if bytes(data) != expected:
                differences = [index for index, (a, b) in enumerate(zip(data, expected)) if a != b]
                raise ValueError("Typed data differs: " + name + " " + str(differences[:32]))
            objects.append(dict(evidence, kind="initialized-data", exactAfterDeclaredRelocation=True, rawSha256=sha(raw), outputSha256=sha(data), targetSha256=sha(expected), relocations=relocations))
    padding = native[0x021E0218 - 0x021D7240:0x021E0220 - 0x021D7240]
    if len(padding) != 8 or any(padding):
        raise ValueError("Read-only/data alignment padding differs")
    aliases = {name: hex(address) for name, address in lookup.items() if name.startswith("data_ov003_")}
    result = {"schemaVersion": 1, "date": "2026-10-27", "romSha256": ROM_HASH, "module": "ov003", "source": report["source"], "sourceSha256": report["sourceSha256"], "object": report["object"], "objectSha256": report["objectSha256"], "compilerSha256": report["compilerSha256"], "flags": report["flags"], "dataMatches": objects, "nativeSymbols": {item["symbol"]: item["target"] for obj in objects for item in obj.get("relocations", [])}, "dataAliases": aliases, "alignmentPadding": {"address": "0x021e0218", "size": 8, "allZero": True}, "wholeModuleLinked": False, "observations": {"callbackTriplets": [3, 9], "panelCallbackPairs": 7, "workPointers": 2, "catalogWords": [17, 11, 20, 62, 2], "byteRows": [[9, 3], [21, 3]]}, "limitations": ["Names describe structural observations; game-level meanings remain unassigned.", "Data labels are views into complete allocations, not overlapping independent storage."]}
    path = ROOT / f"evidence/data/overlays-ov003-{report['sourceSha256'][:12]}.json"
    refresh_data_report(path, result)
    print(json.dumps({"report": str(path.relative_to(ROOT)), "initializedBytes": 820, "alignmentBytes": 8, "bssBytes": 2816, "objects": len(objects), "source": str(frozen.relative_to(ROOT))}, indent=2))


if __name__ == "__main__":
    main()
