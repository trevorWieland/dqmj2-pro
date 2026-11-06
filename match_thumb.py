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
from elftools.elf.relocation import RelocationSection
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_CPSR, UC_ARM_REG_PC

OUT = ROOT / "evidence/matches"
WORK = ROOT / "work/thumb-matches"
SOURCE = ROOT / "src/thumb_helpers.c"
COMPILER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
GLOBALS = {"data_021cfcf8": 0x021CFCF8, "data_020e33e4": 0x020E33E4, "data_021d1540": 0x021D1540}
ADDRESSES = [0x0208B8FC, 0x0208B900, 0x0208BAA0, 0x0208D744, 0x0208D754, 0x0208D7F8, 0x0208EB10, 0x0208EC10]
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_functions(obj):
    results = {}
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        symbols = elf.get_section_by_name(".symtab")
        for symbol in symbols.iter_symbols():
            if not symbol.name.startswith("native_main_"):
                continue
            section = elf.get_section(symbol["st_shndx"])
            start = symbol["st_value"] & ~1
            raw = section.data()[start:start + symbol["st_size"]]
            code = bytearray(raw)
            relocations = []
            for reloc_section in elf.iter_sections():
                if not isinstance(reloc_section, RelocationSection) or reloc_section["sh_info"] != symbol["st_shndx"]:
                    continue
                symtab = elf.get_section(reloc_section["sh_link"])
                for rel in reloc_section.iter_relocations():
                    offset = rel["r_offset"] - start
                    if offset < 0 or offset >= len(code):
                        continue
                    target = symtab.get_symbol(rel["r_info_sym"]).name
                    if rel["r_info_type"] != 2 or target not in GLOBALS:
                        raise ValueError("Unsupported Thumb relocation: " + target)
                    addend = rel["r_addend"] if rel.is_RELA() else struct.unpack_from("<I", code, offset)[0]
                    value = (GLOBALS[target] + addend) & 0xFFFFFFFF
                    struct.pack_into("<I", code, offset, value)
                    relocations.append({"offset": offset, "type": "R_ARM_ABS32", "target": target, "targetAddress": hex(GLOBALS[target]), "addend": addend})
            results[symbol.name] = {"bytes": bytes(code), "rawBytes": raw, "relocations": relocations}
    return results


def execute(code, placement, registers, memory):
    engine = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    for address, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (0x04000000, 0x1000), (0x06000000, 0x10000)]:
        engine.mem_map(address, size)
    for address, data in memory.items():
        engine.mem_write(address, data)
    engine.mem_write(placement, code)
    engine.reg_write(UC_ARM_REG_CPSR, 0x20000030)
    for register, value in zip(REGISTERS, registers):
        engine.reg_write(register, value)
    writes = []
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value]))
    engine.emu_start(placement | 1, 0x04000000, count=128)
    if engine.reg_read(UC_ARM_REG_LR) != 0x04000000 or engine.reg_read(UC_ARM_REG_PC) != 0x04000000:
        raise ValueError("Unexpected return state")
    return {"registers": [engine.reg_read(x) for x in REGISTERS], "cpsr": engine.reg_read(UC_ARM_REG_CPSR), "writes": writes, "targetBytes": bytes(engine.mem_read(0x03000000, 0x2000)).hex(), "globals": [[address, bytes(engine.mem_read(address, len(data))).hex()] for address, data in memory.items() if address < 0x03000000]}


