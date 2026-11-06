import argparse
import hashlib
import json
import os
import random
import re
import struct
import subprocess
import sys
import zipfile
from pathlib import Path
import arm7_runtime
import match_lowlevel as common

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "deps/native"))
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import ARM_OP_MEM, ARM_REG_PC
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_ARM_REG_LR

WORK = ROOT / "work/lowlevel-recovery/arm7-source"
PRELUDE = "typedef unsigned char u8;\ntypedef signed char s8;\ntypedef unsigned short u16;\ntypedef signed short s16;\ntypedef unsigned int u32;\ntypedef signed int s32;\n"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def accepted_spec(entry, instructions=False):
    image = (ROOT / "extract/arm7/arm7.bin").read_bytes()
    layout = arm7_runtime.derive(image)
    module = next(module for module in layout["modules"] if module["id"] == entry["module"])
    if entry.get("processor") != "arm7" or entry.get("program"):
        raise ValueError("Accepted host ARM7 source has a different CPU/program namespace")
    address, base, size = int(entry["address"], 0), int(module["runtimeBase"], 0), entry["bytes"]
    mode = entry.get("mode", "arm")
    binary = (ROOT / module["binary"]).read_bytes()
    if mode not in ("arm", "thumb") or address % (4 if mode == "arm" else 2) or not base <= address < address + size <= base + len(binary):
        raise ValueError("Accepted ARM7 source escapes its canonical runtime module")
    native = binary[address - base:address - base + size]
    if sha(binary) != module["sha256"] or entry.get("inputModuleSha256", module["sha256"]) != module["sha256"] or sha(native) != entry["targetSha256"]:
        raise ValueError("Accepted ARM7 native module/span hash changed")
    result = {"module": module["id"], "processor": "arm7", "mode": mode, "address": address, "base": base, "bytes": size,
              "binary": module["binary"], "inputModuleSha256": module["sha256"], "boundaryEvidence": entry.get("boundaryEvidence", "Frozen accepted source span and native hash in the pinned canonical loader module")}
    if instructions:
        decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if mode == "thumb" else CS_MODE_ARM)
        decoder.detail = True
        decoded = list(decoder.disasm(native, address))
        pools = {(((instruction.address + 4) & ~3) if mode == "thumb" else instruction.address + 8) + operand.mem.disp for instruction in decoded for operand in instruction.operands
                 if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC and address <= (((instruction.address + 4) & ~3) if mode == "thumb" else instruction.address + 8) + operand.mem.disp <= address + size - 4}
        result.update(instructions=[instruction for instruction in decoded if not any(location <= instruction.address < location + 4 for location in pools)],
                      pools={location: struct.unpack_from("<I", native, location - address)[0] for location in pools})
    return result


def candidates(max_body=32):
    layout = json.loads(arm7_runtime.MANIFEST.read_text())
    inventory = json.loads((ROOT / "evidence/arm7/ghidra-runtime-inventory.json").read_text())
    if not inventory.get("runtimeMappingCanonical") or inventory["sha256"] != layout["imageSha256"]:
        raise ValueError("ARM7 function inventory does not use the measured runtime mapping")
    modules = {module["id"]: module for module in layout["modules"]}
    binaries = {module["id"]: (ROOT / module["binary"]).read_bytes() for module in layout["modules"]}
    for module in layout["modules"]:
        if sha(binaries[module["id"]]) != module["sha256"]:
            raise ValueError("ARM7 runtime module hash changed")
    entries = {int(function["address"], 0) for function in inventory["functions"]}
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    result = []
    for function in inventory["functions"]:
        if function["mode"] != "arm" or len(function["ranges"]) != 1 or function["bodyBytes"] > max_body:
            continue
        module = modules[function["module"]]
        binary = binaries[module["id"]]
        base, address = int(module["runtimeBase"], 0), int(function["address"], 0)
        if address % 4 or function["bodyBytes"] % 4:
            continue
        offset = address - base
        code = binary[offset:offset + function["bodyBytes"]]
        instructions = list(decoder.disasm(code, address))
        if sum(instruction.size for instruction in instructions) != len(code):
            continue
        end, pools = address + len(code), {}
        for instruction in instructions:
            for operand in instruction.operands:
                if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC:
                    pool = instruction.address + 8 + operand.mem.disp
                    if not address <= pool <= base + len(binary) - 4:
                        break
                    pools[pool] = struct.unpack_from("<I", binary, pool - base)[0]
                    end = max(end, pool + 4)
        if any(address < entry < end for entry in entries) or end > base + len(binary):
            continue
        result.append({"module": module["id"], "address": address, "bytes": end - address,
                       "binary": module["binary"], "base": base, "instructions": instructions,
                       "pools": pools, "inputModuleSha256": module["sha256"],
                       "boundaryEvidence": "Ghidra runtime-map function body plus own PC-relative literal suffix, with no intervening function entry"})
    return result


