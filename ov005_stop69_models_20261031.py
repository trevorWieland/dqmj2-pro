BUFFER, OTHER, LENGTH, GLOBAL = 0x02350000, 0x02360000, 0x5A88, 0x021E78CC
ARM_CALLBACK, THUMB_CALLBACK = 0x02410000, 0x02411001


def recipes():
    return [dict(seed=0x169000 + index, state=state, irq=(variant & 1) * 0x80, fiq=(variant >> 1 & 1) * 0x40,
        callback=(0, ARM_CALLBACK, THUMB_CALLBACK)[variant % 3], flags=(0, 1, 0x8000, 0xFFFF)[variant % 4],
        shift=(0, 15, 16, 31, 32, 0xFFFF)[variant % 6], innerState=(0, 1, 2, 0xFFFFFFFF)[variant // 4],
        afterBuffer=OTHER if variant >= 8 else BUFFER, callbackState=0xFFFFFFFF if variant & 4 else 1)
        for index, (state, variant) in enumerate((state, variant) for state in (0, 1, 2, 3, 4, 0xFFFFFFFF) for variant in range(16))]


def plan(recipe):
    active = recipe['state'] in (2, 3)
    callback = active and recipe['callback'] != 0
    target = recipe['afterBuffer'] if callback else BUFFER
    query = recipe['flags']
    if query:
        query = (query | (1 << recipe['shift'] if recipe['shift'] < 32 else 0)) & 0xFFFF
    cleanup = active and query == 0
    message = cleanup and recipe['innerState'] not in (0, 1)
    return dict(active=active, callback=callback, target=target, query=query, cleanup=cleanup, message=message,
        state=(recipe['callbackState'] if callback else 1) if active else recipe['state'], nativeReturns=6 + int(cleanup) if active else 3)
