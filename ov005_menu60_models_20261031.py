import struct

CONTEXT, SELECTION, INPUT = 0x021ED438, 0x021ED348, 0x020EDEB8
ROWS_A, ROWS_B, ROW_BYTES = 0x02350000, 0x02380000, 0x268 * 256


def recipes():
    rows = []
    for flags in (0, 1, 2, 3, 0x8000, 0xFFFF):
        for variant in range(12):
            index = len(rows)
            before = (0, 1, 127, 128, 255, 256, 0x800000FF)[variant % 7]
            after = (before, 0, 128, 255, 256, 0xFFFFFFFF)[variant % 6]
            rows.append(dict(seed=0x160000 + index, precondition=1, flags=flags, before=before, after=after,
                flag48=(0, 1, 2, 0xFFFFFFFF)[variant % 4], changedIndex=(after + 7) & 255,
                changedRows=ROWS_B, changedFlag=(0, 1, 255)[variant % 3]))
    for value in (0, 2, 0xFFFFFFFF, 0x80000000):
        rows.append(dict(rows[0], seed=0x160000 + len(rows), precondition=value))
    return rows


def model(recipe, initial_context):
    context, services = bytearray(initial_context), []

    def service(address, args=(), result=0xE0000011, writes=(), probes=()):
        services.append(dict(address=address, arguments=list(args), result=result, writes=list(writes), probes=list(probes)))

    service(0x021DD788, result=recipe['precondition'])
    if recipe['precondition'] != 1:
        return context, services, [], recipe['precondition'], 0
    service(0x021E0040)
    effects = [(SELECTION, struct.pack('<I', recipe['after'])), (CONTEXT + 0x48, struct.pack('<I', recipe['flag48']))]
    service(0x021E0D88, writes=effects)
    struct.pack_into('<I', context, 0x48, recipe['flag48'])
    selector_calls = 2
    signed = (recipe['after'] & 255) - (256 if recipe['after'] & 128 else 0)
    if recipe['flag48'] == 1:
        selector_calls += 1
        service(0x021DE19C, [signed & 0xFFFFFFFF], probes=[(CONTEXT + 0x48, struct.pack('<I', 1))])
        struct.pack_into('<I', context, 0x48, 0)
    if recipe['before'] != recipe['after']:
        selector_calls += 1
        service(0x021DE19C, [signed & 0xFFFFFFFF], probes=[(CONTEXT + 0x48, bytes(context[0x48:0x4C]))])
    if recipe['flags'] & 1:
        selector_calls += 1
        index = recipe['after'] & 255
        context[4] = index
        changed_address = recipe['changedRows'] + recipe['changedIndex'] * 0x268 + 0xFF
        writes = [(CONTEXT + 4, bytes([recipe['changedIndex']])), (CONTEXT + 0x40, struct.pack('<I', recipe['changedRows'])),
            (changed_address, bytes([recipe['changedFlag']]))]
        service(0x020BF4C4, [index], writes=writes, probes=[(CONTEXT + 4, bytes([index]))])
        effects += writes
        context[4] = recipe['changedIndex']
        struct.pack_into('<I', context, 0x40, recipe['changedRows'])
        if recipe['changedFlag']:
            service(0x021E155C, [0x22])
        result = 0xAB000052 if recipe['changedFlag'] else 0xAB000054
        service(0x021E1048, [0x52 if recipe['changedFlag'] else 0x54], result=result)
        return context, services, effects, result, selector_calls * 2 + 2
    if recipe['flags'] & 2:
        service(0x021DDF24)
        service(0x021E026C, [4, 1, 0, 1, 0, 0])
        service(0x021E1048, [0x53])
        service(0x021E155C, [0], result=0xCD000000)
        result = 0xCD000000
    else:
        result = recipe['flags']
    return context, services, effects, result, selector_calls * 2 + 4
