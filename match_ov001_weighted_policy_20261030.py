import json
import struct
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_action_retry_cases_20261030 import vectors
from ov001_action_retry_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from prove_reward_return_abi_20261029 import execute as execute_guard
from recover_linked_runtime import qualified_bindings
from trace_enemy_initialization_context_20261029 import span
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_weighted_policy_4c40ca85ba57.c'
WORK = ROOT / 'work/ov001-command-scheduling/20261030/weighted-policy-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-weighted-policy01.json'
ADDRESS, CALLER = 0x021E6EC4, 0x021E8510


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python and Unicorn required')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM identity differs')
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in
              ('EnmyKindTbl.bin', 'ActTbl.bin', 'ItemTbl.bin', 'EquipTbl.bin', 'AbilityTbl.bin')}
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'compiler'
    records, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation') or records[0]['bytes'] != 276:
        raise ValueError('Frozen weighted policy no longer matches all native bytes')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    rebuilt_overlay = bytearray(overlay)
    rebuilt_overlay[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 276] = linked
    caller_code = overlay[CALLER - 0x021D7240:CALLER - 0x021D7240 + 228]
    results = []
    for vector in vectors():
        if vector['gate'] != 1 or vector['branch'] not in ('policy0', 'policy1', 'policy2', 'policy3'):
            continue
        original = execute(main, overlay, caller_code, assets, vector)
        rebuilt = execute(main, bytes(rebuilt_overlay), caller_code, assets, vector)
        if original != rebuilt:
            raise ValueError('Original caller/native versus linked weighted policy differs')
        calls = original['nativeCallEntries'].count(hex(ADDRESS))
        if calls != vector['attempts'] or calls == 0:
            raise ValueError('Native caller did not actually enter the policy under test')
        results.append({'policyUnderTestCalls': calls, **original})
    guards = []
    for mode in (4, 7, 8, 127, 255, 0x7FFFFFFF):
        arguments = [0, 0, 0, mode]
        original = execute_guard(main, overlay, assets, ADDRESS, arguments, [], [], 0, 1210000 + mode)
        rebuilt = execute_guard(main, bytes(rebuilt_overlay), assets, ADDRESS, arguments, [], [], 0, 1210000 + mode)
        if original != rebuilt or len(original['nativeEntries']) != 1:
            raise ValueError('Native invalid-mode guard differs or dereferenced null inputs')
        guards.append(original)
    weights = overlay[0x0222EC5C - 0x021D7240:0x0222EC5C - 0x021D7240 + 24]
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=276,
                 justifiedAssemblyBytes=0, nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 signature='u32(void*,u32,u32,s32)',
                 oracle={'vectors': len(results) + len(guards), 'executions': 2 * (len(results) + len(guards)),
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'topNativeCaller': span('ov001', CALLER)[0], 'reconstructedCallee': hex(ADDRESS),
                         'nativeCalleesExecuted': True, 'hostCalleeStubs': False,
                         'policyEntriesBothImages': 2 * sum(row['policyUnderTestCalls'] for row in results),
                         'nativeRngReturnsBothImages': 2 * sum(len(row['rngReturns']) for row in results),
                         'nativeValidatorReturnsBothImages': 2 * sum(len(row['validatorReturns']) for row in results),
                         'independentNativeCallerIntentRetryRngAndWholeRamModel': True,
                         'wholeMappedRamAndStackCompared': True, 'instructionBound': 100000,
                         'results': results, 'guardResults': guards,
                         'limitations': ['Policies0..3 execute under the independently modeled native retry caller with repeated native action1 slots and neutral synthetic state',
                                         'This caller corpus does not independently distinguish every weighted slot or exercise the policy internal13-attempt rejection bound',
                                         'Direct modes4..255 and signed positive maximum return0 before dereferencing null inputs; negative modes are outside supported record-byte inputs',
                                         'No host game-function providers, IO, current scene, full AI, optimality or whole-combat claim',
                                         'Existing native caller/candidate/validator source credit is not counted again']})
    dependencies = [Path(__file__).name, 'ov001_action_retry_cases_20261030.py', 'ov001_action_retry_fixture_20261030.py',
                    'ov001_action_candidate_cases_20261030.py', 'ov001_award_fixture_20261029.py',
                    'prove_reward_return_abi_20261029.py', 'trace_enemy_initialization_context_20261029.py']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': config['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {str(SOURCE.relative_to(ROOT)): sha256(SOURCE)},
              'assetHashes': {name: compiler.sha(raw) for name, raw in assets.items()},
              'probabilityTable': {'address': '0x0222ec5c', 'bytes': 24, 'sha256': compiler.sha(weights),
                                   'rows': [list(weights[index * 6:index * 6 + 6]) for index in range(4)],
                                   'rowSums': [sum(weights[index * 6:index * 6 + 6]) for index in range(4)],
                                   'sourceDataCredit': 0},
              'sourceReconstructionComplete': False, 'wholeModuleLinked': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']}}
    write_json(REPORT, report)
    print(json.dumps({'functions': 1, 'bytes': 276, 'executions': entry['oracle']['executions'],
                      'policyEntries': entry['oracle']['policyEntriesBothImages'],
                      'report': str(REPORT.relative_to(ROOT))}))


if __name__ == '__main__':
    run()
