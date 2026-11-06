import ast
import sys
import match_runtime as compiler
import save_link_snapshots
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_forwarding_fixture_20261031 import SIZES, execute
from unicorn import __version__


SOURCES = {0x02038148: '20261031_separate_handle_read', 0x0202A44C: '20261031_measured_input_forwarding'}
MUTATIONS = {0x02038148: ('*volatile *handle', '**handle'),
    0x0202A44C: ('native_fn_0202a37c(heap, bytes, alignment)', 'native_fn_0202a37c(heap, bytes, 0)')}


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    matches, qualifications, symbols, bindings = [], [], {}, {}
    for entry, size in SIZES.items():
        source = ROOT / f'src/runtime/{SOURCES[entry]}/native_main_{entry:08x}.c'
        work = ROOT / f'work/main-measured-forwarding-qualified-20261031/{entry:08x}'
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
        for index in range(768 if entry == 0x02038148 else 280):
            first, second = execute(original, native, entry, index), execute(original, code, entry, index)
            assert first == second and first['modelPassed'], (hex(entry), index, first, second)
            pcs.update(first['pcs'])
            cases.append(dict(index=index, result=first, actualReturns=2))
        before, after = MUTATIONS[entry]
        text = source.read_text()
        assert text.count(before) == 1
        wrong = text.replace(before, after, 1)
        negative = ROOT / f'nonmatching/main-runtime/20261031-measured-forwarding-controls/{entry:08x}/source.c'
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
        for ordinal in range(64):
            index = ordinal * 13 % (768 if entry == 0x02038148 else 280)
            first, second = execute(original, native, entry, index), execute(original, bad, entry, index)
            assert first['modelPassed']
            controls.append(dict(index=index, original=first, wrong=second, actualReturns=2))
        assert any(not value['wrong']['modelPassed'] for value in controls)
        assert any(value['wrong']['modelPassed'] for value in controls)
        row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=2 * len(cases),
            observedOwnCodeBytes=sum(entry <= address < entry + size for address in pcs) * 4,
            actualNativeHelperReturns=sum(len(value['result']['nativeHelperReturns']) * 2 for value in cases),
            suppliedCalls=sum(sum(call['supplied'] for call in value['result']['calls']) * 2 for value in cases))
        row.update(newFunctionCredit=int(entry == 0x02038148), newByteCredit=44 if entry == 0x02038148 else 0)
        matches.append(row)
        qualifications.append(dict(address=hex(entry), cases=cases, wrongC=bad_rows[0], wrongLinkMismatch=mismatch, negativeControls=controls))
        for name, value in typed.items():
            assert name not in bindings or bindings[name] == value
            symbols[name], bindings[name] = value['address'], value
    write_json(ROOT / 'evidence/matches/main-measured-forwarding-20261031.json', dict(
        romSha256=config['romSha256'], matches=matches, qualifications=qualifications,
        nativeSymbols=symbols, nativeSymbolEntries=bindings, newFunctions=1, newSourceBytes=44, zeroCreditMigrationBytes=40,
        limitations=['The44-byte handle wrapper uses a minimum volatile pointer-read view to preserve two separately observed native loads',
            'Replacing the handle between reads is an explicitly supplied synthetic schedule, not an observed game IRQ or lifecycle claim',
            'Original379C4 and memset8D78 execute; timestamp379EC and allocation2A37C outcomes are supplied and receive zero helper credit',
            'The40-byte allocation wrapper migration restores consumed heap/size/alignment inputs while preserving every byte and original source',
            'No original C qualifiers/formal names, heap correctness, whole-scene, source-only ROM or Windows/Android execution is claimed']))
    print(dict(newFunctions=1, newBytes=44, migrationBytes=40, actualReturns=2096, negativeActualReturns=256))


if __name__ == '__main__':
    main()
