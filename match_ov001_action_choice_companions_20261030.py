import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_action_retry_cases_20261030 import vectors as retry_vectors
from ov001_action_retry_fixture_20261030 import execute as execute_retry
from ov001_intent_fallback_cases_20261030 import vectors as fallback_vectors
from project import ROOT, configuration, now, sha256, write_json
from prove_reward_return_abi_20261029 import execute as execute_fields
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCES = {0x021E8510: ('src/overlays/ov001_20261030_action_retry_afaf9ffbccb6.c', 228),
           0x021E865C: ('src/overlays/ov001_20261030_intent_fallback_7adbdcc41b48.c', 112)}
WORK = ROOT / 'work/ov001-command-scheduling/20261030/action-choice-companions-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-action-choice-companions01.json'


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
    matches = []
    for address, (relative, length) in SOURCES.items():
        compiler.WORK = WORK / f'{address:08x}' / 'compiler'
        records, unused = compiler.compare(ROOT / relative, 'ov001', '2', 'off', True)
        if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation') or records[0]['bytes'] != length:
            raise ValueError('Frozen action-choice companion no longer matches every native byte')
        entry = records[0]
        bindings = qualified_bindings(entry)
        directory = WORK / f'{address:08x}' / 'link' / entry['objectSha256']
        proof = validate(entry, bindings, directory)
        linked = (directory / 'caller.bin').read_bytes()
        save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
        entry.update(save_link_snapshots.freeze_link(proof))
        native = overlay[address - 0x021D7240:address - 0x021D7240 + length]
        rebuilt_overlay = bytearray(overlay)
        rebuilt_overlay[address - 0x021D7240:address - 0x021D7240 + length] = linked
        results = []
        for vector in retry_vectors() if address == 0x021E8510 else fallback_vectors():
            if address == 0x021E8510:
                original = execute_retry(main, overlay, native, assets, vector)
                rebuilt = execute_retry(main, overlay, linked, assets, vector)
            else:
                original = execute_fields(main, overlay, assets, address, [vector['side'], vector['slot']],
                                          vector['memory'], vector['patches'], vector['physicalR0'], vector['seed'])
                rebuilt = execute_fields(main, bytes(rebuilt_overlay), assets, address, [vector['side'], vector['slot']],
                                         vector['memory'], vector['patches'], vector['physicalR0'], vector['seed'])
                original = {'seed': vector['seed'], 'side': vector['side'], 'slot': vector['slot'], 'variant': vector['variant'], **original}
                rebuilt = {'seed': vector['seed'], 'side': vector['side'], 'slot': vector['slot'], 'variant': vector['variant'], **rebuilt}
            if original != rebuilt:
                raise ValueError('Original and genuinely linked action-choice companion executions differ')
            results.append(original)
        entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=length,
                     justifiedAssemblyBytes=0, nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                     signature='void(s32,u32)' if address == 0x021E8510 else 'void(s32,s32)',
                     semanticReturnMeaningCertified=False,
                     oracle={'vectors': len(results), 'executions': len(results) * 2,
                             'actualReturnRequired': True, 'freshMachinePerExecution': True,
                             'nativeCalleesExecuted': address == 0x021E8510, 'hostCalleeStubs': False,
                             'independentFullRamIntentGateRetryCounterRngAndPhysicalR0Model': True,
                             'wholeMappedRamAndStackCompared': True, 'instructionBound': 100000,
                             'nativeCandidateReturnsBothImages': 2 * sum(row.get('nativeCandidateReturns', 0) for row in results),
                             'nativeRngReturnsBothImages': 2 * sum(len(row.get('rngReturns', [])) for row in results),
                             'nativeValidatorReturnsBothImages': 2 * sum(len(row.get('validatorReturns', [])) for row in results),
                             'results': results,
                             'limitations': ['Actor+322 raw gate and valid team/slot pointers are supplied prerequisites; their scene lifecycle is not established',
                                             'Neutral synthetic records and repeated native action slots constrain policy paths; no current/future game state is asserted',
                                             'All candidate/policy/validator/RNG callees run natively for the retry wrapper; no IO or host game-function providers',
                                             'Intent fallback writer is a pure field routine with no callees',
                                             'Physical R0 residue is separately checked; void source and discarded caller results do not assign gameplay return meaning',
                                             'No complete AI, action legality, optimality or whole-combat claim']})
        matches.append(entry)
        print(json.dumps({'address': hex(address), 'bytes': length, 'executions': 2 * len(results)}), flush=True)
    dependencies = [Path(__file__).name, 'ov001_action_retry_cases_20261030.py', 'ov001_action_retry_fixture_20261030.py',
                    'ov001_intent_fallback_cases_20261030.py', 'ov001_action_candidate_cases_20261030.py',
                    'ov001_award_fixture_20261029.py', 'prove_reward_return_abi_20261029.py']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': config['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': matches,
              'sourceHashes': {relative: sha256(ROOT / relative) for relative, length in SOURCES.values()},
              'assetHashes': {name: compiler.sha(raw) for name, raw in assets.items()},
              'sourceReconstructionComplete': False, 'wholeModuleLinked': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {row['symbol']: row['target'] for entry in matches for row in entry['relocations']}}
    write_json(REPORT, report)
    print(json.dumps({'functions': 2, 'bytes': 340, 'executions': sum(row['oracle']['executions'] for row in matches),
                      'report': str(REPORT.relative_to(ROOT))}))


if __name__ == '__main__':
    run()
