import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as compiler
from main_bounds_shadows_fixture_20261101 import ENTRIES, execute
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/bounds-shadows124-20261101'


def build(path, label, exact):
    compiler.WORK = WORK / label / 'compile'
    rows, unused = compiler.compare(path, 'main', 2, 'off')
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
    matches, proofs, cases, coverage, controls = [], [], [], {}, []
    for entry, size in ENTRIES.items():
        source = ROOT / f'src/runtime/20261101_bounds_and_shadows/native_main_{entry:08x}.c'
        row, proof, body = build(source, f'{entry:x}-positive', True)
        native = image[entry - 0x02000000:entry - 0x02000000 + size]
        assert body == native
        observed = set()
        for index in range(640):
            original = execute(image, entry, native, index)
            candidate = execute(image, entry, body, index)
            assert original == candidate
            observed.update(original['observed'])
            cases.append(dict(entry=hex(entry), index=index, original=original, candidate=candidate))
        coverage[hex(entry)] = dict(instructionBytesObserved=len(observed), initializedBytes=size,
            literalBytes=size - len(observed))
        assert len(observed) == (44 if entry == 0x0202AD78 else 32)
        row.update(genuineLinkComparison=freeze_link(proof), exactBytes=size)
        matches.append(row)
        proofs.append(freeze_link(proof))
        before, after = {
            0x0202AD78: ('& 0x7F', '& 0x3F'),
            0x02029D5C: ('*(u16 *)0x04000354', '*(u8 *)0x04000354'),
            0x02029E68: ('return (u32) temp_r0;', 'return arg0;')}[entry]
        text = source.read_text()
        assert text.count(before) == 1
        path = ROOT / f'nonmatching/integration/20261101-bounds-shadow-controls/{entry:x}/source.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        changed = text.replace(before, after)
        if path.exists():
            assert path.read_text() == changed
        path.write_text(changed)
        bad, badproof, badbody = build(path, f'{entry:x}-negative', False)
        records = [execute(image, entry, badbody, index, require_model=False) for index in range(0, 640, 11)]
        rejected = sum(not result['modelPassed'] for result in records)
        assert rejected > 0
        controls.append(dict(entry=hex(entry), compilation=bad, genuineLinkComparison=badproof,
            actualReturns=len(records), independentRejections=rejected, records=records))
        try:
            execute(image, entry, native, 0, bound=1)
        except AssertionError:
            pass
        else:
            raise AssertionError('Bounded prefix received false return credit')
    raw = json.dumps(cases, sort_keys=True, separators=(',', ':')).encode()
    trace = ROOT / 'evidence/traces/main-bounds-shadows124-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        fixture='main_bounds_shadows_fixture_20261101.py', fixtureSha256=sha256(ROOT / 'main_bounds_shadows_fixture_20261101.py'),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=matches, matchedFunctions=3, matchedBytes=124, genuineLinkedByteComparisons=proofs,
        oracle=dict(pairs=len(cases), actualTopReturns=2 * len(cases), actualNativeDependencyReturns=0,
            suppliedCalls=0, coverage=coverage, freshMachinePerExecution=True, instructionBound=128,
            actualReturnAndFrameRequired=True, allMappedWritesProtected=True,
            models=['Ordered overlapping output-bound reconstruction', 'Low16 shadow/global/MMIO payload and ordered stores'],
            traceArchive=dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace), decodedSha256=hashlib.sha256(raw).hexdigest())),
        negativeEvidence=dict(compiledReturningControls=controls),
        replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace))],
        reproductionCommand='python match_main_bounds_shadows124_20261101.py',
        limitations=['Bounded aligned mapped objects and five source/output alias arrangements',
            'Unsigned arithmetic wraps in the measured32-bit target; no total heap-object extent or scene claim',
            'MMIO is a RAM-backed bus-payload/store-order model, not physical graphics-device behavior',
            'Original global/qualifier/type provenance remains unproved; no whole-module or ROM source-only claim'])
    write_json(ROOT / 'evidence/matches/main-bounds-shadows124-20261101.json', report)
    print(dict(newFunctions=3, newBytes=124, actualTopReturns=2 * len(cases), suppliedCalls=0,
        negativeReturns=sum(control['actualReturns'] for control in controls),
        independentRejections=sum(control['independentRejections'] for control in controls)))


if __name__ == '__main__':
    main()
