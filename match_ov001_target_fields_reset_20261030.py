import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_award_cases_20261029 import assets
from ov001_target_fields_reset_cases_20261030 import INPUT, vectors
from project import ROOT, configuration, now, sha256, write_json
from prove_reward_return_abi_20261029 import execute
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_target_fields_reset_526d33ebe339.c'
WORK = ROOT / 'work/ov001-command-scheduling/20261030/target-reset-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-target-fields-reset01.json'
ADDRESS = 0x021EC620


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python and Unicorn required')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'compiler'
    records, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', False)
    if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation') or records[0]['bytes'] != 80:
        raise ValueError('Frozen target reset no longer matches every native byte')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    rebuilt_overlay = bytearray(overlay)
    rebuilt_overlay[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 80] = linked
    blobs = assets()
    results = []
    for vector in vectors():
        original = execute(main, overlay, blobs, ADDRESS, [INPUT], vector['memory'],
                           vector['patches'], vector['physicalR0'], vector['seed'])
        rebuilt = execute(main, bytes(rebuilt_overlay), blobs, ADDRESS, [INPUT], vector['memory'],
                          vector['patches'], vector['physicalR0'], vector['seed'])
        if original != rebuilt:
            raise ValueError('Original and genuinely linked native target resets differ')
        results.append({'seed': vector['seed'], 'side': vector['side'], 'validMask': vector['validMask'],
                        'invalidKind': vector['invalidKind'], **original})
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=80,
                 justifiedAssemblyBytes=0, nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 signature='u32(void*)', semanticReturnMeaningCertified=False,
                 oracle={'vectors': len(results), 'executions': 2 * len(results),
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'nativeCalleesExecuted': True, 'hostCalleeStubs': False,
                         'independentEligibilityFieldResetAndPhysicalR0Model': True,
                         'wholeMappedRamAndStackCompared': True, 'instructionBound': 100000,
                         'nativeRngDraws': 0, 'results': results,
                         'limitations': ['Nonnull source actor and valid mapped target records are prerequisites except native eligibility guards tested with null record pointers',
                                         'Only fields340/342 of three selected eligible targets reset; no field names or gameplay effects are inferred',
                                         'Physical R0 retains the last native helper word; no gameplay return meaning is established',
                                         'Synthetic actor/record states are not an observed current scene; no complete AI, battle or lifecycle claim']})
    dependencies = [Path(__file__).name, 'ov001_target_fields_reset_cases_20261030.py',
                    'prove_reward_return_abi_20261029.py', 'ov001_award_cases_20261029.py']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {str(SOURCE.relative_to(ROOT)): sha256(SOURCE)},
              'sourceReconstructionComplete': False, 'wholeModuleLinked': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']}}
    write_json(REPORT, report)
    print(json.dumps({'functions': 1, 'bytes': 80, 'executions': 2 * len(results),
                      'report': str(REPORT.relative_to(ROOT))}))


if __name__ == '__main__':
    run()
