import struct
from unicorn.arm_const import UC_ARM_REG_R0


def seed_flow(engine, address, vector):
    if address != 0x021D76A0:
        return {}
    phase, step = vector % 11, vector // 11
    subphase = [0, 1, 2, 4, 5][step % 5]
    counter = [0, 1, 2, 40, 255][(step // 5) % 5]
    bits = (step // 25) % 8
    words = [0x1234005A | counter << 8, 77, 0x11111111, 0x22222222, 0x33333333, 0x44444444, 0x55555555, 0x66666666, 0x77777777, 0x88888888, subphase, phase, 0x99999999, 99]
    before = struct.pack("<14I", *words)
    engine.mem_write(0x021DA980, before)
    engine.mem_write(0x021DA0F4, struct.pack("<4I", 100, 200, step % 16, 15))
    fields = [0] * 12
    fields[7] = 0x0300B000
    engine.mem_write(0x021DA9DC, struct.pack("<12I", *fields))
    engine.mem_write(0x0300B07C, struct.pack("<I", 0xA5A55A5A))
    return {"phase": phase, "subphase": subphase, "counter": counter, "ready": bits & 1, "busy": (bits >> 1) & 1, "context": (bits >> 2) & 1, "code": [128, 129, 140, 0, 0xFFFFFFFF][step % 5], "choice": step % 16, "before": before}


def flow_call(address, name, value, state):
    if not state:
        return value
    if name in {"func_ov007_021d96b0", "func_ov007_021d9cac", "func_ov007_021d8984"}:
        return state["context"]
    if name in {"func_02041944", "func_ov007_021da04c"}:
        return state["ready"]
    if name == "func_02041814":
        return state["busy"]
    if name == "func_ov007_021d8664":
        return 2 if state["context"] else 0
    if name == "func_02041800":
        return 2 if state["ready"] else 1
    if name == "func_ov007_021d9728":
        return state["code"]
    return value


def assert_flow(engine, address, calls, state):
    if not state:
        return
    phase, subphase, counter = [state[name] for name in ["phase", "subphase", "counter"]]
    ready, busy, context = [state[name] for name in ["ready", "busy", "context"]]
    expected, result = [], 5
    next_phase, next_subphase, next_counter = phase, subphase, counter
    object_enabled = None
    if phase == 0:
        expected = ["func_ov007_021d8af8", "func_ov007_021d966c", "func_ov007_021d96b0"]
        next_phase, next_subphase = (9 if context else 1), 0
    elif phase == 1:
        next_phase, next_subphase = 2, 0
    elif phase == 2:
        expected = ["func_02041898", "func_ov007_021d85e4", "func_ov007_021d74e4", "func_ov007_021d8abc"]
        next_phase, next_subphase, object_enabled = 3, 0, True
    elif phase == 3:
        expected = ["func_ov007_021d88dc", "func_02041944"]
        next_phase, next_subphase = (5 if ready else 4), 0
        if not ready:
            next_counter = 0
    elif phase == 4:
        expected = ["func_02041814"]
        if not busy and counter == 0:
            expected += ["func_ov007_021d85e4", "func_ov007_021d75f0", "func_02041510", "func_ov007_021d8664", "func_ov007_021d8abc", "func_ov007_021d8bc0"]
            next_phase, next_subphase, object_enabled = 6, 0, not context
        else:
            next_counter = (counter - 1) & 255
    elif phase == 5:
        expected = ["func_ov007_021d7ac0"]
        if subphase == 0:
            next_subphase = 4
        else:
            expected += ["func_ov007_021d7ac0"]
            if subphase == 4:
                expected += ["func_ov007_021da04c"]
                if ready:
                    expected += ["func_ov007_021d9cac"]
                    next_phase, next_subphase, next_counter = (10 if context else 4), 0, (0 if context else 40)
                    if context:
                        expected += ["func_ov007_021d953c"]
    elif phase == 6:
        expected = ["func_ov007_021d8bc0"]
    elif phase == 7:
        if subphase == 0:
            expected = ["func_020414b0", "func_02041510"]
            next_subphase = 2
        elif subphase == 2:
            expected = ["func_02041800"]
            if ready:
                expected += ["func_ov007_021d96b0", "func_ov007_021d89a8"]
                next_phase, next_subphase = (9 if context else phase), 5
        elif subphase == 5:
            expected = ["func_0203d138", "func_ov007_021d85c4"]
            next_subphase, result = 0, 11
    elif phase == 8:
        expected = ["func_ov007_021d8984"]
        if context:
            expected += ["func_ov007_021d7658"]
            next_phase, next_subphase = 2, 0
    elif phase == 9:
        expected = ["func_ov007_021d9728"]
        if state["code"] in {128, 129, 140}:
            next_phase = 1 if state["code"] == 128 else 7
            next_subphase = 5 if state["code"] == 129 else 0
    expected += ["func_ov007_021d7690", "func_02041764", "func_ov007_021d769c"]
    after = bytearray(state["before"])
    after[1] = next_counter
    for index, value in [(1, subphase), (10, next_subphase), (11, next_phase), (13, phase)]:
        struct.pack_into("<I", after, index * 4, value)
    if [call["name"] for call in calls] != expected or engine.reg_read(UC_ARM_REG_R0) != result or bytes(engine.mem_read(0x021DA980, 56)) != after:
        raise ValueError("Main phase machine dispatch/current/pending/counter state differs")
    flags = 0xA5A55A5A
    if object_enabled is not None:
        flags = flags | 2 if object_enabled else flags & ~2
    if int.from_bytes(engine.mem_read(0x0300B07C, 4), "little") != flags:
        raise ValueError("Main phase machine native object enable writer differs")
    for call in calls:
        if call["name"] == "func_ov007_021d8664" and call["args"][0] != state["choice"] or call["name"] == "func_ov007_021d74e4" and call["args"][0] != 0x1234:
            raise ValueError("Main phase struct-return/halfword selection forwarding differs")
