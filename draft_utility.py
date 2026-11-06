import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys
from pathlib import Path
import utility_code as matcher
import utility_oracle
import utility_runtime
import utility_bridges
from abi_slots import preserve_argument_slots
from decompiler_shapes import order_register_locals
from draft_arm7 import argument_counts
from utility_abi import argument_hints
from utility_types import scalar_arrays, fixed_work_area, fixed_references
from utility_shapes import reverse_register_locals
from narrow_increments import canonical_byte_increments
from typed_global_fields import recover_global_records
from match_utility_primitives import native_bindings
from capstone import CS_GRP_CALL, CS_GRP_JUMP

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/lowlevel-recovery/utility-drafts"
M2C = ROOT / "tools/m2c/m2c-c632946b8cfbe8fce442b522dba92dfa72f1f317/m2c.py"
PRELUDE = "typedef unsigned char u8;\ntypedef signed char s8;\ntypedef unsigned short u16;\ntypedef signed short s16;\ntypedef unsigned int u32;\ntypedef signed int s32;\ntypedef unsigned long long u64;\ntypedef signed long long s64;\n#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))\n"
FUNCTIONS = {}
ARGUMENTS = {}
OPTIONS = None


def symbol(spec):
    return "func_" + spec["module"].replace("-", "_") + f"_{spec['address']:08x}"


def assembly(spec):
    functions = FUNCTIONS[spec["processor"]]
    counts = ARGUMENTS[spec["processor"]]
    name = symbol(spec)
    lines = [".text", ".global " + name, name + ":"]
    targets, data = {}, {}
    code_end = spec["instructions"][-1].address + spec["instructions"][-1].size
    for instruction in spec["instructions"]:
        lines.append(f".L_code_{instruction.address:08x}:")
        mnemonic, operands = instruction.mnemonic, instruction.op_str
        if mnemonic.startswith("push"):
            mnemonic, operands = "stm" + mnemonic[4:] + "db", "sp!, " + operands
        elif mnemonic.startswith("pop"):
            mnemonic, operands = "ldm" + mnemonic[3:] + "ia", "sp!, " + operands
        if spec["mode"] == "thumb" and mnemonic in ("adds", "subs", "movs", "muls", "lsls", "lsrs", "asrs"):
            mnemonic = mnemonic[:-1]
        if mnemonic in ("add", "sub") and len(operands.split(",")) == 2:
            first, second = operands.split(",", 1)
            operands = first + ", " + first + "," + second
        if mnemonic in ("lsl", "lsr", "asr", "ror"):
            parts = [part.strip() for part in operands.split(",")]
            if len(parts) == 2:
                parts.insert(1, parts[0])
            mnemonic, operands = "mov", f"{parts[0]}, {parts[1]}, {mnemonic} {parts[2]}"
        if mnemonic == "mul" and len(operands.split(",")) == 2:
            operands += ", " + operands.split(",", 1)[0]
        if "[pc" in operands and instruction.operands[-1].type == 3:
            location = ((instruction.address + 4) & ~3 if spec["mode"] == "thumb" else instruction.address + 8) + instruction.operands[-1].mem.disp
            operands = operands.split(",", 1)[0] + f", .L_pool_{location:08x}"
        if (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)) and instruction.operands and instruction.operands[0].type == 2:
            target = instruction.operands[0].imm & 0xFFFFFFFF
            if spec["address"] <= target < code_end:
                operands = f".L_code_{target:08x}"
            else:
                destination = functions.get(target & ~1)
                mode = destination["mode"] if destination else ("arm" if mnemonic.startswith("blx") and spec["mode"] == "thumb" else spec["mode"])
                label = f"func_utility_{spec['processor']}_{mode}_{target:08x}"
                targets[label] = (target, mode)
                operands = label
        lines.append("    " + mnemonic + " " + operands)
    binary = (ROOT / spec["binary"]).read_bytes()
    for location in range((code_end + 3) & ~3, spec["address"] + spec["bytes"], 4):
        value = int.from_bytes(binary[location - spec["base"]:location - spec["base"] + 4], "little")
        if value & ~1 in functions:
            mode = "thumb" if value & 1 else "arm"
            label = f"func_utility_{spec['processor']}_{mode}_{value:08x}"
            targets[label] = (value, mode)
        elif 0x01FF8000 <= value < 0x08000000:
            label = f"data_utility_{spec['processor']}_{value:08x}"
            data[label] = value
        else:
            label = hex(value)
        lines.append(f".L_pool_{location:08x}: .word {label}")
    declarations = []
    for label, (target, mode) in targets.items():
        count = counts.get(target & ~1, 4)
        declarations.append("extern u32 " + label + "(" + (", ".join(["u32"] * count) if count else "void") + ");")
    data_types = scalar_arrays(spec, data) if OPTIONS.scalar_globals else {label: "u8" for label in data}
    declarations.extend("extern " + data_types[label] + " " + label + "[];" for label in data)
    return "\n".join(lines) + "\n", targets, data, declarations


