import hashlib
import os
import struct
import subprocess
import zipfile
from project import ROOT, configuration, native_dependencies, now, sha256, write_json
from match_runtime import COMPILER_PINS


def execute(code, first, second):
    from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
    from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    engine.mem_map(0x02000000, 0x1000)
    engine.mem_map(0x03000000, 0x1000)
    engine.mem_write(0x02000000, code)
    engine.reg_write(UC_ARM_REG_R0, first & 0xFFFFFFFF)
    engine.reg_write(UC_ARM_REG_R1, second & 0xFFFFFFFF)
    engine.reg_write(UC_ARM_REG_SP, 0x03000FF0)
    engine.reg_write(UC_ARM_REG_LR, 0x02000800)
    engine.emu_start(0x02000000, 0x02000800, count=100)
    if engine.reg_read(UC_ARM_REG_PC) != 0x02000800 or engine.reg_read(UC_ARM_REG_SP) != 0x03000FF0:
        raise ValueError("Compiler smoke did not return normally")
    if engine.reg_read(UC_ARM_REG_R0) != (first * second) & 0xFFFFFFFF:
        raise ValueError("Compiler smoke arithmetic differs")


def main():
    config = configuration()
    native_dependencies(config)
    from elftools.elf.elffile import ELFFile
    archive = ROOT / "tools/mwccarm.zip"
    archive_hash = sha256(archive)
    if archive_hash != "dc386e37b2176e960954a733de928337d9b7e7620b9e94228008c31774339ace":
        raise ValueError("Private compiler archive identity differs")
    work = ROOT / "work/toolchain-validation/compiler-members"
    work.mkdir(parents=True, exist_ok=True)
    source = work / "multiply.c"
    source.write_text("int multiply(short x, short y) { return x * y; }\n")
    environment = dict(os.environ, LM_LICENSE_FILE=str(config["license"]))
    rows = []
    with zipfile.ZipFile(archive) as package:
        for path, expected in COMPILER_PINS.items():
            member = path.removeprefix("tools/mwccarm/")
            member_hash = hashlib.sha256(package.read(member)).hexdigest()
            if member_hash != expected or sha256(ROOT / path) != member_hash:
                raise ValueError("Installed compiler differs from verified archive member")
            obj = work / (expected + ".o")
            command = [str(ROOT / path), "-O2", "-proc", "arm946e", "-nolink", "-c", str(source), "-o", str(obj)]
            result = subprocess.run(command, cwd=work, env=environment, capture_output=True, text=True, errors="replace", timeout=30)
            if result.returncode:
                raise ValueError("Pinned archive compiler smoke failed: " + result.stdout + result.stderr)
            with obj.open("rb") as stream:
                elf = ELFFile(stream)
                symbol = next(item for item in elf.get_section_by_name(".symtab").iter_symbols() if item.name == "multiply")
                body = elf.get_section(symbol["st_shndx"]).data()[symbol["st_value"]:symbol["st_value"] + symbol["st_size"]]
            values = [-32768, -32767, -257, -1, 0, 1, 255, 256, 32766, 32767]
            for first in values:
                for second in values:
                    execute(body, first, second)
            rows.append({"compiler": path, "archiveMember": member, "sha256": member_hash, "command": command, "exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr, "objectSha256": sha256(obj), "codeSha256": hashlib.sha256(body).hexdigest(), "codeBytes": len(body), "isolatedExecutions": len(values) ** 2, "verifiedReturn": True, "expectedSigned16Product": True})
    report = {"schemaVersion": 1, "createdUtc": now(), "archiveSha256": archive_hash, "passed": True, "members": rows, "limitations": ["Smoke uses sign-extended signed16 ABI arguments", "Compiler-family identity and historical source settings remain per-unit questions", "Linker correctness is validated separately by native module comparisons"]}
    write_json(ROOT / "evidence/tools/compiler-archive-members.json", report)
    print({"archiveMembersVerified": len(rows), "isolatedCompilerSmokeExecutions": sum(row["isolatedExecutions"] for row in rows)})


if __name__ == "__main__":
    main()
