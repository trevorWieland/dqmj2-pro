from project import ROOT, write_json, sha256
import match_main_oam_reference296_closed_20261101 as builder


def main():
    old = ROOT / 'nonmatching/main/20261102-alarm-section-global-interface/02038970-base4p/native_main_02038970.c'
    source = ROOT / 'nonmatching/main/20261102-alarm-section-view/native_main_02038970.c'
    text = old.read_text(encoding='utf-8').replace('extern u32 native_data_main_020f4c38;',
        'extern u32 native_data_main_020f4c38[2];')
    text = text.replace('(native_data_main_020f4c38 & mask)', '(native_data_main_020f4c38[1] & mask)')
    text = text.replace('native_data_main_020f4c38 |= mask', 'native_data_main_020f4c38[1] |= mask')
    assert source.read_text(encoding='utf-8') == text
    builder.WORK = ROOT / 'work/main-alarm-section-view-20261102'
    row, proof, body = builder.build(source, source.stem, True)
    assert len(body) == 72
    write_json(ROOT / 'evidence/verification/main-alarm-section-view-reproduction-20261102.json',
        dict(passed=True, sourceCredit=0, sourceSha256=sha256(source), completeLinkedBytes=72,
            originalLockAddress='0x020f4c3c', originalSectionBase='0x020f4c38',
            originalDataDefinitionProvided=False, compilerEntry=row, genuineLinkProof=proof))
    print(dict(completeLinkedBytes=72, sourceCredit=0))


if __name__ == '__main__':
    main()
