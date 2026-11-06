import json
from pathlib import Path

from match_overlay_modules import ROOT, ROM_HASH, compile_compare, execute, immutable, sha


def main():
    proof_path = ROOT / "evidence/matches/overlays-ov007-ea42b8d28e09.json"
    proof = json.loads(proof_path.read_text())
    report, codes = compile_compare("ov007", ROOT / proof["source"])
    if report["sourceSha256"] != proof["sourceSha256"] or len(codes) != 14:
        raise ValueError("Frozen typed table source no longer reproduces all fourteen functions")
    native = (ROOT / "extract/arm9_overlays/ov007.bin").read_bytes()
    records = []
    for entry in report["functions"]:
        address = int(entry["address"], 16)
        count = 15 if address in {0x021D86DC, 0x021D86F4, 0x021D870C} else 16
        old = native[address - 0x021D7240:address - 0x021D7240 + entry["bytes"]]
        samples = []
        for index in range(count):
            values = [0, 1, 255, 256, 65535, 65536, 0xFFFFFFFF] if address in {0x021D8724, 0x021D8754} else [index]
            for sample, value in enumerate(values):
                args = {0: index}
                if address in {0x021D8724, 0x021D8754}:
                    args[1] = value
                vector = index * 7 + sample
                first = execute("ov007", address, old, entry, vector, args)
                second = execute("ov007", address, codes[entry["name"]], entry, vector, args)
                if first != second:
                    raise ValueError("Full table validation differs at " + entry["name"])
                samples.append({"index": index, "arguments": args, "stateSha256": sha(json.dumps(first, sort_keys=True).encode())})
        records.append({"name": entry["name"], "address": entry["address"], "sourceRowsTested": count, "vectors": len(samples), "executions": len(samples) * 2, "passed": True, "samples": samples})
    result = {"schemaVersion": 1, "romSha256": ROM_HASH, "module": "ov007", "originalProof": str(proof_path.relative_to(ROOT)), "originalProofSha256": sha(proof_path.read_bytes()), "source": report["source"], "sourceSha256": report["sourceSha256"], "object": report["object"], "objectSha256": report["objectSha256"], "functions": records, "passed": True, "observations": ["The sixteen 48-byte rows start at 0x021da5e8, including their leading ordinal words.", "Resource pointer triplets form a separate fifteen-row table.", "Original accepted source and proof remain immutable; this report extends the validated row range."]}
    raw = json.dumps(result, indent=2).encode()
    path = ROOT / "evidence/validation" / ("ov007-tables-16-" + sha(raw)[:12] + ".json")
    immutable(path, raw)
    print(json.dumps({"report": str(path.relative_to(ROOT)), "functions": len(records), "vectors": sum(x["vectors"] for x in records), "executions": sum(x["executions"] for x in records), "passed": True}, indent=2))


if __name__ == "__main__":
    main()
