import collections
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "deps/native"))
import ndspy.narc
import ndspy.rom
import ndspy.lz10
from ndspy._common import crc16

ROM_HASH = "674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def nds_header(data, offset, logo):
    if len(data) < offset + 0x160 or data[offset + 0xC0:offset + 0x15C] != logo:
        return False
    header = data[offset:offset + 0x160]
    if crc16(header[0xC0:0x15C]) != struct.unpack_from("<H", header, 0x15C)[0] or crc16(header[:0x15E]) != struct.unpack_from("<H", header, 0x15E)[0]:
        return False
    fields = struct.unpack_from("<8I", header, 0x20)
    return all(fields[index] >= 0x200 and fields[index + 3] > 0 and offset + fields[index] + fields[index + 3] <= len(data)
               and 0x02000000 <= fields[index + 2] < 0x04000000 for index in (0, 4))


def ash(data):
    if len(data) < 16 or data[:4] != b"ASH\0":
        raise ValueError("Invalid ASH header")
    length = struct.unpack_from("<I", data, 4)[0]
    if not 0 < length <= 16 * 1024 * 1024:
        raise ValueError("ASH output exceeds the bounded format audit")
    output, source = bytearray(), 16
    while len(output) < length:
        flag = data[source]
        source += 1
        if not flag & 1:
            count = flag // 2
            if count == 0 or source + count > len(data) or len(output) + count > length:
                raise ValueError("Invalid ASH literal extent")
            output.extend(data[source:source + count])
            source += count
        else:
            packed = flag + data[source] * 256
            source += 1
            count = (packed >> 12) + 3
            reference = max(0, len(output) - 2048) + ((packed >> 1) & 2047)
            if reference >= len(output) or len(output) + count > length:
                raise ValueError("Invalid ASH reference extent")
            for _ in range(count):
                output.append(output[reference])
                reference += 1
    return bytes(output), source


def fpk(data):
    count = struct.unpack_from("<I", data, 4)[0]
    end = 8 + count * 40
    if not 0 < count <= 4096 or end > len(data):
        raise ValueError("Invalid FPK directory")
    result = []
    for index in range(count):
        at = 8 + index * 40
        raw = data[at:at + 32].split(b"\0", 1)[0]
        if not raw or any(byte < 32 or byte > 126 or byte in (47, 92) for byte in raw):
            raise ValueError("Invalid FPK member name")
        name = raw.decode("ascii")
        offset, size = struct.unpack_from("<II", data, at + 32)
        if offset < end or offset + size > len(data):
            raise ValueError("Invalid FPK member extent")
        result.append((name, offset, data[offset:offset + size]))
    return result


def narc(data):
    if len(data) < 28:
        raise ValueError("Truncated NARC header")
    magic, bom, version, size, header, blocks = struct.unpack_from("<4sHHIHH", data)
    if magic != b"NARC" or size != len(data) or header != 16 or blocks != 3 or version not in (1, 256):
        raise ValueError("Invalid NARC standard header")
    offset, chunks = 16, []
    for expected in (b"BTAF", b"BTNF", b"GMIF"):
        marker, length = struct.unpack_from("<4sI", data, offset)
        if marker != expected or length < 8 or offset + length > len(data):
            raise ValueError("Invalid NARC block extent")
        chunks.append((offset, length))
        offset += length
    if offset != len(data):
        raise ValueError("Unclaimed NARC tail")
    count = struct.unpack_from("<I", data, 24)[0]
    if 28 + count * 8 > chunks[0][0] + chunks[0][1]:
        raise ValueError("NARC allocation directory exceeds block")
    archive = ndspy.narc.NARC(data)
    start, payload_size = chunks[2][0] + 8, chunks[2][1] - 8
    result = []
    for index in range(count):
        first, last = struct.unpack_from("<II", data, 28 + index * 8)
        if not 0 <= first <= last <= payload_size:
            raise ValueError("NARC member exceeds payload")
        name = archive.filenames.filenameOf(index) or f"member-{index:05d}"
        result.append((name, start + first, data[start + first:start + last]))
    return result


