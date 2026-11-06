import argparse
import json
import re
from pathlib import Path
import match_arm7 as matcher

ROOT = Path(__file__).resolve().parent


def shape_for(entry, source):
    pointer_arguments = {int(index) for index in re.findall(r"\*\s*arg([0-3])\b", source)}
    pointer_arguments.update(int(index) for index in re.findall(r"M2C_FIELD\(arg([0-3]),", source))
    pointers = sorted(pointer_arguments)
    values = {str(index): [0x03002000 + index * 0x1000] if index in pointers else
              [0, 1, 2, 3, 7, 15, 16, 31, 63, 127, 255, 1023] for index in range(4)}
    return {"kind": "source-shaped-initial-runtime", "nativeRuntimeInitialized": True,
            "argumentValues": values, "boundedCalleeReturns": True,
            "callees": {rel["symbol"]: int(rel["target"], 0) for rel in entry["relocations"]
                        if rel["symbol"].startswith("native_arm7_fn_")}}


def assess(entry, spec):
    source = ROOT / entry["source"]
    obj = ROOT / entry["object"]
    if matcher.sha(source.read_bytes()) != entry["sourceSha256"] or matcher.sha(obj.read_bytes()) != entry["objectSha256"]:
        raise ValueError("ARM7 behavioral evidence refers to changed source or object")
    if matcher.sha((ROOT / entry["compiler"]).read_bytes()) != entry["compilerSha256"]:
        raise ValueError("ARM7 behavioral evidence compiler identity changed")
    flags = entry["compilerFlags"]
    record, compiled = matcher.compare(source, spec, ROOT / entry["compiler"], entry["compilerSha256"],
                                       int(flags[0][2:]), flags[flags.index("-inline") + 1], "speed" in flags)
    if compiled is None:
        raise ValueError("ARM7 source no longer matches native before behavioral check")
    shape = shape_for(entry, source.read_text())
    binary = (ROOT / spec["binary"]).read_bytes()
    offset = spec["address"] - spec["base"]
    native = binary[offset:offset + spec["bytes"]]
    successful, unsupported = [], []
    visited, calls = set(), set()
    for vector in range(24):
        try:
            expected = matcher.execute(native, spec, shape, vector)
            actual = matcher.execute(compiled, spec, shape, vector)
        except Exception as error:
            unsupported.append({"vector": vector, "reason": f"{type(error).__name__}: {error}"})
            continue
        if actual != expected:
            raise ValueError("ARM7 source/native bounded effects differ")
        visited.update(expected["visited"])
        calls.update(call["address"] for call in expected["calls"])
        successful.append({"vector": vector, "stateSha256": matcher.sha(json.dumps(expected, sort_keys=True).encode())})
    return {"name": entry["name"], "module": entry["module"], "processor": "arm7", "address": entry["address"],
            "source": entry["source"], "sourceSha256": entry["sourceSha256"], "objectSha256": record["objectSha256"],
            "inputModuleSha256": entry["inputModuleSha256"], "nativeSpanBytes": spec["bytes"],
            "vectorsPassed": len(successful), "nativeAndRecompiledCompletedCalls": len(successful) * 2,
            "successfulVectors": successful, "unsupportedVectors": unsupported, "shape": shape,
            "visitedInstructionAddresses": [hex(address) for address in sorted(visited)],
            "visitedSyntheticCallees": sorted(calls), "allVectorsSupported": not unsupported}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reports", nargs="*", default=["arm7-translated03", "arm7-translated04"])
    args = parser.parse_args()
    results = []
    inputs = []
    for name in args.reports:
        path = ROOT / f"evidence/matches/{name}.json"
        report = json.loads(path.read_text())
        inputs.append({"path": path.relative_to(ROOT).as_posix(), "sha256": matcher.sha(path.read_bytes())})
        for entry in report["matches"]:
            result = assess(entry, matcher.accepted_spec(entry))
            results.append(result)
            print({"name": entry["name"], "vectorsPassed": result["vectorsPassed"]}, flush=True)
    output = {"schemaVersion": 1, "romSha256": matcher.sha((ROOT / "inputs/game.nds").read_bytes()),
              "processor": "arm7", "runtimeMappingCanonical": True, "reports": inputs, "functions": results,
              "nativeAndRecompiledCompletedCalls": sum(result["nativeAndRecompiledCompletedCalls"] for result in results),
              "limitations": ["Measured initialized runtime images and loader-zeroed BSS are used in an isolated synthetic RAM/MMIO map",
                              "Source-observed pointer arguments point into bounded scratch RAM; other argument values are bounded integers",
                              "External callees use declared synthetic return values 0, 1 or scratch pointers; their implementations are not exercised",
                              "Unsupported vectors remain explicit and do not count as completed calls",
                              "Instruction coverage is observed addresses only, not complete path or platform coverage"]}
    path = ROOT / "evidence/arm7/source-effects.json"
    path.write_text(json.dumps(output, indent=2) + "\n")
    print({"report": path.relative_to(ROOT).as_posix(), "functions": len(results),
           "completedCalls": output["nativeAndRecompiledCompletedCalls"]})


if __name__ == "__main__":
    main()
