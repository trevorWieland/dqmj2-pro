import json
import random
import struct
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
WORK = ROOT / "work/ov000-recovery/20261029/registries08"
SOURCE = ROOT / "src/overlays/ov000_20261029_registries_3c92cfe807e5.c"
REPORT = ROOT / "evidence/matches/ov000-20261029-registries01.json"
STACK = 0x03010000
STOP = 0x04000000
GROUPS = [
    (0x02231F64, 48, 16, [0x021DF544, 0x021DF578, 0x021DF5A8]),
    (0x02231E44, 24, 12, [0x021DF5F0, 0x021DF624, 0x021DF654]),
    (0x02231C04, 24, 12, [0x021DF69C, 0x021DF6D0, 0x021DF700]),
    (0x02231D24, 24, 12, [0x021DF748, 0x021DF77C, 0x021DF7AC]),
]


def fixture(index, count):
    randomizer = random.Random(20261029080 + index)
    keys = [randomizer.randrange(1, 0x7FFFFFFF) for unused in range(count)]
    if index < count * 4:
        kind, position = divmod(index, count)
        query = [0, 0x80000000, 0xFFFFFFFF, 0xDEADBEEF][kind]
        if kind == 0:
            keys[position] = 0
        elif kind == 1:
            keys = [0] * count
            keys[position] = query
        elif kind == 2:
            keys[position] = query
            keys[-1] = query
    else:
        edge = index - count * 4
        keys = [[0] * count, [0xFFFFFFFF] * count, [0x80000000] * count,
                list(range(count))][edge // 2]
        query = [0, 1, 0xFFFFFFFF, 0, 0x80000000, 0, count - 1, count][edge]
    return keys, query


def expected_result(keys, query, base, stride, operation):
    if operation == 1:
        return next((index for index, key in enumerate(keys) if key == 0), 0xFFFFFFFF)
    found = next((index for index, key in enumerate(keys) if key == query), None)
    if operation == 0:
        return int(found is not None)
    return 0 if found is None else base + found * stride + 4


def execute(entry, code, base, stride, keys, query, expected, seed):
    randomizer = random.Random(seed)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    engine.ctl_set_cpu_model(UC_CPU_ARM_946)
    engine.mem_map(0x02000000, 0x400000)
    engine.mem_map(STACK, 0x10000)
    engine.mem_map(STOP, 0x1000)
    address = int(entry["address"], 0)
    engine.mem_write(address, code)
    records = bytearray(randomizer.randbytes(stride * len(keys)))
    for index, key in enumerate(keys):
        struct.pack_into("<I", records, index * stride, key)
    engine.mem_write(base, bytes(records))
    engine.mem_write(STACK, randomizer.randbytes(0x10000))
    registers = [randomizer.getrandbits(32) for unused in range(13)]
    registers[0] = query
    engine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
    for index, value in enumerate(registers):
        engine.reg_write(UC_ARM_REG_R0 + index, value)
    engine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    engine.reg_write(UC_ARM_REG_LR, STOP)
    reads, executed = [], []
    literal_start = min([rel["offset"] for rel in entry["relocations"] if rel["type"] == 2])
    initial_ram = compiler.sha(bytes(engine.mem_read(0x02000000, 0x400000)))
    initial_stack = compiler.sha(bytes(engine.mem_read(STACK, 0x10000)))

    def step(machine, pc, size, user):
        if not address <= pc < address + literal_start:
            raise ValueError("Registry execution escaped its own code before literal pool")
        executed.append(pc)

    def read(machine, access, location, size, value, user):
        pool = address + literal_start <= location and location + size <= address + len(code)
        key = base <= location < base + len(records) and (location - base) % stride == 0 and size == 4
        if not pool and not key:
            raise ValueError("Registry read escaped its literal pool or measured32-bit keys")
        reads.append((location, size))

    def written(machine, access, location, size, value, user):
        raise ValueError("Read-only native registry helper unexpectedly wrote memory")

    engine.hook_add(UC_HOOK_CODE, step)
    engine.hook_add(UC_HOOK_MEM_READ, read)
    engine.hook_add(UC_HOOK_MEM_WRITE, written)
    engine.emu_start(address, STOP, count=10000)
    if engine.reg_read(UC_ARM_REG_PC) != STOP:
        raise ValueError("Registry helper did not actually return")
    if engine.reg_read(UC_ARM_REG_R0) != expected:
        raise ValueError("Independent first-match/first-zero model differs")
    if any(engine.reg_read(UC_ARM_REG_R0 + index) != registers[index] for index in range(4, 12)):
        raise ValueError("Registry helper changed a preserved register")
    if engine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError("Registry helper changed SP")
    final_ram = compiler.sha(bytes(engine.mem_read(0x02000000, 0x400000)))
    final_stack = compiler.sha(bytes(engine.mem_read(STACK, 0x10000)))
    if final_ram != initial_ram or final_stack != initial_stack:
        raise ValueError("Registry helper changed read-only fixture memory")
    final_registers = [engine.reg_read(UC_ARM_REG_R0 + index) for index in range(13)]
    final_registers += [engine.reg_read(register) for register in [
        UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
    ]]
    return {"return": expected, "registers": final_registers, "reads": reads,
            "executed": executed, "ramSha256": final_ram, "stackSha256": final_stack}


def oracle(entry, linked, binary, module_base):
    address = int(entry["address"], 0)
    base, stride, count, functions = next(group for group in GROUPS if address in group[3])
    operation = functions.index(address)
    native = binary[address - module_base : address - module_base + entry["bytes"]]
    vectors = []
    for index in range(count * 4 + 8):
        keys, query = fixture(index, count)
        expected = expected_result(keys, query, base, stride, operation)
        seed = 20261029080 + index
        original = execute(entry, native, base, stride, keys, query, expected, seed)
        rebuilt = execute(entry, linked, base, stride, keys, query, expected, seed)
        if original != rebuilt:
            raise ValueError("Full original/linked registry machine effects differ")
        vectors.append({"index": index, "query": query, "keys": keys, "return": expected,
                        "instructions": len(original["executed"]),
                        "stateSha256": compiler.sha(json.dumps(original, sort_keys=True).encode())})
    return {"passed": True, "vectors": len(vectors), "executions": len(vectors) * 2,
            "nativeInstructions": sum(vector["instructions"] for vector in vectors),
            "results": vectors, "actualReturnRequired": True, "instructionLimit": 10000,
            "freshMachinePerExecution": True, "cpuModel": "ARM946", "tableBase": hex(base),
            "recordStride": stride, "recordCount": count, "operation": ["contains-key", "first-zero", "first-key-payload"][operation],
            "independentModel": "Full32-bit key equality, first matching row or first zero row, and payload address at record+4",
            "comparedEffects": "Full R0-R15/CPSR, unchanged4MiB RAM/64KiB stack, ordered reads and executed PCs",
            "externalCallees": [], "externalCalleesExecutedNatively": False,
            "limitations": ["Game-level meaning of keys and payloads is unknown", "Mutable payloads are randomized but never read by these helpers", "Only these native leaf bodies execute; no hardware or other game routines run"]}


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python and Unicorn versions are required")
    binary, metadata, provenance = original_module()
    compiler.WORK = WORK / "compiler"
    save_link_snapshots.DIRECTORY = WORK / "link-artifacts"
    report, codes = compiler.compile_compare("ov000", SOURCE, "2,p", "off")
    if report["returncode"] or len(report["functions"]) != 12:
        raise ValueError("Frozen registry source no longer yields twelve functions")
    compile_path = WORK / ("compile-" + compiler.sha(json.dumps(report, sort_keys=True).encode()) + ".json")
    compiler.immutable(compile_path, json.dumps(report, indent=2).encode())
    matches = []
    for function in report["functions"]:
        if not function["exactAfterDeclaredRelocation"]:
            raise ValueError("Frozen registry source no longer fully matches")
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
