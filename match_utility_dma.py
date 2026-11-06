import json
from pathlib import Path
import utility_code
import utility_oracle
import utility_runtime

ROOT = Path(__file__).resolve().parent


def main():
    source = ROOT / "src/utility/dma/guarded.c"
    compiler = ROOT / "tools/mwccarm/mwccarm/1.2/base/mwccarm.exe"
    targets = {0x01FF81F0: 72, 0x01FF8238: 48}
    previous = json.loads((ROOT / "evidence/matches/utility-dma01.json").read_text())
    entries = {int(entry["address"], 0): entry for entry in previous["matches"]}
    matches = []
    for address, size in targets.items():
        expected = entries[address]
        if expected["source"] != source.relative_to(ROOT).as_posix() or expected["sourceSha256"] != utility_runtime.sha(source.read_bytes()):
            raise ValueError("Frozen utility DMA C source changed")
        spec = dict(utility_code.accepted_spec(expected), compilerPath=compiler)
        if spec["mode"] != "thumb" or spec["bytes"] != size:
            raise ValueError("Utility DMA native extent or mode changed")
        entry, code = utility_code.compile_compare(source, spec)
        if code is None:
            raise ValueError("Frozen utility DMA C no longer matches")
        entry["oracle"] = utility_oracle.oracle(code, spec)
        matches.append(entry)
    bindings = {rel["symbol"]: rel["target"] for entry in matches for rel in entry["relocations"]}
    report = {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM,
              "runtimeMappingCanonical": True, "matches": matches, "nativeSymbols": bindings,
              "nativeSymbolBindings": [{"name": name, "program": utility_runtime.PROGRAM, "processor": "arm9",
                                        "module": "utility-child-arm9-main", "address": address, "mode": "arm"} for name, address in bindings.items()],
              "reproduce": ["python", "match_utility_dma.py"], "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "limitations": ["Matching MW 1.2 configuration is pinned per unit without claiming historical compiler attribution",
                              "Native Thumb CALL relocations target measured ARM helper entries and require real linker interworking to BLX",
                              "Bounded caller tests execute the measured native interrupt-mask helpers; those helpers do not receive source credit from these tests",
                              "No physical DMA transfers or complete embedded-program execution are claimed"]}
    (ROOT / "evidence/matches/utility-dma01.json").write_text(json.dumps(report, indent=2) + "\n")
    print({"functions": len(matches), "nativeBytes": sum(entry["bytes"] for entry in matches),
           "nativeAndRecompiledCalls": sum(entry["oracle"]["nativeAndRecompiledCalls"] for entry in matches)})


if __name__ == "__main__":
    main()
