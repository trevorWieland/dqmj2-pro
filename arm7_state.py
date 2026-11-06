from project import ROOT, read_json, sha256


def runtime_state():
    manifest = read_json(ROOT / "evidence/arm7/runtime-layout.json")
    if sha256(ROOT / manifest["image"]) != manifest["imageSha256"]:
        raise ValueError("ARM7 boot/autoload input identity differs")
    modules = []
    for item in manifest["modules"]:
        if sha256(ROOT / item["binary"]) != item["sha256"]:
            raise ValueError("ARM7 runtime module identity differs: " + item["name"])
        modules.append({**item, "functions": 0, "candidateInventory": "canonical-runtime-addresses-only", "originalObjectScaffolding": True})
    functions_path = ROOT / "evidence/arm7/runtime-functions.json"
    functions = read_json(functions_path) if functions_path.exists() else []
    if isinstance(functions, dict):
        functions = functions["functions"]
    for item in functions:
        if item["module"] not in {module["name"] for module in modules}:
            raise ValueError("Noncanonical ARM7 module identity in active function inventory")
    return modules, [dict(item, processor="arm7", symbol=item.get("symbol", "func_" + item["address"][2:]), boundaryConfidence=item.get("boundaryConfidence", "unverified-runtime-analysis")) for item in functions], manifest