def oracle(address, native, rebuilt):
    rng = random.Random(20261026 + address)
    vectors = []
    for index in range(36):
        values = [rng.getrandbits(32) for _ in REGISTERS]
        values[0] = [0, 1, 0xFFFFFFFF, 0x80000000][index % 4] if address in {0x0208B8FC, 0x0208B900, 0x0208BAA0, 0x0208D744} else 0x03000000
        if address == 0x0208D7F8:
            values[0] = 0x03000000
        values[-2] = 0x0301FFF0
        values[-1] = 0x04000000
        data = bytearray(rng.randbytes(0x2000))
        struct.pack_into("<I", data, 100, [0, 1, 0x80000000, rng.getrandbits(32)][index % 4])
        memory = {0x03000000: bytes(data), 0x020E33E4: struct.pack("<4I", 0, 0x03001000, 0, 0), 0x021CFCF8: rng.randbytes(0x100), 0x021D1540: rng.randbytes(0x100)}
        original = execute(native, address, values, memory)
        compiled = execute(rebuilt, 0x06000000, values, memory)
        if original != compiled:
            raise ValueError(f"Thumb oracle mismatch {hex(address)} vector {index}")
        vectors.append({"index": index, "stateSha256": sha(json.dumps(original, sort_keys=True).encode()), "writes": original["writes"]})
    return {"vectors": len(vectors), "executions": 2 * len(vectors), "instructionLimit": 128, "compared": ["r0-r12", "sp", "lr", "cpsr", "ordered-memory-writes", "target-buffer", "global-buffers"], "results": vectors}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    flags = json.loads((ROOT / "oracle/results.json").read_text())["compiler"]["flags"] + ["-thumb"]
    obj = WORK / "thumb_helpers.o"
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat"))
    result = subprocess.run([str(COMPILER), *flags, "-c", str(SOURCE), "-o", str(obj)], cwd=ROOT, env=env, capture_output=True, timeout=30)
    (WORK / "compile.stdout.txt").write_bytes(result.stdout)
    (WORK / "compile.stderr.txt").write_bytes(result.stderr)
    result.check_returncode()
    functions = load_functions(obj)
    arm9 = (ROOT / "extract/arm9/arm9.bin").read_bytes()
    rom_hash = sha((ROOT / "inputs/game.nds").read_bytes())
    if rom_hash != "674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6":
        raise ValueError("ROM namespace differs from measured modified-build input")
    report = {"schemaVersion": 1, "date": "2026-10-26", "romSha256": rom_hash, "module": "main", "source": "src/thumb_helpers.c", "sourceSha256": sha(SOURCE.read_bytes()), "object": "work/thumb-matches/thumb_helpers.o", "objectSha256": sha(obj.read_bytes()), "compilerSha256": sha(COMPILER.read_bytes()), "compilerFlags": flags, "moduleInputSha256": sha(arm9), "wholeModuleLinked": False, "functions": []}
    symbols = (ROOT / "config/arm9/symbols.txt").read_text()
    for address in ADDRESSES:
        boundary = re.search(rf"^func_{address:08x} kind:function\(thumb,size=(0x[0-9a-f]+)\) addr:0x{address:08x}$", symbols, re.M)
        if not boundary:
            raise ValueError("Missing native Thumb boundary")
        size = int(boundary.group(1), 16)
        name = f"native_main_{address:08x}"
        if name not in functions:
            continue
        function = functions[name]
        native = arm9[address - 0x02000000:address - 0x02000000 + size]
        compiled = function["bytes"]
        match = native == compiled
        entry = {"name": name, "originalSymbol": f"func_{address:08x}", "address": hex(address), "mode": "thumb", "expectedBytes": size, "compiledBytes": len(compiled), "nativeSha256": sha(native), "compiledSha256": sha(compiled), "rawObjectBytesSha256": sha(function["rawBytes"]), "functionMatched": match, "relocations": function["relocations"], "linked": False}
        entry.update(module="main", source="src/thumb_helpers.c", object="work/thumb-matches/thumb_helpers.o", size=size, matchingBytes=size if match else 0, exactBytes=match and native == function["rawBytes"], exactAfterDeclaredRelocation=match, compilerFlags=flags, sha256=sha(compiled))
        if match:
            entry["oracle"] = oracle(address, native, compiled)
            (WORK / (name + ".bin")).write_bytes(compiled)
        else:
            entry.update(nativeHex=native.hex(), compiledHex=compiled.hex(), failure="Compiler bytes differ after documented relocation resolution")
        report["functions"].append(entry)
    report["matchedFunctions"] = sum(x["functionMatched"] for x in report["functions"])
    report["matches"] = report["functions"]
    report["allMatched"] = len(report["functions"]) == len(ADDRESSES) and all(x["functionMatched"] for x in report["functions"])
    report["executions"] = sum(x.get("oracle", {}).get("executions", 0) for x in report["functions"])
    (OUT / "thumb.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    with (OUT / "thumb-attempts.jsonl").open("a", encoding="utf-8") as history:
        history.write(json.dumps(report, separators=(",", ":")) + "\n")
    print(json.dumps({"functions": [{k: x[k] for k in ["name", "functionMatched", "expectedBytes", "compiledBytes"]} for x in report["functions"]], "executions": report["executions"]}, indent=2))
    if not report["allMatched"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
