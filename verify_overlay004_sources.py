import json
import os
import random
from pathlib import Path

import audit_overlay004 as audit
import dsprot128
import match_overlay_modules as matcher
import overlay_oracle004
import overlay_oracle004_guards
import overlay_oracle004_platform
import overlay004_baseline_source
import verify_overlay_report

ROOT = Path(__file__).resolve().parent
PROOFS = [
    "evidence/matches/overlays-ov004-34a4df168881.json",
    "evidence/matches/overlays-ov004-268baadf1de0.json",
    "evidence/matches/overlays-ov004-cd0d2a29abe4.json",
    "evidence/matches/overlays-ov004-bee2293789e7.json",
    "evidence/matches/overlays-ov004-6e0b89d105db.json",
    "evidence/matches/overlays-ov004-d3263cdce4b0.json",
    "evidence/matches/overlays-ov004-227612f24e11.json",
    "evidence/matches/overlays-ov004-da6de73ea12b.json",
    "evidence/matches/overlays-ov004-6a712934cc15.json",
    "evidence/matches/overlays-ov004-b19e28630aef.json",
    "evidence/matches/overlays-ov004-6b2e120236d4.json",
]
DATA_PROOF = "evidence/data/overlays-ov004-1e819dc4f7db.json"


class Machine(audit.Machine):
    def step(self, engine, address, size, user):
        super().step(engine, address, size, user)
        if address == self.observe_target:
            self.entry_snapshot = bytes(engine.mem_read(address, self.observed_size))


class PlatformMachine(overlay_oracle004_platform.Machine, Machine):
    pass


def compile_sources(data):
    rebuilt = bytearray(data["analysis"])
    inventory = {}
    sources = []
    for path in PROOFS:
        replay = verify_overlay_report.verify(path)
        frozen = json.loads((ROOT / path).read_text())
        sample = frozen["matches"][0]
        flags = sample["compilerFlags"]
        matcher.COMPILER = ROOT / sample["compiler"]
        optimization = next(flag[2:] for flag in flags if flag.startswith("-O"))
        inline = verify_overlay_report.option(flags, "-inline")
        report, codes = matcher.compile_compare(
            "ov004", ROOT / frozen["source"], optimization, inline
        )
        originals = {entry["name"]: entry for entry in frozen["matches"]}
        if set(codes) != set(originals) or report["flags"] != flags:
            raise ValueError("Frozen compiled source inventory/flags differ")
        for entry in report["functions"]:
            original = originals[entry["name"]]
            for field in [
                "address",
                "size",
                "outputSha256",
                "targetSha256",
                "sourceSha256",
                "compilerSha256",
                "relocations",
            ]:
                if entry[field] != original[field]:
                    raise ValueError(
                        "Frozen source/span/relocation proof differs: " + field
                    )
            if not entry["exactAfterDeclaredRelocation"]:
                raise ValueError(
                    "Source function does not match its complete native span"
                )
            address = int(entry["address"], 16)
            if address in inventory:
                raise ValueError("Duplicate source function")
            inventory[address] = dict(
                entry,
                sourceLanguage=original.get("sourceLanguage", "c"),
                ordinaryCBytes=original.get("ordinaryCBytes", entry["size"]),
                justifiedAssemblyBytes=original.get("justifiedAssemblyBytes", 0),
            )
            offset = address - audit.BASE
            rebuilt[offset : offset + entry["size"]] = codes[entry["name"]]
        sources.append(
            {
                "proof": path,
                "source": frozen["source"],
                "sourceSha256": frozen["sourceSha256"],
                "compiler": sample["compiler"],
                "compilerSha256": sample["compilerSha256"],
                "flags": flags,
                "functions": replay["functions"],
                "bytes": replay["bytes"],
                "oracleExecutions": replay["oracleExecutions"],
                "sourceLanguage": frozen.get("sourceLanguage", "c"),
                "ordinaryCBytes": frozen.get("ordinaryCBytes", replay["bytes"]),
                "justifiedAssemblyBytes": frozen.get("justifiedAssemblyBytes", 0),
            }
        )
    return bytes(rebuilt), inventory, sources


