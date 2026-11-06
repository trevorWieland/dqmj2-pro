import ast
import sys
import match_runtime as compiler
import save_link_snapshots
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_state_dispatch_fixture_20261031 import SIZES, execute
from unicorn import __version__


MUTATIONS = {0x0203FCEC: ('= 0xD;', '= 0xC;'), 0x0203D52C: ('| 0xF00;', '| 0xE00;')}


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    unused, overlay, unused = measured_module('ov000')
    matches, qualifications, symbols, bindings = [], [], {}, {}
    for entry, size in SIZES.items():
        source = ROOT / f'src/runtime/20261031_main_state_dispatch/native_main_{entry:08x}.c'
        work = ROOT / f'work/main-state-dispatch-qualified-20261031/{entry:08x}'
        compiler.WORK = work / 'compile'
        rows, unused = compiler.compare(source, 'main', 2, 'off')
        assert len(rows) == 1
        row = rows[0]
        typed = qualified_bindings(row)
        proof = validate(row, typed, work / 'link')
        save_link_snapshots.DIRECTORY = work / 'immutable-links'
        row.update(save_link_snapshots.freeze_link(proof))
        row.update(exactAfterRealMwLink=True, exactAfterGenuineLink=True, linkedMatchingBytes=size)
        native = original[entry - 0x02000000:entry - 0x02000000 + size]
        code = (work / 'link/caller.bin').read_bytes()
        assert code == native
        cases, pcs = [], set()
        for index in range(256 if entry == 0x0203FCEC else 96):
            first, second = execute(original, overlay, native, entry, index), execute(original, overlay, code, entry, index)
            assert first == second and first['modelPassed']
            pcs.update(first['pcs'])
            cases.append(dict(index=index, result=first, actualReturns=2))
        before, after = MUTATIONS[entry]
        text = source.read_text()
        assert text.count(before) == 1
        wrong = text.replace(before, after, 1)
        negative = ROOT / f'nonmatching/main-runtime/20261031-main-state-dispatch-controls/{entry:08x}/source.c'
        negative.parent.mkdir(parents=True, exist_ok=True)
        assert not negative.exists() or negative.read_bytes() == wrong.encode()
        negative.write_bytes(wrong.encode())
        compiler.WORK = work / 'negative-compile'
        bad_rows, unused = compiler.compare(negative, 'main', 2, 'off')
        try:
            validate(bad_rows[0], qualified_bindings(bad_rows[0]), work / 'negative-link')
        except ValueError as error:
            mismatch = ast.literal_eval(str(error))
        else:
            raise ValueError('Wrong C unexpectedly matched')
        bad = (work / 'negative-link/caller.bin').read_bytes()
        controls = []
        for index in range(32):
            first, second = execute(original, overlay, native, entry, index), execute(original, overlay, bad, entry, index)
            assert first['modelPassed']
            controls.append(dict(index=index, original=first, wrong=second, actualReturns=2))
        assert any(not value['wrong']['modelPassed'] for value in controls)
        row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=2 * len(cases),
            observedOwnCodeBytes=len(pcs) * 4, actualNativeHelperReturns=0,
            suppliedCalls=sum(len(value['result']['calls']) * 2 for value in cases), signatureConfidence='Void matching view; no original C formal-type claim')
        matches.append(row)
        qualifications.append(dict(address=hex(entry), cases=cases, wrongC=bad_rows[0], wrongLinkMismatch=mismatch, negativeControls=controls))
        for name, value in typed.items():
            assert name not in bindings or bindings[name] == value
            symbols[name], bindings[name] = value['address'], value
    write_json(ROOT / 'evidence/matches/main-state-dispatch-20261031.json', dict(
        romSha256=config['romSha256'], matches=matches, qualifications=qualifications,
        nativeSymbols=symbols, nativeSymbolEntries=bindings, overlayContext='ov000',
        limitations=['Both source bodies and genuine linker bytes match; bounded original/source own effects and explicit call arguments agree',
            'All helper outcomes are supplied register contracts, with no helper-body, VRAM clear, scene entry or hardware execution credit',
            'MMIO is disposable synthetic mapped RAM; byte6054+8 modes cover all256 raw values, no semantic mode names inferred',
            'No whole-scene, original C formal-signature, Windows/Android game or source-only ROM proof']))
    print(dict(functions=2, bytes=564, actualReturns=704, negativeActualReturns=128))


if __name__ == '__main__':
    main()
