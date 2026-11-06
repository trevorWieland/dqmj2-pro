import json
import random
import sys
from pathlib import Path

import match_overlay_modules as compiler
import save_link_snapshots
from link_runtime_unit import validate
from match_ov000_20261029_leaf import original_module
from project import now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn import __version__ as unicorn_version
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP,
    UC_CPU_ARM_946,
)

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/ov000-recovery/20261029/clearbytes27"
SOURCE = ROOT / "src/overlays/ov000_20261029_clear_bytes_f193ed4b29bb.c"
REPORT = ROOT / "evidence/matches/ov000-20261029-clearbytes01.json"
STACK = 0x03010000
STOP = 0x04000000
DATA = 0x022322D0


def execute(entry, code, vector):
    randomizer = random.Random(20261029270 + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    engine.ctl_set_cpu_model(UC_CPU_ARM_946)
    engine.mem_map(0x02000000, 0x400000)
    engine.mem_map(STACK, 0x10000)
    engine.mem_map(STOP, 0x1000)
    address = int(entry["address"], 0)
    engine.mem_write(address, code)
    initial = bytes([vector, 255 - vector, vector * 17 & 255, vector ^ 0x5A])
    engine.mem_write(DATA, initial)
    engine.mem_write(STACK, randomizer.randbytes(0x10000))
    registers = [randomizer.getrandbits(32) for unused in range(13)]
    engine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
    for index, value in enumerate(registers):
        engine.reg_write(UC_ARM_REG_R0 + index, value)
    engine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    engine.reg_write(UC_ARM_REG_LR, STOP)
    initial_stack = compiler.sha(bytes(engine.mem_read(STACK, 0x10000)))
    reads, writes, executed = [], [], []
    literal_start = min([rel["offset"] for rel in entry["relocations"] if rel["type"] == 2])

    def step(machine, pc, size, user):
        if not address <= pc < address + literal_start:
            raise ValueError("Byte reset escaped its own executable instructions")
        executed.append(pc)

    def read(machine, access, location, size, value, user):
        if location != address + literal_start or size != 4:
            raise ValueError("Byte reset read beyond its own literal")
        reads.append((location, size))

    def written(machine, access, location, size, value, user):
        if location != DATA + len(writes) or size != 1 or value & 255 != 255:
            raise ValueError("Byte reset write differs from four ordered FF bytes")
        writes.append((location, size, value & 255))

    engine.hook_add(UC_HOOK_CODE, step)
    engine.hook_add(UC_HOOK_MEM_READ, read)
    engine.hook_add(UC_HOOK_MEM_WRITE, written)
    engine.emu_start(address, STOP, count=10000)
    if engine.reg_read(UC_ARM_REG_PC) != STOP or engine.reg_read(UC_ARM_REG_R0) != 0xFFFFFFFF:
        raise ValueError("Byte reset failed actual return or its measured word result")
    if len(writes) != 4 or bytes(engine.mem_read(DATA, 4)) != bytes([255]) * 4:
        raise ValueError("Independent complete byte model differs")
    if engine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError("Byte reset changed SP")
    if any(engine.reg_read(UC_ARM_REG_R0 + index) != registers[index] for index in range(3, 13)):
        raise ValueError("Byte reset changed a register beyond its native R0-R2 effects")
    final_stack = compiler.sha(bytes(engine.mem_read(STACK, 0x10000)))
    if final_stack != initial_stack:
        raise ValueError("Byte reset changed its private stack")
    final_registers = [engine.reg_read(UC_ARM_REG_R0 + index) for index in range(13)]
    final_registers += [engine.reg_read(register) for register in [
        UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
    ]]
    return {"return": 0xFFFFFFFF, "registers": final_registers, "reads": reads,
            "writes": writes, "executed": executed,
            "ramSha256": compiler.sha(bytes(engine.mem_read(0x02000000, 0x400000))),
            "stackSha256": final_stack}


def oracle(entry, linked, binary, base):
    address = int(entry["address"], 0)
    native = binary[address - base : address - base + entry["bytes"]]
    vectors = []
    for index in range(256):
        original = execute(entry, native, index)
        rebuilt = execute(entry, linked, index)
        if original != rebuilt:
            raise ValueError("Full native/linked byte-reset effects differ")
        vectors.append({"index": index, "instructions": len(original["executed"]),
                        "stateSha256": compiler.sha(json.dumps(original, sort_keys=True).encode())})
    return {"passed": True, "vectors": len(vectors), "executions": len(vectors) * 2,
            "nativeInstructions": sum(vector["instructions"] for vector in vectors),
            "results": vectors, "actualReturnRequired": True, "instructionLimit": 10000,
            "freshMachinePerExecution": True, "cpuModel": "ARM946",
            "independentModel": "Four ordered FF-byte writes; all256 initial values covered at each byte position; R0 returns FFFFFFFF",
            "comparedEffects": "Full R0-R15/CPSR,4MiB RAM,unchanged64KiB stack, ordered reads/value-bearing writes and executed PCs",
            "externalCallees": [], "externalCalleesExecutedNatively": False,
            "limitations": ["The four-byte field's game meaning is unknown", "The measured R0 bit pattern does not establish the original source-level signedness", "No hardware or other native routines execute"]}


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python and Unicorn versions are required")
    binary, metadata, provenance = original_module()
    compiler.WORK = WORK / "compiler"
    save_link_snapshots.DIRECTORY = WORK / "link-artifacts"
    report, codes = compiler.compile_compare("ov000", SOURCE, "2", "off")
    if report["returncode"] or len(report["functions"]) != 1:
        raise ValueError("Frozen byte-reset source no longer yields one function")
    compile_path = WORK / ("compile-" + compiler.sha(json.dumps(report, sort_keys=True).encode()) + ".json")
    compiler.immutable(compile_path, json.dumps(report, indent=2).encode())
    entry = {**report["functions"][0], "processor": "arm9", "sourceLanguage": "C"}
    if not entry["exactAfterDeclaredRelocation"]:
        raise ValueError("Frozen byte-reset C no longer fully matches")
    bindings = qualified_bindings(entry)
    directory = WORK / "links" / entry["name"] / entry["objectSha256"]
    proof = validate(entry, bindings, directory)
    linked = (directory / "caller.bin").read_bytes()
    entry.update(save_link_snapshots.freeze_link(proof))
    entry.update(nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 oracle=oracle(entry, linked, binary, int(metadata["base"], 0)),
                 ordinaryCBytes=entry["bytes"], justifiedAssemblyBytes=0,
                 compileReport=str(compile_path.relative_to(ROOT)))
    result = {"schemaVersion": 1, "createdUtc": now(), "module": "ov000", "processor": "arm9",
              **provenance, "matches": [entry], "source": str(SOURCE.relative_to(ROOT)),
              "sourceSha256": sha256(SOURCE), "generator": Path(__file__).name,
              "generatorSha256": sha256(Path(__file__)), "generatorDependencies": {
                  "match_ov000_20261029_leaf.py": sha256(ROOT / "match_ov000_20261029_leaf.py")},
              "pythonVersion": sys.version, "unicornVersion": unicorn_version,
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "nativeSymbols": {rel["symbol"]: rel["target"] for rel in entry["relocations"]}}
    snapshot = WORK / ("match-" + compiler.sha(json.dumps(result, sort_keys=True).encode()) + ".json")
    compiler.immutable(snapshot, json.dumps(result, indent=2).encode())
    write_json(REPORT, result)
    print(json.dumps({"functions": 1, "bytes": entry["bytes"], "executions": entry["oracle"]["executions"],
                      "report": str(REPORT.relative_to(ROOT))}))


if __name__ == "__main__":
    run()
