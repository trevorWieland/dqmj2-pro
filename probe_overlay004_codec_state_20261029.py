import json
import random
import struct
import sys
from pathlib import Path

import audit_overlay004 as audit
import match_overlay_modules as matcher
from unicorn import UC_HOOK_MEM_WRITE, __version__ as unicorn_version
from unicorn.arm_const import (
    UC_ARM_REG_CPSR,
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_SP,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "work/overlay004-recovery/20261029/native-state14"
MASK = 0xFFFFFFFF


def word(arena, position):
    return int.from_bytes(arena[position : position + 4], "little")


def store(arena, position, value):
    arena[position : position + 4] = (value & MASK).to_bytes(4, "little")


def classify(instruction):
    opcode = instruction >> 24
    if opcode & 14 != 10:
        return 0
    if opcode & 240 == 240:
        return 1
    return 2 if opcode & 1 else 3


def reference(raw_state, initial, start, destination, length, encrypt):
    arena = bytearray(initial)
    feedback, first, second = struct.unpack_from("<3I", raw_state)
    table = list(raw_state[12:])
    if length & 3:
        return raw_state, bytes(arena), MASK

    def key_byte():
        nonlocal first, second
        first = (first + 1 + feedback) & 255
        left = table[first]
        second = (second + left + feedback) & 255
        right = table[second]
        table[second] = left
        table[first] = right
        return table[(left + right) & 255]

    for offset in range(0, length, 4):
        source = start + offset
        output = destination + offset
        instruction = word(arena, source)
        kind = classify(instruction)
        if kind in ([1, 2] if encrypt else [1, 3]):
            store(arena, output, instruction)
            high = (word(arena, output) & 0xFF000000) ^ 0x01000000
            delta = 0x402 if encrypt else -0x402
            low = ((word(arena, output) & 0xFFFFFF) + delta) & 0xFFFFFF
            feedback = (feedback + ((high if encrypt else instruction) >> 24)) & MASK
            store(arena, output, high | low)
            continue
        if encrypt and kind == 3:
            store(arena, source, word(arena, source) ^ 0x01000000)
        for index in [0, 1]:
            encoded = arena[source + index]
            value = key_byte() ^ encoded
            feedback = value if encrypt else encoded
            arena[output + index] = value
        if encrypt:
            arena[output + 2] = arena[source + 2] ^ 255
            arena[output + 3] = arena[source + 3]
            feedback = (feedback * arena[output + 2] - arena[output + 3]) & MASK
        else:
            feedback = (feedback * arena[source + 2] - arena[source + 3]) & MASK
            arena[output + 2] = arena[source + 2] ^ 255
            arena[output + 3] = arena[source + 3]
            if kind == 2:
                store(arena, source, word(arena, source) ^ 0x01000000)
    state = struct.pack("<3I", feedback, first, second) + bytes(table)
    return state, bytes(arena), 0


def fixture(index):
    randomizer = random.Random(0x00402900 + index)
    table = list(range(256))
    randomizer.shuffle(table)
    if index % 7 == 0:
        table = list(randomizer.randbytes(256))
    feedback = [0xAA, 0, 255, 65535, 0x7FFFFFFF, MASK][index % 6]
    first = randomizer.getrandbits(32) if index % 13 == 0 else randomizer.randrange(256)
    second = randomizer.getrandbits(32) if index % 17 == 0 else randomizer.randrange(256)
    state = struct.pack("<3I", feedback, first, second) + bytes(table)
    arena = bytearray(randomizer.randbytes(1024))
    length = [0, 4, 8, 16, 32, 64, 128, 1, 2, 3, 5][index % 11]
    if length & 3 and index % 3 == 0:
        length |= 0xFFFFFF00
    start = 256
    shift = [-16, -4, 0, 4, 16, 256][(index // 11) % 6]
    populated = 4 if length & 3 else length
    for offset in range(0, populated, 4):
        opcode = (index + offset // 4) & 255
        if index % 3 == 0:
            opcode = [0xEA, 0xEB, 0xFA, 0xFB, 0x1A, 0x1B, 0xE1, 0xE5][
                (index + offset // 4) % 8
            ]
        store(arena, start + offset, opcode << 24 | randomizer.randrange(0x1000000))
    return state, bytes(arena), start, start + shift, length


def execute(image, bss, entry, vector, state, arena, start, destination, length):
    machine = audit.Machine(image, bss, vector)
    state_address = audit.STACK + 0x1000
    arena_address = audit.STACK + 0x2000
    machine.engine.mem_write(state_address, state)
    machine.engine.mem_write(arena_address, arena)
    writes = []

    def written(engine, access, address, size, value, user):
        writes.append((address, size, value & ((1 << (8 * size)) - 1)))

    machine.engine.hook_add(UC_HOOK_MEM_WRITE, written)
    arguments = (state_address, arena_address + start, arena_address + destination, length)
    poisoned = bool(length & 3 and vector % 2 or length == 0)
    if poisoned:
        arguments = (0xDEAD0000, 0xDEAD1000, 0xDEAD2000, length)
    result = machine.call(entry, arguments=arguments)
    allowed = [(entry, entry + (280 if entry == 0x021D8B00 else 392))]
    allowed += [(0x021D7DE8, 0x021D7E3C), (0x021D8A70, 0x021D8AC8)]
    allowed += [(0x021D8AC8, 0x021D8B00)]
    if any(not any(a <= pc < b for a, b in allowed) for pc in machine.executed):
        raise ValueError("Codec execution escaped target and three native helpers")
    registers = [machine.engine.reg_read(UC_ARM_REG_R0 + index) for index in range(13)]
    registers += [machine.engine.reg_read(register) for register in [
        UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
    ]]
    if machine.image() != image:
        raise ValueError("Codec changed its executable image")
    return {
        "return": result["result"],
        "state": bytes(machine.engine.mem_read(state_address, 268)),
        "arena": bytes(machine.engine.mem_read(arena_address, len(arena))),
        "stackSha256": audit.sha(bytes(machine.engine.mem_read(audit.STACK, 0x10000))),
        "registers": registers,
        "writes": writes,
        "instructions": machine.steps,
        "executed": sorted(machine.executed),
        "poisonedUnusedPointers": poisoned,
    }


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != "2.1.4":
        raise ValueError("Pinned Python 3.13.5 and Unicorn 2.1.4 are required")
    OUT.mkdir(parents=True, exist_ok=True)
    matcher.WORK = OUT / "compiler"
    data = audit.inputs()
    results = []
    for encrypt, address, inline in [
        (True, 0x021D8B00, "all"), (False, 0x021D8C18, "on,noauto")
    ]:
        name = "encrypt" if encrypt else "decrypt"
        source = ROOT / f"src/overlays/ov004_20261029_codec_{name}_draft.c"
        report, codes = matcher.compile_compare("ov004", source, "4,p", inline)
        if report["returncode"] or len(report["functions"]) != 1:
            raise ValueError("Draft source no longer compiles to one target")
        function = report["functions"][0]
        if function["compiledBytes"] != function["bytes"]:
            raise ValueError("Draft no longer has native target size")
        report_path = OUT / (audit.sha(json.dumps(report, sort_keys=True).encode()) + ".json")
        matcher.immutable(report_path, json.dumps(report, indent=2).encode())
        compiled = bytes.fromhex(function["compiledHex"])
        rebuilt = bytearray(data["analysis"])
        rebuilt[address - audit.BASE : address - audit.BASE + len(compiled)] = compiled
        vectors = []
        for vector in range(264):
            state, arena, start, destination, length = fixture(vector)
            expected_state, expected_arena, expected_return = reference(
                state, arena, start, destination, length, encrypt
            )
            paired = [execute(
                image, data["entry"][3], address, vector, state, arena, start,
                destination, length
            ) for image in [data["analysis"], bytes(rebuilt)]]
            for observed in paired:
                if (observed["state"], observed["arena"], observed["return"]) != (
                    expected_state, expected_arena, expected_return
                ):
                    raise ValueError(f"Independent model differs: {name} vector {vector}")
            if paired[0]["registers"] != paired[1]["registers"]:
                raise ValueError(f"Native/draft returned register state differs: {name} vector {vector}")
            observed = paired[0]
            differing = [key for key in paired[0] if paired[0][key] != paired[1][key]]
            write_differences = [
                {"index": index, "native": list(native), "draft": list(draft)}
                for index, (native, draft) in enumerate(zip(paired[0]["writes"], paired[1]["writes"]))
                if native != draft
            ]
            vectors.append({
                "index": vector, "length": length, "outputShift": destination - start,
                "return": expected_return, "instructions": observed["instructions"],
                "poisonedUnusedPointers": observed["poisonedUnusedPointers"],
                "stateSha256": audit.sha(observed["state"]),
                "arenaSha256": audit.sha(observed["arena"]),
                "stackSha256": observed["stackSha256"],
                "traceSha256": audit.sha(json.dumps(observed["writes"]).encode()),
                "registerSha256": audit.sha(json.dumps(observed["registers"]).encode()),
                "executedSha256": audit.sha(json.dumps(observed["executed"]).encode()),
                "fullMachineEffectsEqual": not differing,
                "differingMachineEffects": differing,
                "draftStackSha256": paired[1]["stackSha256"],
                "draftTraceSha256": audit.sha(json.dumps(paired[1]["writes"]).encode()),
                "nativeWriteCount": len(observed["writes"]),
                "draftWriteCount": len(paired[1]["writes"]),
                "writeDifferences": write_differences,
                "inputSha256": audit.sha(state + arena + struct.pack("<3I", start, destination, length)),
                "permutationState": len(set(state[12:])) == 256,
            })
        results.append({
            "address": hex(address), "mode": "ARM", "processor": "ARM9", "module": 4,
            "source": str(source.relative_to(ROOT)), "sourceSha256": audit.sha(source.read_bytes()),
            "compileReport": str(report_path.relative_to(ROOT)),
            "nativeBytes": function["bytes"], "matchingBytes": function["matchingBytes"],
            "functionMatched": function["exactAfterDeclaredRelocation"],
            "acceptedSourceBytes": 0, "vectors": vectors,
        })
    result = {
        "schema": 1, "independentBehaviorPassed": True,
        "fullMachineEffectsEqual": all(
            vector["fullMachineEffectsEqual"] for entry in results for vector in entry["vectors"]
        ),
        "evidenceClass": "unaccepted-behavioral-draft",
        "romSha256": audit.ROM_HASH, "analysisSha256": audit.sha(data["analysis"]),
        "driverSha256": audit.sha(Path(__file__).read_bytes()),
        "independentModel": "Instruction categories, mutable overlapping input/output arena, full 268-byte stream state, 32-bit feedback arithmetic",
        "nativeCallees": ["0x021d7de8", "0x021d8a70", "0x021d8ac8"],
        "pythonVersion": sys.version, "unicornVersion": unicorn_version,
        "executions": sum(len(entry["vectors"]) * 2 for entry in results),
        "instructionLimitPerExecution": 100000,
        "comparison": "Return, complete state/arena and R0-R15/CPSR must agree; differences in full64KiB stack, ordered value-bearing writes, instruction count and executed addresses are retained as unaccepted evidence",
        "limitations": "No matching-byte acceptance or linker claim. Aligned valid arena/state pointers; zero lengths and selected rejected odd lengths also use poisoned pointers. No hardware, exception, interrupt, unaligned-pointer, or source/state alias coverage. Frozen compiler behavior of signed arithmetic is measured; portable C overflow semantics are not asserted. Nested native helper spills can expose the draft's nonmatching register allocation in the private scratch stack.",
        "results": results,
    }
    path = OUT / ("behavior-" + audit.sha(json.dumps(result, sort_keys=True).encode()) + ".json")
    matcher.immutable(path, json.dumps(result, indent=2).encode())
    print(json.dumps({"independentBehaviorPassed": True, "fullMachineEffectsEqual": result["fullMachineEffectsEqual"], "executions": result["executions"], "report": str(path.relative_to(ROOT))}))


if __name__ == "__main__":
    run()
