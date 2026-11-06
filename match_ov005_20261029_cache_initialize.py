import json
import sys
from pathlib import Path

import match_overlay_modules as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov005_cache_initialize_fixture_20261029 import CACHE, execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / "src/overlays/ov005_20261029_cache_initialize_d96bd5d9ceb0.c"
WORK = ROOT / "work/overlay-cache-abi/20261029/ov005-initialize"
REPORT = ROOT / "evidence/matches/ov005-20261029-cache-initialize01.json"
ABI_REPORT = ROOT / "evidence/abi/main-cache-view-alias-20261029.json"


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python/Unicorn required")
    module, overlay, unused = measured_module("ov005")
    main_metadata, main, unused = measured_module("main")
    compiler.WORK = WORK / "compiler"
    report, code = compiler.compile_compare("ov005", SOURCE, "2", "off")
    if report["returncode"] or len(report["functions"]) != 1:
        raise ValueError("Frozen initializer did not compile as one function")
    entry = report["functions"][0]
    if not entry["exactAfterDeclaredRelocation"]:
        raise ValueError("Frozen initializer no longer matches all140 bytes")
    entry.update(processor="arm9", sourceLanguage="C")
    bindings = qualified_bindings(entry)
    directory = WORK / "link" / entry["objectSha256"]
    proof = validate(entry, bindings, directory)
    linked = (directory / "caller.bin").read_bytes()
    save_link_snapshots.DIRECTORY = WORK / "link-artifacts"
    entry.update(save_link_snapshots.freeze_link(proof))
    address = 0x021DDD60
    native = overlay[address - 0x021D7240:address - 0x021D7240 + 140]
    results = []
    counters, kinds = (0, 1, 0xFFFE, 0xFFFF), (0, 1, 4, 0xFFFFFFFF)
    for record_index in range(8):
        for lease_index in (0, 31, 63):
            vector = len(results)
            counter, kind = counters[vector % 4], kinds[(vector // 2) % 4]
            original = execute(main, overlay, native, record_index, lease_index, counter, kind, vector)
            rebuilt = execute(main, overlay, linked, record_index, lease_index, counter, kind, vector)
            if original != rebuilt:
                raise ValueError("Native/source initializer register, memory or trace difference")
            results.append(original)
    ranges = [(0x0204854C, 104), (0x020489F0, 84), (0x0204837C, 68),
              (0x02036BB8, 192), (0x02036C78, 348)]
    abi = {"schemaVersion": 1, "createdUtc": now(), "romSha256": configuration()["romSha256"],
           "processor": "arm9", "module": "main", "moduleInputSha256": main_metadata["sha256"],
           "nativeFunctions": [{"address": hex(start), "mode": "arm", "bytes": size,
                                "nativeSha256": compiler.sha(main[start - 0x02000000:start - 0x02000000 + size])}
                               for start, size in ranges],
           "measuredAlias": {"bank": 0, "bankBase": hex(CACHE),
                             "candidateCellBase": hex(CACHE + 0x320), "candidateStride": 8,
                             "nativeScanBound": 128, "initializedContext": hex(CACHE + 0x520),
                             "contextBytes": 24, "overlappedCandidateIndices": [64, 65, 66]},
           "scope": "Native address arithmetic and actual initializer writes; high scan candidates are not asserted to be independent semantically valid lease objects",
           "dynamicEvidence": str(REPORT.relative_to(ROOT)), "vectors": len(results),
           "executions": len(results) * 2, "newSourceCreditBytes": 0,
           "limitations": ["Initializer vectors use selected free candidates0/31/63 before the overlapping context",
                           "Earlier standalone128-cell scan probes remain physical byte/register evidence with synthetic state",
                           "No save persistence, valid live scene or original SDK type/layout declaration is inferred"]}
    write_json(ABI_REPORT, abi)
    entry.update(nativeSymbolEntries=bindings, isolatedCallerLink=proof, ordinaryCBytes=140,
                 justifiedAssemblyBytes=0,
                 oracle={"vectors": len(results), "executions": len(results) * 2,
                         "actualReturnRequired": True, "nativeCalleesExecuted": True,
                         "hostCalleeStubs": False, "instructionBound": 600000, "results": results,
                         "supportedContext": "Bank0 cache hits and free candidates0/31/63; actual native SDK initialization, OAM/VRAM CPU fills, palette flush and counter wrap",
                         "limitations": ["No physical display/timing/DMA guarantee; MMIO/OAM/VRAM are explicit mapped-memory models",
                                         "Filesystem loading, cache exhaustion, malformed names/pointers and high overlapping candidates unsupported",
                                         "Synthetic cache and rendering state do not establish a live game scene",
                                         "Routine returns void; final registers are measured machine effects"]})
    result = {"schemaVersion": 1, "createdUtc": now(), "romSha256": configuration()["romSha256"],
              "processor": "arm9", "module": "ov005", "moduleInputSha256": module["sha256"],
              "mainInputSha256": main_metadata["sha256"], "source": str(SOURCE.relative_to(ROOT)),
              "sourceSha256": sha256(SOURCE), "matches": [entry], "compileReport": report,
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "generator": Path(__file__).name, "generatorSha256": sha256(Path(__file__)),
              "fixture": "ov005_cache_initialize_fixture_20261029.py",
              "fixtureSha256": sha256(ROOT / "ov005_cache_initialize_fixture_20261029.py"),
              "nativeSymbols": {item["symbol"]: item["target"] for item in entry["relocations"]},
              "sdkAliasProof": str(ABI_REPORT.relative_to(ROOT)), "sdkAliasProofSha256": sha256(ABI_REPORT)}
    write_json(REPORT, result)
    compiler.immutable(WORK / ("match-" + compiler.sha(json.dumps(result, sort_keys=True).encode()) + ".json"),
                       json.dumps(result, indent=2).encode())
    print(json.dumps({"functions": 1, "bytes": 140, "executions": len(results) * 2,
                      "report": str(REPORT.relative_to(ROOT))}))


if __name__ == "__main__":
    run()
