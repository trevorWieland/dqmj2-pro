import argparse
import json

import audit_overlay004 as audit
from match_overlay_modules import (
    ELFFile,
    ROOT,
    ROM_HASH,
    compile_compare,
    immutable,
    sha,
)
from overlay_report_refresh import refresh_data_report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="src/overlays/ov004_data_1e819dc4f7db.c")
    args = parser.parse_args()
    source = (ROOT / args.source).resolve()
    if not source.is_relative_to(ROOT / "src/overlays"):
        raise ValueError("Overlay004 data source must be frozen inside src/overlays")
    if sha((ROOT / "inputs/game.nds").read_bytes()) != ROM_HASH:
        raise ValueError("Original ROM namespace differs")
    frozen = ROOT / f"src/overlays/ov004_data_{sha(source.read_bytes())[:12]}.c"
    immutable(frozen, source.read_bytes())
    report, codes = compile_compare("ov004", frozen)
    if report["returncode"] or report["functions"] or codes:
        raise ValueError(
            "Expected a data-only C unit: " + report["stdout"] + report["stderr"]
        )
    data = audit.inputs()
    specs = [
        ("native_ov004_complemented_identifier", 0x021D8EB4, 6, ".rodata"),
        ("native_ov004_protection_storage", 0x021D8EE0, 32, ".bss"),
    ]
    objects = []
    with (ROOT / report["object"]).open("rb") as stream:
        elf = ELFFile(stream)
        symbols = elf.get_section_by_name(".symtab")
        for name, address, size, kind in specs:
            found = symbols.get_symbol_by_name(name)
            if not found or len(found) != 1:
                raise ValueError("Expected exactly one named data object")
            symbol = found[0]
            if symbol["st_size"] != size:
                raise ValueError("Typed data object size differs")
            section = (
                elf.get_section(symbol["st_shndx"])
                if isinstance(symbol["st_shndx"], int)
                else None
            )
            evidence = {
                "name": name,
                "section": kind,
                "address": hex(address),
                "size": size,
                "source": report["source"],
                "sourceSha256": report["sourceSha256"],
                "object": report["object"],
                "objectSha256": report["objectSha256"],
            }
            if kind == ".bss":
                if section is not None and section["sh_type"] != "SHT_NOBITS":
                    raise ValueError(
                        "Uninitialized storage unexpectedly occupies initialized bytes"
                    )
                if data["entry"][3] != size or data["bssVariable"] != address:
                    raise ValueError(
                        "ROM overlay BSS extent or protection metadata base differs"
                    )
                objects.append(
                    dict(
                        evidence,
                        kind="bss",
                        exactZeroStorage=True,
                        elfAllocation=str(symbol["st_shndx"]),
                    )
                )
                continue
            start = symbol["st_value"]
            raw = section.data()[start : start + size]
            expected = data["analysis"][
                address - audit.BASE : address - audit.BASE + size
            ]
            if raw != expected:
                raise ValueError("Complemented identifier configuration differs")
            for relocations in elf.iter_sections():
                if (
                    relocations["sh_type"] in {"SHT_REL", "SHT_RELA"}
                    and relocations["sh_info"] == symbol["st_shndx"]
                ):
                    if any(
                        start <= relocation["r_offset"] < start + size
                        for relocation in relocations.iter_relocations()
                    ):
                        raise ValueError(
                            "Literal configuration unexpectedly requires relocation"
                        )
            objects.append(
                dict(
                    evidence,
                    kind="initialized-data",
                    exactAfterDeclaredRelocation=True,
                    rawSha256=sha(raw),
                    outputSha256=sha(raw),
                    targetSha256=sha(expected),
                    relocations=[],
                )
            )
    padding = data["analysis"][0x021D8EBA - audit.BASE : 0x021D8EBC - audit.BASE]
    if padding != bytes(2):
        raise ValueError("Identifier/constructor alignment padding differs")
    result = {
        "schemaVersion": 1,
        "date": "2026-10-27",
        "romSha256": ROM_HASH,
        "module": "ov004",
        "source": report["source"],
        "sourceSha256": report["sourceSha256"],
        "object": report["object"],
        "objectSha256": report["objectSha256"],
        "compilerSha256": report["compilerSha256"],
        "flags": report["flags"],
        "dataMatches": objects,
        "nativeSymbols": {},
        "dataAliases": {"data_ov004_021d8eb4": "0x21d8eb4", "DSProt_BSS": "0x21d8ee0"},
        "alignmentPadding": {"address": "0x21d8eba", "size": 2, "allZero": True},
        "wholeModuleLinked": False,
        "observations": {
            "initializedConfigurationBytes": 6,
            "protectionRuntimeZeroStorageBytes": 32,
            "usageProof": "Both exact176-byte platform-check functions compare all six complemented identifier bytes; independent actual-SDK buffer fixtures exercise every mismatch position and all-zero fallback.",
        },
        "limitations": [
            "The preceding24-byte unreferenced analysis data remains opaque and uncredited; no executable ciphertext or native protection template is represented as a C byte array.",
            "The eight-word storage declaration represents the measured zero-initialized BSS extent; individual field meanings remain unassigned.",
            "Constructor pointer tables and native protection templates remain separate from these recovered data objects.",
        ],
    }
    target = ROOT / f"evidence/data/overlays-ov004-{report['sourceSha256'][:12]}.json"
    refresh_data_report(target, result)
    print(
        json.dumps(
            {
                "report": str(target.relative_to(ROOT)),
                "initializedBytes": 6,
                "bssBytes": 32,
                "alignmentBytes": 2,
            }
        )
    )


if __name__ == "__main__":
    main()
