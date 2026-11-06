import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_roster_layout12_fixture_20261030 import execute, recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_roster_layout_setup_03c51177e451.c'
SOURCE_HASH = '03c51177e4510a90d2cf4f6338d8ff4abf5f40a5df94b45ca635d5d5064ca454'
WORK = ROOT / 'work/ov001-roster-layout12-final-20261030'
REPORT = ROOT / 'evidence/matches/ov001-20261030-roster-layout12.json'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def compact(results, rom_hash):
    raw = encoded(dict(schemaVersion=1, romSha256=rom_hash, module='ov001', processor='arm9', mode='arm',
                       address='0x02210E18', sourceSha256=SOURCE_HASH, results=results))
    compressed = gzip.compress(raw, mtime=0)
    path = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != compressed:
        raise ValueError('Content-addressed roster trace differs')
    path.write_bytes(compressed)
    summaries = []
    for index, result in enumerate(results):
        machine = result['result']
        row = dict(case=index, recipeSha256=compiler.sha(encoded(result['recipe'])))
        row.update({key: machine[key] for key in ('actualReturn', 'returnBits', 'nativeInstructions', 'nativeWrites',
                    'wholeRamSha256', 'writeTraceSha256', 'pcTraceSha256', 'stackSha256', 'cpsr')})
        row.update(registersSha256=compiler.sha(encoded(machine['registers'])), providedCalls=len(machine['providerCalls']),
            providedTraceSha256=compiler.sha(encoded(machine['providerCalls'])), nativeDependencyActualReturns=len(machine['nativeDependencyReturns']),
            nativeReturnTraceSha256=compiler.sha(encoded(machine['nativeDependencyReturns'])))
        summaries.append(row)
    return summaries, dict(path=str(path.relative_to(ROOT)), sha256=compiler.sha(compressed), bytes=len(compressed), format='json+gzip',
                           gzipMtime=0, uncompressedSha256=compiler.sha(raw), uncompressedBytes=len(raw))


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4' or sha256(SOURCE) != SOURCE_HASH:
        raise ValueError('Pinned roster source/runtime differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM differs')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 332 or not rows[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Complete original roster source span differs')
    row = rows[0]
    bindings = qualified_bindings(row)
    directory = WORK / 'link' / row['objectSha256']
    proof = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-link-artifacts'
    row.update(save_link_snapshots.freeze_link(proof))
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    itcm_metadata, unused, unused = measured_module('itcm')
    candidate = bytearray(overlay)
    candidate[0x02210E18 - 0x021D7240:0x02210E18 - 0x021D7240 + 332] = linked
    results = []
    for index, recipe in enumerate(recipes()):
        original = execute(main, overlay, recipe)
        rebuilt = execute(main, bytes(candidate), recipe)
        if original != rebuilt:
            raise ValueError('Exact original/source roster machines differ')
        results.append(dict(recipe=recipe, result=original))
        if index % 128 == 0:
            print('actual-return roster recipes', index, flush=True)
    row['oracle'] = dict(evidenceClass='native caller/state/getters with explicit provided rendering/name boundaries',
        executions=2 * len(results), actualReturns=2 * len(results), freshMachinePerExecution=True,
        completeImageEquality=True, instructionBound=100000, hardwareEmulation=False,
        nativeDependencyActualReturns=2 * sum(len(v['result']['nativeDependencyReturns']) for v in results),
        providedCalls=2 * sum(len(v['result']['providerCalls']) for v in results), nativeProviderCredit=0,
        maximumNativeInstructions=max(v['result']['nativeInstructions'] for v in results))
    row['oracle']['results'], row['oracle']['rawTraceArtifact'] = compact(results, config['romSha256'])
    row['nativeSymbolEntries'] = bindings
    dependencies = ['ov001_roster_layout12_fixture_20261030.py', 'ov001_damage_pipeline_fixture_20261030.py', 'ov001_award_fixture_20261029.py']
    record = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=[row],
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'],
        inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in dependencies],
        generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
        limitations=['Only332 reconstructed caller bytes receive proposed source credit; providers and original dependencies receive no new credit',
                    'Mode/flags, three raw roster records, validity markers, opaque14-byte supplied labels and state metric are explicit synthetic inputs',
                    'Name copy/render, lower window setup and two render finalizers are provided; native lower contracts/scene/VRAM/text encoding are not established',
                    'Original eligibility/getters, metric/state preparation, window-call wrappers and aggregate-delay store execute without substitution',
                    'Provided effects and calls are separate from actual native returns; no actual display, valid save, live scene or UI-adapter change is inferred',
                    'All full comparisons execute before compact serialization; complete raw evidence is separately compressed and hashed'],
        reproductionCommand='python match_ov001_roster_layout12_20261030.py')
    write_json(REPORT, record)
    print(json.dumps({key: row['oracle'][key] for key in ('executions', 'nativeDependencyActualReturns', 'providedCalls', 'maximumNativeInstructions')}), flush=True)


if __name__ == '__main__':
    run()
