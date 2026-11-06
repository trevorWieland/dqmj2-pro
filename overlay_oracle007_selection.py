import struct
from unicorn.arm_const import UC_ARM_REG_R0

FUNCTIONS = {0x021D80B0, 0x021D8170, 0x021D81D0, 0x021D82D8}


def word(engine, address):
    return int.from_bytes(engine.mem_read(address, 4), "little")


def seed_selection(engine, address, vector):
    if address not in FUNCTIONS:
        return {}
    state = {"choice": vector % 17 if vector % 17 < 16 else 0xFFFFFFFF, "enabled": (vector // 17) % 2, "flags": vector % 16, "buttons": (vector // 16) % 16, "change": vector // 256, "value": [-1, 0, 1, 127][(vector // 2) % 4], "mode": [-1, 0, 1, 170][(vector // 8) % 4], "pressed": vector % 2}
    if address == 0x021D81D0:
        state["choice"] = 4
    engine.mem_write(0x021DA0FC, struct.pack("<2I", state["choice"], 0xFFFFFFFF))
    if address == 0x021D81D0:
        buttons = sum(mask for index, mask in enumerate([64, 128, 32, 16]) if state["buttons"] & 1 << index)
        engine.mem_write(0x03005000, struct.pack("<H", buttons))
    if address == 0x021D82D8:
        engine.mem_write(0x03005002, struct.pack("<H", state["pressed"]))
    return state


def selection_call(engine, address, name, value, state):
    if not state:
        return value
    if name == "func_ov007_021d7e1c":
        direction = engine.reg_read(UC_ARM_REG_R0)
        if address == 0x021D8170:
            return 7 if state["flags"] & 1 << (direction - 1) else 0xFFFFFFFF
        return state["choice"] if not state["change"] else 5 + direction
    if name == "func_ov007_021d8170":
        return state["flags"]
    if name == "func_ov007_021d873c":
        return state["enabled"]
    if name in {"func_ov007_021d8634", "func_ov007_021d864c", "func_ov007_021d867c"}:
        return ({"func_ov007_021d8634": 100, "func_ov007_021d864c": 200, "func_ov007_021d867c": 300}[name] + engine.reg_read(UC_ARM_REG_R0)) & 0xFFFFFFFF
    if name == "func_ov007_021d86ac":
        return state["value"] & 0xFFFFFFFF
    if name == "func_ov007_021d86c4":
        return 123
    if name == "func_ov007_021d876c":
        return state["mode"] & 0xFFFFFFFF
    return value


def assert_selection(engine, address, calls, state):
    if not state:
        return
    result = engine.reg_read(UC_ARM_REG_R0)
    names = [call["name"] for call in calls]
    if address == 0x021D8170:
        if result != state["flags"] or [call["args"][0] for call in calls] != [1, 2, 3, 4]:
            raise ValueError("Directional availability mask differs")
    if address in {0x021D80B0, 0x021D81D0}:
        selected = state["choice"]
        changed = False
        if address == 0x021D80B0 and selected in {9, 10, 11, 12}:
            selected = 0 if state["enabled"] else 14
        if address == 0x021D81D0:
            valid = state["buttons"] & state["flags"]
            direction = next((index + 1 for index in range(4) if valid & 1 << index), 0)
            selected = 5 + direction if direction and state["change"] else selected
            changed = selected != state["choice"]
            if result != int(changed) or word(engine, 0x021DA100) != (state["choice"] if direction else 0xFFFFFFFF):
                raise ValueError("Directional priority/prior-selection behavior differs")
            expected = ["func_0202a634", "func_ov007_021d8170"] + (["func_ov007_021d7e1c"] if direction else [])
        else:
            expected = ["func_ov007_021d873c"] if state["choice"] in {9, 10, 11, 12} else []
        if address == 0x021D80B0 or changed:
            expected += ["func_ov007_021d8634", "func_ov007_021d864c", "func_ov007_021d867c", "func_ov007_021d7aa0"]
            if [word(engine, 0x021DA0F4), word(engine, 0x021DA0F8)] != [(100 + selected) & 0xFFFFFFFF, (200 + selected) & 0xFFFFFFFF]:
                raise ValueError("Selection descriptor fields differ")
            target_call = next(call for call in calls if call["name"] == "func_ov007_021d7aa0")
            if target_call["args"][0] != (300 + selected) & 0xFFFFFFFF:
                raise ValueError("Selection descriptor forwarding differs")
        if address == 0x021D81D0 and changed:
            expected += ["func_ov007_021d9628"]
        if names != expected or word(engine, 0x021DA0FC) != selected:
            raise ValueError("Selection dispatch/order differs")
    if address == 0x021D82D8:
        active = state["pressed"] and state["value"] != -1
        expected = ["func_ov007_021d86ac", "func_0202a634"]
        if active:
            expected += ["func_0205be34", "func_0205bdfc", "func_020c20f4", "func_0205bf2c", "func_ov007_021d86c4", "func_0205c060", "func_020c211c", "func_ov007_021d876c"]
            if state["mode"] > 0:
                expected += ["func_0203d0d8"]
            expected += ["func_ov007_021d9628"]
            for call in calls:
                if call["name"] in {"func_0205be34", "func_0205bdfc"} and call["args"][0] != state["value"]:
                    raise ValueError("Selection commit value differs")
        if result != int(active) or names != expected:
            raise ValueError("Selection confirmation gating/order differs")
