from wave20261106_arm7_wl_followon_source_receive_fixture import Plan, SP, STOP, p32

STATE, TABLE, CACHE = 0x02242aac, 0x02242abc, 0x0222f1c8
ACTOR, OTHER = 0x02710000, 0x02711000


def fixtures():
    result = []
    for entry, states in [(0x02213da8, [0, 5, 10, 100, 1, 127, 128, 255]),
                          (0x02213ee0, [0, 5, 10, 20, 30, 1, 127, 128, 255])]:
        for state in states:
            for ready in [0, 2]:
                result.append(dict(entry=entry, state=state, ready=ready, counter=0))
        if entry == 0x02213da8:
            for cached in [0,127,128,255]:
                for mutate in [0,1]:
                    result.append(dict(entry=entry,state=10,ready=2,counter=0,saved=cached,initialCache=cached,mutate=mutate))
        if entry == 0x02213ee0:
            for state in [10, 30]:
                for counter in [0, 14, 15, 16, 29, 30, 31, 127, 128, 254, 255]:
                    result.append(dict(entry=entry, state=state, ready=0, counter=counter))
        for selector in [0, 1, 2, 3, 127]:
            for kind in [0x31, 0xff]:
                result.append(dict(entry=entry, state=5 if entry == 0x02213da8 else 20,
                                   ready=2, counter=0, selector=selector, kind=kind))
        for present, null, raw in [(0, False, 0), (0, True, 0), (1, False, 0),
                                   (1, False, 128), (1, False, 255), (1, False, 127)]:
            result.append(dict(entry=entry, state=0, ready=2, counter=0,
                               present=present, null=null, raw=raw))
    for number, f in enumerate(result):
        f.update(seed=number, mutate=f.get('mutate',number % 2), selector=f.get('selector', number % 4),
                 kind=f.get('kind', [0x30, 0x31, 0x80, 0xff][number % 4]),
                 raw=f.get('raw', 0), present=f.get('present', 1), null=f.get('null', False),
                 signedValue=[0x80, 0xff, 0, 0x7f][number % 4], saved=f.get('saved',[0, 1, 127, 255][number % 4]))
    return result


def scenario(f, ordinal):
    p = Plan(ordinal, 8)
    p.buffers.clear()
    p.initial.clear()
    p.regions.clear()
    for address, size, fill in [(STATE, 0x800, 0x69), (CACHE, 4, 0x95),
                                (ACTOR, 0x440, 0xa7), (OTHER, 0x440, 0xb9)]:
        p.buffer(address, size, fill)
        p.allowed.append((address, address + size))
    p.args = []
    p.write(STATE, bytes([f['selector'], 0x79, f['state'], f['counter']]))
    pointer = 0 if f['null'] else ACTOR
    p.u32(STATE + 4, pointer)
    p.write(ACTOR + 0x1e4, bytes([f['raw']]))
    p.write(OTHER + 0x1e4, bytes([f['raw']]))
    for index in range(128):
        p.write(TABLE + index * 12, bytes([0x30 if index & 1 else 0x31, f['signedValue']]))
    p.write(TABLE + f['selector'] * 12, bytes([f['kind'], f['signedValue']]))
    if 'initialCache' in f:
        p.write(CACHE,bytes([f['initialCache']]))
    p.capture()

    def actor():
        return int.from_bytes(p.read(STATE + 4, 4), 'little')

    def selector():
        return p.read(STATE, 1)[0]

    def field(first=True):
        raw = p.read(TABLE + selector() * 12 + (0 if first else 1), 1)[0]
        return raw if first or raw < 128 else raw - 256

    def action(address, args=None, returned=0, mutations=None):
        changes = mutations or []
        p.action(address, [a & 0xffffffff for a in (args or [])], returned, mutations=changes)
        for address, raw in changes:
            p.write(address, raw)

    def status():
        changes = [(STATE + 4, p32(OTHER))] if f['mutate'] and pointer else []
        action(0x021db8d0, [actor()], int(bool(pointer and f['present'])), changes)
        return bool(pointer and f['present'])

    def message():
        value = field()
        changes = []
        if f['mutate']:
            new_selector = (selector() + 1) % 4
            new_kind = 0x30 if value == 0x31 else 0x31
            changes = [(STATE, bytes([new_selector])), (TABLE + new_selector * 12, bytes([new_kind]))]
        action(0x021f1354, [11, 0, value, 1], mutations=changes)
        action(0x021f1438, [2])

    def counter():
        raw = (p.read(STATE + 3, 1)[0] + 1) & 255
        p.write(STATE + 3, bytes([raw]))
        return raw if raw < 128 else raw - 256

    state, returned = f['state'], 0
    if f['entry'] == 0x02213da8:
        if state == 0:
            if status():
                p.write(STATE + 2, b'\5')
            else:
                returned = 1
        elif state == 5:
            action(0x021f1294, [16, 2])
            message()
            action(0x021e9708, [int(field() == 0x31)])
            action(0x021e95d8, [0])
            action(0x021e9610, [0], f['saved'])
            p.write(CACHE, bytes([f['saved']]))
            p.write(STATE + 2, b'\12')
        elif state == 10:
            action(0x021ee410, returned=f['ready'])
            if f['ready']:
                changes = [(CACHE, bytes([f['saved']]))] if f['mutate'] else []
                action(0x021f14a4, mutations=changes)
                action(0x021e9610, [p.read(CACHE, 1)[0]])
                p.write(STATE + 2, b'\144')
        elif state == 100:
            action(0x021f1324)
            p.write(STATE + 2, b'\0')
            returned = 1
    else:
        if state == 0:
            if not status():
                returned = 1
            elif p.read(actor() + 0x1e4, 1)[0] == 0:
                p.write(STATE + 2, b'\5')
                action(0x021f1294, [16, 2])
                message()
        elif state == 5:
            changes = [(STATE + 4, p32(OTHER))] if f['mutate'] else []
            action(0x021d7e80, [actor()], mutations=changes)
            action(0x021d9494, [actor(), 4, 1])
            p.write(STATE + 2, b'\12')
            p.write(STATE + 3, b'\0')
        elif state == 10:
            if counter() > 30:
                p.write(STATE + 2, b'\24')
        elif state == 20:
            action(0x021dbf98, [actor(), field(False), 1, 0, 1])
            action(0x022142c0)
            action(0x021e2078)
            p.write(STATE + 2, b'\36')
            changes = [(STATE + 3, b'\177')] if f['mutate'] else []
            action(0x021f14a4, mutations=changes)
            p.write(STATE + 3, b'\0')
        elif state == 30:
            if counter() > 15:
                action(0x021f1324)
                p.write(STATE + 2, b'\0')
                returned = 1
    p.returned = returned
    result = p.finish()
    result.update(sramReads=[], sramWrites=[], sramFault='none', expectedMmioReads=[],
                  faultRegisters=[], spiReadScript=[], instructionBudget=1000,
                  expectedTableReads=[], expectedFlagReads=[])
    return result
