import struct
from unicorn.arm_const import UC_ARM_REG_R0

FUNCTIONS = {0x021D8CC8, 0x021D8D48, 0x021D8DB8, 0x021D8E4C, 0x021D9158, 0x021D91F4, 0x021D929C, 0x021D932C}


def word(engine, address):
    return int.from_bytes(engine.mem_read(address, 4), "little")


def seed_tables(engine, address, vector):
    if address not in FUNCTIONS:
        return {}
    fields = [91, 0x03007000, 0x03008000, 0x03009000, 0x0300A000, 0, 0, 0x0300B000, 0, 0x0300C000, 0x0300D000, 0]
    if address == 0x021D8CC8:
        for index, slot in enumerate([7, 1, 9]):
            if not vector & (1 << index):
                fields[slot] = 0
    engine.mem_write(0x021DA9DC, struct.pack("<12I", *fields))
    flags = []
    for index in range(16):
        pointer = fields[3] + index * 144
        flags.append((word(engine, pointer + 124) & ~2) | (((index + vector) % 2) << 1))
        engine.mem_write(pointer + 124, struct.pack("<I", flags[-1]))
    choice = [value & 0xFFFFFFFF for value in [vector - 4, 4 - vector, vector % 16, 15 - vector % 16]]
    engine.mem_write(0x021DA0F4, struct.pack("<4I", *choice))
    return {"fields": fields, "flags": flags, "choice": choice, "vector": vector, "objectFlags": word(engine, fields[2] + 124), "releaseBytes": {slot: bytes(engine.mem_read(fields[slot] + 129, 1))[0] for slot in [7, 1] if fields[slot]}}


def table_arguments(address, vector, args):
    if address == 0x021D932C:
        args[0] = vector % 16


def table_call(engine, address, name, value, state):
    if not state:
        return value
    index = engine.reg_read(UC_ARM_REG_R0)
    if name in {"func_ov007_021d8634", "func_ov007_021d864c"}:
        return ((100 if name == "func_ov007_021d8634" else 200) + index) & 0xFFFFFFFF
    if name == "func_ov007_021d873c":
        return (index + state["vector"]) % 2
    if name == "func_ov007_021d8664":
        return (index + state["vector"]) % 4
    if name == "func_ov007_021d8828":
        return (index // 4 + state["vector"]) % 2
    if name == "func_020c20e4":
        return (index // 8 + state["vector"]) % 2
    if address == 0x021D932C and name == "func_02048644":
        engine.mem_write(index + 124, struct.pack("<I", word(engine, index + 124) ^ 2))
    return value


def assert_tables(engine, address, args, calls, state):
    if not state:
        return
    fields, vector = state["fields"], state["vector"]
    if address == 0x021D8CC8:
        expected = []
        for slot, released in [(7, 7), (1, 10)]:
            if fields[slot]:
                expected += [("func_0204861c", [0, state["releaseBytes"][slot]]), ("func_0202a51c", [fields[released]])]
        if fields[9]:
            expected += [("func_020485b4", [fields[9]])]
        expected += [("func_020484dc", [0, 91])]
        if len(calls) != len(expected) or any(call["name"] != name or call["args"][:len(values)] != values for call, (name, values) in zip(calls, expected)):
            raise ValueError("Conditional manager release order/alias differs")
    if address == 0x021D8DB8:
        if len(calls) != 98 or [call["name"] for call in calls[-2:]] != ["func_ov007_021d91f4", "func_ov007_021d8d48"]:
            raise ValueError("Sixteen-row manager setup call count differs")
        for index in range(16):
            pointer = fields[3] + index * 144
            if bytes(engine.mem_read(pointer + 108, 8)) != struct.pack("<2I", 96 + index, 196 + index) or bytes(engine.mem_read(pointer + 120, 2)) != b"\0\0":
                raise ValueError("Executed row coordinate/byte writers differ")
    if address in {0x021D8E4C, 0x021D9158}:
        expected = struct.pack("<2I", (state["choice"][0] - 4) & 0xFFFFFFFF, (state["choice"][1] - 4) & 0xFFFFFFFF)
        if bytes(engine.mem_read(fields[2] + 108, 8)) != expected:
            raise ValueError("Executed struct-return coordinate adaptation differs")
        if address == 0x021D8E4C and (word(engine, fields[2] + 124) != state["objectFlags"] | 2 or bytes(engine.mem_read(fields[2] + 120, 2)) != b"\0\0"):
            raise ValueError("Selected object enable/byte state differs")
        if address == 0x021D9158 and word(engine, 0x0210276C) != 1:
            raise ValueError("Selection setup did not store the main-module flag")
    if address in {0x021D91F4, 0x021D929C}:
        expected = []
        for index in range(16):
            if address == 0x021D929C and (index + vector) % 2 == 0:
                continue
            kind = (index + vector) % 4
            mode = 15
            if address == 0x021D929C:
                mode = {0: 16, 1: 15, 2: 17}.get(kind, 15)
            elif kind == 0:
                mode = 2
            elif kind == 1:
                mode = (21 if (index // 8 + vector) % 2 else 1) if (index // 4 + vector) % 2 else 13
            elif kind == 2:
                mode = 3
            expected.append([fields[3] + index * 144, fields[4], mode])
        actual = [call["args"][:3] for call in calls if call["name"] == "func_02048644"]
        if actual != expected:
            raise ValueError("Sixteen-row conditional mode mapping differs")
    if address == 0x021D932C:
        pointer = fields[3] + args[0] * 144
        if len(calls) != 1 or calls[0]["args"][:3] != [pointer, fields[4], args[1]] or word(engine, pointer + 124) != state["flags"][args[0]]:
            raise ValueError("Row mode update did not preserve its original enabled bit")
