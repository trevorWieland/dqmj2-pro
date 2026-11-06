import itertools
import json
import random
import struct
import sys
from pathlib import Path

import match_overlay_modules as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from project import configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from ndspy import codeCompression
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn import __version__ as unicorn_version
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP,
    UC_CPU_ARM_946,
)

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/ov000-recovery/20261029/leaf02"
SOURCE = ROOT / "src/overlays/ov000_20261029_leaf_9f510e0af6a5.c"
REPORT = ROOT / "evidence/matches/ov000-20261029-leaf01.json"
STOP = 0x04000000
STACK = 0x03010000
STATE = 0x0223033C
TABLE = 0x0222B854
MASK = 0xFFFFFFFF


def original_module():
    config = configuration()
    if sha256(config["rom"]) != config["romSha256"]:
        raise ValueError("Original ROM namespace changed")
    rom = config["rom"].read_bytes()
    offset, length = struct.unpack_from("<2I", rom, 0x50)
    rows = [struct.unpack_from("<8I", rom, at) for at in range(offset, offset + length, 32)]
    row = next(row for row in rows if row[0] == 0)
    fat = struct.unpack_from("<I", rom, 0x48)[0]
    first, last = struct.unpack_from("<2I", rom, fat + row[6] * 8)
    stored = rom[first:last]
    decoded = codeCompression.decompress(stored)
    metadata, binary, symbols = measured_module("ov000")
    if decoded != binary or row[1] != 0x021D7240 or row[2] != len(binary):
        raise ValueError("Original stored overlay differs from measured module")
    return binary, metadata, {
        "romSha256": config["romSha256"], "moduleInputSha256": compiler.sha(binary),
        "storedSha256": compiler.sha(stored), "storedRange": [first, last],
        "initializedBytes": len(binary), "bssBytes": row[3],
    }