def audit_files(rom, raw, runtime):
    entries, errors, candidates = [], [], []
    counts = collections.Counter()
    string_locations = collections.defaultdict(list)
    for module, base, binary in runtime:
        for match in re.finditer(rb"[ -~]{4,}\x00", binary):
            text = match.group()[:-1].decode("ascii")
            string_locations[text].append({"module": module, "address": hex(base + match.start())})
    logo = raw[0xC0:0x15C]
    def inspect(path, data, provenance, depth=0):
        counts["objectsInspected"] += 1
        marker = data[:4]
        entry = {"path": path, "bytes": len(data), "sha256": sha(data), "magicHex": marker.hex(),
                 "magicAscii": "".join(chr(byte) if 32 <= byte < 127 else "." for byte in marker),
                 "provenance": provenance}
        entries.append(entry)
        name = re.sub(r"^\d+:", "", path.rsplit("!", 1)[-1].rsplit("/", 1)[-1])
        reference_keys = {name, "/" + name, path, path.lstrip("/"), "rom:" + path}
        refs = [item for key in sorted(reference_keys) for item in string_locations.get(key, [])]
        if refs:
            entry["asciiNameOccurrencesInRuntime"] = refs
        reasons = []
        if len(data) >= 20 and marker == b"\x7fELF" and data[4:6] == b"\x01\x01" and struct.unpack_from("<H", data, 18)[0] == 40:
            reasons.append("Validated 32-bit little-endian ARM ELF header")
        if nds_header(data, 0, logo):
            reasons.append("NDS image header with valid logo/header CRCs and bounded nonempty processor images")
        if Path(name).suffix.lower() in (".elf", ".axf", ".ovl", ".srl", ".nds", ".arm", ".rel", ".o"):
            reasons.append("Explicit executable/object filename suffix requires review")
        elf_at = data.find(b"\x7fELF", 1)
        while elf_at >= 0:
            if len(data) >= elf_at + 20 and data[elf_at + 4:elf_at + 6] == b"\x01\x01" and struct.unpack_from("<H", data, elf_at + 18)[0] == 40:
                reasons.append(f"Embedded ARM ELF header at object offset {elf_at:#x}")
            elf_at = data.find(b"\x7fELF", elf_at + 1)
        logo_at = data.find(logo, 0xC1)
        while logo_at >= 0:
            header_at = logo_at - 0xC0
            if nds_header(data, header_at, logo):
                reasons.append(f"Embedded CRC-verified NDS image header at object offset {header_at:#x}")
            logo_at = data.find(logo, logo_at + 1)
        if reasons:
            candidates.append({"path": path, "sha256": entry["sha256"], "bytes": len(data), "evidence": reasons,
                               "classification": "candidate-only-no-runtime-execution-claim"})
        if depth >= 8:
            errors.append({"path": path, "reason": "Container recursion exceeds bounded depth 8"})
            return
        try:
            if path == "/dwc/utility.bin":
                import utility_runtime
                container = utility_runtime.archive_members(data)
                counts["utilityFntFatContainers"] += 1
                counts["archiveMembers"] += len(container["members"])
                entry.update(format="utility-FNT-FAT", memberCount=len(container["members"]), paddingBytes=sum(gap["bytes"] for gap in container["padding"]))
                for member in container["members"]:
                    member_data = data[member["offset"]:member["offset"] + member["bytes"]]
                    inspect(path + f"!{member['id']:04d}:" + member["path"], member_data,
                            {"container": path, "memberIndex": member["id"], "memberOffset": member["offset"], "memberName": member["path"],
                             "compression": member.get("transformation")}, depth + 1)
            elif provenance.get("compression") == "Nintendo LZ10":
                decoded = ndspy.lz10.decompress(data)
                counts["lz10Streams"] += 1
                entry.update(format="Nintendo-LZ10", decodedBytes=len(decoded), decodedSha256=sha(decoded))
                inspect(path + "!decoded", decoded, {"container": path, "transformation": "bounded Nintendo LZ10 decode"}, depth + 1)
            elif marker == b"ASH\0":
                decoded, consumed = ash(data)
                counts["ashStreams"] += 1
                entry.update(format="ASH", decodedBytes=len(decoded), decodedSha256=sha(decoded), consumedBytes=consumed, tailBytes=len(data) - consumed)
                inspect(path + "!decoded", decoded, {"container": path, "transformation": "bounded native ASH decode"}, depth + 1)
            elif marker in (b"FPK\0", b"NARC"):
                members = fpk(data) if marker == b"FPK\0" else narc(data)
                counts["fpkArchives" if marker == b"FPK\0" else "narcArchives"] += 1
                counts["archiveMembers"] += len(members)
                member_names = collections.Counter(name for name, offset, member in members)
                entry.update(format="FPK" if marker == b"FPK\0" else "NARC", memberCount=len(members),
                             duplicateMemberNames={name: count for name, count in member_names.items() if count > 1})
                for index, (member_name, offset, member) in enumerate(members):
                    inspect(path + f"!{index:04d}:" + member_name, member,
                            {"container": path, "memberIndex": index, "memberOffset": offset, "memberName": member_name}, depth + 1)
        except Exception as error:
            errors.append({"path": path, "reason": f"{type(error).__name__}: {error}"})
    for file_id, data in enumerate(rom.files):
        name = rom.filenames.filenameOf(file_id)
        if name is None:
            continue
        extracted = ROOT / "extract/files" / name
        if not extracted.is_file() or extracted.read_bytes() != data:
            raise ValueError("Named filesystem extraction differs from native FAT file")
        counts["namedFilesystemFiles"] += 1
        inspect("/" + name, data, {"romFileId": file_id})
    return {"counts": dict(counts), "entries": entries, "containerFailures": errors, "executableCandidates": candidates,
            "limitations": ["Code-looking instruction bytes are not classified as executable without measured loader or executable-header evidence",
                            "Validated FPK, NARC, ASH and the measured utility FNT/FAT and LZ10 wrappers are recursively expanded; unknown formats remain individually hashed",
                            "Exact ASCII filename occurrences are evidence of stored names, not execution or even a proven load operation",
                            "Raw native payloads without a recognized executable header are not ruled out; loader/call reachability remains a separate investigation",
                            "Interpreted scripts, event words, graphics and other data may contain application logic without being native CPU executable regions"]}


