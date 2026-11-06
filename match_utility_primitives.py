import argparse
import json
from pathlib import Path
import match_arm7
import utility_code
import utility_oracle
import utility_runtime

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/lowlevel-recovery/utility-primitives"


def native_bindings(matches):
    layout, files = utility_runtime.derive()
    result = {}
    for entry in matches:
        for relocation in entry["relocations"]:
            name, target = relocation["symbol"], int(relocation["target"], 0)
            kind = "data" if "_data_" in name else "function"
            binding = {"name": name, "program": utility_runtime.PROGRAM, "processor": entry["processor"],
                       "address": hex(target), "kind": kind, "mode": "data" if kind == "data" else relocation["targetMode"]}
            module = next((module for module in layout["modules"] if module["processor"] == entry["processor"] and
                           int(module["base"], 0) <= (target & ~1) < int(module["bssEnd"], 0)), None)
            if module:
                binding["module"] = module["id"]
            else:
                binding["externalHardwareAddress"] = True
            result[name] = binding
    return list(result.values())


def template(spec):
    result = match_arm7.template(spec)
    if result is None:
        instructions = spec["instructions"]
        if len(instructions) == 2 and instructions[-1].mnemonic == "bx" and instructions[-1].op_str == "lr" and instructions[0].mnemonic == "movs" and instructions[0].op_str.startswith("r0, #"):
            value = instructions[0].operands[1].imm & 0xFFFFFFFF
            result = (match_arm7.PRELUDE + f"u32 {spec['name']}(void) {{\n    return {value:#x}U;\n}}\n", {"kind": "constant"})
    if result is None:
        return None
    text, shape = result
    text = text.replace("native_arm7_data_", "native_utility_child_" + spec["processor"] + "_data_")
    text = text.replace("native_arm7_fn_", "native_utility_child_" + spec["processor"] + "_fn_")
    return text, shape


def validate(entry, spec, shape):
    source = ROOT / entry["source"]
    flags = entry["compilerFlags"]
    specification = dict(spec, compilerPath=ROOT / entry["compiler"], compilerProc=flags[flags.index("-proc") + 1], oracleShape=shape)
    record, code = utility_code.compile_compare(source, specification, int(flags[0][2:]), flags[flags.index("-inline") + 1], "speed" in flags)
    if code is None:
        raise ValueError("Frozen utility primitive no longer matches")
    try:
        record["oracle"] = utility_oracle.oracle(code, specification)
    except Exception as error:
        record["oracle"] = {"supported": False, "failure": f"{type(error).__name__}: {error}",
                            "limitations": ["Full byte and relocation equality is proven; native runtime effects need a broader isolated model"]}
    record["oracleShape"] = shape
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", default="primitives01")
    parser.add_argument("--limit", type=int, default=240)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = ROOT / f"evidence/matches/utility-{args.batch}.json"
    if args.verify:
        report = json.loads(output.read_text())
        matches = []
        for entry in report["matches"]:
            if utility_runtime.sha((ROOT / entry["source"]).read_bytes()) != entry["sourceSha256"]:
                raise ValueError("Frozen utility primitive source changed")
            matches.append(validate(entry, utility_code.accepted_spec(entry), entry["oracleShape"]))
        report["matches"] = matches
        report["nativeSymbolBindings"] = native_bindings(matches)
        output.write_text(json.dumps(report, indent=2) + "\n")
        print({"verified": len(matches), "bytes": sum(entry["bytes"] for entry in matches)})
        return
    if output.exists():
        raise ValueError("Choose a new utility primitive batch")
    specs = {(spec["module"], spec["address"]): spec for spec in utility_code.candidates()}
    accepted = {(entry["module"], int(entry["address"], 0)) for path in (ROOT / "evidence/matches").glob("utility-*.json")
                for entry in json.loads(path.read_text()).get("matches", [])}
    selected = sorted((spec for key, spec in specs.items() if key not in accepted and spec["bytes"] <= 48), key=lambda spec: spec["bytes"])
    matches, attempts = [], []
    WORK.mkdir(parents=True, exist_ok=True)
    considered = 0
    for spec in selected:
        generated = template(spec)
        if generated is None:
            continue
        if considered >= args.limit:
            break
        considered += 1
        text, shape = generated
        source = WORK / (spec["name"] + ".c")
        source.write_text(text)
        found = None
        compiler_paths = [utility_code.COMPILER, ROOT / "tools/mwccarm/mwccarm/1.2/base/mwccarm.exe"]
        for compiler in compiler_paths:
            if found:
                break
            for proc in (["arm946e", "arm7tdmi"] if spec["processor"] == "arm9" and spec["mode"] == "thumb" else ["arm946e" if spec["processor"] == "arm9" else "arm7tdmi"]):
                record, code = utility_code.compile_compare(source, dict(spec, compilerPath=compiler, compilerProc=proc))
                attempts.append(record)
                if code is not None:
                    found = record
                    break
        if found is not None:
            frozen = ROOT / f"src/utility/{args.batch}/{spec['name']}.c"
            frozen.parent.mkdir(parents=True, exist_ok=True)
            if frozen.exists():
                raise ValueError("Refusing to change accepted utility source")
            frozen.write_bytes(source.read_bytes())
            found.update(source=frozen.relative_to(ROOT).as_posix(), sourceSha256=utility_runtime.sha(frozen.read_bytes()))
            matches.append(validate(found, spec, shape))
        print({"module": spec["module"], "address": hex(spec["address"]), "matched": found is not None}, flush=True)
    bindings = {rel["symbol"]: rel["target"] for entry in matches for rel in entry["relocations"]}
    report = {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM,
              "runtimeMappingCanonical": True, "matches": matches, "nativeSymbols": bindings, "nativeSymbolBindings": native_bindings(matches),
              "sourceReconstructionComplete": False, "wholeModuleLinked": False,
              "limitations": ["Templates describe measured primitive operations; larger logic remains unrecovered",
                              "Only full native spans and declared relocation matches are accepted",
                              "Unsupported behavioral paths remain explicit; no complete program execution is claimed"]}
    (ROOT / f"evidence/attempts/utility-{args.batch}.json").write_text(json.dumps(attempts, indent=2) + "\n")
    output.write_text(json.dumps(report, indent=2) + "\n")
    print({"functions": len(matches), "bytes": sum(entry["bytes"] for entry in matches), "candidates": considered})


if __name__ == "__main__":
    main()
