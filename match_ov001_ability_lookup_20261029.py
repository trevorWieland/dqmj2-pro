import json
import sys
from pathlib import Path

import match_runtime as compiler
import prove_reward_return_abi_20261029 as model
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_award_cases_20261029 import assets
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-ability-lookup/20261029/final'
REPORT = ROOT / 'evidence/matches/ov001-20261029-ability-lookup01.json'
ADDRESS = 0x021E8E08


def vectors(ability):
    for curve in range(33):
        for level in [1, 10, 11, 40, 41, 50, 51, 100]:
            yield {'curve': curve, 'level': level, 'nullTable': False,
                   'expected': ability[curve * 100 + level - 1]}
    for curve in [0, 32, 0xFFFFFFFF, 0x80000000]:
        for level in [0, 100, 0xFFFFFFFF, 0x80000000]:
            yield {'curve': curve, 'level': level, 'nullTable': True, 'expected': -1}


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    sources = list((ROOT / 'src/overlays').glob('ov001_20261029_ability_lookup_*.c'))
    if len(sources) != 1 or sha256(sources[0])[:12] not in sources[0].name:
        raise ValueError('Frozen ability lookup source identity changed')
    compiler.WORK = WORK / 'compiler'
    records, unused = compiler.compare(sources[0], 'ov001', '2', 'off', True)
    if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation') or records[0].get('bytes') != 44:
        raise ValueError('Frozen ability lookup C no longer matches every native byte')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    original = overlay[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 44]
    rebuilt = bytearray(overlay)
    rebuilt[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 44] = linked
    blobs = assets()
    results = []
    for index, vector in enumerate(vectors(blobs['AbilityTbl.bin'])):
        memory = [(0x02238D58, bytes(4))] if vector['nullTable'] else []
        arguments = [vector['curve'], vector['level']]
        native = model.execute(main, overlay, blobs, ADDRESS, arguments, memory, [], vector['expected'], 202610308808 + index)
        source = model.execute(main, bytes(rebuilt), blobs, ADDRESS, arguments, memory, [], vector['expected'], 202610308808 + index)
        if native != source:
            raise ValueError('Original and real-linked ability lookup behavior differs')
        if native['writes'] or native['nativeEntries'] != [[hex(ADDRESS), 44, 'ov001', 'arm']]:
            raise ValueError('Pure ability lookup acquired effects or native callees')
        results.append({'vector': vector, **native})
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=44, justifiedAssemblyBytes=0,
                 nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 oracle={'vectors': len(results), 'executions': len(results) * 2,
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'wholeMappedRamAndStackAndRegistersCompared': True, 'hostCalleeStubs': False,
                         'nativeCallees': [], 'independentTableIndexAndNullErrorModel': True,
                         'supportedErrorPath': 'Null table returns full signed-1 before using either argument',
                         'instructionBound': 100000, 'results': results})
    dependencies = ['prove_reward_return_abi_20261029.py', 'ov001_award_cases_20261029.py',
                    'ov001_award_fixture_20261029.py', 'config/arm9/symbols.txt',
                    'config/arm9/overlays/ov001/symbols.txt']
    result = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {sources[0].relative_to(ROOT).as_posix(): sha256(sources[0])},
              'assetHashes': {name: compiler.sha(blob) for name, blob in blobs.items()},
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']},
              'nativeSymbolEntries': bindings, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'limitations': ['Nonnull input is qualified for curve0..32 and level1..100; other nonnull indices remain unsupported',
                              'Null input includes arbitrary full-width arguments and performs no table access',
                              'Asset loading, current pointer value and whole-scene reachability are separate evidence',
                              'The typed global is a measured address binding; no initialized pointer value is inferred from ROM']}
    write_json(REPORT, result)
    print(json.dumps({'functions': 1, 'bytes': len(original), 'executions': len(results) * 2,
                      'report': REPORT.relative_to(ROOT).as_posix()}))


if __name__ == '__main__':
    run()
