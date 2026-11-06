import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_message198_abi_20261031 import BODIES as ABI_BODIES, run as run_native_abi
from ov001_message198_fixture_20261031 import NATIVE, execute
from ov001_message198_models_20261031 import recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCE = ROOT / 'src/overlays/ov001_20261031_message198/message.c'
PINS = ROOT / 'evidence/verification/ov001-message198-inputs-20261031.json'
WORK = ROOT / 'work/ol198-proof'
REPORT = ROOT / 'evidence/matches/ov001-20261031-message198.json'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Message198 pinned Python/Unicorn differs')
    pins = json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError('Message198 frozen source/header/fixture/model differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Message198 measured private input differs')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True, thumb=False)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 212:
        raise ValueError('Message198 full212-byte ordinary source compilation differs')
    row = rows[0]
    row['sourceDependencies'] = [dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)), sha256=sha256(SOURCE.with_name('context.h')))]
    bindings = qualified_bindings(row)
    directory = WORK / 'l' / row['objectSha256']
    proof = validate(row, bindings, directory)
    row['exactAfterGenuineLink'], row['linkedMatchingBytes'] = True, 212
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    candidate = bytearray(overlay)
    offset = 0x021D7E80 - 0x021D7240
    candidate[offset:offset + 212] = linked
    if bytes(candidate) != overlay:
        raise ValueError('Message198 complete original/source overlay image differs')
    results, summaries = [], []
    for index, recipe in enumerate(recipes()):
        original, rebuilt = execute(main, overlay, recipe), execute(main, bytes(candidate), recipe)
        if original != rebuilt:
            raise ValueError('Message198 complete original/source executions differ')
        results.append(dict(recipe=recipe, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)),
            actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']), providedCalls=2 * len(original['providedCalls']),
            instructions=original['instructions'], observedNativeCallerInstructionBytes=len(original['observedCallerInstructionBytes']),
            ramSha256=original['ramSha256'], stackSha256=original['stackSha256'],
            pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
    control = ROOT / 'nonmatching/overlay-lane/20261031-message198-identifier-negative'
    control.mkdir(parents=True, exist_ok=True)
    body = SOURCE.read_text().replace('0x12)', '0x13)', 1)
    if body == SOURCE.read_text():
        raise ValueError('Message198 source mutation not found')
    for path, text in [(control / 'source.c', body), (control / 'context.h', SOURCE.with_name('context.h').read_text())]:
        if path.exists() and path.read_bytes() != text.encode():
            raise ValueError('Message198 preserve previous control source')
        path.write_bytes(text.encode())
    compiler.WORK = WORK / 'rejected-identifier/c'
    bad_rows, unused = compiler.compare(control / 'source.c', 'ov001', '2', 'off', True, thumb=False)
    if len(bad_rows) != 1 or bad_rows[0].get('compileFailed'):
        raise ValueError('Message198 source control did not compile')
    bad_directory = WORK / 'rejected-identifier/l'
    try:
        rejected_link = validate(bad_rows[0], qualified_bindings(bad_rows[0]), bad_directory)
    except ValueError as error:
        rejected_link = error.args[0]
    if not isinstance(rejected_link, dict) or rejected_link.get('caller') != bad_rows[0]['name']:
        raise ValueError('Message198 source control did not genuinely link')
    directed = next(r for r in recipes() if r['family'] == 1 and r['early'] == 0)
    try:
        execute(main, overlay, directed, (bad_directory / 'caller.bin').read_bytes())
    except ValueError as error:
        failure = error.args[0]
        if not isinstance(failure, tuple) or failure[0] != 'Message198 independent lookup/late-byte arguments differ':
            raise ValueError(('Message198 source control rejected unexpectedly', failure))
    else:
        raise ValueError('Message198 source control unexpectedly passed')
    raw = encoded(dict(romSha256=config['romSha256'], module='ov001', address='0x021D7E80', results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    row['oracle'] = dict(supported=True, evidenceClass='Independent opaque selector/lookup state with actual actor descriptor/getter bodies',
        executions=2 * len(results), actualReturns=2 * len(results),
        nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns'] for r in summaries), providedCalls=sum(r['providedCalls'] for r in summaries),
        freshMachinePerExecution=True, instructionBound=2000, maximumNativeInstructions=max(r['instructions'] for r in summaries),
        completeImageEquality=True, observedNativeCallerInstructionBytes=len({a for r in results for a in r['result']['observedCallerInstructionBytes']}),
        nativeBodies=[dict(processor='arm9', program='', module='main' if a < 0x021D7240 else 'ov001', mode='arm',
            address=hex(a), bytes=n, sha256=compiler.sha((main if a < 0x021D7240 else overlay)[a - (0x02000000 if a < 0x021D7240 else 0x021D7240):a - (0x02000000 if a < 0x021D7240 else 0x021D7240) + n]))
            for a, n in NATIVE.items()], results=summaries,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed),
            format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
        limitations=['Synthetic accessible actor and two descriptor pointers; raw signed16 descriptor field2A has no semantic ID label',
            'Four actual native actor/descriptor/getter bodies execute; lookup/table and four presentation calls remain providers',
            'Actor31E is measured as a raw byte with fresh zero/one tests; no side meaning or valid battle/UI scene is inferred',
            'The DB9E0 input pointer is explicit; physical full-word lookup and final returns do not establish original semantic return types',
            'Null/broken descriptor pointers, original table/provider bodies and persistent/transient ownership remain unsupported'])
    lookup_closure = run_native_abi(main, overlay)
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], processor='arm9', program='', module='ov001', mode='arm',
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=[row],
        nativeSymbols={item['symbol']: item['target'] for item in row['relocations']}, isolatedLink=proof,
        nativeSourceBytes=212, functionMatches=1, acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False,
        separateOriginalLookupClosure=lookup_closure,
        rejectedIdentifierCode=dict(expectedRejected=True, recipe=directed, failure=failure, compilation=bad_rows,
            actualLinkComparison=rejected_link, sourceCredit=0), inputPins=pins['files'], generatorSha256=sha256(Path(__file__)),
        limitations=['Final registration/module/ROM gates remain the integrator responsibility', 'createdUtc is volatile; stable identity excludes only that field',
            'No executable blobs, assembly, opcode modifications, invented register inputs or dependency source credit'],
        reproductionCommand='python match_ov001_message198_20261031.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(REPORT, report)
    body = next(b for b in row['oracle']['nativeBodies'] if int(b['address'], 0) == 0x021DB9E0)
    returned = sorted({n['result'] for result in results for n in result['result']['nativeDependencyActualReturns']
        if int(n['address'], 0) == 0x021DB9E0})
    write_json(ROOT / 'evidence/verification/ov001-db9e0-message198-abi-20261031.json', dict(schemaVersion=1,
        romSha256=config['romSha256'], moduleInputSha256=metadata['sha256'], body=body,
        caller=dict(address='0x021D7E80', bytes=212, mode='arm', module='ov001', processor='arm9', program=''),
        inputRegisters=['R0'], inputRepresentation='Nonzero actor pointer; readable pointer at+1E8 and signed16 descriptor field+2A',
        contextPrototype='extern u32 func_ov001_021db9e0(void *);', originalTailTarget='0x02044CDC',
        measuredRawReturnWords=returned, actualNativeBodyReturns=2 * len(results),
        originalLookupClosure=dict(actualTopReturns=lookup_closure['actualTopReturns'], actualOriginalSdkReturns=lookup_closure['actualOriginalSdkReturns'],
            providers=0, supportedIndices=lookup_closure['supportedIndices'], sourceCredit=0,
            bodyInputs=[dict(module='main' if a < 0x021D7240 else 'ov001', address=hex(a), mode='arm', bytes=n,
                sha256=compiler.sha((main if a < 0x021D7240 else overlay)[a - (0x02000000 if a < 0x021D7240 else 0x021D7240):a - (0x02000000 if a < 0x021D7240 else 0x021D7240) + n]))
                for a, n in ABI_BODIES.items()], limitations=lookup_closure['limitations']),
        fixtureSha256=sha256(ROOT / 'ov001_message198_fixture_20261031.py'), modelSha256=sha256(ROOT / 'ov001_message198_models_20261031.py'),
        generatorSha256=sha256(Path(__file__)), sourceCredit=0,
        limitations=['Wide lookup-word caller cases use explicit providers; separate valid-index original table-chain cases establish downstream R0-only behavior',
            'Pointer input follows actual native loads and caller R0; raw u32 is a word ABI view only',
            'New unmatched primary ov001 contexts only; accepted historical source and declarations remain unchanged']))
    print(json.dumps({key: row['oracle'][key] for key in ['executions', 'nativeDependencyActualReturns', 'providedCalls', 'maximumNativeInstructions']}), flush=True)


if __name__ == '__main__':
    run()
