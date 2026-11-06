import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_advanced_policy_cases_20261030 import vectors
from ov001_advanced_policy_fixture_20261030 import execute
from ov001_action_retry_cases_20261030 import vectors as caller_vectors
from ov001_action_retry_fixture_20261030 import execute as execute_caller
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_advanced_policy_f4980d48a03b.c'
WORK = ROOT / 'work/ov001-command-scheduling/20261030/advanced-policy-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-advanced-policy01.json'
ADDRESS, CALLER = 0x021E6FD8, 0x021E8510


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
    if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation') or records[0]['bytes'] != 620:
        raise ValueError('Frozen advanced policy no longer matches all native bytes')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    rebuilt = bytearray(overlay)
    rebuilt[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 620] = linked
    rebuilt = bytes(rebuilt)
    results = []
    for vector in vectors():
        original = execute(main, overlay, assets, vector)
        candidate = execute(main, rebuilt, assets, vector)
        if original != candidate:
            raise ValueError('Original native versus linked advanced policy differs')
        results.append(original)
    callers = []
    caller_code = overlay[CALLER - 0x021D7240:CALLER - 0x021D7240 + 228]
    for vector in caller_vectors():
        if vector['gate'] != 1 or vector['branch'] not in ('policy4', 'policy5', 'policy6'):
            continue
        original = execute_caller(main, overlay, caller_code, assets, vector)
        candidate = execute_caller(main, rebuilt, caller_code, assets, vector)
        if original != candidate or hex(ADDRESS) not in original['nativeCallEntries']:
            raise ValueError('Native retry caller did not execute the reconstructed policy identically')
        callers.append(original)
    oracle = {'vectors': len(results) + len(callers), 'executions': 2 * (len(results) + len(callers)),
              'actualReturnRequired': True, 'freshMachinePerExecution': True,
              'nativeCalleesExecuted': True, 'hostCalleeStubs': False, 'instructionBound': 100000,
              'independentFullRamRngValidatorVisitedArrayAndRetryModel': True,
              'wholeMappedRamAndStackCompared': True, 'results': results, 'nativeCallerResults': callers,
              'nativeRngReturnsBothImages': 2 * sum(len(row['rngReturns']) for row in results + callers),
              'nativeValidatorReturnsBothImages': 2 * sum(len(row['validatorReturns']) for row in results + callers),
              'direct13AttemptVectors': sum(row['expected']['attempts'] == 13 for row in results),
              'fiveRejectedSlotsVectors': sum(sum(event[0] in ('firstWrite', 'write') for event in row['visitedEvents']) == 5
                                              for row in results),
              'repeatedVisitedSlotVectors': sum(any(event[0] == 'read' and event[2] == 1 for event in row['visitedEvents'])
                                                for row in results),
              'privateStackArray': {'words': 5, 'bytes': 20, 'baseOffsetFromEntrySp': -60,
                                    'actualReadWriteIndicesChecked': [1, 5], 'sourcePointerBits': 32,
                                    'signedAddressArithmeticDomain': 'Private stack object and offsets are positive signed32 addresses'},
              'limitations': ['Direct models use actual action1/action2 records, neutral synthetic status and all live synthetic teams',
                              'Controller signed byte+1A is supplied as0 or1; lifecycle and scene reachability remain unproved',
                              'The action1 signed row+26 flag exercises13 retries; other skill semantics, target availability and history branches remain unsupported',
                              'Mode6 random repeated visits have a100000-instruction execution bound rather than a universal termination proof',
                              'Current or future RNG, optimality, complete AI and whole combat are not claimed',
                              'Native caller/candidate/dependency source credit is not counted again']}
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=620, justifiedAssemblyBytes=0,
                 signature='u32(void*,s32,s32,u32)', nativeSymbolEntries=bindings,
                 isolatedCallerLink=proof, oracle=oracle)
    dependencies = [Path(__file__).name, 'ov001_advanced_policy_cases_20261030.py',
                    'ov001_advanced_policy_fixture_20261030.py', 'ov001_action_retry_cases_20261030.py',
                    'ov001_action_retry_fixture_20261030.py', 'ov001_action_candidate_cases_20261030.py',
                    'ov001_award_fixture_20261029.py']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': config['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {str(SOURCE.relative_to(ROOT)): sha256(SOURCE)},
              'assetHashes': {name: compiler.sha(raw) for name, raw in assets.items()},
              'sourceReconstructionComplete': False, 'wholeModuleLinked': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']}}
    if not oracle['fiveRejectedSlotsVectors'] or not oracle['repeatedVisitedSlotVectors'] or not oracle['direct13AttemptVectors']:
        raise ValueError('Critical policy rejection/retry paths were not independently exercised')
    write_json(REPORT, report)
    print(json.dumps({'functions': 1, 'bytes': 620, 'executions': oracle['executions'],
                      'fiveRejectedSlotsVectors': oracle['fiveRejectedSlotsVectors'],
                      'repeatedVisitedSlotVectors': oracle['repeatedVisitedSlotVectors'],
                      'direct13AttemptVectors': oracle['direct13AttemptVectors'], 'report': str(REPORT.relative_to(ROOT))}))


if __name__ == '__main__':
    run()
