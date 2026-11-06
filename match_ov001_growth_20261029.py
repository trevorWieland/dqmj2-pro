import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_award_cases_20261029 import assets, vectors as award_vectors
from ov001_award_fixture_20261029 import execute as award_execute
from ov001_parent_gain_fixture_20261029 import execute as parent_execute, vectors as parent_vectors
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCES = {
    0x021E409C: 'src/overlays/ov001_20261029_growth_021e409c_6e4e1ef30d18.c',
    0x021E485C: 'src/overlays/ov001_20261029_growth_021e485c_dc94a5ae8ff1.c',
}
WORK = ROOT / 'work/ov001-reward-growth/20261029'
REPORT = ROOT / 'evidence/matches/ov001-20261029-growth01.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    blobs = assets()
    matches = []
    for address, source_path in SOURCES.items():
        source = ROOT / source_path
        compiler.WORK = WORK / f'{address:08x}' / 'compiler'
        records, code = compiler.compare(source, 'ov001', '2', 'off', True)
        if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation'):
            raise ValueError('Frozen growth source no longer matches every native byte')
        entry = records[0]
        bindings = qualified_bindings(entry)
        directory = WORK / f'{address:08x}' / 'link' / entry['objectSha256']
        proof = validate(entry, bindings, directory)
        linked = (directory / 'caller.bin').read_bytes()
        save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
        entry.update(save_link_snapshots.freeze_link(proof))
        results = []
        if address == 0x021E409C:
            original = overlay[address - 0x021D7240:address - 0x021D7240 + entry['bytes']]
            for vector in parent_vectors():
                native = parent_execute(main, overlay, original, blobs['AbilityTbl.bin'], vector)
                rebuilt = parent_execute(main, overlay, linked, blobs['AbilityTbl.bin'], vector)
                if native != rebuilt:
                    raise ValueError('Direct native/source parent growth state differs')
                results.append(native)
            detail = {'directFunctionExecutions': len(results) * 2, 'hostCalleeStubs': False,
                      'independentSignedNarrowingVariantScalingAndDivisionModel': True,
                      'nullAbilityTableErrorPathExercised': True, 'instructionBound': 10000,
                      'unsupported': ['Variants outside0..2, curve IDs outside0..32, levels outside1..100 and arbitrary aliases']}
        else:
            rebuilt_overlay = bytearray(overlay)
            rebuilt_overlay[address - 0x021D7240:address - 0x021D7240 + len(linked)] = linked
            exercised = 0
            for caller, size in [(0x021E49D0, 244), (0x021E4B34, 256)]:
                caller_code = overlay[caller - 0x021D7240:caller - 0x021D7240 + size]
                for vector in award_vectors(caller):
                    native = award_execute(main, overlay, caller, caller_code, {}, blobs, vector)
                    rebuilt = award_execute(main, bytes(rebuilt_overlay), caller, caller_code, {}, blobs, vector)
                    if native != rebuilt:
                        raise ValueError('Native/source callee-in-award-context state differs')
                    entered = any(int(row[0], 0) == address for row in native['nativeFunctionEntries'])
                    exercised += int(entered)
                    results.append({'originalCaller': hex(caller), 'matchedCalleeEntered': entered, **native})
            if not exercised:
                raise ValueError('No original award caller entered the linked matched callee')
            detail = {'directFunctionExecutions': 0, 'actualOriginalCallerReturns': len(results) * 2,
                      'calleeExercisingVectors': exercised, 'calleeEntryExecutionLowerBound': exercised * 2,
                      'nativeGameplayStubs': 0, 'nativeCalleesExecuted': True,
                      'displayProviders': ['ov001/arm/022071a8', 'ov001/arm/022071d0', 'ov001/arm/02207074'],
                      'independentCallerEligibilityExperienceLevelSkillPointsAndReturnModel': True,
                      'calleeReturnWordIndependentlyModeled': False,
                      'nativeStatEffectsComparedButNotIndependentlyInterpreted': True,
                      'instructionBound': 1000000,
                      'unsupported': ['Direct malformed old/new-level arguments and arbitrary actor aliases',
                                      'Display bodies and full-scene reachability',
                                      'Independent numeric stat-growth/cap interpretation; original native dependencies have zero new source credit']}
        entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=entry['bytes'],
                     justifiedAssemblyBytes=0, nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                     oracle={'vectors': len(results), 'executions': len(results) * 2,
                             'actualReturnRequired': True, 'freshMachinePerExecution': True,
                             'wholeMappedRamAndStackCompared': True, **detail, 'results': results})
        matches.append(entry)
        write_json(WORK / f'{address:08x}' / 'result.json', entry)
        print(json.dumps({'address': hex(address), 'bytes': entry['bytes'], 'executions': len(results) * 2}), flush=True)
    dependencies = [Path(__file__).name, 'ov001_parent_gain_fixture_20261029.py', 'ov001_award_cases_20261029.py',
                    'ov001_award_fixture_20261029.py', 'config/arm9/symbols.txt', 'config/arm9/overlays/ov001/symbols.txt', 'deps/native/ndspy/rom.py']
    result = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': matches,
              'sourceHashes': {path: sha256(ROOT / path) for path in SOURCES.values()},
              'assetHashes': {name: compiler.sha(blob) for name, blob in blobs.items()},
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {row['symbol']: row['target'] for entry in matches for row in entry['relocations']},
              'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'ordinarySceneReachabilityCertified': False}
    write_json(REPORT, result)
    print(json.dumps({'functions': len(matches), 'bytes': sum(row['bytes'] for row in matches),
                      'executions': sum(row['oracle']['executions'] for row in matches), 'report': str(REPORT.relative_to(ROOT))}))


if __name__ == '__main__':
    run()
