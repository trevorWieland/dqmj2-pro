import json
import sys
from pathlib import Path

import match_overlay_modules as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov000_cache_constructor_fixture_20261029 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / "src/overlays/ov000_20261029_cache_records_9c1f689a0902.c"
WORK = ROOT / "work/ov000-cache-abi/20261029/cache-records"
REPORT = ROOT / "evidence/matches/ov000-20261029-cache-records01.json"
METADATA = {
    0x0221D6F8: (0x0221D6F8, 132, 0x02246318, 20, 1, 0x0222FB4C, 1, 4),
    0x02221AA4: (0x02221AA4, 124, 0x02246438, 24, 1, 0x0222FBBC, 0, 16),
}


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python/Unicorn required")
    module, overlay, unused = measured_module("ov000")
    main_metadata, main, unused = measured_module("main")
    compiler.WORK = WORK / "compiler"
    report, code = compiler.compile_compare("ov000", SOURCE, "2", "off")
    if report["returncode"] or len(report["functions"]) != len(METADATA):
        raise ValueError("Frozen cache sources did not compile as two functions")
    matches = []
    for entry in report["functions"]:
        if not entry["exactAfterDeclaredRelocation"]:
            raise ValueError("Frozen cache source no longer matches its native span")
        entry.update(processor="arm9", sourceLanguage="C")
        metadata = METADATA[int(entry["address"], 0)]
        bindings = qualified_bindings(entry)
        directory = WORK / "link" / entry["objectSha256"] / entry["name"]
        proof = validate(entry, bindings, directory)
        linked = (directory / "caller.bin").read_bytes()
        save_link_snapshots.DIRECTORY = WORK / "link-artifacts"
        entry.update(save_link_snapshots.freeze_link(proof))
        native = overlay[metadata[0] - 0x021D7240:metadata[0] - 0x021D7240 + metadata[1]]
        results = []
        for index in [None, *range(8)]:
            for repeat in range(5):
                vector = len(results)
                original = execute(main, overlay, native, metadata, index, vector)
                rebuilt = execute(main, overlay, linked, metadata, index, vector)
                if original != rebuilt:
                    raise ValueError("Native/source cache register, memory or trace difference")
                results.append(original)
        entry.update(nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                     ordinaryCBytes=len(linked), justifiedAssemblyBytes=0,
                     oracle={"vectors": len(results), "executions": len(results) * 2,
                             "actualReturnRequired": True, "nativeCalleesExecuted": True,
                             "hostCalleeStubs": False, "instructionBound": 30000, "results": results,
                             "supportedContext": "Bank1 cache-full failure or matching cached name with all128 leases busy and null backing allocations",
                             "limitations": ["Success rendering or filesystem/heap loading not executed",
                                             "Synthetic bounded records do not establish a live application state",
                                             "Malformed pointers and non-null backing frees unsupported"]})
        matches.append(entry)
    result = {"schemaVersion": 1, "createdUtc": now(), "romSha256": configuration()["romSha256"],
              "processor": "arm9", "module": "ov000", "moduleInputSha256": module["sha256"],
              "mainInputSha256": main_metadata["sha256"], "source": str(SOURCE.relative_to(ROOT)),
              "sourceSha256": sha256(SOURCE), "matches": matches, "compileReport": report,
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "generator": Path(__file__).name, "generatorSha256": sha256(Path(__file__)),
              "fixture": "ov000_cache_constructor_fixture_20261029.py",
              "fixtureSha256": sha256(ROOT / "ov000_cache_constructor_fixture_20261029.py"),
              "nativeSymbols": {item["symbol"]: item["target"] for entry in matches for item in entry["relocations"]},
              "sdkCacheAbiProof": "evidence/abi/main-cache-sdk-20261029.json"}
    write_json(REPORT, result)
    compiler.immutable(WORK / ("match-" + compiler.sha(json.dumps(result, sort_keys=True).encode()) + ".json"),
                       json.dumps(result, indent=2).encode())
    print(json.dumps({"functions": len(matches), "bytes": sum(e["ordinaryCBytes"] for e in matches),
                      "executions": sum(e["oracle"]["executions"] for e in matches),
                      "report": str(REPORT.relative_to(ROOT))}))


if __name__ == "__main__":
    run()
