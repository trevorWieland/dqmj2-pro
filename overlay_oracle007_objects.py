import struct
from unicorn.arm_const import UC_ARM_REG_R0

ARRAY_FUNCTIONS = {0x021D88DC, 0x021D8908, 0x021D8944, 0x021D8984, 0x021D89A8}
MANAGER_FUNCTIONS = {0x021D8ABC, 0x021D9138, 0x021D91B8, 0x021D93AC, 0x021D93DC, 0x021D9400, 0x021D953C, 0x021D956C, 0x021D95B0, 0x021D95EC}
HELPERS = {0x021D88DC: {"func_02086b14": (0x02086B14, 16)}, 0x021D93DC: {"func_02048a60": (0x02048A60, 12)}, 0x021D9400: {"func_02048a88": (0x02048A88, 12)}, 0x021D95B0: {"func_02048a60": (0x02048A60, 12)}}
for entry in [0x021D8DB8, 0x021D8E4C, 0x021D9158]:
    HELPERS[entry] = {"func_02048a60": (0x02048A60, 12)}
    if entry != 0x021D8DB8:
        HELPERS[entry]["func_ov007_021d85e4"] = (0x021D85E4, 24)
    if entry != 0x021D9158:
        HELPERS[entry].update({"func_02048a94": (0x02048A94, 8), "func_02048a9c": (0x02048A9C, 8)})
HELPERS[0x021D89C0] = {"func_ov007_021d85e4": (0x021D85E4, 24), "func_02048a60": (0x02048A60, 12), "func_02048a94": (0x02048A94, 8), "func_02048a9c": (0x02048A9C, 8)}
HELPERS[0x021D8BC0] = {"func_ov007_021d85e4": (0x021D85E4, 24), "func_ov007_021d8abc": (0x021D8ABC, 60)}
HELPERS[0x021D8EE8] = {"func_02048a60": (0x02048A60, 12), "func_02048a94": (0x02048A94, 8), "func_02048a9c": (0x02048A9C, 8)}
HELPERS[0x021D8FBC] = {"func_02048a94": (0x02048A94, 8), "func_02048a9c": (0x02048A9C, 8), "func_ov007_021d93ac": (0x021D93AC, 48)}
HELPERS[0x021D7E1C] = {"func_ov007_021d7e1c": (0x021D7E1C, 660), "func_ov007_021d8634": (0x021D8634, 24), "func_ov007_021d864c": (0x021D864C, 24), "func_ov007_021d873c": (0x021D873C, 24)}
HELPERS[0x021D837C] = {"func_ov007_021d7ab0": (0x021D7AB0, 16), "func_ov007_021d7ac0": (0x021D7AC0, 16), "func_ov007_021d7ad0": (0x021D7AD0, 24), "func_ov007_021d8abc": (0x021D8ABC, 60), "func_ov007_021d91b8": (0x021D91B8, 60)}
HELPERS[0x021D9E68] = {"func_02026144": (0x02026144, 524), "func_ov007_021d9400": (0x021D9400, 36), "func_02048a88": (0x02048A88, 12), "func_ov007_021d93ac": (0x021D93AC, 48)}
HELPERS[0x021D9CCC] = {"_fflt": (0x02025A28, 72), "_fdiv": (0x02025578, 952), "_fgr": (0x0202537C, 92), "_fmul": (0x02025AB8, 480), "_fadd": (0x02024E0C, 540), "_fsub": (0x02025CA4, 632), "_ffix": (0x020259B4, 52), "func_ov007_021d93ac": (0x021D93AC, 48), "func_ov007_021d93dc": (0x021D93DC, 36), "func_ov007_021d9400": (0x021D9400, 36), "func_02048a60": (0x02048A60, 12), "func_02048a88": (0x02048A88, 12)}
HELPERS[0x021D9858] = {"func_ov007_021d8724": (0x021D8724, 24), "func_ov007_021d9854": (0x021D9854, 4)}
HELPERS[0x021D76A0] = {"func_ov007_021d85e4": (0x021D85E4, 24), "func_ov007_021d8abc": (0x021D8ABC, 60), "func_ov007_021d7ac0": (0x021D7AC0, 16)}


def word(engine, address):
    return int.from_bytes(engine.mem_read(address, 4), "little")


