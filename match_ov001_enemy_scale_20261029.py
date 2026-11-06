import json
import sys
from pathlib import Path

import match_runtime as compiler
import prove_reward_return_abi_20261029 as machine_model
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_award_cases_20261029 import assets
from ov001_enemy_initialization_fixture_20261029 import scaled
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-enemy-initialization/20261029/scale-final'
REPORT = ROOT / 'evidence/matches/ov001-20261029-enemy-scale01.json'
ADDRESS = 0x021E88A4


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    sources = list((ROOT / 'src/overlays').glob('ov001_20261029_enemy_scale_*.c'))
    if len(sources) != 1 or sha256(sources[0])[:12] not in sources[0].name:
        raise ValueError('Frozen enemy scale source changed')
    compiler.WORK = WORK / 'compiler'
    records, unused = compiler.compare(sources[0], 'ov001', '2', 'off', True)
    if len(records) != 1 or records[0].get('bytes') != 64 or not records[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Frozen enemy scale C no longer matches every native byte')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    main_metadata, main, unused = measured_module('main')
    metadata, overlay, unused = measured_module('ov001')
    rebuilt = bytearray(overlay)
    rebuilt[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 64] = linked
    blobs = assets()
    results = []
    values = [0, 1, -1, 31, 63, 64, 255, 256, 16383, 16384, 32767, -32768,
              65535, 65536, 0x12345678, -0x12345678, 2147483647, -2147483648]
    for value in values:
        for factor in [0, 1, -1, 0x800, 0x1000, 0x1800, 0x2000, -0x1000, -2147483648]:
            for width in range(1, 5):
                expected = scaled(value, factor, width)
                arguments = [value, factor, width]
                seed = 202610308804 + len(results)
                native = machine_model.execute(main, overlay, blobs, ADDRESS, arguments, [], [], expected, seed)
                source = machine_model.execute(main, bytes(rebuilt), blobs, ADDRESS, arguments, [], [], expected, seed)
                if native != source or native['writes'] or native['nativeEntries'] != [[hex(ADDRESS), 64, 'ov001', 'arm']]:
                    raise ValueError('Pure native/source fixed-point scale differs or acquired effects/callees')
                results.append({'value': value, 'factor': factor, 'width': width,
                                'independentExpectedSignedResult': expected, **native})
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=64, justifiedAssemblyBytes=0,
                 nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 oracle={'vectors': len(results), 'executions': len(results) * 2,
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'wholeMappedRamAndStackAndRegistersCompared': True,
                         'nativeGameplayStubs': 0, 'nativeCallees': [],
                         'independentWrappedProductBiasTruncateAndUpperCapModel': True,
                         'instructionBound': 100000, 'results': results})
    dependencies = ['prove_reward_return_abi_20261029.py', 'ov001_enemy_initialization_fixture_20261029.py',
                    'ov001_award_cases_20261029.py', 'ov001_award_fixture_20261029.py',
                    'config/arm9/symbols.txt', 'config/arm9/overlays/ov001/symbols.txt']
    result = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {sources[0].relative_to(ROOT).as_posix(): sha256(sources[0])},
              'assetHashes': {name: compiler.sha(value) for name, value in blobs.items()},
              'nativeSymbols': {}, 'nativeSymbolEntries': {}, 'wholeModuleLinked': False,
              'sourceReconstructionComplete': False, 'generator': Path(__file__).name,
              'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'limitations': ['Native caller uses widths1,2,4; direct width3 probes additionally qualify the same arithmetic',
                  'Widths outside1..4 remain unsupported because the source shift contract differs outside that domain',
                  'Arithmetic wraps32-bit product and bias before signed truncation; there is only an upper cap, no lower clamp',
                  'Extreme inputs are synthetic machine components and do not establish valid game-stat records',
                  'No source credit is added for callers or full-scene reachability']}
    write_json(REPORT, result)
    print(json.dumps({'functions': 1, 'bytes': 64, 'executions': len(results) * 2,
                      'report': REPORT.relative_to(ROOT).as_posix()}))


if __name__ == '__main__':
    run()
