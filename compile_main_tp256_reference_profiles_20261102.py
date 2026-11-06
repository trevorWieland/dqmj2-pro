import concurrent.futures
from pathlib import Path
import match_runtime as compiler
from project import ROOT, write_json, sha256
from link_runtime_unit import validate, measured_module
from recover_linked_runtime import qualified_bindings


def worker(spec):
    source, executable, opt = spec
    compiler.WORK = ROOT / 'work/main-tp256-reference-profiles-20261102' / executable.split('/')[-2] / opt.replace(',', '-')
    compiler.FLAGS = [*compiler.FLAGS, '-lang', 'c99', '-ipa', 'file']
    rows, _ = compiler.compare(source, 'main', opt, 'on,noauto', compiler=ROOT / executable)
    result = dict(compiler=executable, optimization=opt, sourceCredit=0)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        return dict(result, compileRows=rows, genuineExact=False)
    row = rows[0]
    result['compilation'] = row
    try:
        proof = validate(row, qualified_bindings(row), compiler.WORK / 'link')
        result.update(genuineExact=True, genuineLinkComparison=proof)
    except ValueError as error:
        result.update(genuineExact=False, genuineLinkComparison=error.args[0])
    binary = compiler.WORK / 'link/caller.bin'
    if binary.exists():
        _, image, _ = measured_module('main')
        native, body = image[0xDED8:0xDFD8], binary.read_bytes()
        result.update(linkedBytes=len(body), matchingBytes=sum(a == b for a, b in zip(native, body)), linkedSha256=sha256(binary))
    return result


def main():
    report = ROOT / 'evidence/attempts/main-tp256-reference-profiles-20261102.json'
    assert not report.exists()
    source = ROOT / 'nonmatching/main/20261102-tp256-reference/native_main_0200ded8.c'
    jobs = [(source, exe, opt) for exe in compiler.COMPILER_PINS for opt in ['2', '4,p']]
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool: results = list(pool.map(worker, jobs))
    write_json(report, dict(sourceCredit=0, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source), nativeReturns=0,
        selectedInterfacesNotQualified=True, results=results))
    print([(r.get('genuineExact'), r.get('linkedBytes'), r.get('matchingBytes')) for r in results])


if __name__ == '__main__':
    main()
