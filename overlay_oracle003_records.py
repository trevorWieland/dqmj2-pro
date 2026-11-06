import struct
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3
from overlay_oracle003_dispatch import INDIRECT_003, seed_dispatch003, dispatch_call003, assert_dispatch003, native_helpers_intro003

FUNCTIONS = {0x021D744C, 0x021D75C8, 0x021D790C}


def native_helpers003(address):
    if address==0x021DE27C:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12), "func_ov003_021dccc4": (0x021DCCC4, 16)}
    if address in {0x021DE09C,0x021DE0F0,0x021DE1B4,0x021DE378,0x021DE3D4,0x021DE4B8,0x021DE5B0}:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12), "func_ov003_021dada8": (0x021DADA8, 16)}
    if address==0x021DD6C4:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12), "func_02008e0c": (0x02008E0C, 304)}
    if address in {0x021DD8A4,0x021DD94C,0x021DDA30,0x021DDAD8,0x021DDBC0,0x021DDC68,0x021DDD4C,0x021DDDF4,0x021DDED8,0x021DDF80}:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12)}
    if address in {0x021DD074,0x021DD1B0,0x021DD22C,0x021DD28C,0x021DD5F4}:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12)}
    if address in {0x021DCD3C,0x021DCD84,0x021DCE68,0x021DCF60}:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12), "func_ov003_021dada8": (0x021DADA8, 16)}
    if address == 0x021DC52C:
        return {"func_02008c58": (0x02008C58, 76)}
    if address == 0x021DC6C0:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12)}
    if address in {0x021DC214,0x021DC258,0x021DC500}:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12)}
    if address == 0x021DBE4C:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12), "func_ov003_021dad1c": (0x021DAD1C, 128), "func_02008e0c": (0x02008E0C, 304)}
    if address == 0x021DBF68:
        return {"func_ov003_021dc138": (0x021DC138, 136), "func_ov003_021dc1c0": (0x021DC1C0, 40), "func_ov003_021dbed8": (0x021DBED8, 144), "func_02008d78": (0x02008D78, 148)}
    if address == 0x021DC060:
        return {"func_ov003_021dc138": (0x021DC138, 136), "func_ov003_021dc1c0": (0x021DC1C0, 40), "func_02008d78": (0x02008D78, 148)}
    if address == 0x021DC138:
        return {"func_02008d78": (0x02008D78, 148)}
    if address in {0x021DB9BC,0x021DBB18}:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12), "func_ov003_021dada8": (0x021DADA8, 16)}
    if address in {0x021DBA20,0x021DBBC4,0x021DBCA0,0x021DBD18}:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12)}
    if address == 0x021DBDEC:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12), "func_ov003_021dad1c": (0x021DAD1C, 128), "func_02008e0c": (0x02008E0C, 304)}
    if address == 0x021DA50C:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12)}
    if address == 0x021DB290:
        return {"func_02008d78": (0x02008D78, 148), "func_ov003_021db4a8": (0x021DB4A8, 212), "func_02008e0c": (0x02008E0C, 304)}
    if address == 0x021DB4A8:
        return {"func_02008e0c": (0x02008E0C, 304)}
    if address == 0x021DB6EC:
        return {"func_ov003_021db7fc": (0x021DB7FC, 108)}
    if address == 0x021DB868:
        return {"func_ov003_021db978": (0x021DB978, 68)}
    if address == 0x021DB57C:
        return {"func_ov003_021db6ec": (0x021DB6EC, 272), "func_ov003_021db868": (0x021DB868, 272), "func_ov003_021db7fc": (0x021DB7FC, 108), "func_ov003_021db978": (0x021DB978, 68)}
    if address == 0x021DB034:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12), "func_ov003_021db20c": (0x021DB20C, 60)}
    if address == 0x021DAD1C:
        return {"func_02008e0c": (0x02008E0C, 304)}
    if address in {0x021DAE50, 0x021DAF90}:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12)}
    if address == 0x021DADC4:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12), "func_ov003_021dada8": (0x021DADA8, 16)}
    if address == 0x021DAAC4:
        return {"func_ov003_021dac44": (0x021DAC44, 168), "func_02008e0c": (0x02008E0C, 304)}
    if address == 0x021DAC44:
        return {"func_02008e0c": (0x02008E0C, 304)}
    if address == 0x021DA3FC:
        return {"func_ov003_021dad9c": (0x021DAD9C, 12)}
    if address == 0x021D9BD0:
        return {"native_ov003_021d9bd0": (0x021D9BD0, 144)}
    if address == 0x021D87C8:
        return {"native_ov003_021d87c8": (0x021D87C8, 200)}
    return {"func_02008d78": (0x02008D78, 148)} if address == 0x021D744C else {"func_02008e0c": (0x02008E0C, 304)} if address == 0x021D75C8 else native_helpers_intro003(address)


