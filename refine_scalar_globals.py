import argparse
import concurrent.futures
import hashlib
import json
import re
from pathlib import Path
import draft_runtime
import reuse_overlay_c as reuse
from project import ROOT, configuration, read_json, sha256, write_json


def sha(data):
    return hashlib.sha256(data).hexdigest()


def immutable(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != data:
        raise ValueError("Immutable scalar-width source collision")
    if not path.exists():
        path.write_bytes(data)


def recover(row, module, batch):
    best = row["best"]
    original = ROOT / row["draftSource"]
    text = original.read_text()
    pattern = r"(?<![\w*])\*(?:\(\s*)?(native_data_(?:ov\d{3}_)?[0-9a-f]{8})\b"
    labels = sorted(set(re.findall(pattern, text)))
    attempts = []
    result = {
        "nativeAlias": row["nativeAlias"],
        "draftSource": row["draftSource"],
        "sourceSha256": sha256(original),
        "attempts": attempts,
    }
    name = best["name"]
    spec = {"name": name, "module": module, "mode": best["mode"]}
    for label in labels:
        address = int(label[-8:], 16)
        for kind, width in [("u32", 4), ("u16", 2), ("s32", 4), ("s16", 2), ("s8", 1)]:
            if address % width:
                continue
            changed = re.sub(r"(?<![\w*])\*" + re.escape(label) + r"\b", "*(" + kind + " *)" + label, text)
            changed = re.sub(r"(?<![\w*])\*(?=\(\s*" + re.escape(label) + r"\b)", "*(" + kind + " *)", changed)
            if changed == text or len(changed.splitlines()) > 500:
                continue
            snapshot = ROOT / f"work/overlay-recovery/scalar-width/{batch}/{sha(changed.encode())}.c"
            immutable(snapshot, changed.encode())
            try:
                records, found = reuse.compile_entry(snapshot, spec, best)
            except Exception as error:
                attempts.append({"label": label, "type": kind, "failure": f"{type(error).__name__}: {error}"})
                continue
            attempts.append({"label": label, "type": kind, "compilerResults": records})
            if found is None:
                continue
            frozen = (
                ROOT / f"src/overlays/{module}_{batch}_{sha(changed.encode())[:12]}.c"
                if module in ["ov005", "ov006"]
                else ROOT / f"src/runtime/{batch}/{name}_{sha(changed.encode())[:12]}.c"
            )
            immutable(frozen, changed.encode())
            records, found = reuse.compile_entry(frozen, spec, best)
            if found is None:
                raise ValueError("Frozen scalar-width source no longer matches")
            entry, code = found
            binary_path, unused, base = draft_runtime.module_paths(module)
            binary = binary_path.read_bytes()
            at = int(entry["address"], 0) - base
            try:
                entry["oracle"] = reuse.bounded_oracle(entry, code, binary[at : at + entry["bytes"]])
            except Exception as error:
                entry["oracle"] = {
                    "supported": False,
                    "failure": f"{type(error).__name__}: {error}",
                    "limitation": "Complete compiler bytes and declared relocations match; broader platform fixtures remain required",
                }
            entry["sourceHypothesis"] = {
                "kind": "direct-scalar-global-width",
                "symbol": label,
                "pointeeType": kind,
                "draftSource": row["draftSource"],
                "draftSourceSha256": sha256(original),
                "ordinaryCOnly": True,
            }
            result["match"] = entry
            return result
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", required=True, choices=["main", "ov000", "ov001", "ov005", "ov006"])
    parser.add_argument("--batch", required=True)
    parser.add_argument("--input")
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--minimum-ratio", type=float, default=0.85)
    parser.add_argument("--workers", type=int, choices=[1, 2, 3], default=1)
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9-]+", args.batch):
        raise ValueError("Invalid scalar-width batch")
    target = ROOT / f"evidence/matches/{args.module}-{args.batch}.json"
    if args.verify:
        report = read_json(target)
        if report["module"] != args.module or report["romSha256"] != configuration()["romSha256"]:
            raise ValueError("Scalar-width namespace changed")
        report["matches"] = draft_runtime.verify(report)
        report["nativeSymbols"] = {r["symbol"]: r["target"] for e in report["matches"] for r in e["relocations"]}
        write_json(target, report)
        print({"verified": len(report["matches"]), "bytes": sum(e["bytes"] for e in report["matches"])})
        return
    if target.exists():
        raise ValueError("Choose a new scalar-width batch")
    if not args.input:
        raise ValueError("Generation requires an explicit draft-attempt input")
    from ledger_state import collect_matches
    from recovery_ownership import reservation

    accepted, _ = collect_matches(configuration()["romSha256"])
    excluded = {
        int(e["address"], 0)
        for path in args.exclude
        for e in read_json(ROOT / path)["matches"]
        if e["module"] == args.module
    }
    rows = []
    for row in read_json(ROOT / args.input):
        if "match" in row or not row.get("draftSource"):
            continue
        attempts = [
            e
            for e in row.get("attempts", [])
            if e.get("module") == args.module and e.get("bytes") and e.get("compiledBytes") and e.get("object")
        ]
        if not attempts:
            continue
        best = max(attempts, key=lambda e: e["matchingBytes"] / max(e["bytes"], e["compiledBytes"]))
        address = int(best["address"], 0)
        ratio = best["matchingBytes"] / max(best["bytes"], best["compiledBytes"])
        if (args.module, best["mode"], address) in accepted or address in excluded or ratio < args.minimum_ratio:
            continue
        if args.module == "main" and reservation(address):
            continue
        if not re.search(r"(?<![\w*])\*(?:\(\s*)?native_data_", (ROOT / row["draftSource"]).read_text()):
            continue
        rows.append({**row, "best": best, "ratio": ratio})
    rows = sorted(rows, key=lambda r: (-r["ratio"], r["nativeAlias"]))[: args.limit]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for result in pool.map(lambda row: recover(row, args.module, args.batch), rows):
            results.append(result)
            print(
                {"function": result["nativeAlias"], "matched": "match" in result, "attempts": len(result["attempts"])},
                flush=True,
            )
    matches = [r["match"] for r in results if "match" in r]
    report = {
        "schemaVersion": 1,
        "romSha256": configuration()["romSha256"],
        "module": args.module,
        "moduleInputSha256": sha256(draft_runtime.module_paths(args.module)[0]),
        "matches": matches,
        "nativeSymbols": {r["symbol"]: r["target"] for e in matches for r in e["relocations"]},
        "wholeModuleLinked": False,
        "sourceReconstructionComplete": False,
        "limitations": [
            "Only ordinary C scalar-pointee type hypotheses are generated from existing C drafts; no original executable data becomes source.",
            "Each accepted hypothesis requires fresh compilation and complete byte/ELF relocation agreement. Unsupported platform fixtures remain explicit.",
        ],
    }
    write_json(ROOT / f"evidence/attempts/{args.module}-{args.batch}.json", results)
    write_json(target, report)
    print({"functions": len(matches), "bytes": sum(e["bytes"] for e in matches)})


if __name__ == "__main__":
    main()
