import hashlib
import json
import os
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "deps/native"))
from ndspy import codeCompression
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_MEM_WRITE, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_CPSR

ROM_HASH = "674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6"
BASE = 0x021D7240


def sha(data):
    return hashlib.sha256(data).hexdigest()


def metadata():
    text = (ROOT / "extract/arm9_overlays/overlays.yaml").read_text()
    sections = re.split(r"(?m)^  - id: (\d+)\r?$", text)
    return {
        int(sections[i]): {
            "dsprotMetadataPresent": bool(re.search(r"(?m)^    dsprot:", sections[i + 1])),
            "blockSha256": sha(sections[i + 1].encode()),
        }
        for i in range(1, len(sections), 2)
    }


def constructors(module, decoded, entry):
    ident, base, size, bss, start, end, file_id, flags = entry
    sectionText = (ROOT / f"config/arm9/overlays/{module}/delinks.txt").read_text()
    sections = [
        {"name": n, "start": int(a, 16), "end": int(b, 16), "kind": k}
        for n, a, b, k in re.findall(r"(\.\w+)\s+start:(0x[0-9a-f]+) end:(0x[0-9a-f]+) kind:(\w+)", sectionText)
    ]
    textSection = next(x for x in sections if x["kind"] == "code")
    pointers = list(struct.unpack("<" + "I" * ((end - start) // 4), decoded[start - base : end - base]))
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    engine.mem_map(0x02000000, 0x400000)
    engine.mem_map(0x03000000, 0x20000)
    engine.mem_map(0x04000000, 0x1000)
    engine.mem_write(0x02000000, (ROOT / "extract/arm9/arm9.bin").read_bytes())
    engine.mem_write(base, decoded)
    engine.mem_write(base + size, bytes(bss))
    writes = []
    executed = set()

    def write(uc, access, address, width, value, user):
        if not any(
            x["kind"] in ["data", "bss"] and x["start"] <= address and address + width <= x["end"] for x in sections
        ):
            raise ValueError("Constructor wrote outside its own declared writable data/BSS sections")
        writes.append({"address": hex(address), "bytes": width, "value": hex(value & ((1 << (width * 8)) - 1))})

    def step(uc, address, width, user):
        if address != 0x04000000 and not base <= address < base + size:
            raise ValueError("Constructor executed outside measured overlay code")
        executed.add(address)

    engine.hook_add(UC_HOOK_MEM_WRITE, write)
    engine.hook_add(UC_HOOK_CODE, step)
    results = []
    for pointer in pointers:
        if pointer == 0:
            continue
        engine.reg_write(UC_ARM_REG_CPSR, 0x10)
        engine.reg_write(UC_ARM_REG_SP, 0x0301FF00)
        engine.reg_write(UC_ARM_REG_LR, 0x04000000)
        first = len(writes)
        engine.emu_start(pointer, 0x04000000, count=4096)
        if engine.reg_read(UC_ARM_REG_PC) != 0x04000000:
            raise ValueError("Constructor did not return within bound")
        results.append(
            {
                "entry": hex(pointer),
                "writes": writes[first:],
                "textUnchanged": bytes(engine.mem_read(textSection["start"], textSection["end"] - textSection["start"]))
                == decoded[textSection["start"] - base : textSection["end"] - base],
            }
        )
    runtime = bytes(engine.mem_read(base, size))
    if not all(r["textUnchanged"] for r in results):
        raise ValueError("Measured constructor sequence transformed executable text")
    changed = [i for i, (a, b) in enumerate(zip(decoded, runtime)) if a != b]
    return {
        "tableStart": hex(start),
        "tableEnd": hex(end),
        "entries": [hex(p) for p in pointers],
        "nonnullEntriesExecuted": len(results),
        "instructionLimitPerConstructor": 4096,
        "stateModel": "Fresh isolated overlay with zeroed own BSS; exact native constructor instructions execute without substituted call targets",
        "executedInstructionAddresses": [hex(a) for a in sorted(executed)],
        "results": results,
        "sectionEvidenceSha256": sha(sectionText.encode()),
        "sections": sections,
        "runtimeInitializedSha256": sha(runtime),
        "changedInitializedByteCount": len(changed),
        "changedInitializedAddresses": [hex(base + i) for i in changed],
        "runtimeTextSha256": sha(runtime[textSection["start"] - base : textSection["end"] - base]),
        "runtimeBssSha256": sha(bytes(engine.mem_read(base + size, bss))),
        "initializedBytesUnchanged": runtime == decoded,
        "executableTextUnchanged": all(r["textUnchanged"] for r in results),
        "limitations": [
            "This is a bounded constructor-sequence runtime view, not a hardware or full application overlay-load trace. Later function calls and unrelated loader hooks may still write module memory."
        ],
    }


def main():
    rom = (ROOT / "inputs/game.nds").read_bytes()
    if sha(rom) != ROM_HASH:
        raise ValueError("Unexpected original ROM namespace")
    table, table_size = struct.unpack_from("<2I", rom, 0x50)
    fat = struct.unpack_from("<I", rom, 0x48)[0]
    meta = metadata()
    modules = []
    for at in range(table, table + table_size, 32):
        entry = struct.unpack_from("<8I", rom, at)
        ident, base, size, bss, start, end, file_id, flags = entry
        if ident not in [4, 5, 6]:
            continue
        first, last = struct.unpack_from("<2I", rom, fat + file_id * 8)
        stored = rom[first:last]
        decoded = codeCompression.decompress(stored)
        module = f"ov{ident:03}"
        analysis = (ROOT / f"extract/arm9_overlays/{module}.bin").read_bytes()
        item = {
            "module": module,
            "loadAddress": hex(base),
            "initializedBytes": size,
            "bssBytes": bss,
            "overlayTableEntrySha256": sha(rom[at : at + 32]),
            "fatFileId": file_id,
            "fatStart": first,
            "fatEnd": last,
            "storedBytes": len(stored),
            "storedSha256": sha(stored),
            "flags": hex(flags),
            "compressed": bool(flags & 0x01000000),
            "declaredCompressedBytes": flags & 0xFFFFFF,
            "independentDecodedBytes": len(decoded),
            "independentDecodedSha256": sha(decoded),
            "extractedAnalysisSha256": sha(analysis),
            "independentDecodedEqualsExtracted": decoded == analysis,
            **meta[ident],
        }
        if ident in [5, 6]:
            if base != BASE or decoded != analysis or len(decoded) != size or meta[ident]["dsprotMetadataPresent"]:
                raise ValueError("Overlay view qualification differs")
            item["constructorRuntime"] = constructors(module, decoded, entry)
            item["qualification"] = (
                "Stored backward-LZ representation independently decodes byte-for-byte to the existing analysis image. Pinned extraction metadata declares no DSProtect transform; measured native constructors leave executable text unchanged and write only declared writable data/BSS. This qualifies the decoded image for module-scoped compiler matching without claiming absence of all possible later runtime transformations."
            )
        else:
            item["qualification"] = (
                "Positive protection-metadata control only; not constructor-executed or credited as recovered C by this audit."
            )
        modules.append(item)
    pins = [
        "tools/dsd.exe",
        "tools/ds-decomp-source/Cargo.lock",
        "tools/ds-decomp-source/lib/src/config/module.rs",
        "tools/ds-decomp-source/lib/src/config/config.rs",
        "tools/ds-decomp-source/cli/src/cmd/rom/extract.rs",
        "extract/arm9_overlays/overlays.yaml",
    ]
    report = {
        "schemaVersion": 1,
        "date": "2026-10-27",
        "kind": "overlay-stored-decoded-constructor-view-audit",
        "romSha256": ROM_HASH,
        "source": Path(__file__).name,
        "sourceSha256": sha(Path(__file__).read_bytes()),
        "tools": {p: sha((ROOT / p).read_bytes()) for p in pins},
        "independentDecompressor": {
            "path": "deps/native/ndspy/codeCompression.py",
            "sha256": sha(Path(codeCompression.__file__).read_bytes()),
        },
        "modules": modules,
        "acceptedSourceFunctions": 0,
        "acceptedSourceBytes": 0,
        "protectedDataCreditedAsSource": False,
        "loaderEvidence": "Pinned dsd analyze_overlay conditionally decrypts only when overlay.dsprot_state().is_present(); enable_dsprot=true retains this analysis behavior. The supplied extracted metadata marks overlay004 as DSProtect1.28 and leaves005/006 without dsprot entries.",
    }
    raw = json.dumps(report, indent=2).encode()
    target = ROOT / "evidence/validation" / ("overlay-runtime-views-" + sha(raw)[:12] + ".json")
    if target.exists() and target.read_bytes() != raw:
        raise ValueError("Immutable audit collision")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    current = target.parent / "overlay-runtime-views.json"
    temporary = current.with_suffix(".json.tmp")
    temporary.write_bytes(raw)
    os.replace(temporary, current)
    print(
        json.dumps(
            {
                "report": str(target.relative_to(ROOT)),
                "modules": [
                    {
                        "module": x["module"],
                        "decodedEqualsExtracted": x["independentDecodedEqualsExtracted"],
                        "dsprotMetadataPresent": x["dsprotMetadataPresent"],
                        "constructorsExecuted": x.get("constructorRuntime", {}).get("nonnullEntriesExecuted"),
                    }
                    for x in modules
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
