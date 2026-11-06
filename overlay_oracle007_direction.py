import struct
from unicorn.arm_const import UC_ARM_REG_R0


def seed_direction(engine, address, vector):
    if address != 0x021D7E1C:
        return {}
    current = (vector // 4) % 16
    pattern = (vector // 64) % 5
    points = [(32 + index % 4 * 48, 24 + index // 4 * 40) for index in range(16)]
    enabled = [pattern in {0, 4} or pattern == 1 and index % 2 != 0 or pattern == 2 and index == current for index in range(16)]
    x, y = points[current]
    if pattern == 4:
        x, y = [(0, 0), (255, 191), (-1, 0), (0, -1), (256, 192), (128, 96), (80, 64), (0, 191)][current % 8]
    for index, (px, py) in enumerate(points):
        engine.mem_write(0x021DA5EC + index * 48, struct.pack("<2i", px, py))
        engine.mem_write(0x021DA614 + index * 48, bytes([enabled[index]]))
    engine.mem_write(0x021DA0F4, struct.pack("<3i", x, y, current))
    return {"points": points, "enabled": enabled, "origin": (x, y), "current": current}


def direction_arguments(address, vector, args):
    if address == 0x021D7E1C:
        args[0] = vector % 4 + 1


def closest(points, enabled, origin, current, direction):
    sx, sy = {1: (-1, -1), 2: (1, 1), 3: (-1, 1), 4: (1, -1)}[direction]
    ox, oy = origin
    candidates = [(abs(px - ox) + abs(py - oy), index) for index, (px, py) in enumerate(points) if enabled[index] and index != current and ((py + px) - (oy + ox)) * sx >= 0 and ((py - px) - (oy - ox)) * sy >= 0]
    return min(candidates)[1] if candidates else -1


def assert_direction(engine, address, args, calls, state):
    if not state:
        return
    origin, direction = state["origin"], args[0]
    expected = closest(state["points"], state["enabled"], origin, state["current"], direction)
    if expected == -1 and 0 <= origin[0] < 256 and 0 <= origin[1] < 192:
        dx, dy = {1: (0, 192), 2: (0, -192), 3: (256, 0), 4: (-256, 0)}[direction]
        expected = closest(state["points"], state["enabled"], (origin[0] + dx, origin[1] + dy), -1, direction)
    if engine.reg_read(UC_ARM_REG_R0) != expected & 0xFFFFFFFF:
        raise ValueError("Directional nearest/wrapped geometry differs")
    if bytes(engine.mem_read(0x021DA0F4, 12)) != struct.pack("<3i", *origin, state["current"]):
        raise ValueError("Directional recursive search did not restore its full selection state")
    if any(call["args"][0] not in range(16) for call in calls if call["name"] in {"func_ov007_021d8634", "func_ov007_021d864c", "func_ov007_021d873c"}):
        raise ValueError("Directional search read outside its sixteen-row table")
