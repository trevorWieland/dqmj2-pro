import hashlib
from project import ROOT, configuration, read_json, sha256


def runtime_state():
    path = ROOT / "evidence/utility/runtime-layout.json"
    if not path.exists():
        return [], [], None
    report = read_json(path)
    if report["romSha256"] != configuration()["romSha256"] or sha256(ROOT / report["input"]) != report["inputSha256"]:
        raise ValueError("Embedded program parent namespace/input changed")
    if not report["runtimeMappingCanonical"] or not report["child"]["crcVerified"]:
        raise ValueError("Embedded program map is unverified")
    modules = []
    for item in report["modules"]:
        if item["program"] != report["program"] or sha256(ROOT / item["binary"]) != item["sha256"]:
            raise ValueError("Embedded module identity changed")
        modules.append({**item, "originalObjectScaffolding": True, "functionInventoryStatus": "pending-qualified-analysis"})
    inventory = ROOT / "evidence/utility/runtime-functions.json"
    functions = read_json(inventory) if inventory.exists() else []
    classifications = functions.get("moduleClassifications", []) if isinstance(functions, dict) else []
    entry_associations = functions.get("entryPointAssociations", []) if isinstance(functions, dict) else []
    if isinstance(functions, dict):
        if functions["program"] != report["program"] or functions["romSha256"] != report["romSha256"]:
            raise ValueError("Embedded function inventory namespace changed")
        functions = functions["functions"]
    lookup = {module["name"]: module for module in modules}
    candidates = []
    for item in functions:
        module = lookup[item["module"]]
        candidates.append({**item, "processor": module["processor"], "program": report["program"], "symbol": item.get("symbol", item.get("name", "func_" + item["address"][2:])), "boundaryConfidence": item.get("boundaryConfidence", "heuristic-qualified-embedded-analysis")})
        module["functionInventoryStatus"] = "heuristic-qualified-analysis"
    for classification in classifications:
        module = lookup[classification["module"]]
        proof = read_json(ROOT / classification["evidence"])
        if classification["program"] != report["program"] or classification["processor"] != module["processor"] or classification["inputModuleSha256"] != module["sha256"] or sha256(ROOT / classification["evidence"]) != classification["evidenceSha256"]:
            raise ValueError("Embedded data classification identity is stale")
        if proof["romSha256"] != report["romSha256"] or proof["module"] != module["name"] or proof["inputModuleSha256"] != module["sha256"] or not proof["dataOnlyAsLoaded"] or proof["initializedCodeBytes"] != 0 or proof["initializedDataBytes"] != module["bytes"] or proof["bssDataBytes"] != module["bssBytes"]:
            raise ValueError("Embedded data classification is not proven for the complete loaded image")
        if any(item["module"] == module["name"] for item in candidates) or classification["functionInventoryStatus"] != "data-only-verified-as-loaded":
            raise ValueError("Embedded data classification conflicts with candidate executable entries")
        module.update(functionInventoryStatus=classification["functionInventoryStatus"], loadedDataClassification=classification)
    bridges_path = ROOT / "evidence/utility/interworking-bridges.json"
    linkage = []
    aliases = set()
    if bridges_path.exists():
        bridges = read_json(bridges_path)
        if bridges["program"] != report["program"] or bridges["romSha256"] != report["romSha256"]:
            raise ValueError("Linkage inventory program namespace changed")
        for bridge in bridges["bridges"]:
            module = lookup[bridge["module"]]
            body = (ROOT / module["binary"]).read_bytes()
            offset = int(bridge["address"], 0) - int(module["base"], 0)
            if module["sha256"] != bridge["inputModuleSha256"] or hashlib.sha256(body[offset:offset + bridge["bytes"]]).hexdigest() != bridge["sha256"]:
                raise ValueError("Mixed-mode linkage region changed")
            aliases.update((bridge["module"], item["mode"], int(item["address"], 0)) for item in bridge["analysisAliases"])
            linkage.append({key: bridge[key] for key in ("program", "processor", "module", "address", "bytes", "sha256", "targetId", "modeSegments", "analysisAliases")})
            linkage[-1].update(id=report["romSha256"] + "/" + bridge["processor"] + "/" + bridge["module"] + "/mixed/" + bridge["address"], sourceMatchedBytes=0, sourceLinkedBytes=0, evidence=bridges_path.relative_to(ROOT).as_posix())
    candidates = [item for item in candidates if (item["module"], item["mode"].lower(), int(item["address"], 0)) not in aliases]
    for association in entry_associations:
        module = lookup[association["module"]]
        address = int(association["address"], 0)
        body = (ROOT / module["binary"]).read_bytes()
        offset = address - int(module["base"], 0)
        parent = association["parentUnit"]
        if association["program"] != report["program"] or association["processor"] != module["processor"] or association["inputModuleSha256"] != module["sha256"] or hashlib.sha256(body[offset:offset + association["bytes"]]).hexdigest() != association["nativeSpanSha256"]:
            raise ValueError("Embedded interior entry association changed")
        if not association["excludeFromOrdinaryFunctionBacklog"] or association["ordinaryFunctionCredit"] != 0 or association["separateSourceByteCredit"] != 0 or sha256(ROOT / parent["source"]) != parent["sourceSha256"] or address - int(parent["address"], 0) != association["offsetWithinParent"]:
            raise ValueError("Interior entry association lacks qualified zero-credit parent evidence")
        candidates = [item for item in candidates if (item["module"], item["mode"].lower(), int(item["address"], 0)) != (module["name"], association["mode"], address)]
    report["linkageLedger"] = linkage
    report["entryPointAssociations"] = entry_associations
    return modules, candidates, report
