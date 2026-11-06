import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov005_dispatcher13_fixture_20261030 import execute, recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCE = ROOT / 'src/overlays/ov005_20261030_descriptor_search_0a8defe25b6a.c'
SOURCE_HASH = '0a8defe25b6ad7e6cbc15aa9d95d1d3df12b3ede2d18936ccbd8932130d55282'
WORK = ROOT / 'work/ov5s13'
REPORT = ROOT / 'evidence/matches/ov005-20261030-descriptor-search13.json'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4' or sha256(SOURCE) != SOURCE_HASH:
        raise ValueError('Pinned descriptor search source/runtime differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM differs')
    compiler.WORK = WORK / 'c'
    records, unused = compiler.compare(SOURCE, 'ov005', '2', 'off', True)
    if len(records) != 1 or records[0].get('compiledBytes') != 196 or not records[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Full196-byte descriptor C span differs')
    row = records[0]
    bindings = qualified_bindings(row)
    directory = WORK / 'link' / row['objectSha256']
    proof = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-link-artifacts'
    row.update(save_link_snapshots.freeze_link(proof))
    metadata, overlay, unused = measured_module('ov005')
    main_metadata, main, unused = measured_module('main')
    candidate = bytearray(overlay)
    candidate[0x021D7480 - 0x021D7240:0x021D7480 - 0x021D7240 + 196] = linked
    if bytes(candidate) != overlay:
        raise ValueError('Full original/reconstructed helper module image differs')
    results, summaries = [], []
    for index, recipe in enumerate(recipes()):
        original = execute(main, overlay, recipe)
        rebuilt = execute(main, bytes(candidate), recipe)
        if original != rebuilt:
            raise ValueError('Original/reconstructed helper complete caller machines differ')
        results.append(dict(recipe=recipe, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), resultSha256=compiler.sha(encoded(original)),
            callerActualReturns=2, helperActualReturns=2 * len(original['nativeDependencyActualReturns']),
            instructions=original['instructions'], providedCalls=2 * len(original['providedCalls']),
            normalizedRamSha256=original['normalizedRamSha256'], physicalCallerR0=original['returnWord'],
            pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
        if index % 48 == 0:
            print('exact helper caller recipes', index, flush=True)
    raw = encoded(dict(romSha256=config['romSha256'], module='ov005', processor='arm9', mode='arm',
                       address='0x021D7480', sourceSha256=SOURCE_HASH, results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    row['nativeSymbolEntries'] = bindings
    row['oracle'] = dict(evidenceClass='actual original dispatcher with reconstructed byte-exact descriptor search and explicit supplied callbacks',
        executions=2 * len(results), actualReturns=2 * len(results), nativeDependencyActualReturns=2 * len(results),
        providedCalls=sum(item['providedCalls'] for item in summaries), freshMachinePerExecution=True,
        completeImageEquality=True, instructionBound=10000, maximumNativeInstructions=max(item['instructions'] for item in summaries),
        results=summaries, rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed),
            bytes=len(compressed), format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw), uncompressedBytes=len(raw)))
    pins = ['ov005_dispatcher13_fixture_20261030.py']
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=[row],
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'],
        inputPins=[dict(path=p, sha256=sha256(ROOT / p)) for p in pins],
        generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
        limitations=['Only196 reconstructed helper bytes are proposed; original1500-byte caller and all other module scaffolding receive zero new source credit',
                     'Full zero/missing/exact first/last/high-marker/special80400120 search paths execute over explicit16x48-byte tables',
                     'Actual helper returns are separately checked; full-word callback outputs0/1/80000000/FFFFFFFF are retained',
                     'Virtual selection and outer request callbacks are synthetic ARM/Thumb interfaces, not observed loaded game targets; their calls are not native return credit',
                     'Pointers/table fields are explicit supported aligned inputs; malformed/unmapped structures, retained stack pointers, resource validity and whole-scene reachability remain unsupported',
                     'All registers, flags, full RAM, private stacks and traces compare identically between native and identical genuinely compiled helper images',
                     'No assembly, inherited-register parameters, binary/disassembly sources, opcode patches, RNG/live state, hardware/audio or application edits',
                     'createdUtc is volatile; deterministic report identity excludes only that field'],
        reproductionCommand='python match_ov005_descriptor_search13_20261030.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(REPORT, report)
    print(json.dumps({key: row['oracle'][key] for key in ['executions', 'nativeDependencyActualReturns', 'providedCalls', 'maximumNativeInstructions']}), flush=True)


if __name__ == '__main__':
    run()
