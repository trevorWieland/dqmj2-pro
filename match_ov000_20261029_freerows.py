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
WORK = ROOT / "work/ov000-recovery/20261029/freerows29"
SOURCE = ROOT / "src/overlays/ov000_20261029_free_rows_c6d833a66a67.c"
REPORT = ROOT / "evidence/matches/ov000-20261029-freerows01.json"
STACK = 0x03010000
STOP = 0x04000000
GROUPS = {
    0x021E54F4: (0x02232868, 20, 32, 2),
    0x021E57F8: (0x022332E8, 64, 32, 1),
    0x021E5C10: (0x02232AE8, 32, 64, 1),
    0x021E5FC8: (0x02232668, 16, 32, 1),
}


def fixture(index, count, width):
    maximum = (1 << (8 * width)) - 1
    keys = [0x100 if width == 2 else maximum] * count
    if index < count * 2:
        kind, position = divmod(index, count)
        keys[position] = 0
        if kind:
            keys[-1] = 0
    else:
        edge = index - count * 2
        keys = [[0] * count, [maximum] * count, [maximum >> 1 | 1] * count,
                [0 if row % 2 else maximum for row in range(count)],
                [maximum] + [0] * (count - 1), [maximum] * (count - 1) + [0],
                [0x100 if width == 2 else 128] * count,
                [1] * count][edge]
    return keys


