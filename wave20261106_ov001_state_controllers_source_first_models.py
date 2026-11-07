from wave20261106_arm7_wl_followon_source_receive_fixture import Plan, SP, STOP, p32

ACTOR, OTHER, CHILD, OTHER_CHILD = 0x02710000, 0x02711000, 0x02720000, 0x02721000
CONFIG = {
    0x021ddd80: (0x022388ec, 2, 13, [0, 10, 100], [10], None),
    0x021df808: (0x022388ec, 46, 45, [0, 10, 100], [10], 72),
    0x021edd10: (0x02238d7c, 35, 17, [0, 10, 20, 30, 100], [10, 30], 96),
    0x021f8c50: (0x0223989c, 30, 29, [0, 10, 20, 30, 100], [30], 132),
    0x022146d4: (0x02242b50, 9, 8, [0, 2, 5, 10, 20, 30, 100], [2, 30], 16),
    0x02214e68: (0x02242b94, 0, 2, [0, 10, 20, 30, 100], [30], 8),
    0x02216460: (0x02242ba0, 1, 0, [0, 5, 10, 20, 100], [10], None),
    0x0221671c: (0x02242be8, 2, 3, [0, 10, 100], [10], 8),
}


def fixtures():
    result = []
    for entry, (_, _, _, states, counters, _) in CONFIG.items():
        for state in states + [1, 127, 128, 255]:
            for ready in [0, 2]:
                result.append(dict(entry=entry, state=state, counter=0, ready=ready))
        for state in counters:
            for counter in [28, 29, 30, 31, 39, 40, 41, 44, 45, 46, 59, 60, 61, 127, 128, 254, 255]:
                result.append(dict(entry=entry, state=state, counter=counter, ready=2))
        if entry == 0x021ddd80:
            for mode in [0, 1, 2, 0xffffffff]:
                result.append(dict(entry=entry, state=100, counter=45, ready=2, mode=mode))
        if entry in [0x021edd10,0x0221671c]:
            for halfword in [0,127,128,256,32768,65535]:
                result.append(dict(entry=entry,state=0,counter=0,ready=2,halfword=halfword))
        if entry == 0x02214e68:
            result.append(dict(entry=entry, state=20, counter=0, ready=1))
    for ordinal, f in enumerate(result):
        f.update(seed=ordinal, mutate=ordinal % 2, selector=[0, 1, 2, 255][ordinal % 4],
                 otherSelector=[255, 2, 1, 0][ordinal % 4],
                 mode=f.get('mode', [0, 1, 2][ordinal % 3]),
                 payload=0xa1b20000 + ordinal, halfword=f.get('halfword',[0, 127, 128, 65535][ordinal % 4]))
    return result


def signed_byte(value):
    return value - 256 if value & 128 else value