def crc_value(data):
    result = 0xFFFFFFFF
    for byte in data:
        result ^= byte
        for _ in range(8):
            result = (result >> 1) ^ (((result & 1) ^ 1) * 0xEDB88320)
    return (~result) & 0xFFFFFFFF


def compile_data(data, analysis):
    frozen = json.loads((ROOT / DATA_PROOF).read_text())
    source = ROOT / frozen["source"]
    if audit.sha(source.read_bytes()) != frozen["sourceSha256"]:
        raise ValueError("Frozen data C source differs")
    matcher.COMPILER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
    report, codes = matcher.compile_compare("ov004", source, "2", "off")
    if (
        report["returncode"]
        or codes
        or report["flags"] != frozen["flags"]
        or report["compilerSha256"] != frozen["compilerSha256"]
    ):
        raise ValueError("Frozen typed data compiler/inventory differs")
    rebuilt = bytearray(analysis)
    bss = 0
    initialized = 0
    with (ROOT / report["object"]).open("rb") as stream:
        elf = matcher.ELFFile(stream)
        symbols = elf.get_section_by_name(".symtab")
        for expected in frozen["dataMatches"]:
            symbol = symbols.get_symbol_by_name(expected["name"])[0]
            if symbol["st_size"] != expected["size"]:
                raise ValueError("Typed data allocation extent differs")
            section = (
                elf.get_section(symbol["st_shndx"])
                if isinstance(symbol["st_shndx"], int)
                else None
            )
            if expected["kind"] == "bss":
                if section is not None and section["sh_type"] != "SHT_NOBITS":
                    raise ValueError("Typed BSS unexpectedly initializes file bytes")
                bss += expected["size"]
                continue
            start = symbol["st_value"]
            raw = section.data()[start : start + expected["size"]]
            if audit.sha(raw) != expected["targetSha256"]:
                raise ValueError("Typed configuration target differs")
            offset = int(expected["address"], 16) - audit.BASE
            rebuilt[offset : offset + expected["size"]] = raw
            initialized += len(raw)
    if bss != data["entry"][3]:
        raise ValueError("Typed BSS differs from measured native runtime zero storage")
    return bytes(rebuilt), {
        "proof": DATA_PROOF,
        "source": frozen["source"],
        "sourceSha256": frozen["sourceSha256"],
        "initializedBytes": initialized,
        "bssBytes": bss,
        "unreferencedDataBytesCredited": 0,
    }


def wrapped_runtime(data, image, inventory, seed):
    firmware, valid = overlay_oracle004_platform.fixture(data, [0, 1, 56, 58][seed])
    machine = PlatformMachine(image, data["entry"][3], seed, firmware)
    constructors = [
        machine.call(pointer) for pointer in data["constructors"] if pointer
    ]
    targets = [
        (0x021D7CC4, 0x021D7854, 0xAA65),
        (0x021D7D00, 0x021D7970, 0xB177),
        (0x021D7D3C, 0x021D7A8C, 0xAA65),
        (0x021D7D78, 0x021D7BA8, 0xB177),
        (0x021D83D4, 0x021D8340, None),
        (0x021D82C8, 0x021D8168, (251 if valid else 241) * 197),
        (0x021D8304, 0x021D8218, (241 if valid else 251) * 193),
    ]
    randomizer = random.Random(seed)
    results = []
    for wrapper, target, expected in targets:
        spec = next(item for item in data["functions"] if item["address"] == target)
        span = inventory[target]["size"]
        offset = target - audit.BASE
        machine.observed_size = span
        for iteration in range(2):
            arguments = ()
            if expected is None:
                count = [0, 1, 7, 128][seed % 4]
                buffer = randomizer.randbytes(count)
                machine.engine.mem_write(audit.STACK + 0x4000, buffer)
                arguments = (audit.STACK + 0x4000, count)
                expected_result = crc_value(buffer)
            else:
                expected_result = expected
            result = machine.call(wrapper, target, arguments)
            after = machine.image()[offset : offset + span]
            if (
                result["result"] != expected_result
                or machine.entry_snapshot != data["analysis"][offset : offset + span]
            ):
                raise ValueError(
                    "Full source-compiled keyed span/model result differs at runtime entry"
                )
            prefix = spec["codeBytes"]
            if (
                after[:prefix] == data["analysis"][offset : offset + prefix]
                or after[prefix:] != data["analysis"][offset + prefix : offset + span]
            ):
                raise ValueError(
                    "Native post-return instruction re-encryption or literal preservation differs"
                )
            results.append(
                {
                    **result,
                    "target": hex(target),
                    "iteration": iteration,
                    "observedFullFunctionBytes": span,
                    "entryFullSpanEqualsSourceCompiledAnalysis": True,
                    "instructionPrefixReencryptedAfterReturn": True,
                    "poolUnchanged": True,
                    "independentResultExact": True,
                }
            )
    return {
        "seed": seed,
        "constructors": constructors,
        "keyedCalls": results,
        "instructions": machine.steps,
        "writes": len(machine.writes),
        "substitutedNativeCallees": 0,
        "finalImageSha256": audit.sha(machine.image()),
    }


