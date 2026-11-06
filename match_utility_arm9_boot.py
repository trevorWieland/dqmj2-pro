import json
import os
import re
import struct
import subprocess
from pathlib import Path
import utility_runtime
import utility_code
import match_utility_hardware
from match_utility_primitives import native_bindings
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_GRP_CALL, CS_GRP_JUMP
from capstone.arm import ARM_OP_MEM, ARM_REG_PC
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/lowlevel-recovery/utility-arm9-boot"
RANGES = {0x02000850: [(0x02000850, 0x02000968)],
          0x02000A4C: [(0x02000A4C, 0x02000AC0), (0x02000AC4, 0x02000AC8)],
          0x02000AC8: [(0x02000AC8, 0x02000B80)]}
SIZES = {0x02000850: 316, 0x02000A4C: 124, 0x02000AC8: 232}
POOLS = {0x02000850: set(range(0x02000968, 0x0200098C, 4)),
         0x02000A4C: {0x02000AC0}, 0x02000AC8: set(range(0x02000B80, 0x02000BB0, 4))}
JUSTIFICATIONS = {
    0x02000850: "ARM9 reset controls interrupt MMIO, CPSR processor modes and banked stacks, establishes TCM handoff addresses, maintains caches and transfers control to the loaded Thumb application without a C caller",
    0x02000A4C: "Startup autoload copy/zero and cache maintenance uses a stack-free boot ABI clobbering normal C callee-saved registers r4-r7, followed by a header-referenced interior BX-LR loader callback",
    0x02000AC8: "Dedicated ARM946E-S CP15 initialization configures MPU regions, instruction/data caches, TCM mappings and control state; ordinary C cannot express these privileged register operations"}


def external(target, mode):
    return f"native_utility_child_arm9_{mode}_{target:08x}"


def source_text(address, binary):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = {instruction.address: instruction for first, last in RANGES[address]
                    for instruction in decoder.disasm(binary[first - 0x02000000:last - 0x02000000], first)}
    measured = set()
    for instruction in instructions.values():
        for operand in instruction.operands:
            if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC:
                measured.add(instruction.address + 8 + operand.mem.disp)
    if measured != POOLS[address]:
        raise ValueError("Startup literal addresses do not match the frozen measured pools")
    name = f"native_utility_child_arm9_main_boot_{address:08x}"
    lines = [".section .text", ".arm", ".global " + name, ".type " + name + ", @function", name + ":"]
    externs = set()
    if address == 0x02000A4C:
        lines.append(".global native_utility_child_arm9_arm_02000ac4")
    for location in range(address, address + SIZES[address], 4):
        lines.append(f"local_{location:08x}:")
        if location in POOLS[address]:
            value = struct.unpack_from("<I", binary, location - 0x02000000)[0]
            pointer = address != 0x02000AC8 and value in (0x027E0000, 0x02000BB4, 0x01FF8000, 0x02000BD9)
            mode = "thumb" if value == 0x02000BD9 else "data"
            token = external(value, mode) if pointer else hex(value)
            if pointer:
                externs.add(token)
            lines.append("    .word " + token)
            continue
        if location not in instructions:
            raise ValueError("Unclassified startup word cannot be substituted as instruction data")
        if location == 0x02000AC4:
            lines.append("native_utility_child_arm9_arm_02000ac4:")
        instruction = instructions[location]
        mnemonic, operands = instruction.mnemonic, instruction.op_str.replace("apsr", "cpsr")
        if mnemonic in ("mcr", "mrc"):
            operands = operands.replace("#", "")
        if "[pc" in operands:
            target = location + 8 + instruction.operands[-1].mem.disp
            operands = operands.split(",", 1)[0] + f", local_{target:08x}"
        if (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)) and instruction.operands and instruction.operands[0].type == 2:
            target = instruction.operands[0].imm
            if target in instructions:
                operands = f"local_{target:08x}"
            else:
                operands = external(target, "thumb" if mnemonic == "blx" else "arm")
                externs.add(operands)
        lines.append("    " + mnemonic + " " + operands)
    lines.append(".size " + name + ", .-" + name)
    return name, "\n".join(".extern " + name for name in sorted(externs)) + "\n" + "\n".join(lines) + "\n"


