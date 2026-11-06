import gzip
import hashlib
import json
from pathlib import Path
import match_runtime as compiler
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import main_global_width_fixture_20261101 as fixture

WORK = ROOT / 'work/main-global-width780-20261101'
FOLDER = ROOT / 'src/runtime/20261101_global_width780'
CONTROLS = {
    0x0201980C: ('*native_data_020ec588 = arg0;', '*native_data_020ec588 = arg0 + 4;'),
    0x0201434C: ('return *native_data_020ec36c + 0x1772;', 'return *native_data_020ec36c + 0x1776;'),
    0x0200C2C8: ('return 4U;', 'return 5U;'),
    0x020143D0: ('== 7)', '== 8)'),
    0x0202E958: ('s32 *, 0xC)', 's32 *, 0x10)'),
    0x020D34FC: ('*native_data_021d71ec = 0;', '*native_data_021d71ec = 2;'),
    0x02002C14: ('temp_r0 = temp_ip & ~0x30000;', 'temp_r0 = temp_ip & ~0x10000;'),
    0x0200BCDC: ('*native_data_020e5358 = 1;', '*native_data_020e5358 = 3;'),
    0x02014324: ('u32 *, 0x14E4) = arg0;', 'u32 *, 0x14E4) = arg0 ^ 1;'),
    0x02006DE4: ('0x82000001', '0x82000003')}


def build(source, label, original, exact):
    flags = original['compilerFlags']
    compiler.WORK = WORK / label / 'compile'
    rows, unused = compiler.compare(source, 'main', int(flags[0][2:]), flags[flags.index('-inline') + 1],
        speed='-opt' in flags and flags[flags.index('-opt') + 1] == 'speed', compiler=ROOT / original['compilerPath'])
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
    survey_path = ROOT / 'evidence/attempts/root-global-width-survey-20261101.json'
    survey = read_json(survey_path)
    candidates = [row for row in survey['results'] if row['exactNativeBytes']
        and int(row['identity']['address'], 0) in CONTROLS]
    assert len(candidates) == 10
    FOLDER.mkdir(parents=True, exist_ok=True)
    matches, traces, controls = [], [], []
    own_observed, irq_observed = {}, set()
    irq_returns = supplied = 0
    for candidate in sorted(candidates, key=lambda row: int(row['identity']['address'], 0)):
        source_input = ROOT / candidate['source']
        assert sha256(source_input) == candidate['sourceSha256']
        entry = int(candidate['identity']['address'], 0)
        source = FOLDER / f'native_main_{entry:08x}.c'
        text = source_input.read_text()
        if source.exists():
            assert source.read_text() == text
        else:
            source.write_text(text, encoding='utf-8')
        row, proof, body = build(source, f'correct-{entry:08x}', candidate['compilation'], True)
        size = candidate['identity']['initializedBytes']
        original_body = image[entry - 0x02000000:entry - 0x02000000 + size]
        assert len(body) == size and body == original_body
        own = set()
        cases = []
        for index in range(192):
            original = fixture.execute(image, entry, original_body, index)
            recovered = fixture.execute(image, entry, body, index)
            assert original == recovered and original['modelPassed'], (hex(entry), index, original)
            own.update(original['ownedObserved'])
            irq_observed.update(original['irqObserved'])
            irq_returns += original['actualIrqReturns'] * 2
            supplied += len(original['calls']) * 2
            cases.append(dict(index=index, original=original, candidate=recovered))
        before, after = CONTROLS[entry]
        assert text.count(before) == (2 if entry == 0x02006DE4 else 1)
        wrong = ROOT / f'nonmatching/integration/20261101-global-width-controls/{entry:08x}/source.c'
        wrong.parent.mkdir(parents=True, exist_ok=True)
        changed = text.replace(before, after)
        if wrong.exists():
            assert wrong.read_text() == changed
        else:
            wrong.write_text(changed, encoding='utf-8')
        bad_row, bad_proof, bad_body = build(wrong, f'wrong-{entry:08x}', candidate['compilation'], False)
        bad_cases = [fixture.execute(image, entry, bad_body, index) for index in range(48)]
        rejected = sum(not case['modelPassed'] for case in bad_cases)
        assert rejected, hex(entry)
        controls.append(dict(address=hex(entry), compilation=bad_row, genuineLinkComparison=bad_proof,
            actualReturns=48, independentRejections=rejected, unchangedPositives=48 - rejected, cases=bad_cases))
        row.update(genuineLinkComparison=freeze_link(proof), exactBytes=size,
            sourceOnlyCompilerInput=True, originalObjectScaffolding=False)
        matches.append(row)
        traces.append(dict(address=hex(entry), pairs=cases))
        own_observed[hex(entry)] = sorted(own)
        print(dict(address=hex(entry), exactBytes=size, actualPairedReturns=384, wrongRejections=rejected), flush=True)
    try:
        fixture.execute(image, 0x02006DE4, image[0x6DE4:0x6DFC], 0, bound=1)
    except AssertionError:
        pass
    else:
        raise AssertionError('Bounded prefix counted as a completed return')
    trace = ROOT / 'evidence/traces/main-global-width780-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    trace.write_bytes(gzip.compress(raw, mtime=0))
    dependencies = [dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace)),
        dict(path=survey_path.relative_to(ROOT).as_posix(), sha256=sha256(survey_path)),
        dict(path='main_global_width_fixture_20261101.py', sha256=sha256(ROOT / 'main_global_width_fixture_20261101.py'))]
    for candidate in candidates:
        dependencies.append(dict(path=candidate['source'], sha256=candidate['sourceSha256']))
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=matches, matchedFunctions=10, matchedBytes=sum(row['bytes'] for row in matches),
        oracle=dict(pairs=1920, actualTopReturns=3840, actualIrqReturnsSeparate=irq_returns,
            suppliedCallsSeparate=supplied, ownedInstructionAddresses=own_observed,
            originalIrqInstructionAddressesSeparate=sorted(irq_observed), actualReturnRequired=True,
            fullCoreFlagsPagesGlobalsStackAndOrderedWritesCompared=True,
            independentModel='Per-entry full-word/halfword effects, branch predicates, service input words and bounded provider effects'),
        negativeEvidence=dict(compiledWrongSources=controls, actualWrongReturns=480,
            independentRejections=sum(row['independentRejections'] for row in controls), prefixCompletionCredit=0),
        replayDependencies=dependencies, reproductionCommand='python match_main_global_width780_20261101.py',
        limitations=['Compatible measured global access widths only; full aggregate extents and historical names unproved',
            'All non-IRQ callees are explicitly supplied boundaries; original queues, threads, allocation and service semantics unproved',
            'Copy/clear are supplied bounded memory-effect contracts, not original native helper execution',
            'Display register uses isolated mapped RAM; actual hardware display behavior is not tested',
            'Finite valid pointers/slots and single-thread contexts only; no malformed, concurrent or permanent-wait coverage',
            'The separately reconstructed list60 is excluded, and no helper bytes are credited',
            'Whole-module/source-only ROM and a full Windows game remain separate gates'])
    assert report['matchedBytes'] == 780
    write_json(ROOT / 'evidence/matches/main-global-width780-20261101.json', report)
    print(dict(newFunctions=10, initializedBytes=780, actualTopReturns=3840, sourceAcceptancePending=True))


if __name__ == '__main__':
    main()
