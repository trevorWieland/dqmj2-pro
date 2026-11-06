import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from elf_units import split_symbol, thumb_alignment
from project import write_json
from source_export_scope_v2_20261105 import source_weak_export, weak_record

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "build/link-work"
EVIDENCE = ROOT / "evidence/linking"
DSD_HASH = "5917df26bffc05d4752276a2e0b1edd21bd6e920aabe1992be8a50efc9d10932"
LINKER_HASH = "bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(command, cwd, env, report, timeout=180):
    result = subprocess.run(
        [str(x) for x in command], cwd=cwd, env=env, capture_output=True,
        text=True, errors="replace", timeout=timeout
    )
    item = {
        "argv": [str(x) for x in command], "cwd": str(cwd),
        "exitCode": result.returncode, "stdout": result.stdout,
        "stderr": result.stderr
    }
    report["commands"].append(item)
    print(result.stdout[:6000], end="")
    print(result.stderr[:6000], end="", file=sys.stderr)
    return result.returncode == 0


def prepare_units(path, report):
    if path is None:
        return []
    sys.path.insert(0, str(ROOT / "deps/native"))
    from elftools.elf.elffile import ELFFile
    specification = json.loads(path.read_text())
    if specification.get("schemaVersion") != 1:
        raise ValueError("Source units require schemaVersion 1")
    units = specification["units"]
    report["nativeSymbols"] = specification.get("nativeSymbols", {})
    report["excludedUnmatchedFunctions"] = specification.get("excludedUnmatchedFunctions", [])
    config_tree = WORK / "config-arm9"
    shutil.copytree(ROOT / "config/arm9", config_tree, dirs_exist_ok=True)
    occupied = {}
    metadata = {item["name"]: item for item in json.loads((ROOT / "manifest.json").read_text())["modules"]}
    binaries, symbol_updates, delink_updates, data_extents, weak_updates = {}, {}, {}, {}, {}
    for unit in units:
        module, name = unit["module"], unit["unit"]
        if Path(name).name != name or "." not in name:
            raise ValueError("Source unit must have one filename and extension")
        start, end = int(unit["start"], 0), int(unit["end"], 0)
        section_name = unit.get("section", ".text")
        if end <= start or any(start < b and a < end for a, b in occupied.get(module, [])):
            raise ValueError("Source ranges must be nonempty and disjoint")
        occupied.setdefault(module, []).append((start, end))
        relative = Path(".") if module == "main" else Path("overlays") / module if module.startswith("ov") else Path(module)
        source = (ROOT / unit["object"]).resolve()
        from source_dependencies import dependencies_current
        if not dependencies_current(unit):
            raise ValueError("Source unit include dependency is incomplete or stale")
        if sha(source) != unit["sha256"]:
            raise ValueError("Source object hash mismatch")
        if unit.get("source") and sha(ROOT / unit["source"]) != unit["sourceSha256"]:
            raise ValueError("Authored source hash differs from accepted source unit: " + unit["source"])
        module_info = metadata[module]
        if module not in binaries:
            binaries[module] = (ROOT / module_info["binary"]).read_bytes()
        target = binaries[module]
        target_object = WORK / Path(name).with_suffix(".o")
        with source.open("rb") as stream:
            elf = ELFFile(stream)
            weak_export = source_weak_export(unit, elf)
            if unit.get("function") or unit.get("symbol"):
                placement_section = section_name if unit.get("sourceSection", section_name) != section_name else None
                section_bytes, relocation_offsets = split_symbol(elf, unit.get("function", unit.get("symbol")), target_object, unit.get("interiorSymbols"), unit.get("relocationAliases"), unit.get("sectionPaddingBytes", 0), target_section=placement_section)
                placement = thumb_alignment(target_object, unit)
                if placement:
                    unit["placementAlignment"] = placement
            else:
                section_indices = [index for index, section in enumerate(elf.iter_sections()) if section.name == section_name]
                section_bytes = b"".join(elf.get_section(index).data() for index in section_indices)
                relocation_offsets = [r["r_offset"] for s in elf.iter_sections()
                                      if s["sh_type"] in ("SHT_REL", "SHT_RELA") and s["sh_info"] in section_indices
                                      for r in s.iter_relocations()]
                if relocation_offsets:
                    raise ValueError("Relocated source units require a function selector")
                shutil.copyfile(source, target_object)
            native_bytes = target[start - int(module_info["base"], 0):end - int(module_info["base"], 0)]
            if section_name == ".bss":
                ranges = (ROOT / "config/arm9" / relative / "delinks.txt").read_text()
                bss = re.search(r"^\s*\.bss\s+start:(0x[0-9a-f]+) end:(0x[0-9a-f]+)", ranges, re.M)
                if not bss or not int(bss[1], 0) <= start < end <= int(bss[2], 0):
                    raise ValueError("Source BSS unit lies outside measured BSS allocation")
                native_bytes = bytes(end - start)
            ignored = {offset + delta for offset in relocation_offsets for delta in range(4)}
            if len(section_bytes) != end - start or len(native_bytes) != len(section_bytes) or any(
                a != b and index not in ignored for index, (a, b) in enumerate(zip(section_bytes, native_bytes))
            ):
                raise ValueError("Source unit section bytes do not match entire specified range")
        delinks = config_tree / relative / "delinks.txt"
        delink_updates.setdefault(delinks, []).append(f"\n{name}:\n    complete\n    {section_name} start:{start:#010x} end:{end:#010x}\n")
        symbols = config_tree / relative / "symbols.txt"
        declaration = unit.get("nativeDataDeclaration")
        if declaration:
            if unit.get("kind") != "data" or declaration["name"] not in unit.get("symbols", {}) or int(declaration["address"], 0) != start or declaration["kind"] != "data(word)":
                raise ValueError("Native data declaration does not match its proven source placement")
            existing_names = {line.split(" ", 1)[0] for line in symbols.read_text().splitlines()}
            if declaration["name"] not in existing_names:
                with symbols.open("a") as stream:
                    stream.write(f"\n{declaration['name']} kind:{declaration['kind']} addr:{start:#010x}\n")
        for old, new in unit.get("symbols", {}).items():
            updates = symbol_updates.setdefault(symbols, {})
            if old in updates:
                raise ValueError("Source symbol alias has multiple definitions: " + old)
            updates[old] = new
            if weak_export and new == weak_export['name']:
                weak_updates.setdefault(symbols, set()).add(old)
                report.setdefault('sourceExportScopes', []).append(weak_export)
            if unit.get("kind") == "data":
                data_extents.setdefault(symbols, {})[old] = end - start
        report["sourceUnits"].append({**unit, "compiledBytes": 0 if section_name == ".bss" else len(section_bytes), "allocatedBytes": len(section_bytes) if section_name == ".bss" else 0,
                                      "prelinkUnrelocatedByteCheckPassed": True,
                                      "relocationOffsets": relocation_offsets, "stagedObject": str(target_object),
                                      "stagedObjectSha256": sha(target_object)})
    for path, additions in delink_updates.items():
        with path.open("a") as stream:
            stream.write("".join(additions))
    for path, updates in symbol_updates.items():
        counts = dict.fromkeys(updates, 0)
        lines = []
        for line in path.read_text().splitlines(keepends=True):
            old, separator, rest = line.partition(" ")
            if old in updates and separator:
                counts[old] += 1
                extent = data_extents.get(path, {}).get(old)
                if extent is not None:
                    rest = rest.replace("kind:data(any)", f"kind:data(byte[{extent}])", 1)
                    rest = re.sub(r"kind:bss(?=\s)", f"kind:bss(size={extent:#x})", rest, count=1)
                if old in weak_updates.get(path, set()):
                    rest = weak_record(rest)
                line = updates[old] + separator + rest
            lines.append(line)
        if any(count != 1 for count in counts.values()):
            raise ValueError("Source symbol aliases must each resolve exactly once: " + str(path) + " " + repr({name: count for name, count in counts.items() if count != 1}))
        path.write_text("".join(lines))
    return units


