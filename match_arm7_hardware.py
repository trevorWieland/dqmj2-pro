import hashlib
import json
import os
import subprocess
from pathlib import Path
import match_arm7 as common
import match_lowlevel
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP

ROOT = Path(__file__).resolve().parent
ASSEMBLER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwasmarm.exe"
EXPECTED = "e928cbcce71d687fadf25cf426280f23252e2aaae897fc2ce4e5570d8554dc8c"
WORK = ROOT / "work/lowlevel-recovery/arm7-hardware"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def specs():
    previous = ROOT / "evidence/matches/arm7-hardware01.json"
    if previous.exists():
        return [common.accepted_spec(entry, instructions=True) for entry in json.loads(previous.read_text())["matches"]]
    rows = common.candidates(128)
    inventory = json.loads((ROOT / "evidence/arm7/ghidra-runtime-inventory.json").read_text())
    layout = json.loads((ROOT / "evidence/arm7/runtime-layout.json").read_text())
    modules = {module["id"]: module for module in layout["modules"]}
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    decoder.detail = True
    for function in inventory["functions"]:
        if function["mode"] != "thumb" or len(function["ranges"]) != 1 or function["bodyBytes"] > 32:
            continue
        module = modules[function["module"]]
        address, base = int(function["address"], 0), int(module["runtimeBase"], 0)
        binary = (ROOT / module["binary"]).read_bytes()
        code = binary[address - base:address - base + function["bodyBytes"]]
        rows.append({"module": module["id"], "mode": "thumb", "address": address, "base": base,
                     "binary": module["binary"], "bytes": len(code), "instructions": list(decoder.disasm(code, address)),
                     "pools": {}, "inputModuleSha256": module["sha256"], "boundaryEvidence": "Mapped ARM7 Thumb BIOS wrapper body"})
    return rows


def source_for(spec):
    instructions = spec["instructions"]
    hardware = [instruction for instruction in instructions if instruction.mnemonic in ("mrs", "msr", "svc", "swi", "swp", "swpb")]
    if not hardware or any(instruction.group(CS_GRP_CALL) for instruction in instructions):
        return None
    if any(instruction.group(CS_GRP_JUMP) and instruction.op_str != "lr" for instruction in instructions):
        return None
    name = "native_" + spec["module"].replace("-", "_") + f"_hw_{spec['address']:08x}"
    mode = spec.get("mode", "arm")
    lines = [".section .text", "." + mode, ".global " + name, ".type " + name + ", @function", name + ":"]
    for instruction in instructions:
        mnemonic, operands = instruction.mnemonic, instruction.op_str.replace("apsr", "cpsr")
        if mnemonic == "svc":
            mnemonic = "swi"
            operands = operands.replace("#", "")
        if mnemonic in ("stm", "ldm"):
            mnemonic += "ia"
        if mode == "thumb" and mnemonic in ("movs", "adds", "subs"):
            mnemonic = mnemonic[:-1]
        if "[pc" in operands:
            pool = instruction.address + 8 + instruction.operands[-1].mem.disp
            operands = operands.split(",", 1)[0] + f", local_pool_{pool:08x}"
        lines.append("    " + mnemonic + " " + operands)
    for location, value in sorted(spec["pools"].items()):
        lines.append(f"local_pool_{location:08x}: .word {value:#x}")
    lines.append(".size " + name + ", .-" + name)
    reason = "Thumb ARM7 BIOS service wrapper uses a supervisor-call instruction; the service implementation is external to the ROM" if any(instruction.mnemonic in ("svc", "swi") for instruction in hardware) else "ARM7 kernel processor-state or atomic-swap instructions require privileged architectural behavior not expressible in ordinary C"
    return name, "\n".join(lines) + "\n", reason