def template(spec):
    instructions, pools = spec["instructions"], spec["pools"]
    ops = [(instruction.mnemonic, instruction.op_str) for instruction in instructions]
    name = "native_" + spec["module"].replace("-", "_") + f"_{spec['address']:08x}"
    returns = {"ldr": "u32", "ldrb": "u8", "ldrh": "u16", "ldrsb": "s8", "ldrsh": "s16"}
    stores = {"str": "u32", "strb": "u8", "strh": "u16"}
    def memory(index, scalar, base):
        operand = instructions[index].operands[-1]
        if operand.type != ARM_OP_MEM or operand.mem.index:
            raise ValueError("Indexed memory operand requires a separate source model")
        return f"*(volatile {scalar} *)({base} + {operand.mem.disp})"
    if ops == [("bx", "lr")]:
        return PRELUDE + f"void {name}(void) {{\n}}\n", {"kind": "noop"}
    if len(ops) == 2 and ops[-1] == ("bx", "lr"):
        if ops[0][0] == "mov" and ops[0][1].startswith("r0, #"):
            value = instructions[0].operands[1].imm & 0xFFFFFFFF
            return PRELUDE + f"u32 {name}(void) {{\n    return {value:#x}U;\n}}\n", {"kind": "constant"}
        if ops[0][0] in returns and ops[0][1].startswith("r0, [r0"):
            scalar = returns[ops[0][0]]
            return PRELUDE + f"u32 {name}(u8 *value) {{\n    return {memory(0, scalar, 'value')};\n}}\n", {"kind": "getter", "argumentPointer": True}
        if ops[0][0] in stores and ops[0][1].startswith("r1, [r0"):
            scalar = stores[ops[0][0]]
            return PRELUDE + f"void {name}(u8 *target, u32 value) {{\n    {memory(0, scalar, 'target')} = value;\n}}\n", {"kind": "setter", "argumentPointer": True}
        if ops[0][0] == "ldr" and ops[0][1].startswith("r0, [pc") and len(pools) == 1:
            value = next(iter(pools.values()))
            return PRELUDE + f"u32 {name}(void) {{\n    return {value:#x}U;\n}}\n", {"kind": "constant"}
    if len(ops) == 2 and ops[0][0] == "ldr" and ops[0][1].startswith("ip, [pc") and ops[1] == ("bx", "ip"):
        target = next(iter(pools.values()))
        callee = f"native_arm7_fn_{target:08x}"
        return PRELUDE + f"extern u32 {callee}(u32, u32, u32, u32);\nu32 {name}(u32 a, u32 b, u32 c, u32 d) {{\n    return {callee}(a, b, c, d);\n}}\n", {"kind": "tail-call", "callees": {callee: target}}
    if len(ops) == 3 and ops[-1] == ("bx", "lr") and ops[0][0] == "ldr" and "[pc" in ops[0][1] and len(pools) == 1:
        target = next(iter(pools.values()))
        variable = f"native_arm7_data_{target:08x}"
        if ops[0][1].startswith("r0,") and ops[1][0] in returns and ops[1][1].startswith("r0, [r0"):
            scalar = returns[ops[1][0]]
            return PRELUDE + f"extern u8 {variable}[];\nu32 {name}(void) {{\n    return {memory(1, scalar, variable)};\n}}\n", {"kind": "global-getter"}
        if ops[0][1].startswith("r1,") and ops[1][0] in stores and ops[1][1].startswith("r0, [r1"):
            scalar = stores[ops[1][0]]
            return PRELUDE + f"extern u8 {variable}[];\nvoid {name}(u32 value) {{\n    {memory(1, scalar, variable)} = value;\n}}\n", {"kind": "global-setter"}
    if len(ops) in (3, 4, 5) and ops[0] == ("mov", "r1, #0") and ops[-1] == ("bx", "lr") and all(op == "str" and text.startswith("r1, [r0") for op, text in ops[1:-1]):
        statements = "".join("    " + memory(index, "u32", "target") + " = 0;\n" for index in range(1, len(ops) - 1))
        return PRELUDE + f"void {name}(u8 *target) {{\n{statements}}}\n", {"kind": "clear-fields", "argumentPointer": True}
    return None


