import struct

CTX, INFO, STATS = 0x02217BE0, 0x02350000, 0x02351000
ROOT_DATA, KEYS, RAW_STATE = 0x021C3708, 0x020EDEB8, 0x020F6102
WORD_TABLE = [0x12345678, 0xFFFFFFFF, 0x100, 0xABCDEF01]


def recipes():
    rows = []
    for state in list(range(25)) + [25, 26, 0x80000000, 0xFFFFFFFF]:
        for variant in range(3):
            rows.append(dict(state=state, keys=(0, 8, 0x1000)[variant], status=(0, 1, 0xFFFFFFFF)[variant],
                rawState=(0, 1, 255)[variant], flags=0, index=variant, numeric=variant, counter=(0, 1, 32)[variant],
                selector=0, textWord=variant))
    for state in (5, 9, 11):
        choices = range(4) if state == 5 else (0, 1, 2, 3, 4, 5, 6, 7, 8, 128, 255) if state == 9 else (
            0, 1, 2, 10, 11, 50, 51, 100, 101, 1000, 1001, 5000, 5001, 10000, 10001, 50000, 50001, 100000, 100001, 0xFFFFFFFF)
        for index, value in enumerate(choices):
            rows.append(dict(state=state, keys=(1, 0x800, 0xFFFF)[index % 3], status=2, rawState=0,
                flags=value if state == 9 else 0, index=value if state == 5 else index % 4,
                numeric=value if state == 11 else index, counter=2, selector=index,
                textWord=(0, 1, 0x8000FF44, 0xFFFFFFFF)[index % 4]))
    for counter in (-1, 2, 0x7FFFFFFF):
        rows.append(dict(rows[0], state=24, counter=counter))
    for index, row in enumerate(rows):
        row.update(seed=0x133000 + index, label=(-1, 0, 63)[index % 3])
    return rows


def model(recipe, main, overlay):
    services, writes, returned = [], [], 5
    name_pointer = struct.unpack_from('<I', main, 0x67750)[0]

    def call(address, arguments=(), result=None, native=False):
        if result is None:
            result = (recipe['seed'] * 0x9E3779B9 + len(services) * 0x654321) & 0xFFFFFFFF
        services.append(dict(address=address, arguments=[word & 0xFFFFFFFF for word in arguments],
            returnWord=result, native=native))
        return result

    def keys():
        call(0x021DF150, result=KEYS, native=True)
        call(0x0202A634, result=KEYS, native=True)

    def state(value):
        call(0x021E2F58, [value], value, True)
        writes.append((CTX + 12, struct.pack('<I', value)))

    def getter(address):
        return call(address, result=name_pointer if address == 0x02067748 else STATS, native=True)

    selected = recipe['state']
    if selected in (0, 1, 13, 14, 15):
        call(0x021DFD34, result=recipe['status'])
    elif selected in (7, 21):
        call(0x0205E844, [recipe['label']], 0)
    elif selected == 2:
        call(0x020644C0, result=0)
    elif selected == 17:
        call(0x021E9484, result=0)
    elif selected == 24:
        value = recipe['counter'] - 1
        writes.append((CTX + 8, struct.pack('<i', value)))
        if value == 0:
            call(0x020642CC, [45])
            returned = 0
    elif 0 <= selected <= 23:
        if selected == 18:
            call(0x02041800, result=recipe['rawState'], native=True)
            call(0x020417F8, result=recipe['rawState'], native=True)
            if recipe['rawState'] == 1:
                return services, writes, returned
        keys()
        if not recipe['keys'] & 0xFF7:
            return services, writes, returned
        if selected not in (5, 9, 11):
            raise ValueError('Menu33 active UI branch is outside this declared domain')
        call(0x021DF590, [0x52])
        call(0x021DEE68)
        if selected == 5:
            getter(0x02067748)
            handle = call(0x0205DC70, [15, 2, (recipe['index'] + 0x3B) & 65535])
            call(0x02048034, [handle, 0])
            getter(0x02067748)
            resolved = call(0x02067D54, [WORD_TABLE[recipe['index']]], recipe['textWord'])
            handle = call(0x0205DC70, [15, 2, (resolved + 0xA4) & 65535])
            call(0x02048034, [handle, 32])
            call(0x021DED5C, [15, 4, 0x23])
            state(6)
            call(0x021DB59C, [1, 0, 0])
            call(0x021D77E8, [4])
        elif selected == 9:
            call(0x02063EF8, result=INFO)
            if recipe['flags']:
                for unused in range(3):
                    call(0x02063EF8, result=INFO)
                call(0x02048094, [int(recipe['flags'] & 7).bit_count(), 0])
                call(0x02063EF8, result=INFO)
                resolved = call(0x021DE358, [recipe['selector'] & 255], recipe['textWord'])
                call(0x02048094, [resolved, 32])
                label = 0x8F
            else:
                getter(0x020679F0)
                getter(0x020679F0)
                resolved = call(0x021DE358, [1001 + recipe['numeric']], recipe['textWord'])
                call(0x02048094, [resolved, 0])
                label = 0x52
            call(0x021DED5C, [15, 4, label])
            state(11)
        else:
            getter(0x020679F0)
            value = recipe['numeric']
            classification = 9 if value == 0 else next((index for index, upper in enumerate(
                (1, 10, 50, 100, 1000, 5000, 10000, 50000, 100000)) if value <= upper), 9)
            call(0x021E3B7C, [value], classification, True)
            label = struct.unpack_from('<H', overlay, 0x0220D0F0 - 0x021D7240 + classification * 2)[0]
            call(0x021DED5C, [15, 4, label])
            state(12)
    return services, writes, returned
