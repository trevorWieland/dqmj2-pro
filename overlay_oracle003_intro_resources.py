import struct
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1
from overlay_oracle003_menu import seed_menu003, menu_call003, assert_menu003

FUNCTIONS = {0x021D7C98, 0x021D7E04, 0x021D7EE8}


def word(engine, address, width=4):
    return int.from_bytes(engine.mem_read(address, width), "little")


def string(engine, address):
    return bytes(engine.mem_read(address, 32)).split(b"\0", 1)[0]


def seed_intro_resources003(engine, address, vector):
    if address not in FUNCTIONS:
        return seed_menu003(engine, address, vector)
    before = bytearray((vector + index * 31) & 255 for index in range(64))
    before[20] = vector % 256
    old_handle = 0x0300D000 + vector * 8
    struct.pack_into("<I", before, 24, old_handle)
    engine.mem_write(0x021E0440, bytes(before))
    success = vector // 256 % 2 if address == 0x021D7EE8 else vector // 4 % 2
    handle = 0x0300F000 + vector * 8 if success else 0
    mode = [0, 5, 1, 0xFFFFFFFF][vector % 4]
    filename = (b"you_win.d16" if mode == 0 else b"you_draw.d16" if mode == 5 else b"you_lose.d16") if address == 0x021D7C98 else b"vs_start_1.d16" if address == 0x021D7E04 else b"vs_start_2.d16"
    gpu = {target: word(engine, target, 4 if target == 0x04000000 else 2) for target in [0x04000000, 0x04000040, 0x04000044, 0x04000048, 0x0400004A]}
    return {"before": before, "oldHandle": old_handle, "handle": handle, "mode": mode, "filename": filename, "gpu": gpu}


def intro_resources_call003(engine, address, name, value, state):
    if address not in FUNCTIONS:
        return menu_call003(engine, address, name, value, state)
    if not state:
        return value
    if name == "func_020653d0":
        return state["mode"]
    if name == "func_0201d444":
        template = string(engine, engine.reg_read(UC_ARM_REG_R1))
        if template != state["filename"]:
            raise ValueError("Overlay003 intro resource branch selected the wrong filename")
        engine.mem_write(engine.reg_read(UC_ARM_REG_R0), template + b"\0")
        return len(template)
    if name == "func_020bb338":
        if string(engine, engine.reg_read(UC_ARM_REG_R0)) != state["filename"] or engine.reg_read(UC_ARM_REG_R1) != 1:
            raise ValueError("Overlay003 intro resource open filename/heap differs")
        return state["handle"]
    return value


def assert_intro_resources003(engine, address, calls, state, args=None):
    if address not in FUNCTIONS:
        return assert_menu003(engine, address, args, calls, state)
    if not state:
        return
    after = bytearray(state["before"])
    expected = []
    result = None
    gpu = dict(state["gpu"])
    if address in {0x021D7C98, 0x021D7E04}:
        if address == 0x021D7C98:
            expected += ["func_020653d0"]
        expected += ["func_0201d444", "func_020bb338"]
        if state["handle"]:
            expected += ["func_020bb3cc"]
        expected += ["func_020414b0", "func_02041510", "func_020456ac"]
        struct.pack_into("<I", after, 24, state["handle"])
        gpu[0x04000000] = ((gpu[0x04000000] & ~0x1F00) | 0xA00) & ~0xE000 | 0x2000
        gpu[0x04000040], gpu[0x04000044] = 255, 5311
        gpu[0x04000048] = gpu[0x04000048] & ~0x3F | 0x28
        gpu[0x0400004A] = gpu[0x0400004A] & ~0x3F | 0x2A
        setup = calls[-1]
        if setup["args"] != [0, 1, 0, 4] or bytes.fromhex(setup["stack"])[:8] != struct.pack("<2I", 32, 24):
            raise ValueError("Overlay003 intro display setup register/stack arguments differ")
        if address == 0x021D7E04:
            after[20], result = 40, 1
    elif address == 0x021D7EE8:
        after[20] = (after[20] - 1) & 255
        result = int(after[20] == 0)
        if result:
            expected += ["func_0201d444", "func_020bb38c", "func_020bb338"]
            if state["handle"]:
                expected += ["func_020bb3cc"]
            expected += ["func_0205e7a8", "func_0205e814"]
            struct.pack_into("<I", after, 24, state["handle"])
            after[20] = 40
            if calls[1]["args"][:2] != [state["oldHandle"], 1] or calls[-2]["args"][:2] != [0xFFFFFFFF, 147] or calls[-1]["args"][:3] != [0, 0, 30]:
                raise ValueError("Overlay003 intro resource replacement/sound arguments differ")
    if [call["name"] for call in calls] != expected or result is not None and engine.reg_read(UC_ARM_REG_R0) != result:
        raise ValueError("Overlay003 intro resource countdown/open/start order differs")
    if bytes(engine.mem_read(0x021E0440, 64)) != after or any(word(engine, target, 4 if target == 0x04000000 else 2) != value for target, value in gpu.items()):
        raise ValueError("Overlay003 intro resource handle/countdown/window/blend state differs")
