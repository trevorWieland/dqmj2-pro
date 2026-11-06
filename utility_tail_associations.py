import json
import struct
from pathlib import Path
import utility_runtime

ROOT = Path(__file__).resolve().parent


def main():
    path = ROOT / "evidence/matches/utility-primitives01.json"
    source_report = json.loads(path.read_text())
    layout, files = utility_runtime.derive()
    modules = {module["id"]: module for module in layout["modules"]}
    rows = []
    for entry in source_report["matches"]:
        if entry.get("oracleShape", {}).get("kind") != "tail-call":
            continue
        module = modules[entry["module"]]
        data = bytes(files[ROOT / module["binary"]])
        first = int(entry["address"], 0) - int(module["base"], 0)
        native = data[first:first + entry["bytes"]]
        if len(native) != 12 or native[:8] != bytes.fromhex("00c09fe51cff2fe1"):
            continue
        target = struct.unpack_from("<I", native, 8)[0]
        if not target & 1:
            continue
        destination = next(module for module in layout["modules"] if module["processor"] == entry["processor"] and
                           int(module["base"], 0) <= target & ~1 < int(module["runtimeEnd"], 0))
        rows.append({"program": utility_runtime.PROGRAM, "processor": entry["processor"], "module": entry["module"],
                     "address": entry["address"], "bytes": 12, "sha256": utility_runtime.sha(native),
                     "creditedSourceReport": path.relative_to(ROOT).as_posix(), "creditedSourceSymbol": entry["name"],
                     "source": entry["source"], "sourceSha256": entry["sourceSha256"], "objectSha256": entry["objectSha256"],
                     "entryMode": "arm", "targetModule": destination["id"], "targetAddress": hex(target), "targetMode": "thumb",
                     "nativeOperation": "Load the tagged target into IP and tail-transfer through BX IP",
                     "historicalOrigin": "Uncertain whether an original C tail wrapper or linker-generated trampoline",
                     "separateExecutableRegion": False, "additionalSourceByteCredit": 0, "additionalFunctionCredit": 0})
    report = {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM,
              "associations": rows, "classification": "Historical-origin annotations on already credited C symbols",
              "additionalSourceByteCredit": 0, "additionalFunctionCredit": 0,
              "limitations": ["C reconstruction is proven by the referenced full native byte/relocation matches",
                              "Historical origin remains uncertain; these annotations create no second region or coverage credit"]}
    (ROOT / "evidence/utility/c-tail-associations.json").write_text(json.dumps(report, indent=2) + "\n")
    print({"associations": len(rows), "additionalCredit": 0})


if __name__ == "__main__":
    main()
