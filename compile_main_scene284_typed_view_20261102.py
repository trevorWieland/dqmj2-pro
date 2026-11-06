from project import ROOT, write_json, sha256
import match_main_oam_reference296_closed_20261101 as builder


def main():
    old = ROOT / 'nonmatching/main/20261102-scene284-store-paths-v2/native_main_0203db28.c'
    text = old.read_text(encoding='utf-8')
    assert text.count('extern u32 native_fn_ov000_021d9580(u32);') == 1
    text = text.replace('extern u32 native_fn_ov000_021d9580(u32);',
        'extern u32 native_fn_ov000_021d9580(u8);')
    source = ROOT / 'src/runtime/20261102_scene284/native_main_0203db28.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    if source.exists(): assert source.read_text(encoding='utf-8') == text
    else: source.write_text(text, encoding='utf-8')
    builder.WORK = ROOT / 'work/main-scene284-typed-view-20261102'
    row, proof, body = builder.build(source, 'positive', True)
    write_json(ROOT / 'evidence/attempts/main-scene284-typed-view-20261102.json',
        dict(sourceCredit=0, source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
            genuineExact=True, compiledEntry=row, genuineLinkProof=proof, linkedBytes=len(body),
            selectedF200RawWordMigrationStillPending=True, nativeBehaviorProofPending=True))
    print(dict(genuineExact=True, bytes=len(body), sourceCredit=0, abiMigrationPending=True))


if __name__ == '__main__':
    main()
