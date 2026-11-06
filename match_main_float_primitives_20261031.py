import ast
import sys
import match_float_primitives_runtime_20261031 as compiler
import save_link_snapshots
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_float_primitives_fixture_20261031 import SIZES, execute
from unicorn import __version__


MUTATIONS = {
    0x0202263C: ('0x80000000', '0x40000000'),
    0x02022684: ('*ptr = -54;', '*ptr = -53;'),
    0x02022740: ('1.80143985094819840000e+16', '9.00719925474099200000e+15'),
    0x02023E48: ('0x80000000', '0x00000000'),
    0x02023E5C: ('return 4;', 'return 6;'),
}


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    matches, qualifications, symbols, bindings = [], [], {}, {}
    for entry, size in SIZES.items():
        source = ROOT / f'src/runtime/20261031_float_primitives/native_main_{entry:08x}.c'
        work = ROOT / f'work/main-float-primitives-qualified-20261031/{entry:08x}'
        compiler.WORK = work / 'compile'
        rows, unused = compiler.compare(source, 'main', 3, 'off', True)
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
        for index in range(160):
            first, second = execute(original, entry, native, index), execute(original, entry, code, index)
            assert first == second and first['modelPassed'], (hex(entry), index)
            pcs.update(pc for pc in first['pcs'] if entry <= pc < entry + size)
            cases.append(dict(index=index, result=first, actualReturns=2))
        text = source.read_text()
        old, replacement = MUTATIONS[entry]
        wrong = text.replace(old, replacement, 1)
        assert wrong != text
        negative = ROOT / f'nonmatching/main-runtime/20261031-float-primitives-controls/{entry:08x}/source.c'
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
        for index in range(32):
            good, other = execute(original, entry, native, index), execute(original, entry, bad, index)
            assert good['modelPassed']
            controls.append(dict(index=index, original=good, wrong=other, actualReturns=2))
        assert any(not case['wrong']['modelPassed'] for case in controls), hex(entry)
        assert any(case['wrong']['modelPassed'] for case in controls), hex(entry)
        row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=320,
            suppliedCalls=0, observedOwnInstructionBytes=len(pcs) * 4,
            poolOrUnobservedBytes=size - len(pcs) * 4,
            logicalNativeDependencyReturns=2 * sum(len(case['result']['logicalNativeReturns']) - 1 for case in cases))
        matches.append(row)
        qualifications.append(dict(address=hex(entry), cases=cases, negativeControls=controls,
            wrongC=bad_rows[0], wrongLinkMismatch=mismatch))
        for name, binding in typed.items():
            assert name not in bindings or bindings[name] == binding
            bindings[name] = binding
            symbols[name] = binding['address']
    write_json(ROOT / 'evidence/matches/main-float-primitives-20261031.json', dict(
        romSha256=config['romSha256'], matches=matches, qualifications=qualifications,
        nativeSymbols=symbols, nativeSymbolEntries=bindings,
        generator='match_main_float_primitives_20261031.py', generatorSha256=sha256(__file__),
        reference=dict(path='provenance/msl-math-reference-20261031.json',
            sha256=sha256(ROOT / 'provenance/msl-math-reference-20261031.json')),
        limitations=['160 deterministic binary64 edge/random cases per unit are not exhaustive',
            'Sign query returns the raw high-word mask, not a normalized boolean',
            'Scale samples include50001/-50001 but exclude signed exponent-addition overflow',
            'Unvisited/dead branches and pools are not claimed as executed code',
            'Original arithmetic/classification helpers execute, no providers or added callee credit',
            'No Windows/Android game or scene execution']))
    print(dict(functions=5, bytes=948, actualReturns=1600, negativeActualReturns=320))


if __name__ == '__main__':
    main()
