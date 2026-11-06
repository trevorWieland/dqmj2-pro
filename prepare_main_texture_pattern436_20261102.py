import re
from project import ROOT, read_json, write_json, sha256


def main():
    archive = ROOT / 'evidence/attempts/main-sdk-visibility-v4-candidate-archive-20261102.json'
    own = {0x02034248: 'SetTexParamaters_', 0x02034320: 'SetPlttParamaters_',
        0x02034388: 'NNSi_G3dAnmCalcNsBtp'}
    callees = {'NNS_G3dGetResDataByName': 0x0202BBB4, 'FX_Div': 0x0200235C,
        'NNSi_G3dGetTexPatAnmFV': 0x0202BFE0,
        'NNSi_G3dGetTexPatAnmTexNameByIdx': 0x0202BF88,
        'NNSi_G3dGetTexPatAnmPlttNameByIdx': 0x0202BFB4}
    callees.update({name: address for address, name in own.items()})
    rows = []
    for row in read_json(archive)['rows']:
        address = int(row['identity']['address'], 0)
        if address not in own:
            continue
        original = ROOT / row['candidate']
        assert sha256(original) == row['sourceSha256']
        text = original.read_text(encoding='utf-8')
        for name, target in callees.items():
            alias = f'native_main_{target:08x}' if target == address else f'native_fn_{target:08x}'
            text = re.sub(r'\b' + re.escape(name) + r'\b', alias, text)
        text = text.replace('typedef unsigned long u32;', 'typedef unsigned int u32;')
        text = text.replace('typedef signed long s32;', 'typedef signed int s32;')
        assert len(text.splitlines()) <= 500 and '/*' not in text and '//' not in text
        path = ROOT / f'src/runtime/20261102_texture_pattern436/native_main_{address:08x}.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            assert path.read_text(encoding='utf-8') == text
        else:
            path.write_text(text, encoding='utf-8')
        rows.append(dict(address=hex(address), bytes=row['identity']['bytes'],
            source=path.relative_to(ROOT).as_posix(), sourceSha256=sha256(path),
            referenceCandidate=row['candidate'], referenceCandidateSha256=row['sourceSha256']))
    assert len(rows) == 3
    write_json(ROOT / 'evidence/attempts/main-texture-pattern436-source-preparation-20261102.json',
        dict(sourceCredit=0, acceptancePending=True, functions=rows,
            changedTypes='Explicit32-bit int word types; ARM and PE32 use32-bit long as well',
            renamedFunctions='Typed entry and helper names carry measured native addresses',
            referenceArchiveSha256=sha256(archive)))
    print(dict(preparedFunctions=len(rows), initializedBytes=sum(r['bytes'] for r in rows), sourceCredit=0))


if __name__ == '__main__':
    main()
