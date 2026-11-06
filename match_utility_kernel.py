import argparse
import json
import os
import re
import subprocess
from pathlib import Path
import utility_code
import utility_oracle
import utility_runtime
import match_utility_hardware
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/lowlevel-recovery/utility-kernel"


def source_for(spec):
    instructions = spec["instructions"]
    hardware = [instruction for instruction in instructions if instruction.mnemonic.startswith(("mrs", "msr", "mcr", "mrc", "swp", "svc", "swi"))]
    if not hardware or any(instruction.group(CS_GRP_CALL) for instruction in instructions):
        return None
    last = instructions[-1]
    returned = last.mnemonic == "bx" and last.op_str == "lr" or last.mnemonic.startswith(("pop", "ldm")) and "pc" in last.op_str or last.mnemonic.startswith(("mov", "sub")) and last.op_str.startswith("pc, lr")
    if not returned:
        return None
    name = "native_" + spec["module"].replace("-", "_") + f"_hw_{spec['address']:08x}"
    mapping = {instruction.address: instruction for instruction in instructions}
    binary = (ROOT / spec["binary"]).read_bytes()
    if utility_runtime.sha(binary) != spec["inputModuleSha256"]:
        raise ValueError("Utility kernel input module differs from the measured embedded program")
    lines = [".section .text", "." + spec["mode"], ".global " + name, ".type " + name + ", @function", name + ":"]
    cursor = spec["address"]
    while cursor < spec["address"] + spec["bytes"]:
        if cursor in spec["pools"]:
            if cursor in mapping:
                return None
            lines.append(f"local_{cursor:08x}: .word {spec['pools'][cursor]:#x}")
            cursor += 4
            continue
        if cursor not in mapping:
            if spec["mode"] == "thumb" and binary[cursor - spec["base"]:cursor - spec["base"] + 2] == b"\xc0\x46":
                lines.append(f"local_{cursor:08x}: mov r8, r8")
                cursor += 2
                continue
            return None
        instruction = mapping[cursor]
        mnemonic, operands = instruction.mnemonic, instruction.op_str.replace("apsr", "cpsr")
        if mnemonic in ("svc", "swi"):
            mnemonic, operands = "swi", operands.replace("#", "")
        if re.fullmatch(r"(?:stm|ldm)(?:eq|ne|lt|ge|gt|le|mi|pl|lo|hs|vs|vc|hi|ls)?", mnemonic):
            mnemonic += "ia"
        if spec["mode"] == "thumb" and mnemonic in ("movs", "adds", "subs"):
            mnemonic = mnemonic[:-1]
        if mnemonic in ("mrc", "mcr"):
            operands = operands.replace("#", "")
        if "[pc" in operands:
            target = ((cursor + 4) & ~3 if spec["mode"] == "thumb" else cursor + 8) + instruction.operands[-1].mem.disp
            operands = operands.split(",", 1)[0] + f", local_{target:08x}"
        if instruction.group(CS_GRP_JUMP) and instruction.operands and instruction.operands[0].type == 2:
            target = instruction.operands[0].imm
            if target not in mapping:
                return None
            operands = f"local_{target:08x}"
        lines.extend([f"local_{cursor:08x}:", "    " + mnemonic + " " + operands])
        cursor += instruction.size
    lines.append(".size " + name + ", .-" + name)
    return name, "\n".join(lines) + "\n", hardware


