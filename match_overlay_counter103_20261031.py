import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from overlay_counter103_fixture_20261031 import execute, SPANS
from overlay_counter103_models_20261031 import recipes, model
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCES = {'statea': ('ov001', 'src/overlays/ov001_20261031_statea103/statea.c'),
    'stateb': ('ov001', 'src/overlays/ov001_20261031_stateb103/stateb.c')}
PINS = ROOT / 'evidence/verification/overlay-counter103-inputs-20261031.json'
PINS_HASH = '793b05f5a8742453fcfdd72f12c62a70b5444c62dbcfae36d16fa0e9436417ed'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run_one(kind, config, main, main_metadata, pins):
    module, source_path = SOURCES[kind]
    source = ROOT / source_path
    entry, size = SPANS[kind]
    work = ROOT / ('work/ol103-proof/' + kind)
    metadata, overlay, unused = measured_module(module)
    compiler.WORK = work / 'c'
    rows, unused = compiler.compare(source, module, '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != size or not rows[0].get('exactAfterDeclaredRelocation'):
        raise ValueError(('Counter103 full caller source differs', kind))
    row = rows[0]
    row['sourceDependencies'] = [dict(path=str(source.with_name('context.h').relative_to(ROOT)), sha256=sha256(source.with_name('context.h')))]
    bindings = qualified_bindings(row)
    directory = work / 'l' / row['objectSha256']
    link = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = work / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(link))
    candidate = bytearray(overlay)
    offset = entry - 0x021D7240
    candidate[offset:offset + size] = linked
    if bytes(candidate) != overlay:
        raise ValueError('Counter103 full original/source overlay image differs')
    results, summaries, observed = [], [], set()
    for index, recipe in enumerate(recipes(kind)):
        original, rebuilt = execute(kind, main, overlay, recipe), execute(kind, main, bytes(candidate), recipe)
        if original != rebuilt:
            raise ValueError(('Counter103 full original/source machine differs', kind, index))
        results.append(dict(recipe=recipe, result=original))
        for pc in original['pcTrace']:
            if entry <= pc < entry + size:
                observed.update(range(pc, pc + 4))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)), actualReturns=2,
            nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']), providedCalls=2 * len(original['providedCalls']), instructions=original['instructions'],
            ramSha256=original['ramSha256'], stackSha256=original['stackSha256'],
            pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
    control = ROOT / ('nonmatching/overlay-lane/20261031-counter103-' + kind + '-negative')
    control.mkdir(parents=True, exist_ok=True)
    before, after = ('> 0x28U', '> 0x29U') if kind == 'statea' else ('> 0x2DU', '> 0x2EU')
    body = source.read_text().replace(before, after)
    if body == source.read_text():
        raise ValueError('Locate independent counter103 C control')
    for path, content in [(control / 'source.c', body.encode()), (control / 'context.h', source.with_name('context.h').read_bytes())]:
        if path.exists() and path.read_bytes() != content:
            raise ValueError('Preserve prior counter103 negative source')
        path.write_bytes(content)
    compiler.WORK = work / 'negative/c'
    bad_rows, unused = compiler.compare(control / 'source.c', module, '2', 'off', True)
    if len(bad_rows) != 1 or bad_rows[0].get('compileFailed'):
        raise ValueError('Counter103 negative source must compile')
    bad_directory = work / 'negative/l'
    try:
        bad_link = validate(bad_rows[0], qualified_bindings(bad_rows[0]), bad_directory)
    except ValueError as error:
        bad_link = error.args[0]
    if not isinstance(bad_link, dict) or bad_link.get('caller') != bad_rows[0]['name']:
        raise ValueError('Counter103 negative source must genuinely link')
    recipe = next(r for r in recipes(kind) if r['phase'] == 10 and r['counter'] == (40 if kind == 'statea' else 45) and r['variant'] == 0)
    try:
        execute(kind, main, overlay, recipe, (bad_directory / 'caller.bin').read_bytes())
    except ValueError as error:
        failure = error.args[0]
        expected = 'Counter103 independent complete RAM model differs' if kind == 'statea' else 'Counter103 independent return/native/provider completion differs'
        if (failure if isinstance(failure, str) else failure[0]) != expected:
            raise ValueError(('Counter103 unexpected negative rejection', kind, failure))
    else:
        raise ValueError('Counter103 negative C unexpectedly passed')
    raw = encoded(dict(romSha256=config['romSha256'], module=module, address=hex(entry), results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = work / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    row['oracle'] = dict(supported=True, evidenceClass='original caller with independent complete raw-field/conditional-provider/return/write models',
        actualReturns=2 * len(results), executions=2 * len(results), nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns'] for r in summaries),
        providedCalls=sum(r['providedCalls'] for r in summaries), instructionBound=5000,
        maximumNativeInstructions=max(r['instructions'] for r in summaries), observedNativeCallerInstructionBytes=len(observed),
        freshMachinePerExecution=True, completeImageEquality=True, results=summaries,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed),
            gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
        limitations=['StateA retains only supplied lower bodies; StateB executes original three raw input getters and qualified side/slot pool lookup with actual return/frame checks',
            'Both contexts/counters/phases/IDs/fields remain raw; no valid actor, scene, mechanics, resources or persistent lifecycle claim',
            'Callbacks change cached inputs and later state fields; independent models distinguish caller overwrites, late field reads and provider changes surviving after the final caller reset',
            'All byte increments wrap0..255; threshold40/45 sequential phases are modeled within one invocation, with full-word callback results treated as zero/nonzero only where native tests them',
            'No RNG or supplied action/UI body receives native/source credit; no original executable blob or assembly source'])
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], processor='arm9', program='', module=module, mode='arm',
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=[row], isolatedLink=link,
        nativeSourceBytes=size, functionMatches=1, acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False,
        rejectedCControl=dict(failure=failure, recipe=recipe, compilation=bad_rows, genuineLink=bad_link, sourceCredit=0),
        inputPins=pins['files'] + [dict(path=str(path.relative_to(ROOT)), sha256=sha256(path)) for path in [control / 'source.c', control / 'context.h']],
        generatorSha256=sha256(Path(__file__)), reproductionCommand='python match_overlay_counter103_20261031.py',
        limitations=['Shared integration/module/ROM acceptance remains integrator owned', 'createdUtc is volatile; stable identity excludes only that field',
            'Original executable scaffolding/providers/disassembly receive zero reconstructed source credit; no accepted source/preferences/application files edited'])
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(ROOT / ('evidence/matches/' + module + '-20261031-' + kind + '103.json'), report)
    print(json.dumps(dict(kind=kind, bytes=size, **{key: row['oracle'][key] for key in ['actualReturns', 'nativeDependencyActualReturns', 'providedCalls', 'observedNativeCallerInstructionBytes']})), flush=True)


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4' or sha256(PINS) != PINS_HASH:
        raise ValueError('Counter103 pinned runtime/source manifest differs')
    pins = json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError(('Counter103 frozen source/input differs', item['path']))
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Counter103 measured private ROM differs')
    main_metadata, main, unused = measured_module('main')
    for kind in SOURCES:
        run_one(kind, config, main, main_metadata, pins)


if __name__ == '__main__':
    run()