def guarded_runtime(data, image, inventory, seed):
    firmware, valid = overlay_oracle004_platform.fixture(data, [0, 1, 56, 58][seed])
    machine = PlatformMachine(image, data["entry"][3], seed, firmware)
    for pointer in data["constructors"]:
        if pointer:
            machine.call(pointer)
    cases = [
        (0x021D76A4, 0x021D7304, 0x021D8890, [0xAA65, 0xAA65]),
        (0x021D76E0, 0x021D73A4, 0x021D88CC, [0xB177, 0xB177]),
        (0x021D7794, 0x021D7584, None, [0xAA65]),
        (0x021D77D0, 0x021D7614, None, [0xA99F]),
        (0x021D771C, 0x021D7444, None, [(251 if valid else 241) * 197, 0xAA65]),
        (0x021D7758, 0x021D74E4, None, [(241 if valid else 251) * 193, 0xB177]),
    ]
    results = []
    for wrapper, target, inspected, canonical in cases:
        spec = next(item for item in data["functions"] if item["address"] == target)
        offset = target - audit.BASE
        span = inventory[target]["size"]
        machine.observed_size = span
        for iteration in range(2):
            argument = ([0xEA, 0xEB, 0xFA, 0xE1][seed] << 24) | 0x123456
            values = canonical
            if inspected is not None:
                signature = bytearray.fromhex("0fc08fe10cc01ce000c0a0031cc08c12")
                if iteration:
                    signature[seed] ^= 1
                    values = [0xB177 if value == 0xAA65 else 0xAA65 for value in values]
                machine.engine.mem_write(inspected, bytes(signature))
            total = (0x30EB87 + sum(values)) & 0xFFFFFFFF
            prime, call_when_zero = overlay_oracle004_guards.GUARDS[target][2:]
            taken = (total % prime == 0) == call_when_zero
            expected = overlay_oracle004_guards.classify(argument) if taken else total
            result = machine.call(wrapper, target, (0x021D7DE8, argument))
            after = machine.image()[offset : offset + span]
            prefix = spec["codeBytes"]
            if (
                result["result"] != expected
                or machine.entry_snapshot != data["analysis"][offset : offset + span]
            ):
                raise ValueError(
                    "Nested real guard/integrity/constant/native callback chain differs"
                )
            if (
                after[:prefix] == data["analysis"][offset : offset + prefix]
                or after[prefix:] != data["analysis"][offset + prefix : offset + span]
            ):
                raise ValueError(
                    "Outer native guard encryption/pool preservation differs"
                )
            results.append(
                {
                    **result,
                    "target": hex(target),
                    "iteration": iteration,
                    "signatureMismatchInjected": inspected is not None
                    and iteration == 1,
                    "callbackTakenByIndependentModel": taken,
                    "entryFullSpanEqualsSourceCompiledAnalysis": True,
                    "instructionPrefixReencryptedAfterReturn": True,
                    "poolUnchanged": True,
                }
            )
    return {
        "seed": seed,
        "calls": results,
        "instructions": machine.steps,
        "substitutedNativeCallees": 0,
        "platformFixtureValidByIndependentModel": valid,
        "executedNativeSdkHelpers": [
            hex(address) for address in sorted(machine.executed_helpers)
        ],
        "limitation": "Platform-backed paths read synthetic private firmware buffers through actual native SDK helpers; physical device behavior is not claimed.",
    }


