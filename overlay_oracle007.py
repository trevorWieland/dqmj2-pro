import struct

from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2

MODES = [*range(19), 19, 0xFFFFFFFF]
MODE_RESULTS = {0: 170, 16: 170, 2: 172, 3: 173, 4: 174, 5: 175, 7: 177, 8: 178, 9: 179, 10: 180, 18: 558}
SCALARS = {0x021D85FC, 0x021D860C, 0x021D8624, 0x021D876C, 0x021D8828, 0x021D9628, 0x021D963C, 0x021D9654, 0x021D966C, 0x021D9714, 0x021D9728, 0x021D9760, 0x021D9CAC, 0x021DA04C}


def seed_scalar(engine, address, vector):
    if address not in SCALARS:
        return {}
    state = {"mode": MODES[vector % len(MODES)], "choice": [0, 1, 14, 15][vector % 4], "handle": 0x0300C000 + (vector % 4) * 256, "character": [65, 66, 90, 255][vector % 4], "ready": vector % 2, "code": [0, 128, 129, 140, 0xFFFFFFFF][vector % 5], "flag": [255, 0, 1, 128, 127][vector % 5]}
    if address in {0x021D85FC, 0x021D860C}:
        engine.mem_write(0x021DA0FC, struct.pack("<I", state["choice"]))
    if address == 0x021D9654:
        engine.mem_write(0x021DAA0C, struct.pack("<I", state["handle"]))
    if address == 0x021D9728:
        engine.mem_write(0x021DAA14, struct.pack("<I", state["code"]))
    if address == 0x021D9CAC:
        engine.mem_write(0x021DA924, bytes([state["flag"]]))
    if address == 0x021DA04C:
        state["pair"] = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (-2147483648, 2147483647), (2147483647, -2147483648)][vector % 7]
        engine.mem_write(0x021DB2CC, struct.pack("<2i", *state["pair"]))
    return state


def scalar_arguments(address, vector, args):
    if address in {0x021D8624, 0x021D9760}:
        args[0] = [0, 1, 255, 256, 65535, 0xFFFFFFFF][vector % 6]


def scalar_call(engine, address, name, value, state):
    if not state:
        return value
    if address == 0x021D876C and name == "func_020726d8":
        return state["mode"]
    if address == 0x021D8828 and name == "func_ov007_021d876c":
        return MODE_RESULTS.get(state["mode"], 0)
    if address == 0x021D963C and name == "func_0205f5dc":
        return state["handle"]
    if address == 0x021D966C and name == "func_0203cfe8":
        return state["character"]
    if address == 0x021D966C and name == "func_0201d444":
        template = bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_R1), 12)).split(b"\0", 1)[0]
        state["name"] = template.replace(b"%c", bytes([engine.reg_read(UC_ARM_REG_R2) & 255])) + b"\0"
        engine.mem_write(engine.reg_read(UC_ARM_REG_R0), state["name"])
        return len(state["name"]) - 1
    if address == 0x021D9714 and name == "func_0204bd6c" or address == 0x021D9728 and name == "func_ov007_021d9714":
        return state["ready"]
    return value


def assert_scalar(engine, address, args, calls, state):
    if not state:
        return
    result = engine.reg_read(UC_ARM_REG_R0)
    if address == 0x021D85FC and result != state["choice"]:
        raise ValueError("Choice scalar extraction differs")
    if address == 0x021D860C:
        if len(calls) != 1 or calls[0]["args"][0] != state["choice"]:
            raise ValueError("Choice forwarding differs")
    if address in {0x021D8624, 0x021D9760}:
        target = 0x021DA9B8 if address == 0x021D8624 else 0x021DA924
        if bytes(engine.mem_read(target, 1)) != bytes([args[0] & 255]):
            raise ValueError("Scalar byte storage differs")
    if address == 0x021D876C and result != MODE_RESULTS.get(state["mode"], 0):
        raise ValueError("Sparse switch result differs")
    if address == 0x021D8828 and (len(calls) != 2 or calls[1]["args"][0] != MODE_RESULTS.get(state["mode"], 0)):
        raise ValueError("Sparse switch forwarding differs")
    if address == 0x021D9628 and (len(calls) != 1 or calls[0]["args"][:2] != [0xFFFFFFFF, args[0]]):
        raise ValueError("Scalar call adaptation differs")
    if address == 0x021D963C and int.from_bytes(engine.mem_read(0x021DAA0C, 4), "little") != state["handle"]:
        raise ValueError("Handle capture differs")
    if address == 0x021D9654 and (len(calls) != 1 or calls[0]["args"][0] != state["handle"]):
        raise ValueError("Handle release forwarding differs")
    if address == 0x021D966C:
        target = next(x for x in calls if x["name"] == "func_0204bc78")["args"][2]
        if bytes(engine.mem_read(target, len(state["name"]))) != state["name"]:
            raise ValueError("Formatted resource name differs")
    if address == 0x021D9714 and result != state["ready"]:
        raise ValueError("Context query forwarding differs")
    if address == 0x021D9728 and result != (state["code"] if state["ready"] else 0):
        raise ValueError("Conditional context result differs")
    if address == 0x021D9CAC and result != int(state["flag"] != 255):
        raise ValueError("Signed sentinel classification differs")
    if address == 0x021DA04C and result != int(state["pair"][0] > state["pair"][1]):
        raise ValueError("Signed field comparison differs")
