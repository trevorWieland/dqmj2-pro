import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import types
from pathlib import Path

import draft_runtime as draft
import match_overlay_modules as compiler
from known_returns import return_catalogue
from ledger_state import collect_matches
from match_ov000_20261029_leaf import original_module
from native_alternate_entries import binding
from project import configuration, now, sha256, write_json

ROOT = Path(__file__).resolve().parent
BATCH = ROOT / "nonmatching/ov000/20261029-broad01"
MANIFEST = BATCH / "manifest.json"
CALL_ALIASES = {}
BASE_SYMBOLS = compiler.symbol_data


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def address_symbols(module):
    lookup, boundaries = BASE_SYMBOLS(module)
    lookup.update({name: row["address"] for name, row in CALL_ALIASES.items()})
    return lookup, boundaries


def data_hints(assembly):
    literals = dict(re.findall(r"^(\.\w+):\s*\.word\s+(data_\w+)\s*$", assembly, re.M))
    origins, accesses = {}, {}
    for line in assembly.splitlines():
        match = re.match(r"\s*(\w+)\s+(.*)", line)
        if not match:
            continue
        opcode, operands = match.groups()
        destination = re.match(r"(r\d+|ip|lr),", operands)
        load_literal = re.match(r"(r\d+|ip|lr),\s*(\.\w+)$", operands)
        if opcode.startswith("ldr") and load_literal and load_literal[2] in literals:
            origins[load_literal[1]] = literals[load_literal[2]]
            continue
        memory = re.match(r"(?:r\d+|ip|lr),\s*\[(r\d+|ip|lr)(?:,.*?)?\]", operands)
        if opcode.startswith(("ldr", "str")) and memory and memory[1] in origins:
            suffix = opcode[3:]
            scalar = "s16" if suffix.startswith("sh") else "s8" if suffix.startswith("sb") else "u8" if suffix.startswith("b") else "u16" if suffix.startswith("h") else "u32"
            accesses.setdefault(origins[memory[1]], set()).add(scalar)
        copy = re.match(r"(r\d+|ip|lr),\s*(r\d+|ip|lr)(?:,|$)", operands)
        if opcode.startswith(("mov", "add", "sub")) and copy and copy[2] in origins:
            origins[copy[1]] = origins[copy[2]]
        elif destination and not opcode.startswith(("str", "cmp", "tst")):
            origins.pop(destination[1], None)
    return {symbol: {"accessTypes": sorted(values),
                     "contextType": next(iter(values)) if len(values) == 1 else "u8",
                     "confidence": "heuristic linear register-origin tracking; CFG merges not proven"}
            for symbol, values in accesses.items()}


def convert_labels(assembly, start, size):
    defined = set(re.findall(r"^(\.\w+):", assembly, re.M))
    aliases, replacements = {}, []
    for opcode, label, raw in re.findall(r"\b(b(?:l|lx)?(?:eq|ne|lt|le|gt|ge|hi|ls|cc|cs|pl|mi)?)\s+(\.L_([0-9a-f]{8}))\b", assembly):
        address = int(raw, 16)
        if label in defined or start <= address < start + size:
            continue
        scope = "main" if address < 0x021D7240 else "ov000"
        measured = scope == "main" and address == 0x02025F2C
        name = "runtime_main_02025f2c" if measured else f"unmeasured_{scope}_entry_{raw}"
        assembly = re.sub(r"\b" + re.escape(label) + r"\b", name, assembly)
        aliases[name] = {"address": address, "module": scope, "kind": "configured external label hypothesis",
                         "measuredReturn": "s64" if measured else None,
                         "nativeBoundaryProven": measured}
        replacements.append({"originalLabel": label, "sourceAlias": name, "address": hex(address),
                             "opcode": opcode, "measuredABI": measured,
                             "scopeConfidence": "main RAM range" if scope == "main" else "own overlay assumption"})
    return assembly, aliases, replacements


def union_bytes(rows):
    ranges = sorted((int(row["address"], 0), int(row["address"], 0) + row["bytes"]) for row in rows)
    result, end = 0, -1
    for start, last in ranges:
        result += max(0, last - max(start, end))
        end = max(end, last)
    return result


