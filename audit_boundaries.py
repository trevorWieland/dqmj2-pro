import bisect
import hashlib
import json
import re
from project import ROOT, configuration, native_dependencies, now, read_json, sha256, write_json


def accepted_functions():
    groups = {}
    for line in (ROOT / "ledger/functions.jsonl").read_text().splitlines():
        item = json.loads(line)
        if item["states"]["functionMatched"]:
            groups.setdefault(item["module"], []).append(item)
    return {module: sorted(items, key=lambda item: int(item["address"], 0)) for module, items in groups.items()}


def containing(groups, starts, module, address):
    values = groups.get(module, [])
    index = bisect.bisect_right(starts.get(module, []), address) - 1
    if index >= 0:
        item = values[index]
        if address < int(item["address"], 0) + item["bytes"]:
            return item
    return None


def products(modules):
    host = {"main": "ARM9", "itcm": "ITCM", "dtcm": "DTCM"}
    host.update({f"ov{index:03d}": f"OV{index:03d}" for index in range(8)})
    yield ROOT / "build/link-work/linked.elf", {section: name for name, section in host.items()}
    for module in modules:
        if module.get("program"):
            continue
        if module["processor"] == "arm7":
            yield ROOT / "build/arm7-link" / module["name"] / "linked.elf", {".image": module["name"], "ARM7": module["name"]}
    for processor in ("arm9", "arm7"):
        selected = [module for module in modules if module.get("program") and module["processor"] == processor]
        yield ROOT / "build/utility-link" / (processor + "-linked.elf"), {"MODULE" + str(index): module["name"] for index, module in enumerate(selected)}


def main():
    config = configuration()
    native_dependencies(config)
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
    from capstone.arm import ARM_OP_IMM
    from elftools.elf.elffile import ELFFile
    manifest = read_json(ROOT / "manifest.json")
    modules = {item["name"]: item for item in manifest["modules"]}
    groups = accepted_functions()
    starts = {name: [int(item["address"], 0) for item in items] for name, items in groups.items()}
    engines = {"arm": Cs(CS_ARCH_ARM, CS_MODE_ARM), "thumb": Cs(CS_ARCH_ARM, CS_MODE_THUMB)}
    for engine in engines.values():
        engine.detail = True
    report = {"schemaVersion": 1, "createdUtc": now(), "romSha256": config["romSha256"], "functionLedgerSha256": sha256(ROOT / "ledger/functions.jsonl"), "products": [], "modules": [], "externalInteriorBranches": [], "ambiguousOverlayBranches": [], "modeConflicts": [], "sourceReconstructionComplete": False}
    report["matchedFunctionCount"] = sum(len(items) for items in groups.values())
    for path, sections in products(list(modules.values())):
        if not path.is_file():
            raise ValueError("Current linked product missing: " + str(path))
        with path.open("rb") as stream:
            elf = ELFFile(stream)
            mapping = {}
            for symbol in elf.get_section_by_name(".symtab").iter_symbols():
                match = re.fullmatch(r"\$([atd])(?:\..*)?", symbol.name)
                if not match or not isinstance(symbol["st_shndx"], int):
                    continue
                section = elf.get_section(symbol["st_shndx"]).name
                if section in sections:
                    mapping.setdefault(sections[section], {}).setdefault(symbol["st_value"] & ~1, set()).add({"a": "arm", "t": "thumb", "d": "data"}[match[1]])
            report["products"].append({"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path), "sections": sections})
        for name, values in mapping.items():
            module = modules[name]
            binary = ROOT / module["binary"]
            body = binary.read_bytes()
            if hashlib.sha256(body).hexdigest() != module["sha256"]:
                raise ValueError("Mapped executable input changed")
            base = int(module["base"], 0)
            end = base + len(body)
            positions = sorted(address for address in values if base <= address < end)
            stats = {"module": name, "inputModuleSha256": module["sha256"], "mappedCodeBytes": 0, "mappedDataBytes": 0, "decodedInstructions": 0, "directBranches": 0, "mappingUndecodedBytes": 0, "unmappedPrefixBytes": positions[0] - base if positions else len(body)}
            for address, stop in zip(positions, positions[1:] + [end]):
                modes = values[address]
                if len(modes) != 1:
                    report["modeConflicts"].append({"module": name, "address": hex(address), "end": hex(stop), "modes": sorted(modes)})
                    continue
                mode = next(iter(modes))
                if mode == "data":
                    stats["mappedDataBytes"] += stop - address
                    continue
                stats["mappedCodeBytes"] += stop - address
                decoded = 0
                for instruction in engines[mode].disasm(body[address - base:stop - base], address):
                    decoded += instruction.size
                    stats["decodedInstructions"] += 1
                    if not instruction.mnemonic.startswith("b") or instruction.mnemonic in ("bic", "bics", "bkpt") or not instruction.operands or instruction.operands[0].type != ARM_OP_IMM:
                        continue
                    target = instruction.operands[0].imm & 0xFFFFFFFF
                    stats["directBranches"] += 1
                    candidates = [item for item in modules.values() if item.get("program") == module.get("program") and item["processor"] == module["processor"] and int(item["base"], 0) <= target & ~1 < int(item["base"], 0) + item["bytes"]]
                    if len(candidates) > 1:
                        if name.startswith("ov") and any(item["name"] == name for item in candidates):
                            candidates = [module]
                        else:
                            report["ambiguousOverlayBranches"].append({"sourceModule": name, "address": hex(instruction.address), "mode": mode, "target": hex(target), "candidateModules": [item["name"] for item in candidates]})
                            continue
                    if len(candidates) != 1:
                        continue
                    destination = candidates[0]["name"]
                    accepted = containing(groups, starts, destination, target & ~1)
                    if not accepted or target & ~1 == int(accepted["address"], 0):
                        continue
                    origin = containing(groups, starts, name, instruction.address)
                    if origin and origin["id"] == accepted["id"]:
                        continue
                    report["externalInteriorBranches"].append({"sourceModule": name, "address": hex(instruction.address), "mode": mode, "mnemonic": instruction.mnemonic, "targetModule": destination, "target": hex(target), "targetFunctionId": accepted["id"], "targetFunctionSource": accepted["sourceUnit"], "targetOffset": (target & ~1) - int(accepted["address"], 0), "sourceFunctionId": origin["id"] if origin else None, "reconciliation": "pending shared-tail, alternate-entry, mapping and boundary analysis"})
                stats["mappingUndecodedBytes"] += stop - address - decoded
            report["modules"].append(stats)
    report["limitations"] = ["ELF mapping symbols from verified source and heuristic original-object delinking guide decoding; this does not prove complete code/data discovery", "Overlapping overlays are never resolved by numeric address alone from the main program", "Within-overlay branches assume that the originating overlay remains loaded", "Computed branches and indirect call targets require separate dataflow and runtime analysis", "Incoming interior edges require reconciliation before a function boundary can be declared proven", "This audit grants no additional source or ordinary function credit"]
    report["modulesWithoutMappingSymbols"] = sorted(set(modules) - {item["module"] for item in report["modules"]})
    write_json(ROOT / "evidence/verification/boundaries.json", report)
    print({"mappedModules": len(report["modules"]), "interiorEdges": len(report["externalInteriorBranches"]), "ambiguousOverlayEdges": len(report["ambiguousOverlayBranches"]), "modeConflicts": len(report["modeConflicts"])})


if __name__ == "__main__":
    main()
