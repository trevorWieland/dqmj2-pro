import json
import os
import random
from pathlib import Path

import audit_overlay004 as audit
import dsprot128
import match_overlay_modules as matcher
import verify_overlay_report

ROOT = Path(__file__).resolve().parent
PROOF = "evidence/matches/overlays-ov004-34a4df168881.json"


def main():
    replay = verify_overlay_report.verify(PROOF)
    proof = json.loads((ROOT / PROOF).read_text())
    source = ROOT / proof["source"]
    report, codes = matcher.compile_compare("ov004", source, "2", "off")
    expected = {entry["name"]: entry for entry in proof["matches"]}
    if report["sourceSha256"] != proof["sourceSha256"] or len(report["functions"]) != 3:
        raise ValueError("Frozen source content/inventory differs")
    data = audit.inputs()
    rebuilt = bytearray(data["analysis"])
    for entry in report["functions"]:
        original = expected[entry["name"]]
        if any(
            entry[field] != original[field]
            for field in [
                "address",
                "size",
                "outputSha256",
                "targetSha256",
                "compilerSha256",
            ]
        ):
            raise ValueError("Source-compiled target/span/compiler differs")
        if not entry["exactBytes"] or entry["relocations"]:
            raise ValueError(
                "Expected exact ordinary leaf functions without relocations"
            )
        address = int(entry["address"], 16)
        offset = address - audit.BASE
        rebuilt[offset : offset + entry["size"]] = codes[entry["name"]]
    encrypted = dsprot128.image_transform(
        bytes(rebuilt), data["functions"], audit.BASE, True
    )
    if encrypted != data["decoded"]:
        raise ValueError(
            "Source-compiled analysis then encrypted image differs from cold native image"
        )
    runs = []
    for seed in [4, 0x128, 0xAA65, 0xA99F]:
        variant = dict(data, decoded=encrypted)
        runs.append(audit.runtime(variant, seed))
    classification = []
    for label, image in [
        ("original", data["analysis"]),
        ("sourceCompiled", bytes(rebuilt)),
    ]:
        machine = audit.Machine(image, data["entry"][3], 0x0047DE8)
        randomizer = random.Random(0x128)
        cases = 0
        for opcode in range(256):
            for low in [
                0,
                0xFFFFFF,
                1,
                0x800000,
                *[randomizer.randrange(0x1000000) for _ in range(4)],
            ]:
                instruction = (opcode << 24) | low
                expected_kind = 0
                if opcode & 14 == 10:
                    expected_kind = 1 if opcode & 240 == 240 else 2 if opcode & 1 else 3
                result = machine.call(0x021D7DE8, arguments=(instruction,))
                if result["result"] != expected_kind:
                    raise ValueError(
                        "Opcode classification disagrees with independent category oracle"
                    )
                cases += 1
        classification.append(
            {
                "view": label,
                "vectors": cases,
                "instructions": machine.steps,
                "writes": len(machine.writes),
            }
        )
    result = {
        "schemaVersion": 1,
        "date": "2026-10-27",
        "kind": "ordinary-c-through-native-dsprotect-boot-and-keyed-wrappers",
        "romSha256": audit.ROM_HASH,
        "module": "ov004",
        "source": Path(__file__).name,
        "sourceSha256": audit.sha(Path(__file__).read_bytes()),
        "runtimeAuditSourceSha256": audit.sha(
            (ROOT / "audit_overlay004.py").read_bytes()
        ),
        "transformSourceSha256": audit.sha((ROOT / "dsprot128.py").read_bytes()),
        "frozenC": proof["source"],
        "frozenCSha256": proof["sourceSha256"],
        "proof": PROOF,
        "functions": 3,
        "sourceBytes": 84,
        "protectedOrdinaryLeafFunctions": 2,
        "plainRuntimeClassifierFunctions": 1,
        "recompiledSourceThenEncryptedEqualsOriginalColdImage": True,
        "nativeBootAndKeyedWrapperRuns": runs,
        "classification": classification,
        "classificationVectors": sum(item["vectors"] for item in classification),
        "nativeBootAndKeyedWrapperInstructions": sum(
            item["totalInstructions"] for item in runs
        ),
        "sourceReplayer": {
            key: replay[key]
            for key in [
                "functions",
                "bytes",
                "oracleExecutions",
                "sourceSha256",
                "frozenProofPreserved",
            ]
        },
        "substitutedNativeCallees": 0,
        "protectedCiphertextCreditedAsSource": False,
        "limitations": [
            "The complete module still contains original native protection templates and unrecovered functions; only the three proven ordinary C spans receive source credit."
        ],
        "passed": True,
    }
    raw = json.dumps(result, indent=2).encode()
    directory = ROOT / "evidence/validation"
    target = directory / ("overlay004-source-runtime-" + audit.sha(raw)[:12] + ".json")
    if target.exists() and target.read_bytes() != raw:
        raise ValueError("Immutable source runtime report collision")
    target.write_bytes(raw)
    temporary = directory / "overlay004-source-runtime.json.tmp"
    temporary.write_bytes(raw)
    os.replace(temporary, directory / "overlay004-source-runtime.json")
    print(
        json.dumps(
            {
                "report": str(target.relative_to(ROOT)),
                "functions": 3,
                "sourceBytes": 84,
                "classificationVectors": result["classificationVectors"],
                "nativeBootAndKeyedWrapperInstructions": result[
                    "nativeBootAndKeyedWrapperInstructions"
                ],
                "passed": True,
            }
        )
    )


if __name__ == "__main__":
    main()
