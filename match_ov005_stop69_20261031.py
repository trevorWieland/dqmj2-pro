import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov005_stop69_fixture_20261031 import execute
from ov005_stop69_models_20261031 import recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCE = ROOT / 'src/overlays/ov005_20261031_stop69/stop.c'
SOURCE_HASH, HEADER_HASH = 'ca8814b9881251ddb392b59065f10c852c24d8e24db3387dd491b6f2e442b384', 'c5fe82434a905d7e80ce6105ce215564984f091f6654a9dde768e3f7bcd4cb1d'
WORK = ROOT / 'work/ol69-proof'
REPORT = ROOT / 'evidence/matches/ov005-20261031-stop69.json'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Pinned Python/Unicorn differs')
    if sha256(SOURCE) != SOURCE_HASH or sha256(SOURCE.with_name('context.h')) != HEADER_HASH:
        raise ValueError('Frozen stop69 source/header differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private input differs')
    metadata, overlay, unused = measured_module('ov005')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov005', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 144 or not rows[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Full144-byte ordinary stop caller C differs')
    row = rows[0]
    row['sourceDependencies'] = [dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)), sha256=HEADER_HASH)]
    bindings = qualified_bindings(row)
    directory = WORK / 'l' / row['objectSha256']
    proof = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    candidate = bytearray(overlay)
    offset = 0x021D9060 - 0x021D7240
    candidate[offset:offset + 144] = linked
    if bytes(candidate) != overlay:
        raise ValueError('Full original/source stop69 module image differs')
    results, summaries = [], []
    for index, recipe in enumerate(recipes()):
        original, rebuilt = execute(main, overlay, recipe), execute(main, bytes(candidate), recipe)
        if original != rebuilt:
            raise ValueError('Stop69 original/source complete machines differ')
        results.append(dict(recipe=recipe, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)),
            actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']),
            providedCalls=2 * len(original['providedCalls']), instructions=original['instructions'],
            observedNativeCallerInstructionBytes=original['observedNativeCallerInstructionBytes'], ramSha256=original['ramSha256'],
            stackSha256=original['stackSha256'], pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
    control = ROOT / 'nonmatching/overlay-lane/20261031-stop69-inner-negative'
    control.mkdir(parents=True, exist_ok=True)
    before = '+ 0x120, 0);'
    body = SOURCE.read_text().replace(before, before.replace(', 0);', ', 1);'))
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
        execute(main, overlay, recipes()[32], (bad_directory / 'caller.bin').read_bytes())
    except ValueError as error:
        failure = error.args[0]
        if failure != 'Stop69 message-provider arguments differ':
            raise ValueError(('State control rejected unexpectedly', failure))
    else:
        raise ValueError('State source control unexpectedly passed')
    failure = json.loads(json.dumps(failure, default=lambda value: dict(bytesHex=value.hex()) if isinstance(value, bytes) else str(value)))
    raw = encoded(dict(romSha256=config['romSha256'], module='ov005', address='0x021D9060', results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    row['oracle'] = dict(supported=True, evidenceClass='original native state-transition caller plus actual IRQ/guard/halfword-query/inner-field helpers, independent full RAM/virtual I-F/late-pointer/protocol models',
        executions=2 * len(results), actualReturns=2 * len(results),
        nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns'] for r in summaries), providedCalls=sum(r['providedCalls'] for r in summaries),
        freshMachinePerExecution=True, instructionBound=2000, maximumNativeInstructions=max(r['instructions'] for r in summaries),
        completeImageEquality=True, observedNativeCallerInstructionBytes=len({pc + offset for row in results for pc in row['result']['pcTrace'] if 0x021D9060 <= pc < 0x021D9060 + 144 for offset in range(4)}), results=summaries,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed),
            format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
        limitations=['Synthetic state0/1/2/3/4/FFFFFFFF and two buffers do not establish live session/resource lifecycle; only states2/3 enter the transition body',
            'Actual privileged IRQ helper instructions execute only in isolated Unicorn System mode, restoring initial I/F bits and returning raw80 without host/device changes or success meaning',
            'Supplied ARM/Thumb callback receives1/0 after native state1 store, then may change state, global buffer pointer and flags; actual query and conditional inner stores use the new pointer',
            'Actual9124 halfword query and8788 field update execute; downstream7874 remains an explicit provider on raw inner-state2/FFFFFFFF cases, with zero native body credit',
            'All actual return/SP/preserved-register/native-completion gates and final registers/CPSR/full RAM/private stack/PC/writes compare; unobserved native downstream behavior unsupported'])
    paths = [str(SOURCE.relative_to(ROOT)), str(SOURCE.with_name('context.h').relative_to(ROOT)),
        'ov005_stop69_fixture_20261031.py', 'ov005_stop69_models_20261031.py', 'ov001_ability28_fixture_20261031.py',
        str((control / 'source.c').relative_to(ROOT)), str((control / 'context.h').relative_to(ROOT))]
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], processor='arm9', program='', module='ov005', mode='arm',
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=[row],
        nativeSymbols={item['symbol']: item['target'] for item in row['relocations']}, isolatedLink=proof,
        nativeSourceBytes=144, functionMatches=1, acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False,
        rejectedBranchCode=dict(expectedRejected=True, failure=failure, compilation=bad_rows, actualLinkComparison=rejected_link, sourceCredit=0),
        inputPins=[dict(path=p, sha256=sha256(ROOT / p)) for p in paths], generatorSha256=sha256(Path(__file__)),
        limitations=['Final registration/module/ROM gates remain the integrator responsibility', 'createdUtc is volatile; stable identity excludes only that field',
            'No executable blobs, assembly, opcode modifications, fake register inputs or dependency source credit'],
        reproductionCommand='python match_ov005_stop69_20261031.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(REPORT, report)
    print(json.dumps({key: row['oracle'][key] for key in ['executions', 'nativeDependencyActualReturns', 'providedCalls', 'maximumNativeInstructions']}), flush=True)


if __name__ == '__main__':
    run()
