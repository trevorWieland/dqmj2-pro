import ast
import sys
import match_runtime as compiler
import save_link_snapshots
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_decimal_family_fixture_20261031 import SIZES, recipes, execute
from unicorn import __version__

WORK = ROOT / 'work/main-decimal-family-qualified-20261031'
REPORT = ROOT / 'evidence/matches/main-decimal-family-20261031.json'


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    matches, qualifications = [], []
    for entry, size in SIZES.items():
        source = ROOT / f'src/runtime/20261031_decimal_family/native_main_{entry:08x}.c'
        directory = WORK / f'{entry:08x}'
        compiler.WORK = directory / 'compile'
        rows, unused = compiler.compare(source, 'main', 3, 'off', True)
        assert len(rows) == 1
        row = rows[0]
        proof = validate(row, qualified_bindings(row), directory / 'link')
        save_link_snapshots.DIRECTORY = directory / 'immutable-links'
        row.update(save_link_snapshots.freeze_link(proof))
        row.update(exactAfterRealMwLink=True, exactAfterGenuineLink=True, linkedMatchingBytes=size)
        native = original[entry - 0x02000000:entry - 0x02000000 + size]
        code = (directory / 'link/caller.bin').read_bytes()
        assert code == native
        cases, pcs = [], set()
        for item in recipes(entry):
            first, second = execute(original, entry, native, item), execute(original, entry, code, item)
            assert first == second and first['modelPassed'], (hex(entry), item)
            pcs.update(first['pcs'])
            cases.append(dict(recipe=item, result=first, actualReturns=2))
        text = source.read_text()
        if entry in [0x02023104, 0x020231E4]:
            wrong = text.replace('return 1;', 'return 2;', 1)
        elif entry == 0x02022CE4:
            wrong = text.replace("*pStr++ - '0'", "*pStr++ - '1'", 1)
        else:
            wrong = text.replace('accumulator % 10', 'accumulator % 9', 1)
        assert wrong != text
        negative = ROOT / f'nonmatching/main-runtime/20261031-decimal-family-negative/{entry:08x}/source.c'
        negative.parent.mkdir(parents=True, exist_ok=True)
        assert not negative.exists() or negative.read_bytes() == wrong.encode()
        negative.write_bytes(wrong.encode())
        compiler.WORK = directory / 'negative-compile'
        bad_rows, unused = compiler.compare(negative, 'main', 3, 'off', True)
        assert len(bad_rows) == 1
        try:
            validate(bad_rows[0], qualified_bindings(bad_rows[0]), directory / 'negative-link')
        except ValueError as error:
            mismatch = ast.literal_eval(str(error))
        else:
            raise ValueError('Wrong decimal C unexpectedly matched')
        bad = (directory / 'negative-link/caller.bin').read_bytes()
        controls = []
        for item in recipes(entry)[:24]:
            if entry == 0x02022B60 and item['index'] == 0:
                item = dict(item, unitProduct=True)
            good, other = execute(original, entry, native, item), execute(original, entry, bad, item)
            assert good['modelPassed']
            controls.append(dict(recipe=item, original=good, wrong=other, actualReturns=2))
        assert any(not item['wrong']['modelPassed'] for item in controls)
        assert any(item['wrong']['modelPassed'] for item in controls), hex(entry)
        observed = len([pc for pc in pcs if entry <= pc < entry + size]) * 4
        assert observed == size - (4 if entry == 0x02022B60 else 0)
        row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=2 * len(cases),
            actualNativeHelperReturns=2 * sum(len(case['result']['helperReturns']) for case in cases),
            suppliedCalls=0, observedCodeBytes=observed, literalPoolBytes=size - observed)
        matches.append(row)
        qualifications.append(dict(address=hex(entry), cases=cases, negativeControls=controls,
            wrongC=bad_rows[0], wrongLinkMismatch=mismatch))
    write_json(REPORT, dict(romSha256=config['romSha256'], matches=matches, qualifications=qualifications,
        generator='match_main_decimal_family_20261031.py', generatorSha256=sha256(__file__),
        fixture=dict(path='main_decimal_family_fixture_20261031.py', sha256=sha256(ROOT / 'main_decimal_family_fixture_20261031.py')),
        reference=dict(path='provenance/msl-ansi-reference-20261031.json', sha256=sha256(ROOT / 'provenance/msl-ansi-reference-20261031.json')),
        limitations=['Normalized1..32-digit positive magnitude records, zero sentinels and supported output/input aliasing; sign ignored by comparison semantics',
                     'Conversion includes measured raw next-byte comparisons with numeric5; no conventional text-rounding/API meaning inferred',
                     'Original rounding helper executes with zero extra callee credit; independent integer products/comparisons and bounded byte conversion models',
                     'Unused output bytes compared original/source; numeric fields and padding modeled independently; no Windows/Android game execution']))
    print(dict(functions=4, bytes=sum(row['bytes'] for row in matches),
               actualReturns=sum(row['nativeOracle']['actualReturns'] for row in matches), negativeActualReturns=192))


if __name__ == '__main__':
    main()
