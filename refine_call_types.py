import argparse
import concurrent.futures
import re
import draft_runtime
import reuse_overlay_c as reuse
from refine_scalar_globals import immutable, sha
from project import ROOT, configuration, read_json, sha256, write_json


def unused_call_types(text):
    prototypes = set(re.findall(r"(?m)^extern u32 (native_fn_\w+)\([^;\n]*\);$", text))
    body = re.sub(r"(?m)^extern[^\n]*;\s*$", "", text)
    observations = {}
    for match in re.finditer(r"\b(native_fn_\w+)\s*\(", body):
        name = match[1]
        depth = 1
        end = match.end()
        while depth and end < len(body):
            depth += (body[end] == "(") - (body[end] == ")")
            end += 1
        prefix = body[body.rfind("\n", 0, match.start()) + 1 : match.start()].strip()
        unused = not prefix and body[end:].lstrip().startswith(";")
        observations.setdefault(name, []).append(unused)
    names = sorted(
        name
        for name in prototypes
        if observations.get(name)
        and all(observations[name])
        and len(re.findall(r"\b" + re.escape(name) + r"\b", body)) == len(observations[name])
    )
    changed = text
    for name in names:
        changed = re.sub(r"(?m)^extern u32 (" + re.escape(name) + r"\()", r"extern void \1", changed)
    return changed, names


def late_independent_counters(text):
    moves = []
    for close in re.finditer(r"(?m)^([ \t]*)}\s*while\s*\(([^;\n]*)\);", text):
        indent = close[1]
        opening = list(re.finditer(r"(?m)^" + re.escape(indent) + r"do\s*{", text[: close.start()]))
        if not opening:
            continue
        start = opening[-1].end()
        for name in set(re.findall(r"\bvar_\w+\b", close[2])):
            if re.search(r"&\s*" + re.escape(name) + r"\b", text):
                continue
            if re.search(r"(?m)^.*\bvolatile\b.*\b" + re.escape(name) + r"\b", text):
                continue
            increments = list(
                re.finditer(
                    r"(?m)^" + re.escape(indent + "    ") + re.escape(name) + r"\s*\+=\s*(?:0x[0-9a-fA-F]+|\d+);\n",
                    text[start : close.start()],
                )
            )
            if not increments:
                continue
            increment = increments[-1]
            first, last = start + increment.start(), start + increment.end()
            suffix = text[last : close.start()]
            if not suffix.strip() or re.search(
                r"\b" + re.escape(name) + r"\b|native_fn_\w+\s*\(|\b(?:goto|return|break|continue)\b|[{}]", suffix
            ):
                continue
            moves.append((first, last, close.start(), name))
    changed = text
    for first, last, close, name in sorted(moves, reverse=True):
        changed = changed[:first] + changed[last:close] + changed[first:last] + changed[close:]
    return changed, [move[3] for move in moves]