def tools():
    archive = ROOT / "tools/mwccarm.zip"
    if archive.exists() and sha(archive.read_bytes()) == "dc386e37b2176e960954a733de928337d9b7e7620b9e94228008c31774339ace":
        with zipfile.ZipFile(archive) as package:
            rows = []
            for version in ("2.0/base", "1.2/base", "1.2/sp2", "1.2/sp2p3", "1.2/sp3", "1.2/sp4"):
                member = "mwccarm/" + version + "/mwccarm.exe"
                path = ROOT / "tools/mwccarm" / member
                if path.exists():
                    expected = sha(package.read(member))
                    if sha(path.read_bytes()) != expected:
                        raise ValueError("Compiler executable differs from pinned private archive: " + version)
                    rows.append((path, expected))
            return rows
    path = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
    expected = "7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880"
    if sha(path.read_bytes()) != expected:
        raise ValueError("ARM7 compiler identity differs")
    return [(path, expected)]


def compare(source, spec, compiler, compiler_hash, optimization, inline, speed=False):
    if sha(compiler.read_bytes()) != compiler_hash:
        raise ValueError("ARM7 source compiler differs from its declared immutable pin")
    directory = WORK / "compile" / source.stem
    directory.mkdir(parents=True, exist_ok=True)
    flags = common.FLAGS[:]
    flags[0] = f"-O{optimization}"
    flags[flags.index("-proc") + 1] = "arm7tdmi"
    flags[flags.index("-inline") + 1] = inline
    if speed:
        flags.extend(["-opt", "speed"])
    key = sha((str(compiler) + json.dumps(flags)).encode())[:16]
    obj = directory / (key + ".o")
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat"))
    result = subprocess.run([str(compiler), *flags, "-c", str(source), "-o", str(obj)], cwd=ROOT, env=env, capture_output=True, timeout=30)
    if result.returncode:
        return {"compileFailed": True, "stdout": result.stdout.decode(errors="replace"), "stderr": result.stderr.decode(errors="replace"), "compilerFlags": flags, "compilerSha256": compiler_hash}, None
    object_hash = sha(obj.read_bytes())
    stable = WORK / "objects" / (object_hash + ".o")
    stable.parent.mkdir(parents=True, exist_ok=True)
    if not stable.exists():
        stable.write_bytes(obj.read_bytes())
    name = "native_" + spec["module"].replace("-", "_") + f"_{spec['address']:08x}"
    relocations = []
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        symbol = next(symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols() if symbol.name == name)
        code = bytearray(elf.get_section(symbol["st_shndx"]).data())
        for section in elf.iter_sections():
            if section["sh_type"] not in ("SHT_REL", "SHT_RELA") or section["sh_info"] != symbol["st_shndx"]:
                continue
            table = elf.get_section(section["sh_link"])
            for rel in section.iter_relocations():
                target_name = table.get_symbol(rel["r_info_sym"]).name
                try:
                    target = common.symbol_address(target_name)
                except common.UnresolvedNativeSymbol as error:
                    error.details.update(name=name, module=spec['module'], address=hex(spec['address']), bytes=spec['bytes'],
                        source=source.relative_to(ROOT).as_posix(), sourceSha256=sha(source.read_bytes()),
                        object=stable.relative_to(ROOT).as_posix(), objectSha256=object_hash, compilerFlags=flags,
                        compilerSha256=compiler_hash, relocationOffset=rel['r_offset'])
                    raise
                offset, kind = rel["r_offset"], rel["r_info_type"]
                value = struct.unpack_from("<I", code, offset)[0]
                addend = rel["r_addend"] if section["sh_type"] == "SHT_RELA" else value
                if kind == 2:
                    value = target + addend
                elif kind in (1, 28, 29):
                    if section["sh_type"] == "SHT_REL":
                        addend = (value & 0xFFFFFF) << 2
                        if addend & 0x2000000:
                            addend -= 0x4000000
                    value = (value & 0xFF000000) | (((target + addend - spec["address"] - offset) >> 2) & 0xFFFFFF)
                else:
                    raise ValueError("Unsupported ARM7 compiler relocation: " + str(kind))
                struct.pack_into("<I", code, offset, value & 0xFFFFFFFF)
                relocations.append({"offset": offset, "type": kind, "symbol": target_name, "target": hex(target), "addend": addend})
        index, value = symbol["st_shndx"], symbol["st_value"]
    binary = (ROOT / spec["binary"]).read_bytes()
    if sha(binary) != spec["inputModuleSha256"]:
        raise ValueError("ARM7 compiler target module changed")
    native = binary[spec["address"] - spec["base"]:spec["address"] - spec["base"] + spec["bytes"]]
    matched = bytes(code) == native
    record = {"name": name, "module": spec["module"], "processor": "arm7", "mode": "arm", "address": hex(spec["address"]),
              "bytes": spec["bytes"], "compiledBytes": len(code), "matchingBytes": sum(a == b for a, b in zip(native, code)),
              "exactAfterDeclaredRelocation": matched, "nativeAlias": "func_" + spec["module"].replace("-", "_") + f"_{spec['address']:08x}",
              "boundaryEvidence": spec["boundaryEvidence"], "inputModuleSha256": spec["inputModuleSha256"],
              "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha(source.read_bytes()),
              "object": stable.relative_to(ROOT).as_posix(), "objectSha256": object_hash,
              "compiler": compiler.relative_to(ROOT).as_posix(), "compilerSha256": compiler_hash, "compilerFlags": flags,
              "sectionIndex": index, "sectionOffset": value, "targetSha256": sha(native), "outputSha256": sha(code), "relocations": relocations,
              "linked": False}
    return record, bytes(code) if matched else None


