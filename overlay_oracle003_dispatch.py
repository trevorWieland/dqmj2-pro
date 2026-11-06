import struct
from unicorn.arm_const import UC_ARM_REG_R0
from overlay_oracle003_intro import native_helpers_intro003, seed_intro003, intro_call003, assert_intro003, intro_resources_call003

INDIRECT_003 = {0x021D7A78: "func_ov003_021d7a78", 0x021D7AFC: "func_ov003_021d7afc", 0x021D7C70: "func_ov003_021d7c70"}


def seed_dispatch003(engine, address, vector):
    if address != 0x021D72D0:
        return seed_intro003(engine, address, vector)
    if bytes(engine.mem_read(0x021E0104, 12)) != struct.pack("<3I", *INDIRECT_003):
        raise ValueError("Overlay003 initialized callback table identity differs")
    phase, returned, mode = vector % 6, [0, 1, 0xFFFFFFFF][(vector // 6) % 3], (vector // 18) % 3
    before = bytearray((vector + index * 23) & 255 for index in range(64))
    before[1:5] = bytes([phase, 0, [127, 255][vector // 54 % 2], mode])
    engine.mem_write(0x021E0440, bytes(before))
    return {"callbacks": INDIRECT_003, "before": before, "phase": phase, "returned": returned, "mode": mode}


def dispatch_call003(address, name, value, state, engine=None):
    if address != 0x021D72D0:
        value = intro_call003(address, name, value, state)
        return intro_resources_call003(engine, address, name, value, state) if address not in {0x021D79E4, 0x021D7A14, 0x021D7A48, 0x021D7A78, 0x021D7AFC, 0x021D7C70, 0x021D7DAC, 0x021D7DC8, 0x021D7F90, 0x021D7FA4} else value
    if state and name == "func_ov003_021d7afc":
        return state["returned"]
    return value


def assert_dispatch003(engine, address, calls, state, args=None):
    if address != 0x021D72D0:
        return assert_intro003(engine, address, args, calls, state)
    if not state:
        return
    phase, mode = state["phase"], state["mode"]
    after = bytearray(state["before"])
    expected, result = [], 12
    if phase == 0:
        expected = ["func_ov003_021d7a78"]
        after[1] = 1
    elif phase == 1:
        expected = ["func_ov003_021d7afc"]
        if state["returned"]:
            after[3], after[1] = 0, 2
    elif phase == 2:
        expected = ["func_ov003_021d7c70"]
        if mode in {1, 2}:
            after[1] = 4 if mode == 1 else 3
    elif phase == 3:
        expected, result = ["func_0206258c"], 2
    elif phase == 4:
        expected = ["func_ov003_021d75c8", "func_ov003_021d7c70", "func_020407bc", "func_020c3a30", "func_020c40f4", "func_0205bf2c"]
        result = 1
    expected += ["func_02041764"]
    if [call["name"] for call in calls] != expected or engine.reg_read(UC_ARM_REG_R0) != result or bytes(engine.mem_read(0x021E0440, 64)) != after:
        raise ValueError("Overlay003 indirect callback phase/completion state differs")
    if phase == 3 and calls[0]["args"][0] != 0 or phase == 4 and any(call["args"][0] != 1 for call in calls[2:-1]):
        raise ValueError("Overlay003 callback exit argument forwarding differs")
