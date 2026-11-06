import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov007_constructor_fixture_20261029 import OPEN, LEASE, execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCES = {
    OPEN: ("src/runtime/20261029_cache_sdk/lookup_8f132205fc42.c", "2,p"),
    LEASE: ("src/runtime/20261029_cache_sdk/acquire_22c90cbd192f.c", "2"),
}
WORK = ROOT / "work/main-cache-sdk/20261029/lookup-acquire"
REPORT = ROOT / "evidence/matches/main-20261029-cache-lookup01.json"


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python/Unicorn required")
    metadata, main, unused = measured_module("main")
    overlay_metadata, overlay, unused = measured_module("ov007")
    matches = []
    for address, (source_path, optimization) in SOURCES.items():
        source = ROOT / source_path
        compiler.WORK = WORK / f"{address:08x}" / "compiler"
        records, code = compiler.compare(source, "main", optimization, "off")
        if len(records) != 1 or records[0].get("compileFailed"):
            raise ValueError("Frozen SDK source did not compile as one function")
        entry = records[0]
        if not entry["exactAfterDeclaredRelocation"]:
            raise ValueError("Frozen SDK source no longer matches its full native span")
        bindings = qualified_bindings(entry)
        directory = WORK / f"{address:08x}" / "link" / entry["objectSha256"]
        proof = validate(entry, bindings, directory)
        linked = (directory / "caller.bin").read_bytes()
        save_link_snapshots.DIRECTORY = WORK / "link-artifacts"
        entry.update(save_link_snapshots.freeze_link(proof))
        native = main[address - 0x02000000:address - 0x02000000 + entry["bytes"]]
        cases = []
        if address == OPEN:
            for bank in range(2):
                for index in [None, *range(8)]:
                    for repeat in range(5):
                        cases.append({"bank": bank, "index": index, "repeat": repeat})
            limitations = ["Cache-miss filesystem/loading path is not dynamically executed",
                          "Auxiliary loader arguments4/5 are fixed in these cached/full fixtures",
                          "Only exact ASCII cached names and differing names are exercised; no encoding claim"]
        else:
            indices = [*range(8), -1, 0x100, 0xFFFFFF00, 0x7FFFFFFF, 0x80000000]
            for bank in range(2):
                for index in indices:
                    for free_slot in (0, 63, 127, None):
                        cases.append({"bank": bank, "index": index, "freeSlot": free_slot})
            limitations = ["Negative/high indices test raw modulo32 pointer-word stores only; pointers are not dereferenced",
                          "High candidate views overlap other SDK context; no independent valid-object interpretation",
                          "Banks0/1 only; invalid bank addressing and live scene validity unsupported"]
        results = []
        for vector, case in enumerate(cases):
            original = execute(main, overlay, address, native, case, 6000 + vector)
            rebuilt = execute(main, overlay, address, linked, case, 6000 + vector)
            if original != rebuilt:
                raise ValueError("Native/linked SDK registers, memory or traces differ")
            results.append(original)
        entry.update(processor="arm9", sourceLanguage="C", ordinaryCBytes=entry["bytes"],
                     justifiedAssemblyBytes=0, nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                     oracle={"vectors": len(results), "executions": len(results) * 2,
                             "actualReturnRequired": True, "freshMachinePerExecution": True,
                             "nativeCalleesExecuted": address == OPEN, "hostCalleeStubs": False,
                             "instructionBound": 30000, "results": results, "limitations": limitations})
        matches.append(entry)
    result = {"schemaVersion": 1, "createdUtc": now(), "romSha256": configuration()["romSha256"],
              "processor": "arm9", "module": "main", "moduleInputSha256": metadata["sha256"],
              "fixtureOverlayModule": "ov007", "fixtureOverlaySha256": overlay_metadata["sha256"],
              "sourceHashes": {path: sha256(ROOT / path) for path, optimization in SOURCES.values()},
              "matches": matches, "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "generator": Path(__file__).name, "generatorSha256": sha256(Path(__file__)),
              "fixture": "ov007_constructor_fixture_20261029.py",
              "fixtureSha256": sha256(ROOT / "ov007_constructor_fixture_20261029.py"),
              "nativeSymbols": {row["symbol"]: row["target"] for entry in matches for row in entry["relocations"]},
              "sdkAbiProof": "evidence/abi/main-cache-sdk-20261029.json",
              "sdkAliasQualification": "evidence/abi/main-cache-view-alias-20261029.json",
              "calleeCodeOrSourceCredit": 0}
    write_json(REPORT, result)
    snapshot = WORK / ("match-" + compiler.sha(json.dumps(result, sort_keys=True).encode()) + ".json")
    snapshot.write_text(json.dumps(result, indent=2))
    print(json.dumps({"functions": len(matches), "bytes": sum(entry["bytes"] for entry in matches),
                      "executions": sum(entry["oracle"]["executions"] for entry in matches),
                      "report": str(REPORT.relative_to(ROOT))}))


if __name__ == "__main__":
    run()
