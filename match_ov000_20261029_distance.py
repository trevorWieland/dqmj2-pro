import itertools
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
WORK = ROOT / "work/ov000-recovery/20261029/distance15"
SOURCE = ROOT / "src/overlays/ov000_20261029_distance_e298aa833414.c"
REPORT = ROOT / "evidence/matches/ov000-20261029-distance01.json"
STACK = 0x03010000
STOP = 0x04000000
STATE = 0x0223033C
MASK = 0xFFFFFFFF
WIDE = 0xFFFFFFFFFFFFFFFF


def fixtures():
    randomizer = random.Random(20261029150)
    result = []
    special = [0, 1, MASK, 0x7FFFFFFF, 0x80000000, 0x80000001]
    for deltas in itertools.product(special, repeat=3):
        global_values = [randomizer.getrandbits(32) for unused in range(3)]
        input_values = [(value - delta) & MASK for value, delta in zip(global_values, deltas)]
        result.append((global_values, input_values, False))
    for unused in range(64):
        result.append(([randomizer.getrandbits(32) for unused in range(3)],
                       [randomizer.getrandbits(32) for unused in range(3)], False))
    for unused in range(16):
        values = [randomizer.getrandbits(32) for unused in range(3)]
        result.append((values, values, True))
    return result


def model(global_values, input_values):
    deltas = [((left - right + 0x80000000) & MASK) - 0x80000000
              for left, right in zip(global_values, input_values)]
    unsigned_sum = sum(delta * delta for delta in deltas) & WIDE
    signed_sum = unsigned_sum - (1 << 64) if unsigned_sum >> 63 else unsigned_sum
    return (signed_sum >> 12) & WIDE, bool(unsigned_sum >> 63)


def execute(entry, code, global_values, input_values, alias, expected, seed):
    randomizer = random.Random(seed)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    engine.ctl_set_cpu_model(UC_CPU_ARM_946)
    engine.mem_map(0x02000000, 0x400000)
    engine.mem_map(STACK, 0x10000)
    engine.mem_map(STOP, 0x1000)
    address = int(entry["address"], 0)
    engine.mem_write(address, code)
    state = bytearray(randomizer.randbytes(0x68))
    struct.pack_into("<3I", state, 0x5C, *global_values)
    engine.mem_write(STATE, bytes(state))
    engine.mem_write(STACK, randomizer.randbytes(0x10000))
    argument = STATE + 0x5C if alias else STACK + 0x1000
    if not alias:
        engine.mem_write(argument, struct.pack("<3I", *input_values))
    registers = [randomizer.getrandbits(32) for unused in range(13)]
    registers[0] = argument
    engine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
    for index, value in enumerate(registers):
        engine.reg_write(UC_ARM_REG_R0 + index, value)
    engine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    engine.reg_write(UC_ARM_REG_LR, STOP)
    reads, writes, executed = [], [], []
    literal_start = min([rel["offset"] for rel in entry["relocations"] if rel["type"] == 2])
    initial_ram = compiler.sha(bytes(engine.mem_read(0x02000000, 0x400000)))

    def step(machine, pc, size, user):
        if not address <= pc < address + literal_start:
            raise ValueError("Wide arithmetic escaped its own instructions")
        executed.append(pc)

    def read(machine, access, location, size, value, user):
        pool = address + literal_start <= location and location + size <= address + len(code)
        coordinate = location in [STATE + 0x5C, STATE + 0x60, STATE + 0x64,
                                  argument, argument + 4, argument + 8] and size == 4
        stack = STACK + 0xFFE8 <= location and location + size <= STACK + 0xFFF0
        if not pool and not coordinate and not stack:
            raise ValueError("Wide arithmetic read escaped known words, pool or saved frame")
        reads.append((location, size))

    def written(machine, access, location, size, value, user):
        if not STACK + 0xFFE8 <= location or location + size > STACK + 0xFFF0:
            raise ValueError("Wide arithmetic wrote beyond its eight-byte saved frame")
        writes.append((location, size, value & ((1 << (8 * size)) - 1)))

    engine.hook_add(UC_HOOK_CODE, step)
    engine.hook_add(UC_HOOK_MEM_READ, read)
    engine.hook_add(UC_HOOK_MEM_WRITE, written)
    engine.emu_start(address, STOP, count=10000)
    pair = engine.reg_read(UC_ARM_REG_R0) | engine.reg_read(UC_ARM_REG_R0 + 1) << 32
    if engine.reg_read(UC_ARM_REG_PC) != STOP or pair != expected:
        raise ValueError("Independent signed64-bit result or actual return differs")
    if engine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError("Wide arithmetic failed to restore SP")
    if any(engine.reg_read(UC_ARM_REG_R0 + index) != registers[index] for index in range(4, 12)):
        raise ValueError("Wide arithmetic changed a preserved register")
    final_ram = compiler.sha(bytes(engine.mem_read(0x02000000, 0x400000)))
    if final_ram != initial_ram:
        raise ValueError("Wide arithmetic modified its code or global operands")
    if bytes(engine.mem_read(argument, 12)) != struct.pack("<3I", *input_values):
        raise ValueError("Wide arithmetic modified its input")
    final_registers = [engine.reg_read(UC_ARM_REG_R0 + index) for index in range(13)]
    final_registers += [engine.reg_read(register) for register in [
        UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
    ]]
    return {"returnUnsignedBits": pair, "registers": final_registers, "reads": reads,
            "writes": writes, "executed": executed, "ramSha256": final_ram,
            "stackSha256": compiler.sha(bytes(engine.mem_read(STACK, 0x10000)))}


