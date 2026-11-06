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
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_MEM_WRITE, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_CPSR, UC_ARM_REG_PC

REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]
COMPILER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
WORK = ROOT / "work/lowlevel-recovery"
FLAGS = ["-O2", "-enum", "int", "-char", "signed", "-str", "noreuse", "-proc", "arm946e", "-gccext,on", "-fp", "soft", "-inline", "off", "-Cpp_exceptions", "off", "-RTTI", "off", "-interworking", "-w", "off", "-sym", "on", "-gccinc", "-nolink", "-msgstyle", "gcc"]


class UnresolvedNativeSymbol(ValueError):
    def __init__(self, name):
        super().__init__('Unknown native symbol identity: ' + name)
        self.details = {'unresolvedNativeSymbol': name, 'comparisonCompleted': False, 'exactAfterDeclaredRelocation': False}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def symbol_address(name):
    match = re.search(r"(?:^|_)([0-9a-f]{8})$", name)
    if not match:
        raise UnresolvedNativeSymbol(name)
    return int(match.group(1), 16)


def compare(source, module, optimization, inline, speed=False):
    flags = FLAGS[:]
    flags[0] = f"-O{optimization}"
    flags[flags.index("-inline") + 1] = inline
    if speed:
        flags.extend(["-opt", "speed"])
    directory = WORK / source.stem
    directory.mkdir(parents=True, exist_ok=True)
    obj = directory / (f"{optimization}-{inline}{'-speed' if speed else ''}.o".replace(',', '-'))
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat"))
    result = subprocess.run([str(COMPILER), *flags, "-c", str(source), "-o", str(obj)], cwd=ROOT, env=env, capture_output=True, timeout=60)
    if result.returncode:
        return [{"compileFailed": True, "flags": flags, "stdout": result.stdout.decode(errors="replace"), "stderr": result.stderr.decode(errors="replace")}], {}
    object_hash = sha(obj.read_bytes())
    stable = WORK / "objects" / (object_hash + ".o")
    stable.parent.mkdir(parents=True, exist_ok=True)
    if not stable.exists():
        stable.write_bytes(obj.read_bytes())
    data = (ROOT / f"extract/arm9/{module}.bin").read_bytes()
    expected_hash = {"itcm": "69b4ab1dc8c4f9c05388bbcc456ba6037fd8f09ab774d65a3eb8adc130e1c1fb",
                     "dtcm": "8b37cdd1c1c304deb8c6355aa56411d80adc4a55d29ccf4b7a52e5afd64d75f4"}[module]
    if sha(data) != expected_hash:
        raise ValueError("Low-level input module differs from the measured native ROM")
    base = 0x01FF8000 if module == "itcm" else 0x027E0000
    boundaries = (ROOT / f"config/arm9/{module}/symbols.txt").read_text()
    records, compiled = [], {}
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        for symbol in elf.get_section_by_name(".symtab").iter_symbols():
            if not symbol.name.startswith(f"native_{module}_") or not isinstance(symbol["st_shndx"], int):
                continue
            address = symbol_address(symbol.name)
            boundary = re.search(rf"^(\S+) kind:function\(arm,size=(0x[0-9a-f]+)\) addr:0x{address:08x}$", boundaries, re.M)
            if not boundary:
                raise ValueError("Unverified function boundary: " + symbol.name)
            size = int(boundary.group(2), 16)
            raw = elf.get_section(symbol["st_shndx"]).data()
            start = symbol["st_value"]
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
                    except UnresolvedNativeSymbol as error:
                        error.details.update(name=symbol.name, module=module, address=hex(address), bytes=size,
                            source=source.relative_to(ROOT).as_posix(), sourceSha256=sha(source.read_bytes()),
                            object=stable.relative_to(ROOT).as_posix(), objectSha256=object_hash, compilerFlags=flags,
                            compilerSha256=sha(COMPILER.read_bytes()), relocationOffset=offset)
                        raise
                    value = struct.unpack_from("<I", code, offset)[0]
                    kind = rel["r_info_type"]
                    if kind == 2:
                        addend = rel["r_addend"] if section["sh_type"] == "SHT_RELA" else value
                        struct.pack_into("<I", code, offset, (target + addend) & 0xFFFFFFFF)
                    elif kind in (1, 28, 29):
                        addend = rel["r_addend"] if section["sh_type"] == "SHT_RELA" else ((value & 0xFFFFFF) << 2)
                        displacement = target + addend - address - offset
                        struct.pack_into("<I", code, offset, value & 0xFF000000 | ((displacement >> 2) & 0xFFFFFF))
                    else:
                        raise ValueError("Unsupported relocation: " + str(kind))
                    relocations.append({"offset": offset, "type": kind, "symbol": name, "target": hex(target), "addend": addend})
            native = data[address - base:address - base + size]
            matched = bytes(code) == native
            entry = {"name": symbol.name, "module": module, "processor": "arm9", "mode": "arm", "address": hex(address), "bytes": size, "compiledBytes": len(code), "matchingBytes": sum(a == b for a, b in zip(native, code)), "exactAfterDeclaredRelocation": matched, "targetSha256": sha(native), "outputSha256": sha(code), "relocations": relocations, "compilerFlags": flags, "object": stable.relative_to(ROOT).as_posix(), "objectSha256": object_hash, "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha(source.read_bytes()), "compilerSha256": sha(COMPILER.read_bytes()), "sectionIndex": symbol["st_shndx"], "sectionOffset": start, "nativeAlias": boundary.group(1), "linked": False}
            records.append(entry)
            if matched:
                compiled[symbol.name] = (entry, bytes(code))
    return records, compiled


def execute(code, address, registers, memory, flags, callees=None, vector=0):
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for location, size in [(0x01FF8000, 0x8000), (0x02000000, 0x500000), (0x03000000, 0x20000), (0x04000000, 0x1000)]:
        engine.mem_map(location, size)
    for location, payload in memory.items():
        engine.mem_write(location, payload)
    engine.mem_write(address, code)
    engine.reg_write(UC_ARM_REG_CPSR, flags)
    for register, value in zip(REGISTERS, registers):
        engine.reg_write(register, value)
    writes = []
    calls = []
    visited = set()
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, location, size, value, user: writes.append([location, size, value]))
    def intercept(uc, pc, size, user):
        if address <= pc < address + len(code):
            visited.add(pc)
        if pc not in (callees or {}):
            return
        arguments = [uc.reg_read(register) for register in REGISTERS[:4]]
        calls.append({"address": hex(pc), "arguments": arguments, "stackArguments": bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 16)).hex()})
        pointers = {0x02223C60, 0x020844D0, 0x01FFB4EC, 0x02049AE4, 0x01FFB340, 0x02061DCC, 0x02223C54, 0x02049AD0, 0x020840A0, 0x02062A10, 0x020633B0}
        if pc in (0x01FFB8BC, 0x020845AC):
            result = [0xFFFFFFFE, 0, 1, 0xFFFFFFFF][vector % 4]
        elif pc == 0x02027F30:
            result = int(vector % 4 != 0)
        elif pc == 0x01FFB35C:
            result = 0x03006000
        elif pc == 0x01FFA6C0:
            result = 0 if vector % 3 == 0 else 0x03004000
        elif pc == 0x01FFA824 and address == 0x01FFA394:
            result = vector % 2
        elif pc in pointers:
            result = 0 if pc == 0x02062A10 and vector % 3 == 0 else 0x03002000
        elif pc in (0x02062A68, 0x02062A78):
            result = (arguments[0] + vector) % 5
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
        uc.reg_write(UC_ARM_REG_CPSR, ((pc + vector + len(calls)) & 15) << 28 | 0x10)
        location = 0x03008000 + (len(calls) % 64) * 4
        uc.mem_write(location, struct.pack("<I", result))
        writes.append([location, 4, result])
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
    engine.hook_add(UC_HOOK_CODE, intercept)
    engine.emu_start(address, 0x04000000, count=2000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x04000000:
        raise ValueError("Low-level oracle did not return within bound")
    return {"registers": [engine.reg_read(x) for x in REGISTERS], "cpsr": engine.reg_read(UC_ARM_REG_CPSR), "writes": writes, "calls": calls, "visitedInstructions": sorted(visited),
            "memory": [sha(bytes(engine.mem_read(location, len(payload)))) for location, payload in memory.items()]}


def oracle(entry, compiled, native):
    address = int(entry["address"], 0)
    rng = random.Random(20261027 + address)
    callees = {int(rel["target"], 0): rel["symbol"] for rel in entry["relocations"] if rel["symbol"].startswith("native_fn_")}
    results = []
    visited = set()
    called = set()
    for index in range(40):
        registers = [rng.getrandbits(32) for _ in REGISTERS]
        registers[:4] = [rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32)]
        registers[-2:] = [0x0301FFF0, 0x04000000]
        memory = {0x01FFF800: rng.randbytes(0x800), 0x021CE000: rng.randbytes(0x10000), 0x02246000: rng.randbytes(0x1000), 0x0301F000: rng.randbytes(0x1000), 0x03002000: rng.randbytes(0x1000), 0x03004000: rng.randbytes(0x1000), 0x03006000: rng.randbytes(0x1000), 0x03008000: rng.randbytes(0x1000)}
        event = bytearray(memory[0x03006000])
        struct.pack_into("<H", event, 2, [0, 1, 2, 0x10, 0xFFF7, 8, 3, 0xFFFF][index % 8])
        memory[0x03006000] = bytes(event)
        if address == 0x01FFA4B4:
            local = bytearray(memory[0x01FFF800])
            struct.pack_into("<I", local, 0x14C, [0, 1, 149, 150, 299, 300, 301, 0xFFFFFFFF][index % 8])
            memory[0x01FFF800] = bytes(local)
        if address == 0x01FF81B4:
            memory[0x020E3724] = struct.pack("<H", index + 1)
        first, second = bytearray(memory[0x03002000]), bytearray(memory[0x03004000])
        struct.pack_into("<I", first, 0, 0x03004000)
        if address == 0x01FFADD8 and index % 2:
            struct.pack_into("<I", first, 0, 0)
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
        if address == 0x01FF8580:
            registers[0] = index % 8
        if address in (0x01FF8448, 0x01FF8488, 0x01FF84F8, 0x01FF851C):
            registers[0] = index % 4
        if address == 0x01FFA394:
            registers[0] = index % 8
        flags = rng.getrandbits(4) << 28 | 0x10
        original = execute(native, address, registers, memory, flags, callees, index)
        rebuilt = execute(compiled, address, registers, memory, flags, callees, index)
        if original != rebuilt:
            raise ValueError(f"Low-level behavior differs at {address:#x} vector {index}")
        visited.update(original["visitedInstructions"])
        called.update(call["address"] for call in original["calls"])
        results.append(sha(json.dumps(original, sort_keys=True).encode()))
    return {"vectors": len(results), "nativeAndRecompiledCalls": len(results) * 2, "instructionLimit": 2000,
            "verifiedReturn": True, "compared": ["r0-r12", "sp", "lr", "cpsr", "ordered-memory-writes", "initialized-memory-regions"], "stateSha256": results,
            "externalCalls": {hex(target): name for target, name in callees.items()},
            "functionInstructionAddressesVisited": [hex(location) for location in sorted(visited)],
            "externalCallTargetsVisited": sorted(called),
            "externalStubContract": "When external calls occur, target-qualified synthetic callees return deterministic values or mapped pointers, clobber caller-saved registers and flags, and write isolated scratch RAM",
            "externalStubDetails": {key: value for key, value in {"0x01ffb35c": "Synthetic mapped event record with varied halfword flags; measured native entry tail-transfers to 0202a634, whose implementation is not executed or credited",
                                    "0x01ffa6c0": "Synthetic lookup returns NULL every third vector or a mapped scratch record; native lookup semantics are not asserted",
                                    "0x01ffb8bc": "Synthetic status returns the caller-compared values -2,0,1,-1; native status implementation is not executed",
                                    "0x020845ac": "Synthetic status returns the caller-compared values -2,0,1,-1; native status implementation is not executed",
                                    "0x02027f30": "Synthetic Boolean gate returns0 or1; native gate implementation is not executed"}.items() if hex(int(key, 0)) in called},
            "inputRestrictions": (["The release halfword starts nonzero; native restart handoff is modeled by an external synthetic callee"] if address == 0x01FF81B4 else
                                  ["Channel argument is 0 through 3; MMIO is isolated synthetic memory"] if address in (0x01FF8448, 0x01FF8488, 0x01FF84F8, 0x01FF851C) else
                                  ["Bank argument is 0 through 7; lookup callees use declared synthetic ID/pointer results"] if address == 0x01FF8580 else []),
            "limitations": ["Synthetic RAM-state comparisons do not establish native gameplay semantics", "External stub contracts compare recovered caller behavior, not the native implementation of callees"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--module", choices=["itcm", "dtcm"], default="itcm")
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
        try:
            records, found = compare(source, args.module, optimization, inline, speed)
        except UnresolvedNativeSymbol as error:
            attempts.append(error.details)
            continue
        attempts.extend(records)
        for name, item in found.items():
            matches.setdefault(name, item)
    binary = (ROOT / f"extract/arm9/{args.module}.bin").read_bytes()
    base = 0x01FF8000 if args.module == "itcm" else 0x027E0000
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
