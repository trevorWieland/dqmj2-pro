import hashlib
import json
import random
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "deps/native"))
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_R12,
    UC_ARM_REG_SP,
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_CPSR,
)

BASE = 0x021D7240
HEAD = 0x021E78C0
FUNCTIONS = {0x021D7338, 0x021D738C}
REGS = [
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_R12,
    UC_ARM_REG_SP,
    UC_ARM_REG_LR,
]
INSERT = [
    (length, index, fill)
    for length in range(9)
    for index in range(length + 1)
    for fill in [0, 1, 0x80000000, 0xFFFFFFFF]
]
LOOKUP = [(length, query, alias) for length in range(9) for query in range(length + 3) for alias in [0, 1]]
NAMES = [b"", b"a", b"ab", b"a\x80", b"a\xff", b"x" * 15, b"ab", b"last"]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def machine(patches=None):
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for at, size in [(0x02000000, 0x400000), (0x03000000, 0x20000), (0x04000000, 0x1000)]:
        engine.mem_map(at, size)
    engine.mem_write(0x02000000, (ROOT / "extract/arm9/arm9.bin").read_bytes())
    engine.mem_write(BASE, (ROOT / "extract/arm9_overlays/ov005.bin").read_bytes())
    for at, data in (patches or {}).items():
        engine.mem_write(at, data)
    return engine


def vector_run(address, code, vector):
    engine = machine({address: code})
    rng = random.Random(20261028005 + address + vector)
    nodes = [0x03002000 + i * 64 for i in range(8)]
    new = 0x03003000
    allNodes = nodes + [new]
    before = {}
    for i, node in enumerate(allNodes):
        data = bytearray(rng.randbytes(44))
        struct.pack_into("<I", data, 0, 0x03005000 + i * 32)
        engine.mem_write(node, bytes(data))
        if i < 8:
            engine.mem_write(0x03005000 + i * 32, NAMES[i] + b"\x00")
    if address == 0x021D7338:
        length, index, fill = INSERT[vector]
        candidate = nodes[index] if index < length else new
        query = None
        engine.mem_write(new + 40, struct.pack("<I", fill))
        args = [candidate, rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32)]
    else:
        length, index, alias = LOOKUP[vector]
        query = NAMES[index] if index < length else [b"missing", b"a", b"x" * 14][index - length]
        pointer = 0x03005000 + index * 32 if alias and index < length else 0x03004000
        engine.mem_write(0x03004000, query + b"\x00")
        args = [pointer, rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32)]
    for i, node in enumerate(nodes[:length]):
        engine.mem_write(node + 40, struct.pack("<I", nodes[i + 1] if i + 1 < length else 0))
    engine.mem_write(HEAD, struct.pack("<I", nodes[0] if length else 0))
    headBefore = bytes(engine.mem_read(HEAD, 4))
    before = {p: bytes(engine.mem_read(p, 44)) for p in allNodes}
    strings = bytes(engine.mem_read(0x03004000, 0x1400))
    stack = rng.randbytes(256)
    engine.mem_write(0x0301FF00, stack)
    registers = args + [rng.getrandbits(32) for i in range(9)] + [0x0301FFF0, 0x04000000]
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for reg, value in zip(REGS, registers):
        engine.reg_write(reg, value)
    writes = []
    calls = []
    engine.hook_add(
        UC_HOOK_MEM_WRITE,
        lambda uc, access, at, width, value, user: writes.append([at, width, value & ((1 << (width * 8)) - 1)]),
    )

    def call(uc, at, width, user):
        if at == 0x02019DA8:
            calls.append([uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)])

    engine.hook_add(UC_HOOK_CODE, call)
    engine.emu_start(address, 0x04000000, count=4096)
    if engine.reg_read(UC_ARM_REG_PC) != 0x04000000:
        raise ValueError("Registry operation did not return in bound")
    expected = {p: bytearray(data) for p, data in before.items()}
    head = bytearray(headBefore)
    dataWrites = []
    if address == 0x021D7338:
        if candidate not in nodes[:length]:
            target = HEAD if not length else nodes[length - 1] + 40
            dataWrites = [[target, 4, candidate], [candidate + 40, 4, 0]]
            if length:
                struct.pack_into("<I", expected[nodes[length - 1]], 40, candidate)
            else:
                head[:] = struct.pack("<I", candidate)
            struct.pack_into("<I", expected[candidate], 40, 0)
        if writes != dataWrites or calls:
            raise ValueError("Registry duplicate suppression/append ordered writes differ")
    else:
        found = next((i for i in range(length) if NAMES[i] == query), None)
        result = nodes[found] if found is not None else 0
        visited = range(found + 1) if found is not None else range(length)
        wanted = [[args[0], 0x03005000 + i * 32] for i in visited]
        if (
            calls != wanted
            or engine.reg_read(UC_ARM_REG_R0) != result
            or any(at < 0x0301FF00 for at, width, value in writes)
        ):
            raise ValueError("Registry lookup string identity/order/first-match result differs")
    if (
        bytes(engine.mem_read(HEAD, 4)) != bytes(head)
        or any(bytes(engine.mem_read(p, 44)) != bytes(data) for p, data in expected.items())
        or bytes(engine.mem_read(0x03004000, 0x1400)) != strings
    ):
        raise ValueError("Registry complete node prefixes/links/strings/head effects differ")
    return {
        "registers": [engine.reg_read(r) for r in REGS],
        "cpsr": engine.reg_read(UC_ARM_REG_CPSR),
        "writes": writes,
        "stringCalls": calls,
        "nodeStateSha256": sha(bytes(head) + b"".join(bytes(engine.mem_read(p, 44)) for p in allNodes)),
        "stackSha256": sha(bytes(engine.mem_read(0x0301FF00, 256))),
    }


