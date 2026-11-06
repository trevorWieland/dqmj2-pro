import struct
from unicorn.arm_const import UC_ARM_REG_R0


def word(engine, address, width=4):
    return int.from_bytes(engine.mem_read(address, width), "little")


def seed_sequence(engine, address, vector):
    if address != 0x021D9858:
        return {}
    phase = [0, 5, 7, 10, 15, 18, 20, 25, 30, 40, 99][vector % 11]
    step = vector // 11
    row = step % 10
    links = list(struct.unpack("<5b", engine.mem_read(0x021DA07C + row * 5, 5)))
    length = links.index(-1) if -1 in links else 5
    index = (step // 10) % length
    timer = [-1, 0, 1, 2, 59, 60][(step // 10) % 6]
    state = [0x10203040, timer, [0, 1, 8, 16][step % 4], index, phase, 0x500 + step]
    engine.mem_write(0x021DB2B0, struct.pack("<IiiiII", *state))
    engine.mem_write(0x021DA924, bytes([row]))
    target = links[index]
    engine.mem_write(0x021DA614 + target * 48, b"\0")
    return {"state": state, "links": links, "target": target, "ready": (step // 60) % 2, "newSound": 0x10200000 + step, "newEffect": 0x22000000 + step, "display": word(engine, 0x04001000), "blend": word(engine, 0x04001052, 2)}


def sequence_call(address, name, value, state):
    if not state:
        return value
    if name in {"func_02041814", "func_ov007_021d873c"}:
        return state["ready"]
    if name == "func_0205e814":
        return state["newSound"]
    if name == "func_0205f35c":
        return state["newEffect"]
    if name in {"func_ov007_021d8634", "func_ov007_021d864c"}:
        return (0x1234 if name == "func_ov007_021d8634" else 0x5678) + state["target"]
    return value


def assert_sequence(engine, address, calls, state):
    if not state:
        return
    after = state["state"][:]
    sound, timer, blend, index, phase, effect = after
    expected = []
    result = 0
    changed_enabled = False
    display, blend_register = state["display"], state["blend"]
    if phase == 0:
        expected = ["func_ov007_021d9770"]
        after[2:5] = [16, 0, 5]
    elif phase == 5:
        expected = ["func_02041814"]
        if not state["ready"]:
            expected += ["func_020042c4", "func_0205e814"]
            after[0], after[1], after[4] = state["newSound"], 30, 7
    elif phase in {7, 20, 25}:
        after[1] -= 1
        if timer <= 0:
            if phase == 7:
                expected += ["func_0205f35c", "func_0205e7f4"]
                after[1], after[4], after[5] = 60, 10, state["newEffect"]
            elif phase == 20:
                expected += ["func_ov007_021d9628", "func_ov007_021d932c", "func_ov007_021d8724"]
                after[1], after[4] = 10, 25
                changed_enabled = True
            else:
                after[3] += 1
                if state["links"][after[3]] != -1:
                    after[4] = 18
                else:
                    after[1], after[4] = 0, 30
                    expected += ["func_02041538", "func_02041908", "func_0205e7f4", "func_0205e814"]
    elif phase == 10:
        blend_register = (blend | ((16 - blend) << 8)) & 65535
        after[1] -= 1
        numerator = after[1] * 16
        after[2] = abs(numerator) // 60 * (-1 if numerator < 0 else 1)
        if after[1] < 0:
            after[4] = 15
            display = display & ~0x1F00 | 0x1200
            expected += ["func_0205f404", "func_02041538", "func_0204157c"]
    elif phase == 15:
        expected = ["func_02041814"]
        if not state["ready"]:
            after[4] = 18
            expected += ["func_020414c8", "func_02041538", "func_0204157c", "func_ov007_021d929c"]
    elif phase == 18:
        expected += ["func_ov007_021d873c"]
        if state["ready"]:
            after[1], after[4] = 0, 25
        else:
            expected += ["func_ov007_021d8634", "func_ov007_021d864c", "func_ov007_021d95b0"]
            after[1], after[4] = 32, 20
    elif phase == 30:
        expected += ["func_02041814"]
        if not state["ready"]:
            expected += ["func_020414c8", "func_020418b0", "func_ov007_021d91f4"]
            after[4] = 40
    elif phase == 40:
        after[4] = 0
        expected += ["func_ov007_021d9854"]
        result = 1
    if not result:
        expected += ["func_ov007_021d95ec"]
    if [call["name"] for call in calls] != expected or engine.reg_read(UC_ARM_REG_R0) != result:
        raise ValueError("Unlock sequence dispatch/completion order differs")
    if bytes(engine.mem_read(0x021DB2B0, 24)) != struct.pack("<IiiiII", *after):
        raise ValueError("Unlock sequence countdown/index/state differs")
    if word(engine, 0x04001000) != display or word(engine, 0x04001052, 2) != blend_register:
        raise ValueError("Unlock sequence blend/division/display state differs")
    if bytes(engine.mem_read(0x021DA614 + state["target"] * 48, 1)) != bytes([changed_enabled]):
        raise ValueError("Executed unlock table-byte setter differs")
    for call in calls:
        if call["name"] in {"func_ov007_021d932c", "func_ov007_021d8724"} and call["args"][:2] != [state["target"], 1]:
            raise ValueError("Unlock selected row forwarding differs")
        if call["name"] == "func_ov007_021d95b0" and call["args"][:2] != [0x1234 + state["target"], 0x5678 + state["target"]]:
            raise ValueError("Unlock coordinate adaptation differs")
