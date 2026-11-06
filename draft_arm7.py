import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys
from pathlib import Path
import match_arm7 as matcher
import match_lowlevel as lowlevel
from abi_slots import preserve_argument_slots
from decompiler_shapes import order_register_locals
from capstone import CS_GRP_CALL

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/lowlevel-recovery/arm7-drafts"
M2C = ROOT / "tools/m2c/m2c-c632946b8cfbe8fce442b522dba92dfa72f1f317/m2c.py"
PRELUDE = matcher.PRELUDE + "typedef unsigned long long u64;\ntypedef signed long long s64;\ntypedef float f32;\ntypedef double f64;\n#define NULL ((void *)0)\n#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))\n"
TOOLS = []
FUNCTIONS = {}
ARGUMENTS = {}
OPTIONS = None


def symbol(spec):
    return "func_" + spec["module"].replace("-", "_") + f"_{spec['address']:08x}"


def argument_counts(specs, forwarded_targets=None):
    forwarded_targets = forwarded_targets or {}
    masks = {spec["address"]: 0 for spec in specs}
    registers = {f"r{index}": 1 << index for index in range(4)}
    for _ in range(6):
        for spec in specs:
            defined, needed = set(), 0
            for instruction in spec["instructions"]:
                reads, writes = instruction.regs_access()
                if instruction.mnemonic.startswith("push") or (instruction.mnemonic.startswith("stmdb") and instruction.op_str.startswith("sp!")):
                    reads = [register for register in reads if instruction.reg_name(register) not in registers]
                for register in reads:
                    name = instruction.reg_name(register)
                    if name in registers and name not in defined:
                        needed |= registers[name]
                if instruction.group(CS_GRP_CALL):
                    destination = instruction.operands[0].imm if instruction.operands else 0
                    target_mask = masks.get(destination, 15)
                    for name, bit in registers.items():
                        if target_mask & bit and name not in defined:
                            needed |= bit
                    if instruction.cc in (0, 15):
                        defined.update(registers)
                if instruction.cc in (0, 15):
                    defined.update(instruction.reg_name(register) for register in writes)
            masks[spec["address"]] |= needed
        for address, target in forwarded_targets.items():
            masks[address] = masks.get(address, 0) | masks.get(target, 15)
    return {address: mask.bit_length() for address, mask in masks.items()}


def assembly(spec):
    name = symbol(spec)
    lines = [".text", ".global " + name, name + ":"]
    targets = {}
    code_end = spec["instructions"][-1].address + 4
    for instruction in spec["instructions"]:
        lines.append(f".L_code_{instruction.address:08x}:")
        mnemonic, operands = instruction.mnemonic, instruction.op_str
        if mnemonic.startswith("push"):
            mnemonic, operands = "stm" + mnemonic[4:] + "db", "sp!, " + operands
        elif mnemonic.startswith("pop"):
            mnemonic, operands = "ldm" + mnemonic[3:] + "ia", "sp!, " + operands
        elif mnemonic in ("lsl", "lsr", "asr", "ror"):
            parts = [part.strip() for part in operands.split(",")]
            mnemonic, operands = "mov", f"{parts[0]}, {parts[1]}, {mnemonic} {parts[2]}"
        if "[pc" in operands and instruction.operands[-1].type == 3:
            location = instruction.address + 8 + instruction.operands[-1].mem.disp
            operands = operands.split(",", 1)[0] + f", .L_pool_{location:08x}"
        if mnemonic.startswith("b") and instruction.operands and instruction.operands[0].type == 2:
            target = instruction.operands[0].imm & 0xFFFFFFFF
            if spec["address"] <= target < code_end:
                operands = f".L_code_{target:08x}"
            else:
                destination = FUNCTIONS.get(target)
                label = symbol(destination) if destination else f"func_arm7_external_{target:08x}"
                targets[label] = target
                operands = label
        lines.append("    " + mnemonic + " " + operands)
    binary = (ROOT / spec["binary"]).read_bytes()
    data = {}
    for location in range(code_end, spec["address"] + spec["bytes"], 4):
        value = int.from_bytes(binary[location - spec["base"]:location - spec["base"] + 4], "little")
        if value & ~1 in FUNCTIONS:
            label = f"func_arm7_pointer_{value:08x}"
            targets[label] = value
        elif 0x02000000 <= value < 0x08000000:
            label = f"data_arm7_{value:08x}"
            data[label] = value
        else:
            label = hex(value)
        lines.append(f".L_pool_{location:08x}: .word {label}")
    declarations = []
    for label, target in targets.items():
        count = ARGUMENTS.get(target & ~1, 4)
        declarations.append("extern u32 " + label + "(" + (", ".join(["u32"] * count) if count else "void") + ");")
    declarations.extend("extern u32 " + label + ";" for label in data)
    return "\n".join(lines) + "\n", targets, data, declarations