def prepare():
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text())
        if manifest["generatorSha256"] != sha256(Path(__file__)):
            raise ValueError("Resume generator changed; preserve this batch and choose a fresh one")
        return manifest
    binary, metadata, provenance = original_module()
    accepted, unused = collect_matches(provenance["romSha256"])
    excluded = {(row["module"], row["mode"], row["address"]) for row in accepted.values()}
    for path in (ROOT / "evidence/matches").glob("ov000-20261029-*.json"):
        report = json.loads(path.read_text())
        excluded.update(("ov000", row["mode"], int(row["address"], 0)) for row in report.get("matches", []))
    catalogue = return_catalogue("ov000")
    abi = json.loads((ROOT / "evidence/abi/ov000-021d8c34-20261029.json").read_text())
    if abi["romSha256"] != provenance["romSha256"] or abi["module"] != "ov000" or abi["sourceReturnType"] != "s64":
        raise ValueError("Measured wide return belongs to another native namespace")
    if sha256(ROOT / abi["proofReport"]) != abi["proofReportSha256"]:
        raise ValueError("Measured wide-return immutable proof changed")
    catalogue["func_ov000_021d8c34"] = {"type": "s64", "module": "ov000", "mode": "arm",
                                                  "address": "0x21d8c34", "evidence": "measured native return ABI"}
    draft.OPTIONS = types.SimpleNamespace(module="ov000", thumb=False, word_args=True, abi_slots=True,
        register_order=True, stack_buffers=True, direct_increments=True, typed_globals=False,
        source_returns=False)
    draft.WORK = BATCH / "generated"
    draft.SOURCE_RETURNS.update(catalogue)
    draft.inputs()
    lookup, functions = compiler.symbol_data("ov000")
    candidates = []
    for address, spec in sorted(functions.items()):
        if ("ov000", spec["mode"], address) in excluded:
            continue
        row = {"romSha256": provenance["romSha256"], "processor": "arm9", "module": "ov000",
               "address": hex(address), "mode": spec["mode"], "bytes": spec["size"], "symbol": spec["name"],
               "nativeSpanSha256": compiler.sha(binary[address - 0x021D7240:address - 0x021D7240 + spec["size"]]),
               "nativeModuleSha256": metadata["sha256"], "boundaryConfidence": "configured heuristic ds-decomp span",
               "directory": f"functions/{address:08x}-{spec['mode']}"}
        folder = BATCH / row["directory"]
        folder.mkdir(parents=True, exist_ok=True)
        original = draft.FUNCTION_INPUTS.get(spec["name"])
        if original is None:
            row["inputFailure"] = "No module-qualified analysis assembly"
            candidates.append(row)
            continue
        assembly, context = original
        row["originalAnalysisAssemblySha256"] = digest(assembly)
        assembly, aliases, replacements = convert_labels(assembly, address, spec["size"])
        CALL_ALIASES.update(aliases)
        hints = data_hints(assembly)
        for name, info in catalogue.items():
            context = context.replace(f"extern u32 {name}();", f"extern {info['type']} {name}();")
        for symbol, info in hints.items():
            context = context.replace(f"extern u8 {symbol}[];", f"extern {info['contextType']} {symbol}[];")
        for name, info in aliases.items():
            declaration = f"extern {'s64' if info['measuredReturn'] else 'u32'} {name}();\n"
            context += declaration
        (folder / "input.s").write_text(assembly)
        (folder / "context.c").write_text(context)
        row.update(analysisAssemblySha256=digest(assembly), contextSha256=digest(context),
                   dataHints=hints, externalLabelReplacements=replacements,
                   externalLabelAliases=aliases,
                   returnContexts={name: info for name, info in catalogue.items() if name in assembly})
        candidates.append(row)
    manifest = {"schemaVersion": 1, "createdUtc": now(), "generator": Path(__file__).name,
                "generatorSha256": sha256(Path(__file__)), **provenance,
                "module": "ov000", "processor": "arm9", "candidates": candidates,
                "candidateFunctions": len(candidates), "uniqueCandidateNativeBytes": union_bytes(candidates),
                "returnContexts": catalogue, "diagnosticLabelAliases": CALL_ALIASES,
                "measuredWideReturnRecord": "evidence/abi/ov000-021d8c34-20261029.json",
                "measuredAlternateEntry": binding("main", 0x02025F2C),
                "decompiler": str(draft.M2C.relative_to(ROOT)), "decompilerSha256": sha256(draft.M2C),
                "acceptedSourceCredit": 0, "sourceReconstructionComplete": False}
    write_json(MANIFEST, manifest)
    return manifest


