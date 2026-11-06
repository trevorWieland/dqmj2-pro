import gzip
import hashlib
import json
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as compiler
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import main_slot_initializer96_fixture_20261101 as initializer
import main_slot_reference56_fixture_20261101 as caller

WORK = ROOT / 'work/slot-core152-proof-20261101'
FOLDER = ROOT / 'src/runtime/20261101_slot_core152'


def build(source, label, profile, exact):
    compiler.WORK = WORK / label / 'compile'
    executable = ROOT / f'tools/mwccarm/mwccarm/{profile}/mwccarm.exe'
    rows, unused = compiler.compare(source, 'main', 2, 'off', compiler=executable)
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
    source96 = FOLDER / 'native_main_0203b5d8.c'
    source56 = FOLDER / 'native_main_0203a650.c'
    row96, proof96, body96 = build(source96, 'initializer', '2.0/sp1p6', True)
    row56, proof56, body56 = build(source56, 'caller', '2.0/base', True)
    start = initializer.ENTRY - 0x02000000
    native96 = image[start:start + initializer.SIZE]
    native56 = image[caller.ENTRY - 0x02000000:caller.ENTRY - 0x02000000 + caller.SIZE]
    assert body96 == native96 and body56 == native56
    source_image = image[:start] + body96 + image[start + initializer.SIZE:]
    cases, owned, lower, connected_defined = [], set(), set(), 0
    direct_native_returns = connected_native_returns = provided = 0
    for index in range(512):
        first = initializer.execute(image, native96, index)
        second = initializer.execute(image, body96, index)
        assert first == second
        owned.update(first['observed'])
        lower.update(first['helperObserved'])
        direct_native_returns += first['actualNativeDependencyReturns'] * 2
        provided += first['suppliedCalls'] * 2
        cases.append(dict(kind='initializer', index=index, cDefinedDomain=True, original=first, candidate=second))
        original = caller.execute(image, native56, index)
        recovered = caller.execute(source_image, body56, index)
        assert original == recovered
        calls = original['calls']
        raw_count = calls[0][1][1] if calls else 0
        signed_count = raw_count - 0x100000000 if raw_count & 0x80000000 else raw_count
        defined = not calls or signed_count <= 0 or (index // 8 + index // 72) % 2 == 1
        connected_defined += int(defined)
        connected_native_returns += original['actualNativeDependencyReturns'] * 2
        cases.append(dict(kind='source-linked-caller', index=index, cDefinedDomain=defined,
            original=original, candidate=recovered))
    assert len(owned) == 96 and len(lower) == 68
    controls = []
    for number, (before, after) in enumerate([
        ('state->count = count;', 'state->count = (s32)((u32)count + 1);'),
        ('mask |= 1U << slots[index];', 'mask ^= 1U << slots[index];')]):
        text = source96.read_text(encoding='utf-8')
        assert text.count(before) == 1
        path = ROOT / f'nonmatching/integration/20261101-slot-core152-controls/{number}/source.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        header = os.path.relpath(FOLDER / 'state.h', path.parent).replace('\\', '/')
        text = text.replace(before, after).replace('#include "state.h"', '#include "' + header + '"')
        if path.exists():
            assert path.read_text(encoding='utf-8') == text
        path.write_text(text, encoding='utf-8')
        bad, bad_proof, bad_body = build(path, 'negative-' + str(number), '2.0/sp1p6', False)
        results = [initializer.execute(image, bad_body, index, require_model=False) for index in range(144)]
        rejected = sum(not result['modelPassed'] for result in results)
        assert rejected > 0
        controls.append(dict(compilation=bad, genuineLinkComparison=bad_proof,
            actualReturns=144, independentRejections=rejected, unchangedPositives=144 - rejected, cases=results))
    try:
        initializer.execute(image, native96, 0, bound=1)
    except AssertionError:
        pass
    else:
        raise AssertionError('Exhausted prefix is not a completed return')
    trace = ROOT / 'evidence/traces/main-slot-core152-20261101.json.gz'
    raw = json.dumps(cases, sort_keys=True, separators=(',', ':')).encode()
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(raw, mtime=0))
    header = dict(path=(FOLDER / 'state.h').relative_to(ROOT).as_posix(), sha256=sha256(FOLDER / 'state.h'))
    for row, proof, size in [(row96, proof96, 96), (row56, proof56, 56)]:
        row.update(genuineLinkComparison=freeze_link(proof), exactBytes=size, sourceOnlyCompilerInput=True,
            originalObjectScaffolding=False, sourceDependencies=[header])
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=[row96, row56], matchedFunctions=2, matchedBytes=152, newFunctionCandidates=1, newByteCandidates=96,
        zeroByteMigrationFunctions=1, zeroByteMigrationBytes=56,
        fixtures=[dict(path=name, sha256=sha256(ROOT / name)) for name in
            ['main_slot_initializer96_fixture_20261101.py', 'main_slot_reference56_fixture_20261101.py']],
        nativeDependencies=[dict(address='0x020388dc', mode='arm', bytes=72,
            targetSha256=hashlib.sha256(image[0x388DC:0x38924]).hexdigest(), newSourceCredit=0)],
        oracle=dict(directPairs=512, directActualTopReturns=1024, directActualNativeReturns=direct_native_returns,
            connectedPairs=512, connectedActualTopReturns=1024, connectedActualNativeReturns=connected_native_returns,
            connectedCDefinedPairs=connected_defined, connectedBinaryOnlyPairs=512 - connected_defined,
            actualSourceLinkedInitializer=True, providedWordServiceCalls=provided,
            newCodeBytesObserved=96, originalReservationCodeBytesObserved=68,
            actualReturnRequired=True, fullPagesStackCpuAndOrderedStores=True,
            independentModel='Sequential aliased byte copies; slot-bit reservation conflict/success; count/mask stores and unsigned caller reference wrap',
            traceArchive=dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace),
                decodedSha256=hashlib.sha256(raw).hexdigest())),
        negativeEvidence=dict(compiledReturningControls=controls, prefixCompletionCredit=0),
        replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace))],
        reproductionCommand='python match_main_slot_core152_20261101.py',
        limitations=['Slot IDs0..31 and counts negative/zero or0..32 in the initializer C domain',
            'Connected cases with positive counts and slot bytes >=32 establish only original/compiled ARM behavior, not portable C shift semantics',
            'Word command entry020092A4 is an explicit two-word provider; actual reservation helper executes and receives zero duplicate credit',
            'Header is a compatible measured prefix view, not a historical full aggregate extent or API name',
            'Both sp1p5 and sp1p6 match this initializer; chosen profile is demonstrated, not uniquely identified',
            'No real command queue, malformed pointers, concurrency, module acceptance or full native game proof'])
    output = ROOT / 'evidence/matches/main-slot-core152-20261101.json'
    write_json(output, report)
    print(dict(newFunctions=1, newBytes=96, zeroMigrationBytes=56, directTopReturns=1024,
        connectedTopReturns=1024, connectedCDefinedPairs=connected_defined,
        suppliedWordCalls=provided, wrongActualReturns=288,
        independentRejections=sum(control['independentRejections'] for control in controls)))


if __name__ == '__main__':
    main()
