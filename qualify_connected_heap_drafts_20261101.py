import ast
import match_runtime as compiler
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_heap_connected_fixture_20261101 import execute, ENTRY


def linked(source, work, optimization=2, inline='off', speed=False):
    compiler.WORK = work / 'compile'
    rows, unused = compiler.compare(source, 'main', optimization, inline, speed=speed)
    row = rows[0]
    assert not row.get('compileFailed'), row
    try:
        validate(row, qualified_bindings(row), work / 'link')
    except ValueError as error:
        mismatch = ast.literal_eval(str(error))
    else:
        raise AssertionError('Unexpected genuine equality needs separate source acceptance review')
    return dict(compilerResult=row, linkMismatch=mismatch), (work / 'link/caller.bin').read_bytes()


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    root = ROOT / 'work/connected-heap-drafts-20261101'
    commit_source = ROOT / 'src/runtime/20261101_heap_block_commit/native_main_0202ae9c.c'
    commit_row, commit_code = linked(commit_source, root / 'commit')
    native_commit = original[ENTRY - 0x02000000:ENTRY - 0x02000000 + 424]
    results = []
    for entry, size, optimization, speed in [(0x0202B044, 180, 2, False), (0x0202B0F8, 176, 3, True)]:
        source = ROOT / f'src/runtime/20261031_heap_block_search/native_main_{entry:08x}.c'
        row, code = linked(source, root / f'{entry:08x}', optimization, 'on', speed)
        native = original[entry - 0x02000000:entry - 0x02000000 + size]
        cases = []
        for index in range(560):
            first = execute(original, native_commit, index, entry, native)
            second = execute(original, commit_code, index, entry, code)
            assert first['modelPassed'] and second['modelPassed'], (hex(entry), index, first, second)
            assert first['backingSha256'] == second['backingSha256'] and first['result'] == second['result']
            cases.append(dict(index=index, original=first, reconstructed=second))
        results.append(dict(address=hex(entry), freshSearchBuild=row, freshCommitBuild=commit_row,
            cases=cases, actualReturns=1120, actualHelperReturns=sum(c['original']['actualHelperReturns'] +
                c['reconstructed']['actualHelperReturns'] for c in cases)))
    report = dict(romSha256=config['romSha256'], generator='qualify_connected_heap_drafts_20261101.py',
        generatorSha256=sha256(__file__), fixture='main_heap_connected_fixture_20261101.py',
        fixtureSha256=sha256(ROOT / 'main_heap_connected_fixture_20261101.py'), results=results,
        actualReturns=2240, actualHelperReturns=sum(r['actualHelperReturns'] for r in results),
        freshlyCompiledOrdinaryCFunctions=3, draftedNativeBytes=780, suppliedCalls=0,
        sourceFunctionMatch=False, acceptedSourceCredit=0, limitations=[
            'One stable free block, zero or one used block, power-of-two alignments 1 through 64, and word-rounded requests',
            'Both reconstructed search and commit bodies execute together; remaining helper bodies execute from original measured code',
            'Independent expected full-page heap state, actual termination, callee-saved registers, mode and stack guards are checked',
            'No caller-scratch/APSR equality, exact compiled-byte credit, malformed heap, concurrent mutation or game-scene proof'])
    write_json(ROOT / 'evidence/attempts/main-connected-heap-behavior-qualified-drafts-20261101.json', report)
    print(dict(actualReturns=2240, actualHelperReturns=report['actualHelperReturns'],
               freshlyCompiledFunctions=3, draftedNativeBytes=780, suppliedCalls=0, sourceCredit=0))


if __name__ == '__main__':
    main()
