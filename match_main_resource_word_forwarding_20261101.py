import ast
import sys
import match_runtime as compiler
import save_link_snapshots
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from main_resource_forwarding_fixture_20261101 import execute, ENTRY
from unicorn import __version__


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    native = original[ENTRY - 0x02000000:ENTRY - 0x02000000 + 16]
    source = ROOT / 'src/runtime/20261101_resource_word_forwarding/native_main_020380e4.c'
    work = ROOT / 'work/main-resource-word-forwarding-20261101'
    compiler.WORK = work / 'compile'
    rows, unused = compiler.compare(source, 'main', 2, 'off')
    assert len(rows) == 1
    row = rows[0]
    bindings = qualified_bindings(row)
    proof = validate(row, bindings, work / 'link')
    save_link_snapshots.DIRECTORY = work / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    row.update(exactAfterRealMwLink=True, exactAfterGenuineLink=True, linkedMatchingBytes=16)
    candidate = (work / 'link/caller.bin').read_bytes()
    assert candidate == native
    cases = []
    for index in range(2048):
        first, second = execute(original, native, index), execute(original, candidate, index)
        assert first == second and first['modelPassed'], (index, first, second)
        cases.append(dict(index=index, result=first, actualReturns=2))
    negatives = []
    for label, replacement in [('zero-word', '0'), ('truncated-word', 'value & 255')]:
        text = source.read_text()
        assert text.count('(*handle, value);') == 1
        path = ROOT / f'nonmatching/main-runtime/20261101-resource-word-controls/{label}/source.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.replace('(*handle, value);', f'(*handle, {replacement});'), encoding='utf-8')
        compiler.WORK = work / label / 'compile'
        bad_rows, unused = compiler.compare(path, 'main', 2, 'off')
        bad_row = bad_rows[0]
        try:
            validate(bad_row, qualified_bindings(bad_row), work / label / 'link')
        except ValueError as error:
            mismatch = ast.literal_eval(str(error))
        else:
            raise AssertionError('Wrong forwarding C unexpectedly matches original bytes')
        bad = (work / label / 'link/caller.bin').read_bytes()
        failed, positive = [], 0
        for index in range(2048):
            result = execute(original, bad, index)
            if result['modelPassed']:
                positive += 1
            else:
                failed.append(dict(index=index, result=result))
        assert failed and positive
        negatives.append(dict(label=label, compilerResult=bad_row, linkMismatch=mismatch,
            actualReturns=2048, independentRejections=len(failed), positiveCases=positive, failures=failed))
    row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=4096,
        actualOriginalTargetReturns=4096, suppliedServiceCalls=sum(len(c['result']['calls']) * 2 for c in cases),
        definedCReturnValueClaim=False)
    write_json(ROOT / 'evidence/matches/main-resource-word-forwarding-20261101.json', dict(
        romSha256=config['romSha256'], matches=[row], nativeSymbols={name: value['address'] for name, value in bindings.items()},
        nativeSymbolEntries=bindings, qualifications=cases, negativeControls=negatives,
        newFunctions=0, newSourceBytes=0, duplicateMigrationFunctions=1, duplicateMigrationBytes=16,
        limitations=['Explicitly forwards the complete second input word through the original 40-byte native target',
            'Native target compares all bits before storing the low byte; zero and byte-truncation controls are rejected',
            'The lower 02009128 service result is supplied explicitly; its body and real resource effects receive no credit',
            'Raw R0, registers, memory, termination and mode are measured; the void C wrapper declares no return-value meaning',
            'Prior source and original executable bytes remain unchanged; source preference requires separate integration approval and validation',
            'No original type names, resource semantics, game-scene feasibility, Android execution or source-only game claim']))
    print(dict(functions=1, duplicateBytes=16, newByteCredit=0, actualReturns=4096, wrongBodyReturns=4096,
               independentRejections=sum(r['independentRejections'] for r in negatives)))


if __name__ == '__main__':
    main()
