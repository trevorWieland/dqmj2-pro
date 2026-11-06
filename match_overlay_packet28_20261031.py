import gzip
import json
import re
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_ability28_fixture_20261031 import execute as ability_execute, recipes as ability_recipes, RULES
from ov006_summary28_fixture_20261031 import execute as summary_execute
from ov006_summary28_models_20261031 import recipes as summary_recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

WORK = ROOT / 'work/ol28-proof'
SPECS = [dict(module='ov001', address=0x0220FA6C, size=788, name='ability',
    source='src/overlays/ov001_20261031_ability28/flags.c',
    sourceHash='8dfc73fd4fabc3aa8626079d64f2e715dd1c4b8f3431eb91f73b73ae2288ca35',
    headerHash='250e65fd3b8edf112792b0769725e470605088f7e57fb2df85f97632418b6902',
    fixture=['ov001_ability28_fixture_20261031.py'], execute=ability_execute, recipes=ability_recipes),
    dict(module='ov006', address=0x021DCB20, size=508, name='summary',
    source='src/overlays/ov006_20261031_summary28/summary.c',
    sourceHash='a040fede8fc7f4611a97f05d3dc31caca93d3716bc8063a3c31387f57e4c5397',
    headerHash='b4c569e9d0e51d8392f05ebd993e2a787f4d92a369927825c118b58863ef91ed',
    fixture=['ov006_summary28_fixture_20261031.py', 'ov006_summary28_models_20261031.py'],
    execute=summary_execute, recipes=summary_recipes)]


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def control(spec, main, overlay):
    source = ROOT / spec['source']
    body = source.read_text()
    if spec['name'] == 'ability':
        replaced = body.replace(' | 0x40);', ' | 0x80);', 1)
        expected_failure = 'Ability28 complete flag-memory/order model differs'
        recipe = spec['recipes']()[72]
    else:
        replaced = re.sub(r'\btext\b', '&sp8', body.replace('    u16 text[32];', '    u32 sp8;'))
        expected_failure = 'Summary28 output buffer escapes locals'
        recipe = spec['recipes']()[0]
    if replaced == body:
        raise ValueError('Locate actual source mutation control')
    folder = ROOT / 'nonmatching/overlay-lane/20261031-packet28-negative' / (spec['name'] if spec['name'] == 'ability' else 'summary-scalar')
    folder.mkdir(parents=True, exist_ok=True)
    for path, text in [(folder / 'source.c', replaced), (folder / 'context.h', source.with_name('context.h').read_text())]:
        if path.exists() and path.read_bytes() != text.encode():
            raise ValueError('Preserve prior packet28 negative source')
        path.write_bytes(text.encode())
    compiler.WORK = WORK / spec['name'] / 'rejected/c'
    rows, unused = compiler.compare(folder / 'source.c', spec['module'], '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError('Packet28 mutation control failed compilation')
    directory = WORK / spec['name'] / 'rejected/l'
    try:
        link = validate(rows[0], qualified_bindings(rows[0]), directory)
    except ValueError as error:
        link = error.args[0]
    if not isinstance(link, dict) or link.get('caller') != rows[0]['name']:
        raise ValueError('Packet28 mutation control did not genuinely link')
    try:
        spec['execute'](main, overlay, recipe, (directory / 'caller.bin').read_bytes())
    except ValueError as error:
        failure = error.args[0]
        actual = failure[0] if isinstance(failure, tuple) else failure
        if actual != expected_failure:
            raise ValueError(('Packet28 control failed unexpectedly', failure))
    else:
        raise ValueError('Packet28 mutation control unexpectedly passed')
    return dict(expectedRejected=True, failure=failure, sourceCredit=0, compilation=rows,
        actualLinkComparison=link), [str((folder / name).relative_to(ROOT)) for name in ('source.c', 'context.h')]


def run_one(spec):
    source = ROOT / spec['source']
    if sha256(source) != spec['sourceHash'] or sha256(source.with_name('context.h')) != spec['headerHash']:
        raise ValueError('Frozen packet28 source/header differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private input differs')
    metadata, overlay, unused = measured_module(spec['module'])
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / spec['name'] / 'c'
    rows, unused = compiler.compare(source, spec['module'], '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != spec['size'] or not rows[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Full ordinary packet28 C differs')
    row = rows[0]
    row['sourceDependencies'] = [dict(path=str(source.with_name('context.h').relative_to(ROOT)), sha256=spec['headerHash'])]
    bindings = qualified_bindings(row)
    directory = WORK / spec['name'] / 'l' / row['objectSha256']
    proof = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / spec['name'] / 'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    rebuilt = bytearray(overlay)
    offset = spec['address'] - 0x021D7240
    rebuilt[offset:offset + spec['size']] = linked
    if bytes(rebuilt) != overlay:
        raise ValueError('Full original/rebuilt packet28 module image differs')
    results, summaries = [], []
    for index, recipe in enumerate(spec['recipes']()):
        original = spec['execute'](main, overlay, recipe)
        candidate = spec['execute'](main, bytes(rebuilt), recipe)
        if original != candidate:
            raise ValueError('Packet28 original/rebuilt complete machines differ')
        results.append(dict(recipe=recipe, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)),
            actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeDependencyActualReturns']),
            providedCalls=2 * len(original['providedCalls']), instructions=original['instructions'], returnWord=original['returnWord'],
            ramSha256=original['ramSha256'], stackSha256=original['stackSha256'],
            pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
    rejected, control_paths = control(spec, main, overlay)
    raw = encoded(dict(romSha256=config['romSha256'], module=spec['module'], processor='arm9', mode='arm',
        address=hex(spec['address']), sourceSha256=spec['sourceHash'], results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / spec['name'] / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    limits = ['Two explicit lower-call providers supply raw lookup/gate return words; no native RNG, lookup, resource lifecycle or full-scene execution claim',
        'Lookup result is tested as signed32 >0; gate result is tested as any nonzero word',
        'Only caller writes to actor+0x33C and physical return0/1 are modeled; raw IDs/masks/parameters do not establish human ability names',
        'All12 ordered calls, signed extremes, skips, successful already-set bits, preserving all unrelated flags and write order are covered'] if spec['name'] == 'ability' else [
        'Native main getters and raw-ID transform execute and actually return; text/format/label/display services are explicitly provided',
        'UTF16-sized supplied words are synthetic; no game text encoding/rendering, hardware, resource lifecycle or scene reachability claim',
        'Five signed numeric source fields use modest signed values to avoid signed-overflow extrapolation; field0xC is0..7',
        'Full64-byte text capacity is verified against actual frame bounds, supplied lengths0/1/31 and NUL consumption',
        'Final physical R0 is the last display provider return word; no semantic return interpretation']
    row['oracle'] = dict(supported=True, evidenceClass='original native caller with independent protocol/complete RAM/write models and explicitly separated lower providers',
        executions=2 * len(results), actualReturns=2 * len(results), nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns'] for r in summaries),
        providedCalls=sum(r['providedCalls'] for r in summaries), freshMachinePerExecution=True, instructionBound=2000,
        maximumNativeInstructions=max(r['instructions'] for r in summaries), completeImageEquality=True, results=summaries,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed),
            format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
        limitations=limits + ['All registers/flags/full RAM/private stacks/PC and writes compare; actual top return and preserved registers are required'])
    pins = [spec['source'], str(source.with_name('context.h').relative_to(ROOT))] + spec['fixture'] + control_paths
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], module=spec['module'], processor='arm9', mode='arm',
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=[row],
        nativeSymbols={item['symbol']: item['target'] for item in row['relocations']}, isolatedLink=proof,
        nativeSourceBytes=spec['size'], functionMatches=1, acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False,
        nativeRawRules=RULES if spec['name'] == 'ability' else None,
        rejectedSourceMutation=rejected, inputPins=[dict(path=p, sha256=sha256(ROOT / p)) for p in pins], generatorSha256=sha256(Path(__file__)),
        limitations=['Final registration/module/ROM gates remain the integrator responsibility', 'createdUtc is volatile; stable identity excludes only that field',
            'No ordinary code blobs, assembly, padding, opcode changes, fake register inputs or new credits for native dependencies'],
        reproductionCommand='python match_overlay_packet28_20261031.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(ROOT / f"evidence/matches/{spec['module']}-20261031-{spec['name']}28.json", report)
    print(spec['name'], json.dumps({key: row['oracle'][key] for key in ['executions', 'nativeDependencyActualReturns', 'providedCalls', 'maximumNativeInstructions']}), flush=True)


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Pinned Python/Unicorn differs')
    for spec in SPECS:
        run_one(spec)


if __name__ == '__main__':
    run()