def main():
    data = audit.inputs()
    analysis, inventory, sources = compile_sources(data)
    analysis, baseline = overlay004_baseline_source.merge(data, analysis, inventory)
    sources.append(baseline)
    analysis, data_source = compile_data(data, analysis)
    encrypted = dsprot128.image_transform(analysis, data["functions"], audit.BASE, True)
    if analysis != data["analysis"] or encrypted != data["decoded"]:
        raise ValueError(
            "Whole source-substituted image/encrypted cold representation differs"
        )
    basics = [audit.runtime(dict(data, decoded=encrypted), seed) for seed in range(4)]
    wrapped = [wrapped_runtime(data, encrypted, inventory, seed) for seed in range(4)]
    guards = [guarded_runtime(data, encrypted, inventory, seed) for seed in range(4)]
    report = {
        "schemaVersion": 1,
        "date": "2026-10-27",
        "kind": "all-accepted-overlay004-ordinary-c-through-native-protection-runtime",
        "romSha256": audit.ROM_HASH,
        "module": "ov004",
        "source": Path(__file__).name,
        "sourceSha256": audit.sha(Path(__file__).read_bytes()),
        "dependencies": {
            path: audit.sha((ROOT / path).read_bytes())
            for path in [
                "audit_overlay004.py",
                "dsprot128.py",
                "overlay_oracle004.py",
                "overlay_oracle004_guards.py",
                "overlay_oracle004_platform.py",
                "overlay_oracle004_bridge.py",
                "overlay004_baseline_source.py",
            ]
        },
        "sources": sources,
        "dataSources": [data_source],
        "sourceFunctions": len(inventory),
        "sourceBytes": sum(entry["size"] for entry in inventory.values()),
        "ordinaryCBytes": sum(entry["ordinaryCBytes"] for entry in inventory.values()),
        "justifiedAssemblyBytes": sum(
            entry["justifiedAssemblyBytes"] for entry in inventory.values()
        ),
        "sourceThenEncryptedWholeImageExact": True,
        "basicsRuntime": basics,
        "signatureAndCrcRuntime": wrapped,
        "nestedGuardRuntime": guards,
        "totalRuntimeInstructions": sum(item["totalInstructions"] for item in basics)
        + sum(item["instructions"] for item in wrapped)
        + sum(item["instructions"] for item in guards),
        "substitutedNativeCallees": 0,
        "protectedCiphertextCreditedAsSource": False,
        "ordinarySignatureReaderQualification": "Four ordinary C routines inspect the sixteen-byte signature of their native protection wrappers. Their comparisons and address arithmetic are source recovered; the inspected wrapper instructions remain unrecovered native code and receive no C credit.",
        "limitations": [
            "Bounded isolated native protection execution plus independent function models; full hardware execution and complete source recovery are not claimed."
        ],
        "passed": True,
    }
    raw = json.dumps(report, indent=2).encode()
    folder = ROOT / "evidence/validation"
    target = folder / ("overlay004-all-source-runtime-" + audit.sha(raw)[:12] + ".json")
    if target.exists() and target.read_bytes() != raw:
        raise ValueError("Immutable source runtime proof collision")
    target.write_bytes(raw)
    temporary = folder / "overlay004-all-source-runtime.json.tmp"
    temporary.write_bytes(raw)
    os.replace(temporary, folder / "overlay004-all-source-runtime.json")
    print(
        json.dumps(
            {
                "report": str(target.relative_to(ROOT)),
                "sourceFunctions": len(inventory),
                "sourceBytes": report["sourceBytes"],
                "runtimeInstructions": report["totalRuntimeInstructions"],
                "passed": True,
            }
        )
    )


if __name__ == "__main__":
    main()