def seed_records003(engine, address, vector):
    if address not in FUNCTIONS:
        return seed_dispatch003(engine, address, vector)
    state = {"pointers": [], "sources": [], "before": {}, "sourceBytes": {}, "mode": vector // 64 % 2, "alternate": [0, 255, 256, 0xFFFFFFFF][vector % 4], "vector": vector, "buffer": None}
    for group in range(2):
        pointers, sources = [], []
        for index in range(3):
            pointer, source = (0x03006000 if group == 0 else 0x03007000) + index * 256, (0x03008000 if group == 0 else 0x03009000) + index * 256
            engine.mem_write(source + 20, struct.pack("<I", 0x600 + index + group * 3))
            engine.mem_write(pointer + 24, struct.pack("<hB", [0, 1, -1, -32768, 32767, -2][(vector + index) % 6], [0, 127, 128, 255][(vector + index) % 4]))
            state["before"][pointer] = bytes(engine.mem_read(pointer, 132))
            state["sourceBytes"][source] = bytes(engine.mem_read(source, 132))
            pointers.append(pointer if vector & 1 << (index + group * 3) else 0)
            sources.append(source)
        state["pointers"].append(pointers)
        state["sources"].append(sources)
    state["slots"] = [(0x02001000 if state["mode"] else 0x02002000) + index * 16 for index in range(3)]
    return state


def records_call003(engine, address, name, value, state):
    if address not in FUNCTIONS:
        return dispatch_call003(address, name, value, state, engine)
    if not state:
        return value
    index = engine.reg_read(UC_ARM_REG_R0)
    if name in {"func_02062a50", "func_02062a88"}:
        return state["pointers"][int(name == "func_02062a88")][index]
    if name in {"func_020c35a0", "func_020c35d8"}:
        return state["sources"][int(name == "func_020c35d8")][index]
    if address == 0x021D744C:
        if name == "func_02062ad0":
            return state["mode"]
        if name == "func_02062aa0":
            return state["alternate"]
        if name in {"func_02062a78", "func_02062a68"}:
            return state["slots"][index]
        if name == "func_020c3790" and bytes(engine.mem_read(index, 12)) != struct.pack("<3I", *state["slots"]):
            raise ValueError("Overlay003 three-slot association array differs")
        if name == "func_020c386c" and bytes(engine.mem_read(index, 12)) != bytes(12):
            raise ValueError("Overlay003 executed native array clear differs")
    if address == 0x021D790C:
        if name == "func_0207b460":
            scalar = engine.reg_read(UC_ARM_REG_R0)
            payload = struct.pack("<2I", scalar, engine.reg_read(UC_ARM_REG_R1)) * 8
            state["buffer"] = payload
            engine.mem_write(engine.reg_read(UC_ARM_REG_R3), payload)
        if name in {"func_0207c2b8", "func_0207c3d8"}:
            if bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_R1), 64)) != state["buffer"]:
                raise ValueError("Overlay003 formatter output was not forwarded intact")
            return [0, 65535, 65536, 0xFFFFFFFF][(state["vector"] + (name == "func_0207c3d8")) % 4]
    return value


def assert_records003(engine, address, calls, state, args=None):
    if address not in FUNCTIONS:
        return assert_dispatch003(engine, address, calls, state, args)
    if not state:
        return
    expected = []
    after = {pointer: bytearray(data) for pointer, data in state["before"].items()}
    if address == 0x021D744C:
        expected += ["func_020c3528"]
        for getter, setter in [("func_02062a50", "func_020c357c"), ("func_02062a88", "func_020c35b4")]:
            expected += [getter, setter] * 3
        for group, getter in enumerate(["func_02062a50", "func_02062a88"]):
            for index, pointer in enumerate(state["pointers"][group]):
                expected.append(getter)
                if not pointer:
                    break
                after[pointer][49] = 0
        expected += ["func_02062ad0"] + (["func_02062a78"] if state["mode"] else ["func_02062a68"]) * 3
        expected += ["func_020c3790", "func_02062ad0" if state["mode"] else "func_02062aa0", "func_020c384c", "func_02008d78", "func_020c386c", "func_020c3928", "func_020c35ec", "func_020c360c", "func_020c362c", "func_020c364c", "func_020c366c", "func_020c368c"]
        mode_call = next(call for call in calls if call["name"] == "func_020c384c")
        if mode_call["args"][0] != (state["mode"] or state["alternate"] & 255):
            raise ValueError("Overlay003 branch-dependent byte mode differs")
    if address == 0x021D75C8:
        expected += ["func_020628b0", "func_02062980"] * 3
        for group, (source_getter, release, getter) in enumerate([("func_020c35a0", "func_02062850", "func_02062a50"), ("func_020c35d8", "func_02062904", "func_02062a88")]):
            for index, pointer in enumerate(state["pointers"][group]):
                expected += [source_getter, release, getter]
                if not pointer:
                    break
                expected += [source_getter, "func_02008e0c"]
                after[pointer][:] = state["sourceBytes"][state["sources"][group][index]]
        for call in calls:
            if call["name"] == "func_02008e0c" and call["args"][2] != 132:
                raise ValueError("Overlay003 record copy size differs")
    if address == 0x021D790C:
        for group, getter in enumerate(["func_02062a50", "func_02062a88"]):
            for index, pointer in enumerate(state["pointers"][group]):
                expected.append(getter)
                if pointer:
                    expected += ["func_0207b460", "func_0207c2b8", "func_0207c3d8"]
                    struct.pack_into("<2H", after[pointer], 36, *[[0, 65535, 65536, 0xFFFFFFFF][(state["vector"] + other) % 4] & 65535 for other in range(2)])
                    after[pointer][51] = 0
        for call in calls:
            if call["name"] == "func_0207b460":
                pointer = call["args"][2] - 122
                original = state["before"][pointer]
                expected_scalar = int.from_bytes(original[24:26], "little", signed=True) & 0xFFFFFFFF
                if call["args"][:2] != [expected_scalar, original[26]]:
                    raise ValueError("Overlay003 signed/byte formatter inputs differ")
    if [call["name"] for call in calls] != expected:
        raise ValueError("Overlay003 record loop/truncation/early-stop order differs")
    if any(bytes(engine.mem_read(pointer, 132)) != data for pointer, data in after.items()) or any(bytes(engine.mem_read(pointer, 132)) != data for pointer, data in state["sourceBytes"].items()):
        raise ValueError("Overlay003 complete record copy/field effects differ")
