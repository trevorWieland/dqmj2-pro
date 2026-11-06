import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov006_protocol148_fixture_20261031 import execute, NATIVE
from ov006_protocol148_models_20261031 import recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCE = ROOT / 'src/overlays/ov006_20261031_protocol148/protocol.c'
SOURCE_HASH, HEADER_HASH = 'fdbbb487c4733646c069926637eeb8063dae74177fd0cd41cad2c31f975f4da6', '082fd2df329d18ef49106f61ae211ba309d4066e59efcee970b097ba323e928d'
WORK = ROOT / 'work/ol148-proof'
REPORT = ROOT / 'evidence/matches/ov006-20261031-protocol148.json'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Pinned Python/Unicorn differs')
    if sha256(SOURCE) != SOURCE_HASH or sha256(SOURCE.with_name('context.h')) != HEADER_HASH:
        raise ValueError('Frozen protocol148 source/header differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private input differs')
    metadata, overlay, unused = measured_module('ov006')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov006', '2', 'off', True, thumb=True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 144:
        raise ValueError('Full144-byte ordinary fixed-call source differs')
    row = rows[0]
    row['sourceDependencies'] = [dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)), sha256=HEADER_HASH)]
    bindings = qualified_bindings(row)
    directory = WORK / 'l' / row['objectSha256']
    proof = validate(row, bindings, directory)
    row['exactAfterGenuineLink'] = True
    row['linkedMatchingBytes'] = 144
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    candidate = bytearray(overlay)
    offset = 0x0220192C - 0x021D7240
    candidate[offset:offset + 144] = linked
    if bytes(candidate) != overlay:
        raise ValueError('Full original/source protocol148 module image differs')
    results, summaries = [], []
    for index, recipe in enumerate(recipes()):
        original, rebuilt = execute(main, overlay, recipe), execute(main, bytes(candidate), recipe)
        if original != rebuilt:
            raise ValueError('Protocol148 original/source complete machines differ')
        results.append(dict(recipe=recipe, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)),
            actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']),
            providedCalls=2 * len(original['providedCalls']), instructions=original['instructions'],
            observedNativeCallerInstructionBytes=len(original['observedCallerInstructionBytes']), ramSha256=original['ramSha256'],
            stackSha256=original['stackSha256'], pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
    control = ROOT / 'nonmatching/overlay-lane/20261031-protocol148-inner-negative'
    control.mkdir(parents=True, exist_ok=True)
    before = 'return native_fn_ov006_02201270(9);'
    body = SOURCE.read_text().replace(before, 'return native_fn_ov006_02201270(8);', 1)
    if body == SOURCE.read_text():
        raise ValueError('Locate actual ready-state mutation')
    for path, text in [(control / 'source.c', body), (control / 'context.h', SOURCE.with_name('context.h').read_text())]:
        if path.exists() and path.read_bytes() != text.encode():
            raise ValueError('Preserve prior state control source')
        path.write_bytes(text.encode())
    compiler.WORK = WORK / 'rejected-state/c'
    bad_rows, unused = compiler.compare(control / 'source.c', 'ov006', '2', 'off', True, thumb=True)
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
        if (failure if isinstance(failure, str) else failure[0]) != 'Protocol148 independent arguments differ':
            raise ValueError(('State control rejected unexpectedly', failure))
    else:
        raise ValueError('State source control unexpectedly passed')
    failure = json.loads(json.dumps(failure, default=lambda value: dict(bytesHex=value.hex()) if isinstance(value, bytes) else str(value)))
    raw = encoded(dict(romSha256=config['romSha256'], module='ov006', address='0x0220192C', results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    row['oracle'] = dict(supported=True, evidenceClass='Original Thumb halfword/header caller with actual error/state/bitmap selector helpers and mode-checked explicit callback/provider models',
        executions=2 * len(results), actualReturns=2 * len(results), nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns'] for r in summaries),
        providedCalls=sum(r['providedCalls'] for r in summaries), freshMachinePerExecution=True, instructionBound=5000,
        maximumNativeInstructions=max(r['instructions'] for r in summaries), completeImageEquality=True,
        observedNativeCallerInstructionBytes=len({address for result in results for address in result['result']['observedCallerInstructionBytes']}), results=summaries,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed),
            format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
        nativeScopes=[dict(module='ov006', processor='arm9', program='', mode='thumb', address=hex(address), instructionBytes=size,
            nativeCodeSha256=compiler.sha(overlay[address - 0x021D7240:address - 0x021D7240 + size]), sourceCredit=0) for address, size in NATIVE.items()],
        limitations=['Original12C0 reads the caller header halfword inR0; explicit C argument repairs a byte-exact but implicit-register m2c omission, without changing accepted source',
            'Unsigned1U defines the caller shift for supported sequence1..32; sequence0 or wider successful headers are unsupported',
            'Native error/state/selector helpers really execute; main12290 bitmap and19BC request registration remain supplied providers with zero native/source credit',
            'Synthetic ARM/Thumb outer callbacks mutate later halfwords/pointers and disable callbacks before native state setting; inner state-callback paths remain unsupported',
            'Actual selector forwards tagged self callback0220192D and selected sequence; callback body, hardware/resource protocol, ownership and reachability are unclaimed'])
    paths = [str(SOURCE.relative_to(ROOT)), str(SOURCE.with_name('context.h').relative_to(ROOT)),
        'ov006_protocol148_fixture_20261031.py', 'ov006_protocol148_models_20261031.py', 'config/arm9/symbols.txt', 'config/arm9/overlays/ov006/symbols.txt', 'ov001_ability28_fixture_20261031.py',
        str((control / 'source.c').relative_to(ROOT)), str((control / 'context.h').relative_to(ROOT))]
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], processor='arm9', program='', module='ov006', mode='thumb',
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=[row],
        nativeSymbols={item['symbol']: item['target'] for item in row['relocations']}, isolatedLink=proof,
        nativeSourceBytes=144, functionMatches=1, acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False,
        rejectedBranchCode=dict(expectedRejected=True, failure=failure, compilation=bad_rows, actualLinkComparison=rejected_link, sourceCredit=0),
        inputPins=[dict(path=p, sha256=sha256(ROOT / p)) for p in paths], generatorSha256=sha256(Path(__file__)),
        limitations=['Final registration/module/ROM gates remain the integrator responsibility', 'createdUtc is volatile; stable identity excludes only that field',
            'No executable blobs, assembly, opcode modifications, fake register inputs or dependency source credit'],
        reproductionCommand='python match_ov006_protocol148_20261031.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(REPORT, report)
    print(json.dumps({key: row['oracle'][key] for key in ['executions', 'nativeDependencyActualReturns', 'providedCalls', 'maximumNativeInstructions']}), flush=True)


if __name__ == '__main__':
    run()
