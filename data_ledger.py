import re
from project import ROOT, configuration, read_json, sha256, write_json
from recovery_registry import batches


def union_size(ranges):
    result, end = 0, -1
    for start, stop in sorted(ranges):
        result += max(0, stop - max(start, end))
        end = max(end, stop)
    return result


def record_data(modules, source_units, linked_modules, write=True):
    namespace = configuration()["romSha256"]
    records = []
    for batch in batches():
        if batch["kind"] not in ("data", "mixed"):
            continue
        report = read_json(ROOT / batch["report"])
        if report["romSha256"] != namespace:
            raise ValueError("Data build identity differs")
        for item in report["dataMatches"]:
            value = {**report, **item}
            from source_dependencies import dependencies_current
            if not dependencies_current(item, report):
                raise ValueError("Accepted data source dependency is incomplete or stale")
            for label in ("source", "object"):
                if sha256(ROOT / value[label]) != value[label + "Sha256"]:
                    raise ValueError("Accepted data evidence is stale: " + value[label])
            if not (value.get("exactBytes") or value.get("exactAfterDeclaredRelocation") or value.get("kind") == "bss" and value.get("exactZeroStorage")):
                raise ValueError("Accepted data is not exactly matched")
            address, size = int(value["address"], 0), value.get("size", value.get("bytes"))
            linked = value["module"] in linked_modules and any(unit["module"] == value["module"] and int(unit["start"], 0) == address and int(unit["end"], 0) == address + size and unit["sha256"] == value["objectSha256"] for unit in source_units)
            records.append({"id": f"{namespace}/{value.get('processor', 'arm9')}/{value['module']}/{value['kind']}/{address:08x}", "buildSha256": namespace, "module": value["module"], "kind": value["kind"], "section": value["section"], "address": hex(address), "bytes": size, "storedBytes": 0 if value["kind"] == "bss" else size, "source": value["source"], "sourceSha256": value["sourceSha256"], "object": value["object"], "objectSha256": value["objectSha256"], "compilerSha256": value["compilerSha256"], "compilerFlags": value.get("compilerFlags", value.get("flags")), "dependencies": value.get("relocations", []), "states": {"dataMatched": True, "moduleLinked": linked}, "evidence": batch["report"]})
            records[-1]["sourceSection"] = value["section"]
            records[-1]["section"] = value.get("targetSection", value["section"])
            from source_dependencies import dependency_hashes
            records[-1]["sourceDependencies"] = [{"path": path, "sha256": expected} for path, expected in dependency_hashes(item, report).items()]
    for module in modules:
        matching = [row for row in records if row["module"] == module["name"]]
        module["sourceMatchedFunctionBytes"] = module["sourceMatchedBytes"]
        module["sourceLinkedFunctionBytes"] = module["sourceLinkedBytes"]
        for state, source in (("Matched", matching), ("Linked", [row for row in matching if row["states"]["moduleLinked"]])):
            data = [row for row in source if row["kind"] != "bss"]
            bss = [row for row in source if row["kind"] == "bss"]
            module["source" + state + "DataBytes"] = union_size([(int(r["address"], 0), int(r["address"], 0) + r["bytes"]) for r in data])
            module["source" + state + "BssBytes"] = union_size([(int(r["address"], 0), int(r["address"], 0) + r["bytes"]) for r in bss])
            module["source" + state + "Bytes"] += module["source" + state + "DataBytes"]
        linked_padding = linked_modules.get(module["name"], {}).get("sourceAlignmentFill")
        padding_bytes = linked_padding.get("bytes", 0) if linked_padding else 0
        if linked_padding and sha256(ROOT / linked_padding["evidence"]) != linked_padding["evidenceSha256"]:
            raise ValueError("Linked source-alignment evidence changed")
        module["sourceMatchedPaddingBytes"] = padding_bytes
        module["sourceLinkedPaddingBytes"] = padding_bytes
        module["sourceMatchedBytes"] += padding_bytes
        module["sourceLinkedBytes"] += padding_bytes
        module["unresolvedModuleBytes"] = module["bytes"] - module["sourceMatchedBytes"]
        relative = "." if module["name"] == "main" else "overlays/" + module["name"] if module["name"].startswith("ov") else module["name"]
        delinks = ROOT / "config/arm9" / relative / "delinks.txt"
        ranges = re.findall(r"^\s*\.bss\s+start:(0x[0-9a-f]+) end:(0x[0-9a-f]+)", delinks.read_text(), re.M) if delinks.exists() else []
        module["expectedBssBytes"] = module.get("bssBytes") if "bssBytes" in module else sum(int(end, 0) - int(start, 0) for start, end in ranges) if ranges else None
        complete = module["sourceLinkedBytes"] == module["bytes"] and module["sourceLinkedBssBytes"] == module["expectedBssBytes"] and module["name"] in linked_modules and module.get("functionInventoryStatus") != "pending-qualified-analysis"
        module["sourceReconstructionComplete"] = complete
        module["originalObjectScaffolding"] = not complete
    if write:
        write_json(ROOT / "ledger/data.json", {"schemaVersion": 1, "buildSha256": namespace, "records": records})
    return records
