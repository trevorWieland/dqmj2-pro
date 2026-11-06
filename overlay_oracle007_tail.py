import struct
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2

FUNCTIONS = {0x021D8EE8, 0x021D8FBC, 0x021D9424, 0x021D9770}


def word(engine, address):
    return int.from_bytes(engine.mem_read(address, 4), "little")


def string(engine, address):
    return bytes(engine.mem_read(address, 64)).split(b"\0", 1)[0]


def seed_tail(engine, address, vector):
    if address not in FUNCTIONS:
        return {}
    if address == 0x021D9770:
        phase = [-128, -1, *range(11), 127][vector % 14]
        number = 8 if phase == 9 else phase + 1
        engine.mem_write(0x021DA924, bytes([phase & 255]))
        names = [string(engine, target).decode() % number for target in [0x021DA928, 0x021DA944, 0x021DA960]]
        return {"names": names, "bank": 0x0300C000 if (vector // 14) % 2 else 0, "formatted": []}
    fields = [91 | (177 << 8), 0x03007000, 0x03008000, 0x03009000, 0x0300A000, 0x0300C000, 0x0300B000, 0, 0x0300D000, 0, 0x0300E000, 0]
    if address == 0x021D9424:
        for index, slot in enumerate([3, 2, 6, 10, 5]):
            if not vector & 1 << index:
                fields[slot] = 0
    engine.mem_write(0x021DA9DC, struct.pack("<12I", *fields))
    flags = {}
    for slot, count in [(1, 1), (3, 16), (6, 3), (10, 1)]:
        for index in range(count if fields[slot] else 0):
            pointer = fields[slot] + index * 144
            value = (word(engine, pointer + 124) & ~2) | (((vector + index) % 2) << 1)
            engine.mem_write(pointer + 124, struct.pack("<I", value))
            flags[pointer] = value
    release = {slot: [bytes(engine.mem_read(fields[slot] + index * 144 + 129, 1))[0] for index in range(count)] for slot, count in [(3, 16), (2, 1), (6, 3), (10, 1)] if fields[slot]}
    return {"fields": fields, "flags": flags, "release": release}


def tail_arguments(address, vector, args):
    if address == 0x021D8FBC:
        args[0] = [0, 1, 2, 255, 256, 0xFFFFFFFF][vector % 6]


def tail_call(engine, address, name, value, state):
    if not state or address != 0x021D9770:
        return value
    first, second = engine.reg_read(UC_ARM_REG_R0), engine.reg_read(UC_ARM_REG_R1)
    if name == "func_0201d444":
        number = engine.reg_read(UC_ARM_REG_R2)
        number = number if number < 0x80000000 else number - 0x100000000
        formatted = (string(engine, second).decode() % number).encode()
        if len(formatted) >= 32:
            raise ValueError("Formatted resource path exceeds its bounded buffer")
        engine.mem_write(first, formatted + b"\0")
        state["formatted"].append(formatted.decode())
        return len(formatted)
    if name == "func_0203cc2c":
        if string(engine, first).decode() != state["names"][0]:
            raise ValueError("Formatted bank resource name differs")
        return state["bank"]
    if name in {"func_02040d18", "func_02040d5c"}:
        resource = string(engine, second).decode()
        if resource not in state["names"][1:]:
            raise ValueError("Formatted child resource name differs")
        return (0x0300D000 if resource == state["names"][1] else 0x0300E000) if name == "func_02040d18" else (64 if resource == state["names"][1] else 32)
    return value


def assert_tail(engine, address, args, calls, state):
    if not state:
        return
    if address == 0x021D9770:
        expected = ["func_0201d444"] * 3 + ["func_0203cc2c"]
        if state["bank"]:
            expected += ["func_02040d18", "func_02040d5c"] * 2 + ["func_02045a60", "func_02045490"]
            transfers = [call["args"] for call in calls if call["name"] in {"func_02045a60", "func_02045490"}]
            if transfers != [[1, 0x0300E000, 0, 32], [1, 0x0300D000, 0, 64]]:
                raise ValueError("Formatted graphics/palette transfer differs")
        expected += ["func_0202a498"]
        if [call["name"] for call in calls] != expected or state["formatted"] != state["names"] or calls[-1]["args"][:2] != [5, state["bank"]]:
            raise ValueError("Formatted resource lifecycle differs")
        return
    fields = state["fields"]
    if address == 0x021D8EE8:
        for index, coordinates in enumerate([(128, 40), (90, 60), (110, 50)]):
            pointer = fields[6] + index * 144
            if word(engine, pointer + 124) != state["flags"][pointer] & ~2 or bytes(engine.mem_read(pointer + 120, 2)) != b"\2\0" or bytes(engine.mem_read(pointer + 108, 8)) != struct.pack("<2I", *coordinates):
                raise ValueError("Three-row coordinate/disable/byte state differs")
        if len(calls) != 15:
            raise ValueError("Three-row setup call count differs")
    if address == 0x021D8FBC:
        slot = 10 if args[0] else 1
        pointer = fields[slot]
        mode = next(call for call in calls if call["name"] == "func_02048644")
        if mode["args"][:3] != [pointer, fields[4 if args[0] else 8], 18] or calls[0]["args"][:2] != [args[0] & 255, pointer]:
            raise ValueError("Secondary manager selection/truncation differs")
        expected_flags = (state["flags"][pointer] & ~2) | 12
        if word(engine, pointer + 124) != expected_flags or bytes(engine.mem_read(pointer + 120, 2)) != b"\1\0":
            raise ValueError("Secondary manager native flag/byte writer differs")
    if address == 0x021D9424:
        expected = []
        for slot in [3, 2, 6, 10]:
            if fields[slot]:
                expected += [("func_0204861c", [1, byte]) for byte in state["release"][slot]]
                expected += [("func_0202a51c", [fields[slot]])]
        if fields[5]:
            expected += [("func_020485b4", [fields[5]])]
        expected += [("func_020484dc", [1, 177])]
        if len(calls) != len(expected) or any(call["name"] != name or call["args"][:len(values)] != values for call, (name, values) in zip(calls, expected)):
            raise ValueError("Full manager release rows/order differs")
