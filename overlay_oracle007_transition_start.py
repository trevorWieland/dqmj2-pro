import struct
from overlay_oracle007_transition import word


def f32(value):
    return struct.unpack("<f", struct.pack("<f", value))[0]


def parameters(vector):
    return {"y": vector % 256, "x": ((vector % 256) * 73 + 19) & 255, "kind": (vector // 256) % 2, "reverse": (vector // 512) % 2, "duration": [1, 3, 10, 30][vector % 4]}


def seed_transition_start(engine, address, vector):
    if address != 0x021D9CCC:
        return {}
    state = parameters(vector)
    fields = [0] * 12
    fields[1], fields[10] = 0x03007000, 0x0300D000
    engine.mem_write(0x021DA9DC, struct.pack("<12I", *fields))
    pointer = fields[1 if state["kind"] == 0 else 10]
    flags = word(engine, pointer + 124)
    engine.mem_write(0x021DB2C8, struct.pack("<I", 0xA5A5A500))
    engine.mem_write(0x0301FF00, struct.pack("<I", state["y"]))
    before = {target: word(engine, target, 2 if target & 255 == 74 else 4) for target in [0x04000000, 0x0400004A, 0x04001000, 0x0400104A]}
    state.update(pointer=pointer, flags=flags, before=before)
    return state


def transition_start_arguments(address, vector, args):
    if address == 0x021D9CCC:
        state = parameters(vector)
        args[:] = [state[key] for key in ["kind", "reverse", "duration", "x"]]


def assert_transition_start(engine, address, calls, state):
    if not state:
        return
    distance = min(256 - state["y"], state["y"] + 64)
    amount = int(f32(0.5 + f32(4096 * f32(distance / 80))))
    expected_state = struct.pack("<5I", 0xA5A5A500 | state["kind"], 0, state["duration"], amount, state["reverse"])
    if bytes(engine.mem_read(0x021DB2C8, 20)) != expected_state:
        raise ValueError("Float-derived transition amplitude/state differs")
    scale = amount if state["reverse"] else 0
    expected_pair = struct.pack("<4I", scale, scale, state["x"], state["y"])
    if bytes(engine.mem_read(state["pointer"] + 100, 16)) != expected_pair or word(engine, state["pointer"] + 124) != state["flags"] | 2:
        raise ValueError("Executed transition coordinate/scale/flag writers differ")
    expected_gpu = dict(state["before"])
    base = 0x04000000 if state["kind"] == 0 else 0x04001000
    expected_gpu[base] = expected_gpu[base] & ~0xE000 | 0x8000
    expected_gpu[base + 74] = (expected_gpu[base + 74] & ~0x3F3F) | 0x1F3F
    if any(word(engine, target, 2 if target & 255 == 74 else 4) != value for target, value in expected_gpu.items()):
        raise ValueError("Transition setup display/blend masks differ")
    expected_calls = ["func_ov007_021d93ac", "func_ov007_021d93dc", "func_02048a60", "_fflt", "_fdiv", "_fgr", "_fflt", "_fdiv", "_fmul", "_fadd", "_ffix", "func_ov007_021d9400", "func_02048a88"]
    if [call["name"] for call in calls] != expected_calls:
        raise ValueError("Transition setup runtime/helper order differs")
