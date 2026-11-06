from project import ROOT, configuration, read_json, sha256, write_json
from recovery_registry import batches


def record_linkage(modules, measured, source_units, linked_modules, write=True):
    accepted = {}
    for batch in batches():
        if batch["kind"] != "linkage":
            continue
        report = read_json(ROOT / batch["report"])
        if report["romSha256"] != configuration()["romSha256"]:
            raise ValueError("Linkage build identity differs")
        for generator in report["generatorSources"]:
            if sha256(ROOT / generator["path"]) != generator["sha256"]:
                raise ValueError("Linkage generator changed")
        for item in report["linkageMatches"]:
            if not (item["linkerRegenerated"] and item["exactNativeLinkageBytes"] and item["linkageOnlyRelink"]["exactBytes"] and item["ordinaryFunctionCredit"] == 0):
                raise ValueError("Linkage region lacks generated comparison proof")
            for label in ("source", "object"):
                if sha256(ROOT / item[label]) != item[label + "Sha256"]:
                    raise ValueError("Generated linkage artifact changed")
            key = item["module"], int(item["address"], 0)
            if key in accepted:
                raise ValueError("Duplicate accepted generated linkage region")
            accepted[key] = {**item, "evidence": batch["report"]}
    regions = []
    for item in measured:
        key = item["module"], int(item["address"], 0)
        match = accepted.pop(key, None)
        linked = False
        if match:
            if item["bytes"] != match["bytes"] or item["sha256"] != match["sha256"] or item["targetId"] != match["targetId"]:
                raise ValueError("Generated linkage differs from measured qualified region")
            linked = item["module"] in linked_modules and any(unit["module"] == item["module"] and unit["kind"] == "linkage" and int(unit["start"], 0) == key[1] and int(unit["end"], 0) == key[1] + item["bytes"] and unit["sha256"] == match["objectSha256"] for unit in source_units)
        regions.append({**item, "linkerRegenerated": bool(match), "fullProgramLinkedWithReplacement": linked, "ordinaryFunctionCredit": 0, "sourceFunctionCredit": 0, "source": match["source"] if match else None, "object": match["object"] if match else None, "objectSha256": match["objectSha256"] if match else None, "generationEvidence": match["evidence"] if match else None})
    if accepted:
        raise ValueError("Accepted linkage lies outside measured region inventory")
    for module in modules:
        chosen = [item for item in regions if item["module"] == module["name"]]
        module["linkerRegeneratedBytes"] = sum(item["bytes"] for item in chosen if item["linkerRegenerated"])
        module["linkerLinkedBytes"] = sum(item["bytes"] for item in chosen if item["fullProgramLinkedWithReplacement"])
        module["unresolvedModuleBytes"] -= module["linkerRegeneratedBytes"]
        module["sourceReconstructionComplete"] = module["sourceLinkedBytes"] + module["linkerLinkedBytes"] == module["bytes"] and module["sourceLinkedBssBytes"] == module["expectedBssBytes"] and module["name"] in linked_modules and module.get("functionInventoryStatus") != "pending-qualified-analysis"
        module["originalObjectScaffolding"] = not module["sourceReconstructionComplete"]
    result = {"schemaVersion": 2, "buildSha256": configuration()["romSha256"], "regions": regions, "linkerRegeneratedBytes": sum(item["bytes"] for item in regions if item["linkerRegenerated"]), "linkerLinkedBytes": sum(item["bytes"] for item in regions if item["fullProgramLinkedWithReplacement"]), "sourceMatchedBytes": 0, "ordinaryFunctionCredit": 0}
    if write:
        write_json(ROOT / "ledger/linkage.json", result)
    return result
