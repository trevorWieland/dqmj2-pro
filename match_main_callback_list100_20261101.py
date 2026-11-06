import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as compiler
from main_callback_list_fixture_20261101 import ENTRY, SIZE, CALLBACKS, execute
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/callback-list100-20261101'


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
        assert not exact and isinstance(error.args[0], dict)
        proof = error.args[0]
    return row, proof, (WORK / label / 'link/caller.bin').read_bytes()


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    metadata, image, unused = measured_module('main')
    source = ROOT / 'src/runtime/20261101_callback_list/native_main_0202dda0.c'
    row, proof, body = build(source, 'positive', True)
    native = image[ENTRY - 0x02000000:ENTRY - 0x02000000 + SIZE]
    assert body == native
    cases, observed, helper_observed = [], set(), set()
    for index in range(1750):
        original, candidate = execute(image, native, index), execute(image, body, index)
        assert original == candidate
        observed.update(original['observed'])
        helper_observed.update(original['helperObserved'])
        cases.append(dict(index=index, original=original, candidate=candidate))
    assert len(observed) == 100 and len(helper_observed) == 64
    row.update(genuineLinkComparison=freeze_link(proof), exactBytes=SIZE)
    controls = []
    for index, (before, after) in enumerate([
        ('temp_r2 & 0x100', 'temp_r2 & 0x200'),
        ('(u8) temp_r2)', '(u8) (temp_r2 >> 8))'),
        ('var_r0 = 1;', 'var_r0 = 0;'),
        ('arg2 < (u32)', 'arg2 <= (u32)')]):
        text = source.read_text()
        assert text.count(before) == 1
        changed = text.replace(before, after)
        path = ROOT / f'nonmatching/integration/20261101-callback-list-controls/{index}/source.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            assert path.read_text() == changed
        path.write_text(changed)
        bad, badproof, badbody = build(path, f'negative-{index}', False)
        results = [execute(image, badbody, sample, require_model=False) for sample in range(0, 1750, 7)]
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
    trace = ROOT / 'evidence/traces/main-callback-list100-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(raw, mtime=0))
    dependencies = [dict(processor='arm9', program='', module='main', mode='arm', address=hex(entry), bytes=size,
                         targetSha256=hashlib.sha256(image[entry - 0x02000000:entry - 0x02000000 + size]).hexdigest())
                    for entry, size in {callback: 40 for callback in CALLBACKS}.items()]
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        fixture='main_callback_list_fixture_20261101.py', fixtureSha256=sha256(ROOT / 'main_callback_list_fixture_20261101.py'),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=[row], matchedFunctions=1, matchedBytes=SIZE, genuineLinkedByteComparisons=[freeze_link(proof)],
        nativeDependencies=dependencies,
        oracle=dict(pairs=len(cases), actualTopReturns=2 * len(cases),
            actualNativeDependencyReturns=sum(case[side]['actualNativeDependencyReturns'] for case in cases for side in ['original', 'candidate']),
            suppliedCalls=0, initializedBytes=SIZE, ownInstructionBytesObserved=len(observed), literalBytes=SIZE - len(observed),
            helperInstructionBytesObserved=len(helper_observed), freshMachinePerExecution=True, instructionBound=512,
            actualReturnFrameAndControlStateRequired=True, allMappedWritesProtected=True,
            models=['Independent acyclic callback-list traversal and unsigned selector/count gate',
                    'Full measured three-word callback input and low-byte flag payload',
                    'Original native shadow callbacks, full RAM/MMIO effects and ordered writes'],
            traceArchive=dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace), decodedSha256=hashlib.sha256(raw).hexdigest())),
        negativeEvidence=dict(compiledReturningControls=controls, exhaustedPrefixReturnCredit=0),
        replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace))],
        reproductionCommand='python match_main_callback_list100_20261101.py',
        limitations=['Zero to four aligned acyclic mapped nodes; callback mutation of list nodes, cyclic/malformed lists and concurrency remain unsupported',
            'Native test callbacks preserve list links and ignore the second/third input words; those caller words are independently checked at entry',
            'Callback function formal types and scene availability are not inferred from this bounded fixture',
            'MMIO is a RAM-backed bus-payload model; helper source credit is zero',
            'No whole-module, source-only ROM or full Windows-game claim'])
    write_json(ROOT / 'evidence/matches/main-callback-list100-20261101.json', report)
    print(dict(newFunctions=1, newBytes=SIZE, actualTopReturns=2 * len(cases),
        actualNativeDependencyReturns=report['oracle']['actualNativeDependencyReturns'], suppliedCalls=0,
        negativeReturns=sum(control['actualReturns'] for control in controls),
        independentRejections=sum(control['independentRejections'] for control in controls)))


if __name__ == '__main__':
    main()
