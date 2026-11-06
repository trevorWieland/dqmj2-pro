import hashlib
import re
import struct
from collections import defaultdict, deque
from pathlib import Path

from link_runtime_unit import measured_module
from project import ROOT, configuration, now, sha256, write_json

WORK = ROOT / "work/ov000-recovery/20261029/birth-rng/static"
REPORT = ROOT / "evidence/application/ov000-birth-context-20261029.json"
APP = ROOT.parent / "monster-fieldnotes"
SELECTION = {
    "main": [
        0x02026EC0, 0x0203D25C, 0x0203D294, 0x0203D2DC, 0x0203D2EC,
        0x02043718, 0x02043844, 0x020443EC, 0x02044508, 0x02044564,
        0x0204457C, 0x020655E8, 0x020655F8, 0x02065608, 0x02065620,
        0x02063F78, 0x02063F88, 0x02065210, 0x02065D88, 0x02044D60,
        0x0200F3E0, 0x0200F48C, 0x0200F370, 0x0200F418, 0x0200FBC8,
        0x0200FC5C, 0x0200FC74, 0x020626D0, 0x0206271C, 0x0203D128,
    ],
    "ov000": [
        0x0221B070, 0x0221B624, 0x0221F4DC, 0x02220680, 0x02220714,
        0x02220778, 0x02220AFC, 0x022212B8, 0x022212F0, 0x02221344,
        0x02221358, 0x0222136C, 0x02223F34, 0x02224420, 0x02227F94,
        0x022280FC, 0x02228170, 0x02228E54, 0x02228FB8, 0x02228FDC,
        0x0222900C, 0x02229100, 0x0222976C,
        0x0222985C, 0x022298EC, 0x02229ED4,
    ],
    "ov001": [0x021DE598, 0x0220225C, 0x021FB1DC, 0x021FB214, 0x022095F4],
    "ov006": [0x021D9F5C],
    "itcm": [0x01FFA8B8, 0x01FFA8C8],
}


def config_path(module, name):
    if module == "main":
        return ROOT / "config/arm9" / name
    if module == "itcm":
        return ROOT / "config/arm9/itcm" / name
    return ROOT / "config/arm9/overlays" / module / name


def functions(module):
    text = config_path(module, "symbols.txt").read_text()
    return [{"name": name, "mode": mode, "bytes": int(size, 16),
             "address": int(address, 16)}
            for name, mode, size, address in re.findall(
                r"^(\S+) kind:function\((arm|thumb),size=0x([0-9a-f]+)\) "
                r"addr:0x([0-9a-f]+)$", text, re.M)]


def references(module):
    return [{"from": int(start, 16), "kind": kind, "to": int(end, 16),
             "targetModule": target}
            for start, kind, end, target in re.findall(
                r"from:0x([0-9a-f]+) kind:(\S+) to:0x([0-9a-f]+) module:(\S+)",
                config_path(module, "relocs.txt").read_text())]


def assembly(module):
    text = "\n".join(path.read_text() for path in sorted(
        (ROOT / "asm").glob(f"_dsd_gap@{module}_*.s")))
    return {name: ".text\n.global " + name + "\n" + "\n".join(
        line.split(";")[0].rstrip() for line in body.splitlines()) + "\n"
        for name, body in re.findall(
            r"    arm_func_start (\w+)\n(.*?)    arm_func_end \1", text, re.S)}


