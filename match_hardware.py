import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
from pathlib import Path
from project import ROOT, configuration, native_dependencies, now, sha256, verify_inputs, write_json

ASSEMBLER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwasmarm.exe"
ASSEMBLER_HASH = "e928cbcce71d687fadf25cf426280f23252e2aaae897fc2ce4e5570d8554dc8c"
WORK = ROOT / "work/hardware-recovery"


def blocks(text):
    expression = r"    (arm|thumb)_func_start (\w+)\r?\n(.*?)    (?:arm|thumb)_func_end \2"
    for mode, symbol, body in re.findall(expression, text, re.S):
        location = re.search(r"^" + re.escape(symbol) + r": ; 0x([0-9a-f]+)", body, re.M)
        if location:
            yield mode, symbol, int(location[1], 16), body


def prepare(mode, original, address, body, binary, size):
    lines = [line.split(";", 1)[0].rstrip() for line in body.splitlines()]
    lines = [line for line in lines if line.strip()]
    hardware = [line.strip() for line in lines if re.search(r"\b(mcr|mrc|mrs|msr|swi)\b", line)]
    if not hardware or size > 128 or size < 4:
        return None
    if any(re.search(r"\b(bl|blx)\b", line) or ".byte" in line or ".hword" in line for line in lines):
        return None
    if any(re.search(r"\bfunc_\w+", line) for line in lines if not line.startswith(original + ":")):
        return None
    if mode == "thumb" and address % 4 and any(".word" in line for line in lines):
        return None
    name = f"native_main_hw_{address:08x}"
    translated = []
    for line in lines:
        if line.startswith(original + ":"):
            line = name + ":"
        pool = re.match(r"(\.L_([0-9a-f]+)):\s*\.word .+", line.strip())
        if pool:
            label, location = pool[1], int(pool[2], 16)
            if not address <= location < address + size or not any("ldr" in item and label in item for item in lines):
                return None
            value = struct.unpack_from("<I", binary, location - 0x02000000)[0]
            line = f"{label}: .word {value:#x}"
        if re.search(r"\b(mcr|mrc)\b", line):
            line = line.replace("#", "")
        translated.append(line)
    code = [".section .text", "." + mode, ".global " + name, ".type " + name + ", @function", *translated, ".size " + name + ", .-" + name]
    return name, "\n".join(code) + "\n", hardware


def main():
    config = configuration()
    inputs = verify_inputs(config)
    if sha256(ASSEMBLER) != ASSEMBLER_HASH:
        raise ValueError("Assembler identity differs")
    native_dependencies(config)
    from elftools.elf.elffile import ELFFile
    WORK.mkdir(parents=True, exist_ok=True)
    asm = ROOT / "asm/_dsd_gap@main_3.s"
    if not asm.exists():
        subprocess.run([str(config["dsd"]), "dis", "--config-path", str(ROOT / "config/arm9/config.yaml"), "--asm-path", str(ROOT / "asm")], cwd=ROOT, check=True, timeout=180)
    symbols = (ROOT / "config/arm9/symbols.txt").read_text()
    sizes = {int(address, 16): int(size, 16) for _, size, address in re.findall(r"^(\S+) kind:function\((?:arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)", symbols, re.M)}
    binary = (ROOT / "extract/arm9/arm9.bin").read_bytes()
    report = {"schemaVersion": 1, "createdUtc": now(), "romSha256": inputs["rom"]["sha256"], "module": "main", "matches": [], "attempts": [], "sourceReconstructionComplete": False, "reproduction": ["match_hardware.py"], "limitations": ["Only measured hardware/system-call routines are reconstructed as mnemonic assembly", "Cache, coprocessor and BIOS physical effects are not asserted by static matching", "Normal game logic is excluded from assembly recovery"]}
    environment = dict(os.environ, LM_LICENSE_FILE=str(config["license"]))
    for mode, original, address, body in blocks(asm.read_text()):
        if address not in sizes:
            continue
        result = prepare(mode, original, address, body, binary, sizes[address])
        if result is None:
            continue
        name, source_text, instructions = result
        trial = WORK / (name + ".s")
        obj = WORK / (name + ".o")
        trial.write_text(source_text)
        flags = ["-proc", "arm5TE", "-c"]
        command = [str(ASSEMBLER), *flags, str(trial), "-o", str(obj)]
        process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, errors="replace", timeout=30)
        attempt = {"name": name, "address": hex(address), "mode": mode, "command": command, "exitCode": process.returncode, "stdout": process.stdout, "stderr": process.stderr}
        if process.returncode == 0:
            with obj.open("rb") as stream:
                elf = ELFFile(stream)
                section = elf.get_section_by_name(".text")
                code = section.data()
                relocated = any(s["sh_type"] in ("SHT_REL", "SHT_RELA") and s["sh_size"] for s in elf.iter_sections())
                symbol = next(s for s in elf.get_section_by_name(".symtab").iter_symbols() if s.name == name)
                correct_size = symbol["st_size"] == sizes[address]
            target = binary[address - 0x02000000:address - 0x02000000 + sizes[address]]
            exact = code == target and not relocated and correct_size
            attempt.update({"nativeBytes": len(target), "compiledBytes": len(code), "exactBytes": exact, "hasRelocations": relocated})
            if exact:
                source = ROOT / "src/hardware/main" / (name + ".s")
                source.parent.mkdir(parents=True, exist_ok=True)
                if source.exists() and source.read_text() != source_text:
                    raise ValueError("An accepted hardware source changed")
                if not source.exists():
                    source.write_text(source_text)
                object_hash = sha256(obj)
                stable = WORK / "objects" / (object_hash + ".o")
                stable.parent.mkdir(exist_ok=True)
                if not stable.exists():
                    shutil.copy2(obj, stable)
                justification = {"kind": "hardware-or-bios-instruction", "instructions": instructions, "sourceFormat": "mnemonic-assembly", "rawExecutableBytesStoredAsSource": False, "limitation": "No assertion of complete physical cache, interrupt or BIOS behavior"}
                report["matches"].append({"name": name, "module": "main", "mode": mode, "address": hex(address), "size": len(target), "bytes": len(target), "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha256(source), "object": stable.relative_to(ROOT).as_posix(), "objectSha256": object_hash, "compilerSha256": ASSEMBLER_HASH, "compilerFlags": flags, "nativeAlias": original, "exactBytes": True, "exactAfterDeclaredRelocation": True, "nativeSha256": hashlib.sha256(target).hexdigest(), "outputSha256": hashlib.sha256(code).hexdigest(), "relocations": [], "assemblyJustification": justification})
        report["attempts"].append(attempt)
    write_json(ROOT / "evidence/matches/hardware-main.json", report)
    if inputs != verify_inputs(config):
        raise ValueError("Inputs changed during hardware reconstruction")
    print({"hardwareFunctions": len(report["matches"]), "bytes": sum(r["size"] for r in report["matches"]), "attempts": len(report["attempts"])})


if __name__ == "__main__":
    main()
