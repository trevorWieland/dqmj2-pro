import json
import os
import re
import struct
import subprocess
from functools import lru_cache
from pathlib import Path
import utility_runtime
import match_lowlevel
from wave20261104_child_wm_revision_qualify import helper_target, HELPER_NAMES
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import ARM_OP_MEM, ARM_REG_PC
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/wm1104rev/compiler"
COMPILER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
COMPILER_HASH = "7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880"


class InterworkingRequiresLink(ValueError):
    pass


@lru_cache(maxsize=1)
def compiler_pins():
    import match_arm7
    result = {path.relative_to(ROOT).as_posix(): digest for path, digest in match_arm7.tools()}
    result["tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe"] = "89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca"
    return result


@lru_cache(maxsize=1)
def accepted_context():
    return utility_runtime.derive()


def accepted_spec(entry):
    layout, files = accepted_context()
    module = next(module for module in layout["modules"] if module["id"] == entry["module"])
    if entry.get("program") != utility_runtime.PROGRAM or entry["processor"] != module["processor"]:
        raise ValueError("Accepted utility function program or CPU identity changed")
    binary = files[ROOT / module["binary"]]
    address, base = int(entry["address"], 0), int(module["base"], 0)
    size = entry["bytes"]
    if entry["mode"] not in ("arm", "thumb") or address % (4 if entry["mode"] == "arm" else 2) or not base <= address < address + size <= base + len(binary):
        raise ValueError("Accepted utility function lies outside its measured module")
    native = bytes(binary[address - base:address - base + size])
    if module["sha256"] != entry["inputModuleSha256"] or utility_runtime.sha(native) != entry["targetSha256"]:
        raise ValueError("Accepted utility native module or span changed")
    return {"module": module["id"], "program": utility_runtime.PROGRAM, "processor": module["processor"],
            "mode": entry["mode"], "address": address, "base": base, "bytes": size, "name": entry["name"],
            "binary": module["binary"], "inputModuleSha256": module["sha256"]}


def compile_compare(source, spec, optimization=2, inline="off", speed=False):
    compiler = Path(spec.get("compilerPath", COMPILER)).resolve()
    compiler_path = compiler.relative_to(ROOT).as_posix()
    compiler_hash = utility_runtime.sha(compiler.read_bytes())
    if compiler_hash != compiler_pins().get(compiler_path):
        raise ValueError("Utility compiler identity changed")
    flags = match_lowlevel.FLAGS[:]
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
    obj = directory / (utility_runtime.sha((compiler_hash + json.dumps(flags)).encode())[:16] + ".o")
    command = [str(compiler), *flags, "-c", str(source), "-o", str(obj)]
    process = subprocess.run(command, cwd=ROOT, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat")),
                             capture_output=True, text=True, timeout=30)
    if process.returncode:
        return {"command": command, "compileFailed": True, "stdout": process.stdout, "stderr": process.stderr}, None
    digest = utility_runtime.sha(obj.read_bytes())
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
                target = helper_target(name, spec) if name in HELPER_NAMES else match_lowlevel.symbol_address(name)
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
    if utility_runtime.sha(binary) != spec["inputModuleSha256"]:
        raise ValueError("Utility native compiler target module changed")
    native = binary[spec["address"] - spec["base"]:spec["address"] - spec["base"] + spec["bytes"]]
    exact = bytes(output) == native
    record = {"name": spec["name"], "program": utility_runtime.PROGRAM, "processor": spec["processor"], "module": spec["module"],
              "address": hex(spec["address"]), "mode": spec["mode"], "bytes": spec["bytes"], "size": spec["bytes"],
              "compiledBytes": len(output), "matchingBytes": sum(first == second for first, second in zip(output, native)),
              "exactAfterDeclaredRelocation": exact, "relocations": relocations,
              "source": source.relative_to(ROOT).as_posix(), "sourceSha256": utility_runtime.sha(source.read_bytes()),
              "object": stable.relative_to(ROOT).as_posix(), "objectSha256": digest, "compiler": compiler_path,
              "compilerSha256": compiler_hash, "compilerFlags": flags, "sectionIndex": symbol["st_shndx"], "sectionOffset": start,
              "nativeAlias": "func_" + spec["module"].replace("-", "_") + f"_{spec['address']:08x}",
              "inputModuleSha256": spec["inputModuleSha256"], "targetSha256": utility_runtime.sha(native),
              "outputSha256": utility_runtime.sha(output), "linked": False,
              "boundaryEvidence": "Complete matching C span at measured runtime address; Ghidra body plus own PC-relative pool suffix with no intervening function entry"}
    return record, bytes(output) if exact else None
