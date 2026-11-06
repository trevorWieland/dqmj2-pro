import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_enemy_initialization_fixture_20261029 import ADDRESS, execute, vectors, scaled
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261029_enemy_initialize_97cf6d50f894.c'
SOURCE_SHA256 = '97cf6d50f89406920c08e47912da5cd878fb99c2851981a861120bdeef2a1ef7'
WORK = ROOT / 'work/ov001-enemy-initialization/20261029/final'
REPORT = ROOT / 'evidence/matches/ov001-20261029-enemy-initialize01.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    if sha256(SOURCE) != SOURCE_SHA256:
        raise ValueError('Frozen enemy initialization source changed')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM changed')
    rom = NintendoDSRom(config['rom'].read_bytes())
    enemies = bytes(rom.getFileByName('BtlEnmyPrm2.bin'))
    kind_asset = bytes(rom.getFileByName('EnmyKindTbl.bin'))
    kinds = kind_asset[8:]
    compiler.WORK = WORK / 'compiler'
    records, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(records) != 1 or records[0].get('bytes') != 1092 or not records[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Frozen enemy initializer no longer matches every native byte')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    main_metadata, main, unused = measured_module('main')
    metadata, overlay, unused = measured_module('ov001')
    original = overlay[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 1092]
    results = []
    full_width_distinctions = 0
    for vector in vectors(enemies):
        native = execute(main, overlay, original, kinds, vector)
        rebuilt = execute(main, overlay, linked, kinds, vector)
        if native != rebuilt:
            raise ValueError('Native/source enemy initialization state differs')
        for call in native['independentScaleCalls']:
            value, factor, width = call['arguments']
            if width == 4:
                narrowed = (value + 0x8000) % 0x10000 - 0x8000
                full_width_distinctions += int(scaled(value, factor, width) != scaled(narrowed, factor, width))
        results.append(native)
    if not full_width_distinctions:
        raise ValueError('No source/native vector distinguishes full experience word from false signed16 prototype')
    scale_returns = sum(len(row['nativeScaleReturnBits']) for row in results) * 2
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=1092, justifiedAssemblyBytes=0,
                 nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 oracle={'vectors': len(results), 'executions': len(results) * 2,
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'wholeMappedRamAndStackAndRegistersCompared': True,
                         'nativeGameplayStubs': 0, 'nativeCalleesExecuted': True,
                         'independentCopyScalingSaturationRngAndDropRateModel': True,
                         'nativeScaleSubroutineActualReturns': scale_returns,
                         'fullWordExperienceDistinguishingVectors': full_width_distinctions,
                         'supportedErrorPath': 'Negative destination identity returns0 with no destination/RNG changes',
                         'instructionBound': 100000, 'results': results})
    dependencies = ['ov001_enemy_initialization_fixture_20261029.py', 'ov001_award_fixture_20261029.py',
                    'config/arm9/symbols.txt', 'config/arm9/overlays/ov001/symbols.txt', 'deps/native/ndspy/rom.py']
    result = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': config['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {SOURCE.relative_to(ROOT).as_posix(): sha256(SOURCE)},
              'assetHashes': {'BtlEnmyPrm2.bin': compiler.sha(enemies), 'EnmyKindTbl.bin': compiler.sha(kind_asset)},
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']},
              'nativeSymbolEntries': bindings, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'limitations': ['Measured row and synthetic component contexts do not prove encounter or scene reachability',
                              'Flag8 and initial variants/RNG states are explicit synthetic prerequisites, not observed future game state',
                              'No host ROM IO or native memory allocation is needed for this isolated body',
                              'Aliases, inaccessible pointers and missing kind tables remain unsupported',
                              'Original native callees receive zero additional source credit; parent-field naming remains separate from measured offsets']}
    write_json(REPORT, result)
    print(json.dumps({'functions': 1, 'bytes': 1092, 'executions': len(results) * 2,
                      'nativeScaleReturns': scale_returns, 'fullWordDistinctions': full_width_distinctions,
                      'report': REPORT.relative_to(ROOT).as_posix()}))


if __name__ == '__main__':
    run()
