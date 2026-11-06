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
WORK = ROOT / "work/ov000-recovery/20261029/halfkeys12"
SOURCE = ROOT / "src/overlays/ov000_20261029_halfkeys_8d41ce185b7d.c"
REPORT = ROOT / "evidence/matches/ov000-20261029-halfkeys01.json"
STACK = 0x03010000
STOP = 0x04000000
TABLE = 0x02232868
FUNCTIONS = [0x021E5594, 0x021E5744, 0x021E577C]


def fixture(index):
    randomizer = random.Random(20261029120 + index)
    records = bytearray(randomizer.randbytes(32 * 20))
    if index < 128:
        kind, position = divmod(index, 32)
        keys = [0x100 + row for row in range(32)]
        if kind == 0:
            query = 0xABCD0000 | (position + 1)
            keys[position] = query & 255
        elif kind == 1:
            query = 0xFFFFFF00
            keys = [0] * 32
            keys[position] = 0x100
        elif kind == 2:
            query = 0x1234FFFF
            keys[position] = 255
            keys[-1] = 255
        else:
            query = 0xFFFFFF80
            keys = [0x180] * 32
    else:
        edge = index - 128
        keys = [[0] * 32, [255] * 32, [65535] * 32, [256] * 32,
                [0x8000] * 32, [128] * 32, list(range(32)), list(range(32))][edge]
        query = [0, 0xFFFFFFFF, 0xFFFFFFFF, 0, 0, 0x80000080, 0xFFFF001F, 0xFFFF00FF][edge]
    for row, key in enumerate(keys):
        struct.pack_into("<H", records, row * 20, key)
    value = [0, 1, 127, 128, 255, 256, 0xABCDEF01, 0xFFFFFFFF][index % 8]
    return bytes(records), keys, query, value


def model(records, keys, query, value, operation):
    result = bytearray(records)
    matches = [index for index, key in enumerate(keys) if key == query & 255]
    if operation == 0:
        for index in matches:
            struct.pack_into("<H", result, index * 20, 0)
        expected = len(matches)
    elif operation == 1:
        expected = TABLE + matches[0] * 20 + 4 if matches else 0
    else:
        for index in matches:
            result[index * 20 + 3] = value & 255
        expected = keys[-1]
    return bytes(result), expected


def execute(entry, code, records, query, value, expected_records, expected, seed):
    randomizer = random.Random(seed)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    engine.ctl_set_cpu_model(UC_CPU_ARM_946)
    engine.mem_map(0x02000000, 0x400000)
    engine.mem_map(STACK, 0x10000)
    engine.mem_map(STOP, 0x1000)
    address = int(entry["address"], 0)
    engine.mem_write(address, code)
    engine.mem_write(TABLE, records)
    engine.mem_write(STACK, randomizer.randbytes(0x10000))
    registers = [randomizer.getrandbits(32) for unused in range(13)]
    registers[:2] = [query, value]
    engine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
    for index, argument in enumerate(registers):
        engine.reg_write(UC_ARM_REG_R0 + index, argument)
    engine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    engine.reg_write(UC_ARM_REG_LR, STOP)
    reads, writes, executed = [], [], []
    literal_start = min([rel["offset"] for rel in entry["relocations"] if rel["type"] == 2])

    def step(machine, pc, size, user):
        if not address <= pc < address + literal_start:
            raise ValueError("Half-key execution escaped its own instructions")
        executed.append(pc)

    def read(machine, access, location, size, data, user):
        pool = address + literal_start <= location and location + size <= address + len(code)
        key = TABLE <= location < TABLE + 640 and (location - TABLE) % 20 == 0 and size == 2
        stack = STACK <= location and location + size <= STACK + 0x10000
        if not pool and not key and not stack:
            raise ValueError("Half-key read escaped its literal pool,16-bit keys or stack")
        reads.append((location, size))

    def written(machine, access, location, size, data, user):
        stack = STACK <= location and location + size <= STACK + 0x10000
        field = TABLE <= location < TABLE + 640
        offset = (location - TABLE) % 20
        clear = address == FUNCTIONS[0] and offset == 0 and size == 2 and data == 0
        update = address == FUNCTIONS[2] and offset == 3 and size == 1 and data == value & 255
        if not stack and not (field and (clear or update)):
            raise ValueError("Half-key write escaped its supported record fields or stack")
        writes.append((location, size, data & ((1 << (8 * size)) - 1)))

    engine.hook_add(UC_HOOK_CODE, step)
    engine.hook_add(UC_HOOK_MEM_READ, read)
    engine.hook_add(UC_HOOK_MEM_WRITE, written)
    engine.emu_start(address, STOP, count=10000)
    if engine.reg_read(UC_ARM_REG_PC) != STOP or engine.reg_read(UC_ARM_REG_R0) != expected:
        raise ValueError("Independent half-key return or actual termination differs")
    if bytes(engine.mem_read(TABLE, 640)) != expected_records:
        raise ValueError("Independent complete record-memory model differs")
    if engine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError("Half-key helper failed to restore SP")
    if any(engine.reg_read(UC_ARM_REG_R0 + index) != registers[index] for index in range(4, 12)):
        raise ValueError("Half-key helper changed a preserved register")
    final_registers = [engine.reg_read(UC_ARM_REG_R0 + index) for index in range(13)]
    final_registers += [engine.reg_read(register) for register in [
        UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
    ]]
    return {"return": expected, "registers": final_registers, "reads": reads,
            "writes": writes, "executed": executed,
            "ramSha256": compiler.sha(bytes(engine.mem_read(0x02000000, 0x400000))),
            "stackSha256": compiler.sha(bytes(engine.mem_read(STACK, 0x10000)))}


