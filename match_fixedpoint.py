import random
import struct
import match_runtime as compiler
from project import ROOT, configuration, now, sha256, verify_inputs, write_json


def signed(value, bits=32):
    value &= (1 << bits) - 1
    return value - (1 << bits) if value >> (bits - 1) else value


def expected(data, address, source, matrix, destination, factors):
    result = bytearray(data)
    def read(pointer, index):
        return struct.unpack_from("<i", result, pointer - 0x03000000 + index * 4)[0]
    def write(pointer, index, value):
        struct.pack_into("<I", result, pointer - 0x03000000 + index * 4, value & 0xFFFFFFFF)
    if address == 0x02000D0C:
        for index in range(9):
            write(destination, index, (read(source, index) * factors[index // 3]) >> 12)
    else:
        vector = [read(source, index) for index in range(3)]
        for column in range(3):
            total = sum(vector[row] * read(matrix, row * 3 + column) for row in range(3))
            write(destination, column, signed(total, 64) >> 12)
            if address == 0x020017A8:
                write(destination, column, read(destination, column) + read(matrix, column + 9))
    return bytes(result)


def execute(code, address, data, args, fifth, initial):
    from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
    from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    engine.mem_map(0x02000000, 0x100000)
    engine.mem_map(0x03000000, 0x20000)
    engine.mem_map(0x04000000, 0x1000)
    engine.mem_write(address, code)
    engine.mem_write(0x03000000, data)
    engine.reg_write(UC_ARM_REG_CPSR, initial[0] << 28 | 0x10)
    for index, value in enumerate(args):
        engine.reg_write(UC_ARM_REG_R0 + index, value & 0xFFFFFFFF)
    for index in range(8):
        engine.reg_write(UC_ARM_REG_R4 + index, initial[index + 1])
    engine.reg_write(UC_ARM_REG_SP, 0x0301FF80)
    engine.mem_write(0x0301FF80, struct.pack("<I", fifth & 0xFFFFFFFF))
    engine.reg_write(UC_ARM_REG_LR, 0x04000000)
    engine.emu_start(address, 0x04000000, count=1000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x04000000 or engine.reg_read(UC_ARM_REG_SP) != 0x0301FF80:
        raise ValueError("Fixed-point routine did not return normally")
    if any(engine.reg_read(UC_ARM_REG_R4 + i) != initial[i + 1] for i in range(8)):
        raise ValueError("Fixed-point routine did not preserve its ABI registers")
    return bytes(engine.mem_read(0x03000000, len(data))), [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)], engine.reg_read(UC_ARM_REG_CPSR)


def oracle(entry, rebuilt, native):
    address = int(entry["address"], 0)
    rng = random.Random(20261027 + address)
    results = []
    for vector in range(120):
        data = rng.randbytes(0x4000)
        source, matrix = 0x03000080, 0x03001000
        destination = [0x03002000, source, source + 4, matrix, matrix + 36][vector % 5]
        factors = [signed(rng.getrandbits(32)) for _ in range(3)]
        if vector < 10:
            factors = [[0, 1, -1], [4096, -4096, 2048], [0x7FFFFFFF, -0x80000000, -1]][vector % 3]
        args = [source, destination, factors[0], factors[1]] if address == 0x02000D0C else [source, matrix, destination, 0]
        initial = [rng.randrange(16)] + [rng.getrandbits(32) for _ in range(8)]
        before = execute(native, address, data, args, factors[2], initial)
        after = execute(rebuilt, address, data, args, factors[2], initial)
        if before != after or before[0] != expected(data, address, source, matrix, destination, factors):
            raise ValueError(f"Independent fixed-point mismatch at {address:#x} vector{vector}")
        results.append(compiler.sha(before[0]))
    return {"cases": len(results), "nativeAndRecompiledCalls": len(results) * 2, "independentExpectedBytes": True, "aliasingPatterns": 5, "boundedInstructions": 1000, "verifiedReturn": True, "memorySha256": results}


if __name__ == "__main__":
    config = configuration()
    inputs = verify_inputs(config)
    source = ROOT / "src/runtime/fixedpoint01.c"
    matches, attempts = {}, []
    for optimization, inline, speed in [(2, "off", False), (2, "off", True), (3, "off", False), (4, "off", False)]:
        records, compiled = compiler.compare(source, "main", optimization, inline, speed)
        attempts.extend(records)
        for name, pair in compiled.items():
            matches.setdefault(name, pair)
    native = (ROOT / "extract/arm9/arm9.bin").read_bytes()
    for record, code in matches.values():
        offset = int(record["address"], 0) - 0x02000000
        record["oracle"] = oracle(record, code, native[offset:offset + record["bytes"]])
    if len(matches) != 3:
        raise ValueError("A fixed-point function stopped matching")
    report = {"schemaVersion": 1, "createdUtc": now(), "romSha256": inputs["rom"]["sha256"], "module": "main", "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha256(source), "matches": [record for record, _ in matches.values()], "attempts": attempts, "nativeSymbols": {}, "sourceReconstructionComplete": False, "limitations": ["Names describe measured arithmetic, not game-level identities", "Target compiler arithmetic is validated against native 32/64-bit wrap behavior"]}
    write_json(ROOT / "evidence/matches/main-fixedpoint01.json", report)
    if inputs != verify_inputs(config):
        raise ValueError("Inputs changed")
    print({"functions": len(matches), "bytes": sum(r["bytes"] for r, _ in matches.values()), "independentCases": 360, "nativeAndCompiledCalls": 720})
