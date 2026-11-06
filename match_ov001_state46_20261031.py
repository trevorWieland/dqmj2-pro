import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_state46_fixture_20261031 import execute
from ov001_state46_models_20261031 import recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCE = ROOT / 'src/overlays/ov001_20261031_state46/state.c'
SOURCE_HASH, HEADER_HASH = '8877278d0b65729335895020975c0c0c421504fc15ab94a6ee25acda7a9f8cd4', 'f8de4485c321decbd4bfb9684f1537448f566fbb9cce41a609569520f858bb63'
WORK = ROOT / 'work/ol46-proof'
REPORT = ROOT / 'evidence/matches/ov001-20261031-state46.json'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Pinned Python/Unicorn differs')
    if sha256(SOURCE) != SOURCE_HASH or sha256(SOURCE.with_name('context.h')) != HEADER_HASH:
        raise ValueError('Frozen state46 source/header differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private input differs')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 340 or not rows[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Full340-byte ordinary state C differs')
    row = rows[0]
    row['sourceDependencies'] = [dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)), sha256=HEADER_HASH)]
    bindings = qualified_bindings(row)
    directory = WORK / 'l' / row['objectSha256']
    proof = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    candidate = bytearray(overlay)
    offset = 0x021EACB0 - 0x021D7240
    candidate[offset:offset + 340] = linked
    if bytes(candidate) != overlay:
        raise ValueError('Full original/source state46 module image differs')
    results, summaries, observed = [], [], set()
    for index, recipe in enumerate(recipes()):
        original, rebuilt = execute(main, overlay, recipe), execute(main, bytes(candidate), recipe)
        if original != rebuilt:
            raise ValueError('State46 original/source complete machines differ')
        for pc in original['pcTrace']:
            if 0x021EACB0 <= pc < 0x021EACB0 + 340:
                observed.update(range(pc, pc + 4))
        results.append(dict(recipe=recipe, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)),
            actualReturns=2, nativeDependencyActualReturns=0, providedCalls=2 * len(original['providedCalls']),
            instructions=original['instructions'], ramSha256=original['ramSha256'], stackSha256=original['stackSha256'],
            pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
    control = ROOT / 'nonmatching/overlay-lane/20261031-state46-negative'
    control.mkdir(parents=True, exist_ok=True)
    before = 'M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 5;'
    body = SOURCE.read_text().replace(before, before.replace('= 5;', '= 6;'))
    if body == SOURCE.read_text():
        raise ValueError('Locate actual completion-marker mutation')
    for path, text in [(control / 'source.c', body), (control / 'context.h', SOURCE.with_name('context.h').read_text())]:
        if path.exists() and path.read_bytes() != text.encode():
            raise ValueError('Preserve prior marker control source')
        path.write_bytes(text.encode())
    compiler.WORK = WORK / 'rejected-marker/c'
    bad_rows, unused = compiler.compare(control / 'source.c', 'ov001', '2', 'off', True)
    if len(bad_rows) != 1 or bad_rows[0].get('compileFailed'):
        raise ValueError('Marker source control failed compilation')
    bad_directory = WORK / 'rejected-marker/l'
    try:
        rejected_link = validate(bad_rows[0], qualified_bindings(bad_rows[0]), bad_directory)
    except ValueError as error:
        rejected_link = error.args[0]
    if not isinstance(rejected_link, dict) or rejected_link.get('caller') != bad_rows[0]['name']:
        raise ValueError('Marker source control did not genuinely link')
    try:
        execute(main, overlay, next(r for r in recipes() if r['phase'] == 100), (bad_directory / 'caller.bin').read_bytes())
    except ValueError as error:
        failure = error.args[0]
        if failure != 'State46 complete RAM model differs':
            raise ValueError(('Marker control rejected unexpectedly', failure))
    else:
        raise ValueError('Marker source control unexpectedly passed')
    raw = encoded(dict(romSha256=config['romSha256'], module='ov001', address='0x021EACB0', results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    row['oracle'] = dict(supported=True, evidenceClass='original native actor/state caller with independent complete RAM/protocol/late-read/narrowing models and explicit lower providers',
        executions=2 * len(results), actualReturns=2 * len(results), nativeDependencyActualReturns=0,
        providedCalls=sum(r['providedCalls'] for r in summaries), observedNativeCallerInstructionBytes=len(observed),
        freshMachinePerExecution=True, instructionBound=1000, maximumNativeInstructions=max(r['instructions'] for r in summaries),
        completeImageEquality=True, results=summaries,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed),
            format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
        limitations=['Raw context02238D7C phase byte10 uses0/A/64; field13 completion marker5 is measured without a scene/animation meaning claim',
            'Actor1E4 zero/nonzero gates, side/slot bytes and full mode-return words are synthetic inputs; no valid actor/save/resource lifecycle or ordinary battle reachability',
            'All lower callbacks are supplied contracts, with explicit writes and zero native dependency credit; no native movement/audio/RNG effects are established',
            'Global flag is read after its preceding callback, mode word narrows to8 bits before later calls, and height pointer/value is read after its query callback',
            'All final registers/flags/full RAM/private stacks/PC/writes compare; actual return/SP/preserved-register gates are required'])
    paths = [str(SOURCE.relative_to(ROOT)), str(SOURCE.with_name('context.h').relative_to(ROOT)),
        'ov001_state46_fixture_20261031.py', 'ov001_state46_models_20261031.py', 'ov001_ability28_fixture_20261031.py',
        str((control / 'source.c').relative_to(ROOT)), str((control / 'context.h').relative_to(ROOT))]
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], processor='arm9', program='', module='ov001', mode='arm',
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=[row],
        nativeSymbols={item['symbol']: item['target'] for item in row['relocations']}, isolatedLink=proof,
        nativeSourceBytes=340, functionMatches=1, acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False,
        rejectedCompletionMarker=dict(expectedRejected=True, failure=failure, compilation=bad_rows, actualLinkComparison=rejected_link, sourceCredit=0),
        inputPins=[dict(path=p, sha256=sha256(ROOT / p)) for p in paths], generatorSha256=sha256(Path(__file__)),
        limitations=['Final registration/module/ROM gates remain the integrator responsibility', 'createdUtc is volatile; stable identity excludes only that field',
            'No executable blobs, assembly, stack padding, opcode modifications, fake register inputs or dependency source credit'],
        reproductionCommand='python match_ov001_state46_20261031.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(REPORT, report)
    print(json.dumps({key: row['oracle'][key] for key in ['executions', 'providedCalls', 'observedNativeCallerInstructionBytes', 'maximumNativeInstructions']}), flush=True)


if __name__ == '__main__':
    run()