def compile_source(source, name, spec):
    flags = ["-proc", "arm5TE" if spec["processor"] == "arm9" else "arm4t", "-c"]
    obj = WORK / (name + ".o")
    command = [str(match_utility_hardware.ASSEMBLER), *flags, str(source), "-o", str(obj)]
    process = subprocess.run(command, cwd=ROOT, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat")),
                             capture_output=True, text=True, timeout=30)
    attempt = {"command": command, "exitCode": process.returncode, "stdout": process.stdout, "stderr": process.stderr}
    if process.returncode:
        return attempt, None
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        symbol = next(symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols() if symbol.name == name)
        section = elf.get_section(symbol["st_shndx"])
        output = section.data()
        if any(rel["sh_type"] in ("SHT_REL", "SHT_RELA") and rel["sh_size"] and rel["sh_info"] == symbol["st_shndx"] for rel in elf.iter_sections()):
            raise ValueError("Utility kernel unit has an undeclared runtime relocation")
    binary = (ROOT / spec["binary"]).read_bytes()
    if utility_runtime.sha(binary) != spec["inputModuleSha256"]:
        raise ValueError("Utility kernel native target module hash changed")
    native = binary[spec["address"] - spec["base"]:spec["address"] - spec["base"] + spec["bytes"]]
    if output != native or symbol["st_size"] != spec["bytes"]:
        attempt.update(exactBytes=False, nativeBytes=len(native), compiledBytes=len(output))
        return attempt, None
    digest = utility_runtime.sha(obj.read_bytes())
    stable = WORK / "objects" / (digest + ".o")
    stable.parent.mkdir(exist_ok=True)
    if not stable.exists():
        stable.write_bytes(obj.read_bytes())
    entry = {"name": name, "program": utility_runtime.PROGRAM, "processor": spec["processor"], "module": spec["module"],
             "address": hex(spec["address"]), "mode": spec["mode"], "bytes": spec["bytes"], "size": spec["bytes"],
             "compiledBytes": len(output), "matchingBytes": len(output), "exactAfterDeclaredRelocation": True,
             "nativeAlias": "func_" + spec["module"].replace("-", "_") + f"_{spec['address']:08x}",
             "source": source.relative_to(ROOT).as_posix(), "sourceSha256": utility_runtime.sha(source.read_bytes()),
             "object": stable.relative_to(ROOT).as_posix(), "objectSha256": digest,
             "compiler": match_utility_hardware.ASSEMBLER.relative_to(ROOT).as_posix(),
             "compilerSha256": match_utility_hardware.ASSEMBLER_HASH, "assemblerSha256": match_utility_hardware.ASSEMBLER_HASH,
             "compilerFlags": flags, "relocations": [], "sectionIndex": symbol["st_shndx"], "sectionOffset": symbol["st_value"] & ~1,
             "targetSha256": utility_runtime.sha(native), "outputSha256": utility_runtime.sha(output), "inputModuleSha256": spec["inputModuleSha256"], "linked": False}
    return attempt, (entry, output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", default="kernel01")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if utility_runtime.sha(match_utility_hardware.ASSEMBLER.read_bytes()) != match_utility_hardware.ASSEMBLER_HASH:
        raise ValueError("Utility kernel assembler identity changed")
    WORK.mkdir(parents=True, exist_ok=True)
    path = ROOT / f"evidence/matches/utility-{args.batch}.json"
    previous = json.loads(path.read_text()) if args.verify else None
    specs = {(entry["module"], int(entry["address"], 0)): utility_code.accepted_spec(entry) for entry in previous["matches"]} if previous else {(spec["module"], spec["address"]): spec for spec in utility_code.candidates()}
    accepted = {(entry["module"], int(entry["address"], 0)) for report in (ROOT / "evidence/matches").glob("utility-*.json") for entry in json.loads(report.read_text()).get("matches", [])}
    selected = [specs[(entry["module"], int(entry["address"], 0))] for entry in previous["matches"]] if previous else [spec for key, spec in specs.items() if key not in accepted and spec["bytes"] <= 128]
    if not args.verify and path.exists():
        raise ValueError("Choose a new utility kernel batch")
    matches, attempts = [], []
    for spec in selected:
        if args.verify:
            expected = next(entry for entry in previous["matches"] if entry["module"] == spec["module"] and int(entry["address"], 0) == spec["address"])
            name = expected["name"]
            source = ROOT / expected["source"]
            hardware = expected["assemblyJustification"]["instructions"]
            if utility_runtime.sha(source.read_bytes()) != expected["sourceSha256"]:
                raise ValueError("Accepted utility kernel source changed")
        else:
            generated = source_for(spec)
            if generated is None:
                continue
            name, text, operations = generated
            hardware = [instruction.mnemonic + " " + instruction.op_str for instruction in operations]
            source = WORK / (name + ".s")
            source.write_text(text)
        attempt, result = compile_source(source, name, spec)
        attempts.append(attempt)
        if result is None:
            continue
        if not args.verify:
            frozen = ROOT / f"src/utility/{args.batch}/{name}.s"
            frozen.parent.mkdir(parents=True, exist_ok=True)
            if frozen.exists():
                raise ValueError("Refusing to alter accepted utility kernel source")
            frozen.write_bytes(source.read_bytes())
            source = frozen
            attempt, result = compile_source(source, name, spec)
            if result is None:
                raise ValueError("Promoted kernel source stopped matching")
        entry, output = result
        entry["assemblyJustification"] = {"kind": "dedicated-processor-state-cache-atomic-or-bios-primitive",
                                           "instructions": hardware,
                                           "sourceFormat": "mnemonic-assembly", "normalGameLogicFallback": False}
        if any(instruction.split()[0] in ("svc", "swi") for instruction in hardware):
            entry["oracle"] = {"supported": False, "reason": "BIOS service implementation is external to the ROM and not emulated here"}
        else:
            try:
                entry["oracle"] = utility_oracle.oracle(output, spec)
                entry["oracle"]["limitations"].append("Physical cache/controller/co-processor effects remain unproven by isolated architectural emulation")
            except Exception as error:
                entry["oracle"] = {"supported": False, "failure": f"{type(error).__name__}: {error}", "limitation": "Only full native byte equivalence is established for this privileged primitive"}
        matches.append(entry)
    report = {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM,
              "runtimeMappingCanonical": True, "matches": matches, "nativeSymbols": {}, "attempts": attempts,
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "limitations": ["Assembly is limited to measured dedicated architectural/BIOS primitives with no native calls",
                              "All literal words are actual PC-relative data loads; normal game logic is excluded",
                              "Cache, IRQ, BIOS and physical-device effects are not asserted by static or bounded emulator equality"]}
    path.write_text(json.dumps(report, indent=2) + "\n")
    print({"functions": len(matches), "bytes": sum(entry["bytes"] for entry in matches),
           "oracleCalls": sum(entry["oracle"].get("nativeAndRecompiledCalls", 0) for entry in matches)})


if __name__ == "__main__":
    main()
