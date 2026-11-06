import struct

BUFFER, LENGTH, GLOBALS = 0x02350000, 0x5A88, 0x021E78C4
ARM_CALLBACK, THUMB_CALLBACK, INTERNAL = 0x02410000, 0x02411001, 0x021D8900
TEMPLATE = 0x021E6E24


def recipes():
    rows = []
    for state in (0, 1, 2, 0xFFFFFFFF):
        for irq in (0, 0x80):
            for callback in (0, ARM_CALLBACK, THUMB_CALLBACK):
                for variant in range(2):
                    index = len(rows)
                    rows.append(dict(seed=0x147000 + index, state=state, irq=irq, fiq=variant * 0x40, callback=callback,
                        owner=(0x1234, 0x8000FFFF)[variant], ticks=[(index * 0x1234567) & 0xFFFFFFFF, (index * 0x9E3779B9) & 0xFFFFFFFF],
                        upper=[0xFFFFFFFF - index, 0x80000000 + index], callbackState=(2, 0xFFFFFFFF)[variant],
                        callbackMarker=[(0xC0DE0000 + index) & 0xFFFFFFFF, index ^ 0xDEADBEEF]))
    return rows


def model(recipe, initial_buffer, initial_globals, template):
    result, globals_result = bytearray(initial_buffer), bytearray(initial_globals)
    if recipe['state']:
        return result, globals_result, []
    result[:] = bytes(LENGTH)
    struct.pack_into('<II', result, 0, recipe['owner'], recipe['callback'])
    struct.pack_into('<II', result, 8, recipe['ticks'][0] & 3, (recipe['ticks'][1] >> 2) & 3)
    result[0x18:0x58] = template
    for offset, value in [(0xF0, 1), (0x114, 0x200), (0x116, 0x200), (0xF6, 1),
        (0xE0 + 0xE, 1), (0xE0 + 0x18, 0x5A), (0xE0 + 0x32, 1),
        (0x5120 + 0xE4, 0), (0x5120 + 0xE0, recipe['owner'] & 0xFFFF), (0x5120 + 0xE8, 0x220), (0x5120 + 0xEA, 0x3DC0)]:
        struct.pack_into('<H', result, offset, value)
    for offset, value in [(0x5120 + 0xEC, 1), (0x5120 + 0xF8, INTERNAL), (0x5120 + 0xF0, 0), (0x5120 + 0xFC, BUFFER + 0xE0)]:
        struct.pack_into('<I', result, offset, value)
    struct.pack_into('<III', globals_result, 4, BUFFER + 0x120, BUFFER, 2)
    calls = [dict(address=0x02007A9C, irq=0x80, returnWords=[recipe['ticks'][index], recipe['upper'][index]]) for index in range(2)]
    calls.append(dict(address=0x020125BC, irq=0, returnWords=[0xABCD0123]))
    if recipe['callback']:
        calls.append(dict(address=recipe['callback'] & ~1, mode='thumb' if recipe['callback'] & 1 else 'arm',
            irq=0x80, arguments=[2, 0], returnWords=[0xFEEDBEEF]))
        struct.pack_into('<I', globals_result, 12, recipe['callbackState'])
        struct.pack_into('<II', result, LENGTH - 8, *recipe['callbackMarker'])
    return result, globals_result, calls
