import json
import os
import subprocess
from pathlib import Path
import utility_code
import utility_oracle
import utility_runtime
import match_utility_hardware
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent


def main():
    previous = json.loads((ROOT / "evidence/matches/utility-hardware02.json").read_text())
    expected = previous["matches"][0]
    spec = utility_code.accepted_spec(expected)
    if spec["module"] != "utility-child-arm9-itcm" or spec["address"] != 0x01FF81B4:
        raise ValueError("Frozen utility DMA hardware placement changed")
    if spec["bytes"] != 60 or spec["mode"] != "thumb":
        raise ValueError("Utility DMA hardware primitive changed extent or mode")
    assembler = match_utility_hardware.ASSEMBLER
    if utility_runtime.sha(assembler.read_bytes()) != match_utility_hardware.ASSEMBLER_HASH:
        raise ValueError("Utility DMA assembler identity changed")
    name = "native_utility_child_arm9_itcm_dma_01ff81b4"
    source = ROOT / f"src/utility/hardware/{name}.s"
    if expected["source"] != source.relative_to(ROOT).as_posix() or expected["sourceSha256"] != utility_runtime.sha(source.read_bytes()):
        raise ValueError("Frozen utility DMA hardware source changed")
    work = ROOT / "work/lowlevel-recovery/utility-dma-hardware"
    work.mkdir(parents=True, exist_ok=True)
    obj = work / (name + ".o")
    flags = ["-proc", "arm5TE", "-c"]
    command = [str(assembler), *flags, str(source), "-o", str(obj)]
    process = subprocess.run(command, cwd=ROOT, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat")),
                             capture_output=True, text=True, timeout=30)
    attempt = {"command": command, "exitCode": process.returncode, "stdout": process.stdout, "stderr": process.stderr}
    if process.returncode:
        raise ValueError("Utility DMA hardware assembly failed: " + str(attempt))
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        symbol = next(symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols() if symbol.name == name)
        output = elf.get_section(symbol["st_shndx"]).data()
        if any(section["sh_type"] in ("SHT_REL", "SHT_RELA") and section["sh_size"] for section in elf.iter_sections()):
            raise ValueError("Utility DMA leaf must not contain undeclared relocations")
    binary = (ROOT / spec["binary"]).read_bytes()
    native = binary[spec["address"] - spec["base"]:spec["address"] - spec["base"] + 60]
    if output != native or symbol["st_size"] != 60:
        raise ValueError("Utility DMA leaf reconstruction differs")
    digest = utility_runtime.sha(obj.read_bytes())
    stable = work / (digest + ".o")
    if not stable.exists():
        stable.write_bytes(obj.read_bytes())
    entry = {"name": name, "program": utility_runtime.PROGRAM, "module": spec["module"], "processor": "arm9", "mode": "thumb",
             "address": hex(spec["address"]), "bytes": 60, "size": 60, "compiledBytes": 60, "matchingBytes": 60,
             "source": source.relative_to(ROOT).as_posix(), "sourceSha256": utility_runtime.sha(source.read_bytes()),
             "object": stable.relative_to(ROOT).as_posix(), "objectSha256": digest, "compiler": assembler.relative_to(ROOT).as_posix(),
             "compilerSha256": match_utility_hardware.ASSEMBLER_HASH, "assemblerSha256": match_utility_hardware.ASSEMBLER_HASH,
             "compilerFlags": flags, "relocations": [], "sectionIndex": symbol["st_shndx"], "sectionOffset": symbol["st_value"] & ~1,
             "nativeAlias": "func_utility_child_arm9_itcm_01ff81b4", "inputModuleSha256": spec["inputModuleSha256"],
             "targetSha256": utility_runtime.sha(native), "outputSha256": utility_runtime.sha(output), "exactAfterDeclaredRelocation": True,
             "assemblyJustification": "This is a direct DMA-controller register primitive preserving mandatory repeated MMIO reads, the channel-zero shutdown/control sequence, and its leaf LR/stack contract; assembly is limited to this hardware protocol, without claiming historical original source language",
             "oracle": utility_oracle.oracle(output, spec), "linked": False}
    report = {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM,
              "runtimeMappingCanonical": True, "matches": [entry], "nativeSymbols": {}, "attempts": [attempt],
              "sourceReconstructionComplete": False, "wholeModuleLinked": False,
              "limitations": ["C drafts remain recorded in evidence/attempts/utility-dma-compilers.json and utility-dma-leaf-options.json; their mismatching bytes receive no credit",
                              "Physical DMA execution is not modeled; the native MMIO protocol is compared in isolated memory",
                              "The 24 trailing zero module bytes remain separate from this function and its two actual literal words"]}
    (ROOT / "evidence/matches/utility-hardware02.json").write_text(json.dumps(report, indent=2) + "\n")
    print({"functions": 1, "nativeBytes": 60, "nativeAndRecompiledCalls": entry["oracle"]["nativeAndRecompiledCalls"]})


if __name__ == "__main__":
    main()
