import ast
import sys
import match_runtime as compiler
import save_link_snapshots
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_field_width_fixture_20261031 import SIZES, recipes, execute
from unicorn import __version__

WORK = ROOT / 'work/main-field-widths-20261031'
REPORT = ROOT / 'evidence/matches/main-field-widths-20261031.json'


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    assert int.from_bytes(original[0x37768:0x3776C], 'little') == 0x020F1EC8
    assert int.from_bytes(original[0x3776C:0x37770], 'little') == 0x020F1F10
    matches, qualifications = [], []
    for entry, size in SIZES.items():
        source = ROOT / f'src/runtime/20261031_field_widths/native_main_{entry:08x}.c'
        directory = WORK / f'{entry:08x}'
        compiler.WORK = directory / 'compile'
        rows, unused = compiler.compare(source, 'main', 2, 'off')
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
        for item in recipes():
            first, second = execute(original, entry, native, item), execute(original, entry, code, item)
            assert first == second and first['modelPassed'], (hex(entry), item, first)
            pcs.update(first['pcs'])
            cases.append(dict(recipe=item, result=first, actualReturns=2))
        text = source.read_text()
        if entry == 0x02037750:
            wrong = text.replace('*(u32 *)native_data_020f1f10 =', '*native_data_020f1f10 =')
        else:
            wrong = text.replace('(u8 *)arg0 + 4,', 'arg0 + 4,')
        assert wrong != text
        negative = ROOT / f'nonmatching/main-runtime/20261031-field-widths-negative/{entry:08x}/source.c'
        negative.parent.mkdir(parents=True, exist_ok=True)
        assert not negative.exists() or negative.read_bytes() == wrong.encode()
        negative.write_bytes(wrong.encode())
        compiler.WORK = directory / 'negative-compile'
        bad_rows, unused = compiler.compare(negative, 'main', 2, 'off')
        assert len(bad_rows) == 1
        try:
            validate(bad_rows[0], qualified_bindings(bad_rows[0]), directory / 'negative-link')
        except ValueError as error:
            mismatch = ast.literal_eval(str(error))
            assert mismatch['linkedBytes'] == size and mismatch['matchingBytes'] == size - 1
        else:
            raise ValueError('Wrong field scale/store width unexpectedly matched')
        bad = (directory / 'negative-link/caller.bin').read_bytes()
        controls = []
        for item in recipes()[:12]:
            good, other = execute(original, entry, native, item), execute(original, entry, bad, item)
            assert good['modelPassed']
            controls.append(dict(recipe=item, original=good, wrong=other, actualReturns=2))
        assert any(not item['wrong']['modelPassed'] for item in controls)
        observed = len([pc for pc in pcs if entry <= pc < entry + size]) * 4
        assert observed == size - (8 if entry == 0x02037750 else 0)
        row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=2 * len(cases),
            actualPhysicalNativeHelperReturns=2 * sum(len(case['result']['physicalNativeHelperReturns']) for case in cases),
            logicalThunkEntries=2 * sum(case['result']['logicalThunkEntries'] for case in cases),
            suppliedCalls=2 * sum(len(case['result']['suppliedCalls']) for case in cases),
            observedCodeBytes=observed, literalPoolBytes=size - observed)
        matches.append(row)
        qualifications.append(dict(address=hex(entry), cases=cases, negativeControls=controls,
                                   wrongC=bad_rows[0], wrongLinkMismatch=mismatch))
    write_json(REPORT, dict(romSha256=config['romSha256'], matches=matches, qualifications=qualifications,
        generator='match_main_field_widths_20261031.py', generatorSha256=sha256(__file__),
        fixture=dict(path='main_field_width_fixture_20261031.py', sha256=sha256(ROOT / 'main_field_width_fixture_20261031.py')),
        limitations=['Synthetic backed manager/node pages; the single allocator boundary returns a backed20-byte node or null without memory writes',
                     'Original list initialization/append helpers execute; the12-byte trampoline is counted as an entry rather than a second physical return',
                     'No allocator implementation, scene reachability, Windows game or Android execution claim']))
    print(dict(functions=len(matches), bytes=sum(row['bytes'] for row in matches),
               actualReturns=sum(row['nativeOracle']['actualReturns'] for row in matches),
               physicalNativeHelperReturns=sum(row['nativeOracle']['actualPhysicalNativeHelperReturns'] for row in matches),
               negativeActualReturns=72))


if __name__ == '__main__':
    main()
