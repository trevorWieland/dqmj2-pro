import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_actor_writeback_fixture_20261030 import ADDRESS, execute, vectors, status_ids
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_actor_writeback_14b1da071080.c'
SOURCE_SHA256 = '14b1da071080a858f1dabcc3b32e19b4d1d7116fd3e04a65fcfe0261ca5ae833'
WORK = ROOT / 'work/ov001-actor-writeback/20261030/final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-actor-writeback01.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4' or sha256(SOURCE) != SOURCE_SHA256:
        raise ValueError('Pinned interpreter/Unicorn/frozen source changed')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM changed')
    rom = NintendoDSRom(config['rom'].read_bytes())
    names = ['ItemTbl.bin', 'EquipTbl.bin', 'EnmyKindTbl.bin', 'AbilityTbl.bin', 'BtlStsTbl.bin']
    blobs = {name: bytes(rom.getFileByName(name)) for name in names}
    ids = status_ids(blobs['BtlStsTbl.bin'])
    compiler.WORK = WORK / 'compiler'
    records, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(records) != 1 or records[0].get('bytes') != 356 or not records[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Frozen actor writeback no longer matches every native byte')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    main_metadata, main, unused = measured_module('main')
    metadata, overlay, unused = measured_module('ov001')
    original = overlay[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 356]
    results = []
    for vector in vectors():
        native = execute(main, overlay, original, blobs, vector)
        source = execute(main, overlay, linked, blobs, vector)
        if native != source:
            raise ValueError('Original/source actor writeback state differs')
        results.append(native)
    states = sorted({slot['stateByte201'] for row in results for slot in row['slots']})
    if states != [0, 1, 2, 3] or not any(any(row['preservedPolicyByStatusIndex']) and not all(row['preservedPolicyByStatusIndex']) for row in results):
        raise ValueError('Actor writeback failed to exercise state/persistence alternatives')
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=356, justifiedAssemblyBytes=0,
                 nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 oracle={'vectors': len(results), 'executions': len(results) * 2,
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'wholeMappedRamAndStackAndRegistersCompared': True,
                         'nativeGameplayStubs': 0, 'nativeCalleesExecuted': True,
                         'independentConditionalNormalizationSnapshotStatusPolicyAndStateModel': True,
                         'stateByteValuesExercised': states, 'instructionBound': 100000,
                         'policySlotsAreExplicitSyntheticInputs': True, 'results': results})
    dependencies = ['ov001_actor_writeback_fixture_20261030.py', 'match_ov001_current_stat_restore_20261030.py',
                    'prove_reward_return_abi_20261029.py', 'ov001_award_fixture_20261029.py',
                    'config/arm9/symbols.txt', 'config/arm9/overlays/ov001/symbols.txt', 'deps/native/ndspy/rom.py']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': config['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {SOURCE.relative_to(ROOT).as_posix(): sha256(SOURCE)},
              'assetHashes': {name: compiler.sha(value) for name, value in blobs.items()},
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']},
              'nativeSymbolEntries': bindings, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'nativeStatusIds': ids,
              'runtimePolicyInput': {'processor': 'arm9', 'module': 'main', 'base': '0x02102e2c',
                  'slots': 32, 'stride': 172, 'identityWordOffset': 4, 'flagsHalfwordOffset': 120,
                  'lookup': 'main/arm/0205ca0c', 'flagsGetter': 'main/arm/0205d7cc',
                  'policy': 'First matching ID selects flags; missing ID returns0; bit0 preserves the old record status byte',
                  'inputSource': 'Explicit synthetic runtime slots using IDs from measured BtlStsTbl descriptors',
                  'currentSceneValuesKnown': False, 'initializedRomDataClaim': False, 'sourceDataCredit': 0},
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'limitations': ['Runtime policy slot contents/lifecycle are not recovered from ROM and are not claimed as a current game state',
                  'Measured BtlSts descriptors and synthetic policy flags exercise the actual native lookup/filter without host stubs',
                  'Optional HP/MP restore uses empty traits/item0; other trait/item contexts remain separate work',
                  'Nonnegative species includes0; processed count is not an alive/valid-monster count',
                  'This writes prepared battle records, not a serialized save bank; checksums/bank chronology are outside this function',
                  'Aliases, inaccessible pointers, descriptor tables shorter than60 and full-scene reachability remain unsupported']}
    write_json(REPORT, report)
    print(json.dumps({'functions': 1, 'bytes': 356, 'executions': len(results) * 2,
                      'stateBytes': states, 'report': REPORT.relative_to(ROOT).as_posix()}))


if __name__ == '__main__':
    run()
