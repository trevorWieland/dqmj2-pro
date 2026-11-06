import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as compiler
from main_irq_guarded_getters_fixture_20261101 import ENTRIES, IRQ, execute
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/irq-guarded-getters140-20261101'


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
        0x020099E0: ('var_r4 = native_data_020e3780.field_20;', 'var_r4 = native_data_020e3780.field_4;'),
        0x02011EB4: ('u16 *, 0x150', 'u8 *, 0x150'),
        0x02011EE4: ('return (u32) (u16) var_r4;', 'return (u32) (u8) var_r4;')}
    for entry, size in ENTRIES.items():
        source = ROOT / f'src/runtime/20261101_irq_guarded_getters/native_main_{entry:08x}.c'
        row, proof, body = build(source, f'{entry:08x}/positive', True)
        native = image[entry - 0x02000000:entry - 0x02000000 + size]
        assert native == body and row['bytes'] == size
        observed, helpers = set(), set()
        for index in range(640):
            first, second = execute(image, entry, native, index), execute(image, entry, body, index)
            assert first == second
            observed.update(first['observed'])
            helpers.update(first['helperObserved'])
            cases.append(dict(entry=hex(entry), original=first, candidate=second))
        assert len(observed) == size - 4 and len(helpers) == 44
        row.update(genuineLinkComparison=freeze_link(proof), exactBytes=size,
            sourceOnlyCompilerInput=True, originalObjectScaffolding=False,
            oracle=dict(pairs=640, actualTopReturns=1280, actualNativeDependencyReturns=2560,
                suppliedCalls=0, ownCodeBytesObserved=len(observed), generatedLiteralBytes=4))
        matches.append(row)
        text = source.read_text()
        before, after = changes[entry]
        assert text.count(before) == 1
        changed = text.replace(before, after)
        path = ROOT / f'nonmatching/integration/20261101-irq-getter-controls/{entry:08x}/source.c'
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
    raw = json.dumps(cases, sort_keys=True, separators=(',', ':')).encode()
    trace = ROOT / 'evidence/traces/main-irq-guarded-getters140-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(raw, mtime=0))
    dependencies = [dict(processor='arm9', program='', module='main', mode='arm', address=hex(entry), bytes=size,
        targetSha256=hashlib.sha256(image[entry-0x02000000:entry-0x02000000+size]).hexdigest())for entry,size in IRQ.items()]
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        fixture='main_irq_guarded_getters_fixture_20261101.py', fixtureSha256=sha256(ROOT/'main_irq_guarded_getters_fixture_20261101.py'),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=matches, matchedFunctions=3, matchedBytes=140, nativeDependencies=dependencies,
        oracle=dict(pairs=1920, actualTopReturns=3840, actualNativeDependencyReturns=7680, suppliedCalls=0,
            ownCodeBytesObserved=128, generatedLiteralBytes=12, freshMachinePerExecution=True,
            actualReturnFrameAndControlStateRequired=True, fullPagesRegistersFlagsAndOrderedEffectsCompared=True,
            independentModels=['Selector word chooses current or saved global word',
                'Nullable object pointer yields offset336 unsigned halfword or zero',
                'Nullable object pointer yields offset332 word narrowed to16 bits or zero'],
            traceArchive=dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace),decodedSha256=hashlib.sha256(raw).hexdigest())),
        negativeEvidence=dict(compiledReturningControls=controls, exhaustedPrefixReturnCredit=0),
        replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace))],
        reproductionCommand='python match_main_irq_guarded_getters140_20261101.py',
        limitations=['Synthetic aligned mapped objects and nullable object pointer; malformed unmapped pointers are unsupported',
            'Original native IRQ helpers execute; zero helper source credit',
            'No concurrent mutation, scene availability, whole-module acceptance or source-only game claim'])
    write_json(ROOT/'evidence/matches/main-irq-guarded-getters140-20261101.json',report)
    print(dict(newFunctions=3,newBytes=140,actualTopReturns=3840,actualNativeDependencyReturns=7680,
        wrongReturns=sum(x['actualReturns']for x in controls),independentRejections=sum(x['independentRejections']for x in controls),suppliedCalls=0))


if __name__ == '__main__':
    main()