def set_word(engine, address, value):
    engine.mem_write(address, struct.pack("<I", value & 0xFFFFFFFF))


def native_helpers(address):
    return HELPERS.get(address, {})


def seed_objects(engine, address, vector):
    if address == 0x021D8848:
        return {"allocated": 0x0300C000, "objectFlags": word(engine, 0x0300C080)}
    if address == 0x021D96B0:
        return {"value": 0x12345678 + vector, "prior": word(engine, 0x021DAE60), "returned": vector % 2}
    if address == 0x021D9C3C:
        state = [-128, -1, *range(11), 127][vector % 14]
        engine.mem_write(0x021DA924, bytes([state & 255]))
        return {"phase": state, "returned": (vector // 14) % 2}
    if address in ARRAY_FUNCTIONS:
        pointers = [0x03006000 + index * 256 for index in range(8)]
        engine.mem_write(0x021DA9D8, struct.pack("<8I", *pointers))
        for index, pointer in enumerate(pointers):
            set_word(engine, pointer + 24, (word(engine, pointer + 24) & ~2) | (((vector // 8 + index) % 2) << 1))
        pointer = pointers[vector % 8] if address != 0x021D89A8 else pointers[0]
        return {"pointer": pointer, "flags": word(engine, pointer + 24), "prior12": word(engine, pointer + 12)}
    if address in MANAGER_FUNCTIONS:
        fields = [0] * 12
        for index, pointer in [(1, 0x03007000), (2, 0x03008000), (7, 0x03009000), (8, 0x0300A000), (10, 0x0300B000), (11, 0x0300C000)]:
            fields[index] = pointer
            set_word(engine, pointer + 124, (word(engine, pointer + 124) & ~2) | (((vector // 2) % 2) << 1))
        if address == 0x021D956C and vector % 2 == 0:
            fields[11] = 0
        engine.mem_write(0x021DA9DC, struct.pack("<12I", *fields))
        return {"fields": fields, "flags": {pointer: word(engine, pointer + 124) for pointer in fields if pointer}, "releaseByte": bytes(engine.mem_read(fields[11] + 129, 1))[0] if fields[11] else None, "allocated": 0 if vector % 4 == 0 else 0x0300D000 + (vector % 4) * 256}
    return {}


def object_arguments(address, vector, args):
    if address == 0x021D96B0:
        args[0] = [0, 127, 128, 129, 130, 139, 140, 141, 0xFFFFFFFF][vector % 9]
    if address in ARRAY_FUNCTIONS:
        args[0] = vector % 8
    if address in {0x021D8ABC, 0x021D91B8, 0x021D93DC, 0x021D9400}:
        args[0] = vector % 2
    if address == 0x021D93AC:
        args[0], args[1] = (vector // 2) % 2, vector % 2
    if address == 0x021D95B0:
        args[0] = [0, 1, 4, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF][vector % 6]
        args[1] = [0, 3, 4, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF][(vector // 6) % 6]


def object_call(address, name, value, state):
    if address == 0x021D8848 and name == "func_02084924":
        return state["allocated"]
    if address == 0x021D96B0 and name == "func_02025a70":
        return state["value"]
    if address == 0x021D96B0 and name == "func_0204bd00" or address == 0x021D9C3C and name == "func_ov007_021d9858":
        return state["returned"]
    if state and address == 0x021D953C and name == "func_0202a44c":
        return state["allocated"]
    return value


def assert_objects(engine, address, args, calls, state):
    if not state:
        return
    result = engine.reg_read(UC_ARM_REG_R0)
    if address == 0x021D8848:
        expected = [[0, 0, 5], [0, 2, 1], [7, 0, 2, 32], [state["allocated"] + 60, 8, 0]]
        if len(calls) != 4 or any(call["args"][:len(arguments)] != arguments for call, arguments in zip(calls, expected)):
            raise ValueError("Initial object setup arguments differ")
        if word(engine, 0x021DA9D8) != state["allocated"] or word(engine, state["allocated"] + 128) != state["objectFlags"] | 0x800:
            raise ValueError("Initial object storage/flag differs")
    if address == 0x021D96B0:
        valid = args[0] in {128, 129, 140}
        expected_calls = ["func_0205be14", "func_02025a70", "func_0204bd00"] if args[0] in {129, 140} else ["func_0204bd00"] if valid else []
        if [call["name"] for call in calls] != expected_calls or result != (state["returned"] if valid else 0):
            raise ValueError("Context switch dispatch differs")
        expected_value = state["value"] if args[0] in {129, 140} else state["prior"]
        if word(engine, 0x021DAE60) != expected_value or valid and calls[-1]["args"][:2] != [0x021DAA10, args[0]]:
            raise ValueError("Context switch state/call forwarding differs")
    if address == 0x021D9C3C:
        active = 0 <= state["phase"] <= 9
        expected_phase = 255 if active and state["returned"] else state["phase"] & 255
        if len(calls) != int(active) or result != int(not active or state["returned"] != 0) or bytes(engine.mem_read(0x021DA924, 1))[0] != expected_phase:
            raise ValueError("Signed state switch completion differs")
    if address in {0x021D88DC, 0x021D8908}:
        expected = state["flags"] | 2 if address == 0x021D88DC else state["flags"] & ~2
        if word(engine, state["pointer"] + 24) != expected:
            raise ValueError("Object flag update differs")
    if address == 0x021D88DC:
        if word(engine, state["pointer"] + 12) != 16 or word(engine, state["pointer"] + 16) != state["prior12"]:
            raise ValueError("Executed native four-instruction state writer differs")
    if address == 0x021D8944 and calls[-1]["args"] != [state["pointer"] + 60, 6, args[1], args[2]]:
        raise ValueError("Object field call adaptation differs")
    if address == 0x021D8984 and result != int(state["flags"] & 2 != 2):
        raise ValueError("Object flag classification differs")
    if address == 0x021D89A8 and calls[0]["args"][0] != state["pointer"]:
        raise ValueError("Object forwarding differs")
    if address in {0x021D8ABC, 0x021D91B8, 0x021D93AC}:
        index = 7 if address == 0x021D8ABC else 2 if address == 0x021D91B8 else 1 if args[0] == 0 else 10
        pointer = state["fields"][index]
        enabled = args[1] if address == 0x021D93AC else args[0]
        expected = state["flags"][pointer] | 2 if enabled else state["flags"][pointer] & ~2
        if word(engine, pointer + 124) != expected:
            raise ValueError("Selected manager flag update differs")
    if address == 0x021D9138 and calls[0]["args"][:2] != [state["fields"][2] + 8, 1]:
        raise ValueError("Manager field forwarding differs")
    if address in {0x021D93DC, 0x021D9400}:
        pointer = state["fields"][1 if args[0] == 0 else 10]
        offset = 108 if address == 0x021D93DC else 100
        if bytes(engine.mem_read(pointer + offset, 8)) != struct.pack("<2I", args[1], args[2]):
            raise ValueError("Executed native three-instruction field writer differs")
    if address == 0x021D953C:
        if word(engine, 0x021DAA08) != state["allocated"] or calls[-1]["args"][:2] != [1, state["allocated"]]:
            raise ValueError("Allocation storage/forwarding differs")
    if address == 0x021D956C:
        if word(engine, 0x021DAA08) != 0:
            raise ValueError("Manager release did not clear its handle")
        if state["fields"][11] and (len(calls) != 2 or calls[0]["args"][:2] != [1, state["releaseByte"]] or calls[1]["args"][:2] != [5, state["fields"][11]]):
            raise ValueError("Manager release protocol differs")
        if not state["fields"][11] and calls:
            raise ValueError("Null manager handle was unexpectedly released")
    if address == 0x021D95B0:
        pointer = state["fields"][11]
        if bytes(engine.mem_read(pointer + 108, 8)) != struct.pack("<2I", (args[0] - 4) & 0xFFFFFFFF, (args[1] - 4) & 0xFFFFFFFF):
            raise ValueError("Unsigned field-pair offset differs")
    if address == 0x021D95EC:
        pointer = state["fields"][11]
        expected_calls = 1 if state["flags"][pointer] & 2 == 2 else 0
        if len(calls) != expected_calls or calls and calls[0]["args"][:2] != [pointer + 8, 1]:
            raise ValueError("Conditional manager field call differs")
