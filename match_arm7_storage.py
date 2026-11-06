import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
import arm7_runtime

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "deps/native"))
from elftools.elf.elffile import ELFFile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    image = (ROOT / "extract/arm7/arm7.bin").read_bytes()
    layout = arm7_runtime.derive(image)
    if layout != json.loads(arm7_runtime.MANIFEST.read_text()):
        raise ValueError("ARM7 BSS input runtime layout is stale")
    compiler = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
    if sha(compiler.read_bytes()) != "7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880":
        raise ValueError("ARM7 storage compiler identity differs")
    flags = ["-O2", "-proc", "arm7tdmi", "-sym", "on", "-nolink"]
    work = ROOT / "work/lowlevel-recovery/arm7-storage"
    work.mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat"))
    matches = []
    for module in layout["modules"]:
        if not module["bssBytes"]:
            continue
        start = int(module["bssStart"], 0)
        source = ROOT / ("src/arm7/storage/" + module["id"].replace("-", "_") + ".c")
        name = "native_" + module["id"].replace("-", "_") + f"_storage_{start:08x}"
        obj = work / (name + ".o")
        command = [str(compiler), *flags, "-c", str(source), "-o", str(obj)]
        result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, timeout=30)
        if result.returncode:
            raise RuntimeError(result.stdout.decode(errors="replace") + result.stderr.decode(errors="replace"))
        object_hash = sha(obj.read_bytes())
        stable = work / (object_hash + ".o")
        if not stable.exists():
            stable.write_bytes(obj.read_bytes())
        with obj.open("rb") as stream:
            elf = ELFFile(stream)
            symbol = next(symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols() if symbol.name == name)
            section = elf.get_section(symbol["st_shndx"])
            if symbol["st_value"] or symbol["st_size"] != module["bssBytes"] or section["sh_type"] != "SHT_NOBITS":
                raise ValueError("ARM7 compiled BSS allocation does not match its loader descriptor")
            matches.append({"name": name, "symbol": name, "kind": "bss", "module": module["id"], "processor": "arm7",
                            "address": hex(start), "bytes": module["bssBytes"], "size": module["bssBytes"],
                            "section": section.name, "sectionIndex": symbol["st_shndx"], "sectionOffset": 0,
                            "zeroFill": True, "exactAfterDeclaredRelocation": True,
                            "nativeAlias": "data_" + module["id"].replace("-", "_") + f"_{start:08x}",
                            "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha(source.read_bytes()),
                            "object": stable.relative_to(ROOT).as_posix(), "objectSha256": object_hash,
                            "compilerSha256": sha(compiler.read_bytes()), "compilerFlags": flags,
                            "nativeSymbols": {}, "relocations": [], "nativeInteriorSymbols": {},
                            "evidence": "evidence/arm7/runtime-layout.json", "descriptorAddress": module["descriptorAddress"]})
    report = {"schemaVersion": 1, "romSha256": sha((ROOT / "inputs/game.nds").read_bytes()), "processor": "arm7",
              "runtimeMappingCanonical": True, "dataMatches": matches, "nativeSymbols": {}, "dataMatchedBytes": 0,
              "bssMatchedBytes": sum(match["bytes"] for match in matches), "functionMatched": 0,
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "limitations": ["Zero-fill allocation extents follow the measured native autoload descriptors", "Storage byte layout and initialization are reconstructed; variable types and semantics remain unknown", "Allocated BSS is separate from initialized ROM source bytes and function matching"]}
    path = ROOT / "evidence/data/arm7.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n")
    print({"modules": len(matches), "allocatedBssBytes": report["bssMatchedBytes"], "ROMSourceBytes": 0, "functions": 0})


if __name__ == "__main__":
    main()
