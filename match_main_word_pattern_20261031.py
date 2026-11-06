import ast
import sys
from project import ROOT, configuration, write_json, sha256
import match_runtime as compiler
from unicorn import __version__
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_word_pattern_fixture_20261031 import ENTRY, SIZE, HELPER, recipes, execute

SOURCE = ROOT / 'src/runtime/20261031_word_pattern/native_main_0203c5b8.c'
WORK = ROOT / 'work/main-word-pattern-20261031'
REPORT = ROOT / 'evidence/matches/main-word-pattern-20261031.json'


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
    assert native == code
    results = []
    for item in recipes():
        first, second = execute(original, native, item), execute(original, code, item)
        assert first == second and first['modelPassed']
        results.append(dict(recipe=item, result=first, actualReturns=2))
    negative = ROOT / 'nonmatching/main-runtime/20261031-word-pattern-negative/source.c'
    text = SOURCE.read_text(encoding='utf-8')
    wrong = text.replace('M2C_FIELD(var_r4, s32 **, 0) + 1', 'M2C_FIELD(var_r4, s32 **, 0) + 4')
    assert wrong != text
    negative.parent.mkdir(parents=True, exist_ok=True)
    if negative.exists() and negative.read_bytes() != wrong.encode():
        raise ValueError('Earlier wrong-stride source differs')
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
        raise ValueError('Wrong-stride source unexpectedly matched')
    bad = (WORK / 'negative-link/caller.bin').read_bytes()
    controls = []
    for index, mode in enumerate([1, 0]):
        item = dict(index=9000 + index, count=4, default=bool(index), mode=mode)
        first, second = execute(original, native, item), execute(original, bad, item)
        assert first['modelPassed'] and second['modelPassed'] == bool(index)
        controls.append(dict(recipe=item, original=first, wrong=second, actualReturns=2))
    own = {pc for item in results for pc in item['result']['pcs'] if ENTRY <= pc < ENTRY + SIZE}
    helper = {pc for item in results for pc in item['result']['pcs'] if HELPER <= pc < HELPER + 76}
    assert len(own) * 4 == SIZE - 8 and len(helper) * 4 == 76
    row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True,
        actualReturns=2 * len(results), actualNativeHelperReturns=2 * sum(item['recipe']['count'] > 0 for item in results),
        suppliedHelpers=0, observedCodeBytes=len(own) * 4, literalPoolBytes=8)
    write_json(REPORT, dict(romSha256=config['romSha256'], matches=rows, results=results,
        negativeControls=controls, negativeCompiled=bad_rows[0], negativeLinkMismatch=mismatch,
        helper=dict(address=hex(HELPER), originalBytes=76,
                    originalSha256=compiler.sha(original[HELPER-0x02000000:HELPER-0x02000000+76])),
        generator='match_main_word_pattern_20261031.py', generatorSha256=sha256(__file__),
        fixture=dict(path='main_word_pattern_fixture_20261031.py', sha256=sha256(ROOT/'main_word_pattern_fixture_20261031.py')),
        limitations=['Valid aligned buffer with count1..64; nonpositive signed counts are checked without buffer writes',
            'The record is only a measured pointer/count/byte prefix, not a complete object or semantic label',
            'Original fill helper executes and receives no reconstructed source credit; no hardware or full-game claim']))
    print(dict(bytes=SIZE, actualReturns=row['nativeOracle']['actualReturns'],
               actualHelperReturns=row['nativeOracle']['actualNativeHelperReturns'], negativeActualReturns=4))


if __name__ == '__main__':
    main()
