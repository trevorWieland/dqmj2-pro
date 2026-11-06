import gzip
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as compiler
from main_handle_refresh_fixture_20261101 import ENTRY, SIZE, execute
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

SOURCE = ROOT / 'src/runtime/20261101_handle_refresh/native_main_020296b0.c'
WORK = ROOT / 'work/handle-refresh96-20261101'


def build(source, label, exact):
    compiler.WORK = WORK / label / 'compile'
    rows, unused = compiler.compare(source, 'main', 2, 'off')
    assert len(rows) == 1 and not rows[0].get('compileFailed')
    row = rows[0]
    try:
        proof = validate(row, qualified_bindings(row), WORK / label / 'link')
    except ValueError as error:
        assert not exact and isinstance(error.args[0], dict)
        proof = error.args[0]
    return row, proof, (WORK / label / 'link/caller.bin').read_bytes()


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    metadata, image, unused = measured_module('main')
    row, proof, body = build(SOURCE, 'positive', True)
    native = image[ENTRY - 0x02000000:ENTRY - 0x02000000 + SIZE]
    assert native == body and len(body) == SIZE
    cases, observed = [], set()
    for index in range(0, 8192, 3):
        original, candidate = execute(image, native, index), execute(image, body, index)
        assert original == candidate
        observed.update(original['observed'])
        cases.append(dict(index=index, original=original, candidate=candidate))
    assert len(observed) == SIZE
    controls = []
    for label, before, after in [('word-value', 'M2C_FIELD(arg0, s32 *, 0xF8) = 0x1000;', 'M2C_FIELD(arg0, s32 *, 0xF8) = 0x1001;'), ('flag-bit', 'M2C_FIELD(arg0, u8 *, 0xA) & 1', 'M2C_FIELD(arg0, u8 *, 0xA) & 2')]:
        text = SOURCE.read_text()
        assert text.count(before) == 1
        path = ROOT / f'nonmatching/integration/20261101-callback-stream-controls/{label}/source.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        changed = text.replace(before, after)
        if path.exists():
            assert path.read_text() == changed
        path.write_text(changed)
        bad, badproof, badbody = build(path, 'negative-' + label, False)
        records = [execute(image, badbody, index, require_model=False) for index in range(0, 8192, 73)]
        rejected = sum(not record['modelPassed'] for record in records)
        assert rejected > 0
        controls.append(dict(label=label, compilation=bad, genuineLinkComparison=badproof,
            actualReturns=len(records), rawModelRejections=rejected, records=records))
    try:
        execute(image, native, 24, bound=1)
    except AssertionError:
        bounded_return_rejected = True
    else:
        raise AssertionError('Exhausted stream execution received a return')
    raw = json.dumps(cases, sort_keys=True, separators=(',', ':')).encode()
    trace = ROOT / 'evidence/traces/main-handle-refresh96-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(raw, mtime=0))
    row['genuineLinkComparison'] = freeze_link(proof)
    row['exactBytes'] = SIZE
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        fixture='main_handle_refresh_fixture_20261101.py', fixtureSha256=sha256(ROOT / 'main_handle_refresh_fixture_20261101.py'),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        source=SOURCE.relative_to(ROOT).as_posix(), sourceSha256=sha256(SOURCE), matches=[row],
        matchedFunctions=1, matchedBytes=SIZE, genuineLinkedByteComparisons=[freeze_link(proof)],
        oracle=dict(pairs=len(cases), actualTopReturns=2 * len(cases), actualNativeDependencyReturns=sum(c[k]['actualNativeDependencyReturns'] for c in cases for k in ['original', 'candidate']),
            suppliedCalls=sum(c[k]['suppliedCalls'] for c in cases for k in ['original', 'candidate']),
            ownInstructionBytesObserved=len(observed), freshMachinePerExecution=True, actualReturnAndFrameRequired=True,
            boundedExhaustionRejected=bounded_return_rejected, instructionBound=512,
            model='Independent bounded list-removal, word-transfer and byte-flag contract',
            traceArchive=dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace), decodedSha256=__import__('hashlib').sha256(raw).hexdigest())),
        negativeEvidence=dict(compiledReturningControls=controls),
        replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace))],
        reproductionCommand='python match_main_handle_refresh96_20261101.py',
        limitations=['Original 29688/29618/2EBC0/2EB4C helpers execute; zero providers', 'Bounded acyclic three-list contexts and incoming byte bit0x4 clear; owning/free callback path unsupported', 'Raw word, byte and list effects do not establish original object types, total extents, resource meanings or scene reachability', 'All own code, complete seeded page, outside-write guards, frame and raw registers checked', 'Module integration and source acceptance remain separate'])
    write_json(ROOT / 'evidence/matches/main-handle-refresh96-20261101.json', report)
    print(dict(matchedBytes=SIZE, pairs=len(cases), actualTopReturns=2 * len(cases), suppliedCalls=report['oracle']['suppliedCalls'],
        negativeActualReturns=sum(c['actualReturns'] for c in controls), negativeRejections=sum(c['rawModelRejections'] for c in controls)))


if __name__ == '__main__':
    main()
