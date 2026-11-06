NAME = 'native_utility_child_arm7_crc_table16_027f7f74'
POLYNOMIAL = 0xA001


def derive(polynomial=POLYNOMIAL):
    values = []
    for nibble in range(16):
        value = nibble
        for unused in range(4):
            value = value >> 1 ^ (polynomial if value & 1 else 0)
        values.append(value)
    return values


def source_text(values):
    if len(values) != 16 or any(not 0 <= value <= 0xFFFF for value in values):
        raise ValueError('CRC table requires exactly16 unsigned halfwords')
    return 'typedef unsigned short u16;\nu16 ' + NAME + '[16] = {\n    ' + ', '.join(f'0x{value:04x}' for value in values) + '\n};\n'
