import argparse
import hashlib
import shutil
import struct
from pathlib import Path
import compression_recipe
from link_program import build_cpu
from link_arm7 import build_module
from project import ROOT, configuration, native_dependencies, now, read_json, sha256, verify_inputs, write_json
from recovery_registry import batches, entries
from utility_state import runtime_state

WORK = ROOT / "build/utility-link"


def accepted(program, processor=None):
    if processor is not None and processor not in ('arm9', 'arm7'):
        raise ValueError('Unknown embedded link processor')
    selected, symbols, bindings, metadata = [], {}, {}, []
    for batch in batches():
        report = read_json(ROOT / batch["report"])
        if report.get("program") != program:
            continue
        if processor is not None and report.get('processor') not in (None, processor):
            continue
        if report["romSha256"] != configuration()["romSha256"]:
            raise ValueError("Embedded source build namespace differs")
        for entry in entries(report):
            if report.get('processor') and entry.get('processor', report['processor']) != report['processor']:
                raise ValueError('Embedded report and entry processors differ')
            item = {**report, **entry}
            if entry in report.get("linkageMatches", []):
                if not (item.get("linkerRegenerated") and item.get("exactNativeLinkageBytes") and item.get("linkageOnlyRelink", {}).get("exactBytes") and item.get("ordinaryFunctionCredit") == 0):
                    raise ValueError("Embedded generated linkage is not independently regenerated")
                item.update(kind="linkage", mode=item["entryMode"], exactAfterDeclaredRelocation=True)
            if not (item.get("exactBytes") or item.get("exactAfterDeclaredRelocation") or item.get("kind") == "bss" and item.get("exactZeroStorage")):
                raise ValueError("Embedded source is not matched")
            for key in ("source", "object"):
                if sha256(ROOT / item[key]) != item[key + "Sha256"]:
                    raise ValueError("Embedded source/object identity changed")
            if entry in report.get("containerMatches", []):
                metadata.append(item)
            else:
                selected.append(item)
            for binding in entry.get("nativeSymbolBindings", []):
                if binding["program"] != program:
                    raise ValueError("Generated linkage target crosses programs")
                if binding["name"] in bindings and bindings[binding["name"]] != binding:
                    raise ValueError("Conflicting generated linkage binding")
                bindings[binding["name"]] = binding
                if binding["name"] in symbols and int(symbols[binding["name"]], 0) != int(binding["address"], 0):
                    raise ValueError("Conflicting generated linkage address")
                symbols[binding["name"]] = binding["address"]
        for name, address in report.get("nativeSymbols", {}).items():
            if name in symbols and int(symbols[name], 0) != int(address, 0):
                raise ValueError("Conflicting program-qualified native binding")
            symbols[name] = address
        for item in report.get("nativeSymbolBindings", []):
            if item["program"] != program:
                raise ValueError("Native utility binding names a different program")
            if item["name"] in bindings and bindings[item["name"]] != item:
                raise ValueError("Conflicting embedded entry binding")
            bindings[item["name"]] = item
    return selected, symbols, list(bindings.values()), metadata


def accepted_by_cpu(program, processors):
    plans, metadata = {}, {}
    for processor in processors:
        plan = accepted(program, processor)
        plans[processor] = plan
        for item in plan[3]:
            key = (item['source'], item.get('name'), item.get('module'), item.get('address'))
            if key in metadata and metadata[key] != item:
                raise ValueError('Conflicting embedded composition metadata')
            metadata[key] = item
    return plans, list(metadata.values())


