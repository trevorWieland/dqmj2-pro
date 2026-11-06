import struct

CONTEXT, ACTOR_A, ACTOR_B = 0x02238D7C, 0x02350000, 0x02360000
HEIGHT_OLD, HEIGHT_NEW, GLOBAL_FLAG = 0x02370000, 0x02371000, 0x0222EC84
WORDS = [0, 1, 255, 256, 0x80000001, 0xFFFFFFFF]
HEIGHTS = [0, 4096, -1, -4096, 0x7FFFFFFF, -0x80000000]


def recipes():
    rows = []
    for phase in (0, 10, 100, 1, 255):
        for variant in range(16):
            rows.append(dict(phase=phase, blockedA=(1, 255, 128)[variant % 3] if variant & 1 else 0,
                blockedB=(1, 255, 128)[variant % 3] if variant & 2 else 0, side=variant % 4,
                gateReturn=(0, 1, 0xFFFFFFFF)[variant % 3], modeReturn=WORDS[variant % 6],
                flagAfter=255 if variant & 4 else 0, finish=bool(variant & 8), variant=variant))
    for index, word in enumerate(WORDS):
        for finish in (False, True):
            rows.append(dict(phase=0, blockedA=0, blockedB=0, side=(0, 1, 2, 255)[index % 4],
                gateReturn=0, modeReturn=word, flagAfter=255 if finish else 0, finish=finish, variant=index))
    for index, row in enumerate(rows):
        row.update(seed=0x146000 + index, slot=(0, 1, 2, 255)[index % 4],
            height=HEIGHTS[index % 6], heightAfter=HEIGHTS[(index + 1) % 6], field36=(0, 0x1234, 65535)[index % 3],
            field29=(0, 1, 255)[index % 3], flagBefore=0 if row['flagAfter'] else 1)
    return rows


def model(recipe):
    calls, writes = [], []
    phase = recipe['phase']

    def call(address, arguments, result=None, effects=(), probes=()):
        if result is None:
            result = (recipe['seed'] * 0x9E3779B9 + len(calls) * 0x654321) & 0xFFFFFFFF
        calls.append(dict(address=address, arguments=[v & 0xFFFFFFFF for v in arguments], returnWord=result,
            writes=list(effects), probes=list(probes)))
        writes.extend(effects)

    if phase == 0 and recipe['blockedA'] == 0 and recipe['blockedB'] == 0:
        call(0x021F949C, [0xDD if recipe['side'] == 0 else 0xE0, 1])
        call(0x021F14E4, [], recipe['gateReturn'])
        if recipe['gateReturn'] == 0:
            call(0x021EAA3C, [recipe['field36']], effects=[(GLOBAL_FLAG, bytes([recipe['flagAfter']]))])
            if recipe['flagAfter']:
                call(0x021F1438, [recipe['field29']])
        call(0x021E97C0, [], recipe['modeReturn'])
        narrowed = recipe['modeReturn'] & 255
        writes.append((CONTEXT + 10, bytes([narrowed])))
        call(0x021DB618, [ACTOR_A, ACTOR_B], probes=[(CONTEXT + 10, bytes([narrowed]))])
        call(0x021E9884, [narrowed])
        call(0x021D9494, [ACTOR_A, 1, 1])
        call(0x02202528, [recipe['side'], recipe['slot']])
        phase = 10
        writes.append((CONTEXT + 16, bytes([phase])))
    if phase == 10:
        result = ((recipe['heightAfter'] >> 12) + (5 if recipe['finish'] else 6)) & 0xFFFFFFFF
        call(0x021D9534, [ACTOR_A, -1, 1, 0], result, effects=[
            (ACTOR_A + 0x60, struct.pack('<I', HEIGHT_NEW)), (HEIGHT_NEW, struct.pack('<i', recipe['heightAfter']))])
        if recipe['finish']:
            phase = 100
            writes.append((CONTEXT + 16, bytes([phase])))
    if phase == 100:
        writes.extend([(CONTEXT + 16, b'\0'), (CONTEXT + 19, b'\5')])
    return calls, writes
