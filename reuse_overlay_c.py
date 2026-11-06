import argparse
import json
import random
import re
import struct
from pathlib import Path
import match_runtime as compiler
from project import ROOT, configuration, now, read_json, sha256, verify_inputs, write_json


def binding_scope(module, target):
    modules = read_json(ROOT / "provenance/seed-manifest.json")["modules"]
    choices = [item["name"] for item in modules if int(item["base"], 0) <= target & ~1 < int(item["base"], 0) + item["bytes"]]
    return module if module in choices else choices[0] if len(choices) == 1 else None


def source_bindings(origin, spec, payload, text):
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
    from capstone.arm import ARM_OP_IMM
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if spec["mode"] == "thumb" else CS_MODE_ARM)
    decoder.detail = True
    rename = {origin["name"]: spec["name"]}
    bindings = {}
    for relocation in origin.get("relocations", []):
        offset, kind = relocation["offset"], relocation["type"]
        addend = relocation.get("addend", 0)
        old = relocation["symbol"]
        if kind == 2:
            target = (struct.unpack_from("<I", payload, offset)[0] - addend) & 0xFFFFFFFF
            role = "function" if old.startswith(("native_fn_", "func_")) or re.search(r"\b" + re.escape(old) + r"\s*\(", text) else "data"
            mode = ("thumb" if target & 1 else "arm") if role == "function" else "data"
        elif kind in (1, 10, 28, 29):
            instruction = next(decoder.disasm(payload[offset:offset + 4], spec["address"] + offset), None)
            if not instruction or not instruction.operands or instruction.operands[0].type != ARM_OP_IMM or not (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)):
                return None
            if instruction.mnemonic == "blx":
                return None
            target = (instruction.operands[0].imm - addend - (4 if spec["mode"] == "thumb" else 8)) & 0xFFFFFFFF
            role, mode = "function", spec["mode"]
        else:
            return None
        scope = binding_scope(spec["module"], target)
        if role == "function" and scope is None:
            return None
        prefix = "native_fn" if role == "function" else "native_data"
        label = f"{prefix}_{spec['module']}_{target:08x}"
        if old in rename and rename[old] != label:
            return None
        rename[old] = label
        bindings[label] = {"processor": "arm9", "module": scope, "address": hex(target), "mode": mode, "kind": role, "moduleScopeProven": scope in ("main", "itcm") or role == "function" and scope == spec["module"], "scopeLimitation": "Overlay call context follows the originating loaded overlay; data ownership and indirect runtime targets need separate analysis"}
    return rename, bindings


def call_targets(entry, bindings=None):
    bindings = bindings or entry.get("qualifiedDependencies", {})
    targets = {}
    first = int(entry["address"], 0)
    for relocation in entry["relocations"]:
        target = int(relocation["target"], 0)
        binding = bindings.get(relocation["symbol"], {})
        direct = relocation["type"] in (1, 10, 28, 29)
        function_pointer = relocation["type"] == 2 and relocation.get("addend", 0) == 0 and relocation["symbol"].startswith("native_fn_") and binding.get("kind") == "function"
        if function_pointer and (int(binding["address"], 0) & ~1) != target & ~1:
            raise ValueError("Qualified function-pointer target differs from its relocation")
        if (direct or function_pointer) and not first <= (target & ~1) < first + entry["bytes"]:
            targets[target & ~1] = relocation["symbol"]
    return targets


def bounded_oracle(entry, code, native, bindings=None):
    rng = random.Random(20261027005 + int(entry["address"], 0))
    callees = call_targets(entry, bindings)
    passed, unsupported = [], []
    for index in range(32):
        buffers = [0x03002000, 0x03004000, 0x03008000, 0x0300A000]
        memory = {address: bytes(4096) for address in buffers}
        if index % 2:
            for number, address in enumerate(buffers):
                memory[address] = struct.pack("<I", buffers[(number + 1) % len(buffers)]) * 1024
        memory[0x0301F000] = bytes(4096)
        registers = [rng.getrandbits(32) for unused in compiler.REGISTERS]
        registers[:4] = buffers if index < 16 else [index % 4, buffers[1], buffers[2], index % 7]
        registers[-2:] = [0x0301FFF0, 0x04000000]
        flags = rng.getrandbits(4) << 28 | 0x10
        try:
            original = compiler.execute(native, int(entry["address"], 0), registers, memory, flags, callees, index, entry["mode"])
        except Exception as error:
            unsupported.append({"vector": index, "nativeFailure": f"{type(error).__name__}: {error}"})
            continue
        rebuilt = compiler.execute(code, int(entry["address"], 0), registers, memory, flags, callees, index, entry["mode"])
        if original != rebuilt:
            raise ValueError("Reused caller behavior differs in an actually returning fixture")
        passed.append(compiler.sha(json.dumps(original, sort_keys=True).encode()))
    return {"supportedReturningVectors": len(passed), "nativeAndCompiledReturningCalls": len(passed) * 2, "unsupportedVectors": unsupported, "stateSha256": passed, "actualReturnRequiredForSupportedVectors": True, "instructionLimit": 2000, "externalCallContracts": {hex(key): value for key, value in callees.items()}, "externalCalleesExecutedNatively": False, "limitations": ["Only caller behavior under explicit deterministic synthetic callee contracts is compared", "Native callee implementations receive no source credit", "Missing platform/valid-object context remains unsupported rather than passed", "Byte and real module-link comparisons establish source matching independently of fixture coverage", "Game-level meanings and valid input domains remain unassigned"]}


