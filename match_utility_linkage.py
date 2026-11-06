import json
import os
import subprocess
from pathlib import Path
import utility_bridges
import utility_code
import utility_runtime
import utility_linkage_elf
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/lowlevel-recovery/utility-linkage"
LINKER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwldarm.exe"
LINKER_HASH = "bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74"


def run(command, directory):
    process = subprocess.run(command, cwd=directory, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat")),
                             capture_output=True, text=True, timeout=30)
    result = {"command": list(map(str, command)), "cwd": str(directory), "exitCode": process.returncode,
              "stdout": process.stdout, "stderr": process.stderr}
    if process.returncode:
        raise ValueError("Utility linkage probe failed: " + json.dumps(result))
    return result


def immutable(path, suffix):
    data = path.read_bytes()
    digest = utility_runtime.sha(data)
    output = WORK / "objects" / (digest + suffix)
    output.parent.mkdir(exist_ok=True)
    if not output.exists():
        output.write_bytes(data)
    return {"path": output.relative_to(ROOT).as_posix(), "sha256": digest}


def main():
    if utility_runtime.sha(utility_code.COMPILER.read_bytes()) != utility_code.COMPILER_HASH or utility_runtime.sha(LINKER.read_bytes()) != LINKER_HASH:
        raise ValueError("Utility linkage compiler or linker identity changed")
    WORK.mkdir(parents=True, exist_ok=True)
    probes = {"caller": "extern int target(int);\nint caller(int value) { return target(value) + 1; }\n",
              "target": "int target(int value) { return value; }\n"}
    compile_records, artifacts = [], {}
    for name, text in probes.items():
        source = WORK / (name + ".c")
        source.write_text(text)
        obj = WORK / (name + ".o")
        flags = ["-O2", "-proc", "arm7tdmi", "-interworking", "-inline", "off", "-Cpp_exceptions", "off", "-RTTI", "off"]
        if name == "caller":
            flags.append("-thumb")
        compile_records.append(run([str(utility_code.COMPILER), *flags, "-c", str(source), "-o", str(obj)], WORK))
        artifacts[name] = {"source": immutable(source, ".c"), "object": immutable(obj, ".o"), "flags": flags}
    catalog = utility_bridges.derive()
    with (WORK / "caller.o").open("rb") as stream:
        object_flags = ELFFile(stream)["e_flags"]
    layout, files = utility_runtime.derive()
    modules = {module["id"]: module for module in layout["modules"]}
    matches = []
    for bridge in catalog["bridges"]:
        if bridge["processor"] != "arm7" or bridge["entryMode"] != "thumb" or bridge["targetMode"] != "arm":
            raise ValueError("Utility linkage probe supports only measured ARM7 Thumb-to-ARM regions")
        address, target = int(bridge["address"], 0), int(bridge["targetAddress"], 0)
        directory = WORK / (bridge["module"] + f"-{address:08x}")
        directory.mkdir(exist_ok=True)
        origin = address - 16
        lcf = directory / "linkage.lcf"
        lcf.write_text(f"MEMORY {{\nCALL: ORIGIN = {origin:#x} > caller.bin\nTARGET: ORIGIN = {target:#x} > target.bin\n}}\n"
                       "SECTIONS {\n.caller: { caller.o(.text) } > CALL\n.target: { target.o(.text) } > TARGET\n}\n")
        elf_path = directory / "linked.elf"
        command = [str(LINKER), "-nostdlib", "-nodeadstrip", "-interworking", "-proc", "arm7tdmi", "-main", "caller",
                   str(lcf), str(WORK / "caller.o"), str(WORK / "target.o"), "-o", str(elf_path)]
        attempt = run(command, directory)
        with elf_path.open("rb") as stream:
            elf = ELFFile(stream)
            symbols = list(elf.get_section_by_name(".symtab").iter_symbols())
            veneer = next(symbol for symbol in symbols if symbol.name == "$Ven$$target")
            target_symbol = next(symbol for symbol in symbols if symbol.name == "target")
            if veneer["st_value"] != address or veneer["st_size"] != 12 or target_symbol["st_value"] != target:
                raise ValueError("Generated utility linkage region has the wrong placement, size or target")
            mapping = {symbol.name: symbol["st_value"] for symbol in symbols if symbol.name in ("$a", "$t", "$d") and address <= symbol["st_value"] < address + 12}
            if mapping != {"$t": address, "$a": address + 4, "$d": address + 8}:
                raise ValueError("Generated utility linkage mode mappings differ")
        generated = (directory / "caller.bin").read_bytes()[address - origin:address - origin + 12]
        module = modules[bridge["module"]]
        binary = bytes(files[ROOT / module["binary"]])
        offset = address - int(module["base"], 0)
        native = binary[offset:offset + 12]
        if generated != native or utility_runtime.sha(native) != bridge["sha256"]:
            raise ValueError("Real linker output does not match the complete native linkage unit")
        span = directory / "generated-veneer.bin"
        span.write_bytes(generated)
        unit_name = "linkage_" + bridge["module"].replace("-", "_") + f"_{address:08x}"
        target_name = f"native_utility_child_arm7_arm_{target:08x}"
        unit = directory / (unit_name + ".o")
        utility_linkage_elf.write_unit(generated, target, unit_name, target_name, object_flags, unit)
        with unit.open("rb") as stream:
            elf = ELFFile(stream)
            if elf["e_type"] != "ET_REL" or elf.get_section_by_name(".text").data() != generated[:8] + bytes(4):
                raise ValueError("Relocatable linkage unit contains code beyond the fresh linker span")
            symbols = list(elf.get_section_by_name(".symtab").iter_symbols())
            relocations = list(elf.get_section_by_name(".rela.text").iter_relocations())
            if len(relocations) != 1 or relocations[0]["r_offset"] != 8 or relocations[0]["r_info_type"] != 2 or relocations[0]["r_addend"] != 0 or symbols[relocations[0]["r_info_sym"]].name != target_name:
                raise ValueError("Linkage target must remain one real ABS32 relocation")
        relink_lcf = directory / "relink.lcf"
        relink_lcf.write_text(f"MEMORY {{ REGION: ORIGIN = {address:#x} > veneer.bin }}\nSECTIONS {{\n"
                              f".region: {{ {unit.name}(.text) }} > REGION\n{target_name} = {target:#x};\n}}\n")
        relink_elf = directory / "relinked.elf"
        relink = run([str(LINKER), "-nostdlib", "-nodeadstrip", "-interworking", "-proc", "arm7tdmi", "-main", unit_name,
                      str(relink_lcf), str(unit), "-o", str(relink_elf)], directory)
        if (directory / "veneer.bin").read_bytes() != native:
            raise ValueError("Relocatable linkage-only ELF does not reproduce the complete native region through real linking")
        records = []
        for vector in range(16):
            expected = utility_bridges.execute(native, address, target, vector)
            actual = utility_bridges.execute(generated, address, target, vector)
            if expected != actual:
                raise ValueError("Generated utility linkage native effects differ")
            records.append(expected)
        unit_artifact = immutable(unit, ".o")
        matches.append({**bridge, "name": unit_name, "kind": "linker-regenerated-mixed-mode-linkage-unit", "linkerRegenerated": True,
                        "sourceReconstructed": False, "ordinaryFunctionCredit": 0, "sourceFunctionCredit": 0,
                        "probeCompiler": utility_code.COMPILER.relative_to(ROOT).as_posix(), "probeCompilerSha256": utility_code.COMPILER_HASH,
                        "linker": LINKER.relative_to(ROOT).as_posix(), "linkerSha256": LINKER_HASH,
                        "generatedLinkerSymbol": "$Ven$$target", "generatedModeMappings": {name: hex(value) for name, value in mapping.items()},
                        "linkCommand": attempt, "linkerScript": immutable(lcf, ".lcf"), "linkedElf": immutable(elf_path, ".elf"),
                        "generatedSpan": immutable(span, ".bin"), "exactNativeLinkageBytes": True,
                        "object": unit_artifact["path"], "objectSha256": unit_artifact["sha256"], "generatedCodeBytes": 12,
                        "source": "match_utility_linkage.py", "sourceSha256": utility_runtime.sha(Path(__file__).read_bytes()),
                        "section": ".text", "sectionIndex": 1, "sectionOffset": 0, "sectionFlags": 6, "sectionType": "SHT_PROGBITS",
                        "nativeAlias": "func_" + bridge["module"].replace("-", "_") + f"_{address:08x}",
                        "relocations": [{"offset": 8, "type": 2, "symbol": target_name, "target": hex(target), "targetMode": "arm", "addend": 0}],
                        "nativeSymbolBindings": [{"name": target_name, "program": utility_runtime.PROGRAM, "processor": "arm7", "module": bridge["targetModule"], "address": hex(target), "kind": "function", "mode": "arm"}],
                        "linkageOnlyRelink": {"attempt": relink, "linkerScript": immutable(relink_lcf, ".lcf"), "linkedElf": immutable(relink_elf, ".elf"), "exactBytes": True},
                        "nativeTargetModuleSha256": modules[bridge["targetModule"]]["sha256"],
                        "oracle": {"vectors": 16, "nativeAndGeneratedCalls": 32, "stateSha256": records,
                                   "targetBoundaryReached": True, "targetBodyExecuted": False},
                        "fullProgramLinkedWithReplacement": False})
    report = {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM,
              "runtimeMappingCanonical": True, "linkageMatches": matches, "probeArtifacts": artifacts, "compileCommands": compile_records,
              "generatorSources": [{"path": name, "sha256": utility_runtime.sha((ROOT / name).read_bytes())} for name in ["match_utility_linkage.py", "utility_linkage_elf.py"]],
              "linkerRegeneratedRegions": len(matches), "linkerRegeneratedBytes": sum(entry["bytes"] for entry in matches),
              "originalNativeBridgeInstructionsUsedAsBuildInput": 0, "sourceFunctionCredit": 0,
              "fullProgramLinkedWithReplacement": False, "sourceReconstructionComplete": False,
              "reproduce": ["python", "match_utility_linkage.py"],
              "limitations": ["The normal C caller and identity target are isolated linker probes, not reconstructed native functions, and receive no ROM source credit",
                              "Only linker-generated veneers are compared; no original veneer code, literal instruction words or binary fragments enter the probe build",
                              "Measured qualified native addresses are linkage parameters; the target pointer is resolved by the actual linker",
                              "All target routines remain outside these boundary-only execution tests",
                              "Successful isolated regeneration does not yet prove replacement in the complete linked embedded program",
                              "The pinned compatible linker does not establish historical original-tool attribution"]}
    (ROOT / "evidence/utility/linker-bridges.json").write_text(json.dumps(report, indent=2) + "\n")
    print({"linkerGeneratedRegions": len(matches), "exactLinkageBytes": report["linkerRegeneratedBytes"],
           "nativeAndGeneratedBoundaryCalls": len(matches) * 32, "sourceFunctionCredit": 0})


if __name__ == "__main__":
    main()
