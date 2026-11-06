import argparse
import hashlib
import json
import os
import random
import re
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "deps/native"))
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_MODE_THUMB, UC_HOOK_MEM_WRITE, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_CPSR, UC_ARM_REG_PC

REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]
COMPILER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
WORK = ROOT / "work/runtime-recovery"
FLAGS = ["-O2", "-enum", "int", "-char", "signed", "-str", "noreuse", "-proc", "arm946e", "-gccext,on", "-fp", "soft", "-inline", "off", "-Cpp_exceptions", "off", "-RTTI", "off", "-interworking", "-w", "off", "-sym", "on", "-gccinc", "-nolink", "-msgstyle", "gcc"]
COMPILER_PINS = {
    "tools/mwccarm/mwccarm/1.2/base/mwccarm.exe": "87b4f748825ded418355e4ae35e032ce8b27c083cc4c60598ce2a75d346e4399",
    "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe": "7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880",
    "tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe": "89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca",
    "tools/mwccarm/mwccarm/2.0/sp1p6/mwccarm.exe": "2819dea7ae847ff83699d18bbc567238abe2804b6783b3bcc5893c5e546b0334"
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def symbol_address(name):
    match = re.search(r"(?:^|_)([0-9a-f]{8})$", name)
    if not match:
        raise ValueError("Unknown native symbol identity: " + name)
    return int(match.group(1), 16)


def compare(source, module, optimization, inline, speed=False, thumb=False, compiler=None, processor=None):
    executable = Path(compiler or COMPILER).resolve()
    compiler_path = executable.relative_to(ROOT).as_posix()
    compiler_hash = sha(executable.read_bytes())
    if compiler_hash != COMPILER_PINS.get(compiler_path):
        raise ValueError("Unpinned runtime compiler identity")
    flags = FLAGS[:]
    flags[0] = f"-O{optimization}"
    flags[flags.index("-inline") + 1] = inline
    if processor:
        flags[flags.index("-proc") + 1] = processor
    if speed:
        flags.extend(["-opt", "speed"])
    if thumb:
        flags.append("-thumb")
    directory = WORK / source.stem / sha(str(source).encode())[:12]
    directory.mkdir(parents=True, exist_ok=True)
    obj = directory / f"{optimization}-{inline}{'-speed' if speed else ''}{'-thumb' if thumb else ''}{'-' + compiler_hash[:12] if compiler else ''}.o"
    obj = obj.with_name(obj.name.replace(',', '-'))
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat"))
    result = subprocess.run([str(executable), *flags, "-c", str(source), "-o", str(obj)], cwd=ROOT, env=env, capture_output=True, timeout=60)
    if result.returncode:
        return [{"compileFailed": True, "flags": flags, "stdout": result.stdout.decode(errors="replace"), "stderr": result.stderr.decode(errors="replace")}], {}
    object_hash = sha(obj.read_bytes())
    stable = WORK / "objects" / (object_hash + ".o")
    stable.parent.mkdir(parents=True, exist_ok=True)
    if not stable.exists():
        stable.write_bytes(obj.read_bytes())
    if module == "main":
        binary, symbols, base = "extract/arm9/arm9.bin", "config/arm9/symbols.txt", 0x02000000
    elif module in ("ov000", "ov001", "ov002", "ov003", "ov005", "ov006", "ov007"):
        binary, symbols, base = f"extract/arm9_overlays/{module}.bin", f"config/arm9/overlays/{module}/symbols.txt", 0x021D7240
    else:
        raise ValueError("Unsupported runtime comparison namespace")
    data = (ROOT / binary).read_bytes()
    boundaries = (ROOT / symbols).read_text()
    records, compiled = [], {}
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        for symbol in elf.get_section_by_name(".symtab").iter_symbols():
            if not symbol.name.startswith(f"native_{module}_") or not isinstance(symbol["st_shndx"], int):
                continue
            address = symbol_address(symbol.name)
            mode = "thumb" if thumb else "arm"
            boundary = re.search(rf"^(\S+) kind:function\({mode},size=(0x[0-9a-f]+)\) addr:0x{address:08x}$", boundaries, re.M)
            if not boundary:
                raise ValueError("Unverified function boundary: " + symbol.name)
            size = int(boundary.group(2), 16)
            raw = elf.get_section(symbol["st_shndx"]).data()
            start = symbol["st_value"] & ~1
            code = bytearray(raw[start:start + symbol["st_size"]])
            relocations = []
            for section in elf.iter_sections():
                if section["sh_type"] not in ("SHT_REL", "SHT_RELA") or section["sh_info"] != symbol["st_shndx"]:
                    continue
                table = elf.get_section(section["sh_link"])
                for rel in section.iter_relocations():
                    offset = rel["r_offset"] - start
                    if not 0 <= offset < len(code):
                        continue
                    name = table.get_symbol(rel["r_info_sym"]).name
                    try:
                        target = symbol_address(name)
                        binding = "measured-address-symbol"
                    except ValueError:
                        if not re.fullmatch(r"_(?:[us](?:32|64)|f|d)_\w+", name) or rel["r_info_type"] not in (1, 10, 28, 29):
                            raise
                        native_word = struct.unpack_from("<I", data, address - base + offset)[0]
                        if rel["r_info_type"] == 10:
                            high, low = native_word & 0xFFFF, native_word >> 16
                            if high & 0xF800 != 0xF000 or low & 0xF800 != 0xF800:
                                raise ValueError("Compiler helper site is not a native Thumb BL")
                            displacement = (high & 0x7FF) << 12 | (low & 0x7FF) << 1
                            if displacement & 0x400000:
                                displacement -= 0x800000
                            target = address + offset + 4 + displacement
                        else:
                            if native_word & 0x0E000000 != 0x0A000000:
                                raise ValueError("Compiler helper site is not a native branch")
                            displacement = (native_word & 0xFFFFFF) << 2
                            if displacement & 0x2000000:
                                displacement -= 0x4000000
                            target = address + offset + 8 + displacement
                        binding = "compiler-helper-bound-to-measured-native-branch-target"
                    value = struct.unpack_from("<I", code, offset)[0]
                    kind = rel["r_info_type"]
                    if kind == 2:
                        addend = rel["r_addend"] if section["sh_type"] == "SHT_RELA" else value
                        if thumb and re.search(rf"kind:function\(thumb,size=0x[0-9a-f]+\) addr:0x{target:08x}$", boundaries, re.M):
                            target |= 1
                        struct.pack_into("<I", code, offset, (target + addend) & 0xFFFFFFFF)
                    elif kind == 10 and thumb:
                        high, low = value & 0xFFFF, value >> 16
                        if high & 0xF800 != 0xF000 or low & 0xF800 != 0xF800:
                            raise ValueError("Only measured Thumb BL relocations are supported")
                        implicit = (high & 0x7FF) << 12 | (low & 0x7FF) << 1
                        if implicit & 0x400000:
                            implicit -= 0x800000
                        addend = rel["r_addend"] if section["sh_type"] == "SHT_RELA" else implicit
                        displacement = target + addend - address - offset
                        if displacement & 1 or not -0x400000 <= displacement < 0x400000:
                            raise ValueError("Thumb branch target is unaligned or out of range")
                        high = high & 0xF800 | (displacement >> 12) & 0x7FF
                        low = low & 0xF800 | (displacement >> 1) & 0x7FF
                        struct.pack_into("<HH", code, offset, high, low)
                    elif kind in (1, 28, 29):
                        addend = rel["r_addend"] if section["sh_type"] == "SHT_RELA" else ((value & 0xFFFFFF) << 2)
                        displacement = target + addend - address - offset
                        struct.pack_into("<I", code, offset, value & 0xFF000000 | ((displacement >> 2) & 0xFFFFFF))
                    else:
                        raise ValueError("Unsupported relocation: " + str(kind))
                    relocations.append({"offset": offset, "type": kind, "symbol": name, "target": hex(target), "addend": addend, "binding": binding})
            native = data[address - base:address - base + size]
            matched = bytes(code) == native
            entry = {"name": symbol.name, "module": module, "processor": "arm9", "mode": mode, "address": hex(address), "bytes": size, "compiledBytes": len(code), "matchingBytes": sum(a == b for a, b in zip(native, code)), "exactAfterDeclaredRelocation": matched, "targetSha256": sha(native), "outputSha256": sha(code), "relocations": relocations, "compilerFlags": flags, "object": stable.relative_to(ROOT).as_posix(), "objectSha256": object_hash, "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha(source.read_bytes()), "compilerSha256": compiler_hash, "sectionIndex": symbol["st_shndx"], "sectionOffset": start, "nativeAlias": boundary.group(1), "linked": False}
            records.append(entry)
            entry["compilerPath"] = compiler_path
            entry["compilerSha256"] = compiler_hash
            if matched:
                compiled[symbol.name] = (entry, bytes(code))
    return records, compiled


def execute(code, address, registers, memory, flags, callees=None, vector=0, mode="arm", callee_modes=None):
    engine = Uc(UC_ARCH_ARM, UC_MODE_THUMB if mode == "thumb" else UC_MODE_ARM)
    for location, size in [(0x01FF8000, 0x8000), (0x02000000, 0x500000), (0x03000000, 0x20000), (0x04000000, 0x1000)]:
        engine.mem_map(location, size)
    for location, payload in memory.items():
        engine.mem_write(location, payload)
    engine.mem_write(address, code)
    engine.reg_write(UC_ARM_REG_CPSR, flags | (0x20 if mode == "thumb" else 0))
    for register, value in zip(REGISTERS, registers):
        engine.reg_write(register, value)
    writes = []
    calls = []
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, location, size, value, user: writes.append([location, size, value]))
    def intercept(uc, pc, size, user):
        if pc not in (callees or {}):
            return
        if callee_modes and bool(uc.reg_read(UC_ARM_REG_CPSR) & 0x20) != (callee_modes[pc] == "thumb"):
            raise AssertionError("Native call entered a configured callee in the wrong instruction mode")
        arguments = [uc.reg_read(register) for register in REGISTERS[:4]]
        calls.append({"address": hex(pc), "arguments": arguments, "stackArguments": bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 16)).hex()})
        pointers = {0x02223C60, 0x020844D0, 0x01FFB4EC, 0x02049AE4, 0x01FFB340, 0x02061DCC, 0x02223C54}
        if pc in pointers:
            result = 0x03002000
        elif pc == 0x01FFA02C:
            result = 0x03004000
        elif pc == 0x020BB144:
            result = int((arguments[0] + vector) % 3 == 0)
        elif pc in (0x020841D0, 0x02041814, 0x020BA9D0, 0x0221794C, 0x020B9F84):
            result = vector % 3
        elif pc == 0x01FFA358:
            result = vector % 9
        else:
            result = (pc * 2654435761 + vector * 40503 + len(calls)) & 0xFFFFFFFF
        for index, register in enumerate([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]):
            uc.reg_write(register, (result ^ (0x9E3779B9 * (index + 1))) & 0xFFFFFFFF)
        uc.reg_write(UC_ARM_REG_R0, result)
        return_mode = ((uc.reg_read(UC_ARM_REG_LR) & 1) << 5) if callee_modes else 0
        uc.reg_write(UC_ARM_REG_CPSR, ((pc + vector + len(calls)) & 15) << 28 | 0x10 | return_mode)
        location = 0x03008000 + (len(calls) % 64) * 4
        uc.mem_write(location, struct.pack("<I", result))
        writes.append([location, 4, result])
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
    if callees:
        engine.hook_add(UC_HOOK_CODE, intercept)
    engine.emu_start(address | (mode == "thumb"), 0x04000000, count=2000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x04000000:
        raise ValueError("Low-level oracle did not return within bound")
    return {"registers": [engine.reg_read(x) for x in REGISTERS], "cpsr": engine.reg_read(UC_ARM_REG_CPSR), "writes": writes, "calls": calls,
            "memory": [sha(bytes(engine.mem_read(location, len(payload)))) for location, payload in memory.items()]}


def oracle(entry, compiled, native):
    address = int(entry["address"], 0)
    rng = random.Random(20261027 + address)
    callees = {int(rel["target"], 0): rel["symbol"] for rel in entry["relocations"] if rel["symbol"].startswith("native_fn_")}
    results = []
    for index in range(40):
        registers = [rng.getrandbits(32) for _ in REGISTERS]
        registers[:4] = [rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32)]
        registers[-2:] = [0x0301FFF0, 0x04000000]
        memory = {0x01FFF800: rng.randbytes(0x800), 0x021CE000: rng.randbytes(0x10000), 0x02246000: rng.randbytes(0x1000), 0x0301F000: rng.randbytes(0x1000), 0x03002000: rng.randbytes(0x1000), 0x03004000: rng.randbytes(0x1000), 0x03008000: rng.randbytes(0x1000)}
        first, second = bytearray(memory[0x03002000]), bytearray(memory[0x03004000])
        struct.pack_into("<I", first, 0, 0x03004000)
        struct.pack_into("<I", first, 4, 0x03004000 if index % 2 else 0)
        first[0xC0] = index % 2
        struct.pack_into("<H", first, 0x6C, index)
        struct.pack_into("<H", second, 0, index if index % 3 else index + 1)
        memory[0x03002000], memory[0x03004000] = bytes(first), bytes(second)
        global_bytes = bytearray(memory[0x021CE000])
        struct.pack_into("<I", global_bytes, 0xBE0 + 0x30, [0, 1, 2, 0xFFFFFFFF][index % 4])
        struct.pack_into("<I", global_bytes, 0xB54 + 8, [0, 4, 1, 0xFFFFFFFF][index % 4])
        struct.pack_into("<I", global_bytes, 0x6100 + 0x10, [0xF, 0x2B, 0, 1][index % 4])
        memory[0x021CE000] = bytes(global_bytes)
        if index < 4:
            registers[0] = [0, 1, 0x7FFFFFFF, 0xFFFFFFFF][index]
        flags = rng.getrandbits(4) << 28 | 0x10
        original = execute(native, address, registers, memory, flags, callees, index, entry.get("mode", "arm"))
        rebuilt = execute(compiled, address, registers, memory, flags, callees, index, entry.get("mode", "arm"))
        if original != rebuilt:
            raise ValueError(f"Low-level behavior differs at {address:#x} vector {index}")
        results.append(sha(json.dumps(original, sort_keys=True).encode()))
    return {"vectors": len(results), "nativeAndRecompiledCalls": len(results) * 2, "instructionLimit": 2000,
            "verifiedReturn": True, "compared": ["r0-r12", "sp", "lr", "cpsr", "ordered-memory-writes", "initialized-memory-regions"], "stateSha256": results,
            "externalCalls": {hex(target): name for target, name in callees.items()},
            "externalStubContract": "When external calls occur, target-qualified synthetic callees return deterministic values or mapped pointers, clobber caller-saved registers and flags, and write isolated scratch RAM",
            "limitations": ["Synthetic RAM-state comparisons do not establish native gameplay semantics", "External stub contracts compare recovered caller behavior, not the native implementation of callees"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--module", choices=["main"], default="main")
    parser.add_argument("--search", action="store_true")
    parser.add_argument("--oracle", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    source = (ROOT / args.source).resolve()
    if sha(COMPILER.read_bytes()) != "7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880":
        raise ValueError("Pinned compiler differs")
    rom_hash = sha((ROOT / "inputs/game.nds").read_bytes())
    if rom_hash != "674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6":
        raise ValueError("Wrong ROM namespace")
    attempts, matches = [], {}
    configurations = [(2, "off", False), (2, "noauto", False)]
    if args.search:
        configurations.extend((level, "off", False) for level in (0, 1, 3, 4))
        configurations.extend((level, "off", True) for level in (1, 2, 3, 4))
    for optimization, inline, speed in configurations:
        records, found = compare(source, args.module, optimization, inline, speed)
        attempts.extend(records)
        for name, item in found.items():
            matches.setdefault(name, item)
    binary = (ROOT / "extract/arm9/arm9.bin").read_bytes()
    base = 0x02000000
    for entry, code in matches.values():
        if args.oracle:
            address = int(entry["address"], 0)
            entry["oracle"] = oracle(entry, code, binary[address - base:address - base + entry["bytes"]])
    report = {"schemaVersion": 1, "romSha256": rom_hash, "module": args.module, "moduleInputSha256": sha(binary), "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha(source.read_bytes()), "matches": [entry for entry, _ in matches.values()], "attempts": attempts,
              "nativeSymbols": {rel["symbol"]: rel["target"] for entry, _ in matches.values() for rel in entry["relocations"]}, "wholeModuleLinked": False, "sourceReconstructionComplete": False}
    path = ROOT / f"evidence/matches/{args.module}-{source.stem}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        archive = ROOT / "evidence/attempts" / (path.stem + "-" + sha(path.read_bytes())[:16] + ".json")
        archive.parent.mkdir(parents=True, exist_ok=True)
        if not archive.exists():
            archive.write_bytes(path.read_bytes())
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"matches": len(matches), "bytes": sum(entry["bytes"] for entry, _ in matches.values()), "attempts": len(attempts), "unmatched": sorted({entry.get("name") for entry in attempts if entry.get("name")} - set(matches))}))
    if args.strict:
        expected = set(re.findall(r"\bnative_" + args.module + r"_[0-9a-f]{8}(?=\s*\()", source.read_text()))
        if expected != set(matches):
            raise SystemExit(1)


if __name__ == "__main__":
    main()