def recovered_source(text, spec, targets, data):
    for unknown, scalar in [("M2C_UNK8", "s8"), ("M2C_UNK16", "s16"), ("M2C_UNK32", "s32"), ("M2C_UNK64", "s64"), ("M2C_UNK", "s32")]:
        text = re.sub(r"\b" + unknown + r"\b", scalar, text)
    if set(re.findall(r"\bM2C_[A-Z0-9_]+", text)) - {"M2C_FIELD"}:
        raise ValueError("Utility draft contains untranslated decompiler operations")
    text = re.sub(r"\b" + symbol(spec) + r"\b", spec["name"], text)
    text, slots = preserve_argument_slots(text, spec["name"])
    if OPTIONS.register_order:
        text = order_register_locals(text, spec["name"])
    if OPTIONS.reverse_register_order:
        text = reverse_register_locals(text, spec["name"])
    declarations = []
    for original, (target, mode) in targets.items():
        label = f"native_utility_child_{spec['processor']}_{mode}_{target:08x}"
        text = re.sub(r"\b" + original + r"\b", label, text)
        if re.search(r"\b" + label + r"\b", text):
            count = ARGUMENTS[spec["processor"]].get(target & ~1, 4)
            declarations.append("extern u32 " + label + "(" + (", ".join(["u32"] * count) if count else "void") + ");")
    data_types = scalar_arrays(spec, data) if OPTIONS.scalar_globals else {label: "u8" for label in data}
    for original, target in data.items():
        label = f"native_utility_child_{spec['processor']}_data_{target:08x}"
        text = re.sub(r"\b" + original + r"\b", label, text)
        if re.search(r"\b" + label + r"\b", text):
            if OPTIONS.fixed_work_areas and fixed_work_area(spec, target):
                declarations.append(f"#define {label} ((volatile {data_types[original]} *){target:#x})")
            else:
                declarations.append("extern " + data_types[original] + " " + label + "[];")
    text = PRELUDE + "\n".join(declarations) + "\n" + text
    if OPTIONS.direct_increments:
        text, changes = canonical_byte_increments(text)
    if OPTIONS.typed_globals:
        text, changes = recover_global_records(text)
    if len(text.splitlines()) > 500:
        raise ValueError("Utility C requires a semantic source refactor before satisfying the line limit")
    return text


def validate(entry, spec):
    source = ROOT / entry["source"]
    flags = entry["compilerFlags"]
    spec = dict(spec, compilerPath=ROOT / entry["compiler"], compilerProc=flags[flags.index("-proc") + 1], interworking="-nointerworking" not in flags)
    record, code = matcher.compile_compare(source, spec, int(flags[0][2:]), flags[flags.index("-inline") + 1], "speed" in flags)
    if code is None:
        raise ValueError("Accepted utility C draft stopped matching")
    for key in ("fixedWorkAreaReferences",):
        if key in entry:
            record[key] = entry[key]
    text = source.read_text()
    references = fixed_references(text, spec)
    if references:
        record["fixedWorkAreaReferences"] = references
    pointer_registers = {int(index) for index in re.findall(r"\*\s*arg([0-3])\b", text)}
    pointer_registers.update(int(index) for index in re.findall(r"M2C_FIELD\(arg([0-3]),", text))
    spec["oracleShape"] = entry.get("oracleShape", {"kind": "recovered-C", "argumentPointerRegisters": sorted(pointer_registers)})
    if "oracleShape" in entry:
        record["oracleShape"] = spec["oracleShape"]
    try:
        record["oracle"] = utility_oracle.oracle(code, spec)
    except Exception as error:
        record["oracle"] = {"supported": False, "failure": f"{type(error).__name__}: {error}", "limitation": "Full bytes and declared relocations match; native behavior needs a broader isolated runtime model"}
    return record


