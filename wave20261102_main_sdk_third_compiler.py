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
                        if not re.fullmatch(r"(?:_(?:[us](?:32|64)|f|d)_\w+|_ll_(?:sdiv|udiv|mod|umod))", name) or rel["r_info_type"] not in (1, 10, 28, 29):
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

