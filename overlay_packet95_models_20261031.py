import struct

ACTOR, RECORD, FLAG = 0x02350000, 0x02360000, 0x02238D92
WIDE = [0, 1, 0x80000000, 0xFFFFFFFF]


def recipes(kind):
    if kind == 'gate':
        return [dict(seed=0x195000 + i, id=native_id, field244=a, field22D=b, variant=v)
            for i, (native_id, a, b, v) in enumerate((native_id, a, b, v) for native_id in (0x77, 0xD9, 0, 1, 256, 0xFFFFFFFF)
                for a in (0, 1, 128) for b in (0, 1) for v in range(16))]
    return [dict(seed=0x295000 + v, variant=v, argument=WIDE[v % 4]) for v in range(64)]


def model(kind, recipe):
    services, initial, final = [], [], []

    def call(address, arguments, result, writes=()):
        services.append(dict(address=address, arguments=arguments, result=result, writes=list(writes)))

    v = recipe['variant']
    if kind == 'gate':
        native_id = recipe['id']
        initial = [(ACTOR + 0x244, bytes([recipe['field244']])), (ACTOR + 0x22D, bytes([recipe['field22D']])),
            (ACTOR + 0x31E, b'\xFE'), (ACTOR + 0x1FD, b'\xA5'), (FLAG, b'\xF0')]
        arguments = [ACTOR, native_id]
        result = 0
        if recipe['field244'] and native_id != 0xD9:
            return initial, services, final, arguments, result
        if native_id == 0x77:
            call(0x02210AD0, [ACTOR, 2, 1], WIDE[v % 4])
            return initial, services, final, arguments, WIDE[v % 4]
        intercepted = v in (1, 7, 15)
        after22d = recipe['field22D'] if v < 8 else 0
        call(0x0220F098, [ACTOR, native_id], 0xFFFFFFFF if intercepted else 0, [(ACTOR + 0x22D, bytes([after22d]))])
        if intercepted:
            result = WIDE[v % 4]
            call(0x0220F0CC, [ACTOR, native_id], result)
        elif after22d and native_id != 0xD9:
            pass
        elif native_id == 0xD9:
            result = 1
        else:
            predicate, flag = (0 if v in (2, 10) else 32), (1 if v in (3, 11) else 0)
            call(0x0207B004, [native_id, 32], predicate, [(FLAG, bytes([flag])), (ACTOR + 0x31E, bytes([v & 1]))])
            if predicate and flag == 0:
                mode = 4
                if v & 1:
                    query = 0 if v % 3 else 0xFFFFFFFF
                    call(0x020444A8, [], query)
                    mode = 4 if query else 2
                byte, halfword = (v * 17 + 0x91) & 255, (0xFA00 | v * 19) & 0xFFFF
                call(0x0207AFEC, [native_id], RECORD, [(ACTOR + 0x1FD, bytes([byte])), (RECORD + 8, struct.pack('<H', halfword))])
                scalar, forwarded = WIDE[v % 4], WIDE[(v + 1) % 4]
                call(0x0207D5A0, [byte, mode, halfword & 15], scalar)
                call(0x02210AD0, [ACTOR, 256, scalar], forwarded)
                result = WIDE[v // 4 % 4]
                call(0x0220EFD0, [ACTOR, native_id, scalar, forwarded], result, [(FLAG, b'\xEE')])
                if result:
                    final = [(FLAG, b'\x01')]
        return initial, services, final, arguments, result
    saved = [0, 0x02348000, 0xFFFFFFFF][v % 3]
    query = [0, 3, 0xFFFFFFFF][v // 3 % 3]
    call(0x021E5750, [], saved)
    call(0x021E6488, [recipe['argument']], 0)
    if saved:
        call(0x021E801C, [], query)
    if saved and query == 3:
        call(0x021E9DC8, [0x022083DE, saved], 0)
        call(0x021EB9A4, [4, 1, 0], 0)
    else:
        choice = 5 if v & 1 else 0xFFFFFFFF
        call(0x021E9CC0, [], choice)
        call(0x021EB9A4, [5, 0 if choice == 5 else 1, 0], 0)
    call(0x021E81E8, [1, 0x022083E6, 5, 0x02208440, 23, 0, 1, 0, 0], 0)
    selected = [0, 1, 0xFFFFFFFF][v // 9 % 3]
    call(0x021E571C, [], selected)
    argument = 4
    if not selected:
        word = WIDE[v % 4] ^ (recipe['seed'] * 0x9E37 & 0xFFFFFFFF)
        call(0x021E5738, [], RECORD, [(RECORD + 4, struct.pack('<I', word))])
        argument = word & 0x7FFFFFFF
    result = WIDE[v // 3 % 4]
    call(0x021E92F4, [argument], result)
    return initial, services, final, [recipe['argument']], result
