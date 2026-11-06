import json
from pathlib import Path

import match_runtime as compiler
from link_runtime_unit import measured_module
from project import ROOT, configuration, now, sha256, write_json

BATCH = ROOT / "nonmatching/ov000/20261029-birth-context01"
WORK = ROOT / "work/ov000-recovery/20261029/birth-menu-compile"
ADDRESS = 0x02227F94


def run():
    metadata, binary, unused = measured_module("ov000")
    compiler.WORK = WORK
    source = BATCH / "menu_candidates_readable.c"
    reports = []
    for speed in (False, True):
        rows, found = compiler.compare(source, "ov000", "2", "off", speed)
        if len(rows) != 1:
            raise ValueError("Repaired menu candidate did not compile as one function")
        entry = rows[0]
        if int(entry["address"], 0) != ADDRESS:
            raise ValueError("Wrong qualified candidate address")
        path = BATCH / ("compile-readable-speed" + str(int(speed)) + ".json")
        write_json(path, {"createdUtc": now(), "functions": rows})
        reports.append({"path": str(path.relative_to(ROOT)), "sha256": sha256(path), **entry})
    original = ROOT / "nonmatching/ov000/20261029-broad01/functions/02227f94-arm/result.json"
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
        "bytes": 360,
        "moduleSha256": metadata["sha256"],
        "nativeSpanSha256": compiler.sha(binary[offset:offset + 360]),
        "source": str(source.relative_to(ROOT)),
        "sourceSha256": sha256(source),
        "physicalLines": len(source.read_text().splitlines()),
        "derivedFromReport": str(original.relative_to(ROOT)),
        "derivedFromReportSha256": sha256(original),
        "nativeStackArrays": [
            {"spOffset": "0x15", "bytes": 3, "type": "u8[3]"},
            {"spOffset": "0x18", "bytes": 12, "type": "s32[3]"},
            {"spOffset": "0x24", "bytes": 12, "type": "s32[3]"},
        ],
        "repairs": [
            "Recovered omitted stack arrays from native byte/word accesses and three-entry bounds",
            "Corrected pointer increment to one signed32 element for native add4",
            "Retained full32 duplicate sentinel set by native MVN rather than u8 truncation",
        ],
        "compilationReports": reports,
        "bestMatchingBytes": best["matchingBytes"],
        "bestCompiledBytes": best["compiledBytes"],
        "bestByteSimilarity": best["matchingBytes"] / 360,
        "accepted": False,
        "matchedSourceCredit": 0,
        "executionValidated": False,
        "wholeModuleLinked": False,
        "reproduction": "python compile_ov000_birth_menu_20261029.py",
        "generatorSha256": sha256(Path(__file__)),
        "unsupportedBehavior": [
            "Remaining scheduling, conditional-branch and register differences",
            "Complete native delegate/resource fixture and caller contract not yet executed",
            "Selected slot outside0..2 and malformed resources/pointers unsupported",
        ],
    }
    write_json(BATCH / "menu-candidates-result.json", result)
    print(json.dumps({"compiled": True, "nativeBytes": 360,
                      "matchingBytes": best["matchingBytes"], "accepted": False}))


if __name__ == "__main__":
    run()
