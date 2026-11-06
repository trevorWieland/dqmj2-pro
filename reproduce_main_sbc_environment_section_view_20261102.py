import shutil
import struct
from project import ROOT, write_json, sha256
from link_runtime_unit import measured_module
import match_main_oam_reference296_closed_20261101 as builder


def main():
    old = ROOT / 'nonmatching/main/20261102-sbc-external-storage/02031800'
    folder = ROOT / 'nonmatching/main/20261102-sbc-environment-section-view'
    folder.mkdir(parents=True, exist_ok=True)
    text = (old / 'native_main_02031800.c').read_text(encoding='utf-8')
    text = text.replace('extern u32 native_data_main_020dd698[2];', 'extern u32 native_data_main_020dd690[4];')
    text = text.replace('native_data_main_020dd698[1]', 'native_data_main_020dd690[3]')
    text = text.replace('native_data_main_020dd698[0]', 'native_data_main_020dd690[2]')
    source = folder / 'native_main_02031800.c'
    if source.exists(): assert source.read_text(encoding='utf-8') == text
    else: source.write_text(text, encoding='utf-8')
    if (folder / 'types.h').exists(): assert (folder / 'types.h').read_bytes() == (old / 'types.h').read_bytes()
    else: shutil.copyfile(old / 'types.h', folder / 'types.h')
    _, image, _ = measured_module('main')
    assert struct.unpack_from('<4I', image, 0xDD690) == (42, 0, 42, 0)
    builder.WORK = ROOT / 'work/main-sbc-environment-section-view-20261102'
    row, proof, body = builder.build(source, source.stem, True)
    assert len(body) == 836
    write_json(ROOT / 'evidence/verification/main-sbc-environment-section-view-reproduction-20261102.json',
        dict(passed=True, sourceCredit=0, sourceSha256=sha256(source), headerSha256=sha256(folder / 'types.h'),
            completeLinkedBytes=836, originalStorageWords=[42, 0, 42, 0],
            compilerEntry=row, genuineLinkProof=proof, sourceDataCredit=0))
    print(dict(genuineLinkedBytes=836, originalSectionWordsVerified=4, sourceCredit=0))


if __name__ == '__main__':
    main()
