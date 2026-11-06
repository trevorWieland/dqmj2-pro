import ast
import match_runtime as compiler
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_heap_region_fixture_20261101 import execute, ENTRY


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    source = ROOT / 'src/runtime/20261101_heap_region_return/native_main_0202b1a8.c'
    work = ROOT / 'work/heap-region-return-qualification-20261101'
    compiler.WORK = work / 'compile'
    rows, unused = compiler.compare(source, 'main', 2, 'off')
    row = rows[0]
    try:
        validate(row, qualified_bindings(row), work / 'link')
    except ValueError as error:
        mismatch = ast.literal_eval(str(error))
    else:
        raise AssertionError('Unexpected exact match requires separate review')
    code = (work / 'link/caller.bin').read_bytes()
    native = original[ENTRY - 0x02000000:ENTRY - 0x02000000 + 328]
    cases = []
    for index in range(2048):
        first, second = execute(original, native, index), execute(original, code, index)
        assert first['modelPassed'] and second['modelPassed'], (index, first, second)
        assert first['backingSha256'] == second['backingSha256'] and first['result'] == second['result']
        cases.append(dict(index=index, original=first, candidate=second))
    helpers = sum(c['original']['actualHelperReturns'] + c['candidate']['actualHelperReturns'] for c in cases)
    write_json(ROOT / 'evidence/attempts/main-heap-region-return-behavior-qualified-draft-20261101.json', dict(
        generator='qualify_heap_region_return_draft_20261101.py', generatorSha256=sha256(__file__),
        fixture='main_heap_region_fixture_20261101.py', fixtureSha256=sha256(ROOT / 'main_heap_region_fixture_20261101.py'),
        romSha256=config['romSha256'], compilerResult=row, linkMismatch=mismatch, cases=cases,
        actualReturns=4096, actualHelperReturns=helpers, suppliedCalls=0, acceptedSourceCredit=0,
        sourceFunctionMatch=False, limitations=['Stable bounded sorted synthetic free lists and word-rounded returned regions',
            'Original list and fill helpers execute; no service outcome is supplied',
            'Full heap page, actual termination, callee-saved registers, mode and stack guards checked; caller-scratch/APSR equality excluded',
            'Compiled bytes differ; no exact source credit, malformed/concurrent heap or scene feasibility claim']))
    print(dict(draftedFunctions=1, nativeBytes=328, actualReturns=4096, actualHelperReturns=helpers, sourceCredit=0))


if __name__ == '__main__':
    main()
