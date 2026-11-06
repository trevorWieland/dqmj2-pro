import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_actor_construction_fixture_20261029 import ADDRESS, execute, vectors
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261029_actor_construct_8d37d5236792.c'
SOURCE_SHA256 = '8d37d52367925a8ecb7dc5249b2514e316e876f4b0fab838906c021d8d77f4c3'
WORK = ROOT / 'work/ov001-actor-construction/20261029/final'
REPORT = ROOT / 'evidence/matches/ov001-20261029-actor-construct01.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    if sha256(SOURCE) != SOURCE_SHA256:
        raise ValueError('Frozen actor constructor C changed')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM changed')
    rom = NintendoDSRom(config['rom'].read_bytes())
    names = ['ActTbl.bin', 'ItemTbl.bin', 'EquipTbl.bin', 'EnmyKindTbl.bin']
    blobs = {name: bytes(rom.getFileByName(name)) for name in names}
    actions = blobs['ActTbl.bin'][8:]
    compiler.WORK = WORK / 'compiler'
    records, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(records) != 1 or records[0].get('bytes') != 436 or not records[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Frozen actor constructor no longer matches every native byte')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    main_metadata, main, unused = measured_module('main')
    metadata, overlay, unused = measured_module('ov001')
    original = overlay[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 436]
    results = []
    for vector in vectors():
        native = execute(main, overlay, original, actions, vector, blobs)
        rebuilt = execute(main, overlay, linked, actions, vector, blobs)
        if native != rebuilt:
            raise ValueError('Original/native-linked actor constructor state differs')
        results.append(native)
    ranks = sorted({slot['rank'] for row in results for slot in row['slots']})
    if ranks != [0, 1, 2, 3]:
        raise ValueError('Actor constructor fixtures failed to exercise every measured rank branch')
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=436, justifiedAssemblyBytes=0,
                 nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 oracle={'vectors': len(results), 'executions': len(results) * 2,
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'wholeMappedRamAndStackAndRegistersCompared': True,
                         'nativeGameplayStubs': 0, 'nativeCalleesExecuted': True,
                         'independentSlotCopyRankCapsBitsetAndPrioritySortModel': True,
                         'nativeRankValuesExercised': ranks,
                         'nativeStatSetupPaths': ['supplied-modifier-block', 'empty-traits-native-stat-normalization'],
                         'instructionBound': 100000, 'results': results})
    dependencies = ['ov001_actor_construction_fixture_20261029.py', 'ov001_award_fixture_20261029.py',
                    'config/arm9/symbols.txt', 'config/arm9/overlays/ov001/symbols.txt', 'deps/native/ndspy/rom.py']
    result = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': config['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {SOURCE.relative_to(ROOT).as_posix(): sha256(SOURCE)},
              'assetHashes': {name: compiler.sha(blob) for name, blob in blobs.items()},
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']},
              'nativeSymbolEntries': bindings, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'limitations': ['Teams0..3, prepared slot masks and rank-selection globals are deterministic components, not observed scene state',
                  'Native stat setup executes supplied modifiers or empty-trait zero/ordinary-positive stats; random/complex trait paths remain unsupported',
                  'Expanded lists stay within the actor buffer; malformed overflowing bitset populations and arbitrary aliases remain unsupported',
                  'Other team selectors, inaccessible source pointers, row loading and whole-scene reachability remain unsupported',
                  'Original native dependencies and the inspected application adapter receive zero additional source credit']}
    write_json(REPORT, result)
    print(json.dumps({'functions': 1, 'bytes': 436, 'executions': len(results) * 2,
                      'ranks': ranks, 'report': REPORT.relative_to(ROOT).as_posix()}))


if __name__ == '__main__':
    run()