def recover(row, module, batch):
    original = ROOT / row["draftSource"]
    text = original.read_text()
    voids, names = unused_call_types(text)
    late, moved = late_independent_counters(text)
    combined, bothMoved = late_independent_counters(voids)
    attempts = []
    result = {"nativeAlias": row["nativeAlias"], "draftSource": row["draftSource"], "attempts": attempts}
    best = row["best"]
    spec = {"name": best["name"], "module": module, "mode": best["mode"]}
    seen = {text}
    for kind, candidate, callees, counters in [
        ("unused-result-callees", voids, names, []),
        ("late-independent-counters", late, [], moved),
        ("unused-result-callees-and-late-counters", combined, names, bothMoved),
    ]:
        if candidate in seen or len(candidate.splitlines()) > 500:
            continue
        seen.add(candidate)
        snapshot = ROOT / f"work/overlay-recovery/call-types/{batch}/{sha(candidate.encode())}.c"
        immutable(snapshot, candidate.encode())
        try:
            records, found = reuse.compile_entry(snapshot, spec, best)
        except Exception as error:
            attempts.append({"kind": kind, "failure": f"{type(error).__name__}: {error}"})
            continue
        attempts.append(
            {"kind": kind, "calleeTypesChanged": callees, "counterMoves": counters, "compilerResults": records}
        )
        if found is None:
            continue
        frozen = ROOT / (
            f"src/overlays/{module}_{batch}_{sha(candidate.encode())[:12]}.c"
            if module in ["ov005", "ov006"]
            else f"src/runtime/{batch}/{best['name']}_{sha(candidate.encode())[:12]}.c"
        )
        immutable(frozen, candidate.encode())
        records, found = reuse.compile_entry(frozen, spec, best)
        if found is None:
            raise ValueError("Frozen call-type hypothesis no longer matches")
        entry, code = found
        binary, unused, base = draft_runtime.module_paths(module)
        at = int(entry["address"], 0) - base
        try:
            entry["oracle"] = reuse.bounded_oracle(entry, code, binary.read_bytes()[at : at + entry["bytes"]])
        except Exception as error:
            entry["oracle"] = {
                "supported": False,
                "failure": f"{type(error).__name__}: {error}",
                "limitation": "Full bytes and relocations match; broader platform fixtures remain required",
            }
        entry["sourceHypothesis"] = {
            "kind": kind,
            "unusedResultCalleesDeclaredVoid": callees,
            "independentLoopCounterMoves": counters,
            "draftSource": row["draftSource"],
            "draftSourceSha256": sha256(original),
            "calleeDefinitionTypesProven": False,
            "ordinaryCOnly": True,
        }
        result["match"] = entry
        return result
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", required=True, choices=["main", "ov000", "ov001", "ov005", "ov006"])
    parser.add_argument("--batch", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--limit", type=int, default=80)
    parser.add_argument("--minimum-ratio", type=float, default=0.5)
    parser.add_argument("--workers", type=int, choices=[1, 2, 3], default=3)
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9-]+", args.batch):
        raise ValueError("Invalid call-type batch")
    target = ROOT / f"evidence/matches/{args.module}-{args.batch}.json"
    if args.verify:
        report = read_json(target)
        if report["module"] != args.module or report["romSha256"] != configuration()["romSha256"]:
            raise ValueError("Call-type namespace changed")
        report["matches"] = draft_runtime.verify(report)
        report["nativeSymbols"] = {r["symbol"]: r["target"] for e in report["matches"] for r in e["relocations"]}
        write_json(target, report)
        print({"verified": len(report["matches"]), "bytes": sum(e["bytes"] for e in report["matches"])})
        return
    if target.exists():
        raise ValueError("Choose a new call-type batch")
    from ledger_state import collect_matches
    from recovery_ownership import reservation

    accepted, unused = collect_matches(configuration()["romSha256"])
    excluded = {
        int(e["address"], 0)
        for path in args.exclude
        for e in read_json(ROOT / path)["matches"]
        if e.get("module", args.module) == args.module
    }
    candidates = []
    for row in read_json(ROOT / args.input):
        if "match" in row or not row.get("draftSource"):
            continue
        entries = [
            e
            for e in row.get("attempts", [])
            if e.get("module") == args.module and e.get("object") and e.get("bytes") and e.get("compiledBytes")
        ]
        if not entries:
            continue
        best = max(entries, key=lambda e: e["matchingBytes"] / max(e["bytes"], e["compiledBytes"]))
        address = int(best["address"], 0)
        ratio = best["matchingBytes"] / max(best["bytes"], best["compiledBytes"])
        if (args.module, best["mode"], address) in accepted or address in excluded or ratio < args.minimum_ratio:
            continue
        if args.module == "main" and reservation(address):
            continue
        candidates.append({**row, "best": best, "ratio": ratio})
    candidates.sort(key=lambda row: (-row["ratio"], row["nativeAlias"]))
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for result in pool.map(lambda row: recover(row, args.module, args.batch), candidates[: args.limit]):
            results.append(result)
            print(
                {
                    "function": result["nativeAlias"],
                    "matched": "match" in result,
                    "hypotheses": len(result["attempts"]),
                },
                flush=True,
            )
    matches = [r["match"] for r in results if "match" in r]
    binary, unused, base = draft_runtime.module_paths(args.module)
    report = {
        "schemaVersion": 1,
        "romSha256": configuration()["romSha256"],
        "module": args.module,
        "moduleInputSha256": sha256(binary),
        "matches": matches,
        "nativeSymbols": {r["symbol"]: r["target"] for e in matches for r in e["relocations"]},
        "wholeModuleLinked": False,
        "sourceReconstructionComplete": False,
        "limitations": [
            "Ordinary C unused-result callee type and independent loop-counter hypotheses require complete compiler-byte and ELF relocation matches.",
            "Void callee declarations infer caller-use context only; original external callee definition types and full platform behavior remain unproved.",
        ],
    }
    write_json(ROOT / f"evidence/attempts/{args.module}-{args.batch}.json", results)
    write_json(target, report)
    print({"functions": len(matches), "bytes": sum(e["bytes"] for e in matches)})


if __name__ == "__main__":
    main()
