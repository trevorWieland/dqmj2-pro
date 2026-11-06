import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as compiler
from main_heap_support_fixture_20261101 import ENTRIES, execute
import main_heap_initializers_fixture_20261101 as parents
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/heap-support172-20261101'


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
    return row, proof, (WORK / label / 'link/caller.bin').read_bytes()


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    metadata, image, unused = measured_module('main')
    matches, bodies, sources, proofs, dependencies = [], {}, {}, [], []
    for entry, size in {**ENTRIES, **parents.ENTRIES}.items():
        folder = '20261101_heap_support' if entry in ENTRIES else '20261101_heap_initializers'
        source = ROOT / f'src/runtime/{folder}/native_main_{entry:08x}.c'
        row, proof, body = build(source, f'{entry:x}-positive', True)
        assert body == image[entry - 0x02000000:entry - 0x02000000 + size]
        bodies[entry], sources[entry] = body, source
        if entry in ENTRIES:
            row.update(genuineLinkComparison=freeze_link(proof), exactBytes=size)
            matches.append(row)
            proofs.append(freeze_link(proof))
        else:
            dependencies.append(dict(path=source.relative_to(ROOT).as_posix(), sha256=sha256(source)))
    cases, coverage, controls = [], {}, []
    for entry, size in ENTRIES.items():
        observed = set()
        for index in range(640):
            original = execute(image, entry, {}, index)
            candidate = execute(image, entry, {entry: bodies[entry]}, index)
            assert original == candidate
            record = dict(entry=hex(entry), index=index, original=original, candidate=candidate)
            if entry == 0x0202BA20:
                record['sourceComposed'] = execute(image, entry, bodies, index)
                assert record['sourceComposed'] == original
            cases.append(record)
            observed.update(original['observed'])
        assert len(observed) == size
        coverage[hex(entry)] = dict(ownInstructionBytesObserved=len(observed), initializedBytes=size, literalBytes=0)
    for entry in parents.ENTRIES:
        for index in range(0, 1200, 7):
            original = parents.execute(image, entry, {}, index)
            composed = parents.execute(image, entry, bodies, index)
            assert original == composed
            cases.append(dict(entry=hex(entry), index=index, parentContextOnly=True,
                              original=original, sourceComposed=composed))
    changes = [(0x0202ADFC, '+ sizeof(Block)', '+ 8'),
               (0x0202B9F4, 'link->previous = 0;', 'link->previous = object;'),
               (0x0202BA20, 'list->tail = object;', 'list->tail = list->head;')]
    for number, (entry, before, after) in enumerate(changes):
        text = sources[entry].read_text()
        assert text.count(before) == 1
        changed = text.replace(before, after)
        path = ROOT / f'nonmatching/integration/20261101-heap-support-controls/{number}/source.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            assert path.read_text() == changed
        path.write_text(changed)
        bad, badproof, badbody = build(path, f'negative-{number}', False)
        results = [execute(image, entry, {entry: badbody}, index, require_model=False) for index in range(0, 640, 7)]
        rejected = sum(not result['modelPassed'] for result in results)
        assert rejected > 0
        controls.append(dict(entry=hex(entry), compilation=bad, genuineLinkComparison=badproof,
            actualReturns=len(results), independentRejections=rejected, unchangedPositiveCases=len(results) - rejected, cases=results))
        try:
            execute(image, entry, {}, 0, bound=1)
        except AssertionError:
            pass
        else:
            raise AssertionError('Instruction exhaustion received false return credit')
    raw = json.dumps(cases, sort_keys=True, separators=(',', ':')).encode()
    trace = ROOT / 'evidence/traces/main-heap-support172-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(raw, mtime=0))
    executions = [case[role] for case in cases for role in ['original', 'candidate', 'sourceComposed'] if role in case]
    source_returns = sum(sum(address in bodies for address in case['sourceComposed']['returnedHelpers'])
                         for case in cases if 'sourceComposed' in case)
    all_returns = sum(record['actualNativeDependencyReturns'] for record in executions)
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        fixture='main_heap_support_fixture_20261101.py', fixtureSha256=sha256(ROOT / 'main_heap_support_fixture_20261101.py'),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=matches, matchedFunctions=3, matchedBytes=172, genuineLinkedByteComparisons=proofs,
        sourceDependencies=dependencies,
        oracle=dict(actualTopReturns=len(executions), actualNativeDependencyReturns=all_returns,
            actualOriginalHelperReturns=all_returns - source_returns, actualSourceLinkedHelperReturns=source_returns,
            sourceLinkedReturnsIncludedInNativeDependencyTotal=True, suppliedCalls=0, coverage=coverage,
            standaloneOriginalCandidatePairs=1920, parentContextPairs=344, standaloneSourceCompositionExecutions=640,
            actualReturnFrameControlStateAndGuardsRequired=True, freshMachinePerExecution=True,
            models=['Independent block signature/size wrapping and prev/next initialization',
                    'List offsets, empty/nonempty append, full-word pointer effects and low16 counter wrap',
                    'Full five-source initialization composition under independent nested heap models'],
            traceArchive=dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace), decodedSha256=hashlib.sha256(raw).hexdigest())),
        negativeEvidence=dict(compiledReturningControls=controls, boundedPrefixReturnCredit=0),
        replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace))],
        reproductionCommand='python match_main_heap_support172_20261101.py',
        limitations=['Aligned disjoint region/list/node storage; arbitrary object aliasing and concurrency remain unproved',
            'Inconsistent initial counts are bounded raw-word wrap probes, not valid-list invariant claims',
            'Two list functions are declared void; raw R0 is compared without an API return-value claim',
            'Parent/source-linked lower routines receive no duplicate source credit',
            'No source-only ROM or full Windows-game claim'])
    write_json(ROOT / 'evidence/matches/main-heap-support172-20261101.json', report)
    print(dict(newFunctions=3, newBytes=172, actualTopReturns=len(executions),
        actualOriginalHelperReturns=all_returns - source_returns, actualSourceLinkedHelperReturns=source_returns,
        suppliedCalls=0, negativeReturns=sum(c['actualReturns'] for c in controls),
        independentRejections=sum(c['independentRejections'] for c in controls)))


if __name__ == '__main__':
    main()
