from project import ROOT, read_json, write_json, sha256
import match_main_oam_reference296_closed_20261101 as builder


def main():
    original = ROOT / 'nonmatching/main/20261102-tp256-reference/native_main_0200ded8.c'
    text = original.read_text(encoding='utf-8')
    assert text.count('extern struct {') == 1
    text = text.replace('extern struct {', 'extern struct {\n    u32 unknown_0;')
    source = ROOT / 'src/runtime/20261102_tp256/native_main_0200ded8.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    if source.exists(): assert source.read_text(encoding='utf-8') == text
    else: source.write_text(text, encoding='utf-8')
    builder.WORK = ROOT / 'work/main-tp256-measured-layout-20261102'
    row, proof, body = builder.build(source, 'positive', True)
    write_json(ROOT / 'evidence/attempts/main-tp256-measured-layout-20261102.json',
        dict(sourceCredit=0, genuineExact=True, linkedBytes=len(body), compiledEntry=row, genuineLinkProof=proof,
            source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
            referenceSource=original.relative_to(ROOT).as_posix(), referenceSourceSha256=sha256(original),
            measuredStructurePrefixBytes=4, prefixMeaningUnresolved=True, originalStorageSourceCredit=0,
            nativeReturns=0, behavioralAndCallerProofPending=True))
    print(dict(genuineExact=True, bytes=len(body), originalStorageSourceCredit=0, sourceCredit=0))


if __name__ == '__main__':
    main()
