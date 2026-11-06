import ast
import sys
from project import ROOT, configuration, read_json, write_json, sha256
import match_runtime as compiler
import save_link_snapshots
from recover_linked_runtime import qualified_bindings
from link_runtime_unit import validate, measured_module
from main_word_dispatch_fixture_20261031 import ENTRY, SIZE, recipe, recipes, execute
from unicorn import __version__

SOURCE = ROOT / 'src/runtime/20261031_word_dispatch/native_main_02005bd8.c'
REPORT = ROOT / 'evidence/matches/main-word-dispatch-20261031.json'
WORK = ROOT / 'work/main-word-dispatch-20261031'


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    compiler.WORK = WORK / 'compile'
    rows, unused = compiler.compare(SOURCE, 'main', 2, 'off', True)
    assert len(rows) == 1 and rows[0]['compiledBytes'] == SIZE
    row = rows[0]
    directory = WORK / 'link'
    proof = validate(row, qualified_bindings(row), directory)
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    row.update(exactAfterRealMwLink=True, exactAfterGenuineLink=True, linkedMatchingBytes=SIZE)
    unused, original, unused = measured_module('main')
    code = (directory / 'caller.bin').read_bytes()
    native = original[ENTRY - 0x02000000:ENTRY - 0x02000000 + SIZE]
    assert code == native
    results = []
    for item in recipes():
        a, b = execute(original, native, item), execute(original, code, item)
        assert a == b and a['modelPassed']
        results.append(dict(recipe=item, result=a, actualReturns=2))
    negative = ROOT / 'nonmatching/main-runtime/20261031-word-dispatch-byte-negative/source.c'
    body = SOURCE.read_text(encoding='utf-8').replace('return *(u32 *)cursor;', 'return *cursor;')
    assert body != SOURCE.read_text(encoding='utf-8')
    negative.parent.mkdir(parents=True, exist_ok=True)
    if negative.exists() and negative.read_bytes() != body.encode():
        raise ValueError('Previous wrong whole-C body differs')
    negative.write_bytes(body.encode())
    compiler.WORK = WORK / 'negative-compile'
    bad_rows, unused = compiler.compare(negative, 'main', 2, 'off', True)
    assert len(bad_rows) == 1 and bad_rows[0]['compiledBytes'] == SIZE
    bad_row = bad_rows[0]
    try:
        validate(bad_row, qualified_bindings(bad_row), WORK / 'negative-link')
    except ValueError as error:
        mismatch = ast.literal_eval(str(error))
        assert mismatch['nativeBytes'] == SIZE and mismatch['linkedBytes'] == SIZE
        assert mismatch['matchingBytes'] == SIZE - 1
    else:
        raise ValueError('Wrong-width source unexpectedly matches')
    bad = (WORK / 'negative-link/caller.bin').read_bytes()
    controls = []
    for index, mask in enumerate([1, 1 << 8]):
        item = recipe(9000 + index, mask)
        baseline = execute(original, native, item)
        assert baseline['modelPassed'] and baseline['state']['actualReturns'] == 1
        result = execute(original, bad, item)
        assert result['state']['actualReturns'] == 1
        assert result['modelPassed'] == bool(index)
        controls.append(dict(recipe=item, original=baseline, result=result, actualReturns=2, expectedModelRejection=not bool(index)))
    observed = {pc for result in results for pc in result['result']['pcs']}
    assert len(observed) * 4 == SIZE - 8
    row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=2 * len(results),
                               nativeDependencyReturns=0, providedCalls=0, observedCodeBytes=len(observed) * 4, literalPoolBytes=8,
                               maximumInstructions=max(r['result']['state']['instructions'] for r in results))
    report = dict(romSha256=config['romSha256'], matches=rows, results=results, negativeControls=controls,
                  negativeCompiled=bad_row, negativeGenuineLinkMismatch=mismatch,
                  generator='match_main_word_dispatch_20261031.py', generatorSha256=sha256(__file__),
                  fixtureSha256=sha256(ROOT / 'main_word_dispatch_fixture_20261031.py'),
                  limitations=['Synthetic aligned shared words and eight twelve-byte records are supplied RAM context',
                               'No original object extent, table meaning, hardware writer, live synchronization or game lifecycle is inferred',
                               'No reconstructed data, utility-module source, whole-ROM source or Windows-game completion credit'])
    write_json(REPORT, report)
    print(dict(functions=1, bytes=SIZE, actualReturns=row['nativeOracle']['actualReturns'],
               negativeActualReturns=2 * len(controls), providers=0))


if __name__ == '__main__':
    main()