def one(row, catalogue):
    folder = BATCH / row["directory"]
    target = folder / "result.json"
    if target.exists():
        result = json.loads(target.read_text())
        if result.get("source") and sha256(ROOT / result["source"]) != result["sourceSha256"]:
            raise ValueError("Resumable nonmatching source changed")
        return result
    result = {**row, "evidenceClass": "nonmatching ordinary C hypothesis", "accepted": False,
              "matchedExecutableByteCredit": 0, "sourceReconstructionComplete": False,
              "executionValidated": False, "compileAttempts": [], "drafted": False,
              "compiled": False, "createdUtc": now()}
    if row.get("inputFailure"):
        write_json(target, result)
        return result
    source = folder / "source.c"
    command = [sys.executable, str(draft.M2C), "--target", "arm-mwcc-c", "--comment-style", "none",
               "--no-cache", "--valid-syntax", "--context", str(folder / "context.c"),
               "-f", row["symbol"], str(folder / "input.s")]
    result["decompileCommand"] = command
    try:
        process = subprocess.run(command, cwd=ROOT, env=dict(os.environ, PYTHONPATH=str(ROOT / "tools/m2c-python")),
                                 capture_output=True, text=True, timeout=90)
        (folder / "decompiler-output.txt").write_text(process.stdout)
        (folder / "decompiler-errors.txt").write_text(process.stderr)
        result.update(decompileReturnCode=process.returncode, rawHypothesisSha256=digest(process.stdout))
        if process.returncode:
            result["decompileFailure"] = process.stderr[-1000:]
            write_json(target, result)
            return result
        substitutions = sorted(set(re.findall(r"\bM2C_UNK(?:8|16|32|64)?\b", process.stdout)))
        body = process.stdout
        for name in substitutions:
            bits = name.removeprefix("M2C_UNK") or "32"
            body = re.sub(r"\b" + name + r"\b", "u" + bits, body)
        recovered = draft.source_text(body, row["symbol"])
        recovered = recovered.replace("native_fn_", "func_").replace("native_data_", "data_")
        for name, info in row["dataHints"].items():
            recovered = recovered.replace(f"extern u8 {name}[];", f"extern {info['contextType']} {name}[];")
        for name, info in row["externalLabelAliases"].items():
            if name in recovered:
                recovered = f"extern {'signed long long' if info['measuredReturn'] else 'unsigned int'} {name}();\n" + recovered
        if re.search(r"\b(?:asm|__asm|__asm__)\b|/\*|//", recovered):
            raise ValueError("Nonmatching ordinary C must be comment-free and contain no assembly")
        if len(recovered.splitlines()) > 500:
            raise ValueError("Formatted source hypothesis exceeds500 physical lines")
        source.write_text(recovered)
        result.update(drafted=True, source=str(source.relative_to(ROOT)), sourceSha256=sha256(source),
                      physicalLines=len(recovered.splitlines()), unknownTypeSubstitutions=substitutions)
        for optimization in ["2", "2,p"]:
            report, codes = compiler.compile_compare("ov000", source, optimization, "off")
            report_path = folder / ("compile-" + compiler.sha(json.dumps(report, sort_keys=True).encode()) + ".json")
            compiler.immutable(report_path, json.dumps(report, indent=2).encode())
            current = next((entry for entry in report["functions"] if int(entry["address"], 0) == int(row["address"], 0)), None)
            result["compileAttempts"].append({"report": str(report_path.relative_to(ROOT)),
                "reportSha256": sha256(report_path), "returncode": report["returncode"],
                "compiler": report["compiler"], "flags": report["flags"],
                "function": current, "diagnosticComparisonOnly": True})
            if current:
                result["compiled"] = True
            if report["returncode"]:
                break
        successful = [attempt["function"] for attempt in result["compileAttempts"] if attempt["function"]]
        if successful:
            best = max(successful, key=lambda entry: entry["matchingBytes"])
            result.update(bestMatchingBytes=best["matchingBytes"], nativeBytes=best["bytes"],
                          bestByteSimilarity=best["matchingBytes"] / best["bytes"],
                          bestCompiledBytes=best["compiledBytes"],
                          compilerRelocationExactCandidate=best["exactAfterDeclaredRelocation"],
                          bestObjectSha256=best["objectSha256"], unresolvedRelocations=best["unresolvedRelocations"])
        result["cfgAbiUncertainty"] = {
            "boundaries": row["boundaryConfidence"], "externalLabels": row["externalLabelReplacements"],
            "dataTyping": "Native-width hints use linear register origins; CFG merges and aggregate types remain hypotheses",
            "returnContexts": row["returnContexts"], "unknownTypesDefaulted": substitutions,
            "parameters": "Decompiler argument-slot and pointer guesses; unmeasured ABI remains unsupported",
            "codeConcerns": re.findall(r"(?:<<|>>)\s*(?:0x20|32)\b", recovered),
            "linking": "No real linker/module/ROM or callback-mode validation has been performed",
        }
        result["unsupportedBehavior"] = ["No native execution validation", "Unproven external and indirect-call contracts",
            "Unresolved memory domains, overflow semantics, aliasing and error paths", "Generated C is a hypothesis and earns no matched-source credit"]
    except Exception as error:
        result["failure"] = f"{type(error).__name__}: {error}"
    write_json(target, result)
    return result