def main():
    if sha(ASSEMBLER.read_bytes()) != EXPECTED:
        raise ValueError("ARM7 hardware assembler identity differs")
    WORK.mkdir(parents=True, exist_ok=True)
    previous = ROOT / "evidence/matches/arm7-hardware01.json"
    expected_names = {entry["name"] for entry in json.loads(previous.read_text())["matches"]} if previous.exists() else None
    matches, attempts = [], []
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat"))
    for spec in specs():
        generated = source_for(spec)
        if generated is None:
            continue
        name, text, reason = generated
        trial = WORK / (name + ".s")
        trial.write_text(text)
        obj = WORK / (name + ".o")
        flags = ["-proc", "arm4t", "-c"]
        command = [str(ASSEMBLER), *flags, str(trial), "-o", str(obj)]
        result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=30)
        attempt = {"name": name, "command": command, "exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
        attempts.append(attempt)
        if result.returncode:
            continue
        with obj.open("rb") as stream:
            elf = common.ELFFile(stream)
            symbol = next(symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols() if symbol.name == name)
            code = elf.get_section(symbol["st_shndx"]).data()
            relocations = [section for section in elf.iter_sections() if section["sh_type"] in ("SHT_REL", "SHT_RELA") and section["sh_size"]]
            index, value = symbol["st_shndx"], symbol["st_value"]
        binary = (ROOT / spec["binary"]).read_bytes()
        native = binary[spec["address"] - spec["base"]:spec["address"] - spec["base"] + spec["bytes"]]
        attempt["exactBytes"] = code == native and not relocations
        if not attempt["exactBytes"]:
            attempt.update(nativeHex=native.hex(), compiledHex=code.hex())
            continue
        source = ROOT / f"src/arm7/hardware01/{name}.s"
        source.parent.mkdir(parents=True, exist_ok=True)
        if source.exists() and source.read_text() != text:
            raise ValueError("Refusing to alter accepted ARM7 hardware source")
        source.write_text(text)
        final = WORK / ("final-" + name + ".o")
        result = subprocess.run([str(ASSEMBLER), *flags, str(source), "-o", str(final)], cwd=ROOT, env=environment, capture_output=True, timeout=30)
        result.check_returncode()
        object_hash = sha(final.read_bytes())
        stable = WORK / (object_hash + ".o")
        if not stable.exists():
            stable.write_bytes(final.read_bytes())
        record = {"name": name, "module": spec["module"], "processor": "arm7", "mode": spec.get("mode", "arm"),
                  "address": hex(spec["address"]), "bytes": spec["bytes"], "compiledBytes": len(code), "matchingBytes": len(code),
                  "exactBytes": True, "nativeAlias": "func_" + spec["module"].replace("-", "_") + f"_{spec['address']:08x}",
                  "inputModuleSha256": spec["inputModuleSha256"],
                  "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha(source.read_bytes()),
                  "object": stable.relative_to(ROOT).as_posix(), "objectSha256": object_hash,
                  "compilerSha256": EXPECTED, "assemblerSha256": EXPECTED, "compilerFlags": flags,
                  "sectionIndex": index, "sectionOffset": value, "targetSha256": sha(native), "outputSha256": sha(code), "relocations": [],
                  "assemblyJustification": reason, "reconstructionKind": "justified-hardware-assembly", "linked": False}
        if any(instruction.mnemonic in ("svc", "swi") for instruction in spec["instructions"]):
            record["oracle"] = {"supported": False, "reason": "Original ARM7 BIOS service implementation is not present in the ROM; service effects are not claimed"}
        else:
            shape = {"cpsrMode": 0x13, "argumentValues": {"0": [0, 0x80, 0x40, 0xC0]}}
            if any(instruction.mnemonic == "swp" for instruction in spec["instructions"]):
                shape = {"cpsrMode": 0x13, "argumentPointerRegisters": [1]}
            try:
                record["oracle"] = common.oracle(code, spec, shape)
            except Exception as error:
                record["oracle"] = {"supported": False, "reason": f"{type(error).__name__}: {error}"}
        matches.append(record)
    if expected_names is not None and {entry["name"] for entry in matches} != expected_names:
        raise ValueError("ARM7 hardware verification must preserve every accepted source unit")
    report = {"schemaVersion": 1, "romSha256": sha((ROOT / "inputs/game.nds").read_bytes()), "processor": "arm7",
              "runtimeMappingCanonical": True, "matches": matches, "attempts": attempts, "nativeSymbols": {},
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "limitations": ["Only measured BIOS, processor-state and atomic hardware wrappers use assembly", "No ordinary game logic is promoted as disassembly", "Unsupported external BIOS and physical-platform effects remain explicit"]}
    path = ROOT / "evidence/matches/arm7-hardware01.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    print({"matched": len(matches), "bytes": sum(entry["bytes"] for entry in matches), "attempts": len(attempts)})


if __name__ == "__main__":
    main()
