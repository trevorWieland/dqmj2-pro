import hashlib
import json
import os
import re
import struct
import subprocess
import sys
from pathlib import Path
import arm7_runtime
import match_arm7 as common

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "deps/native"))
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_GRP_JUMP, CS_GRP_CALL
from capstone.arm import ARM_OP_MEM, ARM_REG_PC
from elftools.elf.elffile import ELFFile

ASSEMBLER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwasmarm.exe"
ASSEMBLER_HASH = "e928cbcce71d687fadf25cf426280f23252e2aaae897fc2ce4e5570d8554dc8c"
COMPILER = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
COMPILER_HASH = "7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880"
WORK = ROOT / "work/lowlevel-recovery/arm7-boot"
FUNCTIONS = {0x02380000: 0x118, 0x02380118: 0x74, 0x0238018C: 0x78}
CODE_RANGES = {0x02380000: [["0x02380000", "0x023800e4"]],
               0x02380118: [["0x02380118", "0x02380184"], ["0x02380188", "0x0238018c"]],
               0x0238018C: [["0x0238018c", "0x023801fc"]]}
JUSTIFICATIONS = {
    0x02380000: "ARM7 startup sets privileged CPSR modes and banked stack pointers, copies hardware handoff buffers, installs a runtime vector and branches to the loaded entry with a non-C return address",
    0x02380118: "Native startup autoload copy/zero routine has a stack-free ABI that clobbers r4-r7 rather than preserving normal C callee-saved registers; it runs as part of the measured module-loader handoff",
    0x0238018C: "ARM7 startup probes physical RAM aliasing through fixed hardware addresses before entering the loaded application; volatile hardware access and boot handoff are explicitly scoped"
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source_text(address, size, binary, function):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = {}
    pools = {}
    for first, last in function["ranges"]:
        start, end = int(first, 0), int(last, 0)
        for instruction in decoder.disasm(binary[start - 0x02380000:end - 0x02380000], start):
            instructions[instruction.address] = instruction
            for operand in instruction.operands:
                if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC:
                    target = instruction.address + 8 + operand.mem.disp
                    if not address <= target < address + size:
                        raise ValueError("Startup literal is outside its verified source span")
                    pools[target] = struct.unpack_from("<I", binary, target - 0x02380000)[0]
    name = f"native_arm7_boot_hw_{address:08x}"
    lines = [".section .text", ".arm", ".global " + name, ".type " + name + ", @function", name + ":"]
    externs = set()
    for location in range(address, address + size, 4):
        if location in pools:
            lines.append(f"local_{location:08x}: .word {pools[location]:#x}")
            continue
        if location not in instructions:
            raise ValueError(f"Unexplained startup word at {location:#x}; refusing instruction-word substitution")
        instruction = instructions[location]
        mnemonic, operands = instruction.mnemonic, instruction.op_str.replace("apsr", "cpsr")
        for alias, register in (("sb", "r9"), ("sl", "r10"), ("fp", "r11")):
            operands = re.sub(r"\b" + alias + r"\b", register, operands)
        if mnemonic in ("stm", "ldm"):
            mnemonic += "ia"
        if mnemonic in ("lsl", "lsr", "asr", "ror"):
            parts = [part.strip() for part in operands.split(",")]
            mnemonic, operands = "mov", f"{parts[0]}, {parts[1]}, {mnemonic} {parts[2]}"
        if "[pc" in operands:
            target = instruction.address + 8 + instruction.operands[-1].mem.disp
            operands = operands.split(",", 1)[0] + f", local_{target:08x}"
        if (instruction.group(CS_GRP_JUMP) or instruction.group(CS_GRP_CALL)) and instruction.operands[0].type == 2:
            target = instruction.operands[0].imm
            if address <= target < address + size:
                operands = f"local_{target:08x}"
            elif target in FUNCTIONS:
                operands = f"native_arm7_boot_hw_{target:08x}"
                externs.add(operands)
            else:
                raise ValueError("Unresolved startup branch target")
        lines.extend([f"local_{location:08x}:", "    " + mnemonic + " " + operands])
    lines.append(".size " + name + ", .-" + name)
    return name, "".join(".extern " + external + "\n" for external in sorted(externs)) + "\n".join(lines) + "\n"


def object_bytes(obj, symbol_name, address):
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        symbol = next(symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols() if symbol.name == symbol_name)
        section = elf.get_section(symbol["st_shndx"])
        code = bytearray(section.data())
        relocations = []
        for reloc in elf.iter_sections():
            if reloc["sh_type"] not in ("SHT_REL", "SHT_RELA") or reloc["sh_info"] != symbol["st_shndx"]:
                continue
            table = elf.get_section(reloc["sh_link"])
            for item in reloc.iter_relocations():
                name = table.get_symbol(item["r_info_sym"]).name
                target = int(re.search(r"([0-9a-f]{8})$", name).group(1), 16)
                at, kind = item["r_offset"], item["r_info_type"]
                value = struct.unpack_from("<I", code, at)[0]
                addend = item["r_addend"] if reloc["sh_type"] == "SHT_RELA" else value
                if kind == 2:
                    value = target + addend
                elif kind in (1, 28, 29):
                    if reloc["sh_type"] == "SHT_REL":
                        addend = (value & 0xFFFFFF) << 2
                        if addend & 0x2000000:
                            addend -= 0x4000000
                    value = (value & 0xFF000000) | (((target + addend - address - at) >> 2) & 0xFFFFFF)
                else:
                    raise ValueError("Unsupported ARM7 startup relocation")
                struct.pack_into("<I", code, at, value & 0xFFFFFFFF)
                relocations.append({"offset": at, "type": kind, "symbol": name, "target": hex(target), "addend": addend})
        return bytes(code), relocations, symbol["st_shndx"], symbol["st_value"], section.name


def compile_source(source, tool, flags, symbol_name, address, environment):
    obj = WORK / (source.stem + ".o")
    command = [str(tool), *flags, str(source), "-o", str(obj)]
    result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=30)
    attempt = {"command": command, "exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    if result.returncode:
        return attempt, None
    object_hash = sha(obj.read_bytes())
    stable = WORK / (object_hash + ".o")
    if not stable.exists():
        stable.write_bytes(obj.read_bytes())
    code, relocations, index, offset, section = object_bytes(obj, symbol_name, address)
    entry = {"name": symbol_name, "symbol": symbol_name, "module": "arm7-boot", "processor": "arm7", "address": hex(address),
             "bytes": len(code), "size": len(code), "compiledBytes": len(code),
             "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha(source.read_bytes()),
             "object": stable.relative_to(ROOT).as_posix(), "objectSha256": object_hash,
             "compilerSha256": sha(tool.read_bytes()), "compilerFlags": flags, "relocations": relocations,
             "sectionIndex": index, "sectionOffset": offset, "section": section, "outputSha256": sha(code), "linked": False}
    return attempt, (entry, code)


def main():
    if sha(ASSEMBLER.read_bytes()) != ASSEMBLER_HASH or sha(COMPILER.read_bytes()) != COMPILER_HASH:
        raise ValueError("ARM7 startup tool identities changed")
    layout = arm7_runtime.derive((ROOT / "extract/arm7/arm7.bin").read_bytes())
    if layout != json.loads(arm7_runtime.MANIFEST.read_text()):
        raise ValueError("ARM7 startup layout is stale")
    binary = (ROOT / "extract/arm7/runtime/arm7-boot.bin").read_bytes()
    WORK.mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat"))
    matches, attempts = [], []
    for address, size in FUNCTIONS.items():
        name, text = source_text(address, size, binary, {"ranges": CODE_RANGES[address]})
        source = ROOT / f"src/arm7/boot/{name}.s"
        source.parent.mkdir(parents=True, exist_ok=True)
        if source.exists() and source.read_text() != text:
            raise ValueError("Refusing to alter an accepted startup assembly source")
        source.write_text(text)
        attempt, result = compile_source(source, ASSEMBLER, ["-proc", "arm4t", "-c"], name, address, environment)
        attempts.append(attempt)
        if result is None:
            continue
        entry, code = result
        native = binary[address - 0x02380000:address - 0x02380000 + size]
        if code != native:
            attempt.update(exactBytes=False, nativeHex=native.hex(), compiledHex=code.hex())
            continue
        entry.update(mode="arm", exactAfterDeclaredRelocation=True, matchingBytes=size, targetSha256=sha(native),
                     nativeAlias=f"func_arm7_boot_{address:08x}", reconstructionKind="justified-startup-assembly",
                     assemblyJustification=JUSTIFICATIONS[address], assemblerSha256=ASSEMBLER_HASH,
                     oracle={"supported": False, "reason": "Privileged boot mode, physical RAM aliasing and handoff behavior require a broader platform model; no physical startup execution is claimed"})
        matches.append(entry)
    flags = ["-O2", "-proc", "arm7tdmi", "-sym", "on", "-nolink", "-c"]
    source = ROOT / "src/arm7/boot/parameters.c"
    attempt, result = compile_source(source, COMPILER, flags, "native_arm7_boot_parameters_02380204", 0x02380204, environment)
    attempts.append(attempt)
    data_matches = []
    if result:
        entry, code = result
        native = binary[0x204:0x21C]
        if code != native:
            raise ValueError("Typed ARM7 boot parameters do not match")
        entry.update(kind="rodata", exactAfterDeclaredRelocation=True, targetSha256=sha(native), nativeAlias="data_arm7_boot_02380204",
                     nativeInteriorSymbols={}, nativeSymbols={})
        data_matches.append(entry)
    if len(matches) != 3 or len(data_matches) != 1:
        raise ValueError("ARM7 boot reproduction must preserve all three code units and typed parameter data")
    report = {"schemaVersion": 1, "romSha256": sha((ROOT / "inputs/game.nds").read_bytes()), "processor": "arm7", "runtimeMappingCanonical": True,
              "matches": matches, "attempts": attempts, "nativeSymbols": {rel["symbol"]: rel["target"] for entry in matches for rel in entry["relocations"]},
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "limitations": ["Assembly is limited to the measured native startup ABI and hardware handoff", "Every .word in startup assembly is an actual PC-relative literal-load target, never an instruction substitute", "Complete runtime-module linking is validated separately"]}
    (ROOT / "evidence/matches/arm7-boot.json").write_text(json.dumps(report, indent=2) + "\n")
    data_report = {"schemaVersion": 1, "romSha256": report["romSha256"], "processor": "arm7", "runtimeMappingCanonical": True,
                   "dataMatches": data_matches, "nativeSymbols": {}, "dataMatchedBytes": sum(entry["bytes"] for entry in data_matches),
                   "bssMatchedBytes": 0, "functionMatched": 0, "wholeModuleLinked": False,
                   "limitations": ["The sixth native parameter word remains semantically unknown", "The separate physical autoload composition table is not part of the boot runtime-module bytes"]}
    (ROOT / "evidence/data/arm7-boot.json").write_text(json.dumps(data_report, indent=2) + "\n")
    print({"functions": len(matches), "functionSpanBytes": sum(entry["bytes"] for entry in matches), "typedParameterBytes": sum(entry["bytes"] for entry in data_matches)})


if __name__ == "__main__":
    main()