def collect_units(source_units, match_reports):
    if not match_reports:
        return source_units
    spec = json.loads(source_units.read_text()) if source_units else {"schemaVersion": 1, "units": []}
    from native_bindings import merge_target, scoped_bindings
    from project import configuration
    from source_selection import preferences
    policies = preferences(configuration()['romSha256'])
    preferred_reports = {sha(ROOT / row['report']): row['report'] for row in policies.values()}
    scoped = scoped_bindings(match_reports)
    for path in match_reports:
        source_report = preferred_reports.get(sha(path), path.resolve().relative_to(ROOT).as_posix())
        matches = json.loads(path.read_text())
        for name, value in matches.get("nativeSymbols", {}).items():
            merge_target(spec.setdefault("nativeSymbols", {}), scoped[path].get(name, name), value)
        records = matches.get("functionMatches", matches.get("matches", matches.get("functions", [])))
        if not isinstance(records, list):
            raise ValueError("Function match records must be an array")
        items = [(item, "function") for item in records]
        items += [(item, "data") for item in matches.get("dataMatches", [])]
        for item, kind in items:
            match = {**matches, **item}
            if not (match.get("exactAfterDeclaredRelocation") or match.get("functionMatched") or match.get("exactBytes") or kind == "data" and match.get("kind") == "bss" and match.get("exactZeroStorage")):
                spec.setdefault("excludedUnmatchedFunctions", []).append({"report": str(path), "function": match["name"]})
                continue
            start = int(match["address"], 0)
            size = match.get("bytes", match.get("expectedBytes", match.get("size")))
            original = match.get("dsdSymbol", match.get("nativeAlias", match.get("originalSymbol", f"func_{start:08x}")))
            interiors = dict(match.get("nativeInteriorSymbols", {}))
            if kind == "data":
                views = {name: address for name, address in match.get("dataAliases", {}).items() if start <= int(address, 0) < start + size}
                interiors.update(views)
                original = match.get("nativeAlias", next((name for name, address in views.items() if int(address, 0) == start), original))
            spec["units"].append({
                "module": "main" if match["module"] == "arm9" else match["module"],
                "processor": match.get('processor', 'arm9'),
                "unit": match["name"] + ".c", "function" if kind == "function" else "symbol": match["name"],
                "section": match.get("targetSection", match.get("section", ".text")), "sourceSection": match.get("section", ".text"), "kind": kind,
                "nativeDataDeclaration": match.get("nativeDataDeclaration"),
                "mode": match.get("mode", "arm").lower() if kind == "function" else None,
                "targetSha256": match.get("targetSha256"),
                "sectionPaddingBytes": match.get("sectionPaddingBytes", 0),
                "start": hex(start), "end": hex(start + size),
                "object": match["object"], "sha256": match["objectSha256"],
                "source": match["source"], "sourceSha256": match["sourceSha256"],
                "sourceReport": source_report,
                "symbols": {original: match["name"]},
                "interiorSymbols": {name: int(address, 0) - start for name, address in interiors.items()},
                "typedNativeBindings": match.get("nativeSymbolEntries", {}),
                "typedBindingRelocations": match.get("relocations", []) if match.get("nativeSymbolEntries") else [],
                "assemblyJustification": match.get("assemblyJustification")
            })
            from source_dependencies import dependency_hashes
            spec["units"][-1]["sourceDependencies"] = [{"path": path, "sha256": expected} for path, expected in dependency_hashes(item, matches).items()]
            for relocation in match.get("relocations", []):
                name = relocation.get("symbol", relocation["target"])
                address = relocation.get("targetAddress", relocation["target"])
                original_name = name
                name = scoped[path].get(name, name)
                if name != original_name:
                    spec["units"][-1].setdefault("relocationAliases", {})[str(relocation["offset"])] = name
                merge_target(spec["nativeSymbols"], name, address)
                from native_bindings import canonical_target
                if relocation.get("type") == 2 and int(address, 0) != int(canonical_target(original_name, address), 0):
                    alias = "__thumb_pointer_" + name
                    merge_target(spec["nativeSymbols"], alias, address)
                    spec["units"][-1].setdefault("relocationAliases", {})[str(relocation["offset"])] = alias
    from source_variants import consolidate
    spec["units"] = consolidate(spec["units"], policies)
    from host_bindings import apply_typed_bindings
    spec["units"] = apply_typed_bindings(spec["units"])
    target = WORK / "source-units.json"
    target.write_text(json.dumps(spec, indent=2) + "\n")
    return target


