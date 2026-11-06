import argparse
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMAGE_HASH = "9f40087972ccb8b89d4cc4baf8288123e26a479bb43fa68b18a30a59650633a1"
BASE = 0x02380000
OUT = ROOT / "extract/arm7/runtime"
MANIFEST = ROOT / "evidence/arm7/runtime-layout.json"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def word(image, address):
    offset = address - BASE
    if not 0 <= offset <= len(image) - 4:
        raise ValueError("ARM7 boot pointer is outside the measured input image")
    return struct.unpack_from("<I", image, offset)[0]


def literal(image, offset, register):
    instruction = struct.unpack_from("<I", image, offset)[0]
    if instruction & 0x0F7F0000 != 0x051F0000 or (instruction >> 12) & 15 != register:
        raise ValueError("Expected ARM7 PC-relative literal load is absent")
    displacement = instruction & 0xFFF
    location = BASE + offset + 8 + (displacement if instruction & 0x800000 else -displacement)
    value = word(image, location)
    return value, {"instructionAddress": hex(BASE + offset), "instructionWord": hex(instruction),
                   "register": f"r{register}", "literalAddress": hex(location), "value": hex(value)}


def derive(image):
    if len(image) != 160048 or sha(image) != IMAGE_HASH:
        raise ValueError("ARM7 image differs from measured build")
    parameter_address, parameter_trace = literal(image, 0x118, 0)
    descriptor_start, descriptor_end, initialized_source = (word(image, parameter_address + index * 4) for index in range(3))
    bss_start, bss_end = (word(image, parameter_address + index * 4) for index in (3, 4))
    if descriptor_end - descriptor_start != 24 or descriptor_end - BASE != len(image):
        raise ValueError("ARM7 composition table no longer has two final descriptors")
    handoff, handoff_trace = literal(image, 0xD8, 1)
    return_address, return_trace = literal(image, 0xDC, 14)
    if word(image, BASE + 0xE0) != 0xE12FFF11:
        raise ValueError("ARM7 boot no longer transfers control with BX r1")
    boot_bytes = initialized_source - BASE
    modules = [{"id": "arm7-boot", "name": "arm7-boot", "processor": "arm7", "architecture": "ARMv4T",
                "inputFileOffset": 0, "inputBytes": boot_bytes, "runtimeBase": hex(BASE), "base": hex(BASE),
                "runtimeEntry": hex(BASE), "entryMode": "arm", "bssStart": hex(bss_start), "bssBytes": bss_end - bss_start,
                "entryEvidence": "NDS ARM7 header entry and native boot instructions"}]
    cursor = boot_bytes
    composition = []
    for index in range(2):
        address = descriptor_start + 12 * index
        runtime, size, zero_fill = (word(image, address + field * 4) for field in range(3))
        if runtime not in (0x037F8000, 0x027E0000) or size & 3 or zero_fill & 3:
            raise ValueError("ARM7 autoload descriptor differs from validated runtime mapping")
        name = "arm7-wram" if runtime == 0x037F8000 else "arm7-main"
        entry = handoff if runtime <= handoff < runtime + size else None
        row = {"id": name, "name": name, "processor": "arm7", "architecture": "ARMv4T",
               "inputFileOffset": cursor, "inputBytes": size, "runtimeBase": hex(runtime), "base": hex(runtime),
               "runtimeEntry": hex(entry) if entry is not None else None, "entryMode": "arm" if entry is not None else None,
               "bssStart": hex(runtime + size), "bssBytes": zero_fill,
               "entryEvidence": "Native boot BX r1 handoff" if entry is not None else "No independent image entry; recover actual cross-module call targets",
               "descriptorAddress": hex(address), "descriptorFileOffset": address - BASE}
        modules.append(row)
        composition.append({"descriptorIndex": index, "descriptorAddress": hex(address), "descriptorFileOffset": address - BASE,
                            "module": name, "sourceImageAddress": hex(BASE + cursor), "runtimeAddress": hex(runtime),
                            "initializedBytes": size, "zeroFillBytes": zero_fill})
        cursor += size
    if cursor != descriptor_start - BASE:
        raise ValueError("ARM7 initialized ranges do not exactly reach the composition table")
    for module in modules:
        begin, size = module["inputFileOffset"], module["inputBytes"]
        module["binary"] = f"extract/arm7/runtime/{module['id']}.bin"
        module["sha256"] = sha(image[begin:begin + size])
        module["bytes"] = size
        module["runtimeEnd"] = hex(int(module["runtimeBase"], 0) + size)
        module["bssEnd"] = hex(int(module["bssStart"], 0) + module["bssBytes"])
    return {"schemaVersion": 1, "processor": "arm7", "image": "extract/arm7/arm7.bin", "imageSha256": IMAGE_HASH,
            "imageBytes": len(image), "imageLoadAddress": hex(BASE), "modules": modules,
            "parameterBlockAddress": hex(parameter_address), "parameterBlockFileOffset": parameter_address - BASE,
            "compositionTableAddress": hex(descriptor_start), "compositionTableFileOffset": descriptor_start - BASE,
            "compositionTableBytes": descriptor_end - descriptor_start,
            "compositionTableSha256": sha(image[descriptor_start - BASE:descriptor_end - BASE]),
            "composition": composition, "nativeTrace": [parameter_trace, handoff_trace, return_trace],
            "bootHandoffAddress": hex(handoff), "bootHandoffReturnAddress": hex(return_address),
            "rawLinearFunctionInventoryCanonical": False, "sourceReconstructionComplete": False,
            "limitations": ["Only module loading, initialized byte extents and zero-fill allocations are established",
                            "All function boundaries, modes and types still require runtime-module analysis",
                            "ARM7 runtime 0x027e0000 and ARM9 DTCM share numeric addresses but belong to different processor address spaces"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    image = (ROOT / "extract/arm7/arm7.bin").read_bytes()
    manifest = derive(image)
    if args.verify:
        previous = json.loads(MANIFEST.read_text())
        if previous != manifest:
            raise ValueError("Canonical ARM7 runtime manifest changed")
        for module in manifest["modules"]:
            if sha((ROOT / module["binary"]).read_bytes()) != module["sha256"]:
                raise ValueError("Canonical ARM7 initialized bytes changed: " + module["id"])
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        for module in manifest["modules"]:
            start = module["inputFileOffset"]
            (ROOT / module["binary"]).write_bytes(image[start:start + module["inputBytes"]])
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print({"verified": args.verify, "modules": [{key: module[key] for key in ("id", "inputFileOffset", "inputBytes", "runtimeBase", "bssBytes", "runtimeEntry")} for module in manifest["modules"]], "compositionTableBytes": manifest["compositionTableBytes"]})


if __name__ == "__main__":
    main()
