import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as compiler
from main_heap_initializers_fixture_20261101 import HEADER, EXP, ENTRIES, HELPERS, execute
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/heap-initializers276-20261101'


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
    matches, proofs, bodies, sources = [], [], {}, {}
    for entry, size in ENTRIES.items():
        source = ROOT / f'src/runtime/20261101_heap_initializers/native_main_{entry:08x}.c'
        row, proof, body = build(source, f'{entry:x}-positive', True)
        assert body == image[entry - 0x02000000:entry - 0x02000000 + size]
        row.update(genuineLinkComparison=freeze_link(proof), exactBytes=size)
        matches.append(row)
        proofs.append(freeze_link(proof))
        bodies[entry], sources[entry] = body, source
    cases, coverage = [], {}
    for entry, size in ENTRIES.items():
        own, lower = set(), set()
        for index in range(1200):
            original = execute(image, entry, {}, index)
            candidate = execute(image, entry, {entry: bodies[entry]}, index)
            assert original == candidate
            record = dict(entry=hex(entry), index=index, original=original, candidate=candidate)
            if entry == EXP:
                composed = execute(image, entry, bodies, index)
                assert composed == original
                record['sourceComposed'] = composed
            cases.append(record)
            own.update(original['observed'])
            lower.update(original['helperObserved'])
        assert len(own) == size - 8
        coverage[hex(entry)] = dict(ownInstructionBytesObserved=len(own), initializedBytes=size,
            literalBytes=size - len(own), lowerInstructionBytesObserved=len(lower))
    controls = []
    changes = [(HEADER, 'extern u32 native_data_020edf74;', 'extern u8 native_data_020edf74;'),
        (HEADER, ' & 2)', ' & 1)'), (EXP, 'exp->group = 0;', 'exp->group = 1;'),
        (EXP, 'exp->freeTail = block;', 'exp->freeTail = 0;')]
    for number, (entry, before, after) in enumerate(changes):
        text = sources[entry].read_text()
        assert text.count(before) == 1
        changed = text.replace(before, after)
        path = ROOT / f'nonmatching/integration/20261101-heap-initializer-controls/{number}/source.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            assert path.read_text() == changed
        path.write_text(changed)
        bad, badproof, badbody = build(path, f'negative-{number}', False)
        results = [execute(image, entry, {entry: badbody}, index, require_model=False)
                   for index in range(0, 1200, 13)]
        rejected = sum(not result['modelPassed'] for result in results)
        assert rejected > 0
        controls.append(dict(entry=hex(entry), compilation=bad, genuineLinkComparison=badproof,
            actualReturns=len(results), independentRejections=rejected,
            unchangedPositiveCases=len(results) - rejected, cases=results))
    for entry in ENTRIES:
        try:
            execute(image, entry, {}, 0, bound=1)
        except AssertionError:
            pass
        else:
            raise AssertionError('Bounded prefix is not a completed return')
    raw = json.dumps(cases, sort_keys=True, separators=(',', ':')).encode()
    trace = ROOT / 'evidence/traces/main-heap-initializers276-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(raw, mtime=0))
    executions = [record[role] for record in cases for role in ['original', 'candidate', 'sourceComposed'] if role in record]
    source_linked_returns = sum(record['sourceComposed']['returnedHelpers'].count(HEADER)
                                for record in cases if 'sourceComposed' in record)
    native_returns = sum(record['actualNativeDependencyReturns'] for record in executions)
    dependencies = [dict(processor='arm9', program='', module='main', mode='arm', address=hex(entry), bytes=size,
        targetSha256=hashlib.sha256(image[entry - 0x02000000:entry - 0x02000000 + size]).hexdigest())
        for entry, size in HELPERS.items()]
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        fixture='main_heap_initializers_fixture_20261101.py', fixtureSha256=sha256(ROOT / 'main_heap_initializers_fixture_20261101.py'),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=matches, matchedFunctions=2, matchedBytes=276, genuineLinkedByteComparisons=proofs,
        nativeDependencies=dependencies,
        oracle=dict(originalCandidatePairs=2400, sourceCompositionExecutions=1200, actualTopReturns=len(executions),
            actualNativeDependencyReturns=native_returns,
            actualOriginalHelperReturns=native_returns - source_linked_returns,
            actualSourceLinkedHeaderReturns=source_linked_returns,
            sourceLinkedReturnsIncludedInNativeDependencyTotal=True,
            suppliedCalls=0, coverage=coverage, instructionBound=20000, freshMachinePerExecution=True,
            actualReturnFrameControlStateAndStackGuardsRequired=True, allMappedWritesProtected=True,
            models=['Heap signature/bounds/low-byte options and native debug-fill word',
                'Empty/root/nested/nonfirst/sibling parent selection and doubly linked list/count updates',
                'Expanded-heap free block signature/size, free/used roots and group/feature initialization'],
            traceArchive=dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace), decodedSha256=hashlib.sha256(raw).hexdigest())),
        comparativeReference=dict(path='evidence/research/20261101-main-heap-common-reference.json',
            sha256=sha256(ROOT / 'evidence/research/20261101-main-heap-common-reference.json'), compilerInput=False,
            sameHistoricalSdkRevisionProven=False),
        negativeEvidence=dict(compiledReturningControls=controls, boundedPrefixReturnCredit=0),
        replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace))],
        reproductionCommand='python match_main_heap_initializers276_20261101.py',
        limitations=['Aligned disjoint mapped heaps, acyclic valid parent lists with bounded nesting; concurrent/cyclic/corrupted graphs are unsupported',
            'Original header initializer is declared void; raw R0 is compared without a public return-value claim',
            'Native fill is exercised only on aligned positive low-address spans with word-multiple lengths',
            'Original formal SDK types/revision and gameplay names are not established by the comparative source',
            'Lower helper source credit is zero; no source-only whole-ROM or Windows-game claim'])
    write_json(ROOT / 'evidence/matches/main-heap-initializers276-20261101.json', report)
    print(dict(newFunctions=2, newBytes=276, actualTopReturns=len(executions),
        actualNativeDependencyReturns=report['oracle']['actualNativeDependencyReturns'], suppliedCalls=0,
        negativeReturns=sum(control['actualReturns'] for control in controls),
        independentRejections=sum(control['independentRejections'] for control in controls)))


if __name__ == '__main__':
    main()
