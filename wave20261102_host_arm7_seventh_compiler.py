import json
import os
import re
import struct
import subprocess
import hashlib
from functools import lru_cache
from pathlib import Path
import match_arm7
import match_lowlevel
from project import ROOT
from elftools.elf.elffile import ELFFile

WORK = ROOT / 'work/parallel-wave20261102/host-arm7-seventh/compiled'
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'
FLAGS = [*match_lowlevel.FLAGS, '-lang', 'c99']

class InterworkingRequiresLink(ValueError):
    pass

def sha(data):
    return hashlib.sha256(data).hexdigest()

@lru_cache(maxsize=1)
def compiler_pins():
    rows = {p.relative_to(ROOT).as_posix(): h for p, h in match_arm7.tools()}
    rows['tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'] = '89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca'
    return rows

def compile_compare(source, spec, optimization=2, inline="off", speed=False):
    compiler = Path(spec.get("compilerPath", COMPILER)).resolve()
    compiler_path = compiler.relative_to(ROOT).as_posix()
    compiler_hash = sha(compiler.read_bytes())
    if compiler_hash != compiler_pins().get(compiler_path):
        raise ValueError("Utility compiler identity changed")
    flags = FLAGS[:]
    flags[0] = f"-O{optimization}"
    flags[flags.index("-proc") + 1] = spec.get("compilerProc", "arm946e" if spec["processor"] == "arm9" else "arm7tdmi")
    flags[flags.index("-inline") + 1] = inline
    if spec.get("interworking") is False:
        flags[flags.index("-interworking")] = "-nointerworking"
    if speed:
        flags.extend(["-opt", "speed"])
    if spec["mode"] == "thumb":
        flags.append("-thumb")
    directory = WORK / "compile" / source.stem
    directory.mkdir(parents=True, exist_ok=True)
    obj = directory / (sha((compiler_hash + json.dumps(flags)).encode())[:16] + ".o")
    command = [str(compiler), *flags, "-c", str(source), "-o", str(obj)]
    process = subprocess.run(command, cwd=ROOT, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat")),
                             capture_output=True, text=True, timeout=30)
    if process.returncode:
        return {"command": command, "compileFailed": True, "stdout": process.stdout, "stderr": process.stderr}, None
    digest = sha(obj.read_bytes())
    stable = WORK / "objects" / (digest + ".o")
    stable.parent.mkdir(exist_ok=True)
    if not stable.exists():
        stable.write_bytes(obj.read_bytes())
    relocations = []
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        symbol = next(symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols() if symbol.name == spec["name"])
        start = symbol["st_value"] & ~1
        output = bytearray(elf.get_section(symbol["st_shndx"]).data()[start:start + symbol["st_size"]])
        for section in elf.iter_sections():
            if section["sh_type"] not in ("SHT_REL", "SHT_RELA") or section["sh_info"] != symbol["st_shndx"]:
                continue
            table = elf.get_section(section["sh_link"])
            for relocation in section.iter_relocations():
                at = relocation["r_offset"] - start
                if not 0 <= at < len(output):
                    continue
                name = table.get_symbol(relocation["r_info_sym"]).name
                target = match_lowlevel.symbol_address(name)
                kind = relocation["r_info_type"]
                value = struct.unpack_from("<I", output, at)[0]
                addend = relocation["r_addend"] if section["sh_type"] == "SHT_RELA" else value
                mode = "data" if "_data_" in name else "thumb" if target & 1 or re.search(r"_thumb_[0-9a-f]{8}$", name) else "arm"
                if kind == 2:
                    if mode == "thumb":
                        target |= 1
                    value = target + addend
                elif kind in (1, 28, 29):
                    if section["sh_type"] != "SHT_RELA":
                        raise ValueError("Utility ARM C branch requires an explicit RELA addend")
                    displacement = (target & ~1) + addend - spec["address"] - at
                    if mode == "thumb":
                        if spec["processor"] != "arm9" or not value & 0x01000000 or kind == 29:
                            raise InterworkingRequiresLink("ARM interworking jump requires a measured veneer")
                        if value >> 28 != 14:
                            raise InterworkingRequiresLink("Conditional ARM call cannot become unconditional BLX without a real linker veneer")
                        value = 0xFA000000 | ((displacement & 2) << 23) | ((displacement >> 2) & 0xFFFFFF)
                    else:
                        value = value & 0xFF000000 | ((displacement >> 2) & 0xFFFFFF)
                elif kind == 10 and spec["mode"] == "thumb":
                    high, low = value & 0xFFFF, value >> 16
                    if high & 0xF800 != 0xF000 or low & 0xF800 != 0xF800:
                        raise ValueError("Unexpected compiler Thumb call form")
                    if section["sh_type"] != "SHT_RELA":
                        raise ValueError("Utility Thumb C call requires an explicit RELA addend")
                    place = spec["address"] + at
                    displacement = (target & ~1) + addend - place
                    if mode == "arm":
                        if spec["processor"] != "arm9":
                            raise InterworkingRequiresLink("ARMv4T interworking needs a measured veneer")
                        displacement += place & 2
                        low = 0xE800
                        if displacement & 3:
                            raise ValueError("Utility Thumb-to-ARM BLX target is not word-aligned")
                    if displacement & 1 or not -0x400000 <= displacement < 0x400000:
                        raise ValueError("Utility Thumb call is out of range")
                    high = 0xF000 | (displacement >> 12) & 0x7FF
                    low = low & 0xF800 | (displacement >> 1) & 0x7FF
                    value = high | low << 16
                else:
                    raise ValueError("Unsupported utility C relocation")
                struct.pack_into("<I", output, at, value & 0xFFFFFFFF)
                relocations.append({"offset": at, "type": kind, "symbol": name, "target": hex(target), "targetMode": mode, "addend": addend})
    binary = (ROOT / spec["binary"]).read_bytes()
    if sha(binary) != spec["inputModuleSha256"]:
        raise ValueError("Utility native compiler target module changed")
    native = binary[spec["address"] - spec["base"]:spec["address"] - spec["base"] + spec["bytes"]]
    exact = bytes(output) == native
    record = {"name": spec["name"], "program": '', "processor": spec["processor"], "module": spec["module"],
              "address": hex(spec["address"]), "mode": spec["mode"], "bytes": spec["bytes"], "size": spec["bytes"],
              "compiledBytes": len(output), "matchingBytes": sum(first == second for first, second in zip(output, native)),
              "exactAfterDeclaredRelocation": exact, "relocations": relocations,
              "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha(source.read_bytes()),
              "object": stable.relative_to(ROOT).as_posix(), "objectSha256": digest, "compiler": compiler_path,
              "compilerSha256": compiler_hash, "compilerFlags": flags, "sectionIndex": symbol["st_shndx"], "sectionOffset": start,
              "nativeAlias": "func_" + spec["module"].replace("-", "_") + f"_{spec['address']:08x}",
              "inputModuleSha256": spec["inputModuleSha256"], "targetSha256": sha(native),
              "outputSha256": sha(output), "linked": False,
              "boundaryEvidence": "Complete matching C span at measured runtime address; Ghidra body plus own PC-relative pool suffix with no intervening function entry"}
    return record, bytes(output) if exact else None
