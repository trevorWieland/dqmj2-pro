import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "deps/native"))
from elftools.elf.elffile import ELFFile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    source = ROOT / "src/itcm/storage.c"
    compiler = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
    if sha(compiler.read_bytes()) != "7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880":
        raise ValueError("ITCM storage compiler identity differs")
    layout = (ROOT / "config/arm9/itcm/delinks.txt").read_text()
    extent = re.search(r"\.bss\s+start:(0x[0-9a-f]+) end:(0x[0-9a-f]+)", layout)
    start, end = (int(value, 0) for value in extent.groups())
    if (start, end) != (0x01FFF8A0, 0x01FFFBC0):
        raise ValueError("ITCM zero-fill extent changed")
    flags = ["-O2", "-proc", "arm946e", "-sym", "on", "-nolink"]
    work = ROOT / "work/lowlevel-recovery/itcm-storage"
    work.mkdir(parents=True, exist_ok=True)
    obj = work / "storage.o"
    command = [str(compiler), *flags, "-c", str(source), "-o", str(obj)]
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat"))
    result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, timeout=30)
    if result.returncode:
        raise RuntimeError(result.stdout.decode(errors="replace") + result.stderr.decode(errors="replace"))
    object_hash = sha(obj.read_bytes())
    stable = work / (object_hash + ".o")
    if not stable.exists():
        stable.write_bytes(obj.read_bytes())
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        symbol = next(symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols()
                      if symbol.name == "native_itcm_storage_01fff8a0")
        section = elf.get_section(symbol["st_shndx"])
        if section["sh_type"] != "SHT_NOBITS" or symbol["st_value"] != 0 or symbol["st_size"] != end - start:
            raise ValueError("Compiled zero-fill storage differs from measured allocation")
        match = {"name": symbol.name, "symbol": symbol.name, "module": "itcm", "processor": "arm9", "kind": "bss",
                 "section": section.name, "sectionIndex": symbol["st_shndx"], "sectionOffset": 0,
                 "address": hex(start), "bytes": end - start, "size": end - start,
                 "nativeAlias": "data_01fff8a0", "zeroFill": True, "exactAfterDeclaredRelocation": True,
                 "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha(source.read_bytes()),
                 "object": stable.relative_to(ROOT).as_posix(), "objectSha256": object_hash,
                 "compilerSha256": sha(compiler.read_bytes()), "compilerFlags": flags, "relocations": [], "nativeSymbols": {}}
    aliases = {}
    for name, address in re.findall(r"^(\S+) kind:bss addr:(0x[0-9a-f]+)", (ROOT / "config/arm9/itcm/symbols.txt").read_text(), re.M):
        if start < int(address, 0) < end:
            aliases[name] = address
    match["nativeInteriorSymbols"] = aliases
    report = {"schemaVersion": 1, "romSha256": sha((ROOT / "inputs/game.nds").read_bytes()),
              "module": "itcm", "dataMatches": [match], "nativeSymbols": {},
              "functionMatched": 0, "dataMatchedBytes": 0, "bssMatchedBytes": end - start,
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "limitations": ["Reconstructs measured zero-filled allocation only; variable types and native gameplay meanings remain unknown", "Allocated zero-fill bytes are not ROM-byte reconstruction or executable function coverage"]}
    path = ROOT / "evidence/data/itcm.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n")
    print({"bssMatchedBytes": end - start, "nativeInteriorAliases": len(aliases), "functions": 0})


if __name__ == "__main__":
    main()
