import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
from pathlib import Path

from project import ROOT, configuration, now, sha256, write_json

sys.path.insert(0, str(ROOT / "deps/native"))
from elftools.elf.elffile import ELFFile

WORK = ROOT / "work/ov007-finish/20261029/source-alignment"
REPORT = ROOT / "evidence/linkage/ov007-20261029-alignment.json"
DATA_REPORT = ROOT / "evidence/data/overlays-ov007-e0b7b1d37938.json"
COMPILER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
LINKER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwldarm.exe"
LINKER_HASH = "bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74"
START, GAP_START, DATA_START, END = 0x021DA06C, 0x021DA0B0, 0x021DA0C0, 0x021DA980


def invoke(arguments, directory):
    process = subprocess.run([str(value) for value in arguments], cwd=directory,
                             env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat")),
                             capture_output=True, text=True, timeout=60)
    return {"arguments": [str(value) for value in arguments], "cwd": str(directory),
            "returncode": process.returncode, "stdout": process.stdout, "stderr": process.stderr}


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    accepted = json.loads(DATA_REPORT.read_text())
    source = ROOT / accepted["source"]
    if sha256(source) != accepted["sourceSha256"] or sha256(COMPILER) != accepted["compilerSha256"]:
        raise ValueError("Frozen accepted data source/compiler changed")
    if sha256(LINKER) != LINKER_HASH:
        raise ValueError("Verified MW linker changed")
    manifest = json.loads((ROOT / "provenance/seed-manifest.json").read_text())
    metadata = next(row for row in manifest["modules"] if row["name"] == "ov007")
    binary_path = ROOT / metadata["binary"]
    if sha256(binary_path) != metadata["sha256"]:
        raise ValueError("Measured ov007 input changed")
    binary = binary_path.read_bytes()
    base = int(metadata["base"], 0)
    gap = binary[GAP_START - base:DATA_START - base]
    if gap != bytes(16):
        raise ValueError("Native inter-section range is not sixteen zero bytes")
    delinks_path = ROOT / "config/arm9/overlays/ov007/delinks.txt"
    delinks = delinks_path.read_text()
    expected_layout = [r"\.rodata\s+start:0x021da06c end:0x021da0b0 kind:rodata align:4",
                       r"\.ctor\s+start:0x021da0b0 end:0x021da0b0 kind:rodata align:4",
                       r"\.data\s+start:0x021da0c0 end:0x021da980 kind:data align:32"]
    if not all(re.search(pattern, delinks) for pattern in expected_layout):
        raise ValueError("Measured section inventory no longer supports constructor/data alignment")
    symbols_path = ROOT / "config/arm9/overlays/ov007/symbols.txt"
    symbols = symbols_path.read_text()
    functions = [(int(address, 16), int(size, 16)) for size, address in re.findall(
        r"kind:function\(arm,size=0x([0-9a-f]+)\) addr:0x([0-9a-f]+)", symbols)]
    overlaps = [(hex(address), size) for address, size in functions
                if address < DATA_START and address + size > GAP_START]
    if overlaps:
        raise ValueError("A configured executable function overlaps the proposed metadata/fill range")
    references = []
    for path in (ROOT / "config/arm9").rglob("relocs.txt"):
        for line in path.read_text().splitlines():
            match = re.search(r"from:(0x[0-9a-f]+) kind:(\S+) to:(0x[0-9a-f]+) module:overlay\(7\)", line)
            if match and GAP_START <= int(match[3], 0) < DATA_START:
                references.append({"config": str(path.relative_to(ROOT)), "from": match[1],
                                   "kind": match[2], "to": match[3]})
    if any("call" in row["kind"] or "branch" in row["kind"] for row in references):
        raise ValueError("A configured control-flow reference enters the proposed fill")
    source_object = WORK / "source-data.o"
    compile_attempt = invoke([COMPILER, *accepted["flags"], "-c", source, "-o", source_object], WORK)
    if compile_attempt["returncode"]:
        raise ValueError(compile_attempt)
    with source_object.open("rb") as stream:
        elf = ELFFile(stream)
        source_sections = [{"name": section.name, "bytes": section["sh_size"],
                            "alignment": section["sh_addralign"], "type": section["sh_type"]}
                           for section in elf.iter_sections() if section["sh_size"]
                           and section.name in (".text", ".rodata", ".data", ".bss")]
        if any(row["name"] == ".text" for row in source_sections):
            raise ValueError("Data-only proof object unexpectedly contains executable code")
    variants = []
    expected = binary[START - base:END - base]
    for name, terminator, alignment in [("canonical", True, 32),
                                         ("no-alignment-negative", True, 4),
                                         ("alignment-only-equivalent", False, 32)]:
        directory = WORK / name
        directory.mkdir(exist_ok=True)
        local_object = directory / "source-data.o"
        shutil.copy2(source_object, local_object)
        control = directory / "layout.lcf"
        body = ["MEMORY {", f"DATA: ORIGIN = {START:#x} > layout.bin",
                f"BSS: ORIGIN = {END:#x} > bss.bin", "}", "SECTIONS {", ".layout: {",
                "source-data.o(.rodata)", ". = ALIGN(4);", "CTOR_START = .;"]
        if terminator:
            body.append("WRITEW(0);")
        body += ["CTOR_END = .;", f". = ALIGN({alignment});", "INITIALIZED_DATA_START = .;",
                 "source-data.o(.data)", "} > DATA",
                 ".bss: { source-data.o(.bss) } > BSS", "}"]
        control.write_text("\n".join(body) + "\n")
        linked = directory / "layout.elf"
        attempt = invoke([LINKER, "-nostdlib", "-nodeadstrip", "-interworking", "-proc", "arm946e",
                          "-main", "native_ov007_rodata", control, local_object, "-o", linked], directory)
        if attempt["returncode"]:
            raise ValueError(attempt)
        payload_path = directory / "layout.bin"
        payload = payload_path.read_bytes()
        with linked.open("rb") as stream:
            table = ELFFile(stream).get_section_by_name(".symtab")
            selected = {symbol.name: symbol["st_value"] for symbol in table.iter_symbols()
                        if symbol.name in ("CTOR_START", "CTOR_END", "INITIALIZED_DATA_START")}
        identical = payload == expected
        if name == "no-alignment-negative" and identical:
            raise ValueError("Missing native data alignment unexpectedly preserved the exact layout")
        if name != "no-alignment-negative" and not identical:
            raise ValueError("Real MW linker did not reconstruct the complete accepted data/fill interval")
        variants.append({"name": name, "terminatorWord": terminator, "dataAlignment": alignment,
                         "attempt": attempt, "symbols": selected, "exactNativeInterval": identical,
                         "outputBytes": len(payload), "expectedBytes": len(expected),
                         "matchingBytes": sum(a == b for a, b in zip(expected, payload)),
                         "output": str(payload_path.relative_to(ROOT)), "outputSha256": sha256(payload_path),
                         "linkedElf": str(linked.relative_to(ROOT)), "linkedElfSha256": sha256(linked),
                         "lcf": str(control.relative_to(ROOT)), "lcfSha256": sha256(control)})
    result = {"schemaVersion": 1, "createdUtc": now(), "romSha256": configuration()["romSha256"],
              "processor": "arm9", "module": "ov007", "moduleInputSha256": metadata["sha256"],
              "range": {"address": hex(GAP_START), "bytes": 16,
                        "sha256": hashlib.sha256(gap).hexdigest(), "allZero": True},
              "classification": "Non-executable constructor terminator/alignment between measured readonly and initialized data",
              "canonicalGeneration": {"constructorNullTerminatorBytes": 4, "zeroAlignmentBytes": 12,
                                      "alignment": 32, "explicitByteArray": False},
              "historicalAmbiguity": "Raw zeros also match direct16-byte alignment fill; this does not identify the historical linker's unique recipe",
              "configuredFunctionOverlap": overlaps, "incomingModuleQualifiedReferences": references,
              "configHashes": {str(path.relative_to(ROOT)): sha256(path) for path in (delinks_path, symbols_path)},
              "source": str(source.relative_to(ROOT)), "sourceSha256": sha256(source),
              "existingDataReport": str(DATA_REPORT.relative_to(ROOT)), "existingDataReportSha256": sha256(DATA_REPORT),
              "freshObject": str(source_object.relative_to(ROOT)), "freshObjectSha256": sha256(source_object),
              "sourceSections": source_sections, "compilerAttempt": compile_attempt,
              "compilerSha256": sha256(COMPILER), "linkerSha256": sha256(LINKER), "variants": variants,
              "supportsSourceOnlyRegenerationOfRange": True, "proposedLinkerGeneratedBytes": 16,
              "newAuthoredCodeCredit": 0, "newSourceDataCredit": 0,
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "reproduction": "python prove_ov007_alignment_20261029.py",
              "generatorSha256": sha256(Path(__file__))}
    write_json(REPORT, result)
    print(json.dumps({"classifiedBytes": 16, "sourceOnlyRealLinkIntervalBytes": len(expected),
                      "canonicalExact": True, "negativeAlignmentRejected": True,
                      "report": str(REPORT.relative_to(ROOT))}))


if __name__ == "__main__":
    main()
