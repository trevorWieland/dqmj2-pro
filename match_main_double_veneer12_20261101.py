import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as compiler
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
from probe_main_float_word_contracts_20261101 import execute

ENTRY, SIZE = 0x0202298C, 12
WORK = ROOT / 'work/double-veneer12-20261101'


def build(source, label, exact):
    compiler.WORK = WORK / label / 'compile'
    rows, unused = compiler.compare(source, 'main', 2, 'off')
    assert len(rows) == 1 and not rows[0].get('compileFailed')
    row = rows[0]
    try:
        proof = validate(row, qualified_bindings(row), WORK / label / 'link')
    except ValueError as error:
        if exact:
            raise
        assert isinstance(error.args[0], dict)
        proof = error.args[0]
    body = (WORK / label / 'link/caller.bin').read_bytes()
    assert len(body) == SIZE
    return row, proof, body


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    metadata, image, unused = measured_module('main')
    source = ROOT / 'src/runtime/20261101_double_veneer12/native_main_0202298c.c'
    row, proof, body = build(source, 'positive', True)
    offset = ENTRY - 0x02000000
    assert body == image[offset:offset + SIZE]
    candidate = image[:offset] + body + image[offset + SIZE:]
    oracle_path = ROOT / 'evidence/abi/main-float-word-contracts-20261101.json'
    oracle = read_json(oracle_path)
    assert oracle['passed'] and oracle['sourceCredit'] == 0 and oracle['actualNativeReturns'] == 301
    selected = [case for case in oracle['cases'] if case['entry'] == hex(ENTRY)]
    assert len(selected) == 35
    cases = []
    for case in selected:
        original = execute(image, ENTRY, case['arguments'], case['index'])
        recovered = execute(candidate, ENTRY, case['arguments'], case['index'])
        assert original == recovered
        assert recovered['resultWords'] == case['expectedWords']
        assert recovered['nativeTargetWords'] == [case['arguments']]
        cases.append(dict(index=case['index'], original=original, candidate=recovered))
    path = ROOT / 'nonmatching/integration/20261101-double-veneer-controls/zero.c'
    path.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding='utf-8')
    before = 'return native_fn_020212f8(base, exponent);'
    assert text.count(before) == 1
    text = text.replace(before, 'return 0.0;')
    if path.exists():
        assert path.read_text(encoding='utf-8') == text
    path.write_text(text, encoding='utf-8')
    bad_row, bad_proof, bad_body = build(path, 'negative-zero', False)
    bad_image = image[:offset] + bad_body + image[offset + SIZE:]
    bad_cases = [execute(bad_image, ENTRY, case['arguments'], case['index']) for case in selected]
    rejected = sum(result['resultWords'] != case['expectedWords'] for result, case in zip(bad_cases, selected))
    assert rejected == 35
    try:
        machine_case = selected[0]
        execute(image[:offset] + bytes.fromhex('feffffea') * 3 + image[offset + SIZE:], ENTRY,
            machine_case['arguments'], machine_case['index'])
    except AssertionError:
        pass
    else:
        raise AssertionError('Nonreturning code has no completed-return credit')
    row.update(genuineLinkComparison=freeze_link(proof), exactBytes=12, sourceOnlyCompilerInput=True,
        originalObjectScaffolding=False)
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        fixture='probe_main_float_word_contracts_20261101.py',
        fixtureSha256=sha256(ROOT / 'probe_main_float_word_contracts_20261101.py'),
        romSha256=config['romSha256'], module='main', processor='arm9', program='',
        moduleSha256=metadata['sha256'], matches=[row], matchedFunctions=1, matchedBytes=12,
        newSourceByteCredit=0, replacementClassification='Typed double-word ABI forwarding alternative',
        oracle=dict(pairs=35, actualTopReturns=70, suppliedCalls=0, actualReturnRequired=True,
            fourPhysicalArgumentWordsAndTwoResultWordsCompared=True, cases=cases,
            originalMathClosureReceivesNoSourceCredit=True),
        negativeEvidence=dict(compilation=bad_row, genuineLinkComparison=bad_proof, actualReturns=35,
            independentRejections=rejected, cases=bad_cases, nonreturningMutationCompletionCredit=0),
        replayDependencies=[dict(path=oracle_path.relative_to(ROOT).as_posix(), sha256=sha256(oracle_path))],
        reproductionCommand='python match_main_double_veneer12_20261101.py',
        limitations=['Measured finite dyadic and base10 powers; general power rounding, NaNs and overflow unproved',
            'Underlying original212F8 math code remains source-unmatched and is not replaced by a provider',
            'This repairs the selected forwarding contract; it does not recover the historical public API name',
            'Old primary is preserved; no duplicate function or byte credit, complete module or host-game claim'])
    output = ROOT / 'evidence/matches/main-double-veneer12-20261101.json'
    write_json(output, report)
    print(dict(typedVeneerBytes=12, newByteCredit=0, actualTopReturns=70, wrongReturns=35,
        independentRejections=rejected, suppliedCalls=0, reportSha256=sha256(output)))


if __name__ == '__main__':
    main()