def execute(entry, code, context, seed, table):
    randomizer = random.Random(seed)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    engine.ctl_set_cpu_model(UC_CPU_ARM_946)
    engine.mem_map(0x02000000, 0x400000)
    engine.mem_map(STACK, 0x10000)
    engine.mem_map(STOP, 0x1000)
    address = int(entry["address"], 0)
    engine.mem_write(address, code)
    engine.mem_write(TABLE, table)
    state = bytearray(randomizer.randbytes(0x9C))
    if address == 0x021D8528:
        counter, increment, result = context
        struct.pack_into("<I", state, 0x98, counter)
        struct.pack_into("<I", state, 0x4C, result)
        argument = increment
        expected = result
        struct.pack_into("<I", state, 0x98, (counter + increment) & MASK)
    else:
        argument = context[0]
        expected = (argument // 2 if not argument & 1 else -((argument + 1) // 2)) & MASK
    expected_state = bytes(state)
    if address == 0x021D8528:
        struct.pack_into("<I", state, 0x98, context[0])
    engine.mem_write(STATE, bytes(state))
    engine.mem_write(STACK, randomizer.randbytes(0x10000))
    registers = [randomizer.getrandbits(32) for unused in range(13)]
    registers[0] = argument
    engine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
    for index, value in enumerate(registers):
        engine.reg_write(UC_ARM_REG_R0 + index, value)
    engine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    engine.reg_write(UC_ARM_REG_LR, STOP)
    reads, writes, executed = [], [], []
    literal_start = min(
        [relocation["offset"] for relocation in entry["relocations"] if relocation["type"] == 2]
        or [len(code)]
    )

    def step(machine, pc, size, user):
        if not address <= pc < address + literal_start:
            raise ValueError("Leaf execution escaped own executable instructions")
        executed.append(pc)

    def memory(machine, access, location, size, value, user):
        allowed = [(address, address + len(code)), (STATE, STATE + 0x9C),
                   (TABLE, TABLE + 49), (STACK, STACK + 0x10000)]
        if not any(start <= location and location + size <= end for start, end in allowed):
            raise ValueError("Leaf data access escaped measured fixture domain")
        reads.append((location, size))

    def written(machine, access, location, size, value, user):
        if not (STACK <= location and location + size <= STACK + 0x10000) and not (
            address == 0x021D8528 and location == STATE + 0x98 and size == 4
        ):
            raise ValueError("Leaf write escaped counter or own scratch stack")
        writes.append((location, size, value & ((1 << (8 * size)) - 1)))

    engine.hook_add(UC_HOOK_CODE, step)
    engine.hook_add(UC_HOOK_MEM_READ, memory)
    engine.hook_add(UC_HOOK_MEM_WRITE, written)
    engine.emu_start(address, STOP, count=10000)
    returned = engine.reg_read(UC_ARM_REG_PC) == STOP
    if not returned or engine.reg_read(UC_ARM_REG_R0) != expected:
        raise ValueError("Independent leaf return or termination model differs")
    if bytes(engine.mem_read(STATE, 0x9C)) != expected_state:
        raise ValueError("Independent complete state model differs")
    if engine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError("Leaf failed to restore its stack")
    if any(engine.reg_read(UC_ARM_REG_R0 + index) != registers[index] for index in range(4, 12)):
        raise ValueError("Leaf changed an ABI-preserved register")
    final_registers = [engine.reg_read(UC_ARM_REG_R0 + index) for index in range(13)]
    final_registers += [engine.reg_read(register) for register in [
        UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
    ]]
    return {
        "return": expected, "returned": returned, "registers": final_registers,
        "ramSha256": compiler.sha(bytes(engine.mem_read(0x02000000, 0x400000))),
        "stackSha256": compiler.sha(bytes(engine.mem_read(STACK, 0x10000))),
        "reads": reads, "writes": writes, "executed": executed,
    }


def oracle(entry, linked, binary, base):
    table = binary[TABLE - base : TABLE - base + 49]
    expected_table = bytes((index // 2 if not index & 1 else -((index + 1) // 2)) & 255
                           for index in range(49))
    if table != expected_table:
        raise ValueError("Measured signed lookup no longer has the recorded values")
    address = int(entry["address"], 0)
    native = binary[address - base : address - base + entry["bytes"]]
    special = [0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFE, MASK]
    if address == 0x021D8528:
        contexts = list(itertools.product(special, repeat=3))
        randomizer = random.Random(20261029000)
        contexts += [tuple(randomizer.getrandbits(32) for unused in range(3)) for unused in range(64)]
    else:
        contexts = [(index,) for index in range(49)]
    vectors = []
    for index, context in enumerate(contexts):
        seed = 20261029000 + index
        original = execute(entry, native, context, seed, table)
        rebuilt = execute(entry, linked, context, seed, table)
        if original != rebuilt:
            raise ValueError("Full native/linked leaf machine effects differ")
        vectors.append({
            "index": index, "arguments": list(context), "return": original["return"],
            "instructions": len(original["executed"]),
            "stateSha256": compiler.sha(json.dumps(original, sort_keys=True).encode()),
        })
    return {
        "passed": True, "vectors": len(vectors), "executions": len(vectors) * 2,
        "nativeInstructions": sum(vector["instructions"] for vector in vectors),
        "results": vectors, "instructionLimit": 10000, "cpuModel": "ARM946",
        "actualReturnRequired": True, "freshMachinePerExecution": True,
        "independentModel": "32-bit field accumulation with saved scalar return, or complete signed alternating49-byte lookup",
        "comparedEffects": "Full R0-R15/CPSR,4MiB RAM,64KiB stack, ordered reads and value-bearing writes, executed PCs",
        "externalCalleesExecutedNatively": False, "externalCallees": [],
        "limitations": ["Lookup indexes outside0..48 are unsupported", "No hardware or game-level semantic claim", "Only the selected native leaf and its source-built replacement execute; all other RAM is synthetic context"],
    }


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python and Unicorn versions are required")
    binary, metadata, provenance = original_module()
    compiler.WORK = WORK / "compiler"
    save_link_snapshots.DIRECTORY = WORK / "link-artifacts"
    report, codes = compiler.compile_compare("ov000", SOURCE, "2", "off")
    if report["returncode"] or len(report["functions"]) != 2:
        raise ValueError("Frozen leaf unit did not produce the two target functions")
    compile_path = WORK / ("compile-" + compiler.sha(json.dumps(report, sort_keys=True).encode()) + ".json")
    compiler.immutable(compile_path, json.dumps(report, indent=2).encode())
    matches = []
    for function in report["functions"]:
        if not function["exactAfterDeclaredRelocation"]:
            raise ValueError("Frozen ordinary C leaf no longer matches")
        entry = {**function, "processor": "arm9", "sourceLanguage": "C"}
        bindings = qualified_bindings(entry)
        directory = WORK / "links" / entry["name"] / entry["objectSha256"]
        proof = validate(entry, bindings, directory)
        linked = (directory / "caller.bin").read_bytes()
        entry.update(save_link_snapshots.freeze_link(proof))
        entry.update(
            nativeSymbolEntries=bindings, isolatedCallerLink=proof,
            oracle=oracle(entry, linked, binary, int(metadata["base"], 0)),
            ordinaryCBytes=entry["bytes"], justifiedAssemblyBytes=0,
            compileReport=str(compile_path.relative_to(ROOT)),
        )
        matches.append(entry)
    result = {
        "schemaVersion": 1, "createdUtc": now(), "module": "ov000", "processor": "arm9",
        **provenance, "matches": matches,
        "source": str(SOURCE.relative_to(ROOT)), "sourceSha256": sha256(SOURCE),
        "generator": Path(__file__).name, "generatorSha256": sha256(Path(__file__)),
        "pythonVersion": sys.version, "unicornVersion": unicorn_version,
        "wholeModuleLinked": False, "sourceReconstructionComplete": False,
        "nativeSymbols": {rel["symbol"]: rel["target"] for entry in matches for rel in entry["relocations"]},
    }
    snapshot = WORK / ("match-" + compiler.sha(json.dumps(result, sort_keys=True).encode()) + ".json")
    compiler.immutable(snapshot, json.dumps(result, indent=2).encode())
    write_json(REPORT, result)
    print(json.dumps({"functions": len(matches), "bytes": sum(entry["bytes"] for entry in matches),
                      "executions": sum(entry["oracle"]["executions"] for entry in matches),
                      "report": str(REPORT.relative_to(ROOT))}))


if __name__ == "__main__":
    run()
