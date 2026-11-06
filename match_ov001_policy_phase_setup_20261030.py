import json
import random
import struct
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_policy_phase_cases_20261030 import vectors
from ov001_policy_phase_fixture_20261030 import execute
from project import ROOT, configuration, now, read_json, sha256, write_json
from prove_reward_return_abi_20261029 import execute as execute_native
from recover_linked_runtime import qualified_bindings
from trace_enemy_initialization_context_20261029 import span
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_policy_phase_setup_a63d57687ff8.c'
WORK = ROOT / 'work/ov001-command-scheduling/20261030/policy-phase-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-policy-phase-setup01.json'
ADDRESS = 0x021DA124


def snapshot_probes(main, overlay, assets):
    teams = (0x02236F6C, 0x022362AC, 0x022355EC, 0x02237C2C)
    results = []
    for seed in range(1261000, 1261032):
        rng = random.Random(seed)
        blocks = [rng.randbytes(3 * 1088) for unused in teams]
        memory = list(zip(teams, blocks))
        memory.extend([(0x022355E4, rng.randbytes(4)), (0x022355E8, rng.randbytes(4))])
        captured = bytes(blocks[1][slot * 1088 + 0x35B] for slot in range(3))
        patches = [(team, bytes(3 * 1088)) for team in teams]
        patches.extend([(0x022355E4, bytes(4)), (0x022355E8, captured)])
        result = execute_native(main, overlay, assets, 0x021D9710, [], memory, patches, 0x022355E4, seed)
        results.append({'capturedTeam1Phases': list(captured), **result})
    return {'span': span('ov001', 0x021D9710)[0], 'additionalSourceCredit': 0,
            'nativeActualReturns': len(results), 'hostCalleeStubs': False,
            'independentFourTeamClearSavedThreeBytesAndCountClearModel': True, 'results': results,
            'limitations': ['Original reset captures three team1 phase bytes before clearing all actor buffers',
                            'The fourth saved-byte padding is preserved; no disk/save persistence is claimed',
                            'Other save/restore callers and loaded-overlay selection remain unproved']}


def main_caller_context(main):
    caller = span('main', 0x020438A4)[0]
    site = 0x020438C4
    word = struct.unpack_from('<I', main, site - 0x02000000)[0]
    displacement = ((word & 0xFFFFFF) ^ 0x800000) - 0x800000
    if word & 0xFF000000 != 0xEB000000 or site + 8 + displacement * 4 != ADDRESS:
        raise ValueError('Ordinary main phase-setup branch differs')
    expected_words = [0xE5D00005, 0xE3500000, 0x03A00001, 0x13A00000]
    if list(struct.unpack_from('<4I', main, 0x020438B4 - 0x02000000)) != expected_words:
        raise ValueError('Ordinary initialize-if-zero flag argument chain differs')
    if struct.unpack_from('<I', main, 0x020438F0 - 0x02000000)[0] != 0x020F69C4:
        raise ValueError('Ordinary phase flag base pointer differs')
    targets = [span('ov001', ADDRESS)[0], span('ov002', ADDRESS)[0]]
    return {'caller': caller, 'callSite': hex(site), 'targetAddress': hex(ADDRESS),
            'argument': 'R0=(main byte020F69C9==0); byte is set to1 after the call',
            'evidenceClass': 'measured-static-caller', 'mainCallerExecuted': False,
            'possibleTargetModules': targets,
            'targetModulesHaveDifferentNativeBytes': targets[0]['spanSha256'] != targets[1]['spanSha256'],
            'loadedModuleResolved': False,
            'limitations': ['The main address has distinct ov001/ov002 entries; this does not establish the active overlay or execute a complete scene']}


