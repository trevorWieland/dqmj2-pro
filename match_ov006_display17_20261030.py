import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov006_display17_fixture_20261030 import execute
from ov006_display17_models_20261030 import recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCE = ROOT / 'src/overlays/ov006_20261030_display17/display.c'
SOURCE_HASH = '25c1000301410c5a92d3e371f1d64227c96a174a21fe87a870c473d31b847c56'
HEADER_HASH = 'fcd47e23978a6ec1d5fecedbd03dca92f3d0013d7902833f643de9a2b1d2d6ff'
WORK = ROOT / 'work/ol17-proof'
REPORT = ROOT / 'evidence/matches/ov006-20261030-display17.json'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Pinned Python/Unicorn differs')
    if sha256(SOURCE) != SOURCE_HASH or sha256(SOURCE.with_name('context.h')) != HEADER_HASH:
        raise ValueError('Frozen display17 source/header differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private input differs')
    metadata, overlay, unused = measured_module('ov006')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'c'
    records, unused = compiler.compare(SOURCE, 'ov006', '2', 'off', True)
    if len(records) != 1 or records[0].get('compiledBytes') != 812 or not records[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Full812-byte display17 C span differs')
    row = records[0]
    row['sourceDependencies'] = [dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)), sha256=HEADER_HASH)]
    bindings = qualified_bindings(row)
    directory = WORK / 'l' / row['objectSha256']
    proof = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    candidate = bytearray(overlay)
    offset = 0x021DB050 - 0x021D7240
    candidate[offset:offset + 812] = linked
    if bytes(candidate) != overlay:
        raise ValueError('Full original/rebuilt display17 module image differs')
    results, summaries = [], []
    for index, recipe in enumerate(recipes()):
        original = execute(main, overlay, recipe)
        rebuilt = execute(main, bytes(candidate), recipe)
        if original != rebuilt:
            raise ValueError('Display17 original/rebuilt complete machines differ')
        results.append(dict(recipe=recipe, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)),
            actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']),
            providedCalls=2 * len(original['providedCalls']), instructions=original['instructions'],
            returnWord=original['returnWord'], ramSha256=original['ramSha256'], stackSha256=original['stackSha256'],
            pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
    old_source = ROOT / 'nonmatching/overlay-lane/20261030-sweep16/ov006/021db050-arm/source.c'
    compiler.WORK = WORK / 'rejected-scalar/c'
    old_rows, unused = compiler.compare(old_source, 'ov006', '2', 'off', True)
    if len(old_rows) != 1 or old_rows[0].get('compiledBytes') != 812:
        raise ValueError('Frozen scalar-output control profile differs')
    rejected_directory = WORK / 'rejected-scalar/l'
    try:
        rejected_proof = validate(old_rows[0], qualified_bindings(old_rows[0]), rejected_directory)
    except ValueError as error:
        rejected_proof = error.args[0]
    if not isinstance(rejected_proof, dict) or rejected_proof.get('caller') != old_rows[0]['name']:
        raise ValueError('Scalar-output control did not genuinely link')
    try:
        execute(main, overlay, recipes()[0], (rejected_directory / 'caller.bin').read_bytes())
    except ValueError as error:
        failure = error.args[0]
        if not isinstance(failure, tuple) or failure[0] != 'Display17 output buffer escapes locals':
            raise ValueError(('Scalar-output control failed unexpectedly', failure))
    else:
        raise ValueError('Scalar-output control unexpectedly passed')
    raw = encoded(dict(romSha256=config['romSha256'], module='ov006', processor='arm9', mode='arm',
        address='0x021DB050', sourceSha256=SOURCE_HASH, results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    row['oracle'] = dict(evidenceClass='original and byte-exact compiled ordinary display caller with original scalar/getter dependencies and explicit supplied formatting/display services',
        supported=True, executions=2 * len(results), actualReturns=2 * len(results),
        nativeDependencyActualReturns=sum(item['nativeDependencyActualReturns'] for item in summaries),
        providedCalls=sum(item['providedCalls'] for item in summaries), freshMachinePerExecution=True,
        instructionBound=2000, maximumNativeInstructions=max(item['instructions'] for item in summaries), completeImageEquality=True,
        results=summaries, rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed),
            bytes=len(compressed), format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
        limitations=['Display/format/cache preparation services are explicit providers with synthetic opaque16-bit text outputs',
            'Main679F0/67A30 load pointers from root021C3708+2C/+30; synthetic mapped fields are prerequisites, not observed live state',
            'Raw identifier0/1/46/47/239/240/65535 and extreme32-bit word arithmetic are isolated inputs; no valid game identifier/scene meaning is assigned',
            'Actual return/all registers/flags/RAM/private stacks/traces match; supplied callees carry zero native/source credit',
            'No resource lifecycle, original formatting/encoding, hardware, malformed pointer/error path or scene reachability claim'])
    pins = [str(SOURCE.relative_to(ROOT)), str(SOURCE.with_name('context.h').relative_to(ROOT)),
        'ov006_display17_fixture_20261030.py', 'ov006_display17_models_20261030.py',
        str(old_source.relative_to(ROOT)), str(old_source.with_name('context.h').relative_to(ROOT))]
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], module='ov006', processor='arm9', mode='arm',
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=[row],
        nativeSymbols={item['symbol']: item['target'] for item in row['relocations']}, isolatedLink=proof,
        nativeSourceBytes=812, functionMatches=1, acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False,
        originalDependencyFacts=[dict(module='main', address='0x02067A30', nativeBytes=16,
            operation='LDR root021C3708; LDR R0,[R0,30]; BX LR', returnView='byte-addressed four-row base in this caller'),
            dict(module='main', address='0x020679F0', nativeBytes=16, operation='LDR root021C3708; LDR R0,[R0,2C]; BX LR'),
            dict(module='main', address='0x020643FC', nativeBytes=48, operation='Raw identifier below47 maps0->0 and1..46->1;47..65535 map(identifier-46)&FFFF')],
        rejectedScalarBuffer=dict(expectedRejected=True, failure=failure, compilation=old_rows, actualLinkComparison=rejected_proof, sourceCredit=0),
        inputPins=[dict(path=p, sha256=sha256(ROOT / p)) for p in pins], generatorSha256=sha256(Path(__file__)),
        limitations=['Integrator acceptance/module and ROM gates remain separate; this lane never edits registration or source preference',
            'createdUtc is volatile; deterministic identity excludes only that field', 'No original blobs, assembly, opcode patches or inherited-register arguments'],
        reproductionCommand='python match_ov006_display17_20261030.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(REPORT, report)
    print(json.dumps({key: row['oracle'][key] for key in ['executions', 'nativeDependencyActualReturns', 'providedCalls', 'maximumNativeInstructions']}), flush=True)


if __name__ == '__main__':
    run()
