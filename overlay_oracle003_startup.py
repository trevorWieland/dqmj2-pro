import struct
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP
from overlay_oracle003_records import native_helpers003, seed_records003, records_call003, assert_records003, INDIRECT_003
from overlay_oracle003_icons import icon_arguments003
from overlay_oracle003_cells import cell_arguments003
from overlay_oracle003_shared_render import render_arguments003
from overlay_oracle003_main_resources import main_resources_arguments003
from overlay_oracle003_main_dispatch import MAIN_INDIRECT_003
from overlay_oracle003_mode3_network import mode3_network_arguments003
from overlay_oracle003_mode7_setup import mode7_setup_arguments003

FUNCTIONS = {0x021D7240, 0x021D73E4, 0x021D7694, 0x021D770C, 0x021D7724, 0x021D7868, 0x021D7878, 0x021D7888}
COUNTS_003 = {0x021D7888: 64, 0x021D744C: 128, 0x021D75C8: 64, 0x021D790C: 64, 0x021D72D0: 108, 0x021D7AFC: 784, 0x021D7EE8: 512, 0x021D7FF0: 384, 0x021D8348: 1800, 0x021D85E4: 2000, 0x021D867C: 16, 0x021D87C8: 675, 0x021D88E8: 192, 0x021D89D8: 624, 0x021D8CAC: 128, 0x021D8CE8: 64, 0x021D8DDC: 576, 0x021D8FF4: 576, 0x021D91F8: 576, 0x021D93FC: 576, 0x021D9634: 432, 0x021D97A4: 48, 0x021D97F8: 800, 0x021D9984: 432, 0x021D9BD0: 540, 0x021D9CB8: 128, 0x021D9D84: 128, 0x021D9DC0: 64, 0x021D9E80: 48, 0x021DA01C: 24, 0x021DA178: 168, 0x021DA3FC: 108, 0x021DA86C: 6, 0x021DAAC4: 64, 0x021DAC44: 84, 0x021DAD1C: 84, 0x021DADC4: 6, 0x021DAE50: 144, 0x021DAF90: 64, 0x021DB034: 1080, 0x021DB20C: 12, 0x021DB248: 114, 0x021DB7FC: 384, 0x021DB978: 96, 0x021DB6EC: 188, 0x021DB868: 188, 0x021DB57C: 552, 0x021DB4A8: 40, 0x021DB290: 192, 0x021DA50C: 2121, 0x021DB9BC: 7, 0x021DBA20: 48, 0x021DBAE4: 6, 0x021DBB18: 21, 0x021DBBC4: 180, 0x021DBCA0: 12, 0x021DBD18: 144, 0x021DBDEC: 65, 0x021DBE4C: 65, 0x021DBED8: 28, 0x021DBF68: 960, 0x021DC060: 800, 0x021DC138: 16, 0x021DC1C0: 6, 0x021DC1E8: 16, 0x021DC214: 12, 0x021DC258: 1620, 0x021DC500: 12, 0x021DC52C: 104, 0x021DC6C0: 773, 0x021DCAEC: 405, 0x021DCBC4: 324, 0x021DCC8C: 8, 0x021DCCC4: 9, 0x021DCCD4: 256, 0x021DCD3C: 16, 0x021DCD84: 128, 0x021DCE34: 8, 0x021DCE68: 32, 0x021DCF60: 192, 0x021DD074: 24, 0x021DD19C: 12, 0x021DD1B0: 168, 0x021DD22C: 16, 0x021DD28C: 64, 0x021DD5F4: 64, 0x021DD6C4: 160, 0x021DD8A4: 64, 0x021DD94C: 160, 0x021DDA30: 64, 0x021DDAD8: 160, 0x021DDBC0: 64, 0x021DDC68: 160, 0x021DDD4C: 64, 0x021DDDF4: 160, 0x021DDED8: 64, 0x021DDF80: 160, 0x021DE064: 8, 0x021DE09C: 16, 0x021DE0F0: 128, 0x021DE180: 8, 0x021DE1B4: 32, 0x021DE27C: 224, 0x021DE378: 16, 0x021DE3D4: 128, 0x021DE484: 8, 0x021DE4B8: 32, 0x021DE5B0: 224}


def word(engine, address, width=4):
    return int.from_bytes(engine.mem_read(address, width), "little")


def seed_startup003(engine, address, vector):
    if address not in FUNCTIONS:
        return seed_records003(engine, address, vector)
    before = bytearray((vector + index * 17) & 255 for index in range(64))
    before[0] = [0, 127, 128, 255][vector % 4]
    before[4] = [0, 1, 127, 128, 255][vector % 5]
    engine.mem_write(0x021E0440, bytes(before))
    gpu = {target: word(engine, target, 2 if target in range(0x04000008, 0x04000010, 2) else 4) for target in [0x04000000, 0x04000008, 0x0400000A, 0x0400000C, 0x0400000E, 0x0400001C]}
    return {"before": before, "gpu": gpu, "mode": vector % 3, "identifier": [0, 127, 128, 255, 256, 0xFFFFFFFF][vector % 6], "handle": 0x0300F000 + vector * 32, "vector": vector}


def startup_arguments003(address, vector, args):
    icon_arguments003(address, vector, args)
    cell_arguments003(address, vector, args)
    render_arguments003(address, vector, args)
    main_resources_arguments003(address, vector, args)
    mode3_network_arguments003(address, vector, args)
    mode7_setup_arguments003(address, vector, args)
    if address == 0x021D7878:
        args[0] = [0, 255, 256, 65535, 0x80000000, 0xFFFFFFFF][vector % 6]


