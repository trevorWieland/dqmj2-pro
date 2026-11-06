import ast
import sys
import struct
from project import ROOT, configuration, write_json, sha256
import match_runtime as compiler
from unicorn import __version__
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_mask_predicate_fixture_20261031 import ENTRY, SIZE, HELPER, recipe, execute

SOURCE = ROOT / 'src/runtime/20261031_mask_predicate/native_main_020d3f4c.c'
WORK = ROOT / 'work/main-mask-predicate-20261031'
REPORT = ROOT / 'evidence/matches/main-mask-predicate-20261031.json'


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == "2.1.4"
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    compiler.WORK = WORK / 'compile'
    rows, unused = compiler.compare(SOURCE, 'main', 2, 'off', True)
    assert len(rows) == 1 and rows[0]['compiledBytes'] == SIZE
    row = rows[0]
    proof = validate(row, qualified_bindings(row), WORK / 'link')
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    row.update(exactAfterRealMwLink=True, exactAfterGenuineLink=True, linkedMatchingBytes=SIZE)
    unused, original, unused = measured_module('main')
    native = original[ENTRY - 0x02000000:ENTRY - 0x02000000 + SIZE]
    code = (WORK / 'link/caller.bin').read_bytes()
    assert code == native
    results = []
    for index in range(512):
        item = recipe(index)
        first, second = execute(original, native, item), execute(original, code, item)
        assert first == second and first['modelPassed']
        results.append(dict(recipe=item, result=first, actualReturns=2))
    negative = ROOT / 'nonmatching/main-runtime/20261031-mask-predicate-negative/source.c'
    text = SOURCE.read_text(encoding='utf-8')
    wrong = text.replace('var_r4 |= 4;', 'var_r4 |= 8;')
    assert wrong != text
    negative.parent.mkdir(parents=True, exist_ok=True)
    if negative.exists() and negative.read_bytes() != wrong.encode():
        raise ValueError('Earlier whole-C negative differs')
    negative.write_bytes(wrong.encode())
    compiler.WORK = WORK / 'negative-compile'
    bad_rows, unused = compiler.compare(negative, 'main', 2, 'off', True)
    assert len(bad_rows) == 1 and bad_rows[0]['compiledBytes'] == SIZE
    try:
        validate(bad_rows[0], qualified_bindings(bad_rows[0]), WORK / 'negative-link')
    except ValueError as error:
        mismatch = ast.literal_eval(str(error))
        assert mismatch['linkedBytes'] == SIZE and mismatch['matchingBytes'] == SIZE - 1
    else:
        raise ValueError('Wrong return-bit source unexpectedly matched')
    bad = (WORK / 'negative-link/caller.bin').read_bytes()
    controls = []
    for index, fields in enumerate([[0xFFFF, 0, 0], [0, 0xFFFF, 0]]):
        item = recipe(9001 + index)
        item.update(null=False, indices=[0, 1], fields=fields)
        table = bytearray.fromhex(item['table'])
        struct.pack_into('<H', table, 10, 1)
        struct.pack_into('<H', table, 14, 2)
        item['table'] = table.hex()
        first, second = execute(original, native, item), execute(original, bad, item)
        assert first['modelPassed'] and second['modelPassed'] == bool(index)
        controls.append(dict(recipe=item, original=first, wrong=second, actualReturns=2))
    own = {pc for item in results for pc in item['result']['pcs'] if ENTRY <= pc < ENTRY + SIZE}
    helper = {pc for item in results for pc in item['result']['pcs'] if HELPER <= pc < HELPER + 36}
    assert len(own) * 4 == SIZE - 4 and len(helper) * 4 == 32
    row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=1024,
        actualNativeHelperReturns=2048, suppliedHelpers=0, observedCodeBytes=len(own) * 4, literalPoolBytes=4)
    write_json(REPORT, dict(romSha256=config['romSha256'], matches=rows, results=results,
        negativeControls=controls, negativeCompiled=bad_rows[0], negativeLinkMismatch=mismatch,
        helper=dict(address=hex(HELPER), originalBytes=36, originalSha256=compiler.sha(original[HELPER-0x02000000:HELPER-0x02000000+36]), selectedSource='src/runtime/main-scalars01/native_main_020d3540_22d4ffd0e8a9.c', selectedSourceSha256=sha256(ROOT / 'src/runtime/main-scalars01/native_main_020d3540_22d4ffd0e8a9.c')),
        generator='match_main_mask_predicate_20261031.py', generatorSha256=sha256(__file__),
        fixture=dict(path='main_mask_predicate_fixture_20261031.py',sha256=sha256(ROOT/'main_mask_predicate_fixture_20261031.py')),
        limitations=['Indices 0..31 and null/supplied aligned table only; no original table extent or semantic label',
            'Original helper body executes; accepted signed-index helper source is unchanged and no high-word signed-overflow domain is added',
            'No hardware synchronization, whole-ROM source, Windows-game or Android device completion claim']))
    print(dict(bytes=SIZE, actualReturns=1024, actualHelperReturns=2048, negativeActualReturns=4))


if __name__ == '__main__':
    main()
