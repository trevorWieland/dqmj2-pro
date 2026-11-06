import json
import sys
from pathlib import Path

import match_overlay_modules as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov007_constructor_fixture_20261029 import CONSTRUCTORS, OPEN, LEASE, execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / "src/overlays/ov007_20261029_constructors_157d10189451.c"
WORK = ROOT / "work/ov007-finish/20261029/constructors"
REPORT = ROOT / "evidence/matches/ov007-20261029-constructors01.json"
ABI_REPORT = ROOT / "evidence/abi/main-cache-sdk-20261029.json"


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python/Unicorn required")
    metadata, overlay, unused = measured_module("ov007")
    main_metadata, main, unused = measured_module("main")
    compiler.WORK = WORK / "compiler"
    report, code = compiler.compile_compare("ov007", SOURCE, "2", "off")
    if report["returncode"] or len(report["functions"]) != 2:
        raise ValueError("Frozen constructor source did not compile as two functions")
    matches, vector_index = [], 0
    for entry in report["functions"]:
        if not entry["exactAfterDeclaredRelocation"]:
            raise ValueError("Frozen constructor source no longer matches its full native span")
        entry.update(processor="arm9", sourceLanguage="C")
        bindings = qualified_bindings(entry)
        directory = WORK / "link" / entry["objectSha256"] / entry["name"]
        proof = validate(entry, bindings, directory)
        linked = (directory / "caller.bin").read_bytes()
        save_link_snapshots.DIRECTORY = WORK / "link-artifacts"
        entry.update(save_link_snapshots.freeze_link(proof))
        address = int(entry["address"], 0)
        bank = CONSTRUCTORS.index(address)
        native = overlay[address - 0x021D7240:address - 0x021D7240 + len(linked)]
        vectors = []
        for index in [None, *range(8)]:
            for repeat in range(5):
                case = {"bank": bank, "index": index, "freeSlot": None, "repeat": repeat}
                original = execute(main, overlay, address, native, case, vector_index)
                rebuilt = execute(main, overlay, address, linked, case, vector_index)
                if original != rebuilt:
                    raise ValueError("Native/source constructor register, memory or trace difference")
                vectors.append(original)
                vector_index += 1
        entry.update(nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                     ordinaryCBytes=len(linked), justifiedAssemblyBytes=0,
                     oracle={"vectors": len(vectors), "executions": len(vectors) * 2,
                             "actualReturnRequired": True, "nativeCalleesExecuted": True,
                             "hostCalleeStubs": False, "instructionBound": 30000, "results": vectors,
                             "supportedContext": "Both cache banks; all slots busy or matching cached name with exhausted leases; null backing allocations allow native close without heap frees",
                             "limitations": ["Success allocation, rendering and cache-miss file loading not executed",
                                             "Synthetic bounded cache records do not establish a live scene state",
                                             "No malformed pointer, file, heap or hardware-context guarantee"]})
        matches.append(entry)
    sdk_results = []
    for bank in range(2):
        for index in [None, *range(8)]:
            for repeat in range(5):
                case = {"bank": bank, "index": index, "repeat": repeat}
                sdk_results.append(execute(main, overlay, OPEN, None, case, 1000 + len(sdk_results)))
    lease_results = []
    indices = [*range(8), -1, 0x100, 0xFFFFFF00, 0x7FFFFFFF, 0x80000000]
    for bank in range(2):
        for index in indices:
            for free_slot in (0, 63, 127, None):
                case = {"bank": bank, "index": index, "freeSlot": free_slot}
                lease_results.append(execute(main, overlay, LEASE, None, case, 2000 + len(lease_results)))
    abi = {"schemaVersion": 1, "createdUtc": now(), "romSha256": configuration()["romSha256"],
           "processor": "arm9", "module": "main", "moduleInputSha256": main_metadata["sha256"],
           "generator": Path(__file__).name, "generatorSha256": sha256(Path(__file__)),
           "fixture": "ov007_constructor_fixture_20261029.py",
           "fixtureSha256": sha256(ROOT / "ov007_constructor_fixture_20261029.py"),
           "facts": [{"address": "0x02048404", "mode": "arm", "bytes": 216,
                      "nativeSha256": compiler.sha(main[0x48404:0x484DC]),
                      "signature": "u8 (u32 bank, const char *name, u32 argument2, u32 argument3)",
                      "measuredReturnRepresentation": "Full R0 is 0..7 or 0x000000ff; never signed -1 or upper-bit-contaminated in tested cases",
                      "instructionEvidence": {"cachedReturn": ["0x02048448", "0x0204844c"],
                                              "indexByteMasks": ["0x02048454", "0x020484bc"],
                                              "indexBounds": ["0x02048458", "0x020484c0"],
                                              "loadedReturn": ["0x020484b0", "0x020484b4"],
                                              "exhaustedReturn": ["0x020484c8", "0x020484d0"]},
                      "results": sdk_results,
                      "limitations": ["Banks 0 and 1 only; no narrowing or acceptance of negative/high-bit bank IDs inferred",
                                      "Cache-miss loading return block has static index-range evidence but its filesystem/heap path is not dynamically executed"]},
                     {"address": "0x0204854c", "mode": "arm", "bytes": 104,
                      "nativeSha256": compiler.sha(main[0x4854C:0x485B4]),
                      "signature": "CacheLease * (u32 bank, u32 recordIndex)",
                      "argumentEvidence": {"r0BankMla": "0x0204855c", "r1RecordIndexMla": "0x0204857c"},
                      "behavior": "First free of128 eight-byte leases at bankBase+0x320; preserve flags except set bit0, store bankBase+100*full32bitIndex modulo2^32 at lease+4; return lease pointer or0",
                      "negativeUpperBitIndexBehavior": "Raw arithmetic is measured for -1,0x100,0xffffff00,0x7fffffff,0x80000000; no record pointer dereference or record validity claim",
                      "results": lease_results,
                      "limitations": ["Bank is0 or1; invalid indices exercise pointer-word arithmetic only and are not valid cache records"]}],
           "actualReturnRequired": True, "hostCalleeStubs": False,
           "nativeExecutions": len(sdk_results) + len(lease_results), "newSourceCreditBytes": 0,
           "reproduce": "python match_ov007_20261029_constructors.py"}
    write_json(ABI_REPORT, abi)
    result = {"schemaVersion": 1, "createdUtc": now(), "romSha256": configuration()["romSha256"],
              "processor": "arm9", "module": "ov007", "moduleInputSha256": metadata["sha256"],
              "mainInputSha256": main_metadata["sha256"], "source": str(SOURCE.relative_to(ROOT)),
              "sourceSha256": sha256(SOURCE), "matches": matches, "compileReport": report,
              "sdkAbiProof": str(ABI_REPORT.relative_to(ROOT)), "sdkAbiProofSha256": sha256(ABI_REPORT),
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "generator": Path(__file__).name, "generatorSha256": sha256(Path(__file__)),
              "fixture": "ov007_constructor_fixture_20261029.py",
              "fixtureSha256": sha256(ROOT / "ov007_constructor_fixture_20261029.py"),
              "nativeSymbols": {item["symbol"]: item["target"] for entry in matches for item in entry["relocations"]}}
    compiler.immutable(WORK / ("match-" + compiler.sha(json.dumps(result, sort_keys=True).encode()) + ".json"),
                       json.dumps(result, indent=2).encode())
    write_json(REPORT, result)
    print(json.dumps({"functions": len(matches), "bytes": sum(e["ordinaryCBytes"] for e in matches),
                      "constructorExecutions": vector_index * 2, "sdkExecutions": abi["nativeExecutions"],
                      "report": str(REPORT.relative_to(ROOT))}))


if __name__ == "__main__":
    run()
