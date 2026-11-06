BUFFER, OTHER, LENGTH, GLOBAL = 0x02350000, 0x02360000, 0x5A88, 0x021E78CC
ARM_CALLBACK, THUMB_CALLBACK = 0x02410000, 0x02411001


def recipes():
    return [dict(seed=0x181000 + index, state=state, irq=(variant & 1) * 0x80, fiq=(variant >> 1 & 1) * 0x40,
        callback=(0, ARM_CALLBACK, THUMB_CALLBACK)[variant % 3], innerState=(0, 1, 2, 3, 0xFFFFFFFF)[variant % 5],
        afterBuffer=OTHER if variant >= 8 else BUFFER, callbackState=0xFFFFFFFF if variant & 4 else 3)
        for index, (state, variant) in enumerate((state, variant) for state in (0, 1, 2, 3, 4, 0xFFFFFFFF) for variant in range(16))]


def plan(recipe):
    active = recipe['state'] == 2
    callback = active and recipe['callback'] != 0
    return dict(active=active, callback=callback, message=active and recipe['innerState'] not in (1, 3),
        target=recipe['afterBuffer'] if callback else BUFFER, state=recipe['callbackState'] if callback else 3 if active else recipe['state'],
        nativeReturns=6 if active else 3)
