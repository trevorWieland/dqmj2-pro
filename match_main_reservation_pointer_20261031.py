import ast
import sys
import match_runtime as compiler
import save_link_snapshots
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from unicorn import __version__
from main_reservation_pointer_fixture_20261031 import ENTRY, SIZE, LOCK, ACTIVE, recipes, execute

SOURCE = ROOT / 'src/runtime/20261031_reservation_pointer/native_main_0203a1d4.c'
WORK = ROOT / 'work/main-reservation-pointer-20261031'
REPORT = ROOT / 'evidence/matches/main-reservation-pointer-20261031.json'


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    compiler.WORK = WORK / 'compile'
    rows, unused = compiler.compare(SOURCE, 'main', 2, 'off')
    assert len(rows) == 1
    row = rows[0]
    proof = validate(row, qualified_bindings(row), WORK / 'link')
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    row.update(exactAfterRealMwLink=True, exactAfterGenuineLink=True, linkedMatchingBytes=SIZE)
    unused, original, unused = measured_module('main')
    assert int.from_bytes(original[0x3A5E4:0x3A5E8], 'little') == LOCK
    assert int.from_bytes(original[0x3A5E8:0x3A5EC], 'little') == ACTIVE
    native = original[ENTRY - 0x02000000:ENTRY - 0x02000000 + SIZE]
    code = (WORK / 'link/caller.bin').read_bytes()
    assert code == native
    results, pcs = [], set()
    for item in recipes():
        first, second = execute(original, native, item), execute(original, code, item)
        assert first == second and first['modelPassed'], item
        pcs.update(first['pcs'])
        results.append(dict(recipe=item, result=first, actualReturns=2))
    wrong = SOURCE.read_text().replace('native_fn_0203a078(u32 *);', 'native_fn_0203a078();').replace('native_fn_0203a078(arg0);', 'native_fn_0203a078();')
    negative = ROOT / 'nonmatching/main-runtime/20261031-reservation-pointer-negative/source.c'
    negative.parent.mkdir(parents=True, exist_ok=True)
    assert not negative.exists() or negative.read_bytes() == wrong.encode()
    negative.write_bytes(wrong.encode())
    compiler.WORK = WORK / 'negative-compile'
    bad_rows, unused = compiler.compare(negative, 'main', 2, 'off')
    assert len(bad_rows) == 1
    try:
        validate(bad_rows[0], qualified_bindings(bad_rows[0]), WORK / 'negative-link')
    except ValueError as error:
        mismatch = ast.literal_eval(str(error))
        assert mismatch['linkedBytes'] == SIZE and mismatch['matchingBytes'] == SIZE - 2
    else:
        raise ValueError('Omitted consumed pointer unexpectedly byte-matched')
    bad = (WORK / 'negative-link/caller.bin').read_bytes()
    controls = []
    for index in [0, 8, 16, 24, 32, 48, 96, 144]:
        item = recipes()[index]
        good, other = execute(original, native, item), execute(original, bad, item)
        assert good['modelPassed']
        controls.append(dict(recipe=item, original=good, wrong=other, actualReturns=2))
    assert any(not item['wrong']['modelPassed'] for item in controls)
    assert any(item['wrong']['modelPassed'] for item in controls)
    assert len([pc for pc in pcs if ENTRY <= pc < ENTRY + SIZE]) * 4 == 136
    row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=2 * len(results),
        actualNativeHelperReturns=2 * sum(len(item['result']['nativeHelperReturns']) for item in results),
        suppliedCalls=2 * sum(len(item['result']['suppliedCalls']) for item in results), observedCodeBytes=136, literalPoolBytes=4)
    write_json(REPORT, dict(romSha256=config['romSha256'], matches=rows, results=results,
        negativeControls=controls, wrongC=bad_rows[0], wrongLinkMismatch=mismatch,
        generator='match_main_reservation_pointer_20261031.py', generatorSha256=sha256(__file__),
        fixture=dict(path='main_reservation_pointer_fixture_20261031.py', sha256=sha256(ROOT / 'main_reservation_pointer_fixture_20261031.py')),
        limitations=['Synthetic backed slots0..7, full signed priorities, raw flags and handle/record aliasing',
                     'Actual detach24 and release152 execute; five mutex/cleanup/callback/reset boundary identities are supplied without memory writes',
                     'No complete scheduling, cleanup implementation, scene reachability, portable game or Android execution claim']))
    print(dict(bytes=SIZE, **row['nativeOracle'], negativeActualReturns=16))


if __name__ == '__main__':
    main()
