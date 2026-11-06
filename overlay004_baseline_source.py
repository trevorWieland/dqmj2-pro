import json

import audit_overlay004 as audit
import match_overlay_modules as matcher


def merge(data, image, inventory):
    root = audit.ROOT
    frozen = json.loads((root / "evidence/matches/overlay004.json").read_text())
    source = root / frozen["source"]
    if audit.sha(source.read_bytes()) != frozen["sourceSha256"]:
        raise ValueError("Original frozen three-function source differs")
    matcher.COMPILER = root / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
    report, codes = matcher.compile_compare("ov004", source, "2", "noauto")
    if report["flags"] != frozen["compilerFlags"] or len(report["functions"]) != 3:
        raise ValueError("Original source compiler flags/inventory differ")
    rebuilt = bytearray(image)
    for entry in report["functions"]:
        if not entry["exactAfterDeclaredRelocation"]:
            raise ValueError(
                "Original source function no longer matches all native bytes"
            )
        address = int(entry["address"], 16)
        if address in inventory:
            raise ValueError("Original source duplicates a recovered source span")
        inventory[address] = dict(
            entry,
            sourceLanguage="c",
            ordinaryCBytes=entry["size"],
            justifiedAssemblyBytes=0,
        )
        offset = address - audit.BASE
        rebuilt[offset : offset + entry["size"]] = codes[entry["name"]]
    executions = 0
    for vector in range(48):
        callback = [0, 0x021D7258, 0x021D7300][vector % 3]
        states = []
        for candidate in [data["analysis"], bytes(rebuilt)]:
            machine = audit.Machine(candidate, data["entry"][3], vector)
            result = machine.call(0x021D7240, arguments=(callback,))
            if result["result"] != ((~callback) & 0xFFFFFFFF):
                raise ValueError("Original callback-address complement model differs")
            states.append(
                (
                    result,
                    machine.writes,
                    audit.sha(bytes(machine.engine.mem_read(audit.STACK, 0x10000))),
                )
            )
            executions += 1
        if states[0] != states[1]:
            raise ValueError("Original native/C callback path state differs")
    return bytes(rebuilt), {
        "proof": "evidence/matches/overlay004.json",
        "source": frozen["source"],
        "sourceSha256": frozen["sourceSha256"],
        "compiler": report["compiler"],
        "compilerSha256": report["compilerSha256"],
        "flags": report["flags"],
        "functions": 3,
        "bytes": 32,
        "ordinaryCBytes": 32,
        "justifiedAssemblyBytes": 0,
        "sourceLanguage": "c",
        "oracleExecutions": executions,
    }
