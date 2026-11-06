TYPES = {'u8': (1, False, 'unsigned char'), 's8': (1, True, 'signed char'),
         'u16': (2, False, 'unsigned short'), 's16': (2, True, 'signed short'),
         'u32': (4, False, 'unsigned int'), 's32': (4, True, 'signed int'),
         'fx16': (2, True, 'signed short'), 'fx32': (4, True, 'signed int')}


def encode(document):
    assert set(document) == {'version', 'kind', 'symbol', 'elementType', 'elementCount', 'elements'}
    assert document['version'] == 1 and document['kind'] == 'typed-sdk-integer-array'
    width, signed, unused = TYPES[document['elementType']]
    values = document['elements']
    assert document['elementCount'] == len(values) and len(values) > 0
    low, high = (-(1 << (width * 8 - 1)), 1 << (width * 8 - 1)) if signed else (0, 1 << (width * 8))
    assert all(type(value) is int and low <= value < high for value in values)
    return b''.join(value.to_bytes(width, 'little', signed=signed) for value in values)


def render(document, symbol):
    payload = encode(document)
    c_type = TYPES[document['elementType']][2]
    values = document['elements']
    lines = [f'const {c_type} {symbol}[{len(values)}] = {{']
    lines += ['    ' + ', '.join(str(value) for value in values[start:start + 16]) + ','
              for start in range(0, len(values), 16)]
    return '\n'.join(lines + ['};', '']), payload


def validate_layout(layout):
    expected = {('', 'arm9', 'main', 0x020d8c4c, 64), ('', 'arm9', 'main', 0x020d7fe0, 258),
                ('dwc/utility.bin/move/child.srl', 'arm7', 'utility-child-arm7-main', 0x027f8068, 240)}
    actual = {(r['program'], r['processor'], r['module'], int(r['address'], 0), r['bytes']) for r in layout['assets']}
    assert len(layout['assets']) == 3 and actual == expected
    for row in layout['assets']:
        assert row['mode'] == row['kind'] == 'data'
        assert row['compilerProcessor'] == ('arm7tdmi' if row['processor'] == 'arm7' else 'arm946e')
        assert int(row['moduleBase'], 0) == (0x027e0000 if row['processor'] == 'arm7' else 0x02000000)
