import json
import os
import re
import struct
import subprocess
from pathlib import Path
import utility_runtime
import match_arm7_boot
import match_utility_data
import match_utility_hardware
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_OP_MEM, ARM_REG_PC

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/lowlevel-recovery/utility-startup"
SPECS = {0x02380000: 256, 0x02380100: 92, 0x0238015C: 60}
CODE_RANGES = {0x02380000: [(0x02380000, 0x023800CC)],
               0x02380100: [(0x02380100, 0x02380154), (0x02380158, 0x0238015C)],
               0x0238015C: [(0x0238015C, 0x02380194)]}
JUSTIFICATIONS = {
    0x02380000: "Native ARM7 reset entry changes CPSR modes and banked stack pointers, transfers firmware handoff buffers, installs the IRQ vector and branches to the Thumb application with a non-C LR",
    0x02380100: "Startup autoload copy/zero loop consumes native module descriptors and clobbers R4-R7 in its measured stack-free boot ABI rather than preserving normal C callee-saved registers",
    0x0238015C: "Startup physical-RAM alias probe reads and writes fixed shared hardware locations before entering the application; physical alias behavior is not expressible by ordinary hosted RAM objects"
}


def data_entry(source, processor, symbol_name, address, expected, module, kind, source_offset):
    obj, flags, attempt = match_utility_data.compile_source(source, processor)
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        symbol = next(symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols() if symbol.name == symbol_name)
        section = elf.get_section(symbol["st_shndx"])
        first, size = symbol["st_value"], symbol["st_size"]
        output = section.data()[first:first + size]
        if any(rel["sh_type"] in ("SHT_REL", "SHT_RELA") and rel["sh_size"] and rel["sh_info"] == symbol["st_shndx"] for rel in elf.iter_sections()):
            raise ValueError("Utility typed module parameters must have no undeclared relocation")
    if output != expected:
        raise ValueError("Utility typed startup data differs from native fields")
    entry = {"name": symbol_name, "symbol": symbol_name, "program": utility_runtime.PROGRAM, "processor": processor,
             "address": hex(address), "bytes": size, "size": size, "compiledBytes": size, "kind": "data",
             "source": source.relative_to(ROOT).as_posix(), "sourceSha256": utility_runtime.sha(source.read_bytes()),
             "object": obj.relative_to(ROOT).as_posix(), "objectSha256": utility_runtime.sha(obj.read_bytes()),
             "compiler": match_utility_data.COMPILER.relative_to(ROOT).as_posix(), "compilerSha256": match_utility_data.COMPILER_HASH,
             "compilerFlags": flags, "section": section.name, "sectionType": section["sh_type"], "sectionFlags": section["sh_flags"],
             "sectionIndex": symbol["st_shndx"], "sectionOffset": first, "relocations": [],
             "outputSha256": utility_runtime.sha(output), "targetSha256": utility_runtime.sha(expected),
             "exactAfterDeclaredRelocation": True, "linked": False}
    if kind == "runtime":
        entry.update(module=module["id"], inputModuleSha256=module["sha256"],
                     nativeAlias="data_" + module["id"].replace("-", "_") + f"_{address:08x}")
    else:
        entry.update(placement="physical-processor-autoload-metadata", sourceMetadataBytes=size,
                     inputDecodedOffset=source_offset, initializedRuntimeDataBytes=0, functionBytes=0)
    return entry, attempt


