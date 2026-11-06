import struct

STATE, ROOT_DATA = 0x02350000, 0x021C3708
VALUES = [0, 1, 999, 65535, 32000, -1, -999, 1024]


def recipes():
    rows = []
    for identifier in (0, 1, 46, 47, 239, 240, 65535):
        for variant in range(8):
            fields = {offset: VALUES[(variant + index) % 8] & 0xFFFFFFFF
                for index, offset in enumerate((0x2C, 0x30, 0x10, 0x18, 0x14))}
            fields[0xC] = variant
            rows.append(dict(seed=0x628000 + len(rows), identifier=identifier, variant=variant,
                fields={str(key): value for key, value in fields.items()}, textLength=(0, 1, 31)[variant % 3],
                returnWord=(0, 1, 0x80000000, 0xFFFFFFFF)[variant % 4]))
    return rows


def model(recipe, main):
    services = []
    fields = {int(key): value for key, value in recipe['fields'].items()}
    name = struct.unpack_from('<I', main, 0x67750)[0]

    def service(address, arguments, kind='opaque', final=False, **extra):
        value = recipe['returnWord'] if final else (recipe['seed'] * 0x9E3779B9 + len(services) * 0x654321) & 0xFFFFFFFF
        services.append(dict(address=address, arguments=arguments, kind=kind, returnWord=value, **extra))

    def label(slot, value):
        service(0x021D79E4, [slot, 15, 2, value], 'label')

    def number(value, ordinal, slot):
        words = [0x2800 + recipe['variant'] * 32 + ordinal * 7 + i for i in range(recipe['textLength'])] + [0]
        service(0x021D8414, [value & 0xFFFFFFFF, dict(outWords=True), 16, 4], 'number', words=words)
        service(0x021D7AD0, [slot, dict(textWords=words)], 'text', final=slot == 12)

    service(0x021D7860, [])
    service(0x021D77F8, [13])
    service(0x021D7E34, [])
    service(0x021D7D28, [0x0220CF44, 13])
    label(0, 0x81)
    words = [0x2600 + recipe['variant'] * 32 + i for i in range(recipe['textLength'])] + [0]
    service(0x02046AF4, [0x021C9698, name + 16, 31, 0, dict(outWords=True), 255], 'format', words=words)
    service(0x021D7AD0, [1, dict(textWords=words)], 'text')
    service(0x021D79F8, [2, 15, 15, recipe['identifier'], 16], 'labelWide')
    service(0x021D7E34, [])
    identifier = recipe['identifier']
    converted = 0 if identifier == 0 else 1 if identifier < 47 else (identifier - 46) & 65535
    service(0x021D7EBC, [converted, 12, 4])
    service(0x02048094, [fields[12] + 1, 0])
    total = (fields[0x2C] + fields[0x30]) & 0xFFFFFFFF
    remaining = total - fields[0x10] - fields[0x18] - fields[0x14]
    for ordinal, (slot, label_id, value) in enumerate([(4, 0x18, total), (6, 0x95, fields[0x10]),
            (8, 0x97, fields[0x18]), (10, 0x96, fields[0x14]), (12, 0xAD, remaining)]):
        label(slot - 1, label_id)
        number(value, ordinal, slot)
    return services
