import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov005_initializer47_fixture_20261031 import execute
from ov005_initializer47_models_20261031 import recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCE = ROOT / 'src/overlays/ov005_20261031_initializer47/initializer.c'
SOURCE_HASH, HEADER_HASH = 'f48a416a8f60d5889259f60a55f7e890a3cfabe863b1f7ef8038b338feadec37', '472932bfe6e5fc1ac3773765f1e0a875370b5cec953e0f4f84d3d5f37cf7ff54'
WORK = ROOT / 'work/ol47-proof'
REPORT = ROOT / 'evidence/matches/ov005-20261031-initializer47.json'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Pinned Python/Unicorn differs')
    if sha256(SOURCE) != SOURCE_HASH or sha256(SOURCE.with_name('context.h')) != HEADER_HASH:
        raise ValueError('Frozen initializer47 source/header differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private input differs')
    metadata, overlay, unused = measured_module('ov005')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov005', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 276 or not rows[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Full276-byte ordinary initializer C differs')
    row = rows[0]
    row['sourceDependencies'] = [dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)), sha256=HEADER_HASH)]
    bindings = qualified_bindings(row)
    directory = WORK / 'l' / row['objectSha256']
    proof = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    candidate = bytearray(overlay)
    offset = 0x021D8EDC - 0x021D7240
    candidate[offset:offset + 276] = linked
    if bytes(candidate) != overlay:
        raise ValueError('Full original/source initializer47 module image differs')
    results, summaries = [], []
    for index, recipe in enumerate(recipes()):
        original, rebuilt = execute(main, overlay, recipe), execute(main, bytes(candidate), recipe)
        if original != rebuilt:
            raise ValueError('Initializer47 original/source complete machines differ')
        results.append(dict(recipe=recipe, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)),
            actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']),
            providedCalls=2 * len(original['providedCalls']), instructions=original['instructions'],
            observedNativeCallerInstructionBytes=original['observedNativeCallerInstructionBytes'], ramSha256=original['ramSha256'],
            stackSha256=original['stackSha256'], pcTraceSha256=original['pcTraceSha256'], writeTraceSha256=original['writeTraceSha256']))
    control = ROOT / 'nonmatching/overlay-lane/20261031-initializer47-negative'
    control.mkdir(parents=True, exist_ok=True)
    before = 'native_data_ov005_021e78cc.field_4 = 2;'
    body = SOURCE.read_text().replace(before, before.replace('= 2;', '= 3;'))
    if body == SOURCE.read_text():
        raise ValueError('Locate actual ready-state mutation')
    for path, text in [(control / 'source.c', body), (control / 'context.h', SOURCE.with_name('context.h').read_text())]:
        if path.exists() and path.read_bytes() != text.encode():
            raise ValueError('Preserve prior state control source')
        path.write_bytes(text.encode())
    compiler.WORK = WORK / 'rejected-state/c'
    bad_rows, unused = compiler.compare(control / 'source.c', 'ov005', '2', 'off', True)
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
        if not isinstance(failure, tuple) or failure[0] != 'Initializer47 complete independent RAM model differs':
            raise ValueError(('State control rejected unexpectedly', failure))
    else:
        raise ValueError('State source control unexpectedly passed')
    try:
        execute(main, overlay, recipes()[0], misalign=True)
    except ValueError as error:
        unsupported = error.args[0]
        if unsupported != 'Initializer47 unsupported unaligned-buffer assertion reached':
            raise
    else:
        raise ValueError('Unaligned profile unexpectedly returned')
    raw = encoded(dict(romSha256=config['romSha256'], module='ov005', address='0x021D8EDC', results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    row['oracle'] = dict(supported=True, evidenceClass='original native initialization caller plus actual guard/IRQ/memory/record helpers, independent complete RAM/CPSR/protocol models and explicit timing/context/callback providers',
        executions=2 * len(results), actualReturns=2 * len(results),
        nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns'] for r in summaries), providedCalls=sum(r['providedCalls'] for r in summaries),
        freshMachinePerExecution=True, instructionBound=100000, maximumInstructionsIncludingProviderEntries=max(r['instructions'] for r in summaries),
        completeImageEquality=True, results=summaries,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed),
            format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
        limitations=['Buffer0x5A88 and argument owner/callback are synthetic; no valid session/scene/resource lifecycle',
            'Time query02007A9C provides explicit R0/R1 register words twice; no universal64-bit signature, timer hardware or chronology claim',
            'Context setup020125BC is supplied with IRQ enabled; ARM/Thumb callback entries are supplied with IRQ disabled and zero native credit',
            'Actual main IRQ MRS/MSR executes only inside isolated Unicorn System mode; no host/device interrupt or policy change',
            'Initial I/F bits are restored and physicalR0 is80; this raw return is not a semantic success flag',
            'Internal pointer021D8900 is stored without invoking its body; unaligned assertion path is separately rejected unsupported before execution',
            'All final registers/flags/full RAM/private stacks/PC/write hashes compare; actual returns/SP/preserved-register gates are required'])
    paths = [str(SOURCE.relative_to(ROOT)), str(SOURCE.with_name('context.h').relative_to(ROOT)),
        'ov005_initializer47_fixture_20261031.py', 'ov005_initializer47_models_20261031.py', 'ov001_ability28_fixture_20261031.py',
        str((control / 'source.c').relative_to(ROOT)), str((control / 'context.h').relative_to(ROOT))]
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], processor='arm9', program='', module='ov005', mode='arm',
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=[row],
        nativeSymbols={item['symbol']: item['target'] for item in row['relocations']}, isolatedLink=proof,
        nativeSourceBytes=276, functionMatches=1, acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False,
        rejectedReadyState=dict(expectedRejected=True, failure=failure, compilation=bad_rows, actualLinkComparison=rejected_link, sourceCredit=0),
        unsupportedUnaligned=dict(expectedRejected=True, result=unsupported, actualReturn=False, sourceCredit=0),
        inputPins=[dict(path=p, sha256=sha256(ROOT / p)) for p in paths], generatorSha256=sha256(Path(__file__)),
        limitations=['Final registration/module/ROM gates remain the integrator responsibility', 'createdUtc is volatile; stable identity excludes only that field',
            'No executable blobs, assembly, opcode modifications, fake register inputs or dependency source credit'],
        reproductionCommand='python match_ov005_initializer47_20261031.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(REPORT, report)
    print(json.dumps({key: row['oracle'][key] for key in ['executions', 'nativeDependencyActualReturns', 'providedCalls', 'maximumInstructionsIncludingProviderEntries']}), flush=True)


if __name__ == '__main__':
    run()
