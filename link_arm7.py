import hashlib
import os
import re
import struct
import subprocess
from pathlib import Path
from elf_units import split_symbol, thumb_alignment
from project import ROOT, configuration, native_dependencies, now, read_json, sha256, verify_inputs, write_json
from recovery_registry import batches, entries

WORK = ROOT / "build/arm7-link"


def gap_object(data, path, label, definitions=None):
    names = b"\0.text\0.symtab\0.strtab\0.shstrtab\0"
    definitions = sorted(definitions or [], key=lambda item: item["offset"])
    strings = bytearray(b"\0")
    symbols = bytes(16) + struct.pack("<IIIBBH", 0, 0, 0, 3, 0, 1)
    for item in definitions:
        marker = "$a" if item["mode"] == "arm" else "$t"
        at = len(strings)
        strings.extend(marker.encode() + b"\0")
        symbols += struct.pack("<IIIBBH", at, item["offset"], 0, 2, 0, 1)
    for name, offset in [(label, 0)] + [(item["name"], item["offset"]) for item in definitions]:
        if not re.fullmatch(r"[A-Za-z_]\w*", name) or not 0 <= offset < len(data):
            raise ValueError("Invalid native gap entry binding")
        at = len(strings)
        strings.extend(name.encode() + b"\0")
        symbols += struct.pack("<IIIBBH", at, offset, 0, 0x12, 0, 1)
    result, headers = bytearray(52), [bytes(40)]
    for name, kind, flags, payload, link, info, alignment, size in [(1, 1, 6, data, 0, 0, 2, 0), (7, 2, 0, symbols, 3, 2 + len(definitions), 4, 16), (15, 3, 0, strings, 0, 0, 1, 0), (23, 3, 0, names, 0, 0, 1, 0)]:
        result.extend(bytes((-len(result)) % alignment))
        offset = len(result)
        result.extend(payload)
        headers.append(struct.pack("<IIIIIIIIII", name, kind, flags, 0, offset, len(payload), link, info, alignment, size))
    result.extend(bytes((-len(result)) % 4))
    offset = len(result)
    result.extend(b"".join(headers))
    result[:52] = struct.pack("<16sHHIIIIIHHHHHH", b"\x7fELF\x01\x01\x01" + bytes(9), 1, 40, 1, 0, 0, offset, 0x05000000, 52, 0, 0, 40, 5, 4)
    path.write_bytes(result)


def accepted():
    functions = []
    symbols = {}
    for batch in batches():
        if batch["kind"] == "container":
            continue
        report = read_json(ROOT / batch["report"])
        if report.get("program"):
            continue
        if report.get("processor") != "arm7" and not report.get("module", "").startswith("arm7"):
            continue
        if report["romSha256"] != configuration()["romSha256"]:
            raise ValueError("ARM7 source namespace differs")
        for item in entries(report):
            item = {**report, **item}
            if not (item.get("exactBytes") or item.get("exactAfterDeclaredRelocation")):
                raise ValueError("ARM7 source is not exactly matched")
            for key in ("source", "object"):
                if sha256(ROOT / item[key]) != item[key + "Sha256"]:
                    raise ValueError("ARM7 accepted artifact changed")
            functions.append(item)
        for name, value in report.get("nativeSymbols", {}).items():
            if name in symbols and int(symbols[name], 0) != int(value, 0):
                raise ValueError("Conflicting ARM7 native symbol")
            symbols[name] = value
    return functions, symbols


