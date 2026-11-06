import hashlib
import json
from project import ROOT, configuration, now, read_json, sha256, verify_inputs, write_json, write_text


def maybe(path, default=None):
    target = ROOT / path
    return read_json(target) if target.exists() else default


def number(value):
    return int(value, 0) if isinstance(value, str) else value


def current(path, expected):
    target = ROOT / str(path).replace("\\", "/")
    return bool(expected and target.is_file() and sha256(target) == expected)


def union_size(ranges):
    result = 0
    end = -1
    for start, stop in sorted(ranges):
        result += max(0, stop - max(start, end))
        end = max(end, stop)
    return result


def collect_matches(namespace):
    matches = {}
    rejected = []
    from source_selection import preferences, choose, enforce
    policies = preferences(namespace)
    from recovery_registry import batches
    paths = [ROOT / batch["report"] for batch in batches() if batch["kind"] == "functions"] if (ROOT / "recovery.json").exists() else sorted((ROOT / "evidence/matches").glob("*.json"))
    for path in paths:
        report = read_json(path)
        if report.get("romSha256") != namespace:
            rejected.append({"report": path.relative_to(ROOT).as_posix(), "reason": "build namespace differs or absent"})
            continue
        compiler_info = report.get("compiler", {})
        compiler_info = compiler_info if isinstance(compiler_info, dict) else {}
        for item in report.get("functionMatches", report.get("matches", [])):
            source = item.get("source", report.get("source"))
            source_hash = item.get("sourceSha256", report.get("sourceSha256"))
            object_path = item.get("object", report.get("object"))
            object_hash = item.get("objectSha256", report.get("objectSha256"))
            exact = item.get("exactBytes", False) or item.get("exactAfterDeclaredRelocation", False)
            from source_dependencies import dependencies_current
            if not exact or not current(source, source_hash) or not current(object_path, object_hash) or not dependencies_current(item, report):
                rejected.append({"report": path.relative_to(ROOT).as_posix(), "name": item.get("name"), "reason": "nonexact result or stale source/object/dependency hash"})
                continue
            module = item.get("module", "main")
            module = "main" if module in ("arm9", "ARM9") else module
            mode = item.get("mode", "arm").lower()
            address = number(item["address"]) & ~1
            previous = matches.get((module, mode, address))
            candidate = {**item, "module": module, "mode": mode, "address": address, "size": item.get("size", item.get("bytes", item.get("matchingBytes"))), "source": source, "sourceSha256": source_hash, "object": object_path, "objectSha256": object_hash, "report": path.relative_to(ROOT).as_posix(), "compilerFlags": item.get("compilerFlags", item.get("flags", compiler_info.get("flags"))), "compilerSha256": item.get("compilerSha256", report.get("compilerSha256", compiler_info.get("sha256")))}
            from source_dependencies import dependency_hashes
            candidate['sourceDependencies'] = [{"path": path, "sha256": expected} for path, expected in dependency_hashes(item, report).items()]
            matches[(module, mode, address)] = choose(previous, candidate, policies.get((module, mode, address)))
    enforce(matches, rejected, policies)
    return matches, rejected


