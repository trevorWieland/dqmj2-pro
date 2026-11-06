import struct


def word(engine, address, width=4):
    return int.from_bytes(engine.mem_read(address, width), "little")


def seed_transition(engine, address, vector):
    if address != 0x021D9E68:
        return {}
    kind = [0, 1, 255][vector % 3]
    mode = (vector // 3) % 3
    duration = [1, 3, 10, 30][(vector // 9) % 4]
    current = [-1, 0, 1, 2, duration - 11, duration - 10, duration - 3, duration - 2, duration, duration + 1][(vector // 36) % 10]
    scale = -4096 if (vector // 9) % 2 else 4096
    engine.mem_write(0x021DB2C8, struct.pack("<5i", kind, current, duration, scale, mode))
    fields = [0] * 12
    fields[1], fields[10] = 0x03007000, 0x0300D000
    engine.mem_write(0x021DA9DC, struct.pack("<12I", *fields))
    pointer = fields[1 if kind == 0 else 10]
    engine.mem_write(pointer + 124, struct.pack("<I", 0xA5A55A5A))
    before = {target: word(engine, target, 2 if target & 255 == 74 else 4) for target in [0x04000000, 0x0400004A, 0x04001000, 0x0400104A]}
    return {"kind": kind, "current": current, "duration": duration, "scale": scale, "mode": mode, "pointer": pointer, "before": before, "priorPair": bytes(engine.mem_read(pointer + 100, 8))}


def assert_transition(engine, address, calls, state):
    if not state:
        return
    kind, current, duration, mode = [state[name] for name in ["kind", "current", "duration", "mode"]]
    names = [call["name"] for call in calls]
    active = current <= duration
    finished = active and current + 1 > duration
    expected_names = []
    fade = "func_02041510" if kind == 0 else "func_02041538"
    if active:
        if current == 0 and mode == 1:
            expected_names.append(fade)
        divide = mode == 0 and current > 1 or mode != 0 and current <= duration - 3
        if divide:
            expected_names.append("func_02026144")
            numerator = state["scale"] * (current if mode == 0 else duration - current)
            value = abs(numerator) // duration * (-1 if numerator < 0 else 1)
        else:
            value = 0
        expected_names += ["func_ov007_021d9400", "func_02048a88"]
        if mode == 0 and current + 1 == duration - 10:
            expected_names.append(fade)
        if finished:
            expected_names.append("func_ov007_021d93ac")
            if mode == 1:
                expected_names.append("func_02041898" if kind == 0 else "func_020418b0")
        if bytes(engine.mem_read(state["pointer"] + 100, 8)) != struct.pack("<2I", value & 0xFFFFFFFF, value & 0xFFFFFFFF):
            raise ValueError("Executed signed division/field interpolation differs")
    elif bytes(engine.mem_read(state["pointer"] + 100, 8)) != state["priorPair"]:
        raise ValueError("Completed transition unexpectedly changed fields")
    expected_state = struct.pack("<5i", kind, current + int(active), duration, state["scale"], mode)
    if names != expected_names or bytes(engine.mem_read(0x021DB2C8, 20)) != expected_state:
        raise ValueError("Transition lifetime/fade/notification order differs")
    if word(engine, state["pointer"] + 124) != (0xA5A55A5A & ~2 if finished else 0xA5A55A5A):
        raise ValueError("Transition completion enable flag differs")
    expected_gpu = dict(state["before"])
    if finished:
        base = 0x04000000 if kind == 0 else 0x04001000
        expected_gpu[base] &= ~0xE000
        expected_gpu[base + 74] = expected_gpu[base + 74] & ~0x3F00 | 0x3F00
    if any(word(engine, target, 2 if target & 255 == 74 else 4) != value for target, value in expected_gpu.items()):
        raise ValueError("Transition completion display/blend register masks differ")
