import gzip
import json
import sys
from pathlib import Path
import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from project import ROOT, configuration, now, sha256, write_json
from ov001_phases259_models_20261031 import SPECS, NATIVE, recipes, item_table
from ov001_phases259_fixture_20261031 import execute
from unicorn import __version__
BASE = ROOT / 'src/overlays/ov001_20261031_phases259'
PINS = ROOT / 'evidence/verification/ov001-phases259-inputs-20261031.json'
WORK = ROOT / 'work/ol259-proof'
REPORT = ROOT / 'evidence/matches/ov001-20261031-phases259.json'

def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()

def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Phases259 pinned Python/Unicorn differs')
    pins = json.loads(PINS.read_text())
    for p in pins['files']:
        if sha256(ROOT / p['path']) != p['sha256']:
            raise ValueError('Phases259 frozen source/fixture/model differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Phases259 measured input differs')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    matches = []
    links = []
    all_raw = []
    negative = []
    for address, spec in SPECS.items():
        tag = f'{address:08x}'
        source = BASE / tag / 'source.c'
        compiler.WORK = WORK / tag / 'c'
        rows, unused = compiler.compare(source, 'ov001', '2', 'off', True, thumb=False)
        if len(rows) != 1 or rows[0].get('compiledBytes') != spec['bytes']:
            raise ValueError('Phases259 ordinary source size differs')
        row = rows[0]
        row['sourceDependencies'] = [dict(path=str(source.with_name('context.h').relative_to(ROOT)), sha256=sha256(source.with_name('context.h')))]
        bindings = qualified_bindings(row)
        directory = WORK / tag / 'l' / row['objectSha256']
        link = validate(row, bindings, directory)
        linked = (directory / 'caller.bin').read_bytes()
        candidate = bytearray(overlay)
        offset = address - 35484224
        candidate[offset:offset + spec['bytes']] = linked
        if bytes(candidate) != overlay:
            raise ValueError('Phases259 complete native/source module images differ')
        save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
        row.update(save_link_snapshots.freeze_link(link))
        row.update(nativeSymbolEntries=bindings, exactAfterGenuineLink=True, linkedMatchingBytes=spec['bytes'])
        results = []
        summaries = []
        for index, recipe in enumerate(recipes(address)):
            original = execute(main, overlay, address, recipe)
            rebuilt = execute(main, bytes(candidate), address, recipe)
            if original != rebuilt:
                raise ValueError('Phases259 complete original/source executions differ')
            results.append(dict(recipe=recipe, result=original))
            summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)), actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']), providedCalls=2 * len(original['providedCalls']), instructions=original['instructions'], observedNativeCallerInstructionBytes=len(original['observedCallerInstructionBytes']), ramSha256=original['ramSha256'], stackSha256=original['stackSha256'], pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
        used_native = {e['address'] for r in results for e in r['result']['nativeDependencyActualReturns']}
        row['oracle'] = dict(supported=True, evidenceClass='Independent byte-counter transitions and original selected ItemTbl-byte-to-descriptor write with explicit construction/UI boundaries', executions=2 * len(results), actualReturns=2 * len(results), nativeDependencyActualReturns=sum((s['nativeDependencyActualReturns'] for s in summaries)), providedCalls=sum((s['providedCalls'] for s in summaries)), freshMachinePerExecution=True, instructionBound=1000, maximumNativeInstructions=max((s['instructions'] for s in summaries)), completeImageEquality=True, observedNativeCallerInstructionBytes=len({a for r in results for a in r['result']['observedCallerInstructionBytes']}), results=summaries, nativeBodies=[dict(processor='arm9', program='', module='main' if a < 35484224 else 'ov001', mode='arm', address=hex(a), bytes=n, sha256=compiler.sha((main if a < 35484224 else overlay)[a - (33554432 if a < 35484224 else 35484224):a - (33554432 if a < 35484224 else 35484224) + n])) for a, n in NATIVE.items() if hex(a) in used_native], limitations=['All256 byte counters are tested under explicit raw phases; item-copy phase0 has supplied valid actor/descriptor pointers and ROM ItemTbl cache; no ordinary scene/lifecycle claim', 'Original three no-argument LDRB selectors and side/slot lookup execute directly; no duplicate helper/source credit', 'Construction/UI/status bodies in228-byte handler remain explicit providers;196-byte handler executes all selected ItemTbl getters/lookup directly without providers', '196-byte item-copy NULL actor/descriptor cases are outside the returning corpus; ordinary caller validity prerequisites are unresolved, with no automatic application restrictions', 'Actual getters return zero-extended0..255 words; no signed-byte or automatic application restriction is inferred'])
        matches.append(row)
        links.append(link)
        all_raw.append(dict(address=hex(address), results=results))
        print(json.dumps(dict(address=hex(address), actualReturns=row['oracle']['actualReturns'], nativeDependencyActualReturns=row['oracle']['nativeDependencyActualReturns'], providedCalls=row['oracle']['providedCalls'])), flush=True)
        if True:
            control = ROOT / 'nonmatching/overlay-lane/20261031-phases259-threshold-negative' / tag
            control.mkdir(parents=True, exist_ok=True)
            body = source.read_text().replace('> 0x1EU', '>= 0x1EU')
            if body == source.read_text():
                raise ValueError('Phases259 ordinary threshold control missing')
            for path, text in [(control / 'source.c', body), (control / 'context.h', source.with_name('context.h').read_text())]:
                if path.exists() and path.read_bytes() != text.encode():
                    raise ValueError('Phases259 preserve earlier threshold control')
                path.write_bytes(text.encode())
            compiler.WORK = WORK / tag / 'rejected-threshold/c'
            bad_rows, unused = compiler.compare(control / 'source.c', 'ov001', '2', 'off', True, thumb=False)
            if len(bad_rows) != 1 or bad_rows[0].get('compiledBytes') != spec['bytes']:
                raise ValueError('Phases259 threshold control size differs')
            bad_directory = WORK / tag / 'rejected-threshold/l'
            try:
                bad_link = validate(bad_rows[0], qualified_bindings(bad_rows[0]), bad_directory)
            except ValueError as error:
                bad_link = error.args[0]
            if not isinstance(bad_link, dict) or bad_link.get('caller') != bad_rows[0]['name']:
                raise ValueError('Phases259 threshold control failed to link genuinely')
            directed = next((r for r in recipes(address) if r['counter'] == 29 and r['phase'] == (20 if address == 35698940 else 10)))
            try:
                execute(main, overlay, address, directed, (bad_directory / 'caller.bin').read_bytes())
            except ValueError as error:
                failure = error.args[0]
                expected_failure=('Phases259 independent provider order differs','0x21f14a4',0)if address==0x0220B8FC else'Phases259 complete independent RAM differs'
                if failure != expected_failure:
                    raise ValueError(('Phases259 unexpected threshold rejection', failure))
            else:
                raise ValueError('Phases259 threshold mutation unexpectedly passed')
            negative.append(dict(address=hex(address), expectedRejected=True, recipe=directed, failure=failure, compilation=bad_rows, actualLinkComparison=bad_link, sourceCredit=0))
    raw = encoded(dict(romSha256=config['romSha256'], module='ov001', results=all_raw))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    trace = dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed), format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw))
    for row in matches:
        row['oracle']['rawTraceArtifact'] = trace
    report = dict(schemaVersion=1, itemTableEvidence=dict(pathInRom='ItemTbl.bin', fileSha256=compiler.sha(item_table()), bodySha256=compiler.sha(item_table()[8:]), headerBytes=8, rows=256, stride=88, suppliedCachePointer='0x021C2AB4', suppliedTableBase='0x02300000', sourceByteOffset='0x2A', destinationByteOffset='[actor+0x1E8]+0xB0', semantics='Raw byte copy only; descriptorB0 differs from eligibility descriptorAC'), createdUtc=now(), romSha256=config['romSha256'], processor='arm9', program='', module='ov001', mode='arm', moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=matches, isolatedLinks=links, isolatedLink=dict(exactCallerBytes=all((p['exactCallerBytes'] for p in links)), functions=len(matches)), nativeSourceBytes=sum((s['bytes'] for s in SPECS.values())), functionMatches=len(matches), acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False, rejectedThresholdCode=negative, inputPins=pins['files'], generatorSha256=sha256(Path(__file__)), limitations=['Registration/module/ROM gates remain integrator-owned', 'createdUtc is volatile; stable identity excludes only that field', 'No assembly, blobs, opcode patches, fabricated registers/parameters or dependency source credit'], reproductionCommand='python match_ov001_phases259_20261031.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({k: v for k, v in report.items() if k != 'createdUtc'}))
    write_json(REPORT, report)
    print(json.dumps(dict(functions=len(matches), nativeSourceBytes=report['nativeSourceBytes'], actualReturns=sum((r['oracle']['actualReturns'] for r in matches)), nativeDependencyActualReturns=sum((r['oracle']['nativeDependencyActualReturns'] for r in matches)), providedCalls=sum((r['oracle']['providedCalls'] for r in matches)))), flush=True)
if __name__ == '__main__':
    run()
