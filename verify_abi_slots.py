import json
from pathlib import Path
from abi_slots import preserve_argument_slots
import match_arm7 as matcher

ROOT = Path(__file__).resolve().parent


def main():
    report = json.loads((ROOT / "evidence/matches/arm7-translated10.json").read_text())
    entry = next(entry for entry in report["matches"] if entry["address"] == "0x3803544")
    original = ROOT / entry["source"]
    text = original.read_text()
    if matcher.sha(original.read_bytes()) != entry["sourceSha256"]:
        raise ValueError("Accepted ABI adapter proof source changed")
    before_text = text.replace(entry["name"] + "(u32 arg0, ", entry["name"] + "(")
    after_text, slots = preserve_argument_slots(before_text, entry["name"])
    if after_text != text or slots != [0]:
        raise ValueError("ABI adapter did not recreate the accepted native register-slot signature")
    unsupported = "u32 sample(s64 arg1) { return 0; }"
    if preserve_argument_slots(unsupported, "sample") != (unsupported, []):
        raise ValueError("Multiword ABI parameters must remain outside the adapter scope")
    work = ROOT / "work/lowlevel-recovery/slot-proof"
    work.mkdir(parents=True, exist_ok=True)
    before_source, after_source = work / "before.c", work / "after.c"
    before_source.write_text(before_text)
    after_source.write_text(after_text)
    spec = matcher.accepted_spec(entry)
    compiler, digest = matcher.tools()[0]
    before, unexpected_match = matcher.compare(before_source, spec, compiler, digest, 2, "off")
    after, code = matcher.compare(after_source, spec, compiler, digest, 2, "off")
    if unexpected_match is not None or before["matchingBytes"] != 99 or code is None or len(code) != 100:
        raise ValueError("Native whole-function ABI adapter proof no longer holds")
    result = {"schemaVersion": 1, "processor": "arm7", "module": spec["module"], "address": hex(spec["address"]),
              "adapter": "abi_slots.py", "adapterSha256": matcher.sha((ROOT / "abi_slots.py").read_bytes()),
              "acceptedSource": entry["source"], "acceptedSourceSha256": entry["sourceSha256"],
              "addedUnusedArgumentSlots": slots, "before": before, "after": after,
              "reproduce": ["python", "verify_abi_slots.py"],
              "scope": "Single-word scalar or pointer parameters named argN; multiword, aggregate and function-pointer parameters remain unchanged",
              "limitations": ["Argument names must use the measured native register-slot decompiler convention",
                              "This proof covers one complete native 100-byte function; all further outputs still require full byte and relocation matching"]}
    (ROOT / "evidence/arm7/abi-slot-adapter.json").write_text(json.dumps(result, indent=2) + "\n")
    print({"exactNativeBytes": len(code), "beforeMatchingBytes": before["matchingBytes"], "addedUnusedSlots": slots})


if __name__ == "__main__":
    main()
