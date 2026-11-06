import re
from pathlib import Path
from project import ROOT, read_json, write_json, sha256


def main():
    proof = read_json(ROOT / 'evidence/matches/main-random-word152-20261101.json')
    source = ROOT / proof['matches'][0]['source']
    assert sha256(source) == proof['matches'][0]['sourceSha256']
    predicate = ROOT / 'src/runtime/runtime03/native_main_0203d1f0.c'
    pattern = r'typedef struct \{\s*u8 unknown_0\[0xc\];\s*u32 field_c;\s*\} Record_native_data_020f6028;\s*extern Record_native_data_020f6028 native_data_020f6028;'
    text, count = re.subn(pattern, '#include "random_word152_record_20261101.h"', source.read_text())
    assert count == 1
    original_predicate = predicate.read_text()
    assert original_predicate.count('extern u8 native_data_020f6028[];') == 1
    changed_predicate = original_predicate.replace('extern u8 native_data_020f6028[];', '#include "random_word152_record_20261101.h"')
    assert changed_predicate.count('M2C_FIELD(native_data_020f6028,') == 3
    changed_predicate = changed_predicate.replace('M2C_FIELD(native_data_020f6028,', 'M2C_FIELD(&native_data_020f6028,')
    folder = ROOT / 'generated/portability/20261101-random-word152-shared-views'
    folder.mkdir(parents=True, exist_ok=True)
    rows = []
    wrong = ROOT / 'nonmatching/integration/20261101-random-word152/wrong-encoding/source.c'
    wrong_text, wrong_count = re.subn(pattern, '#include "random_word152_record_20261101.h"', wrong.read_text())
    assert wrong_count == 1
    for name, content, original in [('word.c', text, source), ('predicate.c', changed_predicate, predicate),
            ('wrong-word.c', wrong_text, wrong)]:
        output = folder / name
        if output.exists():
            assert output.read_text() == content
        else:
            output.write_text(content, encoding='utf-8')
        rows.append(dict(source=original.relative_to(ROOT).as_posix(), sourceSha256=sha256(original),
            nativeVariant=output.relative_to(ROOT).as_posix(), nativeVariantSha256=sha256(output)))
    write_json(ROOT / 'evidence/portability/random-word152-shared-views-20261101.json',
        dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), sourceCredit=0,
            originalArmSourcesUnchanged=True, sharedRecordBytes=16, wordFieldOffset=12, alignment=4,
            transformation='Shared external object type; predicate obtains its byte view from the address of that record',
            variants=rows, header=dict(path='ports/common/random_word152_record_20261101.h',
                sha256=sha256(ROOT / 'ports/common/random_word152_record_20261101.h')),
            limitations=['Native backend declaration/address-view adapter only; no new original-game source credit',
                'The measured16-byte view is not a complete historical aggregate or full global-RAM alias model']))


if __name__ == '__main__':
    main()
