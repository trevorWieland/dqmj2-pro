import ast
import sys
import match_runtime as compiler
import save_link_snapshots
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_decimal_round_direction_fixture_20261031 import ENTRY, SIZE, execute
from unicorn import __version__


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    source = ROOT / 'src/runtime/20261031_decimal_round_helpers/native_main_02022998.c'
    work = ROOT / 'work/main-decimal-round-direction-qualified-20261031'
    compiler.WORK = work / 'compile'
    rows, unused = compiler.compare(source, 'main', 3, 'off', True)
    assert len(rows) == 1
    row = rows[0]
    proof = validate(row, qualified_bindings(row), work / 'link')
    save_link_snapshots.DIRECTORY = work / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    row.update(exactAfterRealMwLink=True, exactAfterGenuineLink=True, linkedMatchingBytes=SIZE)
    native = original[ENTRY - 0x02000000:ENTRY - 0x02000000 + SIZE]
    code = (work / 'link/caller.bin').read_bytes()
    assert code == native and not row['relocations']
    cases, pcs = [], set()
    for index in range(512):
        first, second = execute(original, native, index), execute(original, code, index)
        assert first == second and first['modelPassed']
        pcs.update(first['pcs'])
        cases.append(dict(index=index, result=first, actualReturns=2))
    assert len(pcs) * 4 == SIZE
    text = source.read_text()
    wrong = text.replace('if (*i > 5)', 'if (*i > 6)', 1)
    assert wrong != text
    negative = ROOT / 'nonmatching/main-runtime/20261031-decimal-round-direction-negative/source.c'
    negative.parent.mkdir(parents=True, exist_ok=True)
    assert not negative.exists() or negative.read_bytes() == wrong.encode()
    negative.write_bytes(wrong.encode())
    compiler.WORK = work / 'negative-compile'
    bad_rows, unused = compiler.compare(negative, 'main', 3, 'off', True)
    try:
        validate(bad_rows[0], qualified_bindings(bad_rows[0]), work / 'negative-link')
    except ValueError as error:
        mismatch = ast.literal_eval(str(error))
    else:
        raise ValueError('Wrong C unexpectedly matched')
    bad = (work / 'negative-link/caller.bin').read_bytes()
    controls = []
    for index in range(64):
        good, other = execute(original, native, index), execute(original, bad, index)
        assert good['modelPassed']
        controls.append(dict(index=index, original=good, wrong=other, actualReturns=2))
    assert any(not item['wrong']['modelPassed'] for item in controls)
    assert any(item['wrong']['modelPassed'] for item in controls)
    row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=1024,
        observedCodeBytes=SIZE, literalPoolBytes=0, actualNativeHelperReturns=0, suppliedCalls=0)
    write_json(ROOT / 'evidence/matches/main-decimal-round-direction-20261031.json', dict(
        romSha256=config['romSha256'], matches=[row], cases=cases, negativeControls=controls,
        wrongC=bad_rows[0], wrongLinkMismatch=mismatch, limitations=[
            'Numeric digits0..9, lengths2..32, positions1..length-1 only',
            'No malformed records, decimal sign meaning, caller reachability or whole-game proof']))
    print(dict(functions=1, bytes=SIZE, actualReturns=1024, negativeActualReturns=128))


if __name__ == '__main__':
    main()
