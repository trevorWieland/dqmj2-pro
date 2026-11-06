import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as compiler
from main_word_channels_fixture_20261101 import ENTRIES, COMMANDS, HARDWARE, execute
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/word-channels340-20261101'


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
        source = ROOT / f'src/runtime/20261101_word_channels/native_main_{entry:08x}.c'
        row, proof, body = build(source, f'{entry:x}-positive', True)
        native = image[entry - 0x02000000:entry - 0x02000000 + size]
        assert body == native
        observed = set()
        for index in range(256):
            original = execute(image, entry, native, index)
            candidate = execute(image, entry, body, index)
            assert original == candidate
            observed.update(original['observed'])
            cases.append(dict(entry=hex(entry), index=index, original=original, candidate=candidate))
        coverage[hex(entry)] = dict(instructionBytesObserved=len(observed), initializedBytes=size,
            literalBytes=size - len(observed))
        assert len(observed) == (20 if entry in HARDWARE else size)
        row.update(genuineLinkComparison=freeze_link(proof), exactBytes=size)
        matches.append(row)
        proofs.append(freeze_link(proof))
        text = source.read_text()
        if entry in COMMANDS:
            import re
            before = re.search(r'native_fn_02009470\((0x[0-9A-F]+|[0-9]+),', text).group(0)
            after = 'native_fn_02009470(arg0,'
        elif entry in HARDWARE:
            before = '= ' + hex(HARDWARE[entry][0]).upper().replace('0X', '0x') + ';'
            after = '= 0;'
        else:
            before, after = '+ arg0)', '+ 4)'
        assert text.count(before) == 1
        path = ROOT / f'nonmatching/integration/20261101-word-channel-controls/{entry:x}/source.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        changed = text.replace(before, after)
        if path.exists():
            assert path.read_text() == changed
        path.write_text(changed)
        bad, badproof, badbody = build(path, f'{entry:x}-negative', False)
        records = [execute(image, entry, badbody, index, require_model=False) for index in range(0, 256, 11)]
        rejected = sum(not result['modelPassed'] for result in records)
        assert rejected > 0
        controls.append(dict(entry=hex(entry), compilation=bad, genuineLinkComparison=badproof,
            actualReturns=sum(result['actualTopReturns'] for result in records),
            suppliedTailReturnCompletions=sum(result['suppliedTailReturnCompletions'] for result in records),
            actualInvocationCompletions=len(records), independentRejections=rejected, records=records))
        try:
            execute(image, entry, native, 0, bound=1)
        except AssertionError:
            pass
        else:
            raise AssertionError('Bounded prefix received false return credit')
    raw = json.dumps(cases, sort_keys=True, separators=(',', ':')).encode()
    trace = ROOT / 'evidence/traces/main-word-channels340-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        fixture='main_word_channels_fixture_20261101.py', fixtureSha256=sha256(ROOT / 'main_word_channels_fixture_20261101.py'),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=matches, matchedFunctions=12, matchedBytes=340, genuineLinkedByteComparisons=proofs,
        oracle=dict(pairs=len(cases), actualTopReturns=sum(case[side]['actualTopReturns'] for case in cases for side in ['original', 'candidate']),
            actualInvocationCompletions=2 * len(cases),
            suppliedTailReturnCompletions=sum(case[side]['suppliedTailReturnCompletions'] for case in cases for side in ['original', 'candidate']), actualNativeDependencyReturns=0,
            suppliedCalls=sum(case[side]['suppliedCalls'] for case in cases for side in ['original', 'candidate']), coverage=coverage, freshMachinePerExecution=True, instructionBound=128,
            actualReturnAndFrameRequired=True, allMappedWritesProtected=True,
            models=['Full-word five-argument channel forwarding', 'Ordered MMIO command and two-word helper forwarding', '32-bit in-place field rebasing'],
            traceArchive=dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace), decodedSha256=hashlib.sha256(raw).hexdigest())),
        negativeEvidence=dict(compiledReturningControls=controls),
        replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace))],
        reproductionCommand='python match_main_word_channels340_20261101.py',
        limitations=['Ten forwarding wrappers use explicit supplied callees; no helper implementation or hardware behavior is proved',
            'MMIO is a RAM-backed bus-payload model and wrappers are tested only with normally returning providers',
            'Three hardware wrappers tail-transfer to supplied services; their completions are separate from observed own-code returns',
            'Seven void callers expose raw R0 observations without establishing a public return-value contract',
            'Two rebasing routines are tested on aligned mapped fields, including full-width arithmetic wrap',
            'No scene availability, source-only module or source-only whole-ROM claim'])
    write_json(ROOT / 'evidence/matches/main-word-channels340-20261101.json', report)
    print(dict(newFunctions=12, newBytes=340, actualTopReturns=report['oracle']['actualTopReturns'],
        suppliedTailReturnCompletions=report['oracle']['suppliedTailReturnCompletions'],
        suppliedCalls=report['oracle']['suppliedCalls'],
        negativeReturns=sum(control['actualReturns'] for control in controls),
        independentRejections=sum(control['independentRejections'] for control in controls)))


if __name__ == '__main__':
    main()
