import struct
from unicorn.arm_const import UC_ARM_REG_R0


def native_helpers002(address):
    return {"func_ov002_021d7850": (0x021D7850, 76)} if address == 0x021D838C else {}


def seed_objects002(engine, address, vector):
    if address != 0x021D838C:
        return {}
    mode = vector % 2
    engine.mem_write(0x021DAEE4, bytes([127, 128, 255, 0]) + struct.pack("<2I", 0, mode))
    objects = []
    for index in range(36):
        pointer, root, nested = 0x03008000 + index * 256, 0x0300B000 + index * 64, 0x0300C000 + index * 256
        kind = [-128, -1, 0, 1, 3, 4, 127][(index + vector) % 7]
        exists, enabled = (index + vector) % 7 != 0, (index + vector) % 3 != 0
        engine.mem_write(pointer, struct.pack("<I", root if exists else 0))
        engine.mem_write(pointer + 5, bytes([kind & 255]))
        engine.mem_write(root + 4, struct.pack("<I", nested))
        engine.mem_write(nested + 24, struct.pack("<I", 2 if enabled else 0))
        values = [(-128, -1, 0, 1, 127)[(index + vector + component) % 5] for component in range(4)]
        engine.mem_write(nested + 92, bytes(value & 255 for value in values))
        objects.append({"pointer": pointer, "kind": kind, "active": exists and enabled, "values": values})
    table = bytes(engine.mem_read(0x021DA57B, 63))
    return {"objects": objects, "mode": mode, "table": [int.from_bytes(table[index:index + 1], "little", signed=True) for index in range(0, 63, 3)]}


def object_call002(engine, address, name, value, state):
    if not state:
        return value
    if name == "func_02049ad0":
        return state["objects"][engine.reg_read(UC_ARM_REG_R0)]["pointer"]
    if name in {"func_02048f5c", "func_02048f6c"}:
        return 0xD10 if name == "func_02048f5c" else 0xD20
    return value


def assert_objects002(engine, address, args, calls, state):
    if not state:
        return
    expected = ["func_02049008"]
    forwarded = []
    for item in state["objects"]:
        expected += ["func_02049ad0"]
        if not item["active"]:
            continue
        expected += ["func_ov002_021d7850"]
        if item["kind"] == 127:
            continue
        if item["kind"] == 3 and state["mode"] == 0:
            expected += ["func_02048f5c", "func_02045dc4", "func_02048f6c", "func_02045dc4"]
            forwarded += [("func_02045dc4", [1, handle, *[value & 255 for value in item["values"]]]) for handle in [0xD10, 0xD20]]
            continue
        if item["kind"] == 3:
            expected += ["func_02049f4c"]
        slot = state["table"].index(item["kind"]) if item["kind"] in state["table"] else 0
        expected += ["func_0206006c"]
        forwarded += [("func_0206006c", [0x021DAF9C + slot * 12, *[value & 0xFFFFFFFF for value in item["values"]]])]
    expected += ["func_020851d4", "func_02085200"]
    if [call["name"] for call in calls] != expected or calls[0]["args"] != [args[0], 127, 0xFFFFFF80, 0xFFFFFFFF]:
        raise ValueError("Thirty-six-object traversal/gating/order differs")
    actual = []
    for call in calls:
        if call["name"] in {"func_02045dc4", "func_0206006c"}:
            count = 2 if call["name"] == "func_02045dc4" else 1
            values = call["args"] + list(struct.unpack("<" + "I" * count, bytes.fromhex(call["stack"])[:count * 4]))
            actual.append((call["name"], values))
    if actual != forwarded:
        raise ValueError("Object slot/signed/unsigned component forwarding differs")
