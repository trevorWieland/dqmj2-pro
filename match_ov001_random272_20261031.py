import gzip
import json
import sys
from pathlib import Path
import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_random272_fixture_20261031 import execute
from ov001_random272_models_20261031 import RNG, DIVIDE
from ov001_reroll59_fixture_20261031 import inventory
from ov001_random272_models_20261031 import recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__
SOURCE = ROOT / 'src/overlays/ov001_20261031_random272/random.c'
PINS = ROOT / 'evidence/verification/ov001-random272-inputs-20261031.json'
WORK = ROOT / 'work/ol272-proof'
REPORT = ROOT / 'evidence/matches/ov001-20261031-random272.json'

def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()

def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Random272 pinned Python/Unicorn differs')
    pins = json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError('Random272 frozen source/header/fixture/model differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Random272 measured private input differs')
    metadata, overlay, unused = measured_module('ov001')
    _, ranges = inventory()
    NATIVE = {address: next((b - a for a, b, m, mode in ranges if a == address)) for address in [RNG, DIVIDE]}
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True, thumb=False)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 40:
        raise ValueError('Random272 full40-byte ordinary source compilation differs')
    row = rows[0]
    row['sourceDependencies'] = [dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)), sha256=sha256(SOURCE.with_name('context.h')))]
    bindings = qualified_bindings(row)
    directory = WORK / 'l' / row['objectSha256']
    proof = validate(row, bindings, directory)
    row['exactAfterGenuineLink'], row['linkedMatchingBytes'] = (True, 40)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    candidate = bytearray(overlay)
    offset = 35833600 - 35484224
    candidate[offset:offset + 40] = linked
    if bytes(candidate) != overlay:
        raise ValueError('Random272 complete original/source overlay image differs')
    results, summaries = ([], [])
    for index, recipe in enumerate(recipes()):
        original, rebuilt = (execute(main, overlay, recipe), execute(main, bytes(candidate), recipe))
        if original != rebuilt:
            raise ValueError('Random272 complete original/source executions differ')
        results.append(dict(recipe=recipe, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)), actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']), providedCalls=2 * len(original['providedCalls']), instructions=original['instructions'], observedNativeCallerInstructionBytes=len(original['observedCallerInstructionBytes']), ramSha256=original['ramSha256'], stackSha256=original['stackSha256'], pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
    control = ROOT / 'nonmatching/overlay-lane/20261031-random272-bias-negative'
    control.mkdir(parents=True, exist_ok=True)
    body = SOURCE.read_text().replace('+ 1;', '+ 2;')
    if body == SOURCE.read_text():
        raise ValueError('Random272 source mutation missing')
    for path, text in [(control / 'source.c', body), (control / 'context.h', SOURCE.with_name('context.h').read_text())]:
        if path.exists() and path.read_bytes() != text.encode():
            raise ValueError('Random272 preserve earlier control')
        path.write_bytes(text.encode())
    compiler.WORK = WORK / 'rejected-counter/c'
    bad_rows, unused = compiler.compare(control / 'source.c', 'ov001', '2', 'off', True, thumb=False)
    if len(bad_rows) != 1 or bad_rows[0].get('compiledBytes') != 40:
        raise ValueError('Random272 ordinary negative did not compile40')
    bad_directory = WORK / 'rejected-counter/l'
    try:
        rejected_link = validate(bad_rows[0], qualified_bindings(bad_rows[0]), bad_directory)
    except ValueError as error:
        rejected_link = error.args[0]
    if not isinstance(rejected_link, dict) or rejected_link.get('caller') != bad_rows[0]['name']:
        raise ValueError('Random272 negative failed to link genuinely')
    directed = next((r for r in recipes() if r['stat']==0 and r['rngWord']==1))
    try:
        execute(main, overlay, directed, (bad_directory / 'caller.bin').read_bytes())
    except ValueError as error:
        failure = error.args[0]
        if failure != 'Random272 actual caller/native return protocol differs':
            raise ValueError(('Random272 unexpected negative failure', failure))
    else:
        raise ValueError('Random272 independent mutation unexpectedly passed')
    raw = encoded(dict(romSha256=config['romSha256'], module='ov001', address='0x0222C700', results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    row['oracle'] = dict(supported=True, evidenceClass='Independent signed32 /10 caller, actual native LCG and quotient/remainder helper, bounded-return and unconditional state-advance model', executions=2 * len(results), actualReturns=2 * len(results), nativeDependencyActualReturns=sum((r['nativeDependencyActualReturns'] for r in summaries)), providedCalls=sum((r['providedCalls'] for r in summaries)), freshMachinePerExecution=True, instructionBound=1000, maximumNativeInstructions=max((r['instructions'] for r in summaries)), completeImageEquality=True, observedNativeCallerInstructionBytes=len({a for r in results for a in r['result']['observedCallerInstructionBytes']}), nativeBodies=[dict(processor='arm9', program='', module='main' if a < 35484224 else 'ov001', mode='arm', address=hex(a), bytes=n, sha256=compiler.sha((main if a < 35484224 else overlay)[a - (33554432 if a < 35484224 else 35484224):a - (33554432 if a < 35484224 else 35484224) + n])) for a, n in NATIVE.items()], results=summaries, rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed), format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw)), limitations=['Original main0203D294 and02026350 execute directly; physical quotientR0/remainderR1 are checked independently; no helper/source credit', 'Original21DBCF0 stat getter remains one explicit provider supplying a signed-word interpretation and seed effects; no native stat, actor validity or real getter range is certified', 'Extreme signed32 stat responses stress caller arithmetic and exceed some actual getter return ranges; they do not assert real game values', 'RNG seeds and stat responses are supplied test context, not observed current or future scene state'])
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], processor='arm9', program='', module='ov001', mode='arm', moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=[row], nativeSymbols={item['symbol']: item['target'] for item in row['relocations']}, isolatedLink=proof, nativeSourceBytes=40, functionMatches=1, acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False, rejectedCounterCode=dict(expectedRejected=True, recipe=directed, failure=failure, compilation=bad_rows, actualLinkComparison=rejected_link, sourceCredit=0), inputPins=pins['files'], generatorSha256=sha256(Path(__file__)), limitations=['Final registration/module/ROM gates remain the integrator responsibility', 'createdUtc is volatile; stable identity excludes only that field', 'No executable blobs, assembly, opcode modifications, invented register inputs or dependency source credit'], reproductionCommand='python match_ov001_random272_20261031.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(REPORT, report)
    print(json.dumps({key: row['oracle'][key] for key in ['executions', 'nativeDependencyActualReturns', 'providedCalls', 'maximumNativeInstructions']}), flush=True)
if __name__ == '__main__':
    run()
