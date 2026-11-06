import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov000_parser169_fixture_20261031 import NATIVE, execute
from ov000_parser169_models_20261031 import recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCE = ROOT / 'src/overlays/ov000_20261031_parser169/parser.c'
PINS = ROOT / 'evidence/verification/ov000-parser169-inputs-20261031.json'
WORK = ROOT / 'work/ol169-proof'
REPORT = ROOT / 'evidence/matches/ov000-20261031-parser169.json'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Parser169 pinned Python/Unicorn differs')
    pins = json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError('Parser169 frozen source/header/fixture/model differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Parser169 measured private input differs')
    metadata, overlay, unused = measured_module('ov000')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov000', '2', 'off', True, thumb=False)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 272:
        raise ValueError('Parser169 full272-byte ordinary source compilation differs')
    row = rows[0]
    row['sourceDependencies'] = [dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)), sha256=sha256(SOURCE.with_name('context.h')))]
    bindings = qualified_bindings(row)
    directory = WORK / 'l' / row['objectSha256']
    proof = validate(row, bindings, directory)
    row['exactAfterGenuineLink'], row['linkedMatchingBytes'] = True, 272
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    candidate = bytearray(overlay)
    offset = 0x021E3C0C - 0x021D7240
    candidate[offset:offset + 272] = linked
    if bytes(candidate) != overlay:
        raise ValueError('Parser169 complete original/source overlay image differs')
    results, summaries = [], []
    for index, recipe in enumerate(recipes()):
        original, rebuilt = execute(main, overlay, recipe), execute(main, bytes(candidate), recipe)
        if original != rebuilt:
            raise ValueError('Parser169 complete original/source executions differ')
        results.append(dict(recipe=recipe, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)),
            actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']), providedCalls=2 * len(original['providedCalls']),
            instructions=original['instructions'], observedNativeCallerInstructionBytes=len(original['observedCallerInstructionBytes']),
            ramSha256=original['ramSha256'], stackSha256=original['stackSha256'],
            pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
    control = ROOT / 'nonmatching/overlay-lane/20261031-parser169-rounding-negative'
    control.mkdir(parents=True, exist_ok=True)
    body = SOURCE.read_text().replace('0.5f', '1.0f', 1)
    if body == SOURCE.read_text():
        raise ValueError('Parser169 source mutation not found')
    for path, text in [(control / 'source.c', body), (control / 'context.h', SOURCE.with_name('context.h').read_text())]:
        if path.exists() and path.read_bytes() != text.encode():
            raise ValueError('Parser169 preserve previous control source')
        path.write_bytes(text.encode())
    compiler.WORK = WORK / 'rejected-rounding/c'
    bad_rows, unused = compiler.compare(control / 'source.c', 'ov000', '2', 'off', True, thumb=False)
    if len(bad_rows) != 1 or bad_rows[0].get('compileFailed'):
        raise ValueError('Parser169 source control did not compile')
    bad_directory = WORK / 'rejected-rounding/l'
    try:
        rejected_link = validate(bad_rows[0], qualified_bindings(bad_rows[0]), bad_directory)
    except ValueError as error:
        rejected_link = error.args[0]
    if not isinstance(rejected_link, dict) or rejected_link.get('caller') != bad_rows[0]['name']:
        raise ValueError('Parser169 source control did not genuinely link')
    directed = next(r for r in recipes() if r['slot'] == 0 and r['branch'] == 1 and r['first'] == 1)
    try:
        execute(main, overlay, directed, (bad_directory / 'caller.bin').read_bytes())
    except ValueError as error:
        failure = error.args[0]
        if not isinstance(failure, tuple) or failure[0] != 'Parser169 independent numeric/native arguments differ':
            raise ValueError(('Parser169 source control rejected unexpectedly', failure))
    else:
        raise ValueError('Parser169 source control unexpectedly passed')
    raw = encoded(dict(romSha256=config['romSha256'], module='ov000', address='0x021E3C0C', results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    row['oracle'] = dict(supported=True, evidenceClass='Independent copied-record/prefix state and binary32 arithmetic with eight original native bodies',
        executions=2 * len(results), actualReturns=2 * len(results),
        nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns'] for r in summaries), providedCalls=sum(r['providedCalls'] for r in summaries),
        freshMachinePerExecution=True, instructionBound=5000, maximumNativeInstructions=max(r['instructions'] for r in summaries),
        completeImageEquality=True, observedNativeCallerInstructionBytes=len({a for r in results for a in r['result']['observedCallerInstructionBytes']}),
        nativeBodies=[dict(processor='arm9', program='', module='main' if a < 0x021D7240 else 'ov000', mode='arm',
            address=hex(a), bytes=n, sha256=compiler.sha((main if a < 0x021D7240 else overlay)[a - (0x02000000 if a < 0x021D7240 else 0x021D7240):a - (0x02000000 if a < 0x021D7240 else 0x021D7240) + n]))
            for a, n in NATIVE.items()], results=summaries,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed),
            format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
        limitations=['Synthetic 64-record pool, source words and provider-supplied parser returns; no valid scene or asset lifecycle claim',
            'Original scan/copy/strncmp, four binary32 routines and raw setter execute; all source-helper credit remains zero',
            'Numeric text parsing, rotation setter and matrix preparation are explicit providers with zero native/body/source credit',
            'Soft-float signatures are qualified on finite caller-domain values and original register-word results; no NaN/infinity ABI claim'])
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], processor='arm9', program='', module='ov000', mode='arm',
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=[row],
        nativeSymbols={item['symbol']: item['target'] for item in row['relocations']}, isolatedLink=proof,
        nativeSourceBytes=272, functionMatches=1, acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False,
        rejectedRoundingCode=dict(expectedRejected=True, recipe=directed, failure=failure, compilation=bad_rows,
            actualLinkComparison=rejected_link, sourceCredit=0), inputPins=pins['files'], generatorSha256=sha256(Path(__file__)),
        limitations=['Final registration/module/ROM gates remain the integrator responsibility', 'createdUtc is volatile; stable identity excludes only that field',
            'No executable blobs, assembly, opcode modifications, invented register inputs or dependency source credit'],
        reproductionCommand='python match_ov000_parser169_20261031.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(REPORT, report)
    contracts = {'0x2025a28': ('float', ['s32']), '0x2024e0c': ('float', ['float', 'float']),
        '0x2025ca4': ('float', ['float', 'float']), '0x20259b4': ('s32', ['float'])}
    facts = []
    for address, (result_type, arguments) in contracts.items():
        vectors = {}
        for result in results:
            actual = result['result']
            for entry, returned in zip(actual['nativeEntries'], actual['nativeDependencyActualReturns']):
                if entry['address'] == address:
                    if returned['address'] != address:
                        raise ValueError('Parser169 native scalar entry/return pairing differs')
                    key = tuple(entry['arguments']) + (returned['result'],)
                    vectors[key] = dict(arguments=entry['arguments'], returnWord=returned['result'])
        body = next(b for b in row['oracle']['nativeBodies'] if int(b['address'], 0) == int(address, 0))
        facts.append(dict(body, resultType=result_type, argumentTypes=arguments, argumentRegisters=['R0', 'R1'][:len(arguments)],
            resultRegisters=['R0'], vectors=[vectors[k] for k in sorted(vectors)], actualFramePreservationChecked=True))
    write_json(ROOT / 'evidence/verification/main-float-parser169-abi-20261031.json', dict(schemaVersion=1,
        romSha256=config['romSha256'], mainInputSha256=main_metadata['sha256'], producerSha256=sha256(Path(__file__)),
        evidenceClass='Original finite caller-domain word inputs/returns against independent binary32 rounding and signed saturation model',
        caller=dict(processor='arm9', program='', module='ov000', address='0x021E3C0C', mode='arm', bytes=272), facts=facts,
        limitations=['No NaN, infinity, signaling, denormal, error flag or exception-state coverage is asserted',
            'The add/subtract observations use one operand equal to0.5; no complete arithmetic implementation or helper source credit',
            'Types qualify new caller contexts only; accepted historical source/prototypes remain unchanged'], sourceCredit=0))
    print(json.dumps({key: row['oracle'][key] for key in ['executions', 'nativeDependencyActualReturns', 'providedCalls', 'maximumNativeInstructions']}), flush=True)


if __name__ == '__main__':
    run()