def resolve(obj, name, address):
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        symbol = next(symbol for symbol in elf.get_section_by_name(".symtab").iter_symbols() if symbol.name == name)
        output = bytearray(elf.get_section(symbol["st_shndx"]).data())
        relocations = []
        for section in elf.iter_sections():
            if section["sh_type"] not in ("SHT_REL", "SHT_RELA") or section["sh_info"] != symbol["st_shndx"]:
                continue
            if section["sh_type"] != "SHT_RELA":
                raise ValueError("Unexpected implicit assembler addend")
            table = elf.get_section(section["sh_link"])
            for relocation in section.iter_relocations():
                at, kind, addend = relocation["r_offset"], relocation["r_info_type"], relocation["r_addend"]
                label = table.get_symbol(relocation["r_info_sym"]).name
                target = int(re.search(r"([0-9a-f]{8})$", label).group(1), 16)
                mode = "thumb" if "_thumb_" in label else "data" if "_data_" in label else "arm"
                value = struct.unpack_from("<I", output, at)[0]
                if kind == 2:
                    value = target + addend
                elif kind in (1, 28, 29) and mode == "arm":
                    displacement = target + addend - address - at
                    if displacement % 4:
                        raise ValueError("Unaligned ARM startup branch")
                    value = value & 0xFF000000 | (displacement >> 2) & 0xFFFFFF
                elif kind == 15 and mode == "thumb" and value >> 28 == 15:
                    displacement = (target & ~1) + addend - address - at
                    if displacement % 2 or not -0x2000000 <= displacement < 0x2000000:
                        raise ValueError("Invalid ARM BLX immediate range")
                    value = 0xFA000000 | ((displacement & 2) << 23) | ((displacement >> 2) & 0xFFFFFF)
                else:
                    raise ValueError("Unexpected startup relocation kind or target mode")
                struct.pack_into("<I", output, at, value & 0xFFFFFFFF)
                relocations.append({"offset": at, "type": kind, "symbol": label, "target": hex(target), "targetMode": mode, "addend": addend})
        return bytes(output), relocations, symbol["st_shndx"], symbol["st_value"], symbol["st_size"]


