import shutil
import re
from project import ROOT, read_json, write_json, sha256


def main():
    split = read_json(ROOT / 'evidence/attempts/main-nitrosdk-split2520-20261102.json')['results']
    rows = []
    for row in split:
        assert row['genuineExact']
        entry = row['compiledEntry']
        source = ROOT / row['source']
        assert sha256(source) == row['sourceSha256']
        target = ROOT / 'src/runtime/20261102_sdk2520' / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        dependencies = []
        for pin in entry.get('sourceDependencies', []):
            path = ROOT / pin['path']
            assert sha256(path) == pin['sha256']
            copied = target.with_name(path.name)
            original_header = path.read_text(encoding='utf-8')
            header = original_header
            for declaration, symbol in re.findall(r'(?m)^(\s*(?:extern\s+)?void\s+(native_fn_\w+)\(\);)\s*$', header):
                assert re.search(r'\bvoid\s+' + symbol + r'\(void\);', header), symbol
                header = header.replace(declaration, '')
            copied.write_text(header, encoding='utf-8')
            dependencies.append(dict(path=copied.relative_to(ROOT).as_posix(), sha256=sha256(copied)))
        rows.append(dict(source=target.relative_to(ROOT).as_posix(), sourceSha256=sha256(target),
            address=entry['address'], bytes=entry['bytes'], compiler=entry['compilerPath'],
            compilerSha256=entry['compilerSha256'], flags=entry['compilerFlags'],
            sourceDependencies=dependencies, priorRelocations=entry['relocations'],
            referenceFunction=row.get('referenceFunction', 'FSi_TranslateCommand')))
    assert len(rows) == 4 and sum(r['bytes'] for r in rows) == 2520
    write_json(ROOT / 'evidence/inputs/main-sdk2520-source-units-20261102.json', dict(sourceCredit=0, sourceUnits=rows,
        ordinaryHeadersBelow500Lines=True, originalStorageSourceCredit=0))
    print(dict(functions=4, bytes=2520, sourceCredit=0))


if __name__ == '__main__':
    main()
