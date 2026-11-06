import argparse
import json
import struct
import sys
from pathlib import Path
import audit_regions

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "deps/native"))
from ndspy import _common, code, codeCompression, fnt, lz10, rom

PROGRAM = "dwc/utility.bin/move/child.srl"
INPUT = ROOT / "extract/files/dwc/utility.bin"
INPUT_HASH = "db8ee36170897f60791f713b7669c50a125e62c6ad775fda98466c85fe48e81e"
OUTPUT = ROOT / "evidence/utility/runtime-layout.json"


def sha(data):
    return audit_regions.sha(data)


def archive_members(data):
    first, length, table, table_bytes = struct.unpack_from("<4I", data)
    if first != 16 or first + length > table or table + table_bytes > len(data) or table_bytes % 8:
        raise ValueError("Invalid utility FNT/FAT header")
    names = fnt.load(data[first:first + length])
    entries, intervals = [], [(0, 16), (first, first + length), (table, table + table_bytes)]
    for index in range(table_bytes // 8):
        start, end = struct.unpack_from("<II", data, table + index * 8)
        name = names.filenameOf(index)
        if name is None or start < table + table_bytes or not start <= end <= len(data):
            raise ValueError("Invalid utility member name or extent")
        member = data[start:end]
        entry = {"id": index, "path": name, "offset": start, "bytes": len(member), "sha256": sha(member), "magicHex": member[:4].hex()}
        if name.endswith(".l"):
            if member[:1] != b"\x10" or int.from_bytes(member[1:4], "little") > 16 * 1024 * 1024:
                raise ValueError("Utility .l member is not a bounded LZ10 stream")
            decoded = lz10.decompress(member)
            entry.update(transformation="Nintendo LZ10", decodedBytes=len(decoded), decodedSha256=sha(decoded), decodedMagicHex=decoded[:4].hex())
        entries.append(entry)
        intervals.append((start, end))
    gaps, cursor = [], 0
    for start, end in sorted(intervals):
        if start < cursor:
            raise ValueError("Utility named or directory extents overlap")
        if start > cursor:
            gap = data[cursor:start]
            if len(set(gap)) != 1 or gap[0] not in (0, 255):
                raise ValueError("Utility unclaimed bytes require classification")
            gaps.append({"offset": cursor, "bytes": len(gap), "fill": gap[0], "sha256": sha(gap)})
        cursor = end
    if cursor < len(data):
        gap = data[cursor:]
        if len(set(gap)) != 1 or gap[0] not in (0, 255):
            raise ValueError("Utility tail requires classification")
        gaps.append({"offset": cursor, "bytes": len(gap), "fill": gap[0], "sha256": sha(gap)})
    return {"header": {"fntOffset": first, "fntBytes": length, "fntSha256": sha(data[first:first + length]),
                       "fatOffset": table, "fatBytes": table_bytes, "fatSha256": sha(data[table:table + table_bytes])},
            "members": entries, "padding": gaps, "physicalBytesFullyPartitioned": True}


def literal(data, base, offset, register):
    word = struct.unpack_from("<I", data, offset)[0]
    if word & 0xFFFFF000 != 0xE59F0000 | register << 12:
        raise ValueError("Utility loader PC-relative LDR changed")
    target = offset + 8 + (word & 0xFFF)
    value = struct.unpack_from("<I", data, target)[0]
    return {"instructionAddress": hex(base + offset), "instructionWord": hex(word), "register": register,
            "literalAddress": hex(base + target), "value": hex(value)}


def physical_map(image, arm9):
    header_bytes = struct.unpack_from("<I", image, 0x84)[0]
    used = struct.unpack_from("<I", image, 0x80)[0]
    arm9_at, _, _, arm9_bytes, arm7_at, _, _, arm7_bytes = struct.unpack_from("<8I", image, 0x20)
    spans = [(0, 0x200, "fixed-header"), (0x200, header_bytes, "declared-header-extension"),
             (header_bytes, arm9_at, "pre-arm9-region"), (arm9_at, arm9_at + arm9_bytes, "arm9-header-image"),
             (arm9_at + arm9_bytes, arm7_at, "inter-processor-region"), (arm7_at, arm7_at + arm7_bytes, "arm7-header-image"),
             (used, len(image), "multiboot-trailer")]
    regions, cursor = [], 0
    for first, last, kind in spans:
        if first != cursor or last < first:
            raise ValueError("Utility child physical map is not a nonoverlapping exact partition")
        data = image[first:last]
        entry = {"kind": kind, "offset": first, "bytes": len(data), "sha256": sha(data),
                 "headerProcessorLoadSpan": kind in ("arm9-header-image", "arm7-header-image")}
        if not entry["headerProcessorLoadSpan"]:
            entry["uniformFill"] = data[0] if data and len(set(data)) == 1 else None
            entry["nonzeroBytes"] = sum(bool(byte) for byte in data)
            entry["classification"] = "uninterpreted-physical-metadata-or-gap"
        if kind == "inter-processor-region":
            words = struct.unpack_from("<3I", data)
            expected = (0xDEC00621, int(arm9["parameterAddress"], 0) - 0x02000000, 0)
            if words != expected or any(byte != 255 for byte in data[12:]):
                raise ValueError("Utility child post-ARM9 footer changed")
            entry.update(classification="measured-code-settings-footer-and-fill", footerBytes=12,
                         footerWords=[hex(word) for word in words], fillBytes=len(data) - 12, fillValue=255)
        regions.append(entry)
        cursor = last
    if cursor != len(image):
        raise ValueError("Utility child physical tail is unclaimed")
    return {"bytes": len(image), "headerDeclaredBytes": header_bytes, "regions": regions,
            "allPhysicalBytesPartitioned": True,
            "limitations": ["A region outside the two header load spans is not automatically proven non-executable under later runtime reads",
                            "The 512-byte pre-ARM9 record and 136-byte trailer remain uninterpreted and preserved"]}


def processor_layout(raw, processor, base, reset_entry, loader, parameter_words, handoff_offset):
    decoded = codeCompression.decompress(raw)
    decoded_file = ROOT / f"extract/utility/runtime/{processor}-decoded.bin"
    parsed = code.MainCodeFile(raw, base)
    trace = literal(decoded, base, loader, 0)
    parameter_address = int(trace["value"], 0)
    offset = parameter_address - base
    if parsed.codeSettingsOffs != offset:
        raise ValueError("Native loader and independent module-parameter decoder disagree")
    first, last, source, bss_start, bss_end = struct.unpack_from("<5I", decoded, offset)
    if not base <= source <= first <= last == base + len(decoded) or (last - first) % 12 or bss_end < bss_start or bss_start != source:
        raise ValueError("Utility runtime descriptors do not exactly partition their initialized image")
    parameter = struct.unpack_from("<" + "I" * parameter_words, decoded, offset)
    if processor == "arm9" and parameter[-2:] != (0xDEC00621, 0x2106C0DE):
        raise ValueError("Utility ARM9 SDK module-parameter magic changed")
    handoff = literal(decoded, base, handoff_offset, 1)
    handoff_target = int(handoff["value"], 0)
    branch = next((offset for offset in range(handoff_offset + 4, handoff_offset + 24, 4)
                   if struct.unpack_from("<I", decoded, offset)[0] == 0xE12FFF11), None)
    if branch is None:
        raise ValueError("Utility startup no longer performs the measured BX r1 handoff")
    handoff["branchInstructionAddress"] = hex(base + branch)
    cursor, modules, descriptors = source - base, [], []
    implicit_name = "main" if processor == "arm9" else "boot"
    rows = [(base, cursor, bss_end - bss_start, 0, implicit_name)]
    for index, location in enumerate(range(first - base, last - base, 12)):
        runtime, size, zeros = struct.unpack_from("<3I", decoded, location)
        if cursor + size > first - base or runtime % 4 or size % 4 or zeros % 4:
            raise ValueError("Utility autoload extent is invalid")
        name = ("itcm" if runtime == 0x01FF8000 else "dtcm" if runtime == 0x027E0000 else None) if processor == "arm9" else ("wram" if runtime == 0x037F8000 else "main" if runtime == 0x027E0000 else None)
        if name is None:
            raise ValueError("Previously unknown utility autoload requires explicit namespace review")
        descriptors.append({"index": index, "address": hex(base + location), "decodedOffset": location,
                            "runtimeAddress": hex(runtime), "initializedBytes": size, "bssBytes": zeros})
        rows.append((runtime, size, zeros, cursor, name))
        cursor += size
    if cursor != first - base:
        raise ValueError("Utility initialized payload has unclaimed bytes")
    for runtime, size, zeros, at, name in rows:
        identifier = f"utility-child-{processor}-{name}"
        binary = decoded[at:at + size]
        file = ROOT / f"extract/utility/runtime/{identifier}.bin"
        runtime_entry = reset_entry if name == implicit_name else handoff_target if runtime <= (handoff_target & ~1) < runtime + size else None
        zero_start = bss_start if name == implicit_name else runtime + size
        modules.append({"id": identifier, "name": identifier, "program": PROGRAM, "processor": processor,
                        "base": hex(runtime), "runtimeBase": hex(runtime), "runtimeEnd": hex(runtime + size),
                        "runtimeEntry": hex(runtime_entry) if runtime_entry is not None else None,
                        "entryMode": "thumb" if runtime_entry and runtime_entry & 1 else "arm" if runtime_entry is not None else None,
                        "applicationEntry": handoff["value"] if runtime <= (handoff_target & ~1) < runtime + size else None,
                        "inputDecodedOffset": at, "inputBytes": size, "bytes": size,
                        "binary": file.relative_to(ROOT).as_posix(), "sha256": sha(binary),
                        "bssStart": hex(zero_start), "bssBytes": zeros, "bssEnd": hex(zero_start + zeros),
                        "sourceMatchedBytes": 0, "sourceMatchedFunctions": 0, "sourceReconstructionComplete": False})
    info = {"processor": processor, "rawBytes": len(raw), "rawSha256": sha(raw), "decodedBytes": len(decoded),
            "decodedSha256": sha(decoded), "decodedBinary": decoded_file.relative_to(ROOT).as_posix(),
            "compressed": raw != decoded, "resetEntry": hex(reset_entry), "parameterAddress": hex(parameter_address),
            "parameterWords": [hex(value) for value in parameter], "nativeLoaderLiteral": trace, "nativeHandoffLiteral": handoff,
            "compositionTableAddress": hex(first), "compositionTableBytes": last - first,
            "compositionTableSha256": sha(decoded[first - base:last - base]), "descriptors": descriptors,
            "initializedPayloadExactlyPartitioned": True}
    files = {decoded_file: decoded}
    files.update({ROOT / module["binary"]: decoded[module["inputDecodedOffset"]:module["inputDecodedOffset"] + module["bytes"]] for module in modules})
    return info, modules, files


def derive():
    data = INPUT.read_bytes()
    if sha(data) != INPUT_HASH:
        raise ValueError("Utility original input identity changed")
    container = archive_members(data)
    entry = next(member for member in container["members"] if member["path"] == "move/child.srl")
    image = data[entry["offset"]:entry["offset"] + entry["bytes"]]
    if _common.crc16(image[0xC0:0x15C]) != struct.unpack_from("<H", image, 0x15C)[0] or _common.crc16(image[:0x15E]) != struct.unpack_from("<H", image, 0x15E)[0]:
        raise ValueError("Utility child header or logo CRC differs")
    child = rom.NintendoDSRom(image)
    if child.files or child.arm9OverlayTable or child.arm7OverlayTable:
        raise ValueError("Utility child filesystem or overlay inventory changed")
    used = struct.unpack_from("<I", image, 0x80)[0]
    if used > len(image):
        raise ValueError("Utility child header exceeds archive member")
    arm9, modules9, files9 = processor_layout(child.arm9, "arm9", child.arm9RamAddress, child.arm9EntryAddress, 0xA4C, 9, 0x954)
    arm7, modules7, files7 = processor_layout(child.arm7, "arm7", child.arm7RamAddress, child.arm7EntryAddress, 0x100, 6, 0xC0)
    report = {"schemaVersion": 1, "program": PROGRAM, "romSha256": audit_regions.ROM_HASH,
              "input": INPUT.relative_to(ROOT).as_posix(), "inputSha256": INPUT_HASH, "inputBytes": len(data),
              "container": container, "child": {"path": "move/child.srl", "containerOffset": entry["offset"], "bytes": len(image),
              "sha256": sha(image), "headerUsedBytes": used, "headerUsedSha256": sha(image[:used]),
              "logoCrc16": hex(struct.unpack_from("<H", image, 0x15C)[0]), "headerCrc16": hex(struct.unpack_from("<H", image, 0x15E)[0]),
              "crcVerified": True, "tailBytes": len(image) - used, "tailSha256": sha(image[used:]),
              "tailClassification": "Uninterpreted 136-byte multiboot trailer; no cryptographic verification or executable classification claimed",
              "filesystemFiles": 0, "arm9Overlays": 0, "arm7Overlays": 0},
              "processors": [arm9, arm7], "modules": modules9 + modules7, "childPhysicalMap": physical_map(image, arm9),
              "runtimeMappingCanonical": True, "sourceReconstructionComplete": False,
              "decoderFiles": {str(path.relative_to(ROOT)): sha(path.read_bytes()) for path in [Path(code.__file__), Path(codeCompression.__file__), Path(lz10.__file__), Path(fnt.__file__)]},
              "toolLimitations": [{"tool": "tools/dsd.exe rom extract", "status": "unsupported-input", "reason": "Multiboot banner offset 0 is interpreted as unknown banner version 18766; no original bytes changed"}],
              "limitations": ["The embedded program has independent CPU/runtime namespaces despite address overlap with the host game",
                              "Native loader literals, descriptor extents, hashes and CRCs establish the runtime map; function boundaries remain unclassified",
                              "All 394 utility member extents and every unclaimed padding byte are accounted for; LZ10 asset outputs are hashed",
                              "This inventory does not prove the host reaches the utility or verifies the multiboot trailer"]}
    files = {ROOT / "extract/utility/child.srl": image, **files9, **files7}
    return report, files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    report, files = derive()
    if args.verify:
        if json.loads(OUTPUT.read_text()) != report or any(not path.is_file() or path.read_bytes() != data for path, data in files.items()):
            raise ValueError("Utility runtime inventory or materialized source inputs are stale")
    else:
        for path, data in files.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print({"program": PROGRAM, "members": len(report["container"]["members"]),
           "modules": [(module["id"], module["bytes"], module["bssBytes"]) for module in report["modules"]], "verified": args.verify})


if __name__ == "__main__":
    main()
