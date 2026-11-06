import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as compiler
from main_fifo_ack300_fixture_20261101 import ENTRIES, LOWER, execute
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/fifo-ack300-20261101'


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
    matches, cases, controls = [], [], []
    changes = {
        0x0200DDF4: ('0x38) | 1);', '0x38) | 2);'),
        0x0200DFD8: ('4)(2, 4, 0);', '4)(3, 4, 0);')}
    all_helpers = set()
    for entry, size in ENTRIES.items():
        source = ROOT / f'src/runtime/20261101_fifo_ack300/native_main_{entry:08x}.c'
        row, proof, body = build(source, f'{entry:08x}/positive', True)
        native = image[entry - 0x02000000:entry - 0x02000000 + size]
        assert native == body and row['bytes'] == size
        observed, helpers = set(), set()
        for index in range(384):
            first, second = execute(image, entry, native, index), execute(image, entry, body, index)
            assert first == second
            observed.update(first['observed'])
            helpers.update(first['helperObserved'])
            cases.append(dict(entry=hex(entry), original=first, candidate=second))
        assert len(observed) == 144 and len(helpers) == 176
        all_helpers.update(helpers)
        row.update(genuineLinkComparison=freeze_link(proof), exactBytes=size,
            sourceOnlyCompilerInput=True, originalObjectScaffolding=False,
            oracle=dict(pairs=384, actualTopReturns=768, actualNativeDependencyReturns=sum(x[side]['actualNativeDependencyReturns']for x in cases if x['entry']==hex(entry)for side in ['original','candidate']),
                suppliedCalls=0, ownCodeBytesObserved=len(observed), generatedLiteralBytes=size-144), sourceDependencies=[dict(path='src/runtime/20261101_fifo_ack300/state.h',sha256=sha256(ROOT/'src/runtime/20261101_fifo_ack300/state.h'))])
        matches.append(row)
        text = source.read_text()
        before, after = changes[entry]
        assert text.count(before) == 1
        changed = text.replace(before, after)
        changed = changed.replace('#include "state.h"', '#include "../../../../src/runtime/20261101_fifo_ack300/state.h"')
        path = ROOT / f'nonmatching/integration/20261101-fifo-ack-controls/{entry:08x}/source.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            assert path.read_text() == changed
        path.write_text(changed, encoding='utf-8')
        bad, badproof, badbody = build(path, f'{entry:08x}/negative', False)
        results = [execute(image, entry, badbody, index, require_model=False) for index in range(96)]
        rejects = sum(not result['modelPassed'] for result in results)
        assert rejects > 0
        controls.append(dict(entry=hex(entry), compilation=bad, genuineLinkComparison=badproof,
            actualReturns=len(results), independentRejections=rejects, unchangedPositiveCases=len(results)-rejects,
            cases=results))
        try:
            execute(image, entry, native, 0, bound=1)
        except AssertionError:
            pass
        else:
            raise AssertionError('Exhausted prefix cannot receive return credit')
    assert len(all_helpers) == 176
    raw = json.dumps(cases, sort_keys=True, separators=(',', ':')).encode()
    trace = ROOT / 'evidence/traces/main-fifo-ack300-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(raw, mtime=0))
    dependencies = [dict(processor='arm9', program='', module='main', mode='arm', address=hex(entry), bytes=size,
        targetSha256=hashlib.sha256(image[entry-0x02000000:entry-0x02000000+size]).hexdigest())for entry,size in LOWER.items()]
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        fixture='main_fifo_ack300_fixture_20261101.py', fixtureSha256=sha256(ROOT/'main_fifo_ack300_fixture_20261101.py'),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=matches, matchedFunctions=2, matchedBytes=300, nativeDependencies=dependencies,
        oracle=dict(pairs=768, actualTopReturns=1536, actualNativeDependencyReturns=sum(x[side]['actualNativeDependencyReturns']for x in cases for side in ['original','candidate']), suppliedCalls=0,
            ownCodeBytesObserved=288, generatedLiteralBytes=12, freshMachinePerExecution=True,
            actualReturnFrameAndControlStateRequired=True, fullPagesRegistersFlagsAndOrderedEffectsCompared=True,
            independentModels=['Successful send sets acknowledgement/clears failure halfwords before actual IRQ restoration',
                'Failed send restores IRQ before setting the failure halfword and selecting null/original three-word FIFO callback',
                'The deliberately selected mapped original callback is a physical word-ABI context; historical callback formal types/game availability are unproved'],
            traceArchive=dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace),decodedSha256=hashlib.sha256(raw).hexdigest())),
        negativeEvidence=dict(compiledReturningControls=controls, exhaustedPrefixReturnCredit=0),
        replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace))],
        reproductionCommand='python match_main_fifo_ack300_20261101.py',
        limitations=['Synthetic disposable FIFO-register byte snapshots; physical hardware and W1C status transitions are unproved',
            'ARM7 message processing, asynchronous completion, interrupt receivers and concurrency are outside this bounded one-shot proof',
            'Original FIFO sender is an explicit constructed callback endpoint on supported failing paths; no provided callback outcomes or extra callback source credit',
            'Only three request entries and the measured40-byte global prefix are covered; no full object, game-scene or source-only ROM claim'])
    write_json(ROOT/'evidence/matches/main-fifo-ack300-20261101.json',report)
    print(dict(newFunctions=2,newBytes=300,actualTopReturns=1536,actualNativeDependencyReturns=report['oracle']['actualNativeDependencyReturns'],
        wrongReturns=sum(x['actualReturns']for x in controls),independentRejections=sum(x['independentRejections']for x in controls),suppliedCalls=0))


if __name__ == '__main__':
    main()