def build_state(write=True):
    config = configuration()
    inputs = verify_inputs(config)
    namespace = inputs["rom"]["sha256"]
    seed = read_json(ROOT / "provenance/seed-manifest.json")
    modules = [dict(item, processor="arm9") for item in seed["modules"]]
    arm7 = maybe("evidence/arm7/summary.json", {})
    from arm7_state import runtime_state
    arm7_modules, arm7_candidates, arm7_layout = runtime_state()
    modules.extend(arm7_modules)
    from utility_state import runtime_state as utility_runtime_state
    utility_modules, utility_candidates, utility_layout = utility_runtime_state()
    modules.extend(utility_modules)
    metadata = {item["name"]: item for item in modules}
    for module in modules:
        if sha256(ROOT / module["binary"]) != module["sha256"]:
            raise ValueError("Analyzed module differs from its measured seed: " + module["name"])
    matches, rejected = collect_matches(namespace)
    for bridge in (utility_layout or {}).get("linkageLedger", []):
        begin = number(bridge["address"])
        if any(item["module"] == bridge["module"] and item["address"] < begin + bridge["bytes"] and begin < item["address"] + item["size"] for item in matches.values()):
            raise ValueError("Accepted function overlaps a measured mixed-mode linkage region")
    linking = maybe("evidence/linking/latest.json", {})
    link_current = not linking.get("failure") and bool(linking.get("allModuleBytesExact")) and bool(linking.get("symbolCheckPassed")) and linking.get("buildNamespace") == namespace
    for unit in linking.get("sourceUnits", []):
        link_current = link_current and current(unit["object"], unit["sha256"])
    linked_modules = {item["module"]: item for item in linking.get("modules", []) if item.get("exactBytes") and current(item["output"], item["outputSha256"])} if link_current else {}
    source_units = linking.get("sourceUnits", []) if link_current else []
    arm7_link = maybe("evidence/linking/arm7-latest.json", {})
    arm7_link_current = bool(arm7_link.get("allModuleBytesExact") and arm7_link.get("symbolCheckPassed") and arm7_link.get("buildNamespace") == namespace and not arm7_link.get("failure"))
    for unit in arm7_link.get("sourceUnits", []):
        arm7_link_current = arm7_link_current and current(unit["object"], unit["sha256"])
    composition = arm7_link.get("composition") or {}
    if composition:
        arm7_link_current = arm7_link_current and composition.get("symbolCheckPassed") and current(composition["output"], composition["outputSha256"])
        for unit in composition.get("sourceUnits", []):
            arm7_link_current = arm7_link_current and current(unit["object"], unit["sha256"]) and current(unit["source"], unit["sourceSha256"])
    if arm7_link_current:
        linked_modules.update({item["module"]: item for item in arm7_link.get("modules", []) if item.get("exactBytes") and current(item["output"], item["outputSha256"])})
        source_units += arm7_link.get("sourceUnits", [])
    utility_link = maybe("evidence/linking/utility-latest.json", {})
    utility_current = bool(utility_link.get("allModuleBytesExact") and utility_link.get("symbolCheckPassed") and utility_link.get("buildNamespace") == namespace and utility_link.get("exactContainerMatch") and not utility_link.get("failure"))
    utility_current = utility_current and current(utility_link.get("output"), utility_link.get("outputSha256"))
    for unit in utility_link.get("sourceUnits", []):
        utility_current = utility_current and current(unit["object"], unit["sha256"]) and current(unit["source"], unit["sourceSha256"])
    for metadata_link in utility_link.get("metadataLinks", []):
        utility_current = utility_current and metadata_link.get("symbolCheckPassed") and current(metadata_link["output"], metadata_link["outputSha256"])
        for unit in metadata_link["sourceUnits"]:
            utility_current = utility_current and current(unit["object"], unit["sha256"]) and current(unit["source"], unit["sourceSha256"])
    if utility_current:
        linked_modules.update({item["module"]: item for item in utility_link["modules"] if item.get("exactBytes") and current(item["output"], item["outputSha256"])})
        source_units += utility_link["sourceUnits"]
    original = read_json(ROOT / "provenance/seed-source-map.json")["functions"]
    candidates = [dict(item, processor="arm9", boundaryConfidence="heuristic-ds-decomp") for item in original]
    candidates += arm7_candidates
    candidates += utility_candidates
    from boundary_reconciliations import reconcile
    candidates = reconcile(candidates, modules)
    from discontiguous_boundaries_20261030 import reconcile as reconcile_discontiguous
    candidates = reconcile_discontiguous(candidates, modules)
    from symbol_inventory import augment
    candidates = augment(candidates, modules, write=write)
    keys = {(item["module"], item["mode"].lower(), number(item["address"]) & ~1) for item in candidates}
    for key, match in matches.items():
        if key not in keys:
            candidates.append({"module": key[0], "processor": metadata[key[0]]["processor"], "mode": key[1], "address": hex(key[2]), "size": match["size"], "symbol": match["name"], "boundaryConfidence": "source-unit-byte-match"})
    records = []
    binaries = {item["name"]: (ROOT / item["binary"]).read_bytes() for item in modules}
    for item in candidates:
        module, mode, address = item["module"], item["mode"].lower(), number(item["address"]) & ~1
        match = matches.get((module, mode, address))
        size = match["size"] if match else item.get("size")
        offset = address - number(metadata[module]["base"])
        valid = size is not None and 0 <= offset and offset + size <= len(binaries[module])
        linked = bool(match and module in linked_modules and any(unit["module"] == module and number(unit["start"]) <= address and address + size <= number(unit["end"]) and unit["sha256"] == match["objectSha256"] for unit in source_units))
        record = {"id": f"{namespace}/{item['processor']}/{module}/{mode}/{address:08x}", "buildSha256": namespace, "processor": item["processor"], "module": module, "address": hex(address), "mode": mode, "symbol": item["symbol"], "bytes": size, "binaryOffset": offset, "boundaryConfidence": item["boundaryConfidence"], "inputModuleSha256": metadata[module]["sha256"], "inputBytesSha256": hashlib.sha256(binaries[module][offset:offset + size]).hexdigest() if valid else None, "sourceUnit": match["source"] if match else None, "sourceSha256": match["sourceSha256"] if match else None, "object": match["object"] if match else None, "objectSha256": match["objectSha256"] if match else None, "compilerSha256": match["compilerSha256"] if match else None, "compilerFlags": match["compilerFlags"] if match else None, "dependencies": match.get("relocations", []) if match else [], "matchingBytes": size if match else 0, "states": {"analyzed": True, "drafted": bool(match), "functionMatched": bool(match), "moduleLinked": linked, "wholeRomMatchedFromSource": False}, "assemblyJustification": match.get("assemblyJustification") if match else None, "evidence": match["report"] if match else item.get("discovery", item.get("evidence")), "unknowns": ["gameplay semantics not established by byte matching"] if match else ["source recovery", "compiler and flags", "verified boundaries and dependencies"]}
        records.append(record)
        record["protectionMetadata"] = item.get("protectionMetadata")
        record["sourceDependencies"] = match.get("sourceDependencies", []) if match else []
        record['sourceSelection'] = match.get('sourceSelection') if match else None
        record['alternativeImplementations'] = match.get('alternativeImplementations', []) if match else []
        record["sourceLanguage"] = match.get("sourceLanguage") if match else None
        record["hardwareAssemblyRanges"] = match.get("hardwareAssemblyRanges", []) if match else []
        record["ordinaryCBytes"] = match.get("ordinaryCBytes") if match else None
        record["justifiedAssemblyBytes"] = match.get("justifiedAssemblyBytes") if match else None
        record["justifiedAssemblyRanges"] = match.get("justifiedAssemblyRanges", []) if match else []
        record["program"] = metadata[module].get("program")
        record["alternativeImplementations"] = match.get("alternativeImplementations", []) if match else []
    (ROOT / "ledger").mkdir(exist_ok=True)
    if write:
        write_text(ROOT / "ledger/functions.jsonl", "".join(json.dumps(item, separators=(",", ":")) + "\n" for item in records))
    for module in modules:
        selected = [r for r in records if r["module"] == module["name"]]
        module["candidateFunctions"] = len(selected)
        module["sourceMatchedBytes"] = union_size([(number(r["address"]), number(r["address"]) + r["bytes"]) for r in selected if r["states"]["functionMatched"]])
        module["sourceLinkedBytes"] = union_size([(number(r["address"]), number(r["address"]) + r["bytes"]) for r in selected if r["states"]["moduleLinked"]])
        module["sourceMatchedFunctions"] = sum(r["states"]["functionMatched"] for r in selected)
        module["unresolvedModuleBytes"] = module["bytes"] - module["sourceMatchedBytes"]
        module["linkOutput"] = linked_modules.get(module["name"])
        module["originalObjectScaffolding"] = True
        module["sourceReconstructionComplete"] = False
        module.pop("sourceRebuiltFunctions", None)
    from data_ledger import record_data
    data_records = record_data(modules, source_units, linked_modules, write=write)
    from linkage_ledger import record_linkage
    linkage = record_linkage(modules, (utility_layout or {}).get("linkageLedger", []), source_units, linked_modules, write=write)
    from linker_layout_regions import record as record_layout
    record_layout(modules, linking, linked_modules, linkage, write=write)
    entrypoints = []
    for association in (utility_layout or {}).get("entryPointAssociations", []):
        parent = association["parentUnit"]
        matched = matches.get((association["module"], association["mode"], number(parent["address"])))
        covered = bool(matched and matched["sourceSha256"] == parent["sourceSha256"] and matched["size"] == parent["bytes"])
        linked = bool(covered and association["module"] in linked_modules and any(unit["module"] == association["module"] and number(unit["start"]) == number(parent["address"]) and unit["sha256"] == matched["objectSha256"] for unit in source_units))
        entrypoints.append({**association, "buildSha256": namespace, "states": {"analyzed": True, "coveredByMatchedParent": covered, "moduleLinked": linked}, "ordinaryFunctionCredit": 0, "separateSourceByteCredit": 0})
    if write:
        from native_alternate_entries import ledger_rows
        entrypoints.extend(ledger_rows())
        write_json(ROOT / "ledger/entrypoints.json", {"schemaVersion": 1, "buildSha256": namespace, "entries": entrypoints, "ordinaryFunctionCredit": 0, "separateSourceByteCredit": 0})
    pack = maybe("evidence/rom/exact-layout-result.json", {})
    arm7_current = bool(arm7.get("linkedOriginalBlobExact") and current("extract/arm7/arm7.bin", arm7.get("inputSha256")) and current("build/link-work/arm7/arm7.bin", arm7.get("linkedSha256")))
    pack_current = bool(pack.get("exactContainerMatch") and pack.get("rebuiltSha256") == namespace and current(pack.get("linkedRom"), pack.get("linkedRomSha256")) and current(pack.get("output"), pack.get("rebuiltSha256")))
    manifest = {"schemaVersion": 2, "createdUtc": now(), "visibility": "private-local-no-remote", "rom": inputs["rom"], "save": inputs["save"], "modules": modules, "discoveredFunctions": len(records), "functionMatched": sum(r["states"]["functionMatched"] for r in records), "sourceMatchedBytes": sum(m["sourceMatchedBytes"] for m in modules), "sourceLinkedBytes": sum(m["sourceLinkedBytes"] for m in modules), "unresolvedModuleBytes": sum(m["unresolvedModuleBytes"] for m in modules), "currentArm9ModuleLinksExact": len(linked_modules), "arm7OriginalBlobLinkExact": arm7_current, "exactContainerMatchWithScaffolding": pack_current, "sourceReconstructionComplete": False, "wholeRomMatchedFromSource": False, "rejectedMatchEvidence": rejected, "linkReportCurrent": link_current, "evidenceIndex": "evidence/index.json", "limitations": ["Function discovery is heuristic and not a complete code/data proof", "Matched-byte totals include associated literal pools", "Remaining binaries include code and data; unresolvedModuleBytes is not an executable-byte denominator", "Exact container matching uses retained layout metadata and token schedules; ordinary executable code remains largely original-object scaffolding"]}
    if write:
        write_json(ROOT / "ledger/modules.json", {"schemaVersion": 1, "buildSha256": namespace, "modules": modules})
    manifest["sourceMatchedFunctionBytes"] = sum(module["sourceMatchedFunctionBytes"] for module in modules)
    manifest["sourceMatchedDataBytes"] = sum(module["sourceMatchedDataBytes"] for module in modules)
    manifest["sourceMatchedBssBytes"] = sum(module["sourceMatchedBssBytes"] for module in modules)
    manifest["sourceMatchedPaddingBytes"] = sum(module["sourceMatchedPaddingBytes"] for module in modules)
    manifest["sourceCompleteModules"] = [module["name"] for module in modules if module["sourceReconstructionComplete"]]
    manifest["assemblyFunctionMatched"] = sum(bool(row["states"]["functionMatched"] and row["assemblyJustification"]) for row in records)
    manifest["cFunctionMatched"] = manifest["functionMatched"] - manifest["assemblyFunctionMatched"]
    manifest["arm7Container"] = {"imageSha256": arm7_layout["imageSha256"], "bytes": arm7_layout["imageBytes"], "compositionTableBytes": arm7_layout["compositionTableBytes"], "canonicalRuntimeModules": [module["name"] for module in arm7_modules], "rawLinearInventorySuperseded": True, "sourceReconstructionComplete": False}
    manifest["arm7Container"]["sourceMetadataBytes"] = arm7_link.get("sourceCompositionMetadataBytes", 0) if arm7_link_current else 0
    manifest["arm7Container"]["metadataLinkReport"] = composition if arm7_link_current else None
    manifest["currentArm9ModuleLinksExact"] = sum(module["name"] in linked_modules for module in modules if module["processor"] == "arm9")
    manifest["arm7RuntimeModuleLinksExact"] = sum(module["name"] in linked_modules for module in arm7_modules)
    manifest["currentHostArm9ModuleLinksExact"] = sum(module["name"] in linked_modules for module in modules if module["processor"] == "arm9" and not module.get("program"))
    manifest["arm7RecomposedImageExact"] = bool(arm7_link_current and current(arm7_link.get("image"), arm7_link.get("imageSha256")))
    manifest["embeddedPrograms"] = [{"program": utility_layout["program"], "parentSha256": utility_layout["inputSha256"], "childSha256": utility_layout["child"]["sha256"], "modules": [item["name"] for item in utility_modules], "runtimeMap": "evidence/utility/runtime-layout.json", "sourceReconstructionComplete": False}] if utility_layout else []
    manifest["currentUtilityModuleLinksExact"] = sum(module["name"] in linked_modules for module in utility_modules)
    manifest["utilityContainerRecomposedExact"] = bool(utility_current)
    manifest["outerRomUsesRecomposedUtility"] = bool(utility_current and link_current and linking.get("utilityRecomposedInput", {}).get("sha256") == utility_link.get("outputSha256"))
    manifest["executableInventoryComplete"] = False
    manifest["functionInventoryPendingModules"] = [module["name"] for module in modules if module.get("functionInventoryStatus") == "pending-qualified-analysis"]
    manifest["executableCoverage"] = {"sourceFunctionBytesIncludingLiteralPools": manifest["sourceMatchedFunctionBytes"], "unresolvedExecutableBytes": None, "unresolvedModuleBytesIncludingData": manifest["unresolvedModuleBytes"], "boundaryAndCodeDataProofComplete": False}
    manifest["linkerRegeneratedBytes"] = linkage["linkerRegeneratedBytes"]
    from interpreted_ledger import measure as measure_interpreted
    manifest['interpretedCoverage'] = measure_interpreted(write=write)
    if not write:
        from native_alternate_entries import ledger_rows
        entrypoints.extend(ledger_rows())
    manifest["qualifiedInteriorEntryPoints"] = len(entrypoints)
    manifest["linkerLinkedBytes"] = linkage["linkerLinkedBytes"]
    manifest["executableCoverage"]["unresolvedLinkageRegionBytesIncludingLiterals"] = sum(item["bytes"] for item in linkage["regions"] if not item["linkerRegenerated"])
    boundary = maybe("evidence/verification/boundaries.json", {})
    boundary_current = boundary.get("romSha256") == namespace and boundary.get("matchedFunctionCount") == manifest["functionMatched"] and current("ledger/functions.jsonl", boundary.get("functionLedgerSha256")) and all(current(product["path"], product["sha256"]) for product in boundary.get("products", []))
    manifest["executableCoverage"]["boundaryAuditCurrent"] = bool(boundary_current)
    manifest["executableCoverage"]["unreconciledIncomingInteriorEdges"] = len(boundary["externalInteriorBranches"]) if boundary_current else None
    manifest["executableCoverage"]["ambiguousMainToOverlayEdges"] = len(boundary["ambiguousOverlayBranches"]) if boundary_current else None
    manifest["executableCoverage"]["mappingUndecodedBytes"] = sum(item["mappingUndecodedBytes"] for item in boundary["modules"]) if boundary_current else None
    if not write:
        return manifest
    write_json(ROOT / "manifest.json", manifest)
    write_json(ROOT / "source-map.json", {"schemaVersion": 2, "buildSha256": namespace, "functionsLedger": "ledger/functions.jsonl", "matchedFunctions": [r for r in records if r["states"]["functionMatched"]]})
    write_json(ROOT / "ledger/backlog.json", {"schemaVersion": 1, "buildSha256": namespace, "priorities": [{"priority": 0, "task": "Keep every accepted match linked and current"}, {"priority": 1, "task": "Recover save bank selection, chronology, torn-write behavior and serialization"}, {"priority": 2, "task": "Recover progression, map/location and inventory predicates with native IDs"}, {"priority": 3, "task": "Recover synthesis, skills and acquisition dependencies"}, {"priority": 4, "task": "Resolve ARM7 boundary/mode conflicts and relocation recovery"}, {"priority": 5, "task": "Replace remaining original objects throughout all executable modules"}], "unmatchedCandidates": sum(not r["states"]["functionMatched"] for r in records), "moduleCoverage": [{"module": m["name"], "matchedBytes": m["sourceMatchedBytes"], "remainingModuleBytes": m["unresolvedModuleBytes"]} for m in modules], "completionRequires": ["All executable regions identified and reconstructed", "All affected modules match from source without original executable blobs", "Repeated clean exact whole-ROM source builds"]})
    return manifest


if __name__ == "__main__":
    result = build_state()
    print({key: result[key] for key in ("discoveredFunctions", "functionMatched", "sourceMatchedBytes", "sourceLinkedBytes", "sourceReconstructionComplete")})
