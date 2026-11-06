import struct
from unicorn.arm_const import UC_ARM_REG_R0


def seed_update(engine, address, vector):
    if address != 0x021D837C:
        return {}
    phase, variant = vector % 12, vector // 12
    state = {"phase": phase, "subphase": [0, 1, 2, 4][variant % 4], "choice": variant % 2, "ready": (variant >> 2) & 1, "confirm": (variant >> 3) & 1, "context": (variant >> 4) & 1}
    engine.mem_write(0x021DA9A8, struct.pack("<2I", state["subphase"], phase))
    engine.mem_write(0x021DA984, struct.pack("<I", state["subphase"]))
    engine.mem_write(0x021DA9B4, struct.pack("<I", phase))
    engine.mem_write(0x021DA0FC, struct.pack("<I", state["choice"]))
    fields = [0] * 12
    fields[2], fields[7] = 0x03008000, 0x0300B000
    engine.mem_write(0x021DA9DC, struct.pack("<12I", *fields))
    for pointer in [fields[2], fields[7]]:
        engine.mem_write(pointer + 124, struct.pack("<I", 0xA5A55A5A))
    return state


def update_call(address, name, value, state):
    if not state:
        return value
    if name in {"func_ov007_021d9040", "func_ov007_021d7c5c", "func_ov007_021d96b0", "func_ov007_021d9c3c"}:
        return state["context"]
    if name in {"func_ov007_021d873c", "func_02041814", "func_ov007_021d82d8", "func_ov007_021da04c"}:
        return state["confirm"]
    if name in {"func_02041944", "func_ov007_021d81d0"}:
        return state["ready"]
    if name == "func_020273c8":
        return 5 if state["context"] else 0
    if name == "func_020725b8":
        return state["choice"]
    if name in {"func_ov007_021d8634", "func_ov007_021d864c", "func_ov007_021d8694"}:
        return {"func_ov007_021d8634": 0x1234, "func_ov007_021d864c": 0x5678, "func_ov007_021d8694": 0x9ABC}[name]
    return value


def assert_update(engine, address, calls, state):
    if not state:
        return
    phase, subphase = state["phase"], state["subphase"]
    ready, confirm, context = state["ready"], state["confirm"], state["context"]
    suffix = ["func_ov007_021d7c4c", "func_0204176c", "func_ov007_021d7c58"]
    expected = ["func_ov007_021d7ab0"]
    next_phase, next_subphase, result = phase, subphase, 5
    transition = None
    if phase == 0:
        expected += ["func_ov007_021d9040"] + ([] if context else ["func_02008430"])
        if state["choice"] == 0:
            expected += ["func_ov007_021d8abc"]
        expected += ["func_ov007_021d91b8"]
    elif phase == 1:
        expected += ["func_ov007_021d873c"] + ([] if confirm else ["func_ov007_021d80b0"])
        expected += ["func_ov007_021d7c5c"] + ([] if context else ["func_02008430"])
        expected += ["func_020c2020", "func_ov007_021d91f4"]
    elif phase == 2:
        expected += ["func_ov007_021d8694", "func_ov007_021d8944"]
    elif phase == 5:
        expected += ["func_ov007_021d7ac0"]
        if subphase == 0:
            expected += ["func_02041944"]
            if ready:
                expected += ["func_02041814"]
                if not confirm:
                    expected += ["func_ov007_021d7d7c", "func_020725b8", "func_ov007_021d8634", "func_020725b8", "func_ov007_021d864c", "func_ov007_021d9ccc"]
        else:
            expected += ["func_ov007_021d7ac0"] + (["func_ov007_021d9e68"] if subphase == 4 else [])
    elif phase == 6:
        expected += ["func_ov007_021d91b8", "func_ov007_021d82d8"]
        if confirm:
            expected += ["func_ov007_021d96b0", "func_ov007_021d7ad0"]
            transition = 9 if context else 7
        else:
            expected += ["func_ov007_021d81d0"]
            if ready:
                expected += ["func_ov007_021d8908", "func_ov007_021d7ad0"]
                transition = 8
    elif phase == 7:
        expected += ["func_ov007_021d7ac0"]
        if subphase == 0:
            expected += ["func_ov007_021d8634", "func_ov007_021d864c", "func_ov007_021d9ccc"]
        else:
            expected += ["func_ov007_021d7ac0"] + (["func_ov007_021d9e68"] if subphase == 2 else [])
        expected += ["func_020273c8"]
        if not context:
            suffix, result = [], 12
    elif phase == 10:
        expected += ["func_ov007_021da04c"]
        if confirm:
            expected += ["func_ov007_021d9c3c"]
            if context:
                expected += ["func_ov007_021d7ad0", "func_ov007_021d956c"]
                transition = 4
    if transition is not None:
        next_phase, next_subphase = transition, 0
    if [call["name"] for call in calls] != expected + suffix or engine.reg_read(UC_ARM_REG_R0) != result:
        raise ValueError("Frame state dispatch/order/result differs: " + str((state, expected + suffix, [call["name"] for call in calls], result, engine.reg_read(UC_ARM_REG_R0))))
    if bytes(engine.mem_read(0x021DA9A8, 8)) != struct.pack("<2I", next_subphase, next_phase):
        raise ValueError("Executed phase setter did not preserve the modeled transition")
    for call in calls:
        if call["name"] == "func_ov007_021d9ccc" and call["args"] != [1, int(phase == 7), 30, 0x34] or call["name"] == "func_ov007_021d9ccc" and int.from_bytes(bytes.fromhex(call["stack"])[:4], "little") != 0x78:
            raise ValueError("Frame coordinate truncation/stack argument differs")
        if call["name"] == "func_ov007_021d8944" and call["args"][:3] != [0, 0, 0x9ABC]:
            raise ValueError("Frame setup field forwarding differs")