def main():
    assembler = match_utility_hardware.ASSEMBLER
    if utility_runtime.sha(assembler.read_bytes()) != match_utility_hardware.ASSEMBLER_HASH:
        raise ValueError("ARM9 startup assembler pin changed")
    layout, files = utility_runtime.derive()
    module = next(module for module in layout["modules"] if module["id"] == "utility-child-arm9-main")
    binary = bytes(files[ROOT / module["binary"]])
    WORK.mkdir(parents=True, exist_ok=True)
    path = ROOT / "evidence/matches/utility-arm9-startup01.json"
    previous = json.loads(path.read_text()) if path.exists() else None
    matches, attempts = [], []
    for address, size in SIZES.items():
        name, text = source_text(address, binary)
        source = ROOT / "src/utility/startup-arm9" / (name + ".s")
        source.parent.mkdir(parents=True, exist_ok=True)
        if previous:
            expected = next(entry for entry in previous["matches"] if entry["name"] == name)
            if source.read_text() != text or utility_runtime.sha(source.read_bytes()) != expected["sourceSha256"]:
                raise ValueError("Frozen ARM9 startup source changed")
            utility_code.accepted_spec(expected)
        elif source.exists():
            if source.read_text() != text:
                raise ValueError("Refusing to replace ARM9 startup source")
        else:
            source.write_text(text)
        obj = WORK / (name + ".o")
        flags = ["-proc", "arm5TE", "-c"]
        command = [str(assembler), *flags, str(source), "-o", str(obj)]
        process = subprocess.run(command, cwd=ROOT, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / "tools/mwccarm/mwccarm/license.dat")), capture_output=True, text=True, timeout=30)
        attempts.append({"command": command, "exitCode": process.returncode, "stdout": process.stdout, "stderr": process.stderr})
        if process.returncode:
            raise ValueError(attempts[-1])
        output, relocations, index, offset, symbol_size = resolve(obj, name, address)
        native = binary[address - 0x02000000:address - 0x02000000 + size]
        if output != native or symbol_size != size:
            raise ValueError({"address": hex(address), "bytes": len(output), "matches": sum(a == b for a, b in zip(native, output))})
        digest = utility_runtime.sha(obj.read_bytes())
        stable = WORK / "objects" / (digest + ".o")
        stable.parent.mkdir(exist_ok=True)
        if not stable.exists():
            stable.write_bytes(obj.read_bytes())
        entry = {"name": name, "program": utility_runtime.PROGRAM, "processor": "arm9", "module": module["id"], "address": hex(address), "mode": "arm",
                 "bytes": size, "size": size, "compiledBytes": size, "matchingBytes": size, "exactAfterDeclaredRelocation": True,
                 "source": source.relative_to(ROOT).as_posix(), "sourceSha256": utility_runtime.sha(source.read_bytes()),
                 "object": stable.relative_to(ROOT).as_posix(), "objectSha256": digest, "sectionIndex": index, "sectionOffset": offset,
                 "compiler": assembler.relative_to(ROOT).as_posix(), "compilerSha256": match_utility_hardware.ASSEMBLER_HASH,
                 "assemblerSha256": match_utility_hardware.ASSEMBLER_HASH, "compilerFlags": flags, "relocations": relocations,
                 "nativeAlias": f"func_utility_child_arm9_main_{address:08x}", "inputModuleSha256": module["sha256"],
                 "targetSha256": utility_runtime.sha(native), "outputSha256": utility_runtime.sha(output), "linked": False,
                 "assemblyJustification": JUSTIFICATIONS[address], "boundaryEvidence": {"codeRanges": [[hex(a), hex(b)] for a, b in RANGES[address]], "literalPoolWords": [hex(a) for a in sorted(POOLS[address])], "entryEvidence": "Embedded ARM9 reset descriptor and statically measured boot call targets; complete mnemonic and own-pool native spans"},
                 "oracle": {"supported": False, "reason": "Physical startup mode/TCM/MPU/cache state and loader handoff require a broader platform model; exact bytes and declared relocations are verified, without claiming physical boot execution"}}
        if address == 0x02000A4C:
            entry["interiorSymbols"] = [{"name": "native_utility_child_arm9_arm_02000ac4", "offset": 120, "address": "0x02000ac4", "mode": "arm", "kind": "header-referenced-loader-callback", "separateFunctionCredit": False}]
        matches.append(entry)
    report = {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM, "runtimeMappingCanonical": True,
              "matches": matches, "nativeSymbols": {rel["symbol"]: rel["target"] for entry in matches for rel in entry["relocations"]},
              "nativeSymbolBindings": native_bindings(matches), "attempts": attempts, "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "reproduce": ["python", "match_utility_arm9_boot.py"], "limitations": ["Assembly is restricted to privileged reset/CP15 and special startup loader ABI units", "Ordinary decompression and memory algorithms called by reset remain separate unresolved C work", "Only measured PC-relative literal data uses word directives; every instruction is an assembler mnemonic"]}
    path.write_text(json.dumps(report, indent=2) + "\n")
    print({"startupUnits": len(matches), "bytes": sum(entry["bytes"] for entry in matches), "relocations": sum(len(entry["relocations"]) for entry in matches)})


if __name__ == "__main__":
    main()