def research(spec):
    directory = WORK / spec["module"] / f"{spec['address']:08x}"
    directory.mkdir(parents=True, exist_ok=True)
    asm, targets, data, declarations = assembly(spec)
    asm_path = directory / ("native-" + utility_runtime.sha(asm.encode())[:16] + ".s")
    asm_path.write_text(asm)
    result = {"module": spec["module"], "address": hex(spec["address"]), "mode": spec["mode"], "nativeBytes": spec["bytes"], "variants": []}
    compilers = [ROOT / "tools/mwccarm/mwccarm/1.2/base/mwccarm.exe", matcher.COMPILER] if spec["mode"] == "thumb" else [matcher.COMPILER, ROOT / "tools/mwccarm/mwccarm/1.2/base/mwccarm.exe"]
    for returns in ("u32", "void"):
        context_text = PRELUDE + "\n".join(declarations) + f"\nextern {returns} {symbol(spec)}();\n"
        context = directory / (returns + "-context-" + utility_runtime.sha(context_text.encode())[:16] + ".c")
        context.write_text(context_text)
        command = [sys.executable, str(M2C), "--target", "arm-mwcc-c", "--context", str(context), "--globals", "none", "--no-cache", "--valid-syntax", "--comment-style", "none", "-f", symbol(spec), str(asm_path)]
        variant = {"returnAssumption": returns, "command": command, "attempts": []}
        result["variants"].append(variant)
        try:
            process = subprocess.run(command, cwd=ROOT, env=dict(os.environ, PYTHONPATH=str(ROOT / "tools/m2c-python")), capture_output=True, text=True, timeout=45)
            variant.update(exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr)
            if process.returncode:
                continue
            text = recovered_source(process.stdout, spec, targets, data)
            source = directory / (returns + "-draft-" + utility_runtime.sha(text.encode())[:16] + ".c")
            source.write_text(text)
            for compiler in compilers:
                for level, speed in [(2, False), (2, True), (3, True)]:
                    record, code = matcher.compile_compare(source, dict(spec, compilerPath=compiler), level, "off", speed)
                    variant["attempts"].append(record)
                    if code is not None:
                        result.update(match=record, draftSource=source.relative_to(ROOT).as_posix())
                        return result
        except Exception as error:
            variant["failure"] = f"{type(error).__name__}: {error}"
    return result


def safe_research(spec):
    try:
        result = research(spec)
    except Exception as error:
        result = {"module": spec["module"], "address": hex(spec["address"]), "mode": spec["mode"], "nativeBytes": spec["bytes"],
                  "variants": [], "failure": f"{type(error).__name__}: {error}"}
    result["inputModuleSha256"] = spec["inputModuleSha256"]
    text = json.dumps(result, indent=2) + "\n"
    journal = WORK / "campaigns" / OPTIONS.batch
    journal.mkdir(parents=True, exist_ok=True)
    path = journal / (spec["module"] + f"-{spec['address']:08x}-" + utility_runtime.sha(text.encode())[:16] + ".json")
    if not path.exists():
        path.write_text(text)
    return result


