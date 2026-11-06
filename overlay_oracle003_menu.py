import struct
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP
from overlay_oracle003_icons import seed_icons003, icons_call003, assert_icons003

FUNCTIONS = {0x021D7FB8, 0x021D7FF0, 0x021D8188, 0x021D81A8, 0x021D823C, 0x021D82F4}


def word(engine, address):
    return int.from_bytes(engine.mem_read(address, 4), "little")


def seed_menu003(engine, address, vector):
    if address not in FUNCTIONS:
        return seed_icons003(engine, address, vector)
    ui = bytearray((vector + index * 37) & 255 for index in range(52))
    ui[0], ui[1] = [0, 1, 2, 255][vector % 4], vector % 6
    context = bytearray((vector + index * 41) & 255 for index in range(228))
    context[209] = 0xA0 | (vector // 4) % 16
    runtime = 0x03004000
    cursor = [0, 4096, 0xFFFFFFF0][vector % 3]
    mode = [42, 41, 255][vector // 64 % 3]
    engine.mem_write(0x021E0464, bytes(ui))
    engine.mem_write(0x021E0498, bytes(context))
    engine.mem_write(runtime + 604, struct.pack("<I", cursor))
    engine.mem_write(runtime + 620, bytes([mode]))
    engine.mem_write(runtime + 623, bytes([128, 255, 0, 1, 127][vector % 5:vector % 5 + 1]))
    engine.mem_write(0x03006018, struct.pack("<h", [-32768, -1, 0, 1, 32767][vector % 5]))
    return {"ui": ui, "context": context, "runtime": runtime, "runtimeBefore": bytes(engine.mem_read(runtime, 624)), "payload": bytes(engine.mem_read(0x03008000, 208)), "recordId": int.from_bytes(engine.mem_read(0x03006018, 2), "little", signed=True), "present": vector // 8 % 2, "fade": vector // 192 % 2, "mode": mode, "running": cursor, "allocations": 0}


def menu_call003(engine, address, name, value, state):
    if address not in FUNCTIONS:
        return icons_call003(engine, address, name, value, state)
    if not state:
        return value
    first = engine.reg_read(UC_ARM_REG_R0)
    if name == "func_02061944":
        return state["runtime"]
    if name == "func_02062a10":
        return 0x03006000 if state["present"] else 0
    if name == "func_02041930":
        return state["fade"]
    if name == "func_0205fc10":
        return 0x03008000
    if name == "func_0201d444":
        template = bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_R1), 32)).split(b"\0", 1)[0]
        if template != b"fld_up_menu_parts.cch":
            raise ValueError("Overlay003 menu resource template differs")
        engine.mem_write(first, template + b"\0")
        return len(template)
    if name == "func_0205ff80" and bytes(engine.mem_read(first, 22)) != b"fld_up_menu_parts.cch\0":
        raise ValueError("Overlay003 menu formatted resource buffer differs")
    if name == "func_02065730":
        index = state["allocations"]
        args = [engine.reg_read(register) for register in [UC_ARM_REG_R0, UC_ARM_REG_R1]]
        if args != [state["runtime"] + 16 + (index + 1) * 12, 44 + index] or word(engine, engine.reg_read(UC_ARM_REG_SP)) != state["running"]:
            raise ValueError("Overlay003 indexed cell/identifier/cursor forwarding differs")
        updated = (state["running"] + 3) & 0xFFFFFFFF
        engine.mem_write(state["runtime"] + 604, struct.pack("<I", updated))
        delta = 7 + index
        state["running"] = (updated + delta) & 0xFFFFFFFF
        state["allocations"] += 1
        return delta
    return value


