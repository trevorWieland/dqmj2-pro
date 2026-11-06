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
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_CPSR, UC_ARM_REG_PC

SOURCE = ROOT / "src/overlay_004.c"
COMPILER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
WORK = ROOT / "work/overlay004-matches"
OUT = ROOT / "evidence/matches"
ADDRESSES = [0x021D7240, 0x021D7258, 0x021D7300]
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def execute(code, address, registers, memory, cpsr):
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    engine.mem_map(0x02000000, 0x400000)
    engine.mem_map(0x03000000, 0x20000)
    engine.mem_map(0x04000000, 0x1000)
    for location, data in memory.items():
        engine.mem_write(location, data)
    engine.mem_write(address, code)
    engine.reg_write(UC_ARM_REG_CPSR, cpsr)
    for register, value in zip(REGISTERS, registers):
        engine.reg_write(register, value)
    writes = []
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, location, size, value, user: writes.append([location, size, value]))
    engine.emu_start(address, 0x04000000, count=128)
    if engine.reg_read(UC_ARM_REG_PC) != 0x04000000:
        raise ValueError("Callback wrapper did not reach return sentinel")
    return {"registers": [engine.reg_read(x) for x in REGISTERS], "cpsr": engine.reg_read(UC_ARM_REG_CPSR), "writes": writes, "target": bytes(engine.mem_read(0x03002000, 4)).hex(), "stack": bytes(engine.mem_read(0x0301FF00, 0x100)).hex()}


def oracle(address, native, compiled):
    rng = random.Random(20261026 + address)
    results = []
    for index in range(36):
        callback = [0, 0x03001000, 0x03001101][index % 3]
        registers = [rng.getrandbits(32) for _ in REGISTERS]
        registers[0] = callback
        registers[2] = 0x03002000
        registers[-2] = 0x0301FFF0
        registers[-1] = 0x04000000
        memory = {0x03001000: struct.pack("<5I", 0xE59F1008, 0xE3A0205A, 0xE5812000, 0xE12FFF1E, 0x03002000), 0x03001100: struct.pack("<3H", 0x215A, 0x6011, 0x4770), 0x03002000: bytes(4), 0x0301FF00: rng.randbytes(0x100)}
        cpsr = (rng.getrandbits(4) << 28) | 0x10
        original = execute(native, address, registers, memory, cpsr)
        rebuilt = execute(compiled, address, registers, memory, cpsr)
        if original != rebuilt:
            raise ValueError(f"Overlay callback oracle mismatch {hex(address)} {index}")
        if address == 0x021D7240:
            if original["registers"][0] != (~callback & 0xFFFFFFFF):
                raise ValueError("Unexpected callback complement result")
            expected = "5a000000" if callback else "00000000"
            if original["target"] != expected:
                raise ValueError("Callback side effect differs from isolated test contract")
        elif original["registers"] != registers or original["cpsr"] != cpsr or original["writes"]:
            raise ValueError("No-op changed isolated state")
        results.append({"index": index, "callback": hex(callback), "stateSha256": sha(json.dumps(original, sort_keys=True).encode()), "memoryWrites": original["writes"]})
    return {"vectors": len(results), "executions": 2 * len(results), "instructionLimit": 128, "callbackModes": ["null", "ARM", "Thumb"], "compared": ["r0-r12", "sp", "lr", "cpsr", "ordered-writes", "stack", "callback-target"], "results": results}


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    flags = json.loads((ROOT / "oracle/results.json").read_text())["compiler"]["flags"]
    obj = WORK / "overlay_004.o"
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat"))
    result = subprocess.run([str(COMPILER), *flags, "-c", str(SOURCE), "-o", str(obj)], cwd=ROOT, env=env, capture_output=True, timeout=30)
    (WORK / "compile.stdout.txt").write_bytes(result.stdout)
    (WORK / "compile.stderr.txt").write_bytes(result.stderr)
    result.check_returncode()
    compiled = {}
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        for symbol in elf.get_section_by_name(".symtab").iter_symbols():
            if symbol.name.startswith("native_ov004_"):
                section = elf.get_section(symbol["st_shndx"])
                compiled[symbol.name] = section.data()[symbol["st_value"]:symbol["st_value"] + symbol["st_size"]]
    rom_sha = sha((ROOT / "inputs/game.nds").read_bytes())
    if rom_sha != "674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6":
        raise ValueError("Unexpected ROM input namespace")
    native_module = (ROOT / "extract/arm9_overlays/ov004.bin").read_bytes()
    report = {"schemaVersion": 1, "date": "2026-10-26", "romSha256": rom_sha, "module": "ov004", "source": "src/overlay_004.c", "sourceSha256": sha(SOURCE.read_bytes()), "object": "work/overlay004-matches/overlay_004.o", "objectSha256": sha(obj.read_bytes()), "compilerSha256": sha(COMPILER.read_bytes()), "compilerFlags": flags, "moduleInputSha256": sha(native_module), "wholeModuleLinked": False, "matches": []}
    symbols = (ROOT / "config/arm9/overlays/ov004/symbols.txt").read_text()
    for address in ADDRESSES:
        boundary = re.search(rf"^func_ov004_{address:08x} kind:function\(arm,size=(0x[0-9a-f]+)\) addr:0x{address:08x}$", symbols, re.M)
        if not boundary:
            raise ValueError("Missing unprotected ARM function boundary")
        size = int(boundary.group(1), 16)
        name = f"native_ov004_{address:08x}"
        original = native_module[address - 0x021D7240:address - 0x021D7240 + size]
        rebuilt = compiled[name]
        matched = original == rebuilt
        entry = {"name": name, "originalSymbol": f"func_ov004_{address:08x}", "module": "ov004", "address": hex(address), "mode": "arm", "size": size, "matchingBytes": size if matched else 0, "source": report["source"], "object": report["object"], "compilerFlags": flags, "nativeSha256": sha(original), "compiledSha256": sha(rebuilt), "sha256": sha(rebuilt), "compiledBytes": len(rebuilt), "exactBytes": matched, "functionMatched": matched, "linked": False, "relocations": []}
        if matched:
            entry["oracle"] = oracle(address, original, rebuilt)
        else:
            entry.update(nativeHex=original.hex(), compiledHex=rebuilt.hex(), failure="Compiler output differs from unprotected native function")
        report["matches"].append(entry)
    report["allMatched"] = all(entry["functionMatched"] for entry in report["matches"])
    report["executions"] = sum(entry.get("oracle", {}).get("executions", 0) for entry in report["matches"])
    (OUT / "overlay004.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    with (OUT / "overlay004-attempts.jsonl").open("a", encoding="utf-8") as history:
        history.write(json.dumps(report, separators=(",", ":")) + "\n")
    print(json.dumps({"allMatched": report["allMatched"], "executions": report["executions"], "matches": [{key: entry[key] for key in ["name", "size", "compiledBytes", "exactBytes"]} for entry in report["matches"]]}, indent=2))
    if not report["allMatched"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