def closures(modules, ledgers, relocs, binaries):
    graph = defaultdict(list)
    names = {module: assembly(module) for module in modules}
    by_entry = {(module, row["address"]): row for module, rows in ledgers.items()
                for row in rows}
    target_modules = {"main": "main", "itcm": "itcm", "overlay(0)": "ov000",
                      "overlay(1)": "ov001", "overlay(6)": "ov006"}
    for module, references_list in relocs.items():
        sorted_functions = sorted(ledgers[module], key=lambda row: row["address"])
        for reference in references_list:
            if reference["kind"] not in ("arm_call", "thumb_call", "arm_branch", "thumb_branch"):
                continue
            owner = next((row for row in reversed(sorted_functions)
                          if row["address"] <= reference["from"]), None)
            if owner is None or reference["from"] >= owner["address"] + owner["bytes"]:
                continue
            target = target_modules.get(reference["targetModule"])
            graph[(module, owner["address"])].append((target, reference))
    results = []
    for root in [("ov000", 0x02229100), ("ov000", 0x0222900C),
                 ("ov000", 0x022298EC), ("main", 0x0206271C)]:
        pending = deque([(root, [])])
        visited, unresolved, indirect, rng_paths = set(), [], [], []
        while pending:
            node, path = pending.popleft()
            if node in visited:
                continue
            visited.add(node)
            if node == ("main", 0x0203D294):
                rng_paths.append(path)
            entry = by_entry.get(node)
            if entry is None:
                unresolved.append({"module": node[0], "address": hex(node[1])})
                continue
            body = names[node[0]].get(entry["name"], "")
            uncertain = re.findall(r"^\s*(?:blx|bx)\s+(?!lr\b)(\w+)", body, re.M)
            if uncertain:
                indirect.append({"module": node[0], "address": hex(node[1]),
                                 "registerTransfers": uncertain})
            for target, reference in graph[node]:
                edge = {"callerModule": node[0], "caller": hex(node[1]), **reference}
                if target is None:
                    unresolved.append(edge)
                else:
                    pending.append(((target, reference["to"]), path + [edge]))
        nodes = []
        for module, address in sorted(visited):
            entry = by_entry.get((module, address))
            if entry is None:
                continue
            offset = address - int(modules[module]["base"], 0)
            nodes.append({"module": module, **entry, "nativeSpanSha256": hashlib.sha256(
                binaries[module][offset:offset + entry["bytes"]]).hexdigest()})
        results.append({"rootModule": root[0], "rootAddress": hex(root[1]),
                        "resolvedNativeNodes": nodes, "unresolvedCalls": unresolved,
                        "potentialRegisterTransfers": indirect, "firstRngPaths": rng_paths,
                        "scope": "Configured direct call/branch closure; not dynamic path feasibility"})
    return results


