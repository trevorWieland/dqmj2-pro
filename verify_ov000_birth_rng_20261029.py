import itertools
import json
import random
import struct
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from ledger_state import collect_matches
from link_runtime_unit import measured_module, validate
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn import __version__ as unicorn_version
from unicorn.arm_const import (
    UC_ARM_REG_CPSR,
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_SP,
    UC_CPU_ARM_946,
)

WORK = ROOT / "work/ov000-recovery/20261029/birth-rng"
REPORT = ROOT / "evidence/application/ov000-birth-rng-20261029.json"
ADDRESS = 0x0222976C
STOP = 0x027FF800
STACK = 0x027FF000
LEFT, RIGHT = 0x02700000, 0x02700200
ITEMS, SPECIES = 0x02500000, 0x02540000
STATE, CONTEXT, CHILD = 0x020F6044, 0x02247480, 0x022474C8
HELPERS = {
    0x0203D294: 72,
    0x02026350: 484,
    0x02044D60: 36,
    0x02065D88: 24,
    ADDRESS: 240,
}


def word(machine, address):
    return struct.unpack("<I", machine.mem_read(address, 4))[0]


def advance(seed, bound):
    seed = (seed * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
    return seed, (seed >> 16) % bound


def model(seed, left_trait, right_trait, forced):
    selector = {1: 0, 2: 1}.get(left_trait, 9)
    if right_trait == 1:
        selector = 9 if selector == 1 else 0
    if right_trait == 2:
        selector = 9 if selector == 0 else 1
    draws = []
    if selector == 9:
        before = seed
        seed, result = advance(seed, 17)
        draws.append((17, before, seed, result))
        selector = 2
        if result:
            before = seed
            seed, result = advance(seed, 1024)
            draws.append((1024, before, seed, result))
            selector = result & 1
    return 2 if forced else selector, seed, draws


def execute(main, overlay, code, item_data, kind_data, case, serial):
    left_id, right_id, species_id, seed = case
    rng = random.Random(202610290000 + serial)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000, 0x00800000)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ADDRESS, code)
    machine.mem_write(ITEMS, item_data)
    machine.mem_write(SPECIES, kind_data)
    machine.mem_write(0x021C2AB4, struct.pack("<I", ITEMS))
    machine.mem_write(0x020F69F0, struct.pack("<I", SPECIES))
    machine.mem_write(STATE, struct.pack("<I", seed))
    parents = [bytearray(rng.randbytes(0x84)), bytearray(rng.randbytes(0x84))]
    for location, parent, item_id in zip((LEFT, RIGHT), parents, (left_id, right_id)):
        parent[0x31] = item_id
        machine.mem_write(location, bytes(parent))
    context = rng.randbytes(0x48)
    child = rng.randbytes(0x84)
    stack = rng.randbytes(0x7000)
    machine.mem_write(CONTEXT, context)
    machine.mem_write(CHILD, child)
    machine.mem_write(STACK - 0x7000, stack)
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[:3] = [LEFT, RIGHT, species_id]
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for index, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    draws, visits, writes = [], [], []
    instruction_count = 0

    def step(engine, pc, size, user):
        nonlocal instruction_count
        instruction_count += 1
        if not any(start <= pc < start + length for start, length in HELPERS.items()):
            raise ValueError("Birth polarity escaped its complete native helper closure")
        if pc in HELPERS:
            visits.append((pc, engine.reg_read(UC_ARM_REG_R0)))
        if pc == 0x0203D294:
            draws.append([engine.reg_read(UC_ARM_REG_R0), word(engine, STATE)])
        if pc == 0x0203D2CC:
            draws[-1].extend([word(engine, STATE), engine.reg_read(UC_ARM_REG_R0 + 1)])

    def written(engine, access, location, size, value, user):
        permitted = ((STATE, 4), (CONTEXT + 4, 8), (CHILD + 0x1B, 1),
                     (STACK - 0x7000, 0x7000))
        if not any(base <= location and location + size <= base + length
                   for base, length in permitted):
            raise ValueError("Birth polarity wrote beyond its measured isolated state")
        writes.append((location, size, value & ((1 << (8 * size)) - 1)))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ADDRESS, STOP, count=10000)
    traits = [item_data[item * 88 + 0x2A] for item in (left_id, right_id)]
    forced = bool(struct.unpack_from("<H", kind_data, species_id * 100 + 4)[0] & 0x8000)
    polarity, final_seed, expected_draws = model(seed, *traits, forced)
    if machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise ValueError("Birth polarity failed to return within its instruction bound")
    if machine.reg_read(UC_ARM_REG_R0) != polarity or word(machine, STATE) != final_seed:
        raise ValueError("Native result or RNG state differs from the independent model")
    if [tuple(draw) for draw in draws] != expected_draws:
        raise ValueError("Native RNG draw order/value differs from independent recurrence")
    expected_context = bytearray(context)
    struct.pack_into("<II", expected_context, 4, LEFT, RIGHT)
    expected_child = bytearray(child)
    expected_child[0x1B] = polarity
    if bytes(machine.mem_read(CONTEXT, 0x48)) != expected_context:
        raise ValueError("Unexpected birth context memory effects")
    if bytes(machine.mem_read(CHILD, 0x84)) != expected_child:
        raise ValueError("Unexpected prepared child memory effects")
    if machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError("Native polarity helper did not restore SP")
    if any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 12)):
        raise ValueError("Native polarity helper changed a callee-preserved register")
    return {
        "case": [left_id, right_id, species_id, hex(seed)],
        "itemTraits": traits,
        "forcedNeutralSpecies": forced,
        "polarity": polarity,
        "stateAfter": hex(final_seed),
        "draws": draws,
        "visits": visits,
        "instructions": instruction_count,
        "registers": [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
        "cpsr": machine.reg_read(UC_ARM_REG_CPSR),
        "writeTraceSha256": compiler.sha(json.dumps(writes).encode()),
        "stackSha256": compiler.sha(bytes(machine.mem_read(STACK - 0x7000, 0x7000))),
        "actualReturn": True,
    }


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python and Unicorn are required")
    namespace = configuration()["romSha256"]
    matches, rejected = collect_matches(namespace)
    accepted = matches[("ov000", "arm", ADDRESS)]
    source = ROOT / accepted["source"]
    if sha256(source) != accepted["sourceSha256"]:
        raise ValueError("Accepted polarity source changed")
    compiler.WORK = WORK / "compiler"
    rows, found = compiler.compare(source, "ov000", "2", "off")
    entry, unused = found[accepted["name"]]
    bindings = qualified_bindings(entry)
    directory = WORK / "links" / entry["objectSha256"]
    proof = validate(entry, bindings, directory)
    save_link_snapshots.DIRECTORY = WORK / "link-artifacts"
    frozen = save_link_snapshots.freeze_link(proof)
    linked = (directory / "caller.bin").read_bytes()
    main_meta, main, unused = measured_module("main")
    overlay_meta, overlay, unused = measured_module("ov000")
    native = overlay[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 240]
    if linked != native:
        raise ValueError("Fresh genuine MW linked polarity source differs")
    item_path = ROOT / "extract/files/ItemTbl.bin"
    kind_path = ROOT / "extract/files/EnmyKindTbl.bin"
    item_data, kind_data = item_path.read_bytes()[8:], kind_path.read_bytes()[8:]
    if len(item_data) != 256 * 88 or len(kind_data) % 100:
        raise ValueError("Measured native resource row layout changed")
    item_traits = sorted(set(item_data[0x2A::88]))
    item_ids = [next(i for i in range(256) if item_data[i * 88 + 0x2A] == trait)
                for trait in item_traits]
    species_ids = [next(i for i in range(len(kind_data) // 100)
                        if bool(struct.unpack_from("<H", kind_data, i * 100 + 4)[0]
                                & 0x8000) == forced) for forced in (False, True)]
    neutral_seeds = [seed for seed in range(1024) if advance(seed, 17)[1] == 0][:8]
    seeds = list(dict.fromkeys(
        [0, 1, 42, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF] + neutral_seeds))
    results = []
    for serial, case in enumerate(itertools.product(item_ids, item_ids, species_ids, seeds)):
        native_result = execute(main, overlay, native, item_data, kind_data, case, serial)
        source_result = execute(main, overlay, linked, item_data, kind_data, case, serial)
        if source_result != native_result:
            raise ValueError("Native/source result, register, state or trace difference")
        results.append(native_result)
    report = {
        "schemaVersion": 1,
        "createdUtc": now(),
        "romSha256": namespace,
        "processor": "arm9",
        "module": "ov000",
        "address": hex(ADDRESS),
        "mode": "arm",
        "bytes": 240,
        "nativeSpanSha256": compiler.sha(native),
        "moduleSha256": overlay_meta["sha256"],
        "mainSha256": main_meta["sha256"],
        "source": accepted["source"],
        "sourceSha256": accepted["sourceSha256"],
        "freshCompilation": rows,
        "genuineLinkProof": proof,
        "frozenLinkArtifacts": frozen,
        "nativeSymbolEntries": bindings,
        "assets": [{"path": str(path.relative_to(ROOT)), "sha256": sha256(path)}
                   for path in (item_path, kind_path)],
        "fixtureItems": item_ids,
        "fixtureItemTraits": item_traits,
        "fixtureSpecies": species_ids,
        "vectors": len(results),
        "executions": len(results) * 2,
        "pythonVersion": sys.version,
        "unicornVersion": unicorn_version,
        "cpuModel": "ARM946",
        "instructionBoundPerExecution": 10000,
        "results": results,
        "matchedSourceCredit": 0,
        "reproduction": "python verify_ov000_birth_rng_20261029.py",
        "generatorSha256": sha256(Path(__file__)),
        "limitations": [
            "Synthetic isolated state and explicitly chosen hypothetical seeds",
            "Does not establish current/future scene RNG state or save serialization",
            "Only polarity helper closure; complete allocation and birth scene unsupported",
            "Accepted source is revalidated; no new function/source coverage is credited",
        ],
    }
    write_json(REPORT, report)
    print(json.dumps({"report": str(REPORT.relative_to(ROOT)), "vectors": len(results),
                      "executions": len(results) * 2, "itemIds": item_ids,
                      "speciesIds": species_ids}))


if __name__ == "__main__":
    run()
