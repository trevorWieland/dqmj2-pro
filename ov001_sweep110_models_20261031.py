import struct

CONTEXT, LOOKUP, INFO = 0x0223E088, 0x02360000, 0x02370000


def recipes():
    rows = [dict(seed=0x210000 + i, phase=p, counter=c, variant=v)
        for i, (p, c, v) in enumerate((p, c, v) for p in (0, 10, 20, 30, 100, 255)
            for c in (0, 29, 30, 31, 254, 255) for v in range(8))]
    for i, row in enumerate(rows):
        row.update(side=(0, 1, 2, 3, 255)[i % 5], slot=(0, 1, 2, 3, 4, 255)[i % 6], nativeId=(0, 1, 47, 255)[i % 4])
    return rows


def construct(recipe, initial_context, pools):
    context = bytearray(initial_context)
    for offset, key in [(16, 'phase'), (15, 'counter'), (26, 'side'), (27, 'nativeId'), (28, 'slot')]:
        context[offset] = recipe[key]
    initial, actors, services = [(CONTEXT, bytes(context))], {}, []
    v = recipe['variant']
    for side, pool in enumerate(pools):
        for slot in range(3):
            pointer, record = pool + slot * 1088, INFO + (side * 3 + slot) * 256
            ready = 0 if v % 4 == 1 and slot == 1 or v % 4 == 3 and slot == 1 else (255 if v % 4 == 3 else 1)
            blocked = 1 if v % 4 == 2 and slot == 2 or v % 4 == 3 and slot == 0 else 0
            info_blocked = 255 if v % 4 == 2 and slot == 0 or v % 4 == 3 and slot == 2 else 0
            status = (v * 37 + slot * 127 + side) & 255
            actors[pointer] = dict(side=side, slot=slot, ready=ready, blocked=blocked, infoBlocked=info_blocked, status=status)
            initial += [(pointer + 0x31C, bytes([ready])), (pointer + 0x1FF, bytes([blocked])),
                (pointer + 0x1E8, struct.pack('<I', record)), (record + 0xAC, bytes([info_blocked])),
                (pointer + 0x234, bytes([status]))]

    def call(address, arguments, returned=0, writes=()):
        services.append(dict(address=address, arguments=arguments, result=returned, writes=list(writes)))
        for target, content in writes:
            if CONTEXT <= target < CONTEXT + len(context):
                context[target - CONTEXT:target - CONTEXT + len(content)] = content

    side, slot, native_id = recipe['side'], recipe['slot'], recipe['nativeId']
    pointer = pools[side] + slot * 1088 if side < 4 and slot < 3 else 0
    native_count = 3 + (slot != 4)
    if context[16] == 0:
        call(0x0220C3F4, [pointer, side, native_id], writes=[(CONTEXT + 15, bytes([250, 238])),
            (CONTEXT + 26, bytes([170, 187, 204]))])
        context[15], context[16] = 0, 10
    if context[16] == 10:
        context[15] = (context[15] + 1) & 255
        if context[15] > 30:
            context[16] = 20
    if context[16] == 20:
        code = 34 if v % 3 != 1 else 255
        call(0x02065D88, [native_id], LOOKUP, [(LOOKUP + 40, bytes([code])), (CONTEXT + 26, bytes([170, 187, 204]))])
        if code == 34:
            targets = [pointer] if pointer else [pools[side] + i * 1088 if side < 4 else 0 for i in range(3)]
            if not pointer:
                native_count += 6
            for target in targets:
                actor = actors.get(target)
                if not pointer and (not actor or not actor['ready'] or actor['blocked'] or actor['infoBlocked']):
                    continue
                status = actor['status']
                signed = status if status < 128 else status - 256
                writes = [(target + 0x234, b'\x5A'), (CONTEXT + 15, bytes([250, 238]))]
                actor['status'] = 90
                if actor['slot'] < 2:
                    following = pools[actor['side']] + (actor['slot'] + 1) * 1088
                    actors[following]['blocked'] = 1
                    writes.append((following + 0x1FF, b'\x01'))
                call(0x021EE91C, [target, signed & 0xFFFFFFFF], writes=writes)
            context[15], context[16] = 0, 30
        else:
            context[16] = 100
    if context[16] == 30:
        context[15] = (context[15] + 1) & 255
        if context[15] > 30:
            context[16] = 100
    if context[16] == 100:
        context[16], context[3] = 0, 14
    return initial, context, services, native_count
