import json
from pathlib import Path
import utility_code
import utility_runtime
import utility_oracle
import match_utility_kernel
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_GRP_CALL, CS_GRP_JUMP

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/lowlevel-recovery/utility-io"
TARGETS = {0x027F7BCC: 64, 0x027F7C0C: 52}


def main():
    assembler = match_utility_kernel.match_utility_hardware.ASSEMBLER
    if utility_runtime.sha(assembler.read_bytes()) != match_utility_kernel.match_utility_hardware.ASSEMBLER_HASH:
        raise ValueError("Utility IO assembler changed")
    path = ROOT / "evidence/matches/utility-io01.json"
    previous = json.loads(path.read_text()) if path.exists() else None
    if previous:
        specs = {}
        decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
        decoder.detail = True
        for entry in previous["matches"]:
            spec = utility_code.accepted_spec(entry)
            payload = (ROOT / spec["binary"]).read_bytes()
            offset = spec["address"] - spec["base"]
            spec.update(instructions=list(decoder.disasm(payload[offset:offset + spec["bytes"]], spec["address"])), pools={})
            specs[(spec["module"], spec["address"])] = spec
    else:
        specs = {(spec["module"], spec["address"]): spec for spec in utility_code.candidates()}
    matches, attempts = [], []
    WORK.mkdir(parents=True, exist_ok=True)
    match_utility_kernel.WORK = WORK
    for address, size in TARGETS.items():
        spec = specs[("utility-child-arm7-main", address)]
        instructions = spec["instructions"]
        if spec["mode"] != "arm" or spec["bytes"] != size or spec["pools"] or [(instruction.mnemonic, instruction.op_str) for instruction in instructions[:2]] != [("mov", "ip, #0x4000000"), ("add", "ip, ip, #0x138")]:
            raise ValueError("Utility IO primitive is not the measured direct hardware leaf")
        allowed = {"mov", "add", "sub", "subs", "bic", "orr", "ldrh", "strh", "bne", "bx"}
        if any(instruction.mnemonic not in allowed or instruction.group(CS_GRP_CALL) for instruction in instructions):
            raise ValueError("Utility IO source would exceed the dedicated hardware protocol scope")
        if any(instruction.mnemonic in ("ldrh", "strh") and instruction.op_str != "r0, [ip]" for instruction in instructions):
            raise ValueError("Utility IO primitive touches non-protocol memory")
        name = "native_utility_child_arm7_main_io_" + f"{address:08x}"
        lines = [".section .text", ".arm", ".global " + name, ".type " + name + ", @function", name + ":"]
        for instruction in instructions:
            operands = instruction.op_str
            if instruction.group(CS_GRP_JUMP) and instruction.operands and instruction.operands[0].type == 2:
                target = instruction.operands[0].imm
                if not address <= target < address + size:
                    raise ValueError("Utility IO leaf has an external control-flow target")
                operands = f"local_{target:08x}"
            lines.extend([f"local_{instruction.address:08x}:", "    " + instruction.mnemonic + " " + operands])
        lines.append(".size " + name + ", .-" + name)
        text = "\n".join(lines) + "\n"
        source = ROOT / "src/utility/io01" / (name + ".s")
        source.parent.mkdir(exist_ok=True)
        if previous:
            expected = next(entry for entry in previous["matches"] if entry["name"] == name)
            if source.read_text() != text or utility_runtime.sha(source.read_bytes()) != expected["sourceSha256"]:
                raise ValueError("Frozen utility IO hardware source changed")
        elif source.exists():
            raise ValueError("Refusing to overwrite utility IO source")
        else:
            source.write_text(text)
        attempt, result = match_utility_kernel.compile_source(source, name, spec)
        attempts.append(attempt)
        if result is None:
            raise ValueError("Utility IO hardware leaf no longer matches its complete native span")
        entry, compiled = result
        entry["assemblyJustification"] = {"kind": "direct-fixed-register-hardware-pulse-and-measured-delay-loop",
                                           "memoryRegister": "0x04000138", "spinLoopInitialCount": 2,
                                           "reason": "This leaf performs ordered halfword device reads/writes and bit transitions separated by exact register-only delay loops; ordinary C does not specify that instruction timing or leaf register/flag contract",
                                           "normalGameLogicFallback": False, "historicalOriginalSourceLanguageAsserted": False}
        entry["oracle"] = utility_oracle.oracle(compiled, spec)
        matches.append(entry)
    report = {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM,
              "runtimeMappingCanonical": True, "matches": matches, "attempts": attempts, "nativeSymbols": {}, "nativeSymbolBindings": [],
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "reproduce": ["python", "match_utility_io.py"],
              "limitations": ["Assembly is restricted to these two measured direct device-interface primitives, not ordinary memory or game logic",
                              "Only native-equivalent register/flag state and ordered synthetic MMIO memory effects are tested; physical device responses and elapsed hardware cycles are not asserted",
                              "All instructions are real assembler mnemonics; no instruction-word or binary source substitution is used"]}
    path.write_text(json.dumps(report, indent=2) + "\n")
    print({"hardwareLeaves": len(matches), "bytes": sum(entry["bytes"] for entry in matches),
           "nativeAndCompiledCalls": sum(entry["oracle"]["nativeAndRecompiledCalls"] for entry in matches)})


if __name__ == "__main__":
    main()
