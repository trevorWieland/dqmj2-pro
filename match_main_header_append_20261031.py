import ast
import sys
from project import ROOT, configuration, write_json, sha256
import match_runtime as compiler
from unicorn import __version__
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_header_append_fixture_20261031 import ENTRY, SIZE, GET, APPEND, EMPTY, recipe, execute

SOURCE = ROOT / 'src/runtime/20261031_header_append/native_main_02037b94.c'
WORK = ROOT / 'work/main-header-append-20261031'
REPORT = ROOT / 'evidence/matches/main-header-append-20261031.json'


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    compiler.WORK = WORK / 'compile'
    rows, unused = compiler.compare(SOURCE, 'main', 2, 'off', True)
    assert len(rows) == 1 and rows[0]['compiledBytes'] == SIZE
    row = rows[0]
    proof = validate(row, qualified_bindings(row), WORK / 'link')
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    row.update(exactAfterRealMwLink=True, exactAfterGenuineLink=True, linkedMatchingBytes=SIZE)
    unused, original, unused = measured_module('main')
    native = original[ENTRY - 0x02000000:ENTRY - 0x02000000 + SIZE]
    code = (WORK / 'link/caller.bin').read_bytes()
    assert code == native
    results = []
    for index in range(512):
        item = recipe(index)
        first, second = execute(original, native, item), execute(original, code, item)
        assert first == second and first['modelPassed']
        results.append(dict(recipe=item, result=first, actualReturns=2))
    negative = ROOT / 'nonmatching/main-runtime/20261031-header-append-negative/source.c'
    body = SOURCE.read_text(encoding='utf-8')
    wrong = body.replace('native_fn_0202bba0(arg0 + 1, 0)', 'native_fn_0202bba0(arg0 + 4, 0)')
    assert wrong != body
    negative.parent.mkdir(parents=True, exist_ok=True)
    if negative.exists() and negative.read_bytes() != wrong.encode():
        raise ValueError('Earlier whole-C stride control differs')
    negative.write_bytes(wrong.encode())
    compiler.WORK = WORK / 'negative-compile'
    bad_rows, unused = compiler.compare(negative, 'main', 2, 'off', True)
    assert len(bad_rows) == 1 and bad_rows[0]['compiledBytes'] == SIZE
    try:
        validate(bad_rows[0], qualified_bindings(bad_rows[0]), WORK / 'negative-link')
    except ValueError as error:
        mismatch = ast.literal_eval(str(error))
        assert mismatch['linkedBytes'] == SIZE and mismatch['matchingBytes'] == SIZE - 1
    else:
        raise ValueError('Wrong-stride C unexpectedly matched')
    bad = (WORK / 'negative-link/caller.bin').read_bytes()
    controls = []
    for index, failed in enumerate([False, True]):
        item = recipe(9000 + index)
        item['failed'] = failed
        first, second = execute(original, native, item), execute(original, bad, item)
        assert first['modelPassed'] and second['modelPassed'] == failed
        controls.append(dict(recipe=item, original=first, wrong=second, actualReturns=2))
    own = {pc for item in results for pc in item['result']['pcs'] if ENTRY <= pc < ENTRY + SIZE}
    assert len(own) * 4 == SIZE
    row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=1024,
        actualNativeHelperReturns=2 * sum(item['result']['state']['actualHelperReturns'] for item in results),
        suppliedAllocatorCompletions=1024, observedCodeBytes=len(own) * 4)
    helpers = [dict(address=hex(a), bytes=n, originalSha256=compiler.sha(original[a-0x02000000:a-0x02000000+n]))
               for a, n in [(GET, 20), (APPEND, 84), (EMPTY, 44)]]
    write_json(REPORT, dict(romSha256=config['romSha256'], matches=rows, results=results,
        negativeControls=controls, negativeCompiled=bad_rows[0], negativeLinkMismatch=mismatch, helpers=helpers,
        generator='match_main_header_append_20261031.py', generatorSha256=sha256(__file__),
        fixture=dict(path='main_header_append_fixture_20261031.py', sha256=sha256(ROOT/'main_header_append_fixture_20261031.py')),
        limitations=['Supplied allocator returns null or an aligned backed object without allocator implementation credit',
            'Payload size0..512, node offset0 and supplied empty/one-node list views only; no full object extent or ownership claim',
            'All three original list/getter bodies execute; full-word handle and fifth stack argument are preserved',
            'No unsupported pointer, heap validation, live synchronization, complete Windows game or Android execution claim']))
    print(dict(bytes=SIZE, actualReturns=1024, actualHelperReturns=row['nativeOracle']['actualNativeHelperReturns'],
               suppliedAllocatorCompletions=1024, negativeActualReturns=4))


if __name__ == '__main__':
    main()