def main():
    global FUNCTIONS, ARGUMENTS, OPTIONS
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", default="translated01")
    parser.add_argument("--limit", type=int, default=240)
    parser.add_argument("--min-bytes", type=int, default=0)
    parser.add_argument("--max-bytes", type=int, default=256)
    parser.add_argument("--processor", choices=["arm9", "arm7", "all"], default="all")
    parser.add_argument("--register-order", action="store_true")
    parser.add_argument("--reverse-register-order", action="store_true")
    parser.add_argument("--forwarding-focused", action="store_true")
    parser.add_argument("--abi-hints", action="store_true")
    parser.add_argument("--scalar-globals", action="store_true")
    parser.add_argument("--fixed-work-areas", action="store_true")
    parser.add_argument("--fixed-area-focused", action="store_true")
    parser.add_argument("--direct-increments", action="store_true")
    parser.add_argument("--typed-globals", action="store_true")
    parser.add_argument("--verify", action="store_true")
    OPTIONS = parser.parse_args()
    path = ROOT / f"evidence/matches/utility-{OPTIONS.batch}.json"
    if OPTIONS.verify:
        report = json.loads(path.read_text())
        matches = []
        for entry in report["matches"]:
            if utility_runtime.sha((ROOT / entry["source"]).read_bytes()) != entry["sourceSha256"]:
                raise ValueError("Accepted utility source changed")
            matches.append(validate(entry, matcher.accepted_spec(entry)))
        report.update(matches=matches, nativeSymbolBindings=native_bindings(matches))
        path.write_text(json.dumps(report, indent=2) + "\n")
        print({"verified": len(matches), "bytes": sum(entry["bytes"] for entry in matches)})
        return
    specs = matcher.candidates()
    FUNCTIONS = {processor: {spec["address"]: spec for spec in specs if spec["processor"] == processor} for processor in ("arm9", "arm7")}
    bridges = utility_bridges.derive()["bridges"]
    forwarded = {processor: {} for processor in FUNCTIONS}
    aliases = set()
    for bridge in bridges:
        address, target = int(bridge["address"], 0), int(bridge["targetAddress"], 0)
        forwarded[bridge["processor"]].update({address: target, address + 4: target})
        aliases.update([(bridge["module"], address), (bridge["module"], address + 4)])
    for spec in specs:
        operations = [(instruction.mnemonic, instruction.op_str) for instruction in spec["instructions"]]
        if len(operations) == 2 and operations[0][0] == "ldr" and operations[0][1].startswith("ip, [pc") and operations[1] == ("bx", "ip") and len(spec["pools"]) == 1:
            forwarded[spec["processor"]][spec["address"]] = next(iter(spec["pools"].values())) & ~1
        last = spec["instructions"][-1]
        if last.mnemonic == "b" and last.operands and last.operands[0].type == 2 and last.operands[0].imm in FUNCTIONS[spec["processor"]]:
            forwarded[spec["processor"]][spec["address"]] = last.operands[0].imm
    ARGUMENTS = {processor: argument_counts(list(functions.values()), forwarded[processor]) for processor, functions in FUNCTIONS.items()}
    if OPTIONS.abi_hints:
        hints = {processor: argument_hints(list(functions.values()), forwarded[processor]) for processor, functions in FUNCTIONS.items()}
        ARGUMENTS = {processor: result[0] for processor, result in hints.items()}
        journal = WORK / "campaigns" / OPTIONS.batch
        journal.mkdir(parents=True, exist_ok=True)
        (journal / "abi-hints.json").write_text(json.dumps({"method": "conditional-register-definitions-and-entry-SP-word-loads", "sourceHypothesesOnly": True,
            "counts": {processor: {hex(address): count for address, count in result[0].items()} for processor, result in hints.items()},
            "stackLoads": {processor: result[1] for processor, result in hints.items()}}, indent=2) + "\n")
    plain = {processor: argument_counts(list(functions.values())) for processor, functions in FUNCTIONS.items()}
    changed = {processor: {address for address, count in counts.items() if plain[processor].get(address) != count}
               for processor, counts in ARGUMENTS.items()}
    focus = {(spec["module"], spec["address"]) for spec in specs if spec["address"] in changed[spec["processor"]] or
             any(instruction.group(CS_GRP_CALL) and instruction.operands and instruction.operands[0].type == 2 and
                 instruction.operands[0].imm in changed[spec["processor"]] for instruction in spec["instructions"])}
    indexed = {(spec["module"], spec["address"]): spec for spec in specs}
    if path.exists():
        raise ValueError("Choose a new utility recovery batch")
    accepted = {(entry["module"], int(entry["address"], 0)) for report in (ROOT / "evidence/matches").glob("utility-*.json") for entry in json.loads(report.read_text()).get("matches", [])}
    selected = sorted((spec for key, spec in indexed.items() if key not in accepted and key not in aliases and OPTIONS.min_bytes <= spec["bytes"] <= OPTIONS.max_bytes
                       and (OPTIONS.processor == "all" or spec["processor"] == OPTIONS.processor)
                       and (not OPTIONS.fixed_area_focused or any(fixed_work_area(spec, value) for value in spec["pools"].values()))
                       and (not OPTIONS.forwarding_focused or key in focus)), key=lambda spec: spec["bytes"])[:OPTIONS.limit]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(safe_research, selected):
            results.append(result)
            print({"module": result["module"], "address": result["address"], "bytes": result["nativeBytes"], "matched": "match" in result}, flush=True)
    matches = []
    for result in results:
        if "match" not in result:
            continue
        entry = result["match"]
        source = ROOT / f"src/utility/{OPTIONS.batch}/{entry['name']}.c"
        source.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            raise ValueError("Refusing to change accepted utility source")
        source.write_bytes((ROOT / result["draftSource"]).read_bytes())
        entry.update(source=source.relative_to(ROOT).as_posix(), sourceSha256=utility_runtime.sha(source.read_bytes()))
        matches.append(validate(entry, indexed[(entry["module"], int(entry["address"], 0))]))
    report = {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM,
              "runtimeMappingCanonical": True, "matches": matches, "nativeSymbols": {rel["symbol"]: rel["target"] for entry in matches for rel in entry["relocations"]},
              "nativeSymbolBindings": native_bindings(matches), "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "limitations": ["Decompiler argument/return/type assumptions remain provisional; only whole native spans with declared relocations are accepted",
                              "Matching configurations do not prove historical original compiler attribution", "Unsupported behavioral paths remain explicit"]}
    (ROOT / f"evidence/attempts/utility-{OPTIONS.batch}.json").write_text(json.dumps(results, indent=2) + "\n")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print({"functions": len(matches), "bytes": sum(entry["bytes"] for entry in matches), "drafts": len(results)})


if __name__ == "__main__":
    main()
