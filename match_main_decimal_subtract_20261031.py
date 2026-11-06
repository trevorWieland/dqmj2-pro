import ast
import sys
import match_runtime as compiler
import save_link_snapshots
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_decimal_subtract_fixture_20261031 import ENTRY, SIZE, recipes, execute
from unicorn import __version__

SOURCE = ROOT / 'src/runtime/20261031_decimal_subtract/native_main_020232c4.c'
WORK = ROOT / 'work/main-decimal-subtract-20261031'
REPORT = ROOT / 'evidence/matches/main-decimal-subtract-20261031.json'


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    compiler.WORK = WORK / 'compile'
    rows, unused = compiler.compare(SOURCE, 'main', 3, 'off', True)
    assert len(rows) == 1
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
        assert first == second and first['modelPassed'], item
        pcs.update(first['pcs'])
        results.append(dict(recipe=item, result=first, actualReturns=2))
    text = SOURCE.read_text()
    assert text.count('*++k += 10;') == 2
    wrong = text.replace('*++k += 10;', '*++k += 9;', 1)
    negative = ROOT / 'nonmatching/main-runtime/20261031-decimal-subtract-negative/source.c'
    negative.parent.mkdir(parents=True, exist_ok=True)
    assert not negative.exists() or negative.read_bytes() == wrong.encode()
    negative.write_bytes(wrong.encode())
    compiler.WORK = WORK / 'negative-compile'
    bad_rows, unused = compiler.compare(negative, 'main', 3, 'off', True)
    assert len(bad_rows) == 1
    try:
        validate(bad_rows[0], qualified_bindings(bad_rows[0]), WORK / 'negative-link')
    except ValueError as error:
        mismatch = ast.literal_eval(str(error))
        assert mismatch['linkedBytes'] == SIZE and mismatch['matchingBytes'] == SIZE - 1
    else:
        raise ValueError('Wrong decimal borrow base unexpectedly matched')
    bad = (WORK / 'negative-link/caller.bin').read_bytes()
    controls = []
    for index in [0, 1, 19, 384, 387, 389, 392]:
        item = recipes()[index]
        good, other = execute(original, native, item), execute(original, bad, item)
        assert good['modelPassed']
        controls.append(dict(recipe=item, original=good, wrong=other, actualReturns=2))
    assert any(not case['wrong']['modelPassed'] for case in controls)
    assert any(case['wrong']['modelPassed'] for case in controls)
    assert len(pcs) * 4 == SIZE
    row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=2 * len(results),
        actualNativeHelperReturns=0, suppliedCalls=0, observedCodeBytes=SIZE, literalPoolBytes=0)
    write_json(REPORT, dict(romSha256=config['romSha256'], matches=rows, results=results,
        negativeControls=controls, wrongC=bad_rows[0], wrongLinkMismatch=mismatch,
        generator='match_main_decimal_subtract_20261031.py', generatorSha256=sha256(__file__),
        fixture=dict(path='main_decimal_subtract_fixture_20261031.py', sha256=sha256(ROOT / 'main_decimal_subtract_fixture_20261031.py')),
        reference=dict(path='provenance/msl-ansi-reference-20261031.json', sha256=sha256(ROOT / 'provenance/msl-ansi-reference-20261031.json')),
        limitations=['Normalized positive magnitude arrays1..32 digits; exponent difference0..31, strict positive supported result, zero subtrahend and output/input alias',
                     'Independent integer model retains measured discarded-digit correction; conventional nearest rounding failed characterization and is not asserted',
                     'Unused output digit bytes are compared original/source; independent model covers numeric fields, copied sign/padding and write bounds',
                     'Complete393 synthetic pairs do not prove every double-conversion caller, invalid/equal operands, broader exponent differences or scene reachability',
                     'Void interface; physical registers compared without promoting incidentalR0 to API semantics; no native Windows/Android execution yet']))
    print(dict(bytes=SIZE, **row['nativeOracle'], negativeActualReturns=2 * len(controls)))


if __name__ == '__main__':
    main()