def scenario(f, ordinal):
    entry = f['entry']
    state_address, state_offset, counter_offset, _, _, actor_offset = CONFIG[entry]
    p = Plan(ordinal, 8)
    p.buffers.clear()
    p.initial.clear()
    p.regions.clear()
    for address, size, fill in [(state_address, 256, 0x79), (ACTOR, 0x440, 0xa3),
                                (OTHER, 0x440, 0xb7), (CHILD, 256, 0xc5), (OTHER_CHILD, 256, 0xd9)]:
        p.buffer(address, size, fill)
        p.allowed.append((address, address + size))
    p.args = [f['payload']] if entry in [0x021edd10, 0x021f8c50, 0x022146d4] else []
    p.write(state_address + state_offset, bytes([f['state']]))
    p.write(state_address + counter_offset, bytes([f['counter']]))
    p.u32(ACTOR + 0x1e8, CHILD)
    p.u32(OTHER + 0x1e8, OTHER_CHILD)
    p.write(ACTOR + 0x31e, bytes([f['selector'], 0x80]))
    p.write(OTHER + 0x31e, bytes([f['otherSelector'], 0xff]))
    if actor_offset is not None:
        p.u32(state_address + actor_offset, ACTOR)
    if entry == 0x021edd10:
        p.write(state_address + 0x36, f['halfword'].to_bytes(2, 'little'))
    if entry == 0x0221671c:
        p.write(state_address + 4, f['halfword'].to_bytes(2, 'little'))
    p.capture()
    returned = 0

    def put(offset, value):
        p.write(state_address + offset, bytes([value & 255]))

    def word(offset):
        return int.from_bytes(p.read(state_address + offset, 4), 'little')

    def actor():
        return word(actor_offset)

    def action(address, args=None, result=0, mutations=None):
        mutations = mutations or []
        p.action(address, args or [], result & 0xffffffff, mutations=mutations)
        for address, raw in mutations:
            p.write(address, raw)

    def mapping():
        selector = p.read(actor() + 0x31e, 1)[0]
        mapped = selector if selector < 2 else 2
        action(0x021f1414, [selector], mapped)
        action(0x021f1438, [mapped], 0xd00d0000 + mapped)

    def borrow():
        changes = [(state_address + actor_offset, p32(OTHER))] if f['mutate'] else []
        action(0x021d7e80, [actor()], 0x51510000, changes)

    def counter(signed=False):
        raw = (p.read(state_address + counter_offset, 1)[0] + 1) & 255
        put(counter_offset, raw)
        return signed_byte(raw) if signed else raw

    state = f['state']
    if entry == 0x021ddd80:
        action(0x02044554, result=f['mode'])
        if state == 0:
            action(0x021d7e30, [1])
            action(0x021f1294, [16, 2])
            action(0x021d94cc, [0, 1])
            action(0x021f1354, [1, 0, 6 if f['mode'] == 1 else 7, 1])
            put(2, 10)
            put(13, 0)
        elif state == 10:
            if counter() >= 30:
                action(0x021f14a4)
                put(2, 100)
        elif state == 100:
            action(0x021f14e4, result=f['ready'])
            if f['ready']:
                if f['mode'] == 1:
                    put(8, 1)
                    put(7, 1)
                else:
                    action(0x021e7fa8)
                    put(8, 3)
                    put(27, 1)
                action(0x021f1324)
                put(2, 0)
                action(0x021d7e30, [0])
                returned = 1
    elif entry == 0x021df808:
        if state == 0:
            borrow()
            action(0x021f1294, [16, 2])
            action(0x021f1354, [1, 0, 0x38, 1])
            action(0x021f1438, [p.read(actor() + 0x31e, 1)[0]])
            put(45, 0)
            put(46, 10)
        elif state == 10:
            if counter(True) >= 30:
                put(46, 100)
                action(0x021f14a4)
        elif state == 100:
            action(0x021f1324)
            put(8, 15)
            put(46, 0)
            returned = 1
    elif entry == 0x021edd10:
        if state == 0:
            borrow()
            action(0x021eaa3c, [f['halfword']])
            mapping()
            put(35, 10)
            put(17, 0)
        elif state == 10:
            if counter() >= 30:
                action(0x021eaa88, [f['halfword']])
                put(35, 20)
        elif state == 20:
            action(0x021f14e4, result=f['ready'])
            if not f['ready']:
                action(0x021f1354, [1, 0, f['payload'], 1])
                put(35, 30)
                put(17, 0)
        elif state == 30:
            if counter() >= 30:
                action(0x021f14a4)
                put(35, 100)
        elif state == 100:
            action(0x021f14e4, result=f['ready'])
            if not f['ready']:
                put(19, 19)
                put(35, 0)
    elif entry in [0x021f8c50, 0x022146d4]:
        if state == 0:
            if entry == 0x021f8c50:
                action(0x021f1324)
                put(state_offset, 10)
            else:
                put(counter_offset, 0)
                put(state_offset, 2)
        elif state == 2 and entry == 0x022146d4:
            if counter() > 30:
                put(state_offset, 5)
        elif state == 5 and entry == 0x022146d4:
            action(0x021f1324)
            put(state_offset, 10)
        elif state == 10:
            action(0x021f1294, [16, 2])
            if entry == 0x021f8c50:
                borrow()
            put(state_offset, 20)
        elif state == 20:
            action(0x021f1354, [1, 0, f['payload'], 1])
            mapping()
            put(state_offset, 30)
            put(counter_offset, 0)
        if p.read(state_address + state_offset, 1)[0] == 30:
            if counter() > 45:
                put(state_offset, 100)
        if p.read(state_address + state_offset, 1)[0] == 100:
            put(state_offset, 0)
            action(0x021f14a4)
            put(27 if entry == 0x021f8c50 else 2, 27 if entry == 0x021f8c50 else 5)
    elif entry == 0x02214e68:
        if state == 0:
            action(0x021f90b4, result=f['ready'])
            if f['ready']:
                put(0, 10)
        elif state == 10:
            action(0x020414b0, [1])
            action(0x02041510, [1, 2, 60])
            put(0, 20)
        elif state == 20:
            action(0x02041800, result=f['ready'])
            if f['ready'] != 1:
                action(0x020414b0, [63])
                action(0x021f1294, [16, 2])
                action(0x021f1354, [1, 0, 34, 1])
                child = int.from_bytes(p.read(actor() + 0x1e8, 4), 'little')
                action(0x02048034, [child + 0xb2, 0])
                put(0, 30)
                put(2, 0)
        elif state == 30:
            if counter(True) >= 60:
                action(0x021f14a4)
                put(0, 100)
        elif state == 100:
            action(0x021f14e4, result=f['ready'])
            if f['ready']:
                action(0x021f1324)
                put(0, 0)
                put(3, 4)
                put(1, 1)
                returned = 1
    elif entry == 0x02216460:
        if state == 0:
            action(0x021f1354, [1, 0, 33, 1])
            action(0x021f1414, [1], 1)
            action(0x021f1438, [1])
            action(0x021d7f54, [1])
            put(1, 5)
        elif state == 5:
            action(0x02041898, [0])
            put(1, 10)
            put(0, 0)
        elif state == 10:
            if counter() >= 30:
                put(1, 100)
        elif state == 20:
            action(0x021f14a4)
            put(1, 100)
        elif state == 100:
            action(0x021f14e4, result=f['ready'])
            if f['ready']:
                p.u32(state_address + 8, 4)
                put(1, 0)
            returned = 1
    elif entry == 0x0221671c:
        if state == 0:
            borrow()
            p.write(actor() + 0x325, b'\1')
            action(0x022025a4, list(p.read(actor() + 0x31e, 2)))
            action(0x021f1354, [7, 0, f['halfword'], 1])
            mapping()
            put(2, 10)
            put(3, 0)
        elif state == 10:
            if counter() >= 40:
                put(2, 100)
        elif state == 100:
            action(0x021f14a4)
            put(2, 0)
            put(1, 3)
    p.returned = returned
    result = p.finish()
    result.update(sramReads=[], sramWrites=[], sramFault='none', expectedMmioReads=[],
                  faultRegisters=[], spiReadScript=[], instructionBudget=1000,
                  expectedTableReads=[], expectedFlagReads=[])
    return result