def native_link_symbols(report):
    defined = {value for unit in report["sourceUnits"] for value in unit.get("symbols", {}).values()}
    defined.update(name for unit in report["sourceUnits"] for name in unit.get("interiorSymbols", {}))
    symbol_root = WORK / "config-arm9" if report["sourceUnits"] else ROOT / "config/arm9"
    defined.update(line.split()[0] for path in symbol_root.rglob("symbols.txt")
                   for line in path.read_text().splitlines() if line.strip() and not line.lstrip().startswith("#"))
    assignments = []
    runtime_aliases = {old: new for unit in report["sourceUnits"] for old, new in unit.get("symbols", {}).items()
                       if old in ("Entry", "BuildInfo", "AutoloadCallback") and old != new}
    defined.update(runtime_aliases)
    for name, address in report.get("nativeSymbols", {}).items():
        if name in defined:
            continue
        if not re.fullmatch(r"[A-Za-z_]\w*", name):
            raise ValueError("Unsupported native link symbol: " + name)
        assignments.append(f"    {name} = {int(address, 0):#010x};")
    assignments.extend(f"    {old} = {new};" for old, new in runtime_aliases.items())
    report["requiredRuntimeSymbolAliases"] = runtime_aliases
    lcf = WORK / "arm9.lcf"
    text = lcf.read_text()
    index = text.rfind("}")
    lcf.write_text(text[:index] + "\n".join(assignments) + "\n" + text[index:])


