import argparse
import base64
import hashlib
import struct
from pathlib import Path
from compression_recipe import encode, make_recipe
from project import ROOT, configuration, native_dependencies, now, read_json, verify_inputs, write_json
from rom_layout import layout


def identity(region):
    if region["kind"] == "asset":
        return "asset:" + str(region["path"])
    if region["kind"] == "overlay":
        return region["processor"] + ":" + region["module"]
    return region["name"]


def prepare(original, config):
    native_dependencies(config)
    from ndspy.codeCompression import decompress
    mapping = layout(original)
    metadata = {}
    schedules = {}
    for region in mapping["regions"]:
        name = identity(region)
        body = original[region["start"]:region["end"]]
        if region["kind"] not in ("asset", "executable", "overlay"):
            metadata[name] = base64.b64encode(body).decode("ascii")
        elif name == "arm9" or region["kind"] == "overlay":
            decoded = decompress(body)
            if decoded != body:
                schedules[name] = make_recipe(body, decoded)
    gaps = [{**atom, "dataBase64": base64.b64encode(original[atom["start"]:atom["end"]]).decode("ascii")} for atom in mapping["partition"] if atom["kind"] == "gap"]
    result = {"schemaVersion": 1, "createdUtc": now(), "romSha256": mapping["romSha256"], "romBytes": mapping["romBytes"], "regions": mapping["regions"], "metadata": metadata, "gaps": gaps, "compression": schedules, "sourceReconstruction": False, "limitations": ["Original container metadata and compression token schedules are retained", "All executable literal bytes must come from the supplied fresh linked ROM", "Original-object scaffolding remains separately accounted for by the linker report"]}
    write_json(ROOT / "evidence/rom/packing-recipe.json", result)
    return result


def build(fresh, recipe, config):
    native_dependencies(config)
    from ndspy.codeCompression import decompress
    rebuilt = bytearray(recipe["romBytes"])
    fresh_regions = {identity(region): region for region in layout(fresh)["regions"]}
    components = []
    for gap in recipe["gaps"]:
        rebuilt[gap["start"]:gap["end"]] = base64.b64decode(gap["dataBase64"])
    for region in recipe["regions"]:
        name = identity(region)
        if name in recipe["metadata"]:
            body = base64.b64decode(recipe["metadata"][name])
            origin = "original-container-metadata"
        else:
            current = fresh_regions[name]
            body = fresh[current["start"]:current["end"]]
            origin = "fresh-linked-rom"
            if name in recipe["compression"]:
                decoded = bytearray(decompress(body))
                if name == "arm9":
                    build_info = int(next(line.split(":", 1)[1] for line in (ROOT / "extract/arm9/arm9.yaml").read_text().splitlines() if line.startswith("build_info:")))
                    struct.pack_into("<I", decoded, build_info + 20, int(region["loadAddress"], 16) + region["bytes"])
                body = encode(recipe["compression"][name], decoded)
        if len(body) != region["bytes"]:
            raise ValueError("Component size changed: " + name)
        rebuilt[region["start"]:region["end"]] = body
        components.append({"identity": name, "origin": origin, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "matchesMeasuredComponent": hashlib.sha256(body).hexdigest() == region["sha256"]})
        if region.get("contentClass"):
            components[-1].update(contentClass=region["contentClass"], executableProgram=region["executableProgram"], ordinarySourceCredit=0)
    return bytes(rebuilt), components


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--linked-rom", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "build/exact-layout.nds")
    args = parser.parse_args()
    config = configuration()
    inputs = verify_inputs(config)
    original = config["rom"].read_bytes()
    recipe = prepare(original, config) if args.prepare else read_json(ROOT / "evidence/rom/packing-recipe.json")
    if args.linked_rom:
        linked = (ROOT / args.linked_rom).resolve()
        fresh = linked.read_bytes()
        rebuilt, components = build(fresh, recipe, config)
        output = (ROOT / args.output).resolve()
        if not output.is_relative_to(ROOT.resolve()):
            raise ValueError("ROM output must stay inside the private repository")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(rebuilt)
        report = {"schemaVersion": 1, "createdUtc": now(), "linkedRom": str(linked), "linkedRomSha256": hashlib.sha256(fresh).hexdigest(), "output": str(output.relative_to(ROOT)), "rebuiltSha256": hashlib.sha256(rebuilt).hexdigest(), "romBytes": len(rebuilt), "exactContainerMatch": rebuilt == original, "sourceReconstructionComplete": False, "containsOriginalExecutableScaffolding": True, "components": components, "packingMethod": "measured layout and original compression token schedule with executable literal bytes regenerated from fresh linker output"}
        write_json(ROOT / "evidence/rom/exact-layout-result.json", report)
        print({key: report[key] for key in ("exactContainerMatch", "romBytes", "rebuiltSha256", "sourceReconstructionComplete")})
        if rebuilt != original:
            raise SystemExit(1)
    assert verify_inputs(config) == inputs
