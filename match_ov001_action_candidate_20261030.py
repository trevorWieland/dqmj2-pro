import copy
import json
import struct
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_action_candidate_cases_20261030 import RECORDS, vectors
from ov001_action_candidate_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from trace_enemy_initialization_context_20261029 import span
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_action_candidate_9b11c822e7b0.c'
WORK = ROOT / 'work/ov001-command-scheduling/20261030/action-candidate-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-action-candidate01.json'
ADDRESS = 0x021E7290


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python and Unicorn required')
    configuration_data = configuration()
    if sha256(configuration_data['rom']) != configuration_data['romSha256']:
        raise ValueError('Measured private ROM identity differs')
    rom = NintendoDSRom(configuration_data['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in
              ('EnmyKindTbl.bin', 'ActTbl.bin', 'ItemTbl.bin', 'EquipTbl.bin', 'AbilityTbl.bin')}
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'compiler'
    records, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', False)
    if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation') or records[0]['bytes'] != 396:
        raise ValueError('Frozen action candidate no longer matches every native byte')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    native = overlay[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 396]
    results = []
    cases = vectors()
    for vector in cases:
        original = execute(main, overlay, native, assets, vector)
        rebuilt = execute(main, overlay, linked, assets, vector)
        if original != rebuilt:
            raise ValueError('Original and real-linked native candidate executions differ')
        results.append(original)
    negative = copy.deepcopy(next(row for row in cases if row['branch'] == 'policy6' and row['side'] == 0 and row['phase'] == 0))
    negative['branch'] = 'policy6-side0-action1-rejected'
    negative['memory'] = [(address, payload[:8] + bytes([1] * 6) + payload[14:]
                           if RECORDS <= address < RECORDS + 12 * 528 else payload)
                          for address, payload in negative['memory']]
    original = execute(main, overlay, native, assets, negative, observe=True)
    rebuilt = execute(main, overlay, linked, assets, negative, observe=True)
    if original != rebuilt or original['validatorReturns'] != [{'action': 1, 'result': 0, 'actualReturn': True}]:
        raise ValueError('Original rejected-action observation differs')
    observations = [original]
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=396,
                 justifiedAssemblyBytes=0, nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 signature='u32(void*,u32,u32,s16*,u8*,u8*)',
                 oracle={'vectors': len(results) + len(observations), 'executions': 2 * (len(results) + len(observations)),
                         'independentlyPredictedVectors': len(results), 'observationalVectors': len(observations),
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'nativeCalleesExecuted': True, 'hostCalleeStubs': False,
                         'independentIntentRngModeRestorationAndWholeRamModel': True,
                         'wholeMappedRamAndStackCompared': True, 'instructionBound': 100000,
                         'nativeRngReturnsBothImages': 2 * sum(len(row['rngReturns']) for row in results + observations),
                         'nativeValidatorReturnsBothImages': 2 * sum(len(row['validatorReturns']) for row in results + observations),
                         'results': results, 'observations': observations,
                         'limitations': ['Direct candidate tests do not establish caller gate actor+322 or its lifecycle',
                                         'Neutral synthetic actor/status/record inputs with repeated native self-target action slots; no current or future scene claimed',
                                         'Policies0..6 and selected237/no-trait40 path are covered; policy7+, trait40 special branch and varied target selectors remain separate work',
                                         'Rejected side0/action1 observation validates native validator/RNG and all other RAM, but its resulting target slot is observed rather than independently predicted',
                                         'No complete AI, legal action, optimal action or whole-battle behavior certified']})
    addresses = (0x021E732C, 0x021E7330, 0x021E7334, 0x021E7340, 0x021E7350, 0x021E6ED0, 0x021E6FF0)
    words = {hex(address): hex(struct.unpack_from('<I', overlay, address - 0x021D7240)[0]) for address in addresses}
    dependencies = [Path(__file__).name, 'ov001_action_candidate_cases_20261030.py',
                    'ov001_action_candidate_fixture_20261030.py', 'ov001_award_fixture_20261029.py',
                    'trace_enemy_initialization_context_20261029.py']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration_data['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {str(SOURCE.relative_to(ROOT)): sha256(SOURCE)},
              'assetHashes': {name: compiler.sha(raw) for name, raw in assets.items()},
              'verifiedPolicyFourthArgument': {'value': 'zero-extended record[AA]', 'physicalRegister': 'R3',
                  'callees': [span('ov001', address)[0] for address in (0x021E6EC4, 0x021E6FD8)],
                  'instructionWords': words, 'calleeSourceCredit': 0},
              'sourceReconstructionComplete': False, 'wholeModuleLinked': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']}}
    write_json(REPORT, report)
    print(json.dumps({'functions': 1, 'bytes': 396, 'executions': entry['oracle']['executions'],
                      'nativeRngReturns': entry['oracle']['nativeRngReturnsBothImages'],
                      'nativeValidatorReturns': entry['oracle']['nativeValidatorReturnsBothImages'],
                      'report': str(REPORT.relative_to(ROOT))}))


if __name__ == '__main__':
    run()
