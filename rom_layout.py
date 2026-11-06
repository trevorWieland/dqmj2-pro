import argparse
import hashlib
import struct
from pathlib import Path
from project import ROOT, configuration, now, verify_inputs, write_json


def u32(data, offset):
    return struct.unpack_from("<I", data, offset)[0]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def file_names(data, start, size):
    names = {}
    visited = set()

    def directory(identifier, prefix):
        index = identifier & 0xFFF
        if index in visited:
            raise ValueError("FNT directory cycle")
        visited.add(index)
        table = start + index * 8
        offset, file_id, _ = struct.unpack_from("<IHH", data, table)
        position = start + offset
        while position < start + size:
            marker = data[position]
            position += 1
            if marker == 0:
                return
            length = marker & 127
            name = data[position:position + length].decode("ascii", errors="backslashreplace")
            position += length
            path = prefix + name
            if marker & 128:
                child = struct.unpack_from("<H", data, position)[0]
                position += 2
                directory(child, path + "/")
            else:
                names[file_id] = path
                file_id += 1
        raise ValueError("FNT directory did not terminate")

    directory(0xF000, "")
    return names


def layout(data):
    regions = []

    def add(name, start, size, kind, **fields):
        if start < 0 or size < 0 or start + size > len(data):
            raise ValueError("Invalid extent: " + name)
        if size:
            regions.append({"name": name, "start": start, "end": start + size, "bytes": size, "kind": kind, "sha256": sha(data[start:start + size]), **fields})

    header_size = u32(data, 0x84)
    add("header", 0, min(header_size, u32(data, 0x20)), "header")
    for processor, offset in (("arm9", 0x20), ("arm7", 0x30)):
        add(processor, u32(data, offset), u32(data, offset + 12), "executable", processor=processor, entry=hex(u32(data, offset + 4)), loadAddress=hex(u32(data, offset + 8)))
    footer = u32(data, 0x20) + u32(data, 0x2C)
    if footer + 12 <= len(data) and u32(data, footer) == 0xDEC00621:
        add("arm9-build-footer", footer, 12, "build-metadata", signature="0xDEC00621", buildInfoOffset=u32(data, footer + 4))
    fnt, fnt_size = u32(data, 0x40), u32(data, 0x44)
    fat, fat_size = u32(data, 0x48), u32(data, 0x4C)
    add("fnt", fnt, fnt_size, "filesystem-table")
    add("fat", fat, fat_size, "filesystem-table")
    names = file_names(data, fnt, fnt_size)
    overlay_ids = {}
    for processor, offset in (("arm9", 0x50), ("arm7", 0x58)):
        start, size = u32(data, offset), u32(data, offset + 4)
        add(processor + "-overlay-table", start, size, "overlay-table")
        for position in range(start, start + size, 32):
            identifier, load, ram_size, bss, init_start, init_end, file_id, flags = struct.unpack_from("<8I", data, position)
            overlay_ids[file_id] = {"processor": processor, "module": f"ov{identifier:03d}", "loadAddress": hex(load), "ramBytes": ram_size, "bssBytes": bss, "staticInitStart": hex(init_start), "staticInitEnd": hex(init_end), "flags": hex(flags)}
    banner = u32(data, 0x68)
    if banner:
        version = struct.unpack_from("<H", data, banner)[0]
        banner_size = {1: 0x840, 2: 0x940, 3: 0xA40, 0x103: 0x23C0}.get(version)
        if banner_size is None:
            raise ValueError("Unsupported banner version")
        add("banner", banner, banner_size, "banner", version=version)
    for file_id in range(fat_size // 8):
        start, end = struct.unpack_from("<II", data, fat + file_id * 8)
        overlay = overlay_ids.get(file_id)
        add("file:" + str(file_id), start, end - start, "overlay" if overlay else "asset", fileId=file_id, path=names.get(file_id), **(overlay or {}))
        if names.get(file_id) == "dwc/utility.bin" and not overlay:
            regions[-1].update(contentClass="embedded-executable-container", executableProgram="dwc/utility.bin/move/child.srl", executableInventory="evidence/utility/runtime-layout.json", executableInventoryComplete=False, measuredContainerHashMatches=regions[-1]["sha256"] == "db8ee36170897f60791f713b7669c50a125e62c6ad775fda98466c85fe48e81e")
    boundaries = sorted({0, len(data)} | {r[key] for r in regions for key in ("start", "end")})
    atoms = []
    for start, end in zip(boundaries, boundaries[1:]):
        owners = [r["name"] for r in regions if r["start"] <= start and end <= r["end"]]
        atoms.append({"start": start, "end": end, "bytes": end - start, "owners": owners, "sha256": sha(data[start:end]), "kind": "gap" if not owners else "component"})
    overlaps = [a for a in atoms if len(a["owners"]) > 1]
    return {"schemaVersion": 1, "romSha256": sha(data), "romBytes": len(data), "usedRomBytes": u32(data, 0x80), "deviceCapacity": data[0x14], "secureArea": {"start": 0x4000, "end": 0x8000, "note": "Overlaps ARM9 stored region; not a separate file"}, "regions": regions, "partition": atoms, "overlaps": overlaps, "fatEntries": fat_size // 8}


def compare(original, rebuilt):
    before, after = layout(original), layout(rebuilt)
    def identity(region):
        if region["kind"] == "asset":
            return "asset:" + str(region["path"])
        if region["kind"] == "overlay":
            return region["processor"] + ":" + region["module"]
        return region["name"]
    index = {identity(r): r for r in after["regions"]}
    components = []
    for old in before["regions"]:
        new = index.get(identity(old))
        components.append({"name": old["name"], "identity": identity(old), "kind": old["kind"], "originalStart": old["start"], "originalEnd": old["end"], "rebuiltStart": new["start"] if new else None, "rebuiltEnd": new["end"] if new else None, "sameBytes": bool(new and old["sha256"] == new["sha256"]), "samePlacement": bool(new and old["start"] == new["start"]), "originalSha256": old["sha256"], "rebuiltSha256": new["sha256"] if new else None})
    ranges = []
    for atom in before["partition"]:
        start, end = atom["start"], atom["end"]
        if original[start:end] != rebuilt[start:end]:
            ranges.append({"start": start, "end": end, "owners": atom["owners"], "kind": atom["kind"], "classification": "position-space mismatch; consult component mapping; unexplained until mapping proves cause"})
    return {"schemaVersion": 1, "createdUtc": now(), "originalSha256": before["romSha256"], "rebuiltSha256": after["romSha256"], "originalBytes": len(original), "rebuiltBytes": len(rebuilt), "exact": original == rebuilt, "componentComparisons": components, "positionMismatchRanges": ranges, "sameComponentBytes": sum(c["sameBytes"] for c in components), "changedComponentBytes": sum(not c["sameBytes"] for c in components), "sourceLinkedRebuild": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", type=Path)
    args = parser.parse_args()
    config = configuration()
    inputs = verify_inputs(config)
    original = config["rom"].read_bytes()
    report = layout(original)
    write_json(ROOT / "evidence/rom/layout.json", report)
    if args.compare:
        result = compare(original, (ROOT / args.compare).read_bytes())
        write_json(ROOT / "evidence/rom/repack-comparison.json", result)
        print({key: result[key] for key in ("exact", "sameComponentBytes", "changedComponentBytes")})
    assert verify_inputs(config) == inputs
    print({"fatEntries": report["fatEntries"], "regions": len(report["regions"]), "partition": len(report["partition"]), "overlaps": len(report["overlaps"])})
