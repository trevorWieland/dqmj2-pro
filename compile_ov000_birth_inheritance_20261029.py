import json
from pathlib import Path

import match_runtime as compiler
from link_runtime_unit import measured_module
from project import ROOT, configuration, now, sha256, write_json

BATCH = ROOT / "nonmatching/ov000/20261029-birth-context01"
WORK = ROOT / "work/ov000-recovery/20261029/birth-inheritance-compile"
ADDRESS = 0x022298EC


def run():
    metadata, binary, unused = measured_module("ov000")
    compiler.WORK = WORK
    source = BATCH / "inheritance_menu.c"
    reports = []
    for optimization, speed in (("2", False), ("2", True), ("4", True)):
        rows, found = compiler.compare(source, "ov000", optimization, "off", speed)
        if len(rows) != 1 or int(rows[0]["address"], 0) != ADDRESS:
            raise ValueError("Repaired inheritance menu did not yield one qualified function")
        path = BATCH / ("inheritance-compile-o" + optimization + "-speed" + str(int(speed)) + ".json")
        write_json(path, {"createdUtc": now(), "functions": rows})
        reports.append({"path": str(path.relative_to(ROOT)), "sha256": sha256(path), **rows[0]})
    original = ROOT / "nonmatching/ov000/20261029-broad01/functions/022298ec-arm/result.json"
    offset = ADDRESS - int(metadata["base"], 0)
    best = max(reports, key=lambda row: row["matchingBytes"])
    result = {
        "schemaVersion": 1,
        "createdUtc": now(),
        "romSha256": configuration()["romSha256"],
        "processor": "arm9",
        "module": "ov000",
        "address": hex(ADDRESS),
        "mode": "arm",
        "bytes": 1512,
        "moduleSha256": metadata["sha256"],
        "nativeSpanSha256": compiler.sha(binary[offset:offset + 1512]),
        "source": str(source.relative_to(ROOT)),
        "sourceSha256": sha256(source),
        "physicalLines": len(source.read_text().splitlines()),
        "derivedFromReport": str(original.relative_to(ROOT)),
        "derivedFromReportSha256": sha256(original),
        "nativeStackArrays": [
            {"spOffset": "0x14", "bytes": 8, "type": "u8 *[2]"},
            {"spOffset": "0x1c", "bytes": 10, "type": "u8[10]"},
            {"spOffset": "0x26", "bytes": 20, "type": "s16[10]"},
        ],
        "repairs": [
            "Recovered20-byte stack pair buffer and10-byte matching mask",
            "Replaced pointer arithmetic across two scalar locals with real two-pointer array",
            "Corrected signed16-pointer increments to measured native byte strides",
            "Used measured byte/halfword dereference widths instead of illegal void/integer dereferences",
            "Explicitly passed left parent identity to first native record lookup",
        ],
        "compilationReports": reports,
        "bestMatchingBytes": best["matchingBytes"],
        "bestCompiledBytes": best["compiledBytes"],
        "bestByteSimilarity": best["matchingBytes"] / 1512,
        "accepted": False,
        "matchedSourceCredit": 0,
        "executionValidated": False,
        "wholeModuleLinked": False,
        "reproduction": "python compile_ov000_birth_inheritance_20261029.py",
        "generatorSha256": sha256(Path(__file__)),
        "unsupportedBehavior": [
            "Source retains unmeasured soft-float helper and external table contracts",
            "Complete native delegate/resource fixture not yet executed",
            "Invalid records, malformed skill resources and pointer/alias domains unsupported",
            "Compiled similarity is diagnostic; source semantics and linking remain unaccepted",
        ],
    }
    write_json(BATCH / "inheritance-menu-result.json", result)
    print(json.dumps({"compiled": True, "nativeBytes": 1512,
                      "matchingBytes": best["matchingBytes"], "accepted": False}))


if __name__ == "__main__":
    run()