def thumb_gap_alignment(report):
    if not any(unit["compiledBytes"] % 4 for unit in report["sourceUnits"]):
        return
    from elftools.elf.elffile import ELFFile
    changes = []
    for path in (WORK / "delinks").glob("_dsd_gap@*.o"):
        with path.open("rb") as stream:
            elf = ELFFile(stream)
            offsets = [elf["e_shoff"] + index * elf["e_shentsize"] + 32
                       for index, section in enumerate(elf.iter_sections())
                       if section.name == ".text" and section["sh_addralign"] > 2]
        if offsets:
            before = sha(path)
            data = bytearray(path.read_bytes())
            for offset in offsets:
                struct.pack_into("<I", data, offset, 2)
            path.write_bytes(data)
            changes.append({"path": str(path), "inputSha256": before, "outputSha256": sha(path)})
    lcf = WORK / "arm9.lcf"
    lcf.write_text(lcf.read_text().replace("ALIGNALL(4)", "ALIGNALL(2)"))
    report["generatedGapAlignmentChanges"] = changes
    report["gapAlignmentReason"] = "Synthetic byte ranges between Thumb units can start at a halfword address; native module section alignment is retained"


def generated_config(units):
    original = ROOT / "config/arm9/config.yaml"
    text = original.read_text()
    keys = "rom_config|build_path|delinks_path|object|delinks|symbols|relocations"

    def rewrite(match):
        indent, key, value = match.groups()
        if key == "build_path":
            path = WORK
        elif key == "delinks_path":
            path = WORK / "delinks" if units else ROOT / "build/delinks"
        elif key == "object":
            path = WORK / "build" / Path(value).name
        else:
            path = (original.parent / value).resolve()
            if units and key in ("delinks", "symbols", "relocations"):
                path = WORK / "config-arm9" / path.relative_to(ROOT / "config/arm9")
        return f"{indent}{key}: '{path.as_posix()}'"

    text = re.sub(rf"^(\s*)({keys}): (.+)$", rewrite, text, flags=re.M)
    config = WORK / "config.yaml"
    config.write_text(text)
    return config