def gate_probes(main, overlay, assets):
    results = []
    for team in range(4):
        for scene in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 255):
            for metadata in (0, 99, 255):
                for fallback in (0, 1, 255):
                    expected = 0 if team != 1 else 2 if metadata == 99 else 1 if scene in (0, 8) else 3 if scene == 1 else 0 if scene in (3, 4, 5, 6, 7) else int(fallback == 0)
                    memory = [(0x020F69E8, bytes([scene])), (0x021C0F04, bytes([fallback]))]
                    row = execute_native(main, overlay, assets, 0x021D9960,
                                         [team, metadata], memory, [], expected, 1260000 + len(results))
                    results.append({'team': team, 'sceneByte': scene, 'metadataByte': metadata,
                                    'fallbackByte': fallback, 'expectedGate': expected, **row})
    prior_path = ROOT / 'evidence/matches/ov001-20261029-actor-construct01.json'
    prior = read_json(prior_path)
    constructor = prior['matches'][0]
    native, unused, unused = span('ov001', 0x021D9F70)
    if prior['romSha256'] != configuration()['romSha256'] or constructor['targetSha256'] != native['spanSha256']:
        raise ValueError('Frozen constructor proof belongs to different measured bytes')
    for path, expected in prior['sourceHashes'].items():
        if sha256(ROOT / path) != expected:
            raise ValueError('Frozen constructor source differs from accepted evidence')
    if constructor['oracle']['nativeGameplayStubs'] != 0 or not constructor['oracle']['actualReturnRequired']:
        raise ValueError('Constructor evidence does not establish actual original dependencies')
    return {'additionalSourceCredit': 0, 'rankHelper': span('ov001', 0x021D9960)[0],
            'nativeActualReturns': len(results), 'hostCalleeStubs': False, 'results': results,
            'nativePhaseSnapshot': snapshot_probes(main, overlay, assets),
            'ordinaryMainCaller': main_caller_context(main),
            'constructorEvidence': {'path': str(prior_path.relative_to(ROOT)), 'sha256': sha256(prior_path),
                                    'span': native, 'sourceHashes': prior['sourceHashes'],
                                    'executions': constructor['oracle']['executions'],
                                    'independentModelVerifiedGateValues': constructor['oracle']['nativeRankValuesExercised']},
            'fieldMapping': {'constructorSourceRecordMetadata': 'prepared+0xAD',
                             'actorRecordPointer': 'prepared+4', 'sameMetadataThroughActorPointer': 'actor.record+0xA9',
                             'gate': 'actor+0x322', 'phase': 'actor+0x35B'},
            'limitations': ['Raw scene/fallback bytes are supplied, not observed live state',
                            'Constructor proof is referenced and hash-checked rather than credited or rerun here',
                            'Only initialization is established; alias, bulk-copy, loaded-overlay and interrupt writers are not exhaustively excluded',
                            'Native chooser execution still requires a supported present actor and ordinary caller preconditions']}


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python and Unicorn required')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM identity differs')
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin')}
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'compiler'
    records, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation') or records[0]['bytes'] != 128:
        raise ValueError('Frozen phase setup no longer matches all native bytes')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    rebuilt = bytearray(overlay)
    rebuilt[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 128] = linked
    rebuilt = bytes(rebuilt)
    results = []
    for vector in vectors():
        original = execute(main, overlay, vector)
        candidate = execute(main, rebuilt, vector)
        if original != candidate:
            raise ValueError('Original native versus linked phase setup differs')
        results.append(original)
    gate = gate_probes(main, overlay, assets)
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=128, justifiedAssemblyBytes=0,
                 signature='u32(s32)', nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 oracle={'vectors': len(results), 'executions': 2 * len(results),
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'nativeCalleesExecuted': True, 'hostCalleeStubs': False,
                         'independentEligibleSlotOrderPhaseRngAndWholeRamModel': True,
                         'wholeMappedRamAndStackCompared': True, 'instructionBound': 100000,
                         'nativeRngReturnsBothImages': 2 * sum(len(row['rngReturns']) for row in results),
                         'results': results,
                         'limitations': ['Raw gate/presence components include absent-record/gate1 combinations not produced by the constructor',
                                         'Scene lifecycle, saved-phase persistence and whole-battle reachability remain unsupported',
                                         'Already accepted initialization/RNG/getter routines gain no duplicate source credit']})
    dependencies = [Path(__file__).name, 'ov001_policy_phase_cases_20261030.py',
                    'ov001_policy_phase_fixture_20261030.py', 'ov001_action_candidate_cases_20261030.py',
                    'prove_reward_return_abi_20261029.py', 'ov001_award_fixture_20261029.py',
                    'trace_enemy_initialization_context_20261029.py']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': config['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry], 'gateInitializationEvidence': gate,
              'sourceHashes': {str(SOURCE.relative_to(ROOT)): sha256(SOURCE)},
              'assetHashes': {name: compiler.sha(raw) for name, raw in assets.items()},
              'sourceReconstructionComplete': False, 'wholeModuleLinked': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']}}
    write_json(REPORT, report)
    print(json.dumps({'functions': 1, 'bytes': 128, 'executions': entry['oracle']['executions'],
                      'nativeRngReturns': entry['oracle']['nativeRngReturnsBothImages'],
                      'zeroSourceGateProbes': gate['nativeActualReturns'],
                      'zeroSourceSnapshotProbes': gate['nativePhaseSnapshot']['nativeActualReturns'],
                      'report': str(REPORT.relative_to(ROOT))}))


if __name__ == '__main__':
    run()
