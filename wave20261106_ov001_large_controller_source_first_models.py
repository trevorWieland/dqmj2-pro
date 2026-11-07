from wave20261106_arm7_wl_followon_source_receive_fixture import Plan, SP, STOP, OUT, p16, p32

OBJECTS = 0x02720000
CHILDREN = 0x02724000
RECORDS = 0x02730000


def word(value):
    return value & 0xffffffff


def signed(value, bits):
    return value - (1 << bits) if value & (1 << (bits - 1)) else value


def fixtures():
    result = []
    for entry in [0x02225c64, 0x02226190]:
        for n in range(64):
            result.append(dict(entry=entry, seed=n, mask=[0, 1, 2, 0x80000000, 0xffffffff][n % 5],
                               available=[[0, 0, 0], [1, 1, 1], [0xffffffff, 0x80000000, 2],
                                          [0, 3, 1], [1, 0, 0]][n % 5],
                               modes=[(n + i) % 3 for i in range(3)],
                               counts=[[0, 1, 3, 6][(n + i) % 4] for i in range(3)]))
    return result


def scenario(f, ordinal):
    record = f['entry'] == 0x02226190
    frame = 40 if record else 48
    p = Plan(ordinal, frame)
    p.buffers.clear()
    p.initial.clear()
    p.regions.clear()
    p.buffer(OUT, 32, 0xa5)
    p.buffer(OBJECTS, 3 * 0x440, 0x69)
    p.buffer(CHILDREN, 3 * 512, 0x78)
    p.buffer(RECORDS, 256 * 40, 0xb2)
    local = SP - frame
    p.buffer(local, 12, 0xa6)
    p.allowed.append((OUT, OUT + 12))
    p.args = [OUT, OBJECTS] + ([] if record else [f['mask']])
    p.constant(0x021c6748, p32(RECORDS))
    rows = []
    for index in range(256):
        flags = [0, 1, 2, 0x80000000, 0xffffffff][(index + f['seed']) % 5]
        value = [-32768, -1, 0, 1, 32767][(index * 3 + f['seed']) % 5]
        p.u32(RECORDS + 40 * index, flags)
        p.u16(RECORDS + 40 * index + 24, value)
        rows.append((flags, value))
    for i in range(3):
        obj = OBJECTS + i * 0x440
        child = CHILDREN + i * 512
        p.u32(obj + 0x1e8, child)
        p.write(obj + 0x322, bytes([f['modes'][i], f['counts'][i]]))
        child_values = [(f['seed'] * 3 + i * 7 + j * 5) % 256 for j in range(6)]
        own_values = [(f['seed'] * 5 + i * 3 + j * 7) % 256 for j in range(6)]
        if f['seed'] % 4 == 0:
            child_values = [255] * 6
            own_values = [0] * 6
        p.write(child + 8, bytes(child_values))
        p.write(obj + 0x35e, bytes(own_values))
        p.u32(OUT + 4 * i, f['available'][i])
    p.capture()
    values = list(f['available'])
    raw = p.read(OUT, 12)
    p.action(0x02008e0c, [OUT, local, 12], checks=[(OUT, raw)], mutations=[(local, raw)])
    p.write(local, raw)
    fields = []
    for i in range(3):
        if not values[i]:
            continue
        obj = OBJECTS + i * 0x440
        count = 6 if f['modes'][i] == 1 else f['counts'][i]
        for j in range(count):
            at = CHILDREN + i * 512 + 8 + j if f['modes'][i] == 1 else obj + 0x35e + j
            index = p.read(at, 1)[0]
            flags, value = rows[index]
            if record:
                p.action(0x0207afec, [index], RECORDS + 40 * index)
                fields.append((RECORDS + 40 * index + 24, 2, value & 65535))
                keep = value > 0
            else:
                keep = bool(flags & f['mask'])
                p.action(0x0207b004, [index, f['mask']], int(keep))
            if keep:
                break
            if j == count - 1:
                values[i] = 0
                p.u32(local + 4 * i, 0)
    result = sum(v != 0 for v in values)
    final = p.read(local, 12)
    p.action(0x02223f20, [local], result, checks=[(local, final)])
    if result:
        p.action(0x02008e0c, [local, OUT, 12], checks=[(local, final)], mutations=[(OUT, final)])
        p.write(OUT, final)
    p.returned = result
    plan = p.finish()
    plan.update(sramReads=[], sramWrites=[], sramFault='none', expectedMmioReads=[],
                faultRegisters=[], spiReadScript=[], instructionBudget=10000,
                expectedTableReads=[], expectedFlagReads=fields)
    return plan