def execute(code, spec, shape, vector):
    rng = random.Random(20261027 + spec["address"] + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    memory = [(0x02380000, 0x30000), (0x027E0000, 0x20000), (0x037F8000, 0x18000), (0x03000000, 0x20000), (0x04000000, 0x2000), (0x05000000, 0x1000)]
    for address, size in memory:
        engine.mem_map(address, size)
        engine.mem_write(address, rng.randbytes(size))
    if shape.get("nativeRuntimeInitialized"):
        layout = json.loads(arm7_runtime.MANIFEST.read_text())
        for module in layout["modules"]:
            initialized = (ROOT / module["binary"]).read_bytes()
            if sha(initialized) != module["sha256"]:
                raise ValueError("ARM7 bounded-state module hash changed")
            engine.mem_write(int(module["runtimeBase"], 0), initialized)
            if module["bssBytes"]:
                engine.mem_write(int(module["bssStart"], 0), bytes(module["bssBytes"]))
    registers = [rng.getrandbits(32) for _ in common.REGISTERS]
    if shape.get("argumentPointer"):
        registers[0] = 0x03002000
    for index in shape.get("argumentPointerRegisters", []):
        registers[index] = 0x03002000 + index * 0x1000
    for index, values in shape.get("argumentValues", {}).items():
        registers[int(index)] = values[vector % len(values)]
    registers[-2:] = [0x0301FFF0, 0x05000000]
    if not shape.get("argumentPointer") and "0" not in shape.get("argumentValues", {}) and vector < 4:
        registers[0] = [0, 1, 0x7FFFFFFF, 0xFFFFFFFF][vector]
    thumb = spec.get("mode") == "thumb"
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | shape.get("cpsrMode", 0x10) | ((rng.randrange(4) << 6) if shape.get("cpsrMode") else 0) | (0x20 if thumb else 0))
    for register, value in zip(common.REGISTERS, registers):
        engine.reg_write(register, value)
    engine.mem_write(spec["address"], code)
    writes, calls, visited = [], [], set()
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value]))
    callees = {target & ~1: name for name, target in shape.get("callees", {}).items()}
    def intercept(uc, address, size, user):
        if spec["address"] <= address < spec["address"] + len(code):
            visited.add(address)
        if address in callees:
            calls.append({"address": hex(address), "thumb": bool(uc.reg_read(UC_ARM_REG_CPSR) & 0x20),
                          "arguments": [uc.reg_read(register) for register in common.REGISTERS[:4]]})
            if shape.get("boundedCalleeReturns"):
                result = [0, 1, 0x03008000, 0x03009000][vector % 4]
            else:
                result = (address * 65537 + vector) & 0xFFFFFFFF
            uc.reg_write(common.REGISTERS[0], result)
            returned = uc.reg_read(UC_ARM_REG_LR)
            uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | ((returned & 1) << 5))
            uc.reg_write(UC_ARM_REG_PC, returned & ~1)
    engine.hook_add(UC_HOOK_CODE, intercept)
    engine.emu_start(spec["address"] | int(thumb), 0x05000000, count=500)
    if engine.reg_read(UC_ARM_REG_PC) != 0x05000000:
        raise ValueError("ARM7 unit did not return to sentinel")
    return {"registers": [engine.reg_read(register) for register in common.REGISTERS], "cpsr": engine.reg_read(UC_ARM_REG_CPSR), "writes": writes, "calls": calls, "visited": sorted(visited),
            "memoryHashes": [sha(bytes(engine.mem_read(address, size))) for address, size in memory]}


