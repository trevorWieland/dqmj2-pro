import os
import re
import struct
import subprocess
from pathlib import Path
import match_runtime as frozen
from project import ROOT,configuration,sha256,read_json
from elftools.elf.elffile import ELFFile
COMPILER=frozen.COMPILER
COMPILER_PINS=frozen.COMPILER_PINS
FLAGS=frozen.FLAGS[:]
WORK=ROOT/'work/msl-float-primitives-20261031'
sha=frozen.sha
BUILTINS={'_dmul':0x02024540,'_deq':0x02025208,'_dadd':0x02023f78}
ADDRESSES={'0202263c','02022684','02022740','02023e48','02023e5c'}


def symbol_address(name):
    return BUILTINS[name] if name in BUILTINS else frozen.symbol_address(name)


FROZEN_SHA='fa61db8211e80a8811323ba5dcea406efd6051ac52fe3f5422ceb00363d42485'

def compare(source, module, optimization, inline, speed=False, thumb=False, compiler=None, processor=None):
    source=Path(source).resolve()
    assert module=='main' and not thumb and processor in [None,'arm946e']
    assert source.is_relative_to(ROOT/'src/runtime/20261031_float_primitives') or source.is_relative_to(ROOT/'nonmatching/main-runtime/20261031-float-primitives-controls')
    names=re.findall(r'\bnative_main_([0-9a-f]{8})\s*\(',source.read_text())
    assert len(names)==1 and names[0] in ADDRESSES
    assert configuration()['romSha256']=='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
    assert sha256(ROOT/'match_runtime.py')==FROZEN_SHA
    seed=next(m for m in read_json(ROOT/'provenance/seed-manifest.json')['modules']if m['name']=='main')
    assert sha256(ROOT/seed['binary'])==seed['sha256']
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
