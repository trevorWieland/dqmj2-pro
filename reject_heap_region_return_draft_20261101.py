import ast
import match_runtime as compiler
from project import ROOT, read_json, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_heap_region_fixture_20261101 import execute, ENTRY


def main():
    positive_path = ROOT / 'evidence/attempts/main-heap-region-return-behavior-qualified-draft-20261101.json'
    positive = read_json(positive_path)
    assert positive['actualReturns'] == 4096 and positive['suppliedCalls'] == 0
    unused, original, unused = measured_module('main')
    source = ROOT / 'src/runtime/20261101_heap_region_return/native_main_0202b1a8.c'
    assert sha256(source) == positive['compilerResult']['sourceSha256']
    results = []
    mutations = [('wrong-marker', '0x4652', '0x4653'),
        ('wrong-minimum-region', 'combined.end - combined.begin < 16', 'combined.end - combined.begin < 20'),
        ('wrong-empty-result', 'if (combined.end - combined.begin < 16) return 0;', 'if (combined.end - combined.begin < 16) return 1;')]
    for label, previous, replacement in mutations:
        text = source.read_text()
        assert text.count(previous) == 1
        path = ROOT / f'generated/heap-region-return-negative-20261101/{label}/native_main_0202b1a8.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.replace(previous, replacement), encoding='utf-8')
        work = ROOT / f'work/heap-region-return-negative-20261101/{label}'
        compiler.WORK = work / 'compile'
        rows, unused = compiler.compare(path, 'main', 2, 'off')
        row = rows[0]
        try:
            validate(row, qualified_bindings(row), work / 'link')
        except ValueError as error:
            mismatch = ast.literal_eval(str(error))
        else:
            raise AssertionError('Wrong region-return body unexpectedly matches original bytes')
        code = (work / 'link/caller.bin').read_bytes()
        failures, positives, helper_returns = [], 0, 0
        for index in range(2048):
            result = execute(original, code, index)
            helper_returns += result['actualHelperReturns']
            if result['modelPassed']:
                positives += 1
            else:
                failures.append(dict(index=index, result=result))
        assert failures and positives
        results.append(dict(label=label, compilerResult=row, linkMismatch=mismatch, failures=failures,
            actualReturns=2048, actualHelperReturns=helper_returns, independentRejections=len(failures), positiveCases=positives))
    write_json(ROOT / 'evidence/attempts/main-heap-region-return-negative-controls-20261101.json', dict(
        generator='reject_heap_region_return_draft_20261101.py', generatorSha256=sha256(__file__),
        positiveReport=positive_path.relative_to(ROOT).as_posix(), positiveReportSha256=sha256(positive_path),
        results=results, actualReturns=6144, independentRejections=sum(r['independentRejections'] for r in results),
        suppliedCalls=0, acceptedSourceCredit=0, sourceFunctionMatch=False,
        limitations=['Wrong-body rejection supports only the positive fixture domain; compiled-byte equality and scene feasibility remain unproved']))
    print(dict(wrongBodies=3, actualReturns=6144, independentRejections=sum(r['independentRejections'] for r in results), sourceCredit=0))


if __name__ == '__main__':
    main()
