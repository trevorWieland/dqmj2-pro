import struct
from unicorn.arm_const import UC_ARM_REG_R0
from overlay_oracle003_intro_resources import seed_intro_resources003, intro_resources_call003, assert_intro_resources003

FUNCTIONS = {0x021D79E4, 0x021D7A14, 0x021D7A48, 0x021D7A78, 0x021D7AFC, 0x021D7C70, 0x021D7DAC, 0x021D7DC8, 0x021D7F90, 0x021D7FA4}


def native_helpers_intro003(address):
    return {"func_ov003_021d7868": (0x021D7868, 16), "func_ov003_021d7dac": (0x021D7DAC, 28), "func_ov003_021d7f90": (0x021D7F90, 20)} if address == 0x021D7AFC else {}


def seed_intro003(engine, address, vector):
    if address not in FUNCTIONS:
        return seed_intro_resources003(engine, address, vector)
    phase = [0, 1, 2, 3, 4, 5, 99][vector % 7]
    counter = [-128, -1, 0, 1, 2, 40, 127][vector // 7 % 7]
    flag = [255, 0, 1, 2][vector // 49 % 4]
    busy, ready = vector // 196 % 2, vector // 392 % 2
    before = bytearray((vector + index * 29) & 255 for index in range(64))
    before[4] = flag
    struct.pack_into("<2I", before, 8, [0, 1, 2, 0xFFFFFFFF][vector % 4], 0x10203040 + vector)
    before[20] = counter & 255
    handle = 0x0300F000 + vector * 8 if vector % 2 else 0
    struct.pack_into("<3I", before, 24, handle, 0xFFFFFFFF if ready else 0, phase)
    engine.mem_write(0x021E0440, bytes(before))
    return {"before": before, "phase": phase, "counter": counter, "flag": flag, "busy": busy, "ready": ready, "handle": handle, "soundHandle": 0x0300E000 + vector * 4, "mode": vector % 3, "display": int.from_bytes(engine.mem_read(0x04000000, 4), "little")}


def intro_call003(address, name, value, state):
    if address not in FUNCTIONS:
        return value
    if not state:
        return value
    if name == "func_0205f5dc":
        return state["soundHandle"]
    if name == "func_02027400":
        return state["mode"]
    if name == "func_02041800":
        return state["busy"]
    if name == "func_ov003_021d7ee8":
        return state["ready"]
    return value


def assert_intro003(engine, address, args, calls, state):
    if address not in FUNCTIONS:
        return assert_intro_resources003(engine, address, calls, state, args)
    if not state:
        return
    after = bytearray(state["before"])
    expected, result = [], None
    display = state["display"]
    if address == 0x021D79E4:
        expected = ["func_ov003_021d7a48", "func_0205e644", "func_0205e66c", "func_0205e73c", "func_0205e7a8", "func_ov003_021d7a14"]
        if calls[3]["args"][0] != args[0] or calls[4]["args"][:2] != [0, args[0]]:
            raise ValueError("Overlay003 sound identifier forwarding differs")
    elif address == 0x021D7A14:
        expected = ["func_0205f5dc", "func_0205e73c", "func_0205e73c"]
        struct.pack_into("<2I", after, 8, 1, state["soundHandle"])
        if [call["args"][0] for call in calls[1:]] != [181, 147]:
            raise ValueError("Overlay003 sound setup constants differ")
    elif address == 0x021D7A48:
        expected = ["func_0205f5f4"] if int.from_bytes(after[8:12], "little") == 1 else []
        if expected and calls[0]["args"][0] != int.from_bytes(after[12:16], "little"):
            raise ValueError("Overlay003 conditional sound handle release differs")
        struct.pack_into("<I", after, 8, 0)
    elif address == 0x021D7A78:
        expected = ["func_020273d8", "func_02027400"]
        struct.pack_into("<I", after, 24, 0)
        if state["mode"] == 2:
            expected += ["func_ov003_021d7c98"]
            struct.pack_into("<2I", after, 28, 0, 0)
        else:
            expected += ["func_02061238", "func_020406a8", "func_020612ec"]
            struct.pack_into("<I", after, 32, 2)
    elif address == 0x021D7AFC:
        phase, busy, ready = state["phase"], state["busy"], state["ready"]
        next_phase, result = phase, 0
        if phase == 0:
            expected = ["func_ov003_021d7dac"]
            if ready:
                expected += ["func_02041510"]
                next_phase = 1
        elif phase == 1:
            expected = ["func_02041800"]
            if busy != 1:
                expected += ["func_ov003_021d7dc8", "func_02061238", "func_020406a8", "func_020612ec"]
                next_phase = 2
        elif phase == 2:
            expected = ["func_0206157c", "func_ov003_021d7868"]
            if state["flag"] == 2:
                next_phase = 3
        elif phase == 3:
            expected = ["func_02041800"]
            if busy != 1:
                expected += ["func_ov003_021d7e04"]
                next_phase = 4
        elif phase == 4:
            expected = ["func_ov003_021d7ee8"]
            if ready:
                next_phase = 5
        elif phase == 5:
            after[20] = (state["counter"] - 1) & 255
            counter = int.from_bytes(after[20:21], "little", signed=True)
            if counter == 0:
                expected += ["func_02041510", "func_020c39d0"]
            if counter <= 0:
                expected += ["func_02041800"]
                if busy != 1:
                    expected += ["func_ov003_021d7f90"]
                    result = 1
                    display &= ~0xE000
        expected += ["func_ov003_021d7868"]
        result = result or int(state["flag"] == 1)
        struct.pack_into("<I", after, 32, next_phase)
    elif address == 0x021D7C70:
        expected = ["func_020bb38c", "func_020bb3f4"] if state["handle"] else []
        if expected and calls[0]["args"][:2] != [state["handle"], 1]:
            raise ValueError("Overlay003 animation handle cleanup differs")
    elif address == 0x021D7DAC:
        result = state["ready"]
    elif address == 0x021D7DC8:
        expected = ["func_020bb38c", "func_02008c58"]
        display &= ~0xE000
        if calls[0]["args"][:2] != [state["handle"], 1] or calls[1]["args"][:3] != [0, 0x06000000, 0x80000]:
            raise ValueError("Overlay003 animation release/VRAM clear arguments differ")
    elif address == 0x021D7F90:
        display &= ~0xE000
    elif address == 0x021D7FA4:
        struct.pack_into("<I", after, 28, 1)
    if [call["name"] for call in calls] != expected or result is not None and engine.reg_read(UC_ARM_REG_R0) != result:
        raise ValueError("Overlay003 intro/sound state dispatch/result differs")
    if bytes(engine.mem_read(0x021E0440, 64)) != after or int.from_bytes(engine.mem_read(0x04000000, 4), "little") != display:
        raise ValueError("Overlay003 intro current/countdown/handle/display state differs")
