import ast
import sys
from project import ROOT, configuration, write_json, sha256
import match_runtime as compiler
from unicorn import __version__
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_numeric_dispatch_fixture_20261031 import ENTRY, SIZE, recipes, execute, compact

SOURCE = ROOT / 'src/runtime/20261031_numeric_dispatch/native_main_0203b660.c'
WORK = ROOT / 'work/main-numeric-dispatch-20261031'
REPORT = ROOT / 'evidence/matches/main-numeric-dispatch-20261031.json'


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    compiler.WORK = WORK / 'compile'
    rows, unused = compiler.compare(SOURCE, 'main', 3, 'off', True)
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
    results, pcs = [], set()
    for item in recipes():
        first, second = execute(original, native, item), execute(original, code, item)
        assert first == second and first['modelPassed'], (item, compact(first))
        pcs.update(first['pcs'])
        results.append(dict(recipe=item, result=compact(first), actualReturns=2))
    text = SOURCE.read_text(encoding='utf-8')
    wrong = text.replace('M2C_FIELD(arg0, s32 *, 0x2C) = 1;', 'M2C_FIELD(arg0, s32 *, 0x2C) = 2;')
    assert wrong != text
    negative = ROOT / 'nonmatching/main-runtime/20261031-numeric-dispatch-negative/source.c'
    negative.parent.mkdir(parents=True, exist_ok=True)
    assert not negative.exists() or negative.read_bytes() == wrong.encode()
    negative.write_bytes(wrong.encode())
    compiler.WORK = WORK / 'negative-compile'
    bad_rows, unused = compiler.compare(negative, 'main', 3, 'off', True)
    assert len(bad_rows) == 1 and bad_rows[0]['compiledBytes'] == SIZE
    try:
        validate(bad_rows[0], qualified_bindings(bad_rows[0]), WORK / 'negative-link')
    except ValueError as error:
        mismatch = ast.literal_eval(str(error))
        assert mismatch['linkedBytes'] == SIZE and mismatch['matchingBytes'] == SIZE - 1
    else:
        raise ValueError('Wrong-C transient word unexpectedly matched')
    bad = (WORK / 'negative-link/caller.bin').read_bytes()
    controls = []
    for index, pool in enumerate([0, 255]):
        item = dict(index=9000 + index, count=2, mode=1, pool=pool, units=2, empty=False)
        first, second = execute(original, native, item), execute(original, bad, item)
        assert first['modelPassed'] and second['modelPassed'] == bool(index)
        controls.append(dict(recipe=item, original=compact(first), wrong=compact(second), actualReturns=2))
    observed = {pc for pc in pcs if ENTRY <= pc < ENTRY + SIZE}
    assert len(observed) * 4 == 404
    row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=2 * len(results),
        actualNativeHelperReturns=2 * sum(item['result']['actualNativeHelperReturns'] for item in results),
        suppliedCalls=2 * sum(item['result']['suppliedCalls'] for item in results),
        observedCodeBytes=404, literalPoolBytes=12)
    write_json(REPORT, dict(romSha256=config['romSha256'], matches=rows, results=results,
        observedPcs=sorted(pcs), negativeControls=controls, wrongC=bad_rows[0], wrongLinkMismatch=mismatch,
        generator='match_main_numeric_dispatch_20261031.py', generatorSha256=sha256(__file__),
        fixture=dict(path='main_numeric_dispatch_fixture_20261031.py', sha256=sha256(ROOT/'main_numeric_dispatch_fixture_20261031.py')),
        limitations=['Synthetic counts-1..3, backed byte selectors0..15 and synthetic8-bit reservation occupancy',
                     'Four lower cleanup/setup/timer/start services are explicit no-memory-write providers; callback remains deferred',
                     'Original unsigned division, reservation, list and IRQ-mask routines execute with zero additional source credit',
                     'Privileged IRQ instructions execute only inside isolated Unicorn; no real audio, interrupt timing or scene execution',
                     'No complete Windows game or Android execution claim']))
    print(dict(bytes=SIZE, **row['nativeOracle'], negativeActualReturns=4))


if __name__ == '__main__':
    main()
