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

SOURCES = {
    0x02207954: "src/overlays/ov000_20261029_cache_position_02207954_01e1077c3139.c",
    0x02208638: "src/overlays/ov000_20261029_cache_position_02208638_2153c3da93a2.c",
}
METADATA = {
    0x02207954: (0x02207954, 260, 0x022382C8, 0x11C, 1, 0x0222F708, 0xF2, 0x108),
    0x02208638: (0x02208638, 368, 0x022383E8, 0x114, 1, 0x0222F740, 0xF2, 0x104),
}
WORK = ROOT / "work/ov000-cache-abi/20261029/positions"
REPORT = ROOT / "evidence/matches/ov000-20261029-cache-positions01.json"


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python/Unicorn required")
    module, overlay, unused = measured_module("ov000")
    main_metadata, main, unused = measured_module("main")
    matches, reports = [], []
    for address, source_path in SOURCES.items():
        source = ROOT / source_path
        compiler.WORK = WORK / f"{address:08x}" / "compiler"
        report, code = compiler.compile_compare("ov000", source, "2,p", "off")
        if report["returncode"] or len(report["functions"]) != 1:
            raise ValueError("Frozen position source did not compile as one function")
        entry = report["functions"][0]
        if not entry["exactAfterDeclaredRelocation"]:
            raise ValueError("Frozen position source no longer matches all native bytes")
        entry.update(processor="arm9", sourceLanguage="C")
        metadata = METADATA[address]
        bindings = qualified_bindings(entry)
        directory = WORK / f"{address:08x}" / "link" / entry["objectSha256"]
        proof = validate(entry, bindings, directory)
        linked = (directory / "caller.bin").read_bytes()
        save_link_snapshots.DIRECTORY = WORK / "link-artifacts"
        entry.update(save_link_snapshots.freeze_link(proof))
        native = overlay[address - 0x021D7240:address - 0x021D7240 + metadata[1]]
        results = []
        for index in [None, *range(8)]:
            for repeat in range(5):
                vector = len(results)
                original = execute(main, overlay, native, metadata, index, vector)
                rebuilt = execute(main, overlay, linked, metadata, index, vector)
                if original != rebuilt:
                    raise ValueError("Native/source position register, memory or trace difference")
                results.append(original)
        entry.update(nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                     ordinaryCBytes=len(linked), justifiedAssemblyBytes=0,
                     oracle={"vectors": len(results), "executions": len(results) * 2,
                             "actualReturnRequired": True, "nativeCalleesExecuted": True,
                             "hostCalleeStubs": False, "instructionBound": 30000, "results": results,
                             "supportedContext": "Bank1 full-cache failure or matching cached name with exhausted candidate scan and null backing allocations",
                             "limitations": ["Success allocations/rendering and filesystem loading not executed",
                                             "Synthetic records do not establish live game state or independent high candidate objects",
                                             "Malformed pointers and non-null backing frees unsupported"]})
        matches.append(entry)
        reports.append(report)
    result = {"schemaVersion": 1, "createdUtc": now(), "romSha256": configuration()["romSha256"],
              "processor": "arm9", "module": "ov000", "moduleInputSha256": module["sha256"],
              "mainInputSha256": main_metadata["sha256"],
              "sourceHashes": {path: sha256(ROOT / path) for path in SOURCES.values()},
              "matches": matches, "compileReports": reports,
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "generator": Path(__file__).name, "generatorSha256": sha256(Path(__file__)),
              "fixture": "ov000_cache_constructor_fixture_20261029.py",
              "fixtureSha256": sha256(ROOT / "ov000_cache_constructor_fixture_20261029.py"),
              "nativeSymbols": {item["symbol"]: item["target"] for entry in matches for item in entry["relocations"]},
              "sdkCacheAbiProof": "evidence/abi/main-cache-sdk-20261029.json",
              "sdkAliasQualification": "evidence/abi/main-cache-view-alias-20261029.json",
              "coordinateEvidence": "Ordinary two-halfword aggregate initialized to{0,0}; native stack address/store bytes match with declared O2,p profile"}
    write_json(REPORT, result)
    compiler.immutable(WORK / ("match-" + compiler.sha(json.dumps(result, sort_keys=True).encode()) + ".json"),
                       json.dumps(result, indent=2).encode())
    print(json.dumps({"functions": len(matches), "bytes": sum(e["ordinaryCBytes"] for e in matches),
                      "executions": sum(e["oracle"]["executions"] for e in matches),
                      "report": str(REPORT.relative_to(ROOT))}))


if __name__ == "__main__":
    run()
