import gzip
import json
import sys
from pathlib import Path
import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from project import ROOT, configuration, now, sha256, write_json
from ov001_family293_models_20261031 import SPECS, NATIVE as BODY_SPECS, DIVIDE, recipes, action_table
from ov001_family293_fixture_20261031 import execute
from unicorn import __version__
BASE = ROOT / 'src/overlays/ov001_20261031_family293'
PINS = ROOT / 'evidence/verification/ov001-family293-inputs-20261031.json'
WORK = ROOT / 'work/ol293-proof'
REPORT = ROOT / 'evidence/matches/ov001-20261031-family293.json'

from ov001_reroll59_fixture_20261031 import inventory
NATIVE=dict(BODY_SPECS)

def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()

def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Family293 pinned Python/Unicorn differs')
    pins = json.loads(PINS.read_text())
    for p in pins['files']:
        if sha256(ROOT / p['path']) != p['sha256']:
            raise ValueError('Family293 frozen source/fixture/model differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Family293 measured input differs')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    _, body_ranges = inventory()
    NATIVE[DIVIDE] = next(b-a for a,b,m,mode in body_ranges if a==DIVIDE)
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
            raise ValueError('Family293 ordinary source size differs')
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
            raise ValueError('Family293 complete native/source module images differ')
        save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
        row.update(save_link_snapshots.freeze_link(link))
        row.update(nativeSymbolEntries=bindings, exactAfterGenuineLink=True, linkedMatchingBytes=spec['bytes'])
        results = []
        summaries = []
        for index, recipe in enumerate(recipes(address)):
            original = execute(main, overlay, address, recipe)
            rebuilt = execute(main, bytes(candidate), address, recipe)
            if original != rebuilt:
                raise ValueError('Family293 complete original/source executions differ')
            results.append(dict(recipe=recipe, result=original))
            summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)), actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']), providedCalls=2 * len(original['providedCalls']), instructions=original['instructions'], observedNativeCallerInstructionBytes=len(original['observedCallerInstructionBytes']), ramSha256=original['ramSha256'], stackSha256=original['stackSha256'], pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
        used_native = {e['address'] for r in results for e in r['result']['nativeDependencyActualReturns']}
        observed=len({a for r in results for a in r['result']['observedCallerInstructionBytes']})
        if observed!=spec['instructions']:
            raise ValueError('Family293 complete instruction-byte coverage differs')
        row['oracle']=dict(supported=True,evidenceClass='Independent byte-state counters, real native scalar changes, side mapper/receiver and connected RNG traversal',executions=2*len(results),actualReturns=2*len(results),nativeDependencyActualReturns=sum(s['nativeDependencyActualReturns']for s in summaries),providedCalls=sum(s['providedCalls']for s in summaries),freshMachinePerExecution=True,instructionBound=5000,maximumNativeInstructions=max(s['instructions']for s in summaries),completeImageEquality=True,observedNativeCallerInstructionBytes=observed,results=summaries,nativeBodies=[dict(processor='arm9',program='',module='main'if a<35484224 else 'ov001',mode='arm',address=hex(a),bytes=n,sha256=compiler.sha((main if a<35484224 else overlay)[a-(33554432 if a<35484224 else 35484224):a-(33554432 if a<35484224 else 35484224)+n]))for a,n in NATIVE.items()if hex(a)in used_native],limitations=['All256 byte counters and explicit phase classes are supplied; no actual scene initialization or reachability asserted','Raw actor ready31C/blocked1FF/descriptorAC, stat words1F0/1F2, rule mask, menu object and RNG seed are synthetic state','Actual actor lookup/eligibility, raw signed16 getters, amount48, HP112/MP104 scalar changes, RNG40/main72/divider and menu mapper/receiver/clear bodies execute; zero dependency credit','Max-stat getters CBC/CF0, lower status/presentation functions and queryC024 remain explicit providers; their internal mechanics and valid domains are not certified','Physical F1414 word return is passed explicitly to native F1438; the older discarded-return/zero-argument hypothesis is retained only as failed draft context','Stats/rule/seed tests are code-level fixtures, not observed scene state, future RNG prediction or inferred persistent-field meaning'])
        matches.append(row)
        links.append(link)
        all_raw.append(dict(address=hex(address), results=results))
        print(json.dumps(dict(address=hex(address), actualReturns=row['oracle']['actualReturns'], nativeDependencyActualReturns=row['oracle']['nativeDependencyActualReturns'], providedCalls=row['oracle']['providedCalls'])), flush=True)
        if True:
            control = ROOT / 'nonmatching/overlay-lane/20261031-family293-threshold-negative' / tag
            control.mkdir(parents=True, exist_ok=True)
            body = source.read_text().replace('> 0x1EU' if address==0x0222C54C else '> 0x2DU', '>= 0x1EU' if address==0x0222C54C else '>= 0x2DU')
            if body == source.read_text():
                raise ValueError('Family293 ordinary threshold control missing')
            for path, text in [(control / 'source.c', body), (control / 'context.h', source.with_name('context.h').read_text())]:
                if path.exists() and path.read_bytes() != text.encode():
                    raise ValueError('Family293 preserve earlier threshold control')
                path.write_bytes(text.encode())
            compiler.WORK = WORK / tag / 'rejected-threshold/c'
            bad_rows, unused = compiler.compare(control / 'source.c', 'ov001', '2', 'off', True, thumb=False)
            if len(bad_rows) != 1 or bad_rows[0].get('compiledBytes') != spec['bytes']:
                raise ValueError('Family293 threshold control size differs')
            bad_directory = WORK / tag / 'rejected-threshold/l'
            try:
                bad_link = validate(bad_rows[0], qualified_bindings(bad_rows[0]), bad_directory)
            except ValueError as error:
                bad_link = error.args[0]
            if not isinstance(bad_link, dict) or bad_link.get('caller') != bad_rows[0]['name']:
                raise ValueError('Family293 threshold control failed to link genuinely')
            directed = next((r for r in recipes(address) if r['counter'] == (29 if address==0x0222C54C else 44) and r['phase'] == (5 if address==0x0222C54C else 50)))
            try:
                execute(main, overlay, address, directed, (bad_directory / 'caller.bin').read_bytes())
            except ValueError as error:
                failure = error.args[0]
                expected_failure='Family293 native entry order differs' if address==0x0222C54C else 'Family293 complete independent RAM differs'
                if failure != expected_failure:
                    raise ValueError(('Family293 unexpected threshold rejection', failure))
            else:
                raise ValueError('Family293 threshold mutation unexpectedly passed')
            negative.append(dict(address=hex(address), expectedRejected=True, recipe=directed, failure=failure, compilation=bad_rows, actualLinkComparison=bad_link, sourceCredit=0))
    raw = encoded(dict(romSha256=config['romSha256'], module='ov001', results=all_raw))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    trace = dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed), format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw))
    for row in matches:
        row['oracle']['rawTraceArtifact'] = trace
    report = dict(schemaVersion=1, actionTableEvidence=dict(pathInRom='ActTbl.bin',sha256=compiler.sha(action_table()),rows=256,stride=40,headerBytes=8,cachePointer='0x021C6748',tableBase='0x02300000'), createdUtc=now(), romSha256=config['romSha256'], processor='arm9', program='', module='ov001', mode='arm', moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=matches, isolatedLinks=links, isolatedLink=dict(exactCallerBytes=all((p['exactCallerBytes'] for p in links)), functions=len(matches)), nativeSourceBytes=sum((s['bytes'] for s in SPECS.values())), functionMatches=len(matches), acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False, rejectedThresholdCode=negative, inputPins=pins['files'], generatorSha256=sha256(Path(__file__)), limitations=['Registration/module/ROM gates remain integrator-owned', 'createdUtc is volatile; stable identity excludes only that field', 'No assembly, blobs, opcode patches, fabricated registers/parameters or dependency source credit'], reproductionCommand='python match_ov001_family293_20261031.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({k: v for k, v in report.items() if k != 'createdUtc'}))
    write_json(REPORT, report)
    print(json.dumps(dict(functions=len(matches), nativeSourceBytes=report['nativeSourceBytes'], actualReturns=sum((r['oracle']['actualReturns'] for r in matches)), nativeDependencyActualReturns=sum((r['oracle']['nativeDependencyActualReturns'] for r in matches)), providedCalls=sum((r['oracle']['providedCalls'] for r in matches)))), flush=True)
if __name__ == '__main__':
    run()