def assert_menu003(engine, address, args, calls, state):
    if address not in FUNCTIONS:
        return assert_icons003(engine, address, args, calls, state)
    if not state:
        return
    ui, context = bytearray(state["ui"]), bytearray(state["context"])
    runtime = bytearray(state["runtimeBefore"])
    expected, result = [], None
    if address == 0x021D7FB8:
        expected = ["func_02061bf0", "func_02060f14", "func_020c39d0", "func_ov003_021d81a8", "func_ov003_021d823c", "func_ov003_021d88e8"]
        ui[:2] = b"\0\0"
    elif address == 0x021D7FF0:
        expected = ["func_02061944"]
        flags = context[209]
        if ui[0] == 0:
            expected += ["func_02062328", "func_02062144", "func_ov003_021d867c"]
            flags |= 8
            if state["mode"] == 42 and flags & 1 == 0:
                context[208] = 0
                flags = (flags | 1) & ~10
                context[:208] = state["payload"]
                expected += ["func_0205fc10", "func_0205fd0c"]
            expected += ["func_02041930"]
            if state["fade"]:
                expected += ["func_02041510"]
            ui[0] = 1
        elif ui[0] == 1 and flags & 1 and flags & 4:
            expected += ["func_0205fd0c"]
            flags &= ~4
        context[209] = flags
        result = int(state["mode"] != 42)
        if result and flags & 1:
            expected += ["func_ov003_021d8ce8"]
        for call in calls:
            if call["name"] == "func_0205fc10" and (call["args"] != [0x021E0498, 0x021D89D8, 0x021D8CAC, 0] or bytes.fromhex(call["stack"]) != struct.pack("<4I", 18, 8192, 2, 0)):
                raise ValueError("Overlay003 menu callback identity/allocation arguments differ")
            if call["name"] == "func_02062144":
                selector = int.from_bytes(runtime[623:624], "little", signed=True) & 0xFFFFFFFF
                if call["args"][:2] != [selector, 0]:
                    raise ValueError("Overlay003 menu signed selector forwarding differs")
    elif address == 0x021D8188:
        expected = ["func_ov003_021d8ce8", "func_ov003_021d8890", "func_020622ec"]
        if calls[-1]["args"][:3] != [6, 10, 0]:
            raise ValueError("Overlay003 menu cleanup constants differ")
    elif address == 0x021D81A8:
        expected = ["func_02061944", "func_0201d444", "func_0205ff80"] + ["func_02065730"] * 14 + ["func_0205ff9c"]
        struct.pack_into("<I", runtime, 604, state["running"])
        if state["allocations"] != 14:
            raise ValueError("Overlay003 fourteen-cell allocation count differs")
        for index, call in enumerate(call for call in calls if call["name"] == "func_02065730"):
            if call["args"][2:] != [0, 2 if index < 2 else 1]:
                raise ValueError("Overlay003 cell count/flags differ")
    elif address == 0x021D823C:
        expected = ["func_02061c1c"] * 4 + ["func_02045ed0"]
        for call, values in zip(calls[:4], [[6, 11, 3, 11], [7, 5, 5, 5], [8, 20, 3, 11], [9, 26, 5, 5]]):
            if call["args"] != values or bytes.fromhex(call["stack"])[:12] != struct.pack("<3I", 2, 0, 0):
                raise ValueError("Overlay003 four-panel geometry/stack arguments differ")
    elif address == 0x021D82F4:
        expected = ["func_02061944", "func_02062a10"] + (["func_ov003_021d8348"] if state["present"] else [])
        if state["present"] and (calls[-1]["args"] != [state["runtime"] + 16 + (ui[1] + 3) * 12, state["recordId"] & 0xFFFFFFFF, ui[1], 1] or bytes.fromhex(calls[-1]["stack"])[:4] != bytes(4)):
            raise ValueError("Overlay003 conditional signed record/cell forwarding differs")
    if [call["name"] for call in calls] != expected or result is not None and engine.reg_read(UC_ARM_REG_R0) != result:
        raise ValueError("Overlay003 menu phase/bitfield/callback dispatch differs")
    if bytes(engine.mem_read(0x021E0464, 52)) != ui or bytes(engine.mem_read(0x021E0498, 228)) != context or bytes(engine.mem_read(state["runtime"], 624)) != runtime:
        raise ValueError("Overlay003 complete menu/payload/cursor state differs")
