import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov005_slider20_fixture_20261030 import execute
from ov005_slider20_models_20261030 import recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCE = ROOT / 'src/overlays/ov005_20261030_slider20/slider.c'
SOURCE_HASH = '0de9c4307e51950c5e416d9dc4f92c159c692c1aebeadcfa0604eaa87b16515d'
HEADER_HASH = '5236324b83669ce90aa44cb4f9cb61b8db43ef4dda1ebb5c3945e9d58f696006'
WORK = ROOT / 'work/ol20-proof'
REPORT = ROOT / 'evidence/matches/ov005-20261030-slider20.json'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Pinned Python/Unicorn differs')
    if sha256(SOURCE) != SOURCE_HASH or sha256(SOURCE.with_name('context.h')) != HEADER_HASH:
        raise ValueError('Frozen slider20 source/header differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private input differs')
    metadata, overlay, unused = measured_module('ov005')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'c'
    records, unused = compiler.compare(SOURCE, 'ov005', '2', 'off', True)
    if len(records) != 1 or records[0].get('compiledBytes') != 464 or not records[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Full464-byte ordinary slider C differs')
    row = records[0]
    row['sourceDependencies'] = [dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)), sha256=HEADER_HASH)]
    bindings = qualified_bindings(row)
    directory = WORK / 'l' / row['objectSha256']
    proof = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    candidate = bytearray(overlay)
    offset = 0x021DB400 - 0x021D7240
    candidate[offset:offset + 464] = linked
    if bytes(candidate) != overlay:
        raise ValueError('Full original/rebuilt slider20 module image differs')
    results, summaries = [], []
    for index, recipe in enumerate(recipes()):
        original, rebuilt = execute(main, overlay, recipe), execute(main, bytes(candidate), recipe)
        if original != rebuilt:
            raise ValueError('Slider20 original/rebuilt complete machines differ')
        results.append(dict(recipe=recipe, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)),
            actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']),
            providedCalls=0, instructions=original['instructions'], returnWord=original['returnWord'],
            ramSha256=original['ramSha256'], ioSha256=original['ioSha256'], stackSha256=original['stackSha256'],
            pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
    control = ROOT / 'nonmatching/overlay-lane/20261030-slider20-negative'
    control.mkdir(parents=True, exist_ok=True)
    body = SOURCE.read_text().replace('native_data_ov005_021e9b48.field_7c |= 2;', 'native_data_ov005_021e9b48.field_7c = 0;')
    if body == SOURCE.read_text():
        raise ValueError('Locate actual flag mutation control')
    for path, content in [(control / 'source.c', body), (control / 'context.h', SOURCE.with_name('context.h').read_text())]:
        if path.exists() and path.read_bytes() != content.encode():
            raise ValueError('Preserve prior wrong-flag source control')
        path.write_bytes(content.encode())
    compiler.WORK = WORK / 'rejected-flag/c'
    bad_rows, unused = compiler.compare(control / 'source.c', 'ov005', '2', 'off', True)
    if len(bad_rows) != 1 or bad_rows[0].get('compileFailed'):
        raise ValueError('Flag mutation control failed compilation')
    rejected_directory = WORK / 'rejected-flag/l'
    try:
        rejected_proof = validate(bad_rows[0], qualified_bindings(bad_rows[0]), rejected_directory)
    except ValueError as error:
        rejected_proof = error.args[0]
    if not isinstance(rejected_proof, dict) or rejected_proof.get('caller') != bad_rows[0]['name']:
        raise ValueError('Wrong-flag control did not genuinely link')
    try:
        execute(main, overlay, next(r for r in recipes() if r['flag'] == 1), (rejected_directory / 'caller.bin').read_bytes())
    except ValueError as error:
        failure = error.args[0]
        if not isinstance(failure, tuple) or failure[0] != 'Slider20 complete RAM/write-order model differs':
            raise ValueError(('Wrong-flag control failed unexpectedly', failure))
    else:
        raise ValueError('Wrong-flag source control unexpectedly passed')
    active_recipe = dict(recipes()[0], objectType=1)
    try:
        execute(main, overlay, active_recipe)
    except ValueError as error:
        active_limit = error.args[0]
        if not isinstance(active_limit, tuple) or active_limit[0] != 'Unsupported slider20 active-object dependency':
            raise ValueError(('Active object audit failed unexpectedly', active_limit))
    else:
        raise ValueError('Active SDK path was unexpectedly modeled completely')
    raw = encoded(dict(romSha256=config['romSha256'], module='ov005', processor='arm9', mode='arm',
        address='0x021DB400', sourceSha256=SOURCE_HASH, results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    row['oracle'] = dict(supported=True, evidenceClass='original native caller/setters/guarded SDK chain with independent complete RAM/MMIO models and zero provided calls',
        executions=2 * len(results), actualReturns=2 * len(results), nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns'] for r in summaries),
        providedCalls=0, freshMachinePerExecution=True, instructionBound=1000,
        maximumNativeInstructions=max(r['instructions'] for r in summaries), completeImageEquality=True, results=summaries,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed),
            format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
        limitations=['SDK object types0/2/FFFFFFFF exercise the real34D68 type!=1 return; active type1 resource-backed path remains explicitly unsupported',
            'All native calls return through actual code; no supplied entry hook or stub is used',
            'MMIO is isolated RAM without hardware timing/display side effects; synthetic objects do not establish original resource lifecycle or scene reachability',
            'Slider naming is organizational; flags/counters/positions remain raw measured fields',
            'All registers/flags/full RAM/MMIO/private stacks/PC and writes compare; physical final R0 is the last position-setter object pointer'])
    pins = [str(SOURCE.relative_to(ROOT)), str(SOURCE.with_name('context.h').relative_to(ROOT)),
        'ov005_slider20_fixture_20261030.py', 'ov005_slider20_models_20261030.py',
        str((control / 'source.c').relative_to(ROOT)), str((control / 'context.h').relative_to(ROOT))]
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], module='ov005', processor='arm9', mode='arm',
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=[row],
        nativeSymbols={item['symbol']: item['target'] for item in row['relocations']}, isolatedLink=proof,
        nativeSourceBytes=464, functionMatches=1, acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False,
        rejectedFlagMutation=dict(expectedRejected=True, failure=failure, compilation=bad_rows, actualLinkComparison=rejected_proof, sourceCredit=0),
        unsupportedActiveSdkObject=dict(recipe=active_recipe, failure=active_limit, actualReturn=False, sourceCredit=0),
        inputPins=[dict(path=p, sha256=sha256(ROOT / p)) for p in pins], generatorSha256=sha256(Path(__file__)),
        limitations=['Final registration/module/ROM gates remain the integrator responsibility', 'createdUtc is volatile; stable identity excludes only that field',
            'No ordinary code blobs, assembly, padding, opcode changes or invented saved-register input'],
        reproductionCommand='python match_ov005_slider20_20261030.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(REPORT, report)
    print(json.dumps({key: row['oracle'][key] for key in ['executions', 'nativeDependencyActualReturns', 'providedCalls', 'maximumNativeInstructions']}), flush=True)


if __name__ == '__main__':
    run()