def replacements(path, report):
    if path is None:
        return
    mapping = json.loads(path.read_text())
    if mapping.get("schemaVersion") != 1:
        raise ValueError("Replacement mapping requires schemaVersion 1")
    text_path = WORK / "objects.txt"
    objects = text_path.read_text().splitlines()
    staged = WORK / "replacement-objects"
    staged.mkdir(exist_ok=True)
    for entry in mapping["objects"]:
        name = entry["originalObject"]
        matches = [i for i, item in enumerate(objects) if Path(item.strip('"')).name == name]
        if len(matches) != 1 or Path(name).name != name:
            raise ValueError("Replacement must identify one unique original object: " + name)
        source = (ROOT / entry["replacementObject"]).resolve()
        if sha(source) != entry["sha256"]:
            raise ValueError("Replacement hash mismatch: " + str(source))
        target = staged / name
        shutil.copyfile(source, target)
        objects[matches[0]] = f'"{target.as_posix()}"'
        report["replacements"].append({**entry, "stagedObject": str(target)})
    text_path.write_text("\n".join(objects) + "\n")


def compare_modules(report):
    manifest = json.loads((ROOT / "manifest.json").read_text())
    for module in manifest["modules"]:
        name = module["name"]
        if module.get("program") or module.get("processor") == "arm7" or name.startswith("arm7"):
            continue
        filename = {"main": "arm9.bin", "itcm": "itcm.bin", "dtcm": "dtcm.bin"}.get(
            name, f"arm9_{name}.bin"
        )
        target = ROOT / module["binary"]
        output = WORK / "build" / filename
        item = {"module": name, "target": str(target), "output": str(output)}
        if output.exists():
            before, after = target.read_bytes(), output.read_bytes()
            item.update({
                "inputSha256": sha(target), "outputSha256": sha(output),
                "inputBytes": len(before), "outputBytes": len(after),
                "exactBytes": before == after,
                "mismatchBytes": sum(a != b for a, b in zip(before, after)) + abs(len(before) - len(after)),
                "firstMismatch": next((i for i, pair in enumerate(zip(before, after)) if pair[0] != pair[1]),
                                      min(len(before), len(after)) if len(before) != len(after) else None)
            })
        else:
            item.update({"exactBytes": False, "failure": "missing output"})
        report["modules"].append(item)