def build_module(module, functions, native_symbols, config, output_root=None, native_bindings=None, prepare_only=False):
    from elftools.elf.elffile import ELFFile
    name, base = module["name"], int(module["base"], 0)
    processor = module.get("processor", "arm7")
    segment = processor.upper()
    native = (ROOT / module["binary"]).read_bytes()
    work = (output_root or WORK) / name
    work.mkdir(parents=True, exist_ok=True)
    chosen = sorted([item for item in functions if item["module"] == name and item.get("kind") != "bss"], key=lambda item: int(item["address"], 0))
    storage = [item for item in functions if item["module"] == name and item.get("kind") == "bss"]
    objects, selectors, units = [], [], []
    entry_bindings = [item for item in (native_bindings or []) if item.get("module") == name and item.get("processor") == processor and item.get("mode") in ("arm", "thumb")]
    entry_bindings = [{**item, "name": "__native_entry_" + item["name"], "address": hex(int(item["address"], 0) & ~1)} for item in entry_bindings]
    gap_definitions = []

    def gap_entries(start, end):
        selected = [{**item, "offset": int(item["address"], 0) - base - start} for item in entry_bindings if base + start <= int(item["address"], 0) < base + end]
        gap_definitions.extend(selected)
        return selected
    cursor = 0
    entry = None
    for item in chosen:
        begin = int(item["address"], 0) - base
        size = item.get("bytes", item.get("size"))
        if begin < cursor or begin + size > len(native):
            raise ValueError("ARM7 source range overlaps or escapes canonical initialized image")
        if begin > cursor:
            path = work / f"{name}_original_gap_{cursor:06x}.o"
            label = "original_" + name.replace("-", "_") + f"_{cursor:06x}"
            gap_object(native[cursor:begin], path, label, gap_entries(cursor, begin))
            objects.append(path)
            selectors.append(path.name + "(.text)")
            if cursor == 0:
                entry = label
        path = work / (item["name"] + ".o")
        function_aliases = {binding["name"]: 0 for binding in entry_bindings if int(binding["address"], 0) == base + begin}
        interior = item.get("interiorSymbols", [])
        for alias in interior:
            if alias.get("separateFunctionCredit") is not False or alias["mode"] not in ("arm", "thumb") or not 0 <= alias["offset"] < size or int(alias["address"], 0) != base + begin + alias["offset"]:
                raise ValueError("Source interior entry is not a qualified zero-credit alias")
            function_aliases[alias["name"]] = alias["offset"]
            for binding in entry_bindings:
                if int(binding["address"], 0) == int(alias["address"], 0) and binding["mode"] == alias["mode"]:
                    function_aliases[binding["name"]] = alias["offset"]
        branch_aliases = {str(rel["offset"]): "__native_entry_" + rel["symbol"] for rel in item.get("relocations", []) if rel.get("type") in (1, 10, 15, 28, 29) and any(binding["name"] == rel["symbol"] and binding.get("mode") in ("arm", "thumb") for binding in (native_bindings or []))}
        with (ROOT / item["object"]).open("rb") as stream:
            elf = ELFFile(stream)
            body, offsets = split_symbol(elf, item["name"], path, function_aliases, branch_aliases, item.get("sectionPaddingBytes", 0), function_aliases)
            symbol = next(symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols() if symbol.name == item["name"])
            section_name = elf.get_section(symbol["st_shndx"]).name
            if section_name != item.get("section", ".text"):
                raise ValueError("ARM7 initialized source section differs")
        alignment = thumb_alignment(path, item)
        ignored = {offset + delta for offset in offsets for delta in range(4)}
        target = native[begin:begin + size]
        if len(body) != size or any(a != b and i not in ignored for i, (a, b) in enumerate(zip(body, target))):
            raise ValueError("ARM7 source bytes differ before declared relocations")
        if begin == 0:
            entry = item["name"]
        objects.append(path)
        selectors.append(path.name + "(" + section_name + ")")
        units.append({"module": name, "unit": path.stem, "function": item["name"], "start": hex(base + begin), "end": hex(base + begin + size), "object": item["object"], "sha256": item["objectSha256"], "source": item["source"], "sourceSha256": item["sourceSha256"], "compiledBytes": size, "kind": item.get("kind", "function")})
        if alignment:
            units[-1]["placementAlignment"] = alignment
        units[-1]["nativeEntryAliases"] = list(function_aliases)
        units[-1]["interiorEntries"] = interior
        units[-1]["branchRelocationAliases"] = branch_aliases
        cursor = begin + size
    alignment_fill = module.get("sourceAlignmentFill")
    if alignment_fill:
        alignment = alignment_fill["alignment"]
        if cursor != int(alignment_fill["start"], 0) - base or any(native[cursor:]) or ((base + cursor + alignment - 1) // alignment) * alignment != base + len(native):
            raise ValueError("Source alignment extent/fill differs from measured module")
        selectors.append(f". = ALIGN({alignment});")
        cursor = len(native)
    if cursor < len(native):
        path = work / f"{name}_original_gap_{cursor:06x}.o"
        label = "original_" + name.replace("-", "_") + f"_{cursor:06x}"
        gap_object(native[cursor:], path, label, gap_entries(cursor, len(native)))
        objects.append(path)
        selectors.append(path.name + "(.text)")
        if cursor == 0:
            entry = label
    bss_selectors = []
    for item in storage:
        size = item.get("bytes", item.get("size"))
        if len(storage) != 1 or int(item["address"], 0) != base + len(native) or size != module["bssBytes"]:
            raise ValueError("ARM7 source BSS differs from measured autoload allocation")
        path = work / (item["name"] + ".o")
        with (ROOT / item["object"]).open("rb") as stream:
            elf = ELFFile(stream)
            body, offsets = split_symbol(elf, item["name"], path)
            symbol = next(symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols() if symbol.name == item["name"])
            if elf.get_section(symbol["st_shndx"])["sh_type"] != "SHT_NOBITS" or len(body) != size or offsets:
                raise ValueError("ARM7 BSS must be zero-fill storage without relocations")
        objects.append(path)
        bss_selectors.append(path.name + "(.bss)")
        units.append({"module": name, "unit": path.stem, "function": item["name"], "start": item["address"], "end": hex(int(item["address"], 0) + size), "object": item["object"], "sha256": item["objectSha256"], "source": item["source"], "sourceSha256": item["sourceSha256"], "compiledBytes": 0, "allocatedBytes": size, "kind": "bss"})
    assignments = []
    defined = {item["name"] for item in chosen + storage + gap_definitions}
    defined.update(alias for unit in units for alias in unit.get("nativeEntryAliases", []))
    for symbol, value in native_symbols.items():
        if symbol not in defined:
            if not re.fullmatch(r"[A-Za-z_]\w*", symbol):
                raise ValueError("Invalid ARM7 link symbol")
            assignments.append(f"{symbol} = {int(value, 0):#x};")
    if module["runtimeEntry"] is not None:
        address = int(module["runtimeEntry"], 0)
        if not base <= address & ~1 < base + len(native):
            raise ValueError("Declared runtime entry lies outside initialized module")
        entry = "entry_" + name.replace("-", "_")
        assignments.append(f"{entry} = {address:#x};")
    lcf = work / "module.lcf"
    bss = ".bss : {\n" + "\n".join(bss_selectors) + f"\n}} >> {segment}\n" if bss_selectors else ""
    lcf.write_text(f"MEMORY {{ {segment} : ORIGIN = {base:#x} > module.bin }}\nSECTIONS {{ .image : {{ ALIGNALL(2);\n" + "\n".join(selectors) + f"\n}} > {segment}\n" + bss + "\n".join(assignments) + "\n}\n")
    response = work / "objects.txt"
    response.write_text("\n".join('"' + str(path) + '"' for path in objects) + "\n")
    command = [str(config["linker"]), "-nostdlib", "-nodeadstrip", "-interworking", "-proc", "arm946e" if processor == "arm9" else "arm7tdmi", "-main", entry, str(lcf), "@" + str(response), "-o", str(work / "linked.elf")]
    if prepare_only:
        return {"module": module, "objects": [str(path) for path in objects], "selectors": selectors, "bssSelectors": bss_selectors, "defined": sorted(defined), "entry": entry, "gapDefinitions": gap_definitions, "sourceAlignmentFill": alignment_fill}, units
    result = subprocess.run(command, cwd=work, env=dict(os.environ, LM_LICENSE_FILE=str(config["license"])), capture_output=True, text=True, errors="replace", timeout=180)
    output = work / "module.bin"
    exact = result.returncode == 0 and output.is_file() and output.read_bytes() == native
    symbol_checks = []
    if result.returncode == 0:
        with (work / "linked.elf").open("rb") as stream:
            elf = ELFFile(stream)
            linked_entry = elf["e_entry"]
            linked_symbols = {symbol.name: symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols()}
            for unit in units:
                symbol = linked_symbols.get(unit["function"])
                correct = symbol is not None and symbol["st_value"] & ~1 == int(unit["start"], 0) and symbol["st_size"] == int(unit["end"], 0) - int(unit["start"], 0)
                if unit["kind"] == "bss" and symbol is not None:
                    correct = correct and any(segment["p_type"] == "PT_LOAD" and segment["p_vaddr"] == int(unit["start"], 0) and segment["p_memsz"] == unit["allocatedBytes"] and segment["p_filesz"] == 0 for segment in elf.iter_segments())
                symbol_checks.append({"symbol": unit["function"], "expectedAddress": unit["start"], "actualAddress": hex(symbol["st_value"]) if symbol is not None else None, "exact": correct})
        exact = exact and all(check["exact"] for check in symbol_checks)
        if module["runtimeEntry"] is not None:
            exact = exact and linked_entry & ~1 == int(module["runtimeEntry"], 0) & ~1
    report = {"module": name, "processor": processor, "inputSha256": module["sha256"], "output": str(output), "outputSha256": sha256(output) if output.is_file() else None, "inputBytes": len(native), "exactBytes": exact, "sourceFunctions": sum(unit["kind"] == "function" for unit in units), "sourceBssBytes": sum(unit.get("allocatedBytes", 0) for unit in units), "sourceBytes": sum(unit["compiledBytes"] for unit in units), "originalScaffoldingBytes": len(native) - sum(unit["compiledBytes"] for unit in units), "runtimeEntry": module["runtimeEntry"], "linkedElfEntry": hex(linked_entry) if result.returncode == 0 else None, "linkEntryIsArtificial": module["runtimeEntry"] is None, "command": command, "exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    report["symbolChecks"] = symbol_checks
    report["originalGapFunctionBindings"] = gap_definitions
    report["symbolCheckPassed"] = result.returncode == 0 and all(check["exact"] for check in symbol_checks)
    if not exact:
        write_json(ROOT / "evidence/linking/arm7-failed-module.json", report)
        raise ValueError("ARM7 module link mismatch: " + name + result.stdout + result.stderr)
    return report, units


def composition(layout, table, config):
    selected = [batch for batch in batches() if batch["kind"] == "container"]
    if not selected:
        return table, None
    if len(selected) != 1:
        raise ValueError("Ambiguous ARM7 composition source")
    report = read_json(ROOT / selected[0]["report"])
    if report["romSha256"] != configuration()["romSha256"] or len(report.get("containerMatches", [])) != 1:
        raise ValueError("ARM7 composition source namespace/count differs")
    item = {**report, **report["containerMatches"][0]}
    if item["inputFileOffset"] != layout["compositionTableFileOffset"] or item["bytes"] != len(table):
        raise ValueError("ARM7 composition source placement differs")
    for key in ("source", "object"):
        if sha256(ROOT / item[key]) != item[key + "Sha256"]:
            raise ValueError("ARM7 composition source/object changed")
    name = "arm7-composition"
    binary = ROOT / "extract/arm7/runtime/composition.bin"
    binary.write_bytes(table)
    module = {"name": name, "base": item["address"], "binary": binary.relative_to(ROOT).as_posix(), "sha256": sha256(binary), "bssBytes": 0, "runtimeEntry": None}
    result, units = build_module(module, [{**item, "module": name}], {}, config)
    result["sourceUnits"] = units
    return Path(result["output"]).read_bytes(), result


def main():
    config = configuration()
    inputs = verify_inputs(config)
    native_dependencies(config)
    if sha256(config["linker"]) != "bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74":
        raise ValueError("ARM7 linker identity differs")
    layout = read_json(ROOT / "evidence/arm7/runtime-layout.json")
    functions, symbols = accepted()
    WORK.mkdir(parents=True, exist_ok=True)
    report = {"schemaVersion": 1, "createdUtc": now(), "buildNamespace": inputs["rom"]["sha256"], "modules": [], "sourceUnits": [], "allModuleBytesExact": False, "sourceReconstructionComplete": False}
    try:
        image = bytearray(layout["imageBytes"])
        for module in layout["modules"]:
            result, units = build_module(module, functions, symbols, config)
            report["modules"].append(result)
            report["sourceUnits"].extend(units)
            start = module["inputFileOffset"]
            image[start:start + module["bytes"]] = Path(result["output"]).read_bytes()
        table = b"".join(struct.pack("<III", int(module["base"], 0), module["bytes"], module["bssBytes"]) for module in layout["modules"] if module.get("descriptorAddress"))
        table, metadata = composition(layout, table, config)
        report["composition"] = metadata
        at = layout["compositionTableFileOffset"]
        image[at:at + len(table)] = table
        output = WORK / "image.bin"
        output.write_bytes(image)
        if hashlib.sha256(image).hexdigest() != layout["imageSha256"]:
            raise ValueError("ARM7 recomposed boot/autoload image differs")
        report.update(allModuleBytesExact=True, symbolCheckPassed=all(module["symbolCheckPassed"] for module in report["modules"]) and (metadata is None or metadata["symbolCheckPassed"]), image=str(output.relative_to(ROOT)), imageSha256=sha256(output), sourceLinkedBytes=sum(unit["compiledBytes"] for unit in report["sourceUnits"]), sourceCompositionMetadataBytes=len(table) if metadata else 0, preservedCompositionMetadataBytes=0 if metadata else len(table), originalInputsUnchanged=inputs == verify_inputs(config))
    except Exception as error:
        report["failure"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        write_json(ROOT / "evidence/linking/arm7-latest.json", report)
        stamp = report["createdUtc"].replace(":", "").replace(".", "").replace("+", "_")
        write_json(ROOT / f"evidence/linking/arm7-{stamp}.json", report)
    print({"arm7RuntimeModulesExact": len(report["modules"]), "sourceFunctions": sum(unit["kind"] == "function" for unit in report["sourceUnits"]), "sourceBytes": report["sourceLinkedBytes"], "sourceBssBytes": sum(unit.get("allocatedBytes", 0) for unit in report["sourceUnits"]), "recomposedImageExact": True})


if __name__ == "__main__":
    from build_lock import accepted_build
    with accepted_build():
        main()