def compose(layout, linked, metadata, config):
    parent = (ROOT / layout["input"]).read_bytes()
    offset = layout["child"]["containerOffset"]
    child = parent[offset:offset + layout["child"]["bytes"]]
    result = bytearray(child)
    transformations = []
    metadata_links = []
    for processor in layout["processors"]:
        cpu = processor["processor"]
        decoded = bytearray(processor["decodedBytes"])
        coverage = []
        for module in layout["modules"]:
            if module["processor"] != cpu:
                continue
            body = Path(linked[module["name"]]["output"]).read_bytes()
            start = module["inputDecodedOffset"]
            decoded[start:start + len(body)] = body
            coverage.append((start, start + len(body)))
        table = b"".join(struct.pack("<III", int(item["runtimeAddress"], 0), item["initializedBytes"], item["bssBytes"]) for item in processor["descriptors"])
        table_offset = processor["descriptors"][0]["decodedOffset"]
        if hashlib.sha256(table).hexdigest() != processor["compositionTableSha256"]:
            raise ValueError("Embedded descriptor construction differs")
        sources = [item for item in metadata if item["processor"] == cpu]
        if sources:
            if len(sources) != 1 or sources[0]["inputDecodedOffset"] != table_offset:
                raise ValueError("Compiled embedded metadata placement differs")
            source = sources[0]
            name = "utility-child-" + cpu + "-composition"
            binary = ROOT / "extract/utility/runtime" / (cpu + "-composition.bin")
            binary.write_bytes(table)
            module = {"name": name, "program": layout["program"], "processor": cpu, "base": source["address"], "binary": binary.relative_to(ROOT).as_posix(), "sha256": sha256(binary), "bssBytes": 0, "runtimeEntry": None}
            metadata_result, source_units = build_module(module, [{**source, "module": name}], {}, config, WORK)
            metadata_result["sourceUnits"] = source_units
            metadata_links.append(metadata_result)
            table = Path(metadata_result["output"]).read_bytes()
        decoded[table_offset:table_offset + len(table)] = table
        coverage.append((table_offset, table_offset + len(table)))
        cursor = 0
        for start, end in sorted(coverage):
            if start != cursor:
                raise ValueError("Embedded processor composition has an unclaimed/overlapping range")
            cursor = end
        if cursor != len(decoded) or hashlib.sha256(decoded).hexdigest() != processor["decodedSha256"]:
            raise ValueError("Embedded decoded processor image differs")
        header_offset = 0x20 if cpu == "arm9" else 0x30
        stored_offset, stored_bytes = struct.unpack_from("<I8xI", child, header_offset)
        original = child[stored_offset:stored_offset + stored_bytes]
        if hashlib.sha256(original).hexdigest() != processor["rawSha256"]:
            raise ValueError("Embedded stored executable identity differs")
        if processor["compressed"]:
            recipe = compression_recipe.make_recipe(original, bytes(decoded))
            packed = compression_recipe.encode(recipe, bytes(decoded))
            write_json(ROOT / f"evidence/utility/{cpu}-compression-recipe.json", recipe)
        else:
            packed = bytes(decoded)
        if packed != original:
            raise ValueError("Embedded stored representation differs")
        result[stored_offset:stored_offset + stored_bytes] = bytes(stored_bytes)
        result[stored_offset:stored_offset + stored_bytes] = packed
        transformations.append({"processor": cpu, "decodedBytes": len(decoded), "decodedSha256": hashlib.sha256(decoded).hexdigest(), "storedBytes": len(packed), "storedSha256": hashlib.sha256(packed).hexdigest(), "descriptorMetadataBytes": len(table), "originalExecutableLiteralBytesRetainedInCompressionRecipe": 0})
    if bytes(result) != child:
        raise ValueError("Embedded child container differs")
    rebuilt = bytearray(parent)
    rebuilt[offset:offset + len(result)] = bytes(len(result))
    rebuilt[offset:offset + len(result)] = result
    if bytes(rebuilt) != parent:
        raise ValueError("Utility container differs after source-module construction")
    output = WORK / "utility.bin"
    output.write_bytes(rebuilt)
    child_output = WORK / "child.srl"
    child_output.write_bytes(result)
    files = WORK / "files"
    shutil.copytree(ROOT / "extract/files", files, dirs_exist_ok=True)
    shutil.copy2(output, files / "dwc/utility.bin")
    return {"output": output.relative_to(ROOT).as_posix(), "outputSha256": sha256(output), "childOutput": child_output.relative_to(ROOT).as_posix(), "childOutputSha256": sha256(child_output), "filesystem": files.relative_to(ROOT).as_posix(), "transformations": transformations, "exactContainerMatch": True, "metadataLinks": metadata_links, "sourceCompositionMetadataBytes": sum(item["sourceBytes"] for item in metadata_links), "unclassifiedContainerRanges": layout.get("childPhysicalMap"), "sourceReconstructionComplete": False}


