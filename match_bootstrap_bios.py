import os
import re
import shutil
import subprocess
from project import ROOT, configuration, native_dependencies, now, sha256, verify_inputs, write_json
from match_hardware import ASSEMBLER, ASSEMBLER_HASH


def main():
    config = configuration()
    inputs = verify_inputs(config)
    native_dependencies(config)
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
    from elftools.elf.elffile import ELFFile
    if sha256(ASSEMBLER) != ASSEMBLER_HASH:
        raise ValueError("Assembler identity changed")
    binary = (ROOT / "extract/arm9/arm9.bin").read_bytes()
    symbols = (ROOT / "config/arm9/symbols.txt").read_text()
    work = ROOT / "work/hardware-recovery/bootstrap-bios"
    work.mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, LM_LICENSE_FILE=str(config["license"]))
    matches = []
    for original, size, address in re.findall(r"^(\S+) kind:function\(thumb,size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)", symbols, re.M):
        address, size = int(address, 0), int(size, 0)
        if not 0x02000000 <= address < 0x02000800:
            continue
        target = binary[address - 0x02000000:address - 0x02000000 + size]
        instructions = list(Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(target, address))
        if sum(item.size for item in instructions) != size or not any(item.mnemonic == "svc" for item in instructions):
            raise ValueError("Secure-prefix candidate is not a complete BIOS wrapper")
        if any(item.mnemonic not in ("svc", "bx", "movs", "adds") for item in instructions):
            raise ValueError("BIOS wrapper has unexplained ordinary instructions")
        if instructions[-1].mnemonic != "bx" or instructions[-1].op_str != "lr":
            raise ValueError("BIOS wrapper return differs")
        name = f"native_main_bios_{address:08x}"
        lines = [".section .text", ".thumb", ".global " + name, ".type " + name + ", @function", name + ":"]
        replacements = {"svc": "swi", "movs": "mov", "adds": "add", "bx": "bx"}
        lines += ["    " + replacements[item.mnemonic] + " " + (item.op_str.replace("#", "") if item.mnemonic == "svc" else item.op_str) for item in instructions]
        lines += [".size " + name + ", .-" + name]
        source = ROOT / "src/hardware/bootstrap_bios" / (name + ".s")
        source.parent.mkdir(parents=True, exist_ok=True)
        text = "\n".join(lines) + "\n"
        if source.exists() and source.read_text() != text:
            raise ValueError("Frozen BIOS source differs")
        if not source.exists():
            source.write_text(text)
        obj = work / (name + ".o")
        flags = ["-proc", "arm5TE", "-c"]
        command = [str(ASSEMBLER), *flags, str(source), "-o", str(obj)]
        result = subprocess.run(command, cwd=work, env=environment, capture_output=True, text=True, errors="replace", timeout=30)
        if result.returncode:
            raise ValueError("BIOS source assembly failed: " + result.stdout + result.stderr)
        with obj.open("rb") as stream:
            elf = ELFFile(stream)
            symbol = next(item for item in elf.get_section_by_name(".symtab").iter_symbols() if item.name == name)
            section = elf.get_section(symbol["st_shndx"])
            padding = section["sh_size"] - size
            if section.data()[:size] != target or symbol["st_size"] != size or symbol["st_value"] & ~1:
                raise ValueError("BIOS wrapper bytes/boundaries differ")
            if padding and (not 0 < padding < section["sh_addralign"] or any(section.data()[size:])):
                raise ValueError("BIOS assembler emitted unexplained bytes after function extent")
            if any(item["sh_type"] in ("SHT_REL", "SHT_RELA") and item["sh_size"] for item in elf.iter_sections()):
                raise ValueError("Unexpected BIOS wrapper relocations")
        stable = work / (sha256(obj) + ".o")
        if not stable.exists():
            shutil.copy2(obj, stable)
        matches.append({"name": name, "module": "main", "processor": "arm9", "mode": "thumb", "address": hex(address), "bytes": size, "size": size, "exactBytes": True, "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha256(source), "object": stable.relative_to(ROOT).as_posix(), "objectSha256": sha256(stable), "compilerSha256": ASSEMBLER_HASH, "compilerFlags": flags, "nativeAlias": original, "assemblyJustification": "Measured BIOS software-interrupt interface requires architectural SVC behavior outside ordinary C", "oracle": {"supported": False, "reason": "Physical BIOS behavior is outside the isolated source model"}, "command": command})
        matches[-1]["sectionPaddingBytes"] = padding
    if len(matches) != 18 or inputs != verify_inputs(config):
        raise ValueError("BIOS wrapper inventory or inputs changed")
    report = {"schemaVersion": 1, "createdUtc": now(), "romSha256": inputs["rom"]["sha256"], "module": "main", "matches": matches, "sourceReconstructionComplete": False, "limitations": ["All mnemonic instruction bytes and native wrapper extents are exact", "BIOS implementation, physical effects and malformed argument support remain unverified", "The rest of the secure prefix remains separately classified in the region inventory"]}
    write_json(ROOT / "evidence/matches/hardware-bootstrap-bios.json", report)
    print({"biosWrappers": len(matches), "bytes": sum(item["bytes"] for item in matches)})


if __name__ == "__main__":
    main()
