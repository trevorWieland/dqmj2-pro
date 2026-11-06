import ast
import sys
import match_decimal_double_runtime_20261031 as compiler
import save_link_snapshots
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_decimal_from_double_fixture_20261031 import ENTRY, SIZE, execute
EXPONENTS = list(range(96))
from unicorn import __version__


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    source = ROOT / 'src/runtime/20261031_decimal_from_double/native_main_02023568.c'
    work = ROOT / 'work/main-decimal-from-double-qualified-20261031'
    compiler.WORK = work / 'compile'
    rows, unused = compiler.compare(source, 'main', 3, 'on', True)
    assert len(rows) == 1
    row = rows[0]
    proof = validate(row, qualified_bindings(row), work / 'link')
    save_link_snapshots.DIRECTORY = work / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    row.update(exactAfterRealMwLink=True, exactAfterGenuineLink=True, linkedMatchingBytes=SIZE)
    native = original[ENTRY - 0x02000000:ENTRY - 0x02000000 + SIZE]
    code = (work / 'link/caller.bin').read_bytes()
    assert code == native
    cases, pcs = [], set()
    for index in range(len(EXPONENTS)):
        first, second = execute(original, native, index), execute(original, code, index)
        assert first == second and first['modelPassed']
        pcs.update(pc for pc in first['pcs'] if ENTRY <= pc < ENTRY + SIZE)
        cases.append(dict(index=index, result=first, actualReturns=2))
    assert len(pcs) * 4 == SIZE
    text = source.read_text()
    wrong = text.replace('pDecimal->sign = sign;', 'pDecimal->sign = sign ^ 1;', 1)
    assert wrong != text
    negative = ROOT / 'nonmatching/main-runtime/20261031-decimal-from-double-controls/source.c'
    negative.parent.mkdir(parents=True, exist_ok=True)
    assert not negative.exists() or negative.read_bytes() == wrong.encode()
    negative.write_bytes(wrong.encode())
    compiler.WORK = work / 'negative-compile'
    bad_rows, unused = compiler.compare(negative, 'main', 3, 'on', True)
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
    row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=2 * len(EXPONENTS),
        observedCodeBytes=SIZE, literalPoolBytes=0, actualNativeHelperReturns=2 * sum(len(case['result']['logicalNativeReturns']) - 1 for case in cases), suppliedCalls=0)
    write_json(ROOT / 'evidence/matches/main-decimal-from-double-20261031.json', dict(
        romSha256=config['romSha256'], matches=[row], cases=cases, negativeControls=controls,
        nativeSymbols={name: binding['address'] for name, binding in qualified_bindings(row).items()},
        nativeSymbolEntries=[dict(name=name, **binding) for name, binding in qualified_bindings(row).items()],
        wrongC=bad_rows[0], wrongLinkMismatch=mismatch, limitations=[
            '96 exact binary64 edge/random encodings, signed zero/subnormal/finite/infinity/NaN; integer significand decomposition and measured per-step32-digit model',
            'Measured input double usesR1:R2 after outputR0; original arithmetic/conversion/classification helpers execute; no new callee source credit',
            'Void API; physical registers compared without promotingR0 residue; no exhaustive rounding or caller reachability, secondary device or game proof']))
    print(dict(functions=1, bytes=SIZE, actualReturns=2 * len(EXPONENTS), negativeActualReturns=128))


if __name__ == '__main__':
    main()
