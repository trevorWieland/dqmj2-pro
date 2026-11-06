import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov006_menu33_fixture_20261031 import execute, functions
from ov006_menu33_models_20261031 import recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCE = ROOT / 'src/overlays/ov006_20261031_menu33/menu.c'
WORK = ROOT / 'work/ol33-proof'
REPORT = ROOT / 'evidence/matches/ov006-20261031-menu33.json'
SOURCE_HASH = '0a21a1d9c5fa433b7a64f9f6ce8a6cf7ddf963a80adeb73106c8e34a1a9606d0'
HEADER_HASH = 'ff1b0d0196c5c77dad1df250c2bab748cbd27d62cb2477e0ed20a50e58e9aebd'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Pinned Python/Unicorn differs')
    if sha256(SOURCE) != SOURCE_HASH or sha256(SOURCE.with_name('context.h')) != HEADER_HASH:
        raise ValueError('Frozen menu33 source/header differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private input differs')
    metadata, overlay, unused = measured_module('ov006')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov006', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 2728 or not rows[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Full2728-byte ordinary menu C differs')
    row = rows[0]
    row['sourceDependencies'] = [dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)), sha256=HEADER_HASH)]
    bindings = qualified_bindings(row)
    directory = WORK / 'l' / row['objectSha256']
    proof = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    candidate = bytearray(overlay)
    offset = 0x021E3064 - 0x021D7240
    candidate[offset:offset + 2728] = linked
    if bytes(candidate) != overlay:
        raise ValueError('Full original/rebuilt menu33 module image differs')
    results, summaries = [], []
    for index, recipe in enumerate(recipes()):
        original, rebuilt = execute(main, overlay, recipe), execute(main, bytes(candidate), recipe)
        if original != rebuilt:
            raise ValueError('Menu33 original/rebuilt complete machines differ')
        results.append(dict(recipe=recipe, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)),
            actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']),
            providedCalls=2 * len(original['providedCalls']), instructions=original['instructions'], returnWord=original['returnWord'],
            ramSha256=original['ramSha256'], stackSha256=original['stackSha256'],
            pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
    control = ROOT / 'nonmatching/overlay-lane/20261031-menu33-negative'
    control.mkdir(parents=True, exist_ok=True)
    body = SOURCE.read_text().replace('*(u32 *)(native_data_ov006_02217bf0 + ', '*(u8 *)(native_data_ov006_02217bf0 + ')
    if body == SOURCE.read_text():
        raise ValueError('Locate actual wrong-word-width mutation')
    for path, content in [(control / 'source.c', body), (control / 'context.h', SOURCE.with_name('context.h').read_text())]:
        if path.exists() and path.read_bytes() != content.encode():
            raise ValueError('Preserve prior wrong-width source control')
        path.write_bytes(content.encode())
    compiler.WORK = WORK / 'rejected-width/c'
    bad_rows, unused = compiler.compare(control / 'source.c', 'ov006', '2', 'off', True)
    if len(bad_rows) != 1 or bad_rows[0].get('compileFailed'):
        raise ValueError('Width mutation control failed compilation')
    rejected_directory = WORK / 'rejected-width/l'
    try:
        rejected_proof = validate(bad_rows[0], qualified_bindings(bad_rows[0]), rejected_directory)
    except ValueError as error:
        rejected_proof = error.args[0]
    if not isinstance(rejected_proof, dict) or rejected_proof.get('caller') != bad_rows[0]['name']:
        raise ValueError('Wrong-width control did not genuinely link')
    try:
        execute(main, overlay, next(r for r in recipes() if r['state'] == 5 and r['keys'] == 1),
            (rejected_directory / 'caller.bin').read_bytes())
    except ValueError as error:
        failure = error.args[0]
        if not isinstance(failure, tuple) or failure[0] != 'Menu33 argument words differ' or failure[1] != '0x2067d54':
            raise ValueError(('Wrong-width control failed unexpectedly', failure))
    else:
        raise ValueError('Wrong-width source control unexpectedly passed')
    raw = encoded(dict(romSha256=config['romSha256'], module='ov006', processor='arm9', mode='arm',
        address='0x021E3064', sourceSha256=SOURCE_HASH, results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    row['oracle'] = dict(supported=True, evidenceClass='native dispatch/getters/key and raw-state tail thunks/state setter/classifier with independent protocol/whole RAM models and explicit UI providers',
        executions=2 * len(results), actualReturns=2 * len(results), nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns'] for r in summaries),
        providedCalls=sum(r['providedCalls'] for r in summaries), freshMachinePerExecution=True, instructionBound=2000,
        maximumNativeInstructions=max(r['instructions'] for r in summaries), completeImageEquality=True, results=summaries,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed),
            format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
        limitations=['All selectors0..24 exercise the inactive dispatch; selected active data paths5/9/11 and countdown24 are modeled',
            'Other active UI paths remain explicitly unsupported; no whole-menu/scene reachability or resource-lifecycle claim',
            'Providers supply exact raw return words and no memory effects; they receive no native execution/source credit',
            'Synthetic BSS word-table entries qualify physical full-word forwarding, not valid resource IDs; original ten-halfword table stays unchanged',
            'Native classifier covers all unsigned interval boundaries and raw state remains a byte compared to1',
            'Countdown avoids signed minimum overflow; numeric sums remain in modest signed ranges',
            'All registers/flags/full RAM/private stacks/PC and writes compare, with actual top and nested tail-chain returns required'])
    pins = [str(SOURCE.relative_to(ROOT)), str(SOURCE.with_name('context.h').relative_to(ROOT)), 'ov006_menu33_fixture_20261031.py',
        'ov006_menu33_models_20261031.py', 'ov001_ability28_fixture_20261031.py',
        str((control / 'source.c').relative_to(ROOT)), str((control / 'context.h').relative_to(ROOT))]
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], module='ov006', processor='arm9', mode='arm',
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=[row],
        nativeSymbols={item['symbol']: item['target'] for item in row['relocations']}, isolatedLink=proof,
        nativeSourceBytes=2728, functionMatches=1, acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False,
        qualifiedNativeDependencies=list(functions().values()), rejectedWordWidthMutation=dict(expectedRejected=True, failure=failure,
            compilation=bad_rows, actualLinkComparison=rejected_proof, sourceCredit=0),
        inputPins=[dict(path=p, sha256=sha256(ROOT / p)) for p in pins], generatorSha256=sha256(Path(__file__)),
        limitations=['Final registration/module/ROM gates remain the integrator responsibility', 'createdUtc is volatile; stable identity excludes only that field',
            'No ordinary code blobs, assembly, stack padding, opcode modifications or fabricated inherited-register inputs'],
        reproductionCommand='python match_ov006_menu33_20261031.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(REPORT, report)
    print(json.dumps({key: row['oracle'][key] for key in ['executions', 'nativeDependencyActualReturns', 'providedCalls', 'maximumNativeInstructions']}), flush=True)


if __name__ == '__main__':
    run()