def main():
    parser = argparse.ArgumentParser(fromfile_prefix_chars="@")
    parser.add_argument("--replacements", type=Path)
    parser.add_argument("--source-units", type=Path)
    parser.add_argument("--source-matches", type=Path, action="append", default=[])
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    args.source_units = (ROOT / args.source_units).resolve() if args.source_units else None
    args.source_matches = [(ROOT / path).resolve() for path in args.source_matches]
    args.replacements = (ROOT / args.replacements).resolve() if args.replacements else None
    if args.clean and WORK.exists():
        if WORK.resolve().parent != (ROOT / "build").resolve() or WORK.name != "link-work":
            raise ValueError("Refusing to clean a path outside the generated link workspace")
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    project = json.loads((ROOT / "project.json").read_text())
    dsd, linker = ROOT / project["dsd"], ROOT / project["linker"]
    report = {
        "schemaVersion": 1, "createdUtc": datetime.now(timezone.utc).isoformat(),
        "buildNamespace": project["romSha256"], "kind": "original-object-link-scaffolding",
        "sourceReconstruction": False, "commands": [], "modules": [], "replacements": [], "sourceUnits": [],
        "tools": {"dsd": {"path": str(dsd), "sha256": sha(dsd)},
                  "linker": {"path": str(linker), "sha256": sha(linker)}}
    }
    success = False
    try:
        if sha(dsd) != DSD_HASH or sha(linker) != LINKER_HASH:
            raise ValueError("Pinned tool hash mismatch")
        units = prepare_units(collect_units(args.source_units, args.source_matches), report)
        config = generated_config(units)
        env = os.environ.copy()
        env["LM_LICENSE_FILE"] = str(ROOT / project["license"])
        run([linker, "-version"], WORK, env, report)
        if units and not run([dsd, "delink", "--config-path", config, "--all-mapping-symbols"], WORK, env, report):
            raise RuntimeError("Source-aware delinking failed")
        if not run([dsd, "lcf", "--config-path", config], WORK, env, report):
            raise RuntimeError("LCF generation failed")
        native_link_symbols(report)
        thumb_gap_alignment(report)
        from data_gap_alignment import apply as data_gap_alignment
        data_gap_alignment(report, WORK)
        replacements(args.replacements, report)
        report["objects"] = [
            {"path": line.strip('"'), "sha256": sha(line.strip('"'))}
            for line in (WORK / "objects.txt").read_text().splitlines() if line
        ]
        linked = run([
            linker, "-nostdlib", "-nodeadstrip", "-interworking", "-proc", "arm946e",
            "-main", "Entry", "-sym", "on", "-map", WORK / "arm9.lcf",
            "@" + str(WORK / "objects.txt"), "-o", WORK / "linked.elf"
        ], WORK, env, report)
        modules_checked = run([dsd, "check", "modules", "--config-path", config, "--fail"],
                              WORK, env, report)
        if linked:
            report["symbolCheckPassed"] = run([
                dsd, "check", "symbols", "--config-path", config,
                "--elf-path", WORK / "linked.elf", "--fail"
            ], WORK, env, report)
        compare_modules(report)
        success = linked and modules_checked and all(m["exactBytes"] for m in report["modules"])
        report["allModuleBytesExact"] = success
        if success:
            success = report.get("symbolCheckPassed", False)
            from linker_layout_regions import annotate
            annotate(report, WORK)
            report["sourceLinkedBytes"] = sum(item["compiledBytes"] for item in report["sourceUnits"])
            report["sourceBssBytes"] = sum(item.get("allocatedBytes", 0) for item in report["sourceUnits"])
            configured = run([dsd, "rom", "config", "--elf", WORK / "linked.elf", "--config", config],
                             WORK, env, report)
            if configured:
                arm7_image = ROOT / "build/arm7-link/image.bin"
                if arm7_image.is_file():
                    if sha(arm7_image) != sha(ROOT / "extract/arm7/arm7.bin"):
                        raise ValueError("Recomposed ARM7 image differs from measured input")
                    rom_config = WORK / "build/rom_config.yaml"
                    text = rom_config.read_text()
                    text, count = re.subn(r"^arm7_bin: .+$", "arm7_bin: '" + arm7_image.as_posix() + "'", text, flags=re.M)
                    if count != 1:
                        raise ValueError("Generated ROM configuration has no unique ARM7 input")
                    rom_config.write_text(text)
                    report["arm7RecomposedInput"] = {"path": str(arm7_image), "sha256": sha(arm7_image)}
                utility_report = ROOT / "evidence/linking/utility-latest.json"
                if utility_report.exists():
                    utility = json.loads(utility_report.read_text())
                    asset = ROOT / utility.get("output", "build/utility-link/utility.bin")
                    files = ROOT / utility.get("filesystem", "build/utility-link/files")
                    if utility.get("failure") or not utility.get("exactContainerMatch") or not asset.is_file() or sha(asset) != utility.get("outputSha256") or sha(files / "dwc/utility.bin") != utility["outputSha256"]:
                        raise ValueError("Recomposed utility input is missing or stale")
                    rom_config = WORK / "build/rom_config.yaml"
                    text, count = re.subn(r"^files_dir: .+$", "files_dir: '" + files.as_posix() + "'", rom_config.read_text(), flags=re.M)
                    if count != 1:
                        raise ValueError("Generated ROM configuration has no unique filesystem input")
                    rom_config.write_text(text)
                    report["utilityRecomposedInput"] = {"path": str(asset), "sha256": sha(asset), "filesystem": str(files), "program": utility["program"]}
                report["mixedScaffoldingRomBuilt"] = run([
                    dsd, "rom", "build", "--config", WORK / "build/rom_config.yaml",
                    "--rom", WORK / "roundtrip.nds"
                ], WORK, env, report)
                if report["mixedScaffoldingRomBuilt"]:
                    report["mixedScaffoldingRomSha256"] = sha(WORK / "roundtrip.nds")
            success = success and configured and report.get("mixedScaffoldingRomBuilt", False)
    except Exception as error:
        success = False
        report["failure"] = f"{type(error).__name__}: {error}"
        print(report["failure"], file=sys.stderr)
    finally:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        write_json(EVIDENCE / f"run-{stamp}.json", report)
        write_json(EVIDENCE / "latest.json", report)
    return 0 if success else 1


if __name__ == "__main__":
    from build_lock import accepted_build
    with accepted_build():
        raise SystemExit(main())