def summary(manifest, results, final=False):
    drafted = [row for row in results if row["drafted"]]
    compiled = [row for row in results if row["compiled"]]
    exact_candidates = [row for row in results if row.get("compilerRelocationExactCandidate")]
    result = {"schemaVersion": 1, "updatedUtc": now(), "completeBatch": final,
              "romSha256": manifest["romSha256"], "processor": "arm9", "module": "ov000",
              "manifestSha256": sha256(MANIFEST), "completedCandidates": len(results),
              "candidateFunctions": manifest["candidateFunctions"],
              "uniqueCandidateNativeBytes": manifest["uniqueCandidateNativeBytes"],
              "draftedFunctions": len(drafted), "uniqueDraftedNativeBytes": union_bytes(drafted),
              "compilableFunctions": len(compiled), "uniqueCompilableNativeBytes": union_bytes(compiled),
              "compilableFractionOfDrafts": len(compiled) / max(1, len(drafted)),
              "compilableFractionOfCompletedCandidates": len(compiled) / max(1, len(results)),
              "compilerRelocationExactCandidates": len(exact_candidates),
              "diagnosticMatchingBytesSum": sum(row.get("bestMatchingBytes", 0) for row in results),
              "matchedSourceCredit": 0, "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "limitations": "Approximate ordinary C hypotheses; compiled byte similarity and inferred types do not establish decompilation, native behavior, callback mode or source module matching"}
    write_json(BATCH / "summary.json", result)
    write_json(BATCH / "index.json", {"candidates": results})
    print(json.dumps({key: result[key] for key in ["completedCandidates", "candidateFunctions", "draftedFunctions",
          "uniqueDraftedNativeBytes", "compilableFunctions", "uniqueCompilableNativeBytes", "compilerRelocationExactCandidates"]}), flush=True)


def main():
    options = argparse.ArgumentParser()
    options.add_argument("--workers", type=int, default=3, choices=range(1, 4))
    args = options.parse_args()
    manifest = prepare()
    CALL_ALIASES.update(manifest["diagnosticLabelAliases"])
    compiler.symbol_data = address_symbols
    compiler.WORK = BATCH / "generated/compiler"
    draft.SOURCE_RETURNS.update(manifest["returnContexts"])
    draft.OPTIONS = types.SimpleNamespace(module="ov000", thumb=False, word_args=True, abi_slots=True,
        register_order=True, stack_buffers=True, direct_increments=True, typed_globals=False)
    draft.FUNCTION_ADDRESSES.update({row["symbol"]: f"{int(row['address'],0):08x}" for row in manifest["candidates"]})
    draft.FUNCTION_INPUTS.update({row["symbol"]: ((BATCH / row["directory"] / "input.s").read_text(), "")
        for row in manifest["candidates"] if not row.get("inputFailure")})
    results, last = [], time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(one, row, manifest["returnContexts"]) for row in manifest["candidates"]]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            if len(results) % 25 == 0 or time.monotonic() - last > 30:
                summary(manifest, results)
                last = time.monotonic()
    summary(manifest, results, True)


if __name__ == "__main__":
    main()
