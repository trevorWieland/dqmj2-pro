import json
from pathlib import Path

import match_runtime as compiler
from project import ROOT, configuration, now, sha256, write_json

WORK = ROOT / "work/ov000-recovery/20261029/birth-menu-profiles"
SOURCE = ROOT / "nonmatching/ov000/20261029-birth-context01/menu_candidates_readable.c"


def run():
    compiler.WORK = WORK
    original_flags = compiler.FLAGS[:]
    results = []
    try:
        for version in ("base", "sp1p5", "sp1p6"):
            for symbols in ("off", "on"):
                compiler.FLAGS[compiler.FLAGS.index("-sym") + 1] = symbols
                executable = ROOT / f"tools/mwccarm/mwccarm/2.0/{version}/mwccarm.exe"
                rows, found = compiler.compare(SOURCE, "ov000", "2", "off", True,
                                               False, executable)
                results.append({"version": version, "debugSymbols": symbols, "functions": rows})
    finally:
        compiler.FLAGS[:] = original_flags
    report = {
        "createdUtc": now(),
        "romSha256": configuration()["romSha256"],
        "source": str(SOURCE.relative_to(ROOT)),
        "sourceSha256": sha256(SOURCE),
        "results": results,
        "accepted": False,
        "matchedSourceCredit": 0,
        "reproduction": "python probe_ov000_birth_menu_profiles_20261029.py",
        "generatorSha256": sha256(Path(__file__)),
    }
    write_json(WORK / "results.json", report)
    print(json.dumps({"profiles": len(results), "sizesAndMatchingBytes": [
        [row["compiledBytes"], row["matchingBytes"]]
        for result in results for row in result["functions"]]}))


if __name__ == "__main__":
    run()
