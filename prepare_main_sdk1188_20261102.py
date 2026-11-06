import shutil
from project import ROOT, read_json, write_json, sha256


def main():
    split = read_json(ROOT / 'evidence/attempts/main-nitrosdk-split788-20261102.json')['results']
    fs = read_json(ROOT / 'evidence/attempts/main-fscommand400-typed-table-20261102.json')
    rows = []
    for row in [*split, fs]:
        assert row['genuineExact']
        entry = row['compiledEntry']
        source = ROOT / row['source']
        assert sha256(source) == row['sourceSha256']
        target = ROOT / 'src/runtime/20261102_sdk1188' / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        dependencies = []
        for pin in entry.get('sourceDependencies', []):
            path = ROOT / pin['path']
            assert sha256(path) == pin['sha256']
            copied = target.with_name(path.name)
            shutil.copyfile(path, copied)
            dependencies.append(dict(path=copied.relative_to(ROOT).as_posix(), sha256=sha256(copied)))
        rows.append(dict(source=target.relative_to(ROOT).as_posix(), sourceSha256=sha256(target),
            address=entry['address'], bytes=entry['bytes'], compiler=entry['compilerPath'],
            compilerSha256=entry['compilerSha256'], flags=entry['compilerFlags'],
            sourceDependencies=dependencies, priorRelocations=entry['relocations'],
            referenceFunction=row.get('referenceFunction', 'FSi_TranslateCommand')))
    assert len(rows) == 4 and sum(r['bytes'] for r in rows) == 1188
    write_json(ROOT / 'evidence/inputs/main-sdk1188-source-units-20261102.json', dict(sourceCredit=0, sourceUnits=rows,
        ordinaryHeadersBelow500Lines=True, originalStorageSourceCredit=0))
    print(dict(functions=4, bytes=1188, sourceCredit=0))


if __name__ == '__main__':
    main()