def oracle(code, spec, shape):
    binary = (ROOT / spec["binary"]).read_bytes()
    offset = spec["address"] - spec["base"]
    native = binary[offset:offset + spec["bytes"]]
    results = []
    for vector in range(24):
        before, after = execute(native, spec, shape, vector), execute(code, spec, shape, vector)
        if before != after:
            raise ValueError("ARM7 native/recompiled effects differ")
        results.append(sha(json.dumps(before, sort_keys=True).encode()))
    return {"vectors": 24, "nativeAndRecompiledCalls": 48, "instructionLimit": 500, "verifiedReturn": True, "stateSha256": results,
            "limitations": ["Synthetic isolated RAM/MMIO model, without physical alias/controller effects", "Tail calls use explicit synthetic target/argument/interworking contracts; native callee implementations are not executed"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", default="primitives01")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    report_path = ROOT / f"evidence/matches/arm7-{args.batch}.json"
    compiler_tools = tools()
    if args.verify:
        previous = json.loads(report_path.read_text())
        accepted = {entry["name"]: entry for entry in previous["matches"]}
        selected = []
        for entry in previous["matches"]:
            spec = accepted_spec(entry, instructions=True)
            generated = template(spec)
            if generated is None:
                raise ValueError("Accepted ARM7 primitive no longer has its measured template shape")
            selected.append((spec, (generated[0], entry.get("oracleShape", generated[1]))))
    else:
        if report_path.exists():
            raise ValueError("Refusing to overwrite an accepted ARM7 batch")
        selected = [(spec, template(spec)) for spec in candidates()]
    matches, attempts = [], []
    for spec, generated in selected:
        if generated is None:
            continue
        text, shape = generated
        name = "native_" + spec["module"].replace("-", "_") + f"_{spec['address']:08x}"
        source = ROOT / f"src/arm7/{args.batch}/{name}.c"
        if args.verify:
            expected = accepted[name]
            if sha(source.read_bytes()) != expected["sourceSha256"]:
                raise ValueError("Accepted ARM7 C source changed")
            choices = [(ROOT / expected["compiler"], expected["compilerSha256"], int(expected["compilerFlags"][0][2:]), expected["compilerFlags"][expected["compilerFlags"].index("-inline") + 1])]
        else:
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(text)
            choices = [(compiler, digest, level, inline) for compiler, digest in compiler_tools for level, inline in [(2, "off"), (2, "noauto"), (0, "off"), (1, "off"), (3, "off"), (4, "off")]]
        found = False
        for compiler, digest, level, inline in choices:
            record, code = compare(source, spec, compiler, digest, level, inline)
            attempts.append(record)
            if code is not None:
                record["oracle"] = oracle(code, spec, shape)
                record["oracleShape"] = shape
                matches.append(record)
                found = True
                break
        print({"function": name, "matched": found, "bytes": spec["bytes"]}, flush=True)
        if args.verify and not found:
            raise ValueError("Accepted ARM7 function stopped matching")
    if args.verify and {entry["name"] for entry in matches} != set(accepted):
        raise ValueError("ARM7 verification must preserve every accepted function")
    report = {"schemaVersion": 1, "romSha256": sha((ROOT / "inputs/game.nds").read_bytes()), "processor": "arm7", "runtimeMappingCanonical": True,
              "matches": matches, "attempts": attempts, "nativeSymbols": {rel["symbol"]: rel["target"] for entry in matches for rel in entry["relocations"]},
              "wholeModuleLinked": False, "sourceReconstructionComplete": False}
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print({"matched": len(matches), "bytes": sum(entry["bytes"] for entry in matches), "attempts": len(attempts)})


if __name__ == "__main__":
    main()
