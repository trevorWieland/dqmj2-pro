import ast
import sys
import match_runtime as compiler
import save_link_snapshots
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_allocation_fixture_20261031 import SIZES, execute
from unicorn import __version__


UNITS = {0x0202A37C: ('20261031_allocation_dispatch_word_index', 3, True),
    0x0202B334: ('20261031_allocation_dispatch', 2, False)}
MUTATIONS = {0x0202A37C: ('native_data_020edd54[2] = 5;', 'native_data_020edd54[2] = 4;'),
    0x0202B334: ('(bytes + 3) & ~3U', '(bytes + 7) & ~7U')}


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    native = {entry: original[entry - 0x02000000:entry - 0x02000000 + size] for entry, size in SIZES.items()}
    matches, linked, bindings, symbols = [], {}, {}, {}
    for entry, size in SIZES.items():
        directory, optimization, speed = UNITS[entry]
        source = ROOT / f'src/runtime/{directory}/native_main_{entry:08x}.c'
        work = ROOT / f'work/main-allocation-dispatch-qualified-20261031/{entry:08x}'
        compiler.WORK = work / 'compile'
        rows, unused = compiler.compare(source, 'main', optimization, 'off', speed=speed)
        assert len(rows) == 1
        row = rows[0]
        typed = qualified_bindings(row)
        proof = validate(row, typed, work / 'link')
        save_link_snapshots.DIRECTORY = work / 'immutable-links'
        row.update(save_link_snapshots.freeze_link(proof))
        row.update(exactAfterRealMwLink=True, exactAfterGenuineLink=True, linkedMatchingBytes=size)
        linked[entry] = (work / 'link/caller.bin').read_bytes()
        assert linked[entry] == native[entry]
        matches.append(row)
        for name, value in typed.items():
            assert name not in bindings or bindings[name] == value
            symbols[name], bindings[name] = value['address'], value
    qualifications = []
    for row in matches:
        entry, size = int(row['address'], 0), row['bytes']
        cases, pcs = [], set()
        for index in range(1260 if entry == 0x0202A37C else 504):
            first, second = execute(original, native, entry, index), execute(original, linked, entry, index)
            assert first == second and first['modelPassed'], (hex(entry), index, first, second)
            pcs.update(first['pcs'])
            cases.append(dict(index=index, result=first, actualReturns=2))
        source = ROOT / row['source']
        before, after = MUTATIONS[entry]
        text = source.read_text()
        assert text.count(before) == 1
        wrong = text.replace(before, after, 1)
        negative = ROOT / f'nonmatching/main-runtime/20261031-allocation-dispatch-controls/{entry:08x}/source.c'
        negative.parent.mkdir(parents=True, exist_ok=True)
        assert not negative.exists() or negative.read_bytes() == wrong.encode()
        negative.write_bytes(wrong.encode())
        work = ROOT / f'work/main-allocation-dispatch-qualified-20261031/{entry:08x}'
        compiler.WORK = work / 'negative-compile'
        unused, optimization, speed = UNITS[entry]
        bad_rows, unused = compiler.compare(negative, 'main', optimization, 'off', speed=speed)
        try:
            validate(bad_rows[0], qualified_bindings(bad_rows[0]), work / 'negative-link')
        except ValueError as error:
            mismatch = ast.literal_eval(str(error))
        else:
            raise ValueError('Wrong C unexpectedly matched')
        bad = dict(linked)
        bad[entry] = (work / 'negative-link/caller.bin').read_bytes()
        controls = []
        for ordinal in range(140):
            index = ordinal * 3
            first, second = execute(original, native, entry, index), execute(original, bad, entry, index)
            assert first['modelPassed']
            controls.append(dict(index=index, original=first, wrong=second, actualReturns=2))
        assert any(not value['wrong']['modelPassed'] for value in controls)
        assert any(value['wrong']['modelPassed'] for value in controls)
        row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=2 * len(cases),
            observedOwnCodeBytes=sum(entry <= address < entry + size for address in pcs) * 4,
            originalOrSourceLinkedNestedReturns=sum(value['result']['nativeNestedReturns'] * 2 for value in cases),
            suppliedLowerCalls=sum(len(value['result']['calls']) * 2 for value in cases))
        qualifications.append(dict(address=hex(entry), cases=cases, wrongC=bad_rows[0], wrongLinkMismatch=mismatch, negativeControls=controls))
    write_json(ROOT / 'evidence/matches/main-allocation-dispatch-20261031.json', dict(
        romSha256=config['romSha256'], matches=matches, qualifications=qualifications,
        nativeSymbols=symbols, nativeSymbolEntries=bindings, newFunctions=2, newSourceBytes=220,
        limitations=['Slot/default/status bytes and allocation-count transitions are measured; names are local working descriptions',
            'Both ordinary C functions are patched together; only the two lower allocation outcomes are supplied, with no lower-body or real-heap correctness credit',
            'Supported indices0..255 and default signed byte; other words with low-byte-valid/full-word-out-of-range pointer arithmetic remain unproved',
            'Size rounding and signed alignment direction include modulo32 overflow and INT_MIN words under supplied lower contracts',
            'No original typedef/heap lifetime, scene reachability, source-only ROM, Windows or Android execution is claimed']))
    print(dict(functions=2, bytes=220, actualReturns=3528, negativeActualReturns=560))


if __name__ == '__main__':
    main()
