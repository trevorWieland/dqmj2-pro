import hashlib
from compression_recipe import encode
from pack_exact import build
from project import ROOT, configuration, native_dependencies, now, read_json, verify_inputs, write_json
from rom_layout import layout


if __name__ == "__main__":
    config = configuration()
    inputs = verify_inputs(config)
    native_dependencies(config)
    from ndspy.codeCompression import decompress
    recipe = read_json(ROOT / "evidence/rom/packing-recipe.json")
    linked_path = ROOT / "build/link-work/roundtrip.nds"
    fresh = linked_path.read_bytes()
    first, components = build(fresh, recipe, config)
    second, _ = build(fresh, recipe, config)
    original = config["rom"].read_bytes()
    if first != original or second != original:
        raise ValueError("Repeated exact layout rebuild failed")
    source_region = next(r for r in layout(fresh)["regions"] if r["name"] == "arm9")
    decoded = bytearray(decompress(fresh[source_region["start"]:source_region["end"]]))
    build_info = int(next(line.split(":", 1)[1] for line in (ROOT / "extract/arm9/arm9.yaml").read_text().splitlines() if line.startswith("build_info:")))
    import struct
    region = next(r for r in recipe["regions"] if r["name"] == "arm9")
    struct.pack_into("<I", decoded, build_info + 20, int(region["loadAddress"], 16) + region["bytes"])
    decoded[0x4000] ^= 1
    try:
        changed = encode(recipe["compression"]["arm9"], decoded)
        mutation_detected = changed != original[region["start"]:region["end"]]
    except ValueError:
        mutation_detected = True
    if not mutation_detected:
        raise ValueError("Executable mutation was silently replaced by original bytes")
    invalid_size_rejected = False
    try:
        encode(recipe["compression"]["arm9"], decoded[:-1])
    except ValueError:
        invalid_size_rejected = True
    if not invalid_size_rejected:
        raise ValueError("Invalid decoded size accepted")
    report = {"schemaVersion": 1, "createdUtc": now(), "romSha256": inputs["rom"]["sha256"], "repeatedBuilds": 2, "exact": first == second == original, "outputSha256": hashlib.sha256(first).hexdigest(), "executableMutationDetected": mutation_detected, "invalidDecodedSizeRejected": invalid_size_rejected, "sourceReconstructionComplete": False, "originalScaffoldingRemains": True, "componentsChecked": len(components)}
    write_json(ROOT / "evidence/verification/packaging.json", report)
    if verify_inputs(config) != inputs:
        raise ValueError("Inputs changed")
    print(report)
