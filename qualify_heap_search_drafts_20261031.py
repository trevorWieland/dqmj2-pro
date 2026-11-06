import ast
import match_runtime as compiler
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_heap_search_fixture_20261031 import execute


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    results = []
    for entry, size, optimization, speed in [(0x0202B044, 180, 2, False), (0x0202B0F8, 176, 3, True)]:
        source = ROOT / f'src/runtime/20261031_heap_block_search/native_main_{entry:08x}.c'
        work = ROOT / f'work/heap-search-draft-qualification-20261031/{entry:08x}'
        compiler.WORK = work / 'compile'
        rows, unused = compiler.compare(source, 'main', optimization, 'on', speed=speed)
        row = rows[0]
        try:
            validate(row, qualified_bindings(row), work / 'link')
        except ValueError as error:
            mismatch = ast.literal_eval(str(error))
        else:
            raise ValueError('Unexpected genuine equality; review before classification')
        candidate = (work / 'link/caller.bin').read_bytes()
        native = original[entry - 0x02000000:entry - 0x02000000 + size]
        cases = []
        for index in range(980):
            first, second = execute(original, native, entry, index), execute(original, candidate, entry, index)
            assert first['modelPassed'] and second['modelPassed'], (hex(entry), index, first, second)
            assert first['calls'] == second['calls'] and first['result'] == second['result']
            assert first['backingSha256'] == second['backingSha256']
            cases.append(dict(index=index, original=first, candidate=second, actualReturns=2))
        results.append(dict(address=hex(entry), source=row['source'], sourceSha256=row['sourceSha256'],
            compilerResult=row, genuineLinkMismatch=mismatch, cases=cases, actualReturns=1960,
            behaviorMatchedWithinFixture=True, sourceFunctionMatch=False, acceptedSourceCredit=0))
    write_json(ROOT / 'evidence/attempts/main-heap-search-behavior-qualified-drafts-20261031.json', dict(
        romSha256=config['romSha256'], results=results, actualReturns=3920, acceptedSourceCredit=0,
        limitations=['Ordinary C draft semantics agree only for bounded stable linked lists, both mode-bit values and power-of-two alignment1..64',
            'Candidate linked bytes still differ; neither function is accepted into module/ROM builds',
            'Commit/allocation body is supplied; malformed/cyclic lists, concurrent mutation and real heap effects remain unproved',
            'Callee-saved registers and stack guards are enforced; ARM caller scratch values are not equated for nonmatching candidates']))
    print(dict(draftedFunctions=2, nativeBytes=356, behaviorActualReturns=3920, acceptedSourceCredit=0))


if __name__ == '__main__':
    main()
