from sdk_constant_data_codec_20261106 import encode, render, TYPES


def validate_layout(layout):
    expected = {('', 'arm9', 'main', 0x020d8354, 1536), ('', 'arm9', 'main', 0x020d8954, 724),
                ('', 'arm9', 'main', 0x020d8254, 256), ('', 'arm9', 'main', 0x020d8154, 256),
                ('dwc/utility.bin/move/child.srl', 'arm9', 'utility-child-arm9-main', 0x02021d94, 724),
                ('dwc/utility.bin/move/child.srl', 'arm9', 'utility-child-arm9-main', 0x02021c94, 256)}
    actual = {(r['program'], r['processor'], r['module'], int(r['address'], 0), r['bytes']) for r in layout['assets']}
    assert layout['version'] == 1 and len(layout['assets']) == 6 and actual == expected
    for row in layout['assets']:
        assert row['mode'] == row['kind'] == 'data'
        assert row['compilerProcessor'] == 'arm946e' and int(row['moduleBase'], 0) == 0x02000000
