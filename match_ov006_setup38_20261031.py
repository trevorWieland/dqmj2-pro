import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov006_setup38_fixture_20261031 import execute, recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCE = ROOT / 'src/overlays/ov006_20261031_setup38/setup.c'
SOURCE_HASH = '14cec743567d4f36eb95e2eacc6723b8774d48c5c2f69d97bcc09f13bd19a028'
HEADER_HASH = 'b6de88605ae3d7496dbfa4f4a91991ecf99db13772cec115576cc6c3056c4a88'
WORK = ROOT / 'work/ol38-proof'
REPORT = ROOT / 'evidence/matches/ov006-20261031-setup38.json'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Pinned Python/Unicorn differs')
    if sha256(SOURCE) != SOURCE_HASH or sha256(SOURCE.with_name('context.h')) != HEADER_HASH:
        raise ValueError('Frozen setup38 source/header differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private input differs')
    metadata, overlay, unused = measured_module('ov006')
    main_metadata, main, unused = measured_module('main')
    itcm_metadata, unused, unused = measured_module('itcm')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov006', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 372 or not rows[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Full372-byte ordinary setup C differs')
    row = rows[0]
    row['sourceDependencies'] = [dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)), sha256=HEADER_HASH)]
    bindings = qualified_bindings(row)
    directory = WORK / 'l' / row['objectSha256']
    proof = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    rebuilt = bytearray(overlay)
    rebuilt[0x021D7860 - 0x021D7240:0x021D7860 - 0x021D7240 + 372] = linked
    if bytes(rebuilt) != overlay:
        raise ValueError('Full original/source setup38 image differs')
    results, summaries = [], []
    for index, recipe in enumerate(recipes()):
        original, candidate = execute(main, overlay, recipe), execute(main, bytes(rebuilt), recipe)
        if original != candidate:
            raise ValueError('Setup38 original/source complete execution evidence differs')
        results.append(dict(recipe=recipe, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)),
            actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']),
            providedCalls=2 * len(original['providedCalls']), instructions=original['instructions'], returnWord=original['returnWord'],
            pcTraceSha256=original['pcTraceSha256'], writeTraceSha256=original['writeTraceSha256'],
            ramSha256=original['ramSha256'], ioSha256=original['ioSha256'], paletteSha256=original['paletteSha256'],
            vramSha256=original['vramSha256'], stackSha256=original['stackSha256']))
    control = ROOT / 'nonmatching/overlay-lane/20261031-setup38-negative'
    control.mkdir(parents=True, exist_ok=True)
    body = SOURCE.read_text().replace('char path[32];', 'char path[4];')
    if body == SOURCE.read_text():
        raise ValueError('Locate actual narrow-path mutation')
    for path, text in [(control / 'source.c', body), (control / 'context.h', SOURCE.with_name('context.h').read_text())]:
        if path.exists() and path.read_bytes() != text.encode():
            raise ValueError('Preserve prior narrow filename control')
        path.write_bytes(text.encode())
    compiler.WORK = WORK / 'rejected-path/c'
    bad_rows, unused = compiler.compare(control / 'source.c', 'ov006', '2', 'off', True)
    if len(bad_rows) != 1 or bad_rows[0].get('compileFailed'):
        raise ValueError('Narrow filename source control failed compilation')
    rejected_directory = WORK / 'rejected-path/l'
    try:
        rejected_proof = validate(bad_rows[0], qualified_bindings(bad_rows[0]), rejected_directory)
    except ValueError as error:
        rejected_proof = error.args[0]
    if not isinstance(rejected_proof, dict) or rejected_proof.get('caller') != bad_rows[0]['name']:
        raise ValueError('Narrow filename source did not genuinely link')
    try:
        execute(main, overlay, recipes()[0], (rejected_directory / 'caller.bin').read_bytes())
    except ValueError as error:
        failure = dict(failure=error.args[0], cause=str(error.__cause__))
        if str(error.__cause__) != 'Setup38 filename buffer escapes caller locals':
            raise ValueError(('Narrow path control failed unexpectedly', failure))
    else:
        raise ValueError('Narrow filename source control unexpectedly passed')
    dma_recipe = dict(recipes()[0], dmaSelector=3)
    try:
        execute(main, overlay, dma_recipe)
    except ValueError as error:
        dma_failure = dict(failure=error.args[0], cause=str(error.__cause__))
        if str(error.__cause__) != 'Setup38 instruction bound exceeded':
            raise ValueError(('Native DMA boundary failed unexpectedly', dma_failure))
    else:
        raise ValueError('RAM-backed DMA profile unexpectedly completed')
    raw = encoded(dict(romSha256=config['romSha256'], module='ov006', address='0x021D7860', results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    row['oracle'] = dict(supported=True, evidenceClass='native setup/video-mode/clear/format/palette-copy execution with independent complete RAM/VRAM/palette/MMIO models and explicit zero-length file providers',
        executions=2 * len(results), actualReturns=2 * len(results), nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns'] for r in summaries),
        providedCalls=sum(r['providedCalls'] for r in summaries), freshMachinePerExecution=True, instructionBound=100000,
        maximumNativeInstructions=max(r['instructions'] for r in summaries), completeImageEquality=True, results=summaries,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed),
            format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
        limitations=['Synthetic 020DCB44=FFFFFFFF selects the existing native CPU-copy path; default3 DMA waits without hardware completion and remains unsupported',
            'Two file-length services return0; positive-length allocation/resource upload/free paths and actual filesystem execution remain unsupported',
            'Native sprintf executes for unchanged static no-percent filename formats; char32 is a sufficient frame-consistent buffer, not a uniquely recovered historical extent',
            'MMIO/VRAM/palette are isolated RAM; no hardware timing/display, emulator, audible output or live-resource lifecycle claim',
            'Physical final R0 is compared and checked to propagate actual final uploader R0; no semantic return interpretation',
            'Original/source compare all final registers/flags/full RAM/ITCM/VRAM/palette/MMIO/private stacks and deterministic PC/write hashes'])
    paths = [str(SOURCE.relative_to(ROOT)), str(SOURCE.with_name('context.h').relative_to(ROOT)), 'ov006_setup38_fixture_20261031.py',
        'ov001_ability28_fixture_20261031.py', str((control / 'source.c').relative_to(ROOT)), str((control / 'context.h').relative_to(ROOT))]
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], module='ov006', processor='arm9', mode='arm',
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'], matches=[row],
        nativeSymbols={item['symbol']: item['target'] for item in row['relocations']}, isolatedLink=proof,
        nativeSourceBytes=372, functionMatches=1, acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False,
        rejectedNarrowFilename=dict(expectedRejected=True, actualReturn=False, evidence=failure, compilation=bad_rows, actualLinkComparison=rejected_proof, sourceCredit=0),
        unsupportedNativeDma=dict(recipe=dma_recipe, actualReturn=False, evidence=dma_failure, sourceCredit=0),
        inputPins=[dict(path=p, sha256=sha256(ROOT / p)) for p in paths], generatorSha256=sha256(Path(__file__)),
        limitations=['Final registration/module/ROM gates remain the integrator responsibility', 'createdUtc is volatile; stable identity excludes only that field',
            'No executable blobs, assembly, stack padding, opcode modifications, fabricated register inputs or dependency source credit'],
        reproductionCommand='python match_ov006_setup38_20261031.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(REPORT, report)
    print(json.dumps({key: row['oracle'][key] for key in ['executions', 'nativeDependencyActualReturns', 'providedCalls', 'maximumNativeInstructions']}), flush=True)


if __name__ == '__main__':
    run()
