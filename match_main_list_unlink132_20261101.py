import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as compiler
from main_list_unlink_fixture_20261101 import ENTRY, SIZE, IRQ, execute
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/list-unlink132-20261101'


def build(source, label, exact):
    compiler.WORK = WORK / label / 'compile'
    rows, unused = compiler.compare(source, 'main', 2, 'off', speed=True)
    assert len(rows) == 1 and not rows[0].get('compileFailed')
    row = rows[0]
    try:
        proof = validate(row, qualified_bindings(row), WORK / label / 'link')
    except ValueError as error:
        if exact:
            raise
        assert not exact and isinstance(error.args[0], dict)
        proof = error.args[0]
    return row, proof, (WORK / label / 'link/caller.bin').read_bytes()


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    metadata, image, unused = measured_module('main')
    source = ROOT / 'src/runtime/20261101_list_unlink/native_main_0200b7c8.c'
    row, proof, body = build(source, 'positive', True)
    native = image[ENTRY - 0x02000000:ENTRY - 0x02000000 + SIZE]
    assert body == native
    cases, observed, helper_observed = [], set(), set()
    for index in range(1200):
        original, candidate = execute(image, native, index), execute(image, body, index)
        assert original == candidate
        observed.update(original['observed'])
        helper_observed.update(original['helperObserved'])
        cases.append(dict(index=index, original=original, candidate=candidate))
    assert len(observed) == 128 and len(helper_observed) == 44
    row.update(genuineLinkComparison=freeze_link(proof), exactBytes=SIZE)
    controls = []
    for index, (before, after) in enumerate([
        ('& ~1', '& ~2'),
        ('M2C_FIELD(temp_r2, void **, 8)', 'M2C_FIELD(temp_r2, void **, 4)'),
        ('native_data_020e5348.field_c = 0;', 'native_data_020e5348.field_c = 1;')]):
        text = source.read_text()
        assert text.count(before) == 1
        changed = text.replace(before, after)
        path = ROOT / f'nonmatching/integration/20261101-list-unlink-controls/{index}/source.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            assert path.read_text() == changed
        path.write_text(changed)
        bad, badproof, badbody = build(path, f'negative-{index}', False)
        results = [execute(image, badbody, sample, require_model=False) for sample in range(0, 1200, 7)]
        rejected = sum(not result['modelPassed'] for result in results)
        assert rejected > 0
        controls.append(dict(compilation=bad, genuineLinkComparison=badproof,
            actualReturns=len(results), independentRejections=rejected,
            unchangedPositiveCases=len(results) - rejected, cases=results))
    try:
        execute(image, native, 0, bound=1)
    except AssertionError:
        pass
    else:
        raise AssertionError('Instruction exhaustion is not a return')
    raw = json.dumps(cases, sort_keys=True, separators=(',', ':')).encode()
    trace = ROOT / 'evidence/traces/main-list-unlink132-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(raw, mtime=0))
    dependencies = [dict(processor='arm9', program='', module='main', mode='arm', address=hex(entry), bytes=size,
                         targetSha256=hashlib.sha256(image[entry - 0x02000000:entry - 0x02000000 + size]).hexdigest())
                    for entry, size in IRQ.items()]
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        fixture='main_list_unlink_fixture_20261101.py', fixtureSha256=sha256(ROOT / 'main_list_unlink_fixture_20261101.py'),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=[row], matchedFunctions=1, matchedBytes=SIZE, genuineLinkedByteComparisons=[freeze_link(proof)],
        nativeDependencies=dependencies,
        oracle=dict(pairs=len(cases), actualTopReturns=2 * len(cases),
            actualNativeDependencyReturns=sum(case[side]['actualNativeDependencyReturns'] for case in cases for side in ['original', 'candidate']),
            suppliedCalls=0, initializedBytes=SIZE, ownInstructionBytesObserved=len(observed), literalBytes=SIZE - len(observed),
            helperInstructionBytesObserved=len(helper_observed), freshMachinePerExecution=True, instructionBound=256,
            actualReturnFrameAndControlStateRequired=True, allMappedWritesProtected=True,
            models=['Independent inactive/active list unlink and optional-neighbor rewrites',
                    'Full flags preservation except bit0 and conditional global-root reset',
                    'Original native IRQ disable/restore with both IRQ/FIQ mask initial states'],
            traceArchive=dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace), decodedSha256=hashlib.sha256(raw).hexdigest())),
        negativeEvidence=dict(compiledReturningControls=controls, exhaustedPrefixReturnCredit=0),
        replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace))],
        reproductionCommand='python match_main_list_unlink132_20261101.py',
        limitations=['Aligned mapped objects and fixed valid optional-neighbor shapes; malformed or concurrent lists are not proved',
            'Global fallback values are measured raw words, with no gameplay or original formal-type meaning inferred',
            'Native helpers execute in ARM946 system mode; physical interrupt delivery and scheduling are not simulated',
            'Helper source credit is zero; no whole-module, source-only ROM or full Windows-game claim'])
    write_json(ROOT / 'evidence/matches/main-list-unlink132-20261101.json', report)
    print(dict(newFunctions=1, newBytes=SIZE, actualTopReturns=2 * len(cases),
        actualNativeDependencyReturns=report['oracle']['actualNativeDependencyReturns'], suppliedCalls=0,
        negativeReturns=sum(control['actualReturns'] for control in controls),
        independentRejections=sum(control['independentRejections'] for control in controls)))


if __name__ == '__main__':
    main()
