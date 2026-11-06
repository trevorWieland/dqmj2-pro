import struct

FUNCTIONS = {0x021D89C0, 0x021D8BC0, 0x021D8AF8}


def word(engine, address):
    return int.from_bytes(engine.mem_read(address, 4), "little")


def seed_manager(engine, address, vector):
    if address not in FUNCTIONS:
        return {}
    fields = [0] * 12
    fields[7], fields[8] = 0x0300B000, 0x0300A000
    engine.mem_write(0x021DA9DC, struct.pack("<12I", *fields))
    flags = (word(engine, fields[7] + 124) & ~2) | ((vector // 24) % 2 << 1)
    engine.mem_write(fields[7] + 124, struct.pack("<I", flags))
    choice = [10, 20, 3 if vector % 2 else 4, 0]
    engine.mem_write(0x021DA0F4, struct.pack("<4I", *choice))
    return {"fields": fields, "flags": flags, "special": choice[2] == 3, "available": [0, 1, 2, 255, 256, 0xFFFFFFFF][(vector // 2) % 6], "value": [10799, 10800][(vector // 12) % 2]}


def manager_call(address, name, value, state):
    if not state:
        return value
    if name == "func_ov007_021d85fc":
        return 3
    if name == "func_020c20e4":
        return state["available"]
    if name == "func_ov007_021d860c":
        return state["value"]
    return value


def assert_manager(engine, address, calls, state):
    if not state:
        return
    low = state["value"] < 10800
    available = state["available"]
    fields = state["fields"]
    if address == 0x021D89C0:
        mode = ((19 if available else 7) if low else (20 if available else 11)) if state["special"] else (available + (5 if low else 9)) & 255
        chosen = [call for call in calls if call["name"] == "func_02048644"]
        if len(chosen) != 1 or chosen[0]["args"][:3] != [fields[7], fields[8], mode]:
            raise ValueError("Threshold-dependent manager mode differs")
        if word(engine, fields[7] + 124) != state["flags"] | 2 or bytes(engine.mem_read(fields[7] + 108, 8)) != struct.pack("<2I", 220, 4) or bytes(engine.mem_read(fields[7] + 120, 2)) != b"\1\1":
            raise ValueError("Executed manager coordinate/enable/byte state differs")
    if address == 0x021D8BC0:
        enabled = state["flags"] & 2 != 0
        skipped = enabled and low and available == 0
        updated = enabled and not skipped
        mode = ((19 if low else 20) if state["special"] else (available + (5 if low else 9)) & 255) if available else 9
        chosen = [call for call in calls if call["name"] == "func_02048644"]
        cleared = [call for call in calls if call["name"] == "func_ov007_021d8abc"]
        if len(chosen) != int(updated) or chosen and chosen[0]["args"][:3] != [fields[7], fields[8], mode] or len(cleared) != int(skipped):
            raise ValueError("Manager refresh disable/mode decision differs")
        expected_flags = state["flags"] & ~2 if skipped else state["flags"]
        if word(engine, fields[7] + 124) != expected_flags or word(engine, 0x020FF028) != 1:
            raise ValueError("Manager refresh flags/main-module notification differ")
