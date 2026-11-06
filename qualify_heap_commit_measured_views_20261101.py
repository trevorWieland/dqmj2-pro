import ast
import match_runtime as compiler
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_heap_commit_fixture_20261101 import execute, ENTRY


def linked(source, work):
    compiler.WORK = work / 'compile'
    rows, unused = compiler.compare(source, 'main', 2, 'off')
    row = rows[0]
    assert not row.get('compileFailed'), row
    try:
        validate(row, qualified_bindings(row), work / 'link')
    except ValueError as error:
        mismatch = ast.literal_eval(str(error))
    else:
        raise AssertionError('Unexpected exact equality requires independent acceptance review')
    return row, mismatch, (work / 'link/caller.bin').read_bytes()


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    source = ROOT / 'src/runtime/20261101_heap_block_commit_measured_views/native_main_0202ae9c.c'
    work = ROOT / 'work/heap-commit-measured-qualification-20261101'
    row, mismatch, code = linked(source, work / 'preferred')
    native = original[ENTRY - 0x02000000:ENTRY - 0x02000000 + 424]
    cases = []
    for index in range(560):
        first, second = execute(original, native, index), execute(original, code, index)
        assert first['modelPassed'] and second['modelPassed'], (index, first, second)
        assert first['backingSha256'] == second['backingSha256'] and first['result'] == second['result']
        cases.append(dict(index=index, original=first, candidate=second))
    negative = []
    changes = [('wrong-marker', '0x5544', '0x5545'), ('wrong-group', 'u16 group = list->group;', 'u16 group = list->group + 1;'),
        ('wrong-fill-mode', 'if (flags & 1)', 'if (flags & 2)'), ('wrong-split-threshold', '< 20', '< 24')]
    for label, previous, replacement in changes:
        text = source.read_text()
        assert previous in text
        path = ROOT / f'generated/heap-commit-negative-20261101/{label}/native_main_0202ae9c.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.replace(previous, replacement), encoding='utf-8')
        bad_row, bad_mismatch, bad_code = linked(path, work / label)
        failed, positive, helpers = [], 0, 0
        for index in range(560):
            result = execute(original, bad_code, index)
            helpers += result['actualHelperReturns']
            if result['modelPassed']:
                positive += 1
            else:
                failed.append(dict(index=index, result=result))
        assert failed
        negative.append(dict(label=label, compilerResult=bad_row, linkMismatch=bad_mismatch,
            actualReturns=560, actualHelperReturns=helpers, independentRejections=len(failed), positiveCases=positive, failures=failed))
    helpers = sum(c['original']['actualHelperReturns'] + c['candidate']['actualHelperReturns'] for c in cases)
    report = dict(romSha256=config['romSha256'], generator='qualify_heap_commit_measured_views_20261101.py',
        generatorSha256=sha256(__file__), fixture='main_heap_commit_fixture_20261101.py',
        fixtureSha256=sha256(ROOT / 'main_heap_commit_fixture_20261101.py'), compilerResult=row, linkMismatch=mismatch,
        cases=cases, actualReturns=1120, actualHelperReturns=helpers, suppliedCalls=0, negativeControls=negative,
        wrongBodyActualReturns=2240, independentRejections=sum(r['independentRejections'] for r in negative),
        acceptedSourceCredit=0, sourceFunctionMatch=False, limitations=[
            'Single selected free block and zero or one pre-existing used node',
            'Word-rounded bounded requests with stable valid synthetic heap metadata; malformed/cyclic/concurrent heaps and game-scene feasibility remain unproved',
            'Callee-saved registers, control mode, stack guards and full heap page compared; caller-scratch and APSR values are excluded',
            'Original helper bodies execute; this fixture supplies no helper outcomes; compiled candidate bytes still differ'])
    write_json(ROOT / 'evidence/attempts/main-heap-commit-measured-views-behavior-qualified-draft-20261101.json', report)
    print(dict(actualReturns=1120, actualHelperReturns=helpers, wrongBodyReturns=2240,
               independentRejections=report['independentRejections'], suppliedCalls=0, sourceCredit=0))


if __name__ == '__main__':
    main()
