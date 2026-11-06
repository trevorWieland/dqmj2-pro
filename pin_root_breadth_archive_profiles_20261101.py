import copy
from pathlib import Path
from project import ROOT, read_json, write_json, sha256


def main():
    original = ROOT / 'evidence/attempts/root-breadth-source-archive-20261101.json'
    report = copy.deepcopy(read_json(original))
    documents = {}
    for row in report['records']:
        if not row['compiledInHistoricalProof']:
            continue
        path = row['sourceReport']
        if path not in documents:
            documents[path] = read_json(ROOT / path)
        unit = next(item for item in documents[path]['results']
                    if item['mode'] == row['mode'] and int(item['address'], 0) == int(row['address'], 0))
        attempt = next(item for item in unit['attempts'] if item.get('objectSha256') == row['originalObjectSha256'])
        compiler = attempt['compilerPath']
        assert compiler.startswith('tools/') and (ROOT / compiler).resolve().is_relative_to(ROOT / 'tools')
        assert sha256(ROOT / compiler) == row['originalCompilerSha256']
        assert attempt['compilerFlags'] == row['compilerFlags'] and attempt['sourceSha256'] == row['sourceSha256']
        row['compilerPath'] = compiler
    report.update(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        originalArchive=original.relative_to(ROOT).as_posix(), originalArchiveSha256=sha256(original),
        eachHistoricalCompilerProfileExplicit=True, freshArchiveRecompileProven=False)
    output = ROOT / 'evidence/attempts/root-breadth-source-archive-v2-20261101.json'
    write_json(output, report)
    names = [row['source'] for row in report['records']] + [output.relative_to(ROOT).as_posix(),
        original.relative_to(ROOT).as_posix(), Path(__file__).name, 'archive_root_breadth_sources_20261101.py',
        'recompile_root_breadth_archive_20261101.py', 'recompile_root_breadth_archive_v2_20261101.py',
        'evidence/attempts/root-breadth-archive-recompile-initial-missing-profile-failure-20261101.json']
    write_json(ROOT / 'provenance/root-breadth-generated-c-v2-20261101.json', dict(schemaVersion=1,
        sourceCredit=0, generatedHypotheses=True, files=[dict(path=name, sha256=sha256(ROOT / name)) for name in names]))
    compilers = sorted({row['compilerPath'] for row in report['records'] if row['compiledInHistoricalProof']})
    print(dict(compiledHistoricalUnits=385, compilerPaths=compilers, sourceCredit=0))


if __name__ == '__main__':
    main()