def compile_entry(source, spec, settings):
    flags = settings.get("compilerFlags", settings.get("flags"))
    optimization = flags[0][2:]
    speed = "speed" in flags or ",p" in flags[0]
    inline = flags[flags.index("-inline") + 1] if "-inline" in flags else "off"
    executable = settings.get("compilerPath", settings.get("compiler", "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"))
    executable = ROOT / executable
    if sha256(executable) != settings["compilerSha256"]:
        raise ValueError("Recovered C compiler provenance changed")
    processor = flags[flags.index("-proc") + 1] if "-proc" in flags else None
    rows, found = compiler.compare(source, spec["module"], optimization, inline, speed, spec["mode"] == "thumb", executable, processor)
    return rows, found.get(spec["name"])


def verify(report, path):
    binary = ROOT / f"extract/arm9_overlays/{report['module']}.bin"
    if sha256(binary) != report["moduleInputSha256"]:
        raise ValueError("Reused overlay input changed")
    matched = []
    for old in report["matches"]:
        provenance = old["sourceReuseProvenance"]
        if sha256(ROOT / old["source"]) != old["sourceSha256"] or sha256(ROOT / provenance["source"]) != provenance["sourceSha256"]:
            raise ValueError("Frozen reused source or original recovered C changed")
        spec = {"name": old["name"], "module": report["module"], "mode": old["mode"]}
        rows, result = compile_entry(ROOT / old["source"], spec, old)
        if result is None:
            raise ValueError("A reused overlay source stopped matching")
        entry, code = result
        for field in ("sourceSha256", "address", "mode", "bytes", "targetSha256", "outputSha256"):
            if entry[field] != old[field]:
                raise ValueError("Reused source extent or native identity changed")
        address = int(entry["address"], 0) - 0x021D7240
        entry["oracle"] = bounded_oracle(entry, code, binary.read_bytes()[address:address + entry["bytes"]], old["qualifiedDependencies"])
        for name, dependency in old["qualifiedDependencies"].items():
            dependency["module"] = binding_scope(report["module"], int(dependency["address"], 0))
            if dependency["kind"] == "function" and dependency["module"] is None:
                raise ValueError("Reused source has an unresolved executable dependency scope")
        for relocation in entry["relocations"]:
            dependency = old["qualifiedDependencies"].get(relocation["symbol"])
            if dependency:
                relocation.update(targetModule=dependency["module"], targetMode=dependency["mode"])
        matched.append({**old, **entry})
    report["matches"] = matched
    report["nativeSymbols"] = {rel["symbol"]: rel["target"] for item in matched for rel in item["relocations"]}
    write_json(path, report)
    print({"verified": len(matched), "bytes": sum(item["bytes"] for item in matched)})


