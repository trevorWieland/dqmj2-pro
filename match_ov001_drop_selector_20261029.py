import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_drop_fixture_20261029 import execute, vectors, ADDRESS
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = 'src/overlays/ov001_20261029_drop_selector_2982dc0eb075.c'
WORK = ROOT / 'work/ov001-drop-selector/20261029'
REPORT = ROOT / 'evidence/matches/ov001-20261029-drop-selector01.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'compiler'
    records, code = compiler.compare(ROOT / SOURCE, 'ov001', '2', 'off', True)
    if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Frozen drop selector no longer matches every native byte')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    original = overlay[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + entry['bytes']]
    results, dependencies = [], set()
    for vector in vectors():
        native = execute(main, overlay, original, vector)
        rebuilt = execute(main, overlay, linked, vector)
        if native != rebuilt:
            raise ValueError('Native/source drop-selector registers, RAM or traces differ')
        results.append(native)
        dependencies.update(tuple(row) for row in native['nativeEntries'] if int(row[0], 0) != ADDRESS)
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=entry['bytes'], justifiedAssemblyBytes=0,
                 nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 oracle={'vectors': len(results), 'executions': len(results) * 2,
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'nativeCalleesExecuted': True, 'hostCalleeStubs': False, 'nativeGameplayStubs': 0,
                         'instructionBound': 20000, 'independentCandidateOrderingTraitRateRngDrawAndResultModel': True,
                         'wholeMappedRamAndStackCompared': True, 'results': results,
                         'limitations': ['Synthetic component states do not establish scene reachability or current/future game RNG state',
                                         'Mode and0x20000 flag retain address-qualified behavior without a scene-specific semantic label',
                                         'Traits other than0x36, malformed pointers, arbitrary aliasing and concurrent mutation are unsupported',
                                         'Original native dependency bodies provide zero additional reconstructed-source credit']})
    native_dependencies = []
    for address, size, module, mode in sorted(dependencies):
        raw, base = (main, 0x02000000) if module == 'main' else (overlay, 0x021D7240)
        offset = int(address, 0) - base
        native_dependencies.append({'module': module, 'processor': 'arm9', 'address': address, 'mode': mode,
                                    'bytes': size, 'spanSha256': compiler.sha(raw[offset:offset + size]), 'additionalSourceCredit': 0})
    paths = [Path(__file__).name, 'ov001_drop_fixture_20261029.py', 'ov001_award_fixture_20261029.py',
             'ov001_award_cases_20261029.py', 'config/arm9/symbols.txt', 'config/arm9/overlays/ov001/symbols.txt']
    result = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {SOURCE: sha256(ROOT / SOURCE)}, 'nativeDependencies': native_dependencies,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in paths],
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']},
              'wholeModuleLinked': False, 'sourceReconstructionComplete': False, 'ordinarySceneReachabilityCertified': False}
    write_json(REPORT, result)
    print(json.dumps({'functions': 1, 'bytes': entry['bytes'], 'executions': len(results) * 2,
                      'nativeRngDraws': sum(len(row['independentDraws']) for row in results), 'report': str(REPORT.relative_to(ROOT))}))


if __name__ == '__main__':
    run()
