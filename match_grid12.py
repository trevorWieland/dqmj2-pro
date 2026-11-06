import json
import random
import struct
import match_runtime as matcher
from project import ROOT, configuration, now, read_json, sha256, verify_inputs, write_json


def validate(entry, code, native):
    rng = random.Random(20261027004)
    values = sorted(set(list(range(-20, 33)) + [-0x80000000, -0x7FFFFFFF, 0x7FFFFFFE, 0x7FFFFFFF] + [rng.getrandbits(32) for unused in range(256)]))
    digests = []
    null_guards = 0
    for raw in values:
        signed = (raw & 0x7FFFFFFF) - (raw & 0x80000000)
        valid = 0 <= signed < 12
        locations = [(0, 0), (0, 4), (4, 0), (4, 4), (0, 12), (12, 0)]
        if not valid:
            locations.append((None, None))
        for first, second in locations:
            address = 0x03002000
            initial = rng.randbytes(64)
            expected = bytearray(initial)
            x = address + first if first is not None else 0
            y = address + second if second is not None else 0
            writes = []
            if valid:
                horizontal = signed % 4 * 40 + 48
                vertical = (signed // 4 + 1) * 40
                struct.pack_into("<I", expected, first, horizontal)
                struct.pack_into("<I", expected, second, vertical)
                writes = [[x, 4, horizontal], [y, 4, vertical]]
            registers = [rng.getrandbits(32) for unused in matcher.REGISTERS]
            registers[:3] = [raw & 0xFFFFFFFF, x, y]
            registers[-2:] = [0x0301FFF0, 0x04000000]
            memory = {address: initial, 0x0301F000: bytes(4096)}
            flags = rng.getrandbits(4) << 28 | 0x10
            original = matcher.execute(native, int(entry["address"], 0), registers, memory, flags)
            rebuilt = matcher.execute(code, int(entry["address"], 0), registers, memory, flags)
            if original != rebuilt or original["registers"][0] != int(valid) or original["memory"][0] != matcher.sha(expected):
                raise ValueError("Native/source coordinates, guard or complete memory differ")
            effects = [row for row in original["writes"] if address <= row[0] < address + len(initial)]
            if effects != writes or original["registers"][4:12] != registers[4:12] or original["registers"][-2] != registers[-2]:
                raise ValueError("Native write order or ABI preservation differs")
            null_guards += int(first is None)
            digests.append(matcher.sha(json.dumps(original, sort_keys=True).encode()))
    return {"vectors": len(digests), "nativeAndRecompiledCalls": 2 * len(digests), "inputIndexPatterns": len(values), "nullOutputGuards": null_guards, "validPositions": 12, "alignedPointerAliases": 6, "externalCalls": 0, "actualReturnRequired": True, "instructionLimit": 2000, "stateSha256": digests, "independentExpectedBehavior": "For signed index0..11, x=(index modulo4)*40+48 and y=(floor(index/4)+1)*40, return1; otherwise return0 without output writes", "limitations": ["Valid indices require aligned writable output pointers; arbitrary malformed pointers are not supported", "The native caller and game-level role of the coordinate pattern remain unidentified"]}


def main():
    config = configuration()
    inputs = verify_inputs(config)
    source = ROOT / "src/runtime/grid12/grid12.c"
    path = ROOT / "evidence/matches/main-grid12.json"
    rows, matches = matcher.compare(source, "main", 2, "off")
    if set(matches) != {"native_main_020cfa78"}:
        raise ValueError("Frozen coordinate helper no longer matches")
    entry, code = matches["native_main_020cfa78"]
    if entry["bytes"] != 88 or entry["relocations"]:
        raise ValueError("Coordinate helper extent or dependency inventory changed")
    if path.exists():
        previous = read_json(path)["matches"][0]
        for field in ("sourceSha256", "address", "bytes", "mode", "targetSha256", "outputSha256"):
            if previous[field] != entry[field]:
                raise ValueError("Accepted coordinate helper identity changed")
    binary = (ROOT / "extract/arm9/arm9.bin").read_bytes()
    entry["oracle"] = validate(entry, code, binary[0xCFA78:0xCFAD0])
    report = {"schemaVersion": 1, "createdUtc": now(), "romSha256": inputs["rom"]["sha256"], "module": "main", "moduleInputSha256": matcher.sha(binary), "matches": [entry], "nativeSymbols": {}, "semanticNameEvidence": "Coordinate formula measured; game-level purpose unassigned", "wholeModuleLinked": False, "sourceReconstructionComplete": False}
    if inputs != verify_inputs(config):
        raise ValueError("Input identities changed")
    write_json(path, report)
    print({"functions": 1, "bytes": 88, "vectors": entry["oracle"]["vectors"], "nativeAndRecompiledCalls": entry["oracle"]["nativeAndRecompiledCalls"]})


if __name__ == "__main__":
    main()
