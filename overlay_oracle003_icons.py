import struct
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2

from overlay_oracle003_cells import seed_cells003, cells_call003, assert_cells003

IDS = [1, 42, 0x9994, 0x9995, 0x9996, 0x9997, 0x9998, 0x9999, 0x999A, 0xFFFFFFFF]
SLOTS = [0, 7, 8, 9, 254, 255, 0xFFFFFFFF]
SPECIAL_COUNTS = {0x9995: 2, 0x9996: 0, 0x9997: 1, 0x9998: 2, 0x9999: 0}


def parameters(vector):
    state = {"id": IDS[vector % 10], "mode": vector // 10 % 3, "size": vector // 30 % 3, "special": vector // 90 % 2, "unavailable": vector // 180 % 2, "failure": vector // 360 % 5, "slot": SLOTS[vector % 7], "frame": vector % 3}
    state["count"] = 0 if state["mode"] == 0 else SPECIAL_COUNTS.get(state["id"], state["size"])
    return state


def string(engine, address):
    return bytes(engine.mem_read(address, 32)).split(b"\0", 1)[0]


def seed_icons003(engine, address, vector):
    if address != 0x021D8348:
        return seed_cells003(engine, address, vector)
    state = parameters(vector)
    engine.mem_write(0x0301FF00, struct.pack("<I", state["special"]))
    state.update(cells=bytes(engine.mem_read(0x0300A000, 36)), paletteCalls=0, graphicsCalls=0)
    return state


def icon_arguments003(address, vector, args):
    if address == 0x021D8348:
        state = parameters(vector)
        args[:] = [0x0300A000, state["id"], state["slot"], state["mode"]]


def icons_call003(engine, address, name, value, state):
    if address != 0x021D8348:
        return cells_call003(engine, address, name, value, state)
    if not state:
        return value
    if name == "func_02044cdc":
        return state["size"]
    if name == "func_02072f48":
        return state["unavailable"]
    if name == "func_02072f1c":
        return state["frame"]
    if name == "func_02061de4":
        return 0x1200 + (engine.reg_read(UC_ARM_REG_R1) & 255)
    if name == "func_0201d444":
        template = string(engine, engine.reg_read(UC_ARM_REG_R1))
        if template == b"MonsterIconDat.NICA":
            rendered = template
        elif template in {b"ic_%04x.NCLD", b"ic_%04x.NCGR"}:
            if engine.reg_read(UC_ARM_REG_R2) != state["id"]:
                raise ValueError("Overlay003 icon formatter identifier differs")
            rendered = (template.decode() % state["id"]).encode()
        else:
            raise ValueError("Overlay003 icon formatter selected an unknown template")
        engine.mem_write(engine.reg_read(UC_ARM_REG_R0), rendered + b"\0")
        return len(rendered)
    if name == "func_0203cf20":
        if string(engine, engine.reg_read(UC_ARM_REG_R0)) != b"MonsterIconDat.NICA" or engine.reg_read(UC_ARM_REG_R2) != 2:
            raise ValueError("Overlay003 icon archive/heap differs")
        filename = string(engine, engine.reg_read(UC_ARM_REG_R1))
        if filename == ("ic_%04x.NCLD" % state["id"]).encode():
            index = state["paletteCalls"]
            state["paletteCalls"] += 1
            return 0 if state["failure"] == 1 and index == 0 or state["failure"] == 2 and index == state["count"] else 0x03008000
        if filename == ("ic_%04x.NCGR" % state["id"]).encode():
            index = state["graphicsCalls"]
            state["graphicsCalls"] += 1
            return 0 if state["failure"] == 3 and index == 0 or state["failure"] == 4 else 0x03009000
        raise ValueError("Overlay003 icon child resource filename differs")
    return value


def assert_icons003(engine, address, args, calls, state):
    if address != 0x021D8348:
        return assert_cells003(engine, address, args, calls, state)
    if not state:
        return
    expected, palettes, graphics, freed = [], [], [], []
    fallback = None
    if state["id"] not in SPECIAL_COUNTS:
        expected += ["func_02044cdc", "func_02072f48"]
        if state["unavailable"] and not state["special"]:
            fallback = 0x9995
    if fallback is None:
        expected += ["func_0201d444"]
        for index in range(state["count"] + 1):
            expected += ["func_0201d444", "func_0203cf20"]
            if state["failure"] == 1 and index == 0 or state["failure"] == 2 and index == state["count"]:
                fallback = 0x9996 + state["count"]
                break
            palette = (state["slot"] + 1 + index) & 255
            if palette >= 9:
                palette = (palette + 1) & 255
            palettes.append([0x03008000, palette * 32, 32])
            freed.append([2, 0x03008000])
            expected += ["func_020481b8", "func_0202a498"]
    if fallback is None:
        for index in range(state["count"] + 1):
            expected += ["func_0201d444", "func_0203cf20"]
            if state["failure"] == 3 and index == 0 or state["failure"] == 4:
                continue
            if state["mode"] != 1:
                expected += ["func_02072f1c"]
            first, second = struct.unpack_from("<2I", state["cells"], index * 12)
            offset = 48 + 800 * (index if state["mode"] == 1 else state["frame"])
            graphics.append([state["cells"][index * 12 + 11], 0x03009000 + offset, first, second])
            freed.append([2, 0x03009000])
            expected += ["func_0204540c", "func_0202a498"]
        expected += ["func_02048308"]
        returned = state["count"]
    else:
        expected += ["func_02061de4"]
        returned = 0x1200 + (fallback & 255)
        target = calls[-1]
        if target["args"] != [0x0300A000, fallback, state["slot"], state["mode"]] or bytes.fromhex(target["stack"])[:4] != bytes(4):
            raise ValueError("Overlay003 icon size/special fallback forwarding differs")
    if [call["name"] for call in calls] != expected or engine.reg_read(UC_ARM_REG_R0) != returned:
        raise ValueError("Overlay003 icon resource/fallback/flush order differs")
    if [call["args"][:3] for call in calls if call["name"] == "func_020481b8"] != palettes or [call["args"] for call in calls if call["name"] == "func_0204540c"] != graphics or [call["args"][:2] for call in calls if call["name"] == "func_0202a498"] != freed:
        raise ValueError("Overlay003 palette slot/wrap/graphics-cell/ownership transfer differs")
    if bytes(engine.mem_read(0x0300A000, 36)) != state["cells"]:
        raise ValueError("Overlay003 icon transfer unexpectedly changed its input cells")
