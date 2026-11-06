import shutil
import re
from project import ROOT, read_json, write_json, sha256


def main():
    original = ROOT / 'evidence/attempts/main-nitrosdk-closed-breadth-20261102.json'
    rows = []
    links = read_json(ROOT / 'work/main-nitrosdk-links-20261102/report.json')['results']
    excluded = set()
    for name in ['cohort146-vram-gecom-sound-recruitment-and-abi-20261102-specification.json',
        'cohort147-arm7-cam-bootstrap-and-native-constructor-20261102-specification.json']:
        for row in read_json(ROOT / name)['expectedAdditions']:
            if row['module'] == 'main': excluded.add(int(row['address'], 0))
    for row in read_json(original)['results']:
        if not row['genuineExact']: continue
        entry = row['compiledEntry']
        if int(entry['address'], 0) in excluded: continue
        origin = next(r for r in links if r.get('genuineLinkedExact') and r['identity']['address'] == entry['address']
            and r['referenceFunction'] == row['referenceFunction'] and r['profile'] == row['profile'])
        reference = ROOT / origin['referenceSource']
        assert sha256(reference) == origin['entry']['sourceSha256']
        source = ROOT / row['source']
        assert sha256(source) == row['sourceSha256']
        original_text = source.read_text(encoding='utf-8')
        text = original_text
        redundant = []
        for declaration, symbol in re.findall(r'(?m)^(\s*(?:extern\s+)?void\s+(native_fn_\w+)\(\);)\s*$', text):
            assert re.search(r'\bvoid\s+' + symbol + r'\(void\);', text), symbol
            text = text.replace(declaration, '')
            redundant.append(symbol)
        target = ROOT / 'src/runtime/20261102_nitrosdk18424' / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists(): assert target.read_text(encoding='utf-8') in [original_text, text]
        target.write_text(text, encoding='utf-8')
        original_flags = list(entry['compilerFlags'])
        flags, skip = [], False
        for token in original_flags:
            if skip:
                skip = False
                continue
            if token == '-i':
                skip = True
                continue
            if token.startswith('-D'): continue
            flags.append(token)
        assert not skip and '-i' not in flags and not any(t.startswith('-D') for t in flags)
        rows.append(dict(source=target.relative_to(ROOT).as_posix(), sourceSha256=sha256(target),
            address=entry['address'], bytes=entry['bytes'], compiler=entry['compilerPath'],
            compilerSha256=entry['compilerSha256'], flags=flags, priorFlags=original_flags,
            priorRelocations=entry['relocations'], referenceFunction=row['referenceFunction'],
            referenceSource=origin['referenceSource'], referenceSourceSha256=sha256(reference),
            removedRedundantEmptyDeclarations=redundant))
    write_json(ROOT / 'evidence/inputs/main-nitrosdk18424-source-units-20261102.json',
        dict(sourceCredit=0, originalCampaignSha256=sha256(original), sourceUnits=rows,
            provisionalIncludeDirectoriesRemoved=True, macrosAlreadyExpanded=True))
    print(dict(sourceUnits=len(rows), bytes=sum(r['bytes'] for r in rows), sourceCredit=0))


if __name__ == '__main__':
    main()