def main():
    layout, files = utility_runtime.derive()
    if utility_runtime.sha(match_utility_hardware.ASSEMBLER.read_bytes()) != match_utility_hardware.ASSEMBLER_HASH or utility_runtime.sha(match_utility_data.COMPILER.read_bytes()) != match_utility_data.COMPILER_HASH:
        raise ValueError("Utility startup tool identity changed")
    modules = {module["id"]: module for module in layout["modules"]}
    module = modules["utility-child-arm7-boot"]
    binary = bytes(files[ROOT / module["binary"]])
    WORK.mkdir(parents=True, exist_ok=True)
    match_utility_data.WORK.mkdir(parents=True, exist_ok=True)
    matches, attempts, bindings = [], [], {}
    for address, size in SPECS.items():
        name = f"native_utility_child_arm7_boot_hw_{address:08x}"
        source = ROOT / f"src/utility/startup/{name}.s"
        text = source.read_text()
        if any(token in text for token in (".byte", ".hword", ".incbin")):
            raise ValueError("Utility startup source must remain mnemonic assembly")
        decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
        decoder.detail = True
        pools = set()
        for first, last in CODE_RANGES[address]:
            for instruction in decoder.disasm(binary[first - 0x02380000:last - 0x02380000], first):
                pools.update(instruction.address + 8 + operand.mem.disp for operand in instruction.operands
                             if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC)
        if pools != {int(value, 16) for value in re.findall(r"local_([0-9a-f]{8}):\s*\.word", text)}:
            raise ValueError("Utility startup .word data must be exactly the native PC-relative literal targets")
        obj = WORK / (name + ".o")
        flags = ["-proc", "arm4t", "-c"]
        command = [str(match_utility_hardware.ASSEMBLER), *flags, str(source), "-o", str(obj)]
        process = subprocess.run(command, cwd=ROOT, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat")),
                                 capture_output=True, text=True, timeout=30)
        attempts.append({"command": command, "exitCode": process.returncode, "stdout": process.stdout, "stderr": process.stderr})
        if process.returncode:
            (ROOT / "evidence/attempts/utility-startup-rejected.json").write_text(json.dumps(attempts, indent=2) + "\n")
            raise ValueError("Utility startup assembly failed")
        output, relocations, index, offset, section = match_arm7_boot.object_bytes(obj, name, address)
        native = binary[address - 0x02380000:address - 0x02380000 + size]
        if output != native:
            raise ValueError("Utility startup reconstruction differs from its complete native span")
        digest = utility_runtime.sha(obj.read_bytes())
        stable = WORK / "objects" / (digest + ".o")
        stable.parent.mkdir(exist_ok=True)
        if not stable.exists():
            stable.write_bytes(obj.read_bytes())
        bindings.update({rel["symbol"]: rel["target"] for rel in relocations})
        matches.append({"name": name, "program": utility_runtime.PROGRAM, "processor": "arm7", "module": module["id"], "mode": "arm",
                        "address": hex(address), "bytes": size, "size": size, "compiledBytes": size, "matchingBytes": size,
                        "source": source.relative_to(ROOT).as_posix(), "sourceSha256": utility_runtime.sha(source.read_bytes()),
                        "object": stable.relative_to(ROOT).as_posix(), "objectSha256": digest,
                        "compiler": match_utility_hardware.ASSEMBLER.relative_to(ROOT).as_posix(),
                        "compilerSha256": match_utility_hardware.ASSEMBLER_HASH, "assemblerSha256": match_utility_hardware.ASSEMBLER_HASH,
                        "compilerFlags": flags, "relocations": relocations, "sectionIndex": index, "sectionOffset": offset,
                        "nativeAlias": f"func_utility_child_arm7_boot_{address:08x}", "inputModuleSha256": module["sha256"],
                        "targetSha256": utility_runtime.sha(native), "outputSha256": utility_runtime.sha(output), "exactAfterDeclaredRelocation": True,
                        "nativeCodeRanges": [[hex(first), hex(last)] for first, last in CODE_RANGES[address]],
                        "assemblyJustification": JUSTIFICATIONS[address], "linked": False,
                        "oracle": {"supported": False, "reason": "Full physical RAM alias, firmware handoff and privileged boot execution are outside the isolated runtime model"}})
    binding_rows = []
    for name, value in bindings.items():
        target = int(value, 0)
        destination = next(module for module in layout["modules"] if module["processor"] == "arm7" and int(module["base"], 0) <= target & ~1 < int(module["runtimeEnd"], 0))
        kind = "data" if "_params_" in name else "function"
        binding_rows.append({"name": name, "program": utility_runtime.PROGRAM, "processor": "arm7", "module": destination["id"],
                             "address": value, "kind": kind, "mode": "data" if kind == "data" else "thumb" if target & 1 else "arm"})
    report = {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM,
              "runtimeMappingCanonical": True, "matches": matches, "nativeSymbols": bindings, "nativeSymbolBindings": binding_rows,
              "attempts": attempts, "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "limitations": ["Assembly is restricted to native reset/autoload and physical hardware probing with their measured boot ABI",
                              "Every literal word is an actual PC-relative load target; no instruction-word substitution is used",
                              "No physical firmware/RAM-alias boot execution is claimed"]}
    (ROOT / "evidence/matches/utility-startup01.json").write_text(json.dumps(report, indent=2) + "\n")
    data_matches, container_matches, data_attempts = [], [], []
    for processor in layout["processors"]:
        cpu = processor["processor"]
        base = 0x02000000 if cpu == "arm9" else 0x02380000
        address = int(processor["parameterAddress"], 0)
        raw = bytes(files[ROOT / processor["decodedBinary"]])
        size = len(processor["parameterWords"]) * 4
        symbol = "native_utility_child_" + cpu + ("_module_params_" if cpu == "arm9" else "_boot_params_") + f"{address:08x}"
        module = modules["utility-child-" + cpu + ("-main" if cpu == "arm9" else "-boot")]
        entry, attempt = data_entry(ROOT / f"src/utility/startup/{cpu}_parameters.c", cpu, symbol, address,
                                    raw[address - base:address - base + size], module, "runtime", address - base)
        data_matches.append(entry)
        data_attempts.append(attempt)
        address = int(processor["compositionTableAddress"], 0)
        symbol = f"native_utility_child_{cpu}_composition_{address:08x}"
        entry, attempt = data_entry(ROOT / f"src/utility/startup/{cpu}_composition.c", cpu, symbol, address,
                                    raw[address - base:address - base + 24], None, "container", address - base)
        container_matches.append(entry)
        data_attempts.append(attempt)
    data_report = {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM,
                   "runtimeMappingCanonical": True, "dataMatches": data_matches, "containerMatches": container_matches,
                   "dataMatchedBytes": sum(entry["bytes"] for entry in data_matches), "bssMatchedBytes": 0,
                   "containerMetadataMatchedBytes": sum(entry["bytes"] for entry in container_matches), "functionMatched": 0,
                   "nativeSymbols": {}, "attempts": data_attempts, "wholeModuleLinked": False, "sourceReconstructionComplete": False,
                   "limitations": ["Physical autoload descriptors are outside canonical initialized runtime module spans and receive no runtime-data/function credit",
                                   "ARM7 sixth parameter word remains semantically unknown; all fields retain measured native values"]}
    (ROOT / "evidence/data/utility-startup.json").write_text(json.dumps(data_report, indent=2) + "\n")
    print({"startupFunctions": len(matches), "startupCodeBytes": sum(entry["bytes"] for entry in matches),
           "typedRuntimeDataBytes": data_report["dataMatchedBytes"], "typedContainerMetadataBytes": data_report["containerMetadataMatchedBytes"]})


if __name__ == "__main__":
    main()