def main(clean=False):
    config = configuration()
    inputs = verify_inputs(config)
    native_dependencies(config)
    if sha256(config["linker"]) != "bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74":
        raise ValueError("Embedded linker identity changed")
    modules, candidates, layout = runtime_state()
    if not layout or len(modules) != 6:
        raise ValueError("Embedded canonical module inventory missing")
    if clean and WORK.exists():
        target = WORK.resolve()
        if target.parent != (ROOT / "build").resolve() or target.name != "utility-link":
            raise ValueError("Unsafe embedded clean-build target")
        shutil.rmtree(target)
    WORK.mkdir(parents=True, exist_ok=True)
    cpu_plans, metadata = accepted_by_cpu(layout['program'], [item['processor'] for item in layout['processors']])
    tail_path = ROOT / "evidence/utility/itcm-tail.json"
    if tail_path.exists():
        tail = read_json(tail_path)
        module = next(item for item in modules if item["name"] == tail["module"])
        if tail["inputModuleSha256"] != module["sha256"] or not tail["supportsDeterministicLinkerZeroAlignment"]:
            raise ValueError("Embedded source alignment evidence is stale")
        module["sourceAlignmentFill"] = {"start": tail["tail"]["address"], "bytes": tail["tail"]["bytes"], "alignment": tail["observedExtentAlignment"], "evidence": tail_path.relative_to(ROOT).as_posix(), "evidenceSha256": sha256(tail_path)}
    report = {"schemaVersion": 1, "createdUtc": now(), "buildNamespace": inputs["rom"]["sha256"], "program": layout["program"], "runtimeMapSha256": sha256(ROOT / "evidence/utility/runtime-layout.json"), "modules": [], "sourceUnits": [], "allModuleBytesExact": False, "sourceReconstructionComplete": False}
    try:
        for processor in layout["processors"]:
            functions, symbols, bindings, unused = cpu_plans[processor['processor']]
            selected = [module for module in modules if module["processor"] == processor["processor"]]
            results, units = build_cpu(selected, functions, symbols, bindings, config, WORK, processor["resetEntry"])
            report["modules"].extend(results)
            report["sourceUnits"].extend(units)
        report.update(compose(layout, {item["module"]: item for item in report["modules"]}, metadata, config))
        report.update(allModuleBytesExact=True, symbolCheckPassed=all(item["symbolCheckPassed"] for item in report["modules"]), sourceLinkedBytes=sum(item["compiledBytes"] for item in report["sourceUnits"] if item["kind"] != "linkage"), linkerRegeneratedBytes=sum(item["compiledBytes"] for item in report["sourceUnits"] if item["kind"] == "linkage"), sourceBssBytes=sum(item.get("allocatedBytes", 0) for item in report["sourceUnits"]), originalInputsUnchanged=inputs == verify_inputs(config))
    except Exception as error:
        report["failure"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        write_json(ROOT / "evidence/linking/utility-latest.json", report)
        stamp = report["createdUtc"].replace(":", "").replace(".", "").replace("+", "_")
        write_json(ROOT / f"evidence/linking/utility-{stamp}.json", report)
    print({"embeddedModulesExact": len(modules), "sourceInitializedBytes": report["sourceLinkedBytes"], "sourceBssBytes": report["sourceBssBytes"], "utilityContainerExact": report["exactContainerMatch"]})


if __name__ == "__main__":
    from build_lock import accepted_build
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true")
    with accepted_build():
        main(parser.parse_args().clean)
