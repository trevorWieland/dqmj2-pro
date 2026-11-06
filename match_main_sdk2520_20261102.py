import concurrent.futures
from pathlib import Path
import match_runtime as compiler
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link


INPUT = ROOT / 'evidence/inputs/main-sdk2520-source-units-20261102.json'


def worker(spec):
    source = ROOT / spec['source']
    assert sha256(source) == spec['sourceSha256']
    text = source.read_text(encoding='utf-8')
    assert len(text.splitlines()) <= 500 and '/*' not in text and '//' not in text
    for pin in spec.get('sourceDependencies', []):
        assert sha256(ROOT / pin['path']) == pin['sha256']
    executable = ROOT / spec['compiler']
    assert sha256(executable) == spec['compilerSha256']
    compiler.FLAGS = list(spec['flags'])
    compiler.WORK = ROOT / 'work/main-sdk2520-matching-20261102' / source.stem / 'compile'
    optimization = compiler.FLAGS[0][2:]
    inlining = compiler.FLAGS[compiler.FLAGS.index('-inline') + 1]
    rows, _ = compiler.compare(source, 'main', optimization, inlining, compiler=executable)
    assert len(rows) == 1 and not rows[0].get('compileFailed'), rows
    row = rows[0]
    row['sourceDependencies'] = spec.get('sourceDependencies', [])
    assert row['bytes'] == spec['bytes'] and row['relocations'] == spec['priorRelocations']
    proof = validate(row, qualified_bindings(row), compiler.WORK.parent / 'link')
    row.update(genuineLinkComparison=freeze_link(proof), exactBytes=row['bytes'], sourceOnlyCompilerInput=True,
        originalObjectScaffolding=False, sourceLanguage='C', referenceFunction=spec['referenceFunction'],
        compilerIncludesAndPreprocessorMacrosAbsent=True)
    return row


def main():
    specs = read_json(INPUT)['sourceUnits']
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool: rows = list(pool.map(worker, specs))
    metadata, _, _ = measured_module('main')
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=configuration()['romSha256'], processor='arm9', program='', module='main',
        moduleSha256=metadata['sha256'], matches=rows, matchedFunctions=len(rows),
        matchedBytes=sum(r['bytes'] for r in rows), actualNativeFunctionReturns=0,
        provisionalIncludesAndMacrosAbsent=True, repositoryLocalDeclaredHeadersAllowed=True, originalStorageSourceCredit=0,
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=sha256(INPUT))],
        reproductionCommand='python match_main_sdk2520_20261102.py',
        limitations=['Complete isolated C function and genuine linked-byte comparisons, not native behavioral or scene qualification',
            'Original global data storage and all unselected lower routines remain zero-credit scaffolding',
            'Reference revision is comparative reconstructed source, not proof of the game SDK revision or authorship',
            'Type/interface and configured-boundary audits must qualify before shared adoption',
            'Whole-module comparisons and exact ROM packaging still use original-object scaffolding'])
    write_json(ROOT / 'evidence/matches/main-sdk2520-20261102.json', report)
    print(dict(functions=len(rows), bytes=report['matchedBytes'], actualNativeFunctionReturns=0,
        provisionalIncludesAbsent=True, acceptancePending=True))


if __name__ == '__main__':
    main()
