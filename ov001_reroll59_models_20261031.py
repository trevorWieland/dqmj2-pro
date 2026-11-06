import struct

CONTEXT, RNG_STATE = 0x0223E088, 0x020F6044


def recipes():
    result = []
    for phase in (0, 10, 20, 30, 100, 255):
        for counter in (0, 29, 30, 31, 254, 255):
            for variant in range(3):
                index = len(result)
                result.append(dict(seed=0x159000 + index, phase=phase, counter=counter, side=(0, 1, 2, 3, 255)[index % 5],
                    slot=(0, 1, 2, 3, 4, 255)[index % 6], nativeId=(0, 1, 47, 255)[index % 4],
                    threshold=(0, 1, 25, 100, 101, 0x80000000, 0x7FFFFFFF)[index % 7],
                    ready=(0, 1, 0xFFFFFFFF)[variant], rngWord=(index * 0x9E3779B9 + 0x12345678) & 0xFFFFFFFF))
    return result


def model(recipe, initial, pools):
    result, services = bytearray(initial), []
    pointer = pools[recipe['side']] + recipe['slot'] * 1088 if recipe['side'] < 4 and recipe['slot'] < 3 else 0
    rng_after = recipe['rngWord']
    if result[14] == 0:
        services.append(dict(address=0x02066A7C, arguments=[recipe['nativeId']], result=recipe['threshold'],
            writes=[(RNG_STATE, struct.pack('<I', recipe['rngWord']))]))
        rng_after = (recipe['rngWord'] * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
        threshold = recipe['threshold'] - (1 << 32) if recipe['threshold'] & (1 << 31) else recipe['threshold']
        result[14] = 10 if (rng_after >> 16) % 100 < threshold else 100
    if result[14] == 10:
        services.append(dict(address=0x0220C6E0, arguments=[pointer, recipe['nativeId'], recipe['side']], result=0xDEAD0001, writes=[]))
        result[13], result[14] = 0, 20
    if result[14] == 20:
        services.append(dict(address=0x0220C7EC, arguments=[pointer, recipe['nativeId'], recipe['side']], result=recipe['ready'], writes=[]))
        if recipe['ready']:
            result[13], result[14] = 0, 30
        else:
            result[13] = (result[13] + 1) & 255
            if result[13] > 30:
                result[13], result[14] = 0, 30
    if result[14] == 30:
        result[13] = (result[13] + 1) & 255
        if result[13] > 30:
            result[14] = 100
    if result[14] == 100:
        result[14], result[3] = 0, 14
    return result, services, rng_after