def recovered_source(text, spec, targets, data):
    for unknown, scalar in [("M2C_UNK8", "s8"), ("M2C_UNK16", "s16"), ("M2C_UNK32", "s32"), ("M2C_UNK64", "s64"), ("M2C_UNK", "s32")]:
        text = re.sub(r"\b" + unknown + r"\b", scalar, text)
    macros = set(re.findall(r"\bM2C_[A-Z0-9_]+", text)) - {"M2C_FIELD"}
    if macros:
        raise ValueError("Unsupported decompiler operations: " + ", ".join(sorted(macros)))
    name = "native_" + spec["module"].replace("-", "_") + f"_{spec['address']:08x}"
    text = re.sub(r"\b" + symbol(spec) + r"\b", name, text)
    text, added_slots = preserve_argument_slots(text, name)
    if OPTIONS.register_order:
        text = order_register_locals(text, name)
    declarations = []
    for original, target in targets.items():
        label = f"native_arm7_fn_{target:08x}"
        text = re.sub(r"\b" + original + r"\b", label, text)
        if re.search(r"\b" + label + r"\b", text):
            count = ARGUMENTS.get(target & ~1, 4)
            declarations.append("extern u32 " + label + "(" + (", ".join(["u32"] * count) if count else "void") + ");")
    for original, address in data.items():
        label = f"native_arm7_data_{address:08x}"
        text = re.sub(r"\b" + original + r"\b", label, text)
        if re.search(r"\b" + label + r"\b", text):
            declarations.append("extern u32 " + label + ";")
            if OPTIONS.byte_addresses:
                text = re.sub(r"&\s*" + label + r"\b", "(u32) &" + label, text)
    text = PRELUDE + "\n".join(declarations) + "\n" + text
    if OPTIONS.native_scalar_widths:
        from utility_types import scalar_arrays
        widths = scalar_arrays(dict(spec, mode='arm'), {f'native_arm7_data_{address:08x}': address for address in data.values()})
        for label, scalar in widths.items():
            text = text.replace('extern u32 ' + label + ';', 'extern ' + scalar + ' ' + label + ';')
    if OPTIONS.repair_call_prototypes:
        from call_prototypes import recover_call_prototypes
        text, changes = recover_call_prototypes(text)
    if OPTIONS.measured_stack_buffers:
        from refine_utility import stack_buffer_variant
        variants = stack_buffer_variant(text, spec)
        if variants:
            text = variants[0][1]
    if len(text.splitlines()) > 500:
        raise ValueError("Routine needs a source refactor before acceptance under the line limit")
    return text


def research(spec):
    directory = WORK / spec["module"] / f"{spec['address']:08x}"
    directory.mkdir(parents=True, exist_ok=True)
    asm, targets, data, declarations = assembly(spec)
    asm_path = directory / ("native-" + matcher.sha(asm.encode())[:16] + ".s")
    asm_path.write_text(asm)
    result = {"module": spec["module"], "address": hex(spec["address"]), "nativeBytes": spec["bytes"], "draftOnly": True, "variants": []}
    for returns in ("u32", "void"):
        context_text = PRELUDE + "\n".join(declarations) + f"\nextern {returns} {symbol(spec)}();\n"
        context = directory / (returns + "-context-" + matcher.sha(context_text.encode())[:16] + ".c")
        context.write_text(context_text)
        command = [sys.executable, str(M2C), "--target", "arm-mwcc-c", "--context", str(context), "--globals", "none", "--no-cache", "--valid-syntax", "--comment-style", "none", "-f", symbol(spec), str(asm_path)]
        variant = {"returnAssumption": returns, "command": command, "attempts": []}
        result["variants"].append(variant)
        try:
            process = subprocess.run(command, cwd=ROOT, env=dict(os.environ, PYTHONPATH=str(ROOT / "tools/m2c-python")), capture_output=True, text=True, timeout=45)
            variant.update(exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr)
            if process.returncode:
                continue
            source_text = recovered_source(process.stdout, spec, targets, data)
            source = directory / (returns + "-draft-" + matcher.sha(source_text.encode())[:16] + ".c")
            source.write_text(source_text)
            for compiler, digest in TOOLS:
                for level, inline, speed in [(2, "off", False), (2, "noauto", False), (2, "off", True), (3, "off", True), (4, "off", True)]:
                    try:
                        record, code = matcher.compare(source, spec, compiler, digest, level, inline, speed)
                    except lowlevel.UnresolvedNativeSymbol as error:
                        variant["attempts"].append(error.details)
                        continue
                    variant["attempts"].append(record)
                    if code is not None:
                        result.update(match=record, draftSource=source.relative_to(ROOT).as_posix())
                        return result
        except Exception as error:
            variant["failure"] = f"{type(error).__name__}: {error}"
    return result


