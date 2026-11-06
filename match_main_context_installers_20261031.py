import ast
import sys
from project import ROOT, configuration, write_json, sha256
import match_runtime as compiler
from unicorn import __version__
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_context_installers_fixture_20261031 import VARIANTS, recipes, execute, compact

WORK = ROOT / 'work/main-context-installers-20261031'
REPORT = ROOT / 'evidence/matches/main-context-installers-20261031.json'


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    matches, evidence = [], []
    for variant in VARIANTS:
        entry, size, bit, destination = variant
        source = ROOT / f'src/runtime/20261031_context_installers/native_main_{entry:08x}.c'
        compiler.WORK = WORK / hex(entry) / 'compile'
        rows, unused = compiler.compare(source, 'main', 2, 'off', True)
        assert len(rows) == 1 and rows[0]['compiledBytes'] == size
        row = rows[0]
        directory = WORK / hex(entry) / 'link'
        proof = validate(row, qualified_bindings(row), directory)
        save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
        row.update(save_link_snapshots.freeze_link(proof))
        row.update(exactAfterRealMwLink=True, exactAfterGenuineLink=True, linkedMatchingBytes=size)
        native = original[entry - 0x02000000:entry - 0x02000000 + size]
        code = (directory / 'caller.bin').read_bytes()
        assert code == native
        results, pcs = [], set()
        for item in recipes():
            first, second = execute(original, native, variant, item), execute(original, code, variant, item)
            assert first == second and first['modelPassed'], (hex(entry), item, compact(first))
            pcs.update(first['pcs'])
            results.append(dict(recipe=item, result=compact(first), actualReturns=2))
        text = source.read_text(encoding='utf-8')
        wrong = text.replace(f'0xA) | {bit})', f'0xA) | {bit << 1})')
        assert wrong != text
        negative = ROOT / f'nonmatching/main-runtime/20261031-context-installers-negative/{hex(entry)}/source.c'
        negative.parent.mkdir(parents=True, exist_ok=True)
        assert not negative.exists() or negative.read_bytes() == wrong.encode()
        negative.write_bytes(wrong.encode())
        compiler.WORK = WORK / hex(entry) / 'negative-compile'
        bad_rows, unused = compiler.compare(negative, 'main', 2, 'off', True)
        assert len(bad_rows) == 1 and bad_rows[0]['compiledBytes'] == size
        bad_directory = WORK / hex(entry) / 'negative-link'
        try:
            validate(bad_rows[0], qualified_bindings(bad_rows[0]), bad_directory)
        except ValueError as error:
            mismatch = ast.literal_eval(str(error))
            assert mismatch['linkedBytes'] == size and mismatch['matchingBytes'] == size - 1
        else:
            raise ValueError('Wrong-C source unexpectedly matched')
        bad = (bad_directory / 'caller.bin').read_bytes()
        controls = []
        for index, flow in enumerate(['allocated', 'provided']):
            item = dict(index=9000 + index, active=1, descriptor=True, query=0, flow=flow, count=1)
            first, second = execute(original, native, variant, item), execute(original, bad, variant, item)
            assert first['modelPassed'] and second['modelPassed'] == bool(index)
            controls.append(dict(recipe=item, original=compact(first), wrong=compact(second), actualReturns=2))
        observed = {pc for pc in pcs if entry <= pc < entry + size}
        assert len(observed) * 4 == size
        row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=2 * len(results),
            actualNativeHelperReturns=2 * sum(item['result']['actualNativeHelperReturns'] for item in results),
            suppliedHeapCompletions=2 * sum(item['result']['providerCounts']['heap'] for item in results),
            suppliedRefreshCompletions=2 * sum(item['result']['providerCounts']['refresh'] for item in results),
            observedCodeBytes=size, literalPoolBytes=0)
        matches.append(row)
        evidence.append(dict(address=hex(entry), results=results, observedPcs=sorted(pcs),
                             negativeControls=controls, wrongC=bad_rows[0], wrongLinkMismatch=mismatch))
        print(dict(address=hex(entry), **row['nativeOracle']), flush=True)
    write_json(REPORT, dict(romSha256=config['romSha256'], matches=matches, evidence=evidence,
        generator='match_main_context_installers_20261031.py', generatorSha256=sha256(__file__),
        fixture=dict(path='main_context_installers_fixture_20261031.py', sha256=sha256(ROOT/'main_context_installers_fixture_20261031.py')),
        limitations=['Synthetic three-entry descriptor and empty destination lists; custom initialization table count explicitly0',
                     'Original query/allocation-size/initializer/list helpers execute and receive no new source credit',
                     'Lower heap callback and 020290C8 no-write refresh completion are explicit providers',
                     'No complete geometry, allocator, factory callback, malformed descriptor or live-game behavior claimed']))
    print(dict(functions=3, bytes=416, actualReturns=sum(r['nativeOracle']['actualReturns'] for r in matches), negativeActualReturns=12))


if __name__ == '__main__':
    main()
