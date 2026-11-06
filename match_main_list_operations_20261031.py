import ast
import sys
from project import ROOT, configuration, write_json, sha256
import match_runtime as compiler
from unicorn import __version__
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_list_operations_fixture_20261031 import REMOVE, SEARCH, INSERT, recipes, execute, initial

WORK = ROOT / 'work/main-list-operations-20261031'
REPORT = ROOT / 'evidence/matches/main-list-operations-20261031.json'


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    matches, evidence = [], []
    for kind, entry, size in [('remove', REMOVE, 116), ('search', SEARCH, 104), ('insert', INSERT, 184)]:
        source = ROOT / f'src/runtime/20261031_list_operations/native_main_{entry:08x}.c'
        compiler.WORK = WORK / kind / 'compile'
        rows, unused = compiler.compare(source, 'main', 2, 'off', True)
        assert len(rows) == 1 and rows[0]['compiledBytes'] == size
        row = rows[0]
        directory = WORK / kind / 'link'
        proof = validate(row, qualified_bindings(row), directory)
        save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
        row.update(save_link_snapshots.freeze_link(proof))
        row.update(exactAfterRealMwLink=True, exactAfterGenuineLink=True, linkedMatchingBytes=size)
        native = original[entry - 0x02000000:entry - 0x02000000 + size]
        code = (directory / 'caller.bin').read_bytes()
        assert code == native
        results = []
        for item in recipes(kind):
            first, second = execute(original, native, kind, item), execute(original, code, kind, item)
            assert first == second and first['modelPassed'], (kind, item, first)
            results.append(dict(recipe=item, result=first, actualReturns=2))
        text = source.read_text(encoding='utf-8')
        old, new = {'remove': ('var_r3 == arg1', 'var_r3 != arg1'),
                    'search': ('var_r0 == 0', 'var_r0 != 0'),
                    'insert': (' > (u32) M2C_FIELD(arg1', ' >= (u32) M2C_FIELD(arg1')}[kind]
        wrong = text.replace(old, new)
        assert wrong != text
        negative = ROOT / f'nonmatching/main-runtime/20261031-list-operations-negative/{kind}/source.c'
        negative.parent.mkdir(parents=True, exist_ok=True)
        if negative.exists() and negative.read_bytes() != wrong.encode():
            raise ValueError('Frozen wrong-C control differs')
        negative.write_bytes(wrong.encode())
        compiler.WORK = WORK / kind / 'negative-compile'
        bad_rows, unused = compiler.compare(negative, 'main', 2, 'off', True)
        assert len(bad_rows) == 1 and bad_rows[0]['compiledBytes'] == size
        bad_directory = WORK / kind / 'negative-link'
        try:
            validate(bad_rows[0], qualified_bindings(bad_rows[0]), bad_directory)
        except ValueError as error:
            mismatch = ast.literal_eval(str(error))
            assert mismatch['linkedBytes'] == size and mismatch['matchingBytes'] == size - 1
        else:
            raise ValueError('Wrong-C source unexpectedly matched')
        bad = (bad_directory / 'caller.bin').read_bytes()
        if kind == 'remove':
            controls = [dict(index=9000, count=1, target=0), dict(index=9001, count=0, target=-1)]
            for candidate in range(8):
                controls[0]['target'] = candidate
                if initial(kind, controls[0])['result']:
                    break
            assert initial(kind, controls[0])['result']
        elif kind == 'search':
            controls = [dict(index=9000, base=0, target=305, empty=False), dict(index=9001, base=0, target=305, empty=True)]
        else:
            controls = [dict(index=9000, count=1, parts=1, priority=128, equal=True),
                        dict(index=9001, count=0, parts=1, priority=128, equal=True)]
        negative_results = []
        for index, item in enumerate(controls):
            first, second = execute(original, native, kind, item), execute(original, bad, kind, item)
            assert first['modelPassed'] and second['modelPassed'] == bool(index)
            negative_results.append(dict(recipe=item, original=first, wrong=second, actualReturns=2))
        observed = {pc for item in results for pc in item['result']['pcs'] if entry <= pc < entry + size}
        assert len(observed) * 4 == size
        row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=2 * len(results),
            actualNativeHelperReturns=2 * sum(item['result']['counters']['actualHelperReturns'] for item in results),
            actualRecursiveCallerReturns=2 * sum(item['result']['counters']['actualRecursiveCallerReturns'] for item in results),
            suppliedCalls=0, observedCodeBytes=size, literalPoolBytes=0)
        matches.append(row)
        evidence.append(dict(kind=kind, results=results, negativeControls=negative_results,
                             wrongC=bad_rows[0], wrongLinkMismatch=mismatch))
    write_json(REPORT, dict(romSha256=config['romSha256'], matches=matches, evidence=evidence,
        generator='match_main_list_operations_20261031.py', generatorSha256=sha256(__file__),
        fixture=dict(path='main_list_operations_fixture_20261031.py', sha256=sha256(ROOT/'main_list_operations_fixture_20261031.py')),
        limitations=['Synthetic acyclic backed lists only; no null list-view or cyclic/malformed-chain behavior claimed',
                     'Search uses three nested levels and synthetic numeric intervals; no gameplay labels inferred',
                     'Insert uses a void C source view; incidental native R0 is compared to compiled execution without asserting an independent return-value meaning',
                     'Existing original next-node helper gets no new source credit; no providers used']))
    print(dict(functions=3, bytes=404, actualReturns=sum(r['nativeOracle']['actualReturns'] for r in matches),
               actualHelperReturns=sum(r['nativeOracle']['actualNativeHelperReturns'] for r in matches),
               recursiveReturns=sum(r['nativeOracle']['actualRecursiveCallerReturns'] for r in matches), negativeActualReturns=12))


if __name__ == '__main__':
    main()