def execute(entry, code, keys, group, vector):
    base, stride, count, width = group
    randomizer = random.Random(20261029290 + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    engine.ctl_set_cpu_model(UC_CPU_ARM_946)
    engine.mem_map(0x02000000, 0x400000)
    engine.mem_map(STACK, 0x10000)
    engine.mem_map(STOP, 0x1000)
    address = int(entry["address"], 0)
    engine.mem_write(address, code)
    records = bytearray(randomizer.randbytes(stride * count))
    for index, key in enumerate(keys):
        records[index * stride : index * stride + width] = key.to_bytes(width, "little")
    engine.mem_write(base, bytes(records))
    engine.mem_write(STACK, randomizer.randbytes(0x10000))
    registers = [randomizer.getrandbits(32) for unused in range(13)]
    engine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
    for index, value in enumerate(registers):
        engine.reg_write(UC_ARM_REG_R0 + index, value)
    engine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    engine.reg_write(UC_ARM_REG_LR, STOP)
    initial_ram = compiler.sha(bytes(engine.mem_read(0x02000000, 0x400000)))
    initial_stack = compiler.sha(bytes(engine.mem_read(STACK, 0x10000)))
    reads, executed = [], []
    literal_start = min([rel["offset"] for rel in entry["relocations"] if rel["type"] == 2])

    def step(machine, pc, size, user):
        if not address <= pc < address + literal_start:
            raise ValueError("First-zero search escaped its own instructions")
        executed.append(pc)

    def read(machine, access, location, size, value, user):
        pool = address + literal_start <= location and location + size <= address + len(code)
        key = base <= location < base + len(records) and (location - base) % stride == 0 and size == width
        if not pool and not key:
            raise ValueError("First-zero search read beyond known-width keys or literal pool")
        reads.append((location, size))

    def written(machine, access, location, size, value, user):
        raise ValueError("Read-only first-zero search unexpectedly wrote memory")

    engine.hook_add(UC_HOOK_CODE, step)
    engine.hook_add(UC_HOOK_MEM_READ, read)
    engine.hook_add(UC_HOOK_MEM_WRITE, written)
    engine.emu_start(address, STOP, count=10000)
    position = next((index for index, key in enumerate(keys) if key == 0), None)
    expected = 0 if position is None else base + position * stride
    if engine.reg_read(UC_ARM_REG_PC) != STOP or engine.reg_read(UC_ARM_REG_R0) != expected:
        raise ValueError("Independent first-zero pointer or actual termination differs")
    observed_keys = [location for location, size in reads if base <= location < base + len(records)]
    expected_keys = [base + index * stride for index in range(count if position is None else position + 1)]
    if observed_keys != expected_keys:
        raise ValueError("First-zero search did not stop at its first matching record")
    if engine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError("First-zero search changed SP")
    if any(engine.reg_read(UC_ARM_REG_R0 + index) != registers[index] for index in range(4, 13)):
        raise ValueError("First-zero search changed a register outside native R0-R3 effects")
    final_ram = compiler.sha(bytes(engine.mem_read(0x02000000, 0x400000)))
    final_stack = compiler.sha(bytes(engine.mem_read(STACK, 0x10000)))
    if final_ram != initial_ram or final_stack != initial_stack:
        raise ValueError("First-zero search modified fixture memory")
    final_registers = [engine.reg_read(UC_ARM_REG_R0 + index) for index in range(13)]
    final_registers += [engine.reg_read(register) for register in [
        UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
    ]]
    return {"return": expected, "registers": final_registers, "reads": reads,
            "executed": executed, "ramSha256": final_ram, "stackSha256": final_stack}


def oracle(entry, linked, binary, base):
    address = int(entry["address"], 0)
    group = GROUPS[address]
    native = binary[address - base : address - base + entry["bytes"]]
    vectors = []
    for index in range(group[2] * 2 + 8):
        keys = fixture(index, group[2], group[3])
        original = execute(entry, native, keys, group, index)
        rebuilt = execute(entry, linked, keys, group, index)
        if original != rebuilt:
            raise ValueError("Full original/linked first-zero effects differ")
        vectors.append({"index": index, "keys": keys, "return": original["return"],
                        "instructions": len(original["executed"]),
                        "stateSha256": compiler.sha(json.dumps(original, sort_keys=True).encode())})
    return {"passed": True, "vectors": len(vectors), "executions": len(vectors) * 2,
            "nativeInstructions": sum(vector["instructions"] for vector in vectors),
            "results": vectors, "actualReturnRequired": True, "instructionLimit": 10000,
            "freshMachinePerExecution": True, "cpuModel": "ARM946",
            "tableBase": hex(group[0]), "recordStride": group[1], "recordCount": group[2],
            "keyBytes": group[3], "independentModel": "First record whose native-width key equals zero; null if all keys are nonzero; exact stopping read sequence",
            "comparedEffects": "Full R0-R15/CPSR,unchanged4MiB RAM/64KiB stack, ordered reads and executed PCs",
            "externalCallees": [], "externalCalleesExecutedNatively": False,
            "limitations": ["Game-level meaning of keys and payloads remains unknown", "The16-bit table includes nonzero keys with a zero low byte to reject byte-only hypotheses", "No hardware or additional native routines execute"]}


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python and Unicorn versions are required")
    binary, metadata, provenance = original_module()
    compiler.WORK = WORK / "compiler"
    save_link_snapshots.DIRECTORY = WORK / "link-artifacts"
    report, codes = compiler.compile_compare("ov000", SOURCE, "2", "off")
    if report["returncode"] or len(report["functions"]) != 4:
        raise ValueError("Frozen first-zero source no longer yields four functions")
    compile_path = WORK / ("compile-" + compiler.sha(json.dumps(report, sort_keys=True).encode()) + ".json")
    compiler.immutable(compile_path, json.dumps(report, indent=2).encode())
    matches = []
    for function in report["functions"]:
        if not function["exactAfterDeclaredRelocation"]:
            raise ValueError("Frozen first-zero C no longer fully matches")
        entry = {**function, "processor": "arm9", "sourceLanguage": "C"}
        bindings = qualified_bindings(entry)
        directory = WORK / "links" / entry["name"] / entry["objectSha256"]
        proof = validate(entry, bindings, directory)
        linked = (directory / "caller.bin").read_bytes()
        entry.update(save_link_snapshots.freeze_link(proof))
        entry.update(nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                     oracle=oracle(entry, linked, binary, int(metadata["base"], 0)),
                     ordinaryCBytes=entry["bytes"], justifiedAssemblyBytes=0,
                     compileReport=str(compile_path.relative_to(ROOT)))
        matches.append(entry)
    result = {"schemaVersion": 1, "createdUtc": now(), "module": "ov000", "processor": "arm9",
              **provenance, "matches": matches, "source": str(SOURCE.relative_to(ROOT)),
              "sourceSha256": sha256(SOURCE), "generator": Path(__file__).name,
              "generatorSha256": sha256(Path(__file__)), "generatorDependencies": {
                  "match_ov000_20261029_leaf.py": sha256(ROOT / "match_ov000_20261029_leaf.py")},
              "pythonVersion": sys.version, "unicornVersion": unicorn_version,
              "wholeModuleLinked": False, "sourceReconstructionComplete": False,
              "nativeSymbols": {rel["symbol"]: rel["target"] for entry in matches for rel in entry["relocations"]}}
    snapshot = WORK / ("match-" + compiler.sha(json.dumps(result, sort_keys=True).encode()) + ".json")
    compiler.immutable(snapshot, json.dumps(result, indent=2).encode())
    write_json(REPORT, result)
    print(json.dumps({"functions": len(matches), "bytes": sum(entry["bytes"] for entry in matches),
                      "executions": sum(entry["oracle"]["executions"] for entry in matches),
                      "report": str(REPORT.relative_to(ROOT))}))


if __name__ == "__main__":
    run()