def run():
    WORK.mkdir(parents=True, exist_ok=True)
    modules, ledgers, relocs, binaries = {}, {}, {}, {}
    entries = []
    for module, addresses in SELECTION.items():
        metadata, binary, unused = measured_module(module)
        modules[module] = {key: metadata[key] for key in
                           ("name", "base", "binary", "bytes", "sha256")}
        modules[module]["symbolsSha256"] = sha256(config_path(module, "symbols.txt"))
        modules[module]["relocationsSha256"] = sha256(config_path(module, "relocs.txt"))
        binaries[module] = binary
        ledgers[module] = functions(module)
        relocs[module] = references(module)
        disassembled = assembly(module)
        for address in addresses:
            entry = next(row for row in ledgers[module] if row["address"] == address)
            offset = address - int(metadata["base"], 0)
            target = WORK / (module + "-" + f"{address:08x}" + ".s")
            if entry["name"] not in disassembled:
                raise ValueError("Selected ARM function lacks qualified generated disassembly")
            target.write_text(disassembled[entry["name"]])
            entries.append({
                **entry,
                "processor": "arm9",
                "module": module,
                "romSha256": configuration()["romSha256"],
                "moduleSha256": metadata["sha256"],
                "nativeSpanSha256": hashlib.sha256(
                    binary[offset:offset + entry["bytes"]]).hexdigest(),
                "generatedAssembly": str(target.relative_to(ROOT)),
                "generatedAssemblySha256": sha256(target),
                "boundaryConfidence": "Configured ds-decomp span; no new boundary acceptance",
                "callsAndReferences": [row for row in relocs[module]
                    if address <= row["from"] < address + entry["bytes"]],
            })
    incoming = {}
    for target_module, address in [
        ("main", 0x0203D25C), ("main", 0x0203D2DC), ("main", 0x0203D2EC),
        ("main", 0x02065608), ("ov000", 0x0222900C), ("ov000", 0x02229100),
    ]:
        target_name = "main" if target_module == "main" else "overlay(0)"
        rows = []
        for module in SELECTION:
            for reference in relocs[module]:
                if reference["to"] != address or reference["targetModule"] != target_name:
                    continue
                if reference["kind"] not in ("arm_call", "thumb_call"):
                    continue
                owner = next((row for row in ledgers[module]
                              if row["address"] <= reference["from"]
                              < row["address"] + row["bytes"]), None)
                if owner is None or owner["mode"] != "arm":
                    raise ValueError("This bounded incoming-call decoder requires an ARM owner")
                offset = reference["from"] - int(modules[module]["base"], 0)
                instruction = int.from_bytes(binaries[module][offset:offset + 4], "little")
                if instruction >> 28 == 15 or (instruction >> 24) & 15 != 11:
                    raise ValueError("Selected incoming ARM call is not ordinary native BL")
                displacement = instruction & 0xFFFFFF
                if displacement & 0x800000:
                    displacement -= 0x1000000
                encoded_target = reference["from"] + 8 + displacement * 4
                if encoded_target != address:
                    raise ValueError("Native BL target differs from configured call reference")
                rows.append({"callerModule": module, **reference, "configuredOwner": owner,
                             "nativeInstruction": hex(instruction), "encodedTarget": hex(encoded_target),
                             "encodedTargetMode": "arm", "nativeBranchValidated": True})
        incoming[f"{target_module}/{address:08x}"] = rows
    app_paths = [
        "src/adapters/j2p-battle/constructed.py", "src/adapters/j2p-battle/recruitment.py",
        "src/adapters/j2p-battle/runtime.py", "src/adapters/j2p-synthesis/recruitment.ts",
        "src/adapters/j2p-synthesis/eligibility.ts", "src/adapters/j2p-synthesis/monetary.ts",
    ]
    data_ranges = []
    for module, address, length, format_name in [
        ("ov000", 0x0222FFBC, 24, "six little-endian signed32 fee entries"),
        ("ov001", 0x0222E040, 4, "four unsigned8 extra-skill thresholds"),
    ]:
        offset = address - int(modules[module]["base"], 0)
        data = binaries[module][offset:offset + length]
        values = list(struct.unpack("<6i", data)) if length == 24 else list(data)
        data_ranges.append({"processor": "arm9", "module": module, "mode": "data",
                            "address": hex(address), "bytes": length, "format": format_name,
                            "sha256": hashlib.sha256(data).hexdigest(), "values": values})
    report = {
        "schemaVersion": 1,
        "createdUtc": now(),
        "romSha256": configuration()["romSha256"],
        "evidenceClass": "Native static caller/context analysis with separate bounded execution proof",
        "generatedDisassemblyIsSourceCredit": False,
        "modules": modules,
        "entries": entries,
        "incoming": incoming,
        "staticDirectCallClosures": closures(modules, ledgers, relocs, binaries),
        "nativeDataRanges": data_ranges,
        "readOnlyApplicationSources": [{"path": str(APP / path), "sha256": sha256(APP / path)}
                                       for path in app_paths],
        "boundedExecutionReport": "evidence/application/ov000-birth-rng-20261029.json",
        "boundedExecutionReportSha256": sha256(ROOT / "evidence/application/ov000-birth-rng-20261029.json"),
        "reproduction": "python trace_ov000_birth_context_20261029.py",
        "generatorSha256": sha256(Path(__file__)),
        "limitations": [
            "Static call presence does not establish every dynamic path or indirect caller",
            "Full RTC initialization, recruitment and birth allocation were not executed by this tracer",
            "Seed arguments in disposable native fixtures are hypothetical state",
            "No complete proof of RNG save serialization or absence of indirect copies",
            "Native item field2A values are measured; display item names are not revalidated",
        ],
    }
    write_json(REPORT, report)
    print(str(REPORT.relative_to(ROOT)))


if __name__ == "__main__":
    run()
