import struct

POOL, GROUP, COPIES, CONTEXT = 0x021BD674, 0x021BD524, 0x02246C84, 0x022468B8


def recipes():
    return [dict(seed=0x137000 + value, variant=value, index=[0, 1, 2, 3, 0xFFFFFFFF, 0][value % 6], disabled=value % 6 == 5)
        for value in range(24)] + [dict(seed=0x137100, variant=0, index=0, disabled=False, descending=True)]


def construct(recipe, raw_pool, raw_copies, raw_context, raw_group):
    v, index = recipe['variant'], recipe['index']
    pool = [bytearray(raw_pool[i * 132:(i + 1) * 132]) for i in range(100)]
    uids = list(range(1, 101))
    uids[0], uids[49] = 0xFFFFFFFF, 0x80000000
    ordered = sorted(uids, reverse=bool(recipe.get('descending')))
    for i, record in enumerate(pool):
        struct.pack_into('<I', record, 20, ordered[i])
    target = [0xFFFFFFFF, 0x80000000, 7, 0][v // 6]
    others = [7, 8, 9]
    patterns = [[], [target], [others[0], target], [others[0], target, others[1]],
        [others[0], others[1], target], [target, target, others[0]], others]
    active = [uid for uid in patterns[v % 7] if uid]
    reserve = [uid for uid in patterns[(v * 3) % 7] if uid]
    group = bytearray(raw_group)
    struct.pack_into('<III', group, 28, *(active + [0] * (3 - len(active))))
    struct.pack_into('<III', group, 40, *(reserve + [0] * (3 - len(reserve))))
    copies, context = bytearray(raw_copies), bytearray(raw_context)
    if index < 3:
        struct.pack_into('<I', copies, index * 132 + 20, target)
        struct.pack_into('<H', copies, index * 132 + 24, 0 if recipe['disabled'] else [1, 0x8000, 0xFFFF][v % 3])
    initial = [(POOL, b''.join(pool)), (GROUP, bytes(group)), (COPIES, bytes(copies)), (CONTEXT, bytes(context))]
    if index >= 3 or recipe['disabled']:
        return initial, [], [], 0, None
    for values in [active, reserve]:
        if target in values:
            values.remove(target)
    struct.pack_into('<III', group, 28, *(active + [0] * (3 - len(active))))
    struct.pack_into('<III', group, 40, *(reserve + [0] * (3 - len(reserve))))
    if target:
        chosen = next(record for record in pool if struct.unpack_from('<I', record, 20)[0] == target)
        struct.pack_into('<I', chosen, 20, 0)
        pool.sort(key=lambda record: (struct.unpack_from('<I', record, 20)[0] == 0, struct.unpack_from('<I', record, 20)[0]))
    copies[index * 132:(index + 1) * 132] = bytes(132)
    before = (0, 127, 128, 255)[v % 4]
    after = (255, 128, 127, 0)[v % 4]
    services = [dict(address=0x02223D58, arguments=[0, index, 0], effects=[(CONTEXT + 29, bytes([before ^ 255]))]),
        dict(address=0x02223E40, arguments=[0, index, 1], effects=[(CONTEXT + 30, bytes([after ^ 255]))]),
        dict(address=0x021F51D4, arguments=[1], effects=[(CONTEXT + 29, bytes([before, after]))])]
    context[29:31] = bytes([(before - 1) & 255, (after + 1) & 255])
    expected = [(POOL, b''.join(pool)), (GROUP, bytes(group)), (COPIES, bytes(copies)), (CONTEXT, bytes(context))]
    return initial, expected, services, 1, COPIES + index * 132