def oracle(entry, linked, binary, base):
    address = int(entry["address"], 0)
    native = binary[address - base : address - base + entry["bytes"]]
    vectors = []
    for index, (global_values, input_values, alias) in enumerate(fixtures()):
        expected, negative_sum = model(global_values, input_values)
        seed = 20261029150 + index
        original = execute(entry, native, global_values, input_values, alias, expected, seed)
        rebuilt = execute(entry, linked, global_values, input_values, alias, expected, seed)
        if original != rebuilt:
            raise ValueError("Full native/linked wide-arithmetic machine effects differ")
        vectors.append({"index": index, "globalWords": global_values, "inputWords": input_values,
                        "exactGlobalAlias": alias, "signedSumNegative": negative_sum,
                        "returnUnsignedBits": expected, "instructions": len(original["executed"]),
                        "stateSha256": compiler.sha(json.dumps(original, sort_keys=True).encode())})
    return {"passed": True, "vectors": len(vectors), "executions": len(vectors) * 2,
            "nativeInstructions": sum(vector["instructions"] for vector in vectors),
            "negativeWrappedSums": sum(vector["signedSumNegative"] for vector in vectors),
            "results": vectors, "actualReturnRequired": True, "instructionLimit": 10000,
            "freshMachinePerExecution": True, "cpuModel": "ARM946", "returnRegisters": ["R0", "R1"],
            "independentModel": "Three signed32-bit wrapped coordinate differences; sum of squares modulo64; signed arithmetic shift12, returned as64-bit R1:R0",
            "comparedEffects": "Full R0-R15/CPSR,4MiB RAM/64KiB stack, ordered reads/value-bearing writes and executed PCs",
            "externalCallees": [], "externalCalleesExecutedNatively": False,
            "limitations": ["Input is a valid aligned three-word object or the exact global vector alias", "Game-level meaning and coordinate scale are not asserted", "Unsigned-to-signed reinterpretation and signed right shift are measured for the pinned compiler/target; portability to other C implementations is not asserted"]}


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python and Unicorn versions are required")
    binary, metadata, provenance = original_module()
    compiler.WORK = WORK / "compiler"
    save_link_snapshots.DIRECTORY = WORK / "link-artifacts"
    report, codes = compiler.compile_compare("ov000", SOURCE, "2", "off")
    if report["returncode"] or len(report["functions"]) != 1:
        raise ValueError("Frozen wide-arithmetic unit did not yield one function")
    compile_path = WORK / ("compile-" + compiler.sha(json.dumps(report, sort_keys=True).encode()) + ".json")
    compiler.immutable(compile_path, json.dumps(report, indent=2).encode())
    entry = {**report["functions"][0], "processor": "arm9", "sourceLanguage": "C", "sourceReturnType": "s64"}
    if not entry["exactAfterDeclaredRelocation"]:
        raise ValueError("Frozen wide-arithmetic C no longer fully matches")
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
                      "negativeWrappedSums": entry["oracle"]["negativeWrappedSums"],
                      "report": str(REPORT.relative_to(ROOT))}))


if __name__ == "__main__":
    run()