def oracle(entry, linked, binary, base):
    address = int(entry["address"], 0)
    operation = FUNCTIONS.index(address)
    native = binary[address - base : address - base + entry["bytes"]]
    vectors = []
    for index in range(136):
        records, keys, query, value = fixture(index)
        expected_records, expected = model(records, keys, query, value, operation)
        seed = 20261029120 + index
        original = execute(entry, native, records, query, value, expected_records, expected, seed)
        rebuilt = execute(entry, linked, records, query, value, expected_records, expected, seed)
        if original != rebuilt:
            raise ValueError("Full original/linked half-key machine effects differ")
        vectors.append({"index": index, "query": query, "valueRegisterCarrier": value,
                        "keys": keys, "return": expected, "instructions": len(original["executed"]),
                        "stateSha256": compiler.sha(json.dumps(original, sort_keys=True).encode())})
    return {"passed": True, "vectors": len(vectors), "executions": len(vectors) * 2,
            "nativeInstructions": sum(vector["instructions"] for vector in vectors),
            "results": vectors, "actualReturnRequired": True, "instructionLimit": 10000,
            "freshMachinePerExecution": True, "cpuModel": "ARM946",
            "operation": ["clear-all-keys-and-count", "first-key-payload", "update-byte3-return-last-key"][operation],
            "independentModel": "32 records of20 bytes; full16-bit record keys compare with low8 query bits; key clears and byte3 writes preserve all other bytes",
            "comparedEffects": "Full R0-R15/CPSR,4MiB RAM/64KiB stack, ordered reads/value-bearing writes and executed PCs",
            "externalCallees": [], "externalCalleesExecutedNatively": False,
            "limitations": ["Game-level field meanings are unknown", "R1 carrier robustness is tested beyond the source u8 parameter's scalar domain; only its low8 bits are stored", "No hardware or additional native routines execute"]}


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python and Unicorn versions are required")
    binary, metadata, provenance = original_module()
    compiler.WORK = WORK / "compiler"
    save_link_snapshots.DIRECTORY = WORK / "link-artifacts"
    report, codes = compiler.compile_compare("ov000", SOURCE, "2", "off")
    if report["returncode"] or len(report["functions"]) != 3:
        raise ValueError("Frozen half-key source no longer yields three functions")
    compile_path = WORK / ("compile-" + compiler.sha(json.dumps(report, sort_keys=True).encode()) + ".json")
    compiler.immutable(compile_path, json.dumps(report, indent=2).encode())
    matches = []
    for function in report["functions"]:
        if not function["exactAfterDeclaredRelocation"]:
            raise ValueError("Frozen half-key C no longer fully matches")
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
