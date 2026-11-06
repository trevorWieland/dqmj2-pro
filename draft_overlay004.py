import argparse
import concurrent.futures
import json
import os
import subprocess
import types
from pathlib import Path

import draft_runtime as draft
import match_overlay_modules as matcher

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/overlay004-recovery"


def decompile(original):
    assembly, context = draft.FUNCTION_INPUTS[original]
    directory = WORK / "m2c" / original
    directory.mkdir(parents=True, exist_ok=True)
    source = directory / "input.s"
    source.write_text(assembly)
    context_path = directory / "context.c"
    context_path.write_text(context)
    command = [
        str(Path(matcher.sys.executable)),
        str(draft.M2C),
        "--target",
        "arm-mwcc-c",
        "--comment-style",
        "none",
        "--no-cache",
        "--valid-syntax",
        "--context",
        str(context_path),
        "-f",
        original,
        str(source),
    ]
    result = subprocess.run(
        command,
        cwd=ROOT,
        env=dict(os.environ, PYTHONPATH=str(ROOT / "tools/m2c-python")),
        capture_output=True,
        text=True,
        timeout=60,
    )
    item = {
        "original": original,
        "command": command,
        "returncode": result.returncode,
        "stderr": result.stderr,
    }
    (directory / "m2c-output.txt").write_text(result.stdout)
    if result.returncode:
        return item
    try:
        recovered = draft.source_text(result.stdout, original)
        recovered = recovered.replace("native_fn_", "func_").replace("native_data_", "data_")
    except Exception as error:
        item["failure"] = str(error)
        return item
    path = directory / (original + ".c")
    path.write_text(recovered)
    item["source"] = str(path.relative_to(ROOT))
    return item


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--batch", default="drafts01")
    parser.add_argument("--include", nargs="+")
    args = parser.parse_args()
    global WORK
    WORK = WORK / args.batch
    if (WORK / "attempts.json").exists():
        raise ValueError("Select a fresh experiment batch")
    draft.WORK = WORK / "inputs"
    draft.OPTIONS = types.SimpleNamespace(
        module="ov004",
        thumb=False,
        word_args=True,
        abi_slots=True,
        register_order=True,
        stack_buffers=True,
        direct_increments=True,
        typed_globals=True,
    )
    draft.inputs()
    lookup, functions = matcher.symbol_data("ov004")
    draft.FUNCTION_ADDRESSES.update(
        {spec["name"]: f"{address:08x}" for address, spec in functions.items()}
    )
    candidates = [
        spec["name"]
        for address, spec in functions.items()
        if spec["size"] not in [4, 12, 24, 60]
        and not spec["name"].startswith("__sinit")
    ]
    if args.include:
        candidates = [name for name in candidates if name in args.include]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(decompile, candidates))
    for item in results:
        item["attempts"] = []
        if "source" not in item:
            print(
                json.dumps(
                    {
                        "function": item["original"],
                        "failure": item.get("failure", item.get("stderr")),
                    }
                ),
                flush=True,
            )
            continue
        best = 0
        for optimization in ["2", "2,p", "3,p", "4,p", "3", "4"]:
            report, codes = matcher.compile_compare(
                "ov004", ROOT / item["source"], optimization, "off"
            )
            attempt_path = (
                WORK
                / "compiles"
                / (matcher.sha(json.dumps(report, sort_keys=True).encode()) + ".json")
            )
            matcher.immutable(attempt_path, json.dumps(report, indent=2).encode())
            score = max(
                (entry["matchingBytes"] for entry in report["functions"]), default=0
            )
            best = max(best, score)
            item["attempts"].append(
                {
                    "optimization": optimization,
                    "report": str(attempt_path.relative_to(ROOT)),
                    "score": score,
                    "returncode": report["returncode"],
                }
            )
            exact = [
                entry
                for entry in report["functions"]
                if entry["exactAfterDeclaredRelocation"]
            ]
            if exact:
                item["exactOptimization"] = optimization
                item["exactFunctions"] = [entry["name"] for entry in exact]
                break
        print(
            json.dumps(
                {
                    "function": item["original"],
                    "bestMatchingBytes": best,
                    "exactOptimization": item.get("exactOptimization"),
                }
            ),
            flush=True,
        )
    matcher.immutable(WORK / "attempts.json", json.dumps(results, indent=2).encode())
    print(
        json.dumps(
            {
                "candidates": len(candidates),
                "decompiled": sum("source" in item for item in results),
                "exactDrafts": sum("exactOptimization" in item for item in results),
                "report": str((WORK / "attempts.json").relative_to(ROOT)),
            }
        )
    )


if __name__ == "__main__":
    main()
