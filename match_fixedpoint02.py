import random
import struct
import match_runtime as compiler
from match_fixedpoint import signed
from project import ROOT, configuration, now, sha256, verify_inputs, write_json


def expected(data, address, source, destination, factors):
    result = bytearray(data)

    def read(pointer, index):
        return struct.unpack_from("<i", result, pointer - 0x03000000 + index * 4)[0]

    def write(pointer, index, value):
        struct.pack_into("<I", result, pointer - 0x03000000 + index * 4, value & 0xFFFFFFFF)

    if address == 0x020019B0:
        if source != destination:
            for group in range(0, 12, 3):
                values = [read(source, group + i) for i in range(3)]
                for index, value in enumerate(values):
                    write(destination, group + index, value)
        for column in range(4):
            total = sum(factors[row] * read(source, row * 4 + column) for row in range(3))
            write(destination, column + 12, read(source, column + 12) + (signed(total, 64) >> 12))
    else:
        for index in range(12):
            write(destination, index, (factors[index // 4] * read(source, index)) >> 12)
        if source != destination:
            for group in (12, 14):
                values = [read(source, group + i) for i in range(2)]
                for index, value in enumerate(values):
                    write(destination, group + index, value)
    return bytes(result)


def execute(entry, code, binary, data, source, destination, factors, registers):
    from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
    from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
    address = int(entry["address"], 0)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    engine.mem_map(0x02000000, 0x100000)
    engine.mem_map(0x03000000, 0x20000)
    engine.mem_map(0x04000000, 0x1000)
    engine.mem_write(0x02000000, binary)
    engine.mem_write(address, code)
    engine.mem_write(0x03000000, data)
    for index, value in enumerate([source, destination, factors[0], factors[1]]):
        engine.reg_write(UC_ARM_REG_R0 + index, value & 0xFFFFFFFF)
    for index, value in enumerate(registers[1:]):
        engine.reg_write(UC_ARM_REG_R4 + index, value)
    engine.reg_write(UC_ARM_REG_CPSR, registers[0] << 28 | 0x10)
    engine.reg_write(UC_ARM_REG_SP, 0x0301FF80)
    engine.mem_write(0x0301FF80, struct.pack("<I", factors[2] & 0xFFFFFFFF))
    engine.reg_write(UC_ARM_REG_LR, 0x04000000)
    calls = []

    def instruction(machine, pc, size, unused):
        if not (address <= pc < address + entry["bytes"] or address == 0x020019B0 and 0x02008D28 <= pc < 0x02008D4C):
            raise ValueError("Fixed-point execution escaped measured routine/dependency")
        if pc == 0x02008D28:
            calls.append(pc)

    engine.hook_add(UC_HOOK_CODE, instruction)
    engine.emu_start(address, 0x04000000, timeout=2000000, count=5000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x04000000 or engine.reg_read(UC_ARM_REG_SP) != 0x0301FF80:
        raise ValueError("Fixed-point routine did not return normally")
    if any(engine.reg_read(UC_ARM_REG_R4 + index) != value for index, value in enumerate(registers[1:])):
        raise ValueError("Fixed-point routine did not preserve ABI registers")
    if calls != ([0x02008D28] if address == 0x020019B0 and source != destination else []):
        raise ValueError("Fixed-point copy dependency path differs")
    return bytes(engine.mem_read(0x03000000, len(data))), [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)], engine.reg_read(UC_ARM_REG_CPSR), calls


def oracle(entry, rebuilt, binary):
    address = int(entry["address"], 0)
    rng = random.Random(2026102702 + address)
    hashes = []
    native = binary[address - 0x02000000:address - 0x02000000 + entry["bytes"]]
    for vector in range(600):
        data = rng.randbytes(0x4000)
        source = 0x03000100
        destination = [0x03002000, source, source + 4, source - 4, source + 12, source + 48][vector % 6]
        factors = [signed(rng.getrandbits(32)) for _ in range(3)]
        if vector < 18:
            factors = [[0, 1, -1], [4096, -4096, 2048], [0x7FFFFFFF, -0x80000000, -1]][vector % 3]
        registers = [rng.randrange(16)] + [rng.getrandbits(32) for _ in range(8)]
        before = execute(entry, native, binary, data, source, destination, factors, registers)
        after = execute(entry, rebuilt, binary, data, source, destination, factors, registers)
        if before != after or before[0] != expected(data, address, source, destination, factors):
            raise ValueError(f"Fixed-point expected behavior differs at {address:#x}, vector {vector}")
        hashes.append(compiler.sha(before[0]))
    return {"cases": len(hashes), "nativeAndRecompiledCalls": len(hashes) * 2, "independentExpectedBytes": True, "isolatedMachinePerCall": True, "aliasingPatterns": 6, "boundedInstructions": 5000, "verifiedReturn": True, "memorySha256": hashes, "nativeCopyDependency": "main/arm/02008d28" if address == 0x020019B0 else None, "copyDependencyReconstructed": False}


if __name__ == "__main__":
    config = configuration()
    inputs = verify_inputs(config)
    binary = (ROOT / "extract/arm9/arm9.bin").read_bytes()
    matches = []
    attempts = []
    for path in ("src/runtime/fixedpoint02.c", "src/runtime/fixedpoint_scale4.c"):
        records, compiled = compiler.compare(ROOT / path, "main", 2, "off", False)
        attempts.extend(records)
        if len(compiled) != 1:
            raise ValueError("A fixed-point function stopped matching: " + path)
        entry, code = next(iter(compiled.values()))
        entry["oracle"] = oracle(entry, code, binary)
        matches.append(entry)
    report = {"schemaVersion": 1, "createdUtc": now(), "romSha256": inputs["rom"]["sha256"], "module": "main", "matches": matches, "attempts": attempts, "nativeSymbols": {rel["symbol"]: rel["target"] for item in matches for rel in item["relocations"]}, "sourceReconstructionComplete": False, "limitations": ["Arithmetic and access ordering are measured; game-level identities remain unknown", "Native 48-byte copy dependency remains original executable scaffolding", "Target 32/64-bit wrapping and overlapping buffer effects are covered by deterministic expected bytes"]}
    write_json(ROOT / "evidence/matches/main-fixedpoint02.json", report)
    if inputs != verify_inputs(config):
        raise ValueError("Inputs changed")
    print({"functions": len(matches), "bytes": sum(item["bytes"] for item in matches), "independentCases": 1200, "nativeAndRecompiledCalls": 2400})
