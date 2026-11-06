import argparse
import hashlib
import os
import random
import struct
import subprocess
from pathlib import Path
from project import ROOT, configuration, native_dependencies, now, read_json, sha256, verify_inputs, write_json


def execute(code, address, data):
    from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_PROT_EXEC, UC_PROT_READ
    from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_SP
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    base = address & ~4095
    span = ((address - base + len(code) + 4095) // 4096) * 4096
    uc.mem_map(base, span, UC_PROT_ALL)
    uc.mem_write(address, code)
    uc.mem_protect(base, span, UC_PROT_READ | UC_PROT_EXEC)
    for memory in (0x03000000, 0x03E00000):
        uc.mem_map(memory, 0x10000)
    uc.mem_map(0x05000000, 4096)
    uc.mem_write(0x03000000, data)
    uc.reg_write(UC_ARM_REG_R0, 0x03000000)
    uc.reg_write(UC_ARM_REG_LR, 0x05000000)
    uc.reg_write(UC_ARM_REG_SP, 0x03E0FFF0)
    for index in range(8):
        uc.reg_write(UC_ARM_REG_R4 + index, 0xA0400000 + index)
    uc.emu_start(address, 0x05000000, timeout=2000000, count=100000)
    if uc.reg_read(UC_ARM_REG_PC) != 0x05000000:
        raise RuntimeError("Execution did not reach return sentinel")
    if uc.reg_read(UC_ARM_REG_SP) != 0x03E0FFF0:
        raise RuntimeError("Stack was not restored")
    if any(uc.reg_read(UC_ARM_REG_R4 + i) != 0xA0400000 + i for i in range(8)):
        raise RuntimeError("Callee-saved register changed")
    if bytes(uc.mem_read(0x03000000, len(data))) != data:
        raise RuntimeError("Checksum helper mutated its input")
    return uc.reg_read(UC_ARM_REG_R0)


def reproduce(config):
    native_dependencies(config)
    from elftools.elf.elffile import ELFFile
    import unicorn
    if unicorn.__version__ != "2.1.4":
        raise RuntimeError("Expected Unicorn 2.1.4")
    inputs = verify_inputs(config)
    if sha256(config["compiler"]) != "7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880":
        raise ValueError("Compiler identity mismatch")
    seed = read_json(ROOT / "provenance/seed-oracle-results.json")
    flags = seed["compiler"]["flags"]
    output = config["output"]
    output.mkdir(parents=True, exist_ok=True)
    obj = output / "matched.o"
    source = ROOT / "src/save_checksum.c"
    env = dict(os.environ, LM_LICENSE_FILE=str(config["license"]))
    command = [str(config["compiler"]), *flags, "-c", str(source), "-o", str(obj)]
    run = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=30)
    if run.returncode:
        raise RuntimeError(run.stdout + run.stderr)
    arm9_path = ROOT / "extract/arm9/arm9.bin"
    arm9 = arm9_path.read_bytes()
    main = next(item for item in read_json(ROOT / "provenance/seed-manifest.json")["modules"] if item["name"] == "main")
    if sha256(arm9_path) != main["sha256"]:
        raise ValueError("Decoded ARM9 identity mismatch")
    specs = {"save_payload_checksum": (0x0207DA70, 48, 0x90, 0x70D0, 0x88), "save_header_checksum": (0x0207DAA0, 40, 0, 0x8C, 0x8C)}
    compiled = {}
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        for symbol in elf.get_section_by_name(".symtab").iter_symbols():
            if symbol.name in specs:
                section = elf.get_section(symbol["st_shndx"])
                code = section.data()[symbol["st_value"]:symbol["st_value"] + symbol["st_size"]]
                address, size, _, _, _ = specs[symbol.name]
                target = arm9[address - 0x02000000:address - 0x02000000 + size]
                if len(code) != size or code != target:
                    raise ValueError("Exact bytes differ: " + symbol.name)
                compiled[symbol.name] = code
    if set(compiled) != set(specs):
        raise ValueError("Required function missing from compiled object")
    save = config["save"].read_bytes()
    rng = random.Random(20261026)
    vectors = [("real-block-0", save[:0x7100]), ("real-block-1", save[0x7100:0xE200]), ("zero", bytes(0x7100)), ("all-ff", bytes([255]) * 0x7100)]
    vectors.extend((f"random-{i}", rng.randbytes(0x7100)) for i in range(32))
    results = []
    for name, data in vectors:
        checks = []
        for symbol, (address, size, start, end, stored) in specs.items():
            expected = sum(struct.unpack_from("<I", data, i)[0] for i in range(start, end, 4)) & 0xFFFFFFFF
            native = execute(arm9[address - 0x02000000:address - 0x02000000 + size], address, data)
            rebuilt = execute(compiled[symbol], 0x06000000, data)
            if native != expected or rebuilt != expected:
                raise ValueError(f"Oracle mismatch {name} {symbol}")
            check = {"function": symbol, "expected": expected, "native": native, "compiled": rebuilt}
            if name.startswith("real-"):
                check["stored"] = struct.unpack_from("<I", data, stored)[0]
                if check["stored"] != native:
                    raise ValueError("Captured checksum differs")
            checks.append(check)
        results.append({"vector": name, "checks": checks})
    if inputs != verify_inputs(config):
        raise ValueError("Inputs changed during reproduction")
    matches = [{"name": name, "module": "main", "processor": "arm9", "mode": "arm", "address": hex(specs[name][0]), "size": len(code), "exactBytes": True, "sha256": hashlib.sha256(code).hexdigest(), "source": "src/save_checksum.c", "object": str(obj.relative_to(ROOT)), "sourceSha256": sha256(source), "objectSha256": sha256(obj), "compilerFlags": flags, "moduleLinked": False} for name, code in compiled.items()]
    report = {"schemaVersion": 2, "createdUtc": now(), "romSha256": inputs["rom"]["sha256"], "romBytes": inputs["rom"]["bytes"], "saveSha256": inputs["save"]["sha256"], "compiler": {"pack": "mwccarm/2.0/base", "sha256": sha256(config["compiler"]), "flags": flags}, "sourceSha256": sha256(source), "command": command, "functionMatches": matches, "oracle": {"engine": "Unicorn", "version": unicorn.__version__, "vectors": len(vectors), "executions": len(vectors) * len(specs) * 2, "isolatedState": True, "verifiedReturn": True, "verifiedPreservedState": True, "results": results}, "wholeLinkedRebuild": False, "wholeRomMatched": False, "inputsUnchanged": True}
    write_json(output / "results.json", report)
    write_json(ROOT / "evidence/matches/checksum.json", report)
    print(f"PASS: {len(matches)} exact functions, {report['oracle']['executions']} isolated native/compiled executions")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path)
    reproduce(configuration(parser.parse_args().config))
