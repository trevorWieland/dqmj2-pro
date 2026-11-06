import struct

STATE, ROWS, ROOT_DATA = 0x02350000, 0x02351000, 0x021C3708
WORDS = [0, 1, 0xFFFFFFFF, 0x7FFFFFFF, 0x80000000, 0xFFFE0001, 999, 0xFFFFFED7]


def recipes():
    result = []
    for identifier in (0, 1, 46, 47, 239, 240, 65535):
        for variant in range(8):
            fields = {offset: WORDS[(variant + ordinal) % 8] for ordinal, offset in enumerate((0, 0x1C, 0x20, 0x24, 0x28))}
            fields[4] = 0 if not variant & 1 else WORDS[(variant + 2) % 8] or 1
            fields[0x38] = 0 if not variant & 2 else WORDS[(variant + 3) % 8] or 1
            result.append(dict(seed=0x617000 + len(result), identifier=identifier, variant=variant,
                fields={str(key): value for key, value in fields.items()},
                rows=[WORDS[(variant + 2 * i) % 8] for i in range(4)], textLength=(0, 1, 31)[variant % 3],
                returnWord=(0, 1, 0x80000000, 0xFFFFFFFF)[variant % 4]))
    return result


def model(recipe, main):
    services = []
    fields = {int(key): value for key, value in recipe['fields'].items()}
    name = struct.unpack_from('<I', main, 0x67750)[0]

    def service(address, arguments, kind='opaque', final=False, **extra):
        value = recipe['returnWord'] if final else (recipe['seed'] * 0x9E3779B9 + len(services) * 0x654321) & 0xFFFFFFFF
        services.append(dict(address=address, arguments=arguments, kind=kind, returnWord=value, **extra))

    def label(slot, third, value):
        service(0x021D79E4, [slot, 0xF, third, value & 0xFFFFFFFF], 'label')

    def format_words(value, width, ordinal, slot):
        words = [0x1400 + recipe['variant'] * 32 + ordinal * 7 + i for i in range(recipe['textLength'])] + [0]
        service(0x021D8414, [value & 0xFFFFFFFF, dict(outWords=True), 16, width], 'number', words=words)
        service(0x021D7AD0, [slot, dict(textWords=words)], 'text', final=slot == 0x12)

    service(0x021D7860, [])
    service(0x021D77F8, [9])
    service(0x021D7D28, [0x0220CBD8, 0x13])
    label(0, 2, 0x81)
    words = [0x1200 + recipe['variant'] * 32 + i for i in range(recipe['textLength'])] + [0]
    service(0x02046AF4, [0x021C9698, name + 0x10, 31, 0, dict(outWords=True), 255], 'format', words=words)
    service(0x021D7AD0, [1, dict(textWords=words)], 'text')
    if recipe['identifier']:
        service(0x021D79F8, [2, 0xF, 0xF, recipe['identifier'], 16], 'labelWide')
        service(0x021D7E34, [])
        converted = 1 if recipe['identifier'] < 47 else (recipe['identifier'] - 46) & 65535
        service(0x021D7EBC, [converted, 12, 5])
    else:
        label(2, 0xF, 0)
    label(3, 2, 0x99)
    label(4, 2, (fields[0] + 0x3B) & 65535)
    label(5, 2, 0x34)
    if fields[4] == 0:
        service(0x021D79F8, [6, 0xF, 2, 0x7A, 0x30], 'labelWide')
    else:
        format_words(fields[4], 6, 0, 6)
    label(7, 2, 0x9D)
    label(8, 2, 0x35)
    if fields[0x38] == 0:
        service(0x021D79F8, [9, 0xF, 2, 0x7A, 0x30], 'labelWide')
    else:
        format_words(fields[0x38], 6, 1, 9)
    label(0xA, 2, 0x9D)
    label(0xB, 2, 0x87)
    label(0xC, 7, 3)
    label(0xD, 7, 4)
    used = (fields[0x24] + fields[0x28]) & 0xFFFFFFFF
    total = (fields[0x1C] + fields[0x20]) & 0xFFFFFFFF
    format_words(used, 2, 2, 0xE)
    format_words(total - used, 2, 3, 0xF)
    label(0x10, 2, 0x8A)
    label(0x11, 2, 0x78)
    format_words(sum(recipe['rows']), 2, 4, 0x12)
    return services
