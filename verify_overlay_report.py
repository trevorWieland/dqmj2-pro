import argparse
import copy
import json
import os
import uuid
from pathlib import Path
import match_overlay_modules as matcher


def option(flags, name, default=None):
    return flags[flags.index(name) + 1] if name in flags else default


def relocation_key(item):
    return item["offset"], item["type"], item["symbol"], int(item["target"], 16), item.get("addend", 0)


def verify(path):
    root = matcher.ROOT
    path = (root / path).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError("Report must be an existing repository file")
    frozen = json.loads(path.read_text())
    if frozen.get("romSha256") != matcher.ROM_HASH or matcher.sha((root / "inputs/game.nds").read_bytes()) != matcher.ROM_HASH:
        raise ValueError("Frozen report/input ROM namespace differs")
    module = frozen["module"]
    if module not in {f"ov{index:03d}" for index in range(8)}:
        raise ValueError("Unsupported overlay namespace")
    expected = frozen.get("matches", frozen.get("functionMatches", []))
    if not expected or any(not entry.get("oracle", {}).get("passed") for entry in expected):
        raise ValueError("Report must contain accepted source functions and passing frozen oracles")
    source = (root / frozen["source"]).resolve()
    if not source.is_relative_to(root / "src") or matcher.sha(source.read_bytes()) != frozen["sourceSha256"]:
        raise ValueError("Frozen source path/content differs")
    configurations = {}
    for entry in expected:
        flags = entry.get("compilerFlags", entry.get("flags"))
        compiler = entry.get("compiler", frozen.get("compiler", "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"))
        compiler_sha = entry.get("compilerSha256", frozen.get("compilerSha256"))
        key = compiler, compiler_sha, tuple(flags)
        configurations.setdefault(key, []).append(entry)
        if (root / entry["source"]).resolve() != source or entry["sourceSha256"] != frozen["sourceSha256"] or entry.get("module", module) != module:
            raise ValueError("Frozen per-function source/namespace differs")
        if not (entry.get("exactBytes") or entry.get("exactAfterDeclaredRelocation")):
            raise ValueError("Frozen function is not an exact byte/relocation match")
    if len(configurations) != 1:
        raise ValueError("A frozen source unit must declare one exact compiler/flag configuration")
    (compiler, compiler_sha, flag_tuple), entries = next(iter(configurations.items()))
    flags = list(flag_tuple)
    matcher.COMPILER = (root / compiler).resolve()
    if not matcher.COMPILER.is_relative_to(root / "tools/mwccarm") or matcher.sha(matcher.COMPILER.read_bytes()) != compiler_sha:
        raise ValueError("Frozen compiler executable content differs")
    optimization = next((flag[2:] for flag in flags if flag.startswith("-O")), None)
    if optimization is None:
        raise ValueError("Frozen compiler optimization is missing")
    modifiers = [flags[index + 1] for index, flag in enumerate(flags) if flag == "-opt"]
    current, codes = matcher.compile_compare(module, source, optimization, option(flags, "-inline", "off"), processor=option(flags, "-proc"), optimizer_extra=modifiers, symbol_mode=option(flags, "-sym"))
    if current["returncode"]:
        raise ValueError("Frozen source compilation failed: " + current["stdout"] + current["stderr"])
    if current["flags"] != flags or current["compilerSha256"] != compiler_sha:
        raise ValueError("Reconstructed compiler command differs from the complete frozen flag list")
    originals = {entry["name"]: entry for entry in entries}
    actual = {entry["name"]: entry for entry in current["functions"]}
    if len(originals) != len(entries) or set(actual) != set(originals):
        raise ValueError("Frozen source function inventory differs; no source promotion is permitted")
    executions = 0
    for name, entry in actual.items():
        original = originals[name]
        for field in ["address", "mode", "size", "bytes", "targetSha256", "outputSha256", "sourceSha256", "compiledBytes"]:
            if entry.get(field) != original.get(field):
                raise ValueError("Frozen function target/span/source differs: " + name + " " + field)
        if not entry["exactAfterDeclaredRelocation"] or entry["compiledBytes"] != entry["size"]:
            raise ValueError("Recompiled function does not match all native bytes: " + name)
        if sorted(map(relocation_key, entry["relocations"])) != sorted(map(relocation_key, original["relocations"])):
            raise ValueError("Frozen declared relocations differ: " + name)
        oracle = matcher.oracle(module, entry, codes[name])
        if not oracle["passed"]:
            raise ValueError("Recompiled isolated oracle failed: " + name)
        executions += oracle["executions"]
    updated = copy.deepcopy(frozen)
    for entry in updated.get("matches", updated.get("functionMatches", [])):
        fresh = actual[entry["name"]]
        entry["object"] = fresh["object"]
        entry["objectSha256"] = fresh["objectSha256"]
    for field in ["object", "objectSha256"]:
        if field in updated:
            updated[field] = current[field]
    updated["nativeSymbols"] = {item["symbol"]: item["target"] for entry in current["functions"] for item in entry["relocations"]}
    changed = updated != frozen
    if changed:
        temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
        temporary.write_bytes(json.dumps(updated, indent=2).encode())
        os.replace(temporary, path)
    return {"report": str(path.relative_to(root)), "module": module, "functions": len(actual), "bytes": sum(entry["size"] for entry in actual.values()), "oracleExecutions": executions, "sourceSha256": frozen["sourceSha256"], "object": current["object"], "objectSha256": current["objectSha256"], "objectMetadataRefreshed": changed, "frozenProofPreserved": all(entry["oracle"] == originals[entry["name"]]["oracle"] for entry in updated.get("matches", updated.get("functionMatches", [])))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("report")
    args = parser.parse_args()
    print(json.dumps(verify(args.report), indent=2))


if __name__ == "__main__":
    main()
