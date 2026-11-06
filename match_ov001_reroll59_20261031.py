import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_reroll59_fixture_20261031 import execute
from ov001_reroll59_models_20261031 import recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCE = ROOT / 'src/overlays/ov001_20261031_reroll59/reroll.c'
SOURCE_HASH, HEADER_HASH = '596e11dccf2051376ca26986cbbc6dbadc74b6c20fbddcc9988217e55628be1f', '0b8a6260e32fd6ac65bfc4f4da83f6755d9b960b1b15e5f04b7cf5b698901dd4'
WORK = ROOT / 'work/ol59-proof'
REPORT = ROOT / 'evidence/matches/ov001-20261031-reroll59.json'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Pinned Python/Unicorn differs')
    if sha256(SOURCE) != SOURCE_HASH or sha256(SOURCE.with_name('context.h')) != HEADER_HASH:
        raise ValueError('Frozen reroll59 source/header differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private input differs')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 356 or not rows[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Full356-byte ordinary reroll caller C differs')
    row = rows[0]
    row['sourceDependencies'] = [dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)), sha256=HEADER_HASH)]
    bindings = qualified_bindings(row)
    directory = WORK / 'l' / row['objectSha256']
    proof = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    candidate = bytearray(overlay)
    offset = 0x0220C888 - 0x021D7240
    candidate[offset:offset + 356] = linked
    if bytes(candidate) != overlay:
        raise ValueError('Full original/source reroll59 module image differs')
    results, summaries = [], []
    for index, recipe in enumerate(recipes()):
        original, rebuilt = execute(main, overlay, recipe), execute(main, bytes(candidate), recipe)
        if original != rebuilt:
            raise ValueError('Reroll59 original/source complete machines differ')
        results.append(dict(recipe=recipe, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)),
            actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']),
            providedCalls=2 * len(original['providedCalls']), instructions=original['instructions'],
            observedNativeCallerInstructionBytes=len({pc + offset for pc, size in original['observedNativeCallerInstructionRanges'] for offset in range(size)}), ramSha256=original['ramSha256'],
            stackSha256=original['stackSha256'], pcTraceSha256=original['pcTraceSha256'], writeTraceSha256=original['writeTraceSha256']))
    control = ROOT / 'nonmatching/overlay-lane/20261031-reroll59-negative'
    control.mkdir(parents=True, exist_ok=True)
    before = 'native_data_ov001_0223e088.field_3 = 0xE;'
    body = SOURCE.read_text().replace(before, before.replace('0xE;', '0xF;'))
    if body == SOURCE.read_text():
        raise ValueError('Locate actual full-word store mutation')
    for path, text in [(control / 'source.c', body), (control / 'context.h', SOURCE.with_name('context.h').read_text())]:
        if path.exists() and path.read_bytes() != text.encode():
            raise ValueError('Preserve prior state control source')
        path.write_bytes(text.encode())
    compiler.WORK = WORK / 'rejected-state/c'
    bad_rows, unused = compiler.compare(control / 'source.c', 'ov001', '2', 'off', True)
    if len(bad_rows) != 1 or bad_rows[0].get('compileFailed'):
        raise ValueError('State source control failed compilation')
    bad_directory = WORK / 'rejected-state/l'
    try:
        rejected_link = validate(bad_rows[0], qualified_bindings(bad_rows[0]), bad_directory)
    except ValueError as error:
        rejected_link = error.args[0]
    if not isinstance(rejected_link, dict) or rejected_link.get('caller') != bad_rows[0]['name']:
        raise ValueError('State source control did not genuinely link')
    try:
        execute(main, overlay, recipes()[0], (bad_directory / 'caller.bin').read_bytes())
    except ValueError as error:
        failure = error.args[0]
        if failure != 'Reroll59 independent complete RAM/RNG model differs':
            raise ValueError(('State control rejected unexpectedly', failure))
    else:
        raise ValueError('State source control unexpectedly passed')
    raw = encoded(dict(romSha256=config['romSha256'], module='ov001', address='0x0220C888', results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    row['oracle'] = dict(supported=True, evidenceClass='original native byte-state caller with actual context selectors, side/slot pool lookup, seeded RNG and original divider; independent full RAM/state/RNG/protocol models',
        executions=2 * len(results), actualReturns=2 * len(results),
        nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns'] for r in summaries), providedCalls=sum(r['providedCalls'] for r in summaries),
        rngActualReturns=sum(row['result']['rngActualReturns'] * 2 for row in results), rngCountIncludedInNativeDependencyTotal=True, freshMachinePerExecution=True, instructionBound=5000, maximumNativeInstructions=max(r['instructions'] for r in summaries),
        completeImageEquality=True, observedNativeCallerInstructionBytes=len({pc + offset for row in results for pc, size in row['result']['observedNativeCallerInstructionRanges'] for offset in range(size)}), results=summaries,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed),
            format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
        limitations=['Synthetic context0223E088 has raw phases0/A/14/1E/64/FF, byte counters, selector side/slot/native ID and full signed threshold words',
            'RNG0203D294 and original software divider02026350 execute, with seeded state set by explicit threshold provider before actual load/update; no observed live/future game state',
            'Actual selectors read bytes1A/1B/1C and nativeDB438 returns address-qualified pool entries or0; no valid actor allocation/lifecycle is established',
            'Threshold and two action/query bodies remain explicit providers, including null/invalid slot-derived opaque addresses, without scene/action semantics',
            'Actual RNG returns are a subset of nativeDependencyActualReturns and must never be added again',
            'All final registers/flags/full RAM/private stack and deterministic PC/write traces compare, with actual return/SP/preserved-register/native completion gates'])
    paths = [str(SOURCE.relative_to(ROOT)), str(SOURCE.with_name('context.h').relative_to(ROOT)),
        'ov001_reroll59_fixture_20261031.py', 'ov001_reroll59_models_20261031.py', 'ov001_ability28_fixture_20261031.py',
        str((control / 'source.c').relative_to(ROOT)), str((control / 'context.h').relative_to(ROOT))]
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], processor='arm9', program='', module='ov001', mode='arm',
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=[row],
        nativeSymbols={item['symbol']: item['target'] for item in row['relocations']}, isolatedLink=proof,
        nativeSourceBytes=356, functionMatches=1, acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False,
        rejectedCompletionMarker=dict(expectedRejected=True, failure=failure, compilation=bad_rows, actualLinkComparison=rejected_link, sourceCredit=0),
        inputPins=[dict(path=p, sha256=sha256(ROOT / p)) for p in paths], generatorSha256=sha256(Path(__file__)),
        limitations=['Final registration/module/ROM gates remain the integrator responsibility', 'createdUtc is volatile; stable identity excludes only that field',
            'No executable blobs, assembly, opcode modifications, fake register inputs or dependency source credit'],
        reproductionCommand='python match_ov001_reroll59_20261031.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(REPORT, report)
    print(json.dumps({key: row['oracle'][key] for key in ['executions', 'nativeDependencyActualReturns', 'providedCalls', 'maximumNativeInstructions']}), flush=True)


if __name__ == '__main__':
    run()
