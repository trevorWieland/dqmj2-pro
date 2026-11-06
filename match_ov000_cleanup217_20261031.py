import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov000_cleanup217_fixture_20261031 import NATIVE, execute
from ov000_cleanup217_models_20261031 import recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCE = ROOT / 'src/overlays/ov000_20261031_cleanup217/cleanup.c'
PINS = ROOT / 'evidence/verification/ov000-cleanup217-inputs-20261031.json'
WORK = ROOT / 'work/ol217-proof'
REPORT = ROOT / 'evidence/matches/ov000-20261031-cleanup217.json'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Cleanup217 pinned Python/Unicorn differs')
    pins = json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError('Cleanup217 frozen source/header/fixture/model differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Cleanup217 measured private input differs')
    metadata, overlay, unused = measured_module('ov000')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov000', '2', 'off', True, thumb=False)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 232:
        raise ValueError('Cleanup217 full232-byte ordinary source compilation differs')
    row = rows[0]
    row['sourceDependencies'] = [dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)), sha256=sha256(SOURCE.with_name('context.h')))]
    bindings = qualified_bindings(row)
    directory = WORK / 'l' / row['objectSha256']
    proof = validate(row, bindings, directory)
    row['exactAfterGenuineLink'], row['linkedMatchingBytes'] = True, 232
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    candidate = bytearray(overlay)
    offset = 0x021EB060 - 0x021D7240
    candidate[offset:offset + 232] = linked
    if bytes(candidate) != overlay:
        raise ValueError('Cleanup217 complete original/source overlay image differs')
    results, summaries = [], []
    for index, recipe in enumerate(recipes()):
        original, rebuilt = execute(main, overlay, recipe), execute(main, bytes(candidate), recipe)
        if original != rebuilt:
            raise ValueError('Cleanup217 complete original/source executions differ')
        results.append(dict(recipe=recipe, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)),
            actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']), providedCalls=2 * len(original['providedCalls']),
            instructions=original['instructions'], observedNativeCallerInstructionBytes=len(original['observedCallerInstructionBytes']),
            ramSha256=original['ramSha256'], stackSha256=original['stackSha256'],
            pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
    control = ROOT / 'nonmatching/overlay-lane/20261031-cleanup217-allocator-negative'
    control.mkdir(parents=True, exist_ok=True)
    body = SOURCE.read_text().replace('native_fn_0202a164(2)', 'native_fn_0202a164(3)')
    if body == SOURCE.read_text():
        raise ValueError('Cleanup217 source mutation not found')
    for path, text in [(control / 'source.c', body), (control / 'context.h', SOURCE.with_name('context.h').read_text())]:
        if path.exists() and path.read_bytes() != text.encode():
            raise ValueError('Cleanup217 preserve previous control source')
        path.write_bytes(text.encode())
    compiler.WORK = WORK / 'rejected-saved-field/c'
    bad_rows, unused = compiler.compare(control / 'source.c', 'ov000', '2', 'off', True, thumb=False)
    if len(bad_rows) != 1 or bad_rows[0].get('compileFailed'):
        raise ValueError('Cleanup217 source control did not compile')
    bad_directory = WORK / 'rejected-saved-field/l'
    try:
        rejected_link = validate(bad_rows[0], qualified_bindings(bad_rows[0]), bad_directory)
    except ValueError as error:
        rejected_link = error.args[0]
    if not isinstance(rejected_link, dict) or rejected_link.get('caller') != bad_rows[0]['name']:
        raise ValueError('Cleanup217 source control did not genuinely link')
    directed = recipes()[0]
    try:
        execute(main, overlay, directed, (bad_directory / 'caller.bin').read_bytes())
    except ValueError as error:
        failure = error.args[0]
        if not isinstance(failure, tuple) or failure[0] != 'Cleanup217 independent saved-word argument differs':
            raise ValueError(('Cleanup217 source control rejected unexpectedly', failure))
    else:
        raise ValueError('Cleanup217 source control unexpectedly passed')
    raw = encoded(dict(romSha256=config['romSha256'], module='ov000', address='0x021EB060', results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    row['oracle'] = dict(supported=True, evidenceClass='Independent cleanup call order, late context word reloads and raw context return with one original empty ARM body',
        executions=2 * len(results), actualReturns=2 * len(results),
        nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns'] for r in summaries), providedCalls=sum(r['providedCalls'] for r in summaries),
        freshMachinePerExecution=True, instructionBound=1000, maximumNativeInstructions=max(r['instructions'] for r in summaries),
        completeImageEquality=True, observedNativeCallerInstructionBytes=len({a for r in results for a in r['result']['observedCallerInstructionBytes']}),
        nativeBodies=[dict(processor='arm9', program='', module='main' if a < 0x021D7240 else 'ov000', mode='arm',
            address=hex(a), bytes=n, sha256=compiler.sha((main if a < 0x021D7240 else overlay)[a - (0x02000000 if a < 0x021D7240 else 0x021D7240):a - (0x02000000 if a < 0x021D7240 else 0x021D7240) + n]))
            for a, n in NATIVE.items()], results=summaries,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed),
            format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
        limitations=['18 actual game cleanup/allocator bodies remain explicit providers, zero dependency source credit',
            'Original main02084920/4 BX LR executes and returns; it consumes no incoming arguments',
            'Main02061898 is a provided 2x2 cleanup loop, not a simple getter; its supplied raw R0 is not assigned semantic meaning',
            'No live object lifetime, allocator correctness or valid scene teardown claim'])
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], processor='arm9', program='', module='ov000', mode='arm',
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=[row],
        nativeSymbols={item['symbol']: item['target'] for item in row['relocations']}, isolatedLink=proof,
        nativeSourceBytes=232, functionMatches=1, acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False,
        rejectedSavedFieldCode=dict(expectedRejected=True, recipe=directed, failure=failure, compilation=bad_rows,
            actualLinkComparison=rejected_link, sourceCredit=0), inputPins=pins['files'], generatorSha256=sha256(Path(__file__)),
        limitations=['Final registration/module/ROM gates remain the integrator responsibility', 'createdUtc is volatile; stable identity excludes only that field',
            'No executable blobs, assembly, opcode modifications, invented register inputs or dependency source credit'],
        reproductionCommand='python match_ov000_cleanup217_20261031.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(REPORT, report)
    print(json.dumps({key: row['oracle'][key] for key in ['executions', 'nativeDependencyActualReturns', 'providedCalls', 'maximumNativeInstructions']}), flush=True)


if __name__ == '__main__':
    run()