def validate(match, spec, source):
    flags = match["compilerFlags"]
    entry, code = matcher.compare(source, spec, ROOT / match["compiler"], match["compilerSha256"], int(flags[0][2:]), flags[flags.index("-inline") + 1], "speed" in flags)
    if code is None:
        raise ValueError("Accepted ARM7 draft stopped matching after source promotion")
    shape = {"kind": "recovered-c", "callees": {rel["symbol"]: int(rel["target"], 0) for rel in entry["relocations"] if rel["symbol"].startswith("native_arm7_fn_")}}
    try:
        entry["oracle"] = matcher.oracle(code, spec, shape)
    except Exception as error:
        entry["oracle"] = {"supported": False, "failure": f"{type(error).__name__}: {error}", "limitation": "Full byte/relocation equality is established; a broader native runtime model is still required for behavioral execution"}
    return entry


def main():
    global TOOLS, FUNCTIONS, ARGUMENTS, OPTIONS
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", default="translated02")
    parser.add_argument("--limit", type=int, default=120)
    parser.add_argument("--max-bytes", type=int, default=512)
    parser.add_argument("--min-bytes", type=int, default=0)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--all-compilers", action="store_true")
    parser.add_argument("--byte-addresses", action="store_true")
    parser.add_argument("--address-file", type=Path)
    parser.add_argument("--register-order", action="store_true")
    parser.add_argument("--native-scalar-widths", action="store_true")
    parser.add_argument("--repair-call-prototypes", action="store_true")
    parser.add_argument("--measured-stack-buffers", action="store_true")
    parser.add_argument("--abi-hints", action="store_true")
    OPTIONS = parser.parse_args()
    path = ROOT / f"evidence/matches/arm7-{OPTIONS.batch}.json"
    if OPTIONS.verify:
        report = json.loads(path.read_text())
        matches = []
        for match in report["matches"]:
            source = ROOT / match["source"]
            if matcher.sha(source.read_bytes()) != match["sourceSha256"]:
                raise ValueError("Accepted ARM7 source changed")
            matches.append(validate(match, matcher.accepted_spec(match), source))
        report["matches"] = matches
        path.write_text(json.dumps(report, indent=2) + "\n")
        print({"verified": len(matches), "bytes": sum(match["bytes"] for match in matches)})
        return
    specs = matcher.candidates(10000)
    FUNCTIONS = {spec["address"]: spec for spec in specs}
    ARGUMENTS = argument_counts(specs)
    if OPTIONS.abi_hints:
        from utility_abi import argument_hints
        ARGUMENTS = argument_hints(specs)[0]
    TOOLS = matcher.tools()
    if not OPTIONS.all_compilers:
        TOOLS = TOOLS[:1]
    if path.exists():
        raise ValueError("Select a new ARM7 research batch")
    accepted = {int(item["address"], 0) for report in (ROOT / "evidence/matches").glob("arm7-*.json") for item in json.loads(report.read_text()).get("matches", [])}
    requested = {int(value, 0) for value in json.loads(OPTIONS.address_file.read_text())} if OPTIONS.address_file else None
    selected = sorted((spec for spec in specs if spec["address"] not in accepted and OPTIONS.min_bytes <= spec["bytes"] <= OPTIONS.max_bytes
                       and (requested is None or spec["address"] in requested)), key=lambda spec: spec["bytes"])[:OPTIONS.limit]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(research, selected):
            results.append(result)
            print({"module": result["module"], "address": result["address"], "bytes": result["nativeBytes"], "matched": "match" in result}, flush=True)
    matches = []
    for result in results:
        if "match" not in result:
            continue
        old = result["match"]
        source = ROOT / f"src/arm7/{OPTIONS.batch}/{old['name']}.c"
        if source.exists():
            raise ValueError("Refusing to change an accepted ARM7 source")
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes((ROOT / result["draftSource"]).read_bytes())
        matches.append(validate(old, FUNCTIONS[int(old["address"], 0)], source))
    report = {"schemaVersion": 1, "romSha256": matcher.sha((ROOT / "inputs/game.nds").read_bytes()), "processor": "arm7", "runtimeMappingCanonical": True,
              "matches": matches, "nativeSymbols": {rel["symbol"]: rel["target"] for entry in matches for rel in entry["relocations"]},
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "limitations": ["Register-argument count and return assumptions are provisional; accepted code must match all native bytes after declared relocations", "Matching compiler configurations do not establish historical original compiler identity", "All rejected drafts and unsupported behavioral paths remain recorded"]}
    attempt_path = ROOT / f"evidence/attempts/arm7-{OPTIONS.batch}.json"
    attempt_path.parent.mkdir(parents=True, exist_ok=True)
    attempt_path.write_text(json.dumps(results, indent=2) + "\n")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print({"matched": len(matches), "bytes": sum(match["bytes"] for match in matches), "drafts": len(results)})


if __name__ == "__main__":
    main()
