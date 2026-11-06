import json
import sys
from pathlib import Path

import match_overlay_modules as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from overlay_cache_active_fixture_20261029 import ACTIVE, execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCES = {
    "ov001": "src/overlays/ov001_20261029_cache_active_5412a95abbde.c",
    "ov005": "src/overlays/ov005_20261029_cache_active_955e2fff10a2.c",
}
METADATA = {
    "ov001": {"address": 0x021FC908, "bytes": 84, "state": 0x02239C10,
              "stateBytes": 40, "bank": 1, "name": 0x0222EE38, "handle": 0x0222ED34,
              "leaseOffset": 32, "recordOffset": 36, "flushPalette": False},
    "ov005": {"address": 0x021E0AB0, "bytes": 96, "state": 0x021ED234,
              "stateBytes": 48, "bank": 1, "name": 0x021E7738, "handle": 0x021E74A8,
              "leaseOffset": 44, "recordOffset": 28, "flushPalette": True},
}


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python/Unicorn required")
    main_metadata, main, unused = measured_module("main")
    summaries = []
    for module, source_path in SOURCES.items():
        source = ROOT / source_path
        work = ROOT / f"work/overlay-cache-abi/20261029/{module}-active"
        metadata = METADATA[module]
        native_metadata, overlay, unused = measured_module(module)
        compiler.WORK = work / "compiler"
        report, code = compiler.compile_compare(module, source, "2", "off")
        if report["returncode"] or len(report["functions"]) != 1:
            raise ValueError("Frozen active-record source did not compile as one function")
        entry = report["functions"][0]
        if not entry["exactAfterDeclaredRelocation"]:
            raise ValueError("Frozen active-record source no longer matches all native bytes")
        entry.update(processor="arm9", sourceLanguage="C")
        bindings = qualified_bindings(entry)
        directory = work / "link" / entry["objectSha256"]
        proof = validate(entry, bindings, directory)
        linked = (directory / "caller.bin").read_bytes()
        save_link_snapshots.DIRECTORY = work / "link-artifacts"
        entry.update(save_link_snapshots.freeze_link(proof))
        address = metadata["address"]
        native = overlay[address - 0x021D7240:address - 0x021D7240 + metadata["bytes"]]
        results = []
        for record_index in range(8):
            for lease_index in (0, 63, 127):
                for repeat in range(3):
                    vector = len(results)
                    original = execute(main, overlay, native, metadata, record_index, lease_index, vector)
                    rebuilt = execute(main, overlay, linked, metadata, record_index, lease_index, vector)
                    if original != rebuilt:
                        raise ValueError("Native/source active-record register, memory or trace difference")
                    results.append(original)
        entry.update(nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                     ordinaryCBytes=len(linked), justifiedAssemblyBytes=0,
                     oracle={"vectors": len(results), "executions": len(results) * 2,
                             "actualReturnRequired": True, "nativeCalleesExecuted": True,
                             "hostCalleeStubs": False, "instructionBound": 100000, "results": results,
                             "supportedContext": "All8 cache-hit record indices; first/middle/last free lease; actual SDK setter; optional CPU palette flush with DMA channel=-1",
                             "limitations": ["Full-cache, exhausted lease, cache-miss filesystem and malformed pointers unsupported",
                                             "No physical display/timing/DMA proof; MMIO and palette VRAM are explicit memory models",
                                             "Final R0 holds the setter argument but these C routines return void",
                                             "Synthetic initialized state does not establish a live or future game scene"]})
        target = ROOT / f"evidence/matches/{module}-20261029-cache-active01.json"
        result = {"schemaVersion": 1, "createdUtc": now(), "romSha256": configuration()["romSha256"],
                  "processor": "arm9", "module": module, "moduleInputSha256": native_metadata["sha256"],
                  "mainInputSha256": main_metadata["sha256"], "source": source_path,
                  "sourceSha256": sha256(source), "matches": [entry], "compileReport": report,
                  "wholeModuleLinked": False, "sourceReconstructionComplete": False,
                  "generator": Path(__file__).name, "generatorSha256": sha256(Path(__file__)),
                  "fixture": "overlay_cache_active_fixture_20261029.py",
                  "fixtureSha256": sha256(ROOT / "overlay_cache_active_fixture_20261029.py"),
                  "nativeSymbols": {item["symbol"]: item["target"] for item in entry["relocations"]},
                  "sdkCacheAbiProof": "evidence/abi/main-cache-sdk-20261029.json",
                  "sdkSetterEvidence": {"address": "0x0204b1a0", "mode": "arm", "bytes": 16,
                      "nativeSpanSha256": compiler.sha(main[0x4B1A0:0x4B1B0]),
                      "argument": "R0 pointer word", "effect": "Store R0 at0x0210297c; return preserving R0",
                      "writeAddress": hex(ACTIVE), "newSourceCreditBytes": 0}}
        write_json(target, result)
        compiler.immutable(work / ("match-" + compiler.sha(json.dumps(result, sort_keys=True).encode()) + ".json"),
                           json.dumps(result, indent=2).encode())
        summaries.append({"module": module, "functions": 1, "bytes": len(linked),
                          "executions": len(results) * 2, "report": str(target.relative_to(ROOT))})
    print(json.dumps(summaries))


if __name__ == "__main__":
    run()