def connected_constructors(registryCode):
    import reuse_overlay_c as reuse

    report = json.loads((ROOT / "evidence/matches/ov005-reuse01.json").read_text())
    ctorAddresses = [0x021D98A0, 0x021D98B4, 0x021DA1A0]
    patches = {0x021D7338: registryCode}
    sources = []
    for address in ctorAddresses:
        old = next(e for e in report["matches"] if int(e["address"], 0) == address)
        spec = {"name": old["name"], "module": "ov005", "mode": "arm"}
        rows, result = reuse.compile_entry(ROOT / old["source"], spec, old)
        if result is None or result[0]["targetSha256"] != old["targetSha256"]:
            raise ValueError("Frozen constructor source stopped matching")
        patches[address] = result[1]
        sources.append({k: old[k] for k in ["source", "sourceSha256", "address", "bytes", "compilerSha256"]})
    snapshots = []
    for replacements in [{}, patches]:
        engine = machine(replacements)
        objects = [0x021E6FE8, 0x021E7018, 0x021E7060]
        prefixes = {p: bytes(engine.mem_read(p, 40)) for p in objects}
        engine.mem_write(HEAD, bytes(4))
        writes = []
        engine.hook_add(
            UC_HOOK_MEM_WRITE, lambda uc, access, at, width, value, user: writes.append([at, width, value & 0xFFFFFFFF])
        )
        states = []
        sequence = ctorAddresses + ctorAddresses + list(reversed(ctorAddresses))
        for i, address in enumerate(sequence):
            engine.reg_write(UC_ARM_REG_CPSR, 0x10)
            engine.reg_write(UC_ARM_REG_SP, 0x0301FFF0)
            engine.reg_write(UC_ARM_REG_LR, 0x04000000)
            first = len(writes)
            engine.emu_start(address, 0x04000000, count=4096)
            if engine.reg_read(UC_ARM_REG_PC) != 0x04000000:
                raise ValueError("Connected compiled constructor did not return")
            expectedWrites = (
                [[HEAD if i == 0 else objects[i - 1] + 40, 4, objects[i]], [objects[i] + 40, 4, 0]] if i < 3 else []
            )
            if writes[first:] != expectedWrites or any(bytes(engine.mem_read(p, 40)) != prefixes[p] for p in objects):
                raise ValueError("Connected constructor registration duplicate/list effects differ")
            states.append(
                {"entry": hex(address), "writes": writes[first:], "registers": [engine.reg_read(r) for r in REGS]}
            )
        if int.from_bytes(engine.mem_read(HEAD, 4), "little") != objects[0] or [
            int.from_bytes(engine.mem_read(p + 40, 4), "little") for p in objects
        ] != objects[1:] + [0]:
            raise ValueError("Connected constructor final registry chain differs")
        snapshots.append(states)
    if snapshots[0] != snapshots[1]:
        raise ValueError("Native/compiled constructor-plus-registry effects differ")
    return {
        "passed": True,
        "callsPerExecution": 9,
        "nativeAndCompiledCalls": 18,
        "sourceDependencies": sources,
        "stateSha256": sha(json.dumps(snapshots[0], sort_keys=True).encode()),
        "nativeCalleesSubstituted": False,
        "registryBodyRecompiled": True,
    }


def oracle(entry, code):
    address = int(entry["address"], 16)
    if address not in FUNCTIONS:
        raise ValueError("Unknown module005 registry operation")
    overlay = (ROOT / "extract/arm9_overlays/ov005.bin").read_bytes()
    native = overlay[address - BASE : address - BASE + entry["bytes"]]
    count = len(INSERT) if address == 0x021D7338 else len(LOOKUP)
    vectors = []
    for vector in range(count):
        first = vector_run(address, native, vector)
        second = vector_run(address, code, vector)
        if first != second:
            raise ValueError("Module005 native/compiled registry state differs")
        vectors.append({"index": vector, "stateSha256": sha(json.dumps(first, sort_keys=True).encode())})
    result = {
        "passed": True,
        "vectors": count,
        "executions": count * 2,
        "instructionLimit": 4096,
        "moduleInputSha256": sha(overlay),
        "results": vectors,
        "independentChecks": [
            "Complete44-byte node records and prefix preservation",
            "Registry head/link mutations and ordered writes",
            "Duplicate insertion is idempotent",
            "First exact string match and callback argument order",
            "Empty lists, prefix strings, signed high bytes and aliased name pointers",
        ],
        "limitations": [
            "Only finite acyclic lists of zero through eight valid non-null nodes are exercised. Cyclic lists, invalid pointers and full platform overlay lifetimes remain outside this bounded contract."
        ],
    }
    if address == 0x021D7338:
        result["connectedConstructors"] = connected_constructors(code)
    else:
        main = (ROOT / "extract/arm9/arm9.bin").read_bytes()
        result["executedNativeHelpers"] = [
            {
                "module": "main",
                "name": "func_02019da8",
                "address": "0x02019da8",
                "bytes": 44,
                "sha256": sha(main[0x19DA8:0x19DD4]),
            }
        ]
    return result