def main():
    raw = (ROOT / "inputs/game.nds").read_bytes()
    if sha(raw) != ROM_HASH:
        raise ValueError("Executable-region audit ROM identity changed")
    rom = ndspy.rom.NintendoDSRom(raw)
    manifest = json.loads((ROOT / "manifest.json").read_text())
    runtime = []
    for module in manifest["modules"]:
        if module.get("processor") == "arm9":
            runtime.append((module["name"], int(module["base"], 0), (ROOT / module["binary"]).read_bytes()))
    layout = json.loads((ROOT / "evidence/arm7/runtime-layout.json").read_text())
    for module in layout["modules"]:
        runtime.append((module["id"], int(module["base"], 0), (ROOT / module["binary"]).read_bytes()))
    import utility_runtime
    utility_layout, utility_files = utility_runtime.derive()
    existing = {name for name, base, binary in runtime}
    for module in utility_layout["modules"]:
        if module["id"] not in existing:
            runtime.append((module["id"], int(module["base"], 0), utility_files[ROOT / module["binary"]]))
    arm9 = next(binary for name, base, binary in runtime if name == "main")
    arm9_file_offset, entry, base, arm9_file_bytes = struct.unpack_from("<4I", raw, 0x20)
    if arm9[:0x800] != raw[arm9_file_offset:arm9_file_offset + 0x800]:
        raise ValueError("Secure prefix has an unaccounted extraction transformation")
    functions = []
    symbols = (ROOT / "config/arm9/symbols.txt").read_text()
    for name, mode, length, address in re.findall(r"^(\S+) kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)$", symbols, re.M):
        location, size = int(address, 0), int(length, 0)
        if base <= location < entry:
            data = arm9[location - base:location - base + size]
            functions.append({"name": name, "module": "main", "processor": "arm9", "mode": mode,
                              "address": address, "bytes": size, "sha256": sha(data)})
    header_gaps = []
    for first, last in [(0x200, 0x4000)]:
        data = raw[first:last]
        header_gaps.append({"romOffset": first, "bytes": len(data), "sha256": sha(data),
                            "byteHistogram": {hex(value): count for value, count in sorted(collections.Counter(data).items())}})
    overlay_offset, overlay_bytes = struct.unpack_from("<2I", raw, 0x50)
    overlays = []
    for at in range(overlay_offset, overlay_offset + overlay_bytes, 32):
        identifier, ram, size, zeros, init_first, init_last, file_id, flags = struct.unpack_from("<8I", raw, at)
        overlays.append({"module": f"ov{identifier:03d}", "processor": "arm9", "fileId": file_id,
                         "headerTableOffset": at, "runtimeBase": hex(ram), "initializedBytes": size,
                         "bssBytes": zeros, "rawFileBytes": len(rom.files[file_id]), "rawFileSha256": sha(rom.files[file_id])})
    unnamed = {index for index in range(len(rom.files)) if rom.filenames.filenameOf(index) is None}
    if unnamed != {overlay["fileId"] for overlay in overlays}:
        raise ValueError("Unnamed FAT payloads are not exactly the declared host ARM9 overlays")
    report = {"schemaVersion": 1, "romSha256": ROM_HASH, "auditScriptSha256": sha(Path(__file__).read_bytes()),
              "securePrefix": {"module": "main", "processor": "arm9", "romOffset": arm9_file_offset,
                               "runtimeBase": hex(base), "entry": hex(entry), "bytes": 0x800,
                               "sha256": sha(arm9[:0x800]), "containedInMainRuntimeModule": True,
                               "existingFunctionCandidates": functions, "candidateFunctionBytes": sum(item["bytes"] for item in functions)},
              "headerToSecureArea": header_gaps,
              "additionalProcessorHeaders": {"arm7OverlayOffset": hex(struct.unpack_from("<I", raw, 0x58)[0]),
                                             "arm7OverlayBytes": struct.unpack_from("<I", raw, 0x5C)[0],
                                             "unitCode": raw[0x12], "dsiProcessorFieldsHex": raw[0x1C0:0x1E0].hex()},
              "arm7Composition": {"imageSha256": layout["imageSha256"], "moduleInitializedBytes": sum(item["bytes"] for item in layout["modules"]),
                                  "descriptorTableBytes": layout["compositionTableBytes"], "physicalImageBytes": layout["imageBytes"]},
              "unnamedFatFiles": overlays,
              "embeddedPrograms": [{"program": utility_layout["program"], "runtimeLayout": "evidence/utility/runtime-layout.json",
                                    "modules": utility_layout["modules"], "sourceReconstructionComplete": False}],
              "filesystem": audit_files(rom, raw, runtime),
              "scope": "Measured native executable-region discovery audit; no additional source-completion claim"}
    out = ROOT / "evidence/regions/discovery.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print({"securePrefixFunctions": len(functions), "secureFunctionBytes": sum(item["bytes"] for item in functions),
           **report["filesystem"]["counts"], "failures": len(report["filesystem"]["containerFailures"]),
           "executableCandidates": len(report["filesystem"]["executableCandidates"])})


if __name__ == "__main__":
    main()