def recover(module, batch, path):
    from reuse_utility_c import origins, normalized
    from ledger_state import collect_matches
    index = origins()
    known, rejected = collect_matches(configuration()["romSha256"])
    accepted = [(address, address + entry["size"]) for (name, mode, address), entry in known.items() if name == module]
    binary_path = ROOT / f"extract/arm9_overlays/{module}.bin"
    binary = binary_path.read_bytes()
    seed = next(item for item in read_json(ROOT / "provenance/seed-manifest.json")["modules"] if item["name"] == module)
    if sha256(binary_path) != seed["sha256"]:
        raise ValueError("Overlay differs from measured seed")
    symbols = (ROOT / f"config/arm9/overlays/{module}/symbols.txt").read_text()
    specs = re.findall(r"^(\S+) kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)$", symbols, re.M)
    work = ROOT / "work/transplants" / batch
    work.mkdir(parents=True, exist_ok=True)
    matches, attempts = [], []
    for original, mode, size_text, address_text in specs:
        address, size = int(address_text, 0), int(size_text, 0)
        if any(first < address + size and address < last for first, last in accepted):
            continue
        spec = {"module": module, "mode": mode, "address": address, "bytes": size, "name": f"native_{module}_{address:08x}"}
        native = binary[address - 0x021D7240:address - 0x021D7240 + size]
        done = False
        for layout, hashes in index.get((mode, size), {}).items():
            for origin in hashes.get(normalized(native, layout), []):
                if origin.get("assemblyJustification") or origin.get("sourceLanguage") in ("assembly", "c-with-hardware-assembly", "metrowerks-assembler-function"):
                    continue
                text = (ROOT / origin["source"]).read_text(encoding="utf-8-sig")
                if re.search(r"\b(?:asm|__asm|__asm__)\b", text):
                    continue
                if "#include" in text or len(text.splitlines()) > 500:
                    continue
                mapping = source_bindings(origin, spec, native, text)
                if mapping is None:
                    continue
                rename, bindings = mapping
                text = re.sub(r"\b(?:" + "|".join(map(re.escape, rename)) + r")\b", lambda match: rename[match[0]], text)
                source = work / (spec["name"] + ".c")
                source.write_text(text)
                try:
                    rows, result = compile_entry(source, spec, origin)
                    attempts.extend(rows)
                except Exception as error:
                    attempts.append({"address": hex(address), "origin": origin["source"], "failure": str(error)})
                    continue
                if result is None:
                    continue
                frozen = ROOT / "src/transplants" / batch / source.name
                if frozen.exists():
                    raise ValueError("Refusing to overwrite a reused source")
                frozen.parent.mkdir(parents=True, exist_ok=True)
                frozen.write_bytes(source.read_bytes())
                rows, result = compile_entry(frozen, spec, origin)
                if result is None:
                    raise ValueError("Frozen source differs from matched draft")
                entry, code = result
                entry["oracle"] = bounded_oracle(entry, code, native, bindings)
                entry["sourceReuseProvenance"] = {key: origin[key] for key in ("name", "module", "address", "source", "sourceSha256", "compilerSha256")}
                entry["sourceReuseProvenance"].update(rename=rename, ordinaryCOnly=True, originalBytesUsedAsSourceInput=False)
                entry["qualifiedDependencies"] = bindings
                for relocation in entry["relocations"]:
                    if relocation["symbol"] in bindings:
                        relocation["targetModule"] = bindings[relocation["symbol"]]["module"]
                        relocation["targetMode"] = bindings[relocation["symbol"]]["mode"]
                matches.append(entry)
                accepted.append((address, address + size))
                print({"address": hex(address), "bytes": size, "returningVectors": entry["oracle"]["supportedReturningVectors"]}, flush=True)
                done = True
                break
            if done:
                break
    report = {"schemaVersion": 1, "createdUtc": now(), "romSha256": configuration()["romSha256"], "module": module, "moduleInputSha256": sha256(binary_path), "matches": matches, "nativeSymbols": {rel["symbol"]: rel["target"] for entry in matches for rel in entry["relocations"]}, "wholeModuleLinked": False, "sourceReconstructionComplete": False, "limitations": ["Complete instruction patterns select hypotheses only; actual C compilation and declared ELF relocation comparison are required", "Only frozen recovered C is copied; no original executable data or generated disassembly becomes source", "Unresolved data ownership, overlay lifetimes and unsupported execution contexts remain explicit"]}
    write_json(ROOT / f"evidence/attempts/{batch}.json", attempts)
    write_json(path, report)
    print({"functions": len(matches), "bytes": sum(item["bytes"] for item in matches)})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("module", choices=("ov000", "ov001", "ov005", "ov006"))
    parser.add_argument("--batch", required=True)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9_-]+", args.batch):
        raise ValueError("Invalid reuse batch")
    inputs = verify_inputs(configuration())
    destination = ROOT / f"evidence/matches/{args.batch}.json"
    if args.verify:
        report = read_json(destination)
        if report["module"] != args.module or report["romSha256"] != inputs["rom"]["sha256"]:
            raise ValueError("Reused source namespace changed")
        verify(report, destination)
    else:
        if destination.exists():
            raise ValueError("Choose a new source reuse batch")
        recover(args.module, args.batch, destination)
    if inputs != verify_inputs(configuration()):
        raise ValueError("Input identity changed")