def startup_call003(engine, address, name, value, state):
    if address not in FUNCTIONS:
        return records_call003(engine, address, name, value, state)
    if not state:
        return value
    if address == 0x021D7240 and name == "func_0202a1e0":
        return state["identifier"]
    if address == 0x021D7240 and name == "func_02027400":
        return state["mode"]
    if address == 0x021D7694:
        if name == "func_0205db90":
            pointer = engine.reg_read(UC_ARM_REG_R0)
            if bytes(engine.mem_read(pointer, 32)) != bytes(32) or engine.reg_read(UC_ARM_REG_R1) != 0x021E0220 or engine.reg_read(UC_ARM_REG_R2) != 0xFFFFFFFF:
                raise ValueError("Overlay003 resource formatting did not receive its complete zeroed buffer")
            engine.mem_write(pointer, b"private-fixture\0")
        if name == "func_0205d9e8":
            arguments = [engine.reg_read(register) for register in [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3]]
            if arguments[0] != 2 or arguments[2:] != [0x021E0210, 0x021E020C] or bytes(engine.mem_read(arguments[1], 16)) != b"private-fixture\0" or word(engine, engine.reg_read(UC_ARM_REG_SP)) != 2:
                raise ValueError("Overlay003 resource handle arguments/formatted buffer differ")
            return state["handle"]
    if address == 0x021D7888 and name in {"func_020c3704", "func_020c3770"}:
        index = engine.reg_read(UC_ARM_REG_R0)
        bit = index + (3 if name == "func_020c3770" else 0)
        return (0x03008000 if bit >= 3 else 0x03006000) + index * 256 if state["vector"] & 1 << bit else 0
    return value


def assert_startup003(engine, address, args, calls, state):
    if address not in FUNCTIONS:
        return assert_records003(engine, address, calls, state, args)
    if not state:
        return
    after = bytearray(state["before"])
    if address == 0x021D7240:
        after[:5] = bytes([state["identifier"] & 255, 0, 0, 3, 3])
        expected = ["func_0202a090"] * 2 + ["func_0202a1e0", "func_ov003_021d7694", "func_ov003_021d7724", "func_0207a9ec", "func_020c39d0", "func_ov003_021d790c", "func_02027400"]
        if state["mode"] == 1:
            expected += ["func_ov003_021d744c"]
        else:
            expected += ["func_02027400"] + (["func_ov003_021d7888"] if state["mode"] == 2 else [])
        if [call["name"] for call in calls] != expected or [call["args"][:2] for call in calls[:2]] != [[1, 0x50000], [2, 0x29800]]:
            raise ValueError("Overlay003 startup branch/heap/state differs")
    if address == 0x021D73E4:
        expected = ["func_020c39d0", "func_020c3a10", "func_0204617c", "func_02084920", "func_ov003_021d770c", "func_ov003_021d8ce8", "func_ov003_021d9dc0", "func_02061898", "func_020406a8", "func_0207aad0", "func_0202a1e0", "func_0202a164", "func_0202a164"]
        signed = int.from_bytes(bytes([state["before"][0]]), "little", signed=True) & 0xFFFFFFFF
        if [call["name"] for call in calls] != expected or calls[10]["args"][0] != signed or [call["args"][0] for call in calls[-2:]] != [2, 1]:
            raise ValueError("Overlay003 teardown signed heap identity/order differs")
    if address == 0x021D7694:
        struct.pack_into("<I", after, 16, state["handle"])
        if [call["name"] for call in calls] != ["func_0205db90", "func_0205d9e8"]:
            raise ValueError("Overlay003 resource initialization order differs")
    if address == 0x021D770C and (len(calls) != 1 or calls[0]["args"][:2] != [2, 0x021E0450]):
        raise ValueError("Overlay003 resource release forwarding differs")
    if address == 0x021D7868 and engine.reg_read(UC_ARM_REG_R0) != int.from_bytes(bytes([after[4]]), "little", signed=True) & 0xFFFFFFFF:
        raise ValueError("Overlay003 signed flag getter differs")
    if address == 0x021D7878:
        after[4] = args[0] & 255
    if address == 0x021D7724:
        expected_gpu = dict(state["gpu"])
        expected_gpu[0x04000000] = (((expected_gpu[0x04000000] & 0xFFCFFFEF) | 0x10) & ~0x1F00 | 0x1F00) & ~0xE000
        expected_gpu[0x0400001C] = 0
        for index, mode, priority in [(0, 0x318, 2), (1, 0x108, 0), (2, 0x210, 1), (3, 0x4884, 3)]:
            target = 0x04000008 + index * 2
            expected_gpu[target] = ((expected_gpu[target] & 0x43) | mode) & ~3 | priority
        if any(word(engine, target, 2 if target in range(0x04000008, 0x04000010, 2) else 4) != value for target, value in expected_gpu.items()):
            raise ValueError("Overlay003 display/mode/priority/scroll masks differ")
        clear = next(call for call in calls if call["name"] == "func_02008c58")
        if clear["args"][:3] != [0, 0x06000000, 0x80000] or calls[-1]["args"][:3] != [0, 0, 2]:
            raise ValueError("Overlay003 display clear/setup arguments differ")
    if address == 0x021D7888:
        expected = [("func_020628b0", 0), ("func_02062980", 0)] * 3
        for group, getter, release in [(0, "func_020c3704", "func_02062850"), (1, "func_020c3770", "func_02062904")]:
            for index in range(3):
                expected.append((getter, index))
                if state["vector"] & 1 << (index + group * 3):
                    expected.append((release, (0x03006000 if group == 0 else 0x03008000) + index * 256))
        if [(call["name"], call["args"][0]) for call in calls] != expected:
            raise ValueError("Overlay003 six optional object releases differ")
    if bytes(engine.mem_read(0x021E0440, 64)) != after:
        raise ValueError("Overlay003 startup local state/byte truncation differs")
