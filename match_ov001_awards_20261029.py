import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_award_cases_20261029 import assets, vectors
from ov001_award_fixture_20261029 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCES = {
    0x021E49D0: 'src/overlays/ov001_20261029_award_021e49d0_d75b8516e261.c',
    0x021E4B34: 'src/overlays/ov001_20261029_award_021e4b34_85728a35b986.c',
    0x021E4C34: 'src/overlays/ov001_20261029_award_021e4c34_bc61ba27a2b1.c',
}
WORK = ROOT / 'work/ov001-reward-helpers/20261029/accepted-candidates'
REPORT = ROOT / 'evidence/matches/ov001-20261029-awards01.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    blobs = assets()
    matches, native_entries = [], set()
    for address, source_path in SOURCES.items():
        source = ROOT / source_path
        compiler.WORK = WORK / f'{address:08x}' / 'compiler'
        records, code = compiler.compare(source, 'ov001', '2', 'off', True)
        if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation'):
            raise ValueError('Frozen award source no longer matches all native bytes')
        entry = records[0]
        bindings = qualified_bindings(entry)
        directory = WORK / f'{address:08x}' / 'link' / entry['objectSha256']
        proof = validate(entry, bindings, directory)
        linked = (directory / 'caller.bin').read_bytes()
        save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
        entry.update(save_link_snapshots.freeze_link(proof))
        native = overlay[address - 0x021D7240:address - 0x021D7240 + entry['bytes']]
        results = []
        for vector in vectors(address):
            original = execute(main, overlay, address, native, bindings, blobs, vector)
            rebuilt = execute(main, overlay, address, linked, bindings, blobs, vector)
            if original != rebuilt:
                raise ValueError('Native/source award registers, memory or traces differ')
            results.append(original)
            native_entries.update(tuple(row) for row in original['nativeFunctionEntries'])
        entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=entry['bytes'],
                     justifiedAssemblyBytes=0, nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                     oracle={'vectors': len(results), 'executions': len(results) * 2,
                             'actualReturnRequired': True, 'freshMachinePerExecution': True,
                             'nativeGameplayCalleesExecuted': True, 'nativeGameplayStubs': 0,
                             'displayProviders': ['ov001/arm/022071a8', 'ov001/arm/022071d0', 'ov001/arm/02207074'],
                             'displayProviderContract': 'Return zero, preserve all other registers/flags and perform no memory writes',
                             'resourceBinding': 'main/arm/0202a818: bounded four-byte LevelUpTbl.bin read with deterministic success/failure and caller-saved argument clobbers',
                             'independentExperienceEligibilityLevelSkillPointAndReturnModel': True,
                             'nativeStatEffectsComparedButNotIndependentlyInterpreted': True,
                             'wholeMappedRamAndStackCompared': True, 'instructionBound': 1000000,
                             'results': results,
                             'limitations': ['Synthetic bounded component states do not establish ordinary scene reachability',
                                             'Display callback implementations are not executed',
                                             'ROM filesystem driver and curve allocation/cache misses are not executed; eighteen curves are preloaded',
                                             'Stat growth/cap machine effects are reproduced by original native callees; their numeric interpretation is not independently certified here',
                                             'Signed-overflow pools, malformed species/curve IDs, invalid level/skill tables and arbitrary aliases are unsupported',
                                             'Original native dependency bytes provide zero additional source-recovery credit']})
        matches.append(entry)
        write_json(WORK / f'{address:08x}' / 'result.json', entry)
        print(json.dumps({'address': hex(address), 'bytes': entry['bytes'], 'executions': len(results) * 2}), flush=True)
    dependency_proofs = []
    for address, size, module, mode in sorted(native_entries):
        start = int(address, 0)
        raw, base = (main, 0x02000000) if module == 'main' else (overlay, 0x021D7240)
        dependency_proofs.append({'module': module, 'processor': 'arm9', 'address': address,
                                 'mode': mode, 'bytes': size, 'spanSha256': compiler.sha(raw[start - base:start - base + size]),
                                 'additionalSourceCredit': 0})
    dependencies = [Path(__file__).name, 'ov001_award_cases_20261029.py', 'ov001_award_fixture_20261029.py',
                    'config/arm9/symbols.txt', 'config/arm9/overlays/ov001/symbols.txt', 'deps/native/ndspy/rom.py']
    result = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': matches,
              'sourceHashes': {path: sha256(ROOT / path) for path in SOURCES.values()},
              'assetHashes': {name: compiler.sha(blob) for name, blob in blobs.items()},
              'nativeDependencies': dependency_proofs,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {row['symbol']: row['target'] for entry in matches for row in entry['relocations']},
              'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'ordinarySceneReachabilityCertified': False}
    write_json(REPORT, result)
    print(json.dumps({'functions': len(matches), 'bytes': sum(entry['bytes'] for entry in matches),
                      'executions': sum(entry['oracle']['executions'] for entry in matches),
                      'report': str(REPORT.relative_to(ROOT))}))


if __name__ == '__main__':
    run()
