import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from main_cache_close_fixture_20261029 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / "src/runtime/20261029_cache_sdk/close_99508969fcf1.c"
WORK = ROOT / "work/main-cache-sdk/20261029/close"
REPORT = ROOT / "evidence/matches/main-20261029-cache-close01.json"


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python/Unicorn required")
    metadata, main, unused = measured_module("main")
    compiler.WORK = WORK / "compiler"
    records, code = compiler.compare(SOURCE, "main", "2", "off")
    if len(records) != 1 or records[0].get("compileFailed"):
        raise ValueError("Frozen SDK close source did not compile as one function")
    entry = records[0]
    if not entry["exactAfterDeclaredRelocation"]:
        raise ValueError("Frozen SDK close source no longer matches all112 bytes")
    bindings = qualified_bindings(entry)
    directory = WORK / "link" / entry["objectSha256"]
    proof = validate(entry, bindings, directory)
    linked = (directory / "caller.bin").read_bytes()
    save_link_snapshots.DIRECTORY = WORK / "link-artifacts"
    entry.update(save_link_snapshots.freeze_link(proof))
    native = main[0x484DC:0x4854C]
    results = []
    for bank in range(2):
        for index in range(8):
            for length in (0, 1, 5, 31, 63):
                for flags in (0, 1, 0x80000000, 0xFFFFFFFF):
                    vector = len(results)
                    original = execute(main, native, bank, index, length, flags, vector)
                    rebuilt = execute(main, linked, bank, index, length, flags, vector)
                    if original != rebuilt:
                        raise ValueError("Native/linked SDK close registers, memory or traces differ")
                    results.append(original)
    entry.update(processor="arm9", sourceLanguage="C", ordinaryCBytes=112,
                 justifiedAssemblyBytes=0, nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 oracle={"vectors": len(results), "executions": len(results) * 2,
                         "actualReturnRequired": True, "freshMachinePerExecution": True,
                         "nativeCalleesExecuted": True, "hostCalleeStubs": False,
                         "instructionBound": 20000, "results": results,
                         "supportedContext": "Both banks/all8 record indices; active/inactive/high flag bits; ASCII lengths0/1/5/31/63; null backing pointers",
                         "limitations": ["Non-null backing allocation frees and heap state unsupported",
                                         "Malformed or unterminated names, invalid bank/index arithmetic unsupported",
                                         "No game scene/save persistence meaning is established"]})
    result = {"schemaVersion": 1, "createdUtc": now(), "romSha256": configuration()["romSha256"],
              "processor": "arm9", "module": "main", "moduleInputSha256": metadata["sha256"],
              "source": str(SOURCE.relative_to(ROOT)), "sourceSha256": sha256(SOURCE),
              "matches": [entry], "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "generator": Path(__file__).name, "generatorSha256": sha256(Path(__file__)),
              "fixture": "main_cache_close_fixture_20261029.py",
              "fixtureSha256": sha256(ROOT / "main_cache_close_fixture_20261029.py"),
              "nativeSymbols": {row["symbol"]: row["target"] for row in entry["relocations"]}}
    write_json(REPORT, result)
    (WORK / ("match-" + compiler.sha(json.dumps(result, sort_keys=True).encode()) + ".json")).write_text(json.dumps(result, indent=2))
    print(json.dumps({"functions": 1, "bytes": 112, "executions": len(results) * 2,
                      "report": str(REPORT.relative_to(ROOT))}))


if __name__ == "__main__":
    run()
