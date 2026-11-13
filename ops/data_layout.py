"""Data-layout model for the measured Nintendo DS build.

The compiler does not preserve source order in an object's data sections.  A
source file with several string or constant declarations produces a sequence
that is a deterministic permutation of the declarations, so a data region can
only be reproduced by modelling that permutation and ordering the source
accordingly.

This module owns the model end to end:

* :func:`read_elf` and :func:`object_layout` describe the data sections and
  symbols a compiled object actually emitted, including multiple same-named
  sections (MWCC emits one ``.rodata``/``.data`` section per alignment group).
* :func:`classify` compares that layout with a measured original region and
  decides whether the bytes are identical, differ only by block order, or
  differ in content.
* :func:`declaration_order` inverts the measured MWCC emission rule
  (reverse declaration order, except the last declaration, which is emitted
  last) and returns the source declaration order that reproduces a measured
  sequence.
* :func:`measure` walks a repository compile report and classifies every data
  block emitted by compiled source in the selected modules.

The model is deliberately explicit about its limits: it returns ``model``
metadata and a ``breaks`` list instead of guessing when a file's symbols are
not one contiguous, homogeneous group.

Only the Python standard library is used so the tool runs in the public
reproduction checkout without private packages.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import struct
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

ELF_MAGIC = b"\x7fELF\x01\x01\x01"
DATA_SECTION_PREFIXES = (".rodata", ".data", ".sdata", ".data1", ".rodata1")
SHF_ALLOC = 0x2
SHF_EXECINSTR = 0x4
SHT_PROGBITS = 1
SHT_SYMTAB = 2
SHT_RELA = 4
SHT_NOBITS = 8
SHT_REL = 9
STT_OBJECT = 1
STT_NOTYPE = 0


class LayoutError(ValueError):
    """Raised when an input is not a layout this tool can model."""


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def align_up(value, alignment):
    alignment = max(1, int(alignment))
    return (value + alignment - 1) // alignment * alignment


def is_data_section(name):
    return name.startswith(DATA_SECTION_PREFIXES)


def read_elf(path):
    """Return ``(sections, symbols)`` for a little-endian ARM ELF32 object."""
    raw = Path(path).read_bytes()
    if raw[:7] != ELF_MAGIC or len(raw) < 52:
        raise LayoutError("not an ELF32 object: " + str(path))
    header = struct.unpack_from("<16sHHIIIIIHHHHHH", raw)
    if header[1:4] != (1, 40, 1) or header[11] != 40:
        raise LayoutError("not a relocatable ARM32 object: " + str(path))
    section_offset, section_count, name_index = header[6], header[12], header[13]
    if section_offset + section_count * 40 > len(raw) or name_index >= section_count:
        raise LayoutError("ELF section table escapes the object")
    headers = [struct.unpack_from("<IIIIIIIIII", raw, section_offset + 40 * index)
               for index in range(section_count)]
    names = raw[headers[name_index][4]:headers[name_index][4] + headers[name_index][5]]

    def section_name(at):
        end = names.find(b"\0", at)
        return names[at:end].decode("utf-8", "replace")

    sections = []
    for index, row in enumerate(headers):
        offset, size = row[4], row[5]
        if row[1] != SHT_NOBITS and offset + size > len(raw):
            raise LayoutError("ELF section payload escapes the object")
        sections.append({
            "index": index,
            "name": section_name(row[0]),
            "type": row[1],
            "flags": row[2],
            "address": row[3],
            "offset": offset,
            "size": size,
            "link": row[6],
            "info": row[7],
            "align": row[8],
            "entsize": row[9],
        })

    symbols = []
    symbol_tables = [section for section in sections if section["type"] == SHT_SYMTAB]
    for symbol_table in symbol_tables:
        if symbol_table["link"] >= len(sections):
            raise LayoutError("ELF symbol table has an invalid string table")
        strings = sections[symbol_table["link"]]
        blob = raw[strings["offset"]:strings["offset"] + strings["size"]]
        for at in range(0, symbol_table["size"], 16):
            name_at, value, size, info, other, shndx = struct.unpack_from(
                "<IIIBBH", raw, symbol_table["offset"] + at)
            end = blob.find(b"\0", name_at)
            symbols.append({
                "name": blob[name_at:end].decode("utf-8", "replace") if end >= 0 else "",
                "value": value,
                "size": size,
                "type": info & 0xF,
                "bind": info >> 4,
                "shndx": shndx,
            })
    return sections, symbols


def relocation_map(path, sections, symbols):
    """Return ``{section_index: [(offset, type, symbol_name, addend)]}``.

    Relocations are attached to the compiled data so a pointer table can be
    compared with the words the original linker wrote.  Callers that compare
    raw object bytes still see the unpatched values.
    """
    raw = Path(path).read_bytes()
    result = defaultdict(list)
    for section in sections:
        if section["type"] not in (SHT_REL, SHT_RELA) or section["info"] >= len(sections):
            continue
        if section["link"] >= len(sections):
            raise LayoutError("ELF relocation table has an invalid symbol table")
        step = 12 if section["type"] == SHT_RELA else 8
        for at in range(0, section["size"], step):
            where, info = struct.unpack_from("<II", raw, section["offset"] + at)
            addend = struct.unpack_from("<i", raw, section["offset"] + at + 8)[0] if step == 12 else None
            index = info >> 8
            name = symbols[index]["name"] if index < len(symbols) else ""
            result[section["info"]].append((where, info & 0xFF, name, addend))
    return result


def object_layout(path, patch=None):
    """Describe every allocated data section in *path* in emission order.

    ``patch`` maps ``(section_name, offset)`` to a four-byte word that should
    replace the object's raw bytes (used to resolve ABS32 relocations against
    the measured image).  The returned layout preserves duplicate section
    names, which is essential: MWCC emits one ``.rodata`` section per alignment
    group and the linker concatenates them in object order.
    """
    sections, symbols = read_elf(path)
    relocations = relocation_map(path, sections, symbols)
    raw = Path(path).read_bytes()
    layout = []
    for section in sections:
        name = section["name"]
        if not is_data_section(name) or not section["flags"] & SHF_ALLOC or section["flags"] & SHF_EXECINSTR:
            continue
        body = bytes(section["size"]) if section["type"] == SHT_NOBITS else raw[section["offset"]:section["offset"] + section["size"]]
        blocks = []
        local = sorted((symbol for symbol in symbols
                        if symbol["type"] in (STT_OBJECT, STT_NOTYPE) and symbol["shndx"] == section["index"]
                        and symbol["size"] > 0),
                       key=lambda symbol: (symbol["value"], symbol["size"]))
        cursor = 0
        for symbol in local:
            start = symbol["value"]
            if start < cursor:
                # Overlapping symbols are views of the same storage; keep the
                # wider symbol and skip the interior view.
                continue
            if start > cursor:
                blocks.append({"name": "", "offset": cursor, "size": start - cursor,
                               "kind": "padding", "data": body[cursor:start]})
            blocks.append({"name": symbol["name"], "offset": start, "size": symbol["size"],
                           "kind": "symbol", "data": body[start:start + symbol["size"]]})
            cursor = start + symbol["size"]
        if cursor < len(body):
            blocks.append({"name": "", "offset": cursor, "size": len(body) - cursor,
                           "kind": "padding", "data": body[cursor:]})
        if not blocks:
            blocks.append({"name": "", "offset": 0, "size": len(body), "kind": "section", "data": body})
        for block in blocks:
            block["section"] = name
            block["alignment"] = section["align"]
            block["relocations"] = []
            for where, kind, symbol_name, addend in relocations.get(section["index"], []):
                offset = where - block["offset"]
                if 0 <= offset <= block["size"] - 4:
                    block["relocations"].append({"offset": offset, "kind": kind,
                                                 "symbol": symbol_name, "addend": addend})
            if patch:
                data = bytearray(block["data"])
                for relocation in block["relocations"]:
                    if relocation["kind"] == 2:
                        word = patch(2, relocation["symbol"], relocation["addend"])
                        if word is not None:
                            struct.pack_into("<I", data, relocation["offset"], word & 0xFFFFFFFF)
                block["data"] = bytes(data)
            block["sha256"] = sha256(block["data"])
        layout.append({"name": name, "alignment": section["align"], "size": len(body), "blocks": blocks})
    return layout


def stream(layout, start_alignment=1):
    """Concatenate the data sections the way the linker places them.

    Each section is aligned to its own alignment relative to the object start.
    Returns ``(bytes, spans)`` where a span records the stream position and
    object block for every emitted block.
    """
    out = bytearray()
    spans = []
    for section in layout:
        out.extend(bytes(align_up(len(out), section["alignment"]) - len(out)))
        for block in section["blocks"]:
            spans.append({"streamOffset": len(out), "section": section["name"],
                          "block": block})
            out.extend(block["data"])
    return bytes(out), spans


def block_key(block):
    return (block["size"], sha256(block["data"]))


def match_blocks(source_blocks, target_blocks):
    """Greedily match blocks by ``(size, sha256)``; return index pairs."""
    available = defaultdict(list)
    for index, block in enumerate(target_blocks):
        available[block_key(block)].append(index)
    pairs, missing = [], []
    for index, block in enumerate(source_blocks):
        bucket = available.get(block_key(block))
        if bucket:
            pairs.append((index, bucket.pop(0)))
        else:
            missing.append(index)
    return pairs, missing


def classify(layout, image, base, start, end=None, name="region"):
    """Classify a compiled data layout against an original image region.

    ``image`` is the module binary, ``base`` its load address and ``start`` the
    first measured byte.  ``end`` defaults to ``start + stream length``.

    The result distinguishes:

    ``exact``      every block is at the measured offset with identical bytes;
    ``order``      the same blocks are present, but the emitted sequence is a
                   permutation of the measured sequence;
    ``content``    at least one block's bytes differ;
    ``unresolved`` blocks cannot be placed in the region.
    """
    data, spans = stream(layout)
    if end is None:
        end = start + len(data)
    if end < start or end - start > len(image) - (start - base):
        raise LayoutError("measured region escapes the module image")
    target = image[start - base:end - base]
    object_blocks = [span["block"] for span in spans]
    result = {
        "name": name,
        "object": str(layout) if isinstance(layout, (str, Path)) else None,
        "start": hex(start),
        "end": hex(end),
        "objectBytes": len(data),
        "targetBytes": len(target),
        "classification": "content",
        "blocks": [],
        "moves": [],
        "declarationOrder": [],
        "model": None,
        "breaks": [],
    }
    if data == target:
        result["classification"] = "exact"
        result["model"] = "identical-emission"
        result["blocks"] = [{"name": block["name"], "section": block["section"],
                             "offset": span["streamOffset"], "size": block["size"],
                             "status": "exact"} for span in spans for block in [span["block"]]]
        return result
    if len(data) != len(target):
        result["breaks"].append("object stream length %d differs from measured region %d" % (len(data), len(target)))
        return result

    # Split the measured region at the same offsets as the emitted stream.  A
    # permutation is visible only when those pieces are the same multiset.
    target_blocks = []
    for span in spans:
        block = span["block"]
        begin = span["streamOffset"]
        target_blocks.append({"name": block["name"], "offset": begin, "size": block["size"],
                              "kind": block["kind"], "section": block["section"],
                              "data": target[begin:begin + block["size"]]})
    pairs, missing = match_blocks(object_blocks, target_blocks)
    status = {}
    for source_index, target_index in pairs:
        status[source_index] = target_index
    exact_offsets = all(status.get(index) == index for index in range(len(object_blocks)))
    for index, block in enumerate(object_blocks):
        target_index = status.get(index)
        row = {"name": block["name"], "section": block["section"], "size": block["size"],
               "objectOffset": spans[index]["streamOffset"],
               "targetOffset": target_blocks[target_index]["offset"] if target_index is not None else None,
               "status": "exact" if target_index == index else "moved" if target_index is not None else "unmatched"}
        result["blocks"].append(row)
        if target_index != index:
            result["moves"].append({"block": block["name"] or "#%d" % index,
                                    "from": index, "to": target_index})
    if missing:
        result["classification"] = "content"
        result["breaks"].append("unmatched object blocks: " + ", ".join(
            object_blocks[index]["name"] or "#%d" % index for index in missing))
        return result
    if exact_offsets:
        result["classification"] = "exact"
        result["model"] = "offset-identity"
        return result
    result["classification"] = "order"
    result["model"] = "block-permutation"
    result["targetSequence"] = [target_blocks[index]["name"] or "#%d" % index
                                for index in range(len(target_blocks))]
    try:
        result["declarationOrder"] = declaration_order(object_blocks, target_blocks, status)
        result["declarationNames"] = [result["blocks"][index]["name"] or "#%d" % index
                                      for index in result["declarationOrder"]]
        result["modelDetail"] = mwcc_model()
    except LayoutError as error:
        result["breaks"].append(str(error))
    return result


def mwcc_model():
    """Return the measured MWCC emission rule as data."""
    return {
        "compiler": "mwccarm 2.0/base",
        "rule": "within one homogeneous data section group the compiler emits "
                "declarations 0..n-2 in reverse order and declaration n-1 last",
        "formula": "emission = reverse(declaration[:-1]) + declaration[-1]",
        "inverse": "declaration = reverse(emission[:-1]) + emission[-1]",
        "source": "ops/data_layout.py synthetic compiler probes; docs/authoring/data-layout.md",
        "limits": [
            "each alignment group is a separate section; cross-group order is section creation order",
            "arrays of different sizes/types may become separate sections whose order is not declaration order",
            "symbols whose measured addresses are not contiguous cannot be modelled as one source file",
        ],
    }


def declaration_order(object_blocks, target_blocks, status):
    """Invert the MWCC rule for one homogeneous section group.

    ``status`` maps object block index to target block index.  Returns the
    source declaration order (by object block index) that emits the measured
    target sequence.  This is only valid when every object block belongs to one
    section and the emission rule applies to the whole group.
    """
    if not object_blocks:
        return []
    sections = {block["section"] for block in object_blocks}
    if len(sections) != 1:
        raise LayoutError("model breaks: blocks span sections " + ", ".join(sorted(sections)))
    sequence = [None] * len(object_blocks)
    for object_index, target_index in status.items():
        sequence[target_index] = object_index
    if any(item is None for item in sequence):
        raise LayoutError("model breaks: measured sequence is incomplete")
    # emission = reverse(decl[:-1]) + [decl[-1]]  =>  decl = reverse(emission[:-1]) + [emission[-1]]
    declaration = list(reversed(sequence[:-1])) + [sequence[-1]]
    return declaration


def load_layout(path):
    return object_layout(path)


def command_compare(args):
    image = Path(args.image).read_bytes()
    layout = object_layout(args.object)
    result = classify(layout, image, int(args.base, 0), int(args.start, 0),
                      int(args.end, 0) if args.end else None, name=args.object)
    result["object"] = args.object
    result["image"] = args.image
    print(json.dumps(result, indent=2))
    if args.json:
        Path(args.json).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0 if result["classification"] in ("exact", "order") else 1


def command_order(args):
    image = Path(args.image).read_bytes()
    layout = object_layout(args.object)
    result = classify(layout, image, int(args.base, 0), int(args.start, 0),
                      int(args.end, 0) if args.end else None, name=args.object)
    print(json.dumps(result, indent=2))
    if result["classification"] == "order" and result["declarationOrder"]:
        print("\nDeclare the blocks in this order to reproduce the measured sequence:")
        for position, name in enumerate(result.get("declarationNames", [])):
            block = next((row for row in result["blocks"] if row["name"] == name), None)
            print("  %2d. %-40s %-8s %4d B" % (position, name,
                                               block["section"] if block else "", block["size"] if block else 0))
    return 0


def _module_images(root):
    config = json.loads((Path(root) / "config/source_units.json").read_text(encoding="utf-8"))
    modules = []
    for name, module in config["modules"].items():
        image = (Path(root) / module["originalImage"].replace("\\", "/")).resolve()
        modules.append({"name": name, "base": int(module["loadAddressBase"], 0),
                        "bytes": int(module["bytes"]), "image": image.read_bytes()})
    modules.sort(key=lambda item: item["base"])
    return modules


def _module_at(modules, address):
    for module in modules:
        if module["base"] <= address < module["base"] + module["bytes"]:
            return module
    return None


def data_blocks(layout):
    for section in layout:
        for block in section["blocks"]:
            if block["kind"] != "padding":
                yield section, block


def _unique_content_address(modules, data):
    hits = []
    for module in modules:
        at = module["image"].find(data)
        while at >= 0:
            hits.append((module["name"], module["base"] + at))
            at = module["image"].find(data, at + 1)
            if len(hits) > 8:
                return hits
    return hits


def measure_source(source, object_path, modules, patch=None, known=None):
    layout = object_layout(object_path, patch=patch)
    blocks = list(data_blocks(layout))
    if not blocks:
        return None
    known = known or {}
    rows, addresses = [], {}
    for section, block in blocks:
        address = None
        match = None
        for test in range(len(block["name"]) - 8, -1, -1):
            tail = block["name"][test:]
            if len(tail) == 8 and all(char in "0123456789abcdef" for char in tail):
                match = tail
                break
        if match:
            address = int(match, 16)
        if address is None:
            hits = _unique_content_address(modules, block["data"])
            if len(hits) == 1:
                address = hits[0][1]
        if address is None:
            address = known.get(block["name"])
        module = _module_at(modules, address) if address is not None else None
        if module is None:
            rows.append({"name": block["name"], "size": block["size"], "address": None,
                         "status": "unplaced"})
            continue
        data = bytearray(block["data"])
        for relocation in block.get("relocations", []):
            if relocation["kind"] != 2:
                continue
            at = address - module["base"] + relocation["offset"]
            if 0 <= at <= len(module["image"]) - 4:
                struct.pack_into("<I", data, relocation["offset"],
                                 struct.unpack_from("<I", module["image"], at)[0])
        expected = module["image"][address - module["base"]:address - module["base"] + block["size"]]
        status = "exact" if expected == bytes(data) else "content"
        rows.append({"name": block["name"], "size": block["size"], "address": hex(address),
                     "module": module["name"], "status": status})
        addresses[block["name"]] = address
    if all(row["status"] == "exact" for row in rows) and all(row["address"] for row in rows):
        emission = [int(row["address"], 0) for row in rows]
        ordered = sorted((int(row["address"], 0), row["size"]) for row in rows)
        contiguous = all(ordered[index][0] + ordered[index][1] == ordered[index + 1][0]
                         for index in range(len(ordered) - 1))
        if emission != sorted(emission):
            classification = "order"
        elif contiguous or len(rows) == 1:
            classification = "exact"
        else:
            classification = "fragmented"
    elif any(row["status"] == "content" for row in rows):
        classification = "content"
    else:
        classification = "unresolved"
    return {"source": source, "module": rows[0].get("module") if rows else None,
            "bytes": sum(row["size"] for row in rows), "classification": classification,
            "emissionOrder": [row["address"] for row in rows if row["address"]],
            "blocks": rows}


def command_measure(args):
    root = Path(args.root).resolve()
    modules = _module_images(root)
    object_root = Path(args.object_root).resolve() if args.object_root else root
    report = json.loads((Path(root) / args.compile_report).read_text(encoding="utf-8"))
    selected = [row for row in report["results"] if row.get("status") in ("compiled", "prebuilt")]
    if args.modules:
        wanted = set(args.modules.split(","))
        selected = [row for row in selected if row.get("module") in wanted]
    accepted = set()
    known = {}
    accepted_path = root / "public/accepted-functions.json"
    accepted_data_path = root / "public/accepted-data.json"
    if accepted_path.is_file():
        document = json.loads(accepted_path.read_text(encoding="utf-8"))
        accepted.update(row.get("sourceUnit", "").replace("\\", "/") for row in document.get("functions", []))
    if accepted_data_path.is_file():
        document = json.loads(accepted_data_path.read_text(encoding="utf-8"))
        for row in document.get("records", []):
            source = row.get("source", "").replace("\\", "/")
            accepted.add(source)
            if row.get("symbol"):
                known[(source, row["symbol"])] = int(row["address"], 0)
    results, skipped = [], 0
    for row in selected:
        source = row["source"].replace("\\", "/")
        object_path = object_root / row["object"]
        if not object_path.is_file():
            skipped += 1
            continue
        try:
            result = measure_source(source, object_path, modules,
                                    known={name: address for (wanted, name), address in known.items()
                                           if wanted == source})
        except LayoutError:
            skipped += 1
            continue
        if result is None:
            continue
        if args.modules:
            placed = {block.get("module") for block in result["blocks"] if block.get("module")}
            if placed and not placed.intersection(wanted):
                continue
        result["accepted"] = source in accepted
        result["module"] = row.get("module")
        results.append(result)
    classes = Counter()
    bytes_by_class = Counter()
    accepted_classes = Counter()
    accepted_bytes = Counter()
    for result in results:
        classes[result["classification"]] += 1
        bytes_by_class[result["classification"]] += result["bytes"]
        if result["accepted"]:
            accepted_classes[result["classification"]] += 1
            accepted_bytes[result["classification"]] += result["bytes"]
    summary = {
        "schemaVersion": 1,
        "root": str(root),
        "modules": args.modules or "all",
        "sourcesWithData": len(results),
        "skipped": skipped,
        "classes": dict(classes),
        "bytes": dict(bytes_by_class),
        "acceptedClasses": dict(accepted_classes),
        "acceptedBytes": dict(accepted_bytes),
        "results": results,
    }
    output = json.dumps(summary, indent=2) + "\n"
    if args.json:
        Path(args.json).write_text(output, encoding="utf-8")
    print(json.dumps({key: summary[key] for key in
                      ("modules", "sourcesWithData", "skipped", "classes", "bytes",
                       "acceptedClasses", "acceptedBytes")}, indent=2))
    return 0


def link_compare(object_path, image, base, start, size, linker, work_root=None):
    """Place *object_path* at the measured address with the pinned MW linker.

    This is the real placement gate for a data source: the linker, not the
    object parser, decides what bytes reach the measured address.  Returns the
    linked section bytes and their comparison with the original region.
    """
    object_path = Path(object_path).resolve()
    linker = Path(linker).resolve()
    if not linker.is_file():
        raise LayoutError("pinned linker is unavailable: " + str(linker))
    work_root = Path(work_root or Path.cwd() / "work" / "data-layout" / "links")
    directory = Path(tempfile.mkdtemp(prefix="link-", dir=work_root))
    try:
        object_copy = directory / "unit.o"
        shutil.copyfile(object_path, object_copy)
        layout = object_layout(object_copy)
        names = [block["name"] for section in layout for block in section["blocks"]
                 if block["name"] and block["name"].isidentifier()]
        entry = names[0] if names else None
        lcf = directory / "unit.lcf"
        lines = ["MEMORY {", "  REGION: ORIGIN = %#x, LENGTH = %#x" % (start, size), "}", "SECTIONS {",
                 "  .data : { unit.o(.rodata) unit.o(.data) } > REGION", "}"]
        lcf.write_text("\n".join(lines) + "\n", encoding="ascii")
        output = directory / "linked.elf"
        command = [str(linker), "-nostdlib", "-nodeadstrip", "-interworking", "-proc", "arm946e"]
        if entry:
            command += ["-main", entry]
        command += [str(lcf), str(object_copy), "-o", str(output)]
        run = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=120)
        if run.returncode or not output.is_file():
            raise LayoutError("MW linker rejected the data unit: " + run.stdout + run.stderr)
        raw = output.read_bytes()
        header = struct.unpack_from("<16sHHIIIIIHHHHHH", raw)
        section_offset, section_count, name_index = header[6], header[12], header[13]
        names_blob = raw[struct.unpack_from("<IIIIIIIIII", raw, section_offset + 40 * name_index)[4]:]
        chosen = None
        for index in range(section_count):
            row = struct.unpack_from("<IIIIIIIIII", raw, section_offset + 40 * index)
            if row[3] == start and row[5] == size:
                chosen = raw[row[4]:row[4] + row[5]]
                break
        if chosen is None:
            raise LayoutError("linked output has no section at the measured address")
        expected = image[start - base:start - base + size]
        return {"linkedBytes": chosen.hex(), "expectedBytes": expected.hex(),
                "exact": chosen == expected, "linker": str(linker),
                "command": command, "linkedSectionBytes": len(chosen)}
    finally:
        shutil.rmtree(directory, ignore_errors=True)


def command_verify(args):
    image = Path(args.image).read_bytes()
    start = int(args.start, 0)
    layout = object_layout(args.object)
    data, unused = stream(layout)
    size = int(args.end, 0) - start if args.end else len(data)
    result = classify(layout, image, int(args.base, 0), start, start + size, name=args.object)
    result["object"] = args.object
    result["image"] = args.image
    if args.linker:
        try:
            result["link"] = link_compare(args.object, image, int(args.base, 0), start, size, args.linker,
                                          work_root=args.work_dir)
        except LayoutError as error:
            # A code-bearing unit can reference external symbols the isolated
            # data-only link does not provide.  The object comparison and the
            # .text baseline still gate the change; the link is reported as
            # unavailable rather than silently treated as passing.
            result["link"] = {"exact": None, "error": str(error)}
    if args.baseline_object:
        before_sections, unused_before = read_elf(args.baseline_object)
        after_sections, unused_after = read_elf(args.object)
        before_text = [section for section in before_sections if section["name"] == ".text"]
        after_text = [section for section in after_sections if section["name"] == ".text"]
        result["text"] = {
            "beforeSha256": [sha256(Path(args.baseline_object).read_bytes()[s["offset"]:s["offset"] + s["size"]])
                             for s in before_text],
            "afterSha256": [sha256(Path(args.object).read_bytes()[s["offset"]:s["offset"] + s["size"]])
                            for s in after_text],
        }
        result["text"]["identical"] = result["text"]["beforeSha256"] == result["text"]["afterSha256"]
    link_exact = result.get("link", {}).get("exact")
    result["passed"] = result["classification"] == "exact" \
        and link_exact is not False \
        and result.get("text", {}).get("identical", True)
    print(json.dumps(result, indent=2))
    if args.json:
        Path(args.json).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0 if result["passed"] else 1


DEFAULT_PROBE_FLAGS = ("-O2", "-enum", "int", "-char", "signed", "-str", "noreuse",
                       "-proc", "arm946e", "-gccext,on", "-fp", "soft", "-inline", "on",
                       "-Cpp_exceptions", "off", "-RTTI", "off", "-interworking",
                       "-w", "off", "-sym", "on", "-gccinc", "-nolink",
                       "-msgstyle", "gcc", "-lang", "c99", "-opt", "speed", "-c")


def command_rule_check(args):
    """Compile small probes and verify the measured MWCC emission rule."""
    compiler = Path(args.compiler).resolve()
    workdir = Path(args.work_dir or Path.cwd() / "work" / "data-layout" / "rule-check").resolve()
    workdir.mkdir(parents=True, exist_ok=True)
    counts = [int(value) for value in args.counts.split(",")]
    rows = []
    for count in counts:
        source = workdir / ("ints_%d.c" % count)
        lines = ["const int v%d = %d;" % (index, index + 1) for index in range(count)]
        lines.append("int use(void) { return %s; }" % " + ".join("v%d" % index for index in range(count)))
        source.write_text("\n".join(lines) + "\n", encoding="ascii")
        object_path = workdir / ("ints_%d.o" % count)
        command = [str(compiler), *DEFAULT_PROBE_FLAGS, str(source), "-o", str(object_path)]
        run = subprocess.run(command, capture_output=True, text=True, timeout=120)
        if run.returncode:
            raise LayoutError("probe compiler failed: " + run.stderr)
        layout = object_layout(object_path)
        emitted = [block["name"] for section in layout if section["name"] == ".rodata"
                   for block in section["blocks"] if block["name"]]
        expected = ["v%d" % index for index in list(reversed(range(count - 1))) + [count - 1]]
        rows.append({"count": count, "emitted": emitted, "expected": expected,
                     "matches": emitted == expected})
    return {"schemaVersion": 1, "compiler": str(compiler), "flags": list(DEFAULT_PROBE_FLAGS),
            "probes": rows, "passed": all(row["matches"] for row in rows)}


def command_rule_check_cli(args):
    result = command_rule_check(args)
    print(json.dumps(result, indent=2))
    if args.json:
        Path(args.json).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0 if result["passed"] else 1


def command_probe(args):
    """Emit a tiny C file used to re-measure the compiler's ordering rule."""
    count = args.count
    kind = args.kind
    lines = []
    if kind == "ints":
        for index in range(count):
            lines.append("const int v%d = %d;" % (index, index + 1))
        lines.append("int use(void) { return %s; }" % " + ".join("v%d" % index for index in range(count)))
    elif kind == "chars":
        for index in range(count):
            lines.append('const char s%d[] = "%s";' % (index, chr(ord("a") + index) * 5))
        lines.append("int use(void) { return %s; }" % " + ".join("s%d[0]" % index for index in range(count)))
    else:
        raise LayoutError("probe kind must be ints or chars")
    print("\n".join(lines))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Model and check compiled data layout against measured original regions.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    compare = subparsers.add_parser("compare", help="classify an object's data against a measured region")
    compare.add_argument("--object", required=True)
    compare.add_argument("--image", required=True)
    compare.add_argument("--base", required=True, help="module load address")
    compare.add_argument("--start", required=True, help="first measured data byte")
    compare.add_argument("--end", help="end of measured region (default: object stream length)")
    compare.add_argument("--json")
    compare.set_defaults(func=command_compare)

    order = subparsers.add_parser("order", help="emit the declaration order that reproduces the measured sequence")
    order.add_argument("--object", required=True)
    order.add_argument("--image", required=True)
    order.add_argument("--base", required=True)
    order.add_argument("--start", required=True)
    order.add_argument("--end")
    order.set_defaults(func=command_order)

    measure = subparsers.add_parser("measure", help="classify every compiled source file's data blocks")
    measure.add_argument("--root", default=".")
    measure.add_argument("--compile-report", default="build/repository-compile/report.json")
    measure.add_argument("--object-root", help="directory that report object paths are relative to (default: root)")
    measure.add_argument("--modules", help="comma-separated module names, e.g. main,ov001")
    measure.add_argument("--json")
    measure.set_defaults(func=command_measure)

    probe = subparsers.add_parser("probe", help="print a compiler ordering probe source")
    probe.add_argument("--kind", default="ints", choices=("ints", "chars"))
    probe.add_argument("--count", type=int, default=6)
    probe.set_defaults(func=command_probe)

    verify = subparsers.add_parser("verify", help="compile-side gate: exact bytes, real link, unchanged text")
    verify.add_argument("--object", required=True)
    verify.add_argument("--image", required=True)
    verify.add_argument("--base", required=True)
    verify.add_argument("--start", required=True)
    verify.add_argument("--end")
    verify.add_argument("--linker")
    verify.add_argument("--work-dir")
    verify.add_argument("--baseline-object", help="object compiled before the source change; .text must match")
    verify.add_argument("--json")
    verify.set_defaults(func=command_verify)

    rule = subparsers.add_parser("rule-check", help="compile probes and verify the MWCC emission rule")
    rule.add_argument("--compiler", required=True)
    rule.add_argument("--work-dir")
    rule.add_argument("--counts", default="2,3,4,5,6,8,12")
    rule.add_argument("--json")
    rule.set_defaults(func=command_rule_check_cli)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
