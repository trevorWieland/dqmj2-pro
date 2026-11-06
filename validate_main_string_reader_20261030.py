import struct
from project import ROOT, configuration, read_json, sha256, write_json
import main_string_reader_native_20261030 as native


def validate(report):
    assert report['romSha256'] == configuration()['romSha256']
    assert report['matchedFunctions'] == 1 and report['matchedBytes'] == 132
    row = report['functionMatches'][0]
    assert row['bytes'] == 132 and row['exactBytes'] and row['exactAfterDeclaredRelocation']
    assert sha256(ROOT / row['source']) == row['sourceSha256']
    assert sha256(ROOT / row['object']) == row['objectSha256']
    directory = (ROOT / row['realMainLink']['linkedElf']).parent
    assert sha256(ROOT / row['realMainLink']['linkedElf']) == row['realMainLink']['linkedElfSha256']
    binary = directory / 'caller.bin'
    assert sha256(binary) == row['targetSha256']
    for entry in report['generatorSources']:
        assert sha256(ROOT / entry['path']) == entry['sha256']
    return binary.read_bytes()


def main():
    path = ROOT / 'evidence/matches/main-string-reader-20261030.json'
    code = validate(read_json(path))
    context, cursor = native.DATA + 0x100, native.DATA + 0x400
    cases = [
        ('wrong-eof-word', 44, 0xE3A01001, 0xE3A01002, 0, 0, 0),
        ('wrong-read-cursor-advance', 60, 0xE2811001, 0xE2811002, 0, 65, 0),
        ('signed-byte-return-instead-of-unsigned', 68, 0xE20200FF, 0xE1A00002, 0, 128, 0),
        ('eof-flag-not-cleared-on-unget', 84, 0x13A02000, 0x13A02001, 1, 65, 1),
        ('wrong-unget-cursor-decrement', 100, 0xE2422001, 0xE2422002, 1, 65, 0),
        ('query-truncates-full-eof-word', 116, 0xE5900004, 0xE3A00000, 2, 65, 0xFFFFFFFF),
        ('nonreturning-entry-is-not-success', 0, 0xE3520000, 0xEAFFFFFE, 0, 65, 0)]
    controls = []
    for name, offset, expected, replacement, mode, byte, eof in cases:
        assert int.from_bytes(code[offset:offset + 4], 'little') == expected
        memory = native.state(context, cursor, eof)
        memory[cursor - native.DATA] = byte
        native.execute(code, memory, context, 0xFEDCBA98, mode, 7)
        changed = bytearray(code)
        struct.pack_into('<I', changed, offset, replacement)
        try:
            native.execute(bytes(changed), memory, context, 0xFEDCBA98, mode, 7)
        except AssertionError:
            controls.append({'name': name, 'rejectedByIndependentModelOrReturnGuard': True})
        else:
            raise AssertionError(name)
    validate(read_json(path))
    write_json(ROOT / 'evidence/verification/main-string-reader-controls-20261030.json',
               {'romSha256': configuration()['romSha256'], 'report': path.relative_to(ROOT).as_posix(),
                'sourceAndObjectUnchanged': True, 'allControlsRejected': len(controls) == len(cases),
                'controls': controls, 'codeMutationsInMemoryOnly': True, 'negativeFunctionReturnCredit': 0,
                'sourceCredit': 0})
    print({'controls': len(controls), 'allRejected': True, 'sourceCredit': 0})


if __name__ == '__main__':
    main()
